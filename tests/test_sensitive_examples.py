"""Checks for the public-content sensitive-data scanner."""

import tempfile
import unittest
from pathlib import Path

from scripts.check_sensitive_examples import scan_paths


class SensitiveExamplesTests(unittest.TestCase):
    def test_synthetic_cpf_is_detected_and_removal_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "evals"
            folder.mkdir()
            sample = folder / "case.md"
            sample.write_text("cpf de teste: 123.456.789-00\n", encoding="utf-8")
            self.assertTrue(scan_paths(root, ["evals"]))
            sample.write_text("identificador pessoal: <redacted>\n", encoding="utf-8")
            self.assertEqual(scan_paths(root, ["evals"]), [])


if __name__ == "__main__":
    unittest.main()
