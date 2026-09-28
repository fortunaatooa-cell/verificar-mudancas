import tempfile
import unittest
from pathlib import Path

from scripts.run_hook import evaluate


class HookTests(unittest.TestCase):
    def test_high_risk_pre_edit_blocks_missing_controls(self):
        result = evaluate("pre-edit", {"risk": "HIGH", "acceptance": []}, Path("."))
        self.assertTrue(result["block"])
        self.assertEqual(result["status"], "BLOCKED")

    def test_investigation_only_blocks_edit(self):
        result = evaluate("pre-edit", {"risk": "LOW", "mode": "investigation-only", "acceptance": ["entender causa"], "hypothesis": "x"}, Path("."))
        self.assertTrue(result["block"])

    def test_low_risk_pre_edit_can_pass(self):
        result = evaluate("pre-edit", {"risk": "LOW", "acceptance": ["teste passa"], "hypothesis": "causa provável"}, Path("."))
        self.assertFalse(result["block"])
        self.assertEqual(result["status"], "PASS")

    def test_pre_finish_blocks_unverified_claim(self):
        result = evaluate("pre-finish", {"risk": "MEDIUM", "claims": [{"text": "corrigido", "evidence": []}], "material_change": True, "verified_after_last_change": False}, Path("."))
        self.assertTrue(result["block"])
        self.assertEqual(result["status"], "VERIFICATION_INCOMPLETE")

    def test_post_edit_classifies_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = evaluate("post-edit", {"changed_files": ["src/AuthController.java", "infra/main.tf"]}, Path(tmp))
        self.assertIn("api/contrato", result["details"]["boundaries"])
        self.assertIn("infra/runtime", result["details"]["boundaries"])


if __name__ == "__main__":
    unittest.main()
