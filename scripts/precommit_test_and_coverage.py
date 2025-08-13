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
        ]
    )

    if result.returncode != 0:
        sys.exit(result.returncode)

    # After successful test run, check coverage
    # Run pytest again with coverage output captured
    coverage_result = subprocess.run(
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

    output = coverage_result.stdout
    for line in output.splitlines():
        if "TOTAL" in line and "%" in line:
            percent = float(line.split()[-1].replace("%", ""))
            # Always generate HTML report
            subprocess.run([sys.executable, "-m", "coverage", "html"])
            if percent < MIN_COVERAGE:
                print(f"Coverage {percent}% below required. Opening HTML report...")
                import webbrowser
                import os

                html_report = os.path.abspath("htmlcov/index.html")
                webbrowser.open(f"file://{html_report}")
                sys.exit(1)
            else:
                print(f"Coverage {percent}% meets requirement.")
                sys.exit(0)

    print("Could not determine test coverage.")
    sys.exit(1)


if __name__ == "__main__":
    main()
