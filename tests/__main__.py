"""
Allows contributors to run tests on their machine (and in GitHub actions / Travis CI)
"""
import os
import subprocess  # nosec: B404
import sys

import coverage


def main() -> int:
    """
    Main test method, callable with `python -m tests`

    1. Calls a subprocess for `coverage run`
    2. Programmatically invokes coverage.report()
    """

    cmd = "coverage run -m pytest -v -s -p no:cacheprovider tests/"
    print(cmd)
    subprocess.call(cmd.split(), shell=False)  # nosec: B603

    print("\ncoverage report -m --skip-empty")
    cov = coverage.Coverage()
    cov.load()
    cov.report(show_missing=True, skip_empty=True)

    # Try to clean up
    try:
        os.remove(".coverage")
    except (FileNotFoundError, PermissionError) as error:
        print("WARN: failed to remove `.coverage`, %s" % repr(error))

    return 0


if __name__ == "__main__":
    sys.exit(main())
