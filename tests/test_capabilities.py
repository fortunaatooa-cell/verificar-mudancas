import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.detect_capabilities import detect

ROOT = Path(__file__).resolve().parents[1]


class CapabilityTests(unittest.TestCase):
    def test_generic_resolves_and_keeps_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = detect(Path(tmp), ROOT / "adapters/generic")
        self.assertEqual(result["adapter"], "generic")
        self.assertIn("fallback", result)

    def test_runtime_env_can_confirm_subagents(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"VM_CAP_SUBAGENTS": "true"}):
            result = detect(Path(tmp), ROOT / "adapters/codex")
        self.assertEqual(result["resolved"]["subagents"], "available")


if __name__ == "__main__":
    unittest.main()
