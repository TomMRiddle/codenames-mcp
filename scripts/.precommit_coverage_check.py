"""
This script checks test coverage for pre-commit. It is not a test file.
"""

import sys
import subprocess

MIN_COVERAGE = 85  # Set your required minimum coverage percentage


def main():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--cov=src",
            "--cov=examples",
            "--cov-report=term",
        ],
        capture_output=True,
        text=True,
    )

    output = result.stdout

    for line in output.splitlines():
        if "TOTAL" in line and "%" in line:
            percent = float(line.split()[-1].replace("%", ""))
            if percent < MIN_COVERAGE:
                print(f"Coverage {percent}% below required.")
                sys.exit(1)
            else:
                print(f"Coverage {percent}% meets requirement.")
                sys.exit(0)

    print("Could not determine test coverage.")
    sys.exit(1)


if __name__ == "__main__":
    main()
