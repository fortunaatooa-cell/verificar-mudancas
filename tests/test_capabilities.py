import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.detect_capabilities import detect

ROOT = Path(__file__).resolve().parents[1]


class CapabilityTests(unittest.TestCase):
    def test_generic_resolves_and_keeps_fallback(self):
        with tempfile.TemporaryDirectory() as tmp: result = detect(Path(tmp), ROOT / "adapters/generic")
        self.assertEqual(result["adapter"], "generic"); self.assertIn("fallback", result); self.assertIn("external_tools", result["resolved"]); self.assertIn("vision_input", result["resolved"]); self.assertIn("visual_generation", result["resolved"])

    def test_runtime_env_can_confirm_agentic_and_visual_capabilities(self):
        env = {"VM_CAP_SUBAGENTS":"true","VM_CAP_EXTERNAL_TOOLS":"true","VM_CAP_VISION":"true","VM_CAP_VISUAL_GENERATION":"false"}
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, env): result = detect(Path(tmp), ROOT / "adapters/codex")
        self.assertEqual(result["resolved"]["subagents"], "available"); self.assertEqual(result["resolved"]["external_tools"], "available"); self.assertEqual(result["resolved"]["vision_input"], "available"); self.assertEqual(result["resolved"]["visual_generation"], "unavailable")


if __name__ == "__main__": unittest.main()
