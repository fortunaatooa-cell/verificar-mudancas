import sys
import tempfile
import unittest
from pathlib import Path

from scripts.quality_gate import run_gate


class QualityGateTests(unittest.TestCase):
    def test_plan_does_not_execute(self):
        checks = [{"name": "ok", "command": [sys.executable, "-c", "raise SystemExit(9)"], "required": True}]
        result = run_gate(Path("."), checks, execute=False)
        self.assertEqual(result["overall"], "PARTIAL")
        self.assertFalse(result["executed"])

    def test_required_success_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            checks = [{"name": "ok", "command": [sys.executable, "-c", "print('ok')"], "required": True}]
            result = run_gate(Path(tmp), checks, execute=True)
        self.assertEqual(result["overall"], "PASS")

    def test_required_failure_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            checks = [{"name": "fail", "command": [sys.executable, "-c", "raise SystemExit(2)"], "required": True}]
            result = run_gate(Path(tmp), checks, execute=True)
        self.assertEqual(result["overall"], "FAIL")


if __name__ == "__main__":
    unittest.main()
