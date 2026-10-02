"""Regression checks for the complete agentic validator."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_agentic import validate

ROOT = Path(__file__).resolve().parents[1]


class ValidateAgenticTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="validate-agentic-"); self.addCleanup(self.temp.cleanup); self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))

    def test_current_repository_is_valid(self): self.assertEqual(validate(self.root), [])

    def test_missing_agent_is_rejected(self):
        (self.root / ".agents/agents/investigador.md").unlink(); self.assertTrue(any("agente ausente" in e for e in validate(self.root)))

    def test_missing_visual_specialist_is_rejected(self):
        (self.root / ".agents/agents/analista-desenhos-tecnicos.md").unlink(); self.assertTrue(any("agente ausente" in e for e in validate(self.root)))

    def test_missing_gameplay_specialist_is_rejected(self):
        (self.root / ".agents/agents/investigador-gameplay.md").unlink(); self.assertTrue(any("agente ausente" in e for e in validate(self.root)))

    def test_missing_game_debug_command_is_rejected(self):
        (self.root / ".agents/commands/depurar-jogo.md").unlink(); self.assertTrue(any("comando ausente" in e for e in validate(self.root)))

    def test_missing_rule_is_rejected(self):
        (self.root / ".agents/rules/visual-evidence.md").unlink(); self.assertTrue(any("regra ausente" in e for e in validate(self.root)))

    def test_missing_hook_is_rejected(self):
        (self.root / ".agents/hooks/pre-finish.md").unlink(); self.assertTrue(any("hook ausente" in e for e in validate(self.root)))

    def test_missing_portuguese_command_is_rejected(self):
        (self.root / ".agents/commands/desenho-tecnico.md").unlink(); self.assertTrue(any("comando ausente" in e for e in validate(self.root)))

    def test_invalid_schema_is_rejected(self):
        path = self.root / "schemas/task.schema.json"; path.write_text("[]", encoding="utf-8"); self.assertTrue(any("schema inválido" in e for e in validate(self.root)))

    def test_invalid_adapter_is_rejected(self):
        path = self.root / "adapters/generic/adapter.json"; data = json.loads(path.read_text(encoding="utf-8")); data["capabilities"]["vision_input"] = "magical"; path.write_text(json.dumps(data), encoding="utf-8"); self.assertTrue(any("capability inválida" in e for e in validate(self.root)))

    def test_agentic_oracle_must_match_cases(self):
        path = self.root / "evals/agentic/oracle.json"; data = json.loads(path.read_text(encoding="utf-8")); data["oracles"].pop(); path.write_text(json.dumps(data), encoding="utf-8"); self.assertTrue(any("oracle correspondente" in e for e in validate(self.root)))

    def test_visual_case_set_is_fixed(self):
        path = self.root / "evals/visual/cases.json"; data = json.loads(path.read_text(encoding="utf-8")); data["cases"].pop(); path.write_text(json.dumps(data), encoding="utf-8"); self.assertTrue(any("visual: conjunto de casos" in e for e in validate(self.root)))


if __name__ == "__main__": unittest.main()
