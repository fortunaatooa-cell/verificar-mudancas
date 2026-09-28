"""Regression checks for the agentic v1.5 validator."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_agentic import validate


ROOT = Path(__file__).resolve().parents[1]


class ValidateAgenticTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="validate-agentic-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(
            ROOT, self.root,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"),
        )

    def test_current_repository_is_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_agent_is_rejected(self):
        (self.root / ".agents/agents/investigador.md").unlink()
        errors = validate(self.root)
        self.assertTrue(any("agente ausente" in error for error in errors), errors)

    def test_missing_portuguese_command_is_rejected(self):
        (self.root / ".agents/commands/portao-qualidade.md").unlink()
        errors = validate(self.root)
        self.assertTrue(any("comando ausente" in error for error in errors), errors)

    def test_invalid_schema_is_rejected(self):
        path = self.root / "schemas/task.schema.json"
        path.write_text("[]", encoding="utf-8")
        errors = validate(self.root)
        self.assertTrue(any("schema inválido" in error for error in errors), errors)

    def test_agentic_oracle_must_match_cases(self):
        path = self.root / "evals/agentic/oracle.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["oracles"].pop()
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = validate(self.root)
        self.assertTrue(any("oracle correspondente" in error for error in errors), errors)

    def test_required_agentic_case_set_is_fixed(self):
        path = self.root / "evals/agentic/cases.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["cases"].pop()
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = validate(self.root)
        self.assertTrue(any("conjunto de casos" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
