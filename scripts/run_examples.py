"""Run every examples/*/check_*.py self-check script.

Install each example's requirements.txt first. Exits non-zero on any failure.
SPDX-License-Identifier: MIT
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    scripts = sorted((ROOT / "examples").glob("*/check_*.py"))
    if not scripts:
        raise SystemExit("No examples/*/check_*.py scripts found.")
    failed = []
    for script in scripts:
        relative = script.relative_to(ROOT)
        grouped = "GITHUB_ACTIONS" in os.environ
        print(f"::group::{relative}" if grouped else f"== {relative}", flush=True)
        result = subprocess.run([sys.executable, str(relative)], cwd=ROOT)
        if grouped:
            print("::endgroup::", flush=True)
        if result.returncode:
            failed.append(str(relative))
    if failed:
        raise SystemExit("Failed examples: " + ", ".join(failed))
    print(f"Ran {len(scripts)} example checks: passed")


if __name__ == "__main__":
    main()
