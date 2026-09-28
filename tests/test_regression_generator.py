import json
import tempfile
import unittest
from pathlib import Path

from scripts.create_regression_eval import create


class RegressionGeneratorTests(unittest.TestCase):
    def test_generates_reviewable_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "lesson.json"
            source.write_text(json.dumps({"id":"lesson-1","kind":"lesson","privacy":{"sanitized":True},"useful_evidence":["limite do container"]}), encoding="utf-8")
            output = create(source, root / "out", "reg-001", "Investigue o OOM", ["medir limite"], ["assumir causa"])
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["status"], "REVIEW_REQUIRED")
            self.assertEqual(data["case"]["id"], "reg-001")

    def test_rejects_unsanitized_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "bad.json"
            source.write_text(json.dumps({"id":"lesson-2","kind":"lesson","privacy":{"sanitized":False}}), encoding="utf-8")
            with self.assertRaises(ValueError):
                create(source, root / "out", "reg-002", "x", ["y"], ["z"])


if __name__ == "__main__":
    unittest.main()
