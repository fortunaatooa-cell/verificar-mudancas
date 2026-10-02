"""Contract tests for explicit human approval on HIGH/CRITICAL outputs."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RegulatedProfileContractTests(unittest.TestCase):
    def test_reference_requires_explicit_true_field(self):
        change = (ROOT / ".agents/skills/verificar-mudancas/references/change-evidence.md").read_text(encoding="utf-8")
        regulated = (ROOT / ".agents/skills/verificar-mudancas/references/regulated-profile.md").read_text(encoding="utf-8")
        self.assertIn("aprovacao_humana_necessaria=true", change)
        self.assertIn("aprovacao_humana_necessaria=true", regulated)

    def test_regulated_oracle_fails_contract_when_field_is_omitted(self):
        payload = json.loads((ROOT / "evals/profiles/regulated-oracle.json").read_text(encoding="utf-8"))
        case = next(item for item in payload["oracles"] if item["id"] == "regulated-human-approval")
        self.assertTrue(any("aprovacao_humana_necessaria=true" in item for item in case["expected"]))
        self.assertTrue(any("Omitir" in item and "aprovacao_humana_necessaria=true" in item for item in case["forbidden"]))


if __name__ == "__main__":
    unittest.main()
