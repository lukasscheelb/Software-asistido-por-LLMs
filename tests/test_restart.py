import os, subprocess, sys
from pathlib import Path


def test_intervention_survives_fresh_process(tmp_path):
    env = {
        **os.environ,
        "MIRA_DB_PATH": str(tmp_path / "restart.sqlite3"),
        "DJANGO_SETTINGS_MODULE": "mira.settings",
    }
    root = Path(__file__).resolve().parents[1]

    def run(*args):
        return subprocess.run(
            [sys.executable, *args],
            cwd=root,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    run("manage.py", "migrate", "--noinput")
    run("manage.py", "load_demo")
    run(
        "manage.py",
        "shell",
        "-c",
        "from mira.composition import register_human_decision; decision,errors=register_human_decision(case_id='CC-F1-04', action_code='approve',reason_code='requirements_met',comment='',expected_case_version=1); assert decision and not errors",
    )
    run(
        "manage.py",
        "shell",
        "-c",
        "from mira.infrastructure.review_store import get_decision,snapshot,history; assert get_decision('CC-F1-04').action=='approve'; assert snapshot('CC-F1-04')[2]['version']=='POL-F4-2026.10'; assert len(history('CC-F1-04'))==1",
    )
