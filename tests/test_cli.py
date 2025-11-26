import subprocess
import sys


def test_cli_run_flag():
    result = subprocess.run(
        [sys.executable, "main.py", "--run"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
