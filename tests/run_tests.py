"""Run the whole automated test suite and save the results.

From the project root, with the virtual environment active:
    python tests/run_tests.py

Results are printed and written to docs/test_results.txt.
Optional: --json PATH also writes machine-readable results.
The tests use temporary databases, so your real data is never touched.
"""
import io
import json
import platform
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


class CollectingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outcomes = {}

    def _record(self, test, outcome):
        self.outcomes[test.id()] = (test.shortDescription() or test.id(), outcome)

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record(test, "PASS")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record(test, "FAIL")

    def addError(self, test, err):
        super().addError(test, err)
        self._record(test, "ERROR")


def main():
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=CollectingResult)
    result = runner.run(suite)
    body = stream.getvalue()

    header = (
        "Course Content Manager - automated test results\n"
        f"Date: {date.today().isoformat()}\n"
        f"Python: {platform.python_version()} on {platform.system()} {platform.release()}\n"
        "Command: python tests/run_tests.py\n"
        + "-" * 70 + "\n"
    )
    print(header + body)
    out = ROOT / "docs" / "test_results.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text(header + body, encoding="utf-8")

    if "--json" in sys.argv:
        path = Path(sys.argv[sys.argv.index("--json") + 1])
        passed = sum(1 for _, o in result.outcomes.values() if o == "PASS")
        path.write_text(json.dumps({
            "date": date.today().isoformat(),
            "python": platform.python_version(),
            "platform": f"{platform.system()} {platform.release()}",
            "ran": result.testsRun,
            "passed": passed,
            "failed": len(result.failures),
            "errors": len(result.errors),
            "tests": [{"id": k, "description": d, "outcome": o} for k, (d, o) in sorted(result.outcomes.items())],
        }, indent=1), encoding="utf-8")

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
