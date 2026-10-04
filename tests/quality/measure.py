"""Diagnostic AD-15/16 run; never certifies unproven hardware limits."""

import json, os, platform, socket, subprocess, sys, tempfile, threading, time
from pathlib import Path
import psutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "qa" / "measurements.json"


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
        rss = []
        cpu = {}
        stop = threading.Event()
        roots = []

        def sample():
            while not stop.is_set():
                processes = {}
                for root in roots:
                    try:
                        parent = psutil.Process(root)
                        for proc in [parent, *parent.children(recursive=True)]:
                            processes[proc.pid] = proc
                    except psutil.Error:
                        pass
                total = 0
                for pid, proc in processes.items():
                    try:
                        total += proc.memory_info().rss
                        now = sum(proc.cpu_times()[:2])
                        first, last = cpu.get(pid, (now, now))
                        cpu[pid] = (first, now)
                    except psutil.Error:
                        pass
                rss.append(total)
                stop.wait(0.05)

        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                driver_pid = pw._impl_obj._connection._transport._proc.pid
                roots[:] = [server.pid, driver_pid]
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
                sampler.start()
                for i in range(30):
                    page.goto(base + f"/casos/QA-{i:03d}/")
                    page.locator("[name=action][value=request_info]").check()
                    page.locator(
                        ".decision-form:has([name=action]) [name=reason]"
                    ).select_option("information_incomplete")
                    page.get_by_role("button", name="Registrar decisión").click()
                    assert "ESPERANDO ANTECEDENTES" in page.locator("main").inner_text()
                elapsed = time.perf_counter() - start
                stop.set()
                sampler.join()
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
                "resource_samples": len(rss),
                "rss_max_bytes": max(rss),
                "cpu_average_cores": sum(last - first for first, last in cpu.values())
                / elapsed,
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
