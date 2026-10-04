"""Diagnostic AD-15/16 run; never certifies unproven hardware limits."""

import json, os, platform, socket, subprocess, sys, tempfile, threading, time
from pathlib import Path
import psutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "qa" / "measurements.json"


class ResourceCounters:
    """Capture endpoint counters and disclose incomplete process lifetimes."""

    def __init__(self, roots):
        self.roots = roots
        self.cpu = {}
        self.rss = []
        self.gaps = {
            "started_after_initial": [],
            "missing_at_final": [],
            "read_errors": [],
        }

    def processes(self):
        processes = {}
        for root in self.roots:
            try:
                parent = psutil.Process(root)
                for proc in [parent, *parent.children(recursive=True)]:
                    processes[(proc.pid, proc.create_time())] = proc
            except psutil.Error as error:
                self.gaps["read_errors"].append(
                    {"pid": root, "error": type(error).__name__}
                )
        return processes

    def capture(self, phase):
        total = 0
        seen = set()
        for key, proc in self.processes().items():
            try:
                total += proc.memory_info().rss
                now = sum(proc.cpu_times()[:2])
                seen.add(key)
                if key not in self.cpu:
                    self.cpu[key] = (now, now)
                    if phase != "initial":
                        self.gaps["started_after_initial"].append(
                            {
                                "pid": key[0],
                                "created_at": key[1],
                                "unobserved_initial_cpu_seconds": now,
                            }
                        )
                else:
                    first, _last = self.cpu[key]
                    self.cpu[key] = (first, now)
            except psutil.Error as error:
                self.gaps["read_errors"].append(
                    {"pid": key[0], "phase": phase, "error": type(error).__name__}
                )
        if phase == "final":
            self.gaps["missing_at_final"] = [
                {"pid": key[0], "created_at": key[1]}
                for key in self.cpu
                if key not in seen
            ]
        self.rss.append(total)

    def cpu_seconds(self):
        return sum(last - first for first, last in self.cpu.values())


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mira-quality-") as scratch:
        env = {**os.environ, "MIRA_DB_PATH": str(Path(scratch) / "quality.sqlite3")}

        def command(*args):
            return subprocess.run(
                [sys.executable, *args],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )

        command("manage.py", "migrate", "--noinput")
        command(
            "manage.py",
            "shell",
            "-c",
            "from dataclasses import replace; from mira.infrastructure.controlled_cases import CONTROLLED_CASES; from mira.infrastructure.review_store import seed_case; base=CONTROLLED_CASES[1]; [seed_case(replace(base,case_id=f'QA-{i:03d}',evidence=(base.evidence[0],base.evidence[1],base.evidence[0]))) for i in range(100)]",
        )
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        server = subprocess.Popen(
            [
                sys.executable,
                "manage.py",
                "runserver",
                f"127.0.0.1:{port}",
                "--noreload",
            ],
            cwd=ROOT,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        base = f"http://127.0.0.1:{port}"
        import urllib.request

        for _ in range(100):
            try:
                urllib.request.urlopen(base + "/bandeja/", timeout=0.5).close()
                break
            except Exception:
                time.sleep(0.1)
        stop = threading.Event()
        counters = None

        def sample():
            while not stop.wait(0.05):
                counters.capture("sample")

        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                driver_pid = pw._impl_obj._connection._transport._proc.pid
                counters = ResourceCounters([server.pid, driver_pid])
                page = browser.new_page()
                times = []
                for i in range(35):
                    start = time.perf_counter()
                    page.goto(base + "/bandeja/")
                    page.get_by_role("link", name=f"QA-{i:03d}", exact=True).click()
                    page.locator("h1").wait_for()
                    if i >= 5:
                        times.append(time.perf_counter() - start)
                sampler = threading.Thread(target=sample, daemon=True)
                start = time.perf_counter()
                counters.capture("initial")
                sampler.start()
                for i in range(30):
                    page.goto(base + f"/casos/QA-{i:03d}/")
                    page.locator("[name=action][value=request_info]").check()
                    page.locator(
                        ".decision-form:has([name=action]) [name=reason]"
                    ).select_option("information_incomplete")
                    page.get_by_role("button", name="Registrar decisión").click()
                    assert "ESPERANDO ANTECEDENTES" in page.locator("main").inner_text()
                stop.set()
                sampler.join()
                counters.capture("final")
                elapsed = time.perf_counter() - start
                browser.close()
            ordered = sorted(times)
            p95 = ordered[28]
            revision = subprocess.run(
                ["git", "-c", f"safe.directory={ROOT.as_posix()}", "rev-parse", "HEAD"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            ).stdout.strip()
            result = {
                "revision_at_run": revision,
                "platform": platform.platform(),
                "python": platform.python_version(),
                "cpu_logical": psutil.cpu_count(),
                "memory_bytes": psutil.virtual_memory().total,
                "hardware_ad15_accredited": False,
                "verdict": "DIAGNÓSTICO; no acredita AD-15",
                "cases": 100,
                "evidence_per_case": 3,
                "warmups": 5,
                "samples_seconds": times,
                "p95_seconds": p95,
                "p95_threshold_seconds": 2,
                "p95_observed_pass": p95 <= 2,
                "reviews": 30,
                "sample_interval_seconds": 0.05,
                "resource_samples": len(counters.rss),
                "rss_max_bytes": max(counters.rss),
                "cpu_average_cores": counters.cpu_seconds() / elapsed,
                "cpu_counter_gaps": counters.gaps,
                "cpu_counter_method": "Initial counters captured synchronously before workload; final counters after workload, before browser shutdown. Missing lifecycle counters explicitly disclosed; CPU may be underestimated when gaps exist",
                "rss_threshold_bytes": 1073741824,
                "cpu_threshold_cores": 1,
                "resource_duration_seconds": elapsed,
                "process_roots": "Django y driver Playwright con árboles Chromium; sin proceso de medición",
                "controlled_clock": "2026-10-06T12:00:00 America/Santiago",
            }
            OUTPUT.write_text(
                json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(json.dumps(result, ensure_ascii=False))
        finally:
            stop.set()
            server.terminate()
            server.wait(timeout=15)


if __name__ == "__main__":
    main()
