import json
import tempfile
import unittest
from pathlib import Path

from scripts.memory_store import add, search, validate


class MemoryStoreTests(unittest.TestCase):
    def _lesson(self):
        return {
            "id": "memory-oom-001",
            "date": "2026-09-28",
            "kind": "lesson",
            "context": {"stack": ["java", "container"]},
            "symptom": "deploy sem memória",
            "useful_evidence": ["limite do container"],
            "root_cause": "limite externo",
            "wrong_paths": ["assumir jar igual RAM"],
            "solution": "medir a fronteira correta",
            "verification": ["deploy controlado"],
            "generalizable_learning": "distinguir artifact size de runtime memory",
            "privacy": {"sanitized": True},
        }

    def test_add_search_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "lesson.json"
            source.write_text(json.dumps(self._lesson()), encoding="utf-8")
            destination = add(root, source)
            self.assertTrue(destination.is_file())
            self.assertEqual(validate(root), [])
            results = search(root, "runtime memory container")
            self.assertEqual(results[0]["id"], "memory-oom-001")

    def test_rejects_unsanitized_secret_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = self._lesson()
            doc["token"] = "valor-real"
            source = root / "bad.json"
            source.write_text(json.dumps(doc), encoding="utf-8")
            with self.assertRaises(ValueError):
                add(root, source)


if __name__ == "__main__":
    unittest.main()
