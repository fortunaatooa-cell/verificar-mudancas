"""Regression checks for the repository validator using disposable copies."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_repo import validate


ROOT = Path(__file__).resolve().parents[1]


class ValidateRepoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="validate-skill-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(
            ROOT, self.root,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"),
        )
        self.skill = self.root / ".agents/skills/verificar-mudancas/SKILL.md"

    def header(self, text):
        body = self.skill.read_text(encoding="utf-8").split("---", 2)[2]
        self.skill.write_text(f"---\n{text}\n---{body}", encoding="utf-8")

    def case_field(self, field, value):
        path = self.root / "evals/cases.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["cases"][0][field] = value
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_current_repository_is_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_crlf_skill_is_accepted(self):
        text = self.skill.read_text(encoding="utf-8")
        self.skill.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual(validate(self.root), [])

    def test_malformed_yaml_is_rejected(self):
        self.header("name: verificar-mudancas\ndescription: [unterminated")
        errors = validate(self.root)
        self.assertTrue(any("YAML" in error for error in errors), errors)

    def test_yaml_mapping_is_required(self):
        for header in ("", "- name: verificar-mudancas", "null", "42"):
            with self.subTest(header=header):
                self.header(header)
                self.assertTrue(validate(self.root))

    def test_description_must_be_nonempty_text(self):
        for value in ('""', '"   "', "null", "true", "42", "[text]", "{text: value}"):
            with self.subTest(value=value):
                self.header(f"name: verificar-mudancas\ndescription: {value}")
                self.assertTrue(validate(self.root))

    def test_quoted_and_folded_yaml_are_supported(self):
        for description in ('"Investigar: causa e efeito"', ">\n  Investigar causas\n  e verificar mudanças"):
            with self.subTest(description=description):
                self.header(f'name: "verificar-mudancas"\ndescription: {description}')
                self.assertEqual(validate(self.root), [])

    def test_duplicate_yaml_keys_are_rejected(self):
        self.header(
            "name: verificar-mudancas\ndescription: Primeira descrição\n"
            "description: Outra descrição"
        )
        self.assertTrue(validate(self.root))

    def test_invalid_domains_are_reported_without_crashing(self):
        for value in ([], {}, None, 42, ""):
            with self.subTest(value=value):
                self.case_field("domain", value)
                self.assertTrue(validate(self.root))

    def test_invalid_modes_are_reported_without_crashing(self):
        for value in ([], {}, None, 42, ""):
            with self.subTest(value=value):
                self.case_field("mode", value)
                self.assertTrue(validate(self.root))

    def test_invalid_ids_are_reported_without_crashing(self):
        for value in ([], {}, None, 42, " "):
            with self.subTest(value=value):
                self.case_field("id", value)
                self.assertTrue(validate(self.root))

    def test_missing_reference_is_rejected(self):
        (self.skill.parent / "references/python.md").unlink()
        self.assertTrue(validate(self.root))

    def test_oracle_must_match_cases(self):
        path = self.root / "evals/oracle.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["oracles"].pop()
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(validate(self.root))

    def test_cli_reports_invalid_input_without_traceback(self):
        self.case_field("domain", [])
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts/validate_repo.py"), str(self.root)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERRO:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
