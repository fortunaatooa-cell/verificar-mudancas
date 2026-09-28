import json
import tempfile
import unittest
from pathlib import Path

from scripts.record_run import record


class RecordRunTests(unittest.TestCase):
    def _doc(self):
        return {
            "run_id": "run-001",
            "task_type": "bug",
            "risk": "LOW",
            "selected_agents": ["investigador"],
            "selected_references": [],
            "selected_playbooks": ["bug-fix"],
            "tools_used": [],
            "verification": {},
            "final_status": "PASS",
            "privacy": {"sanitized": True},
        }

    def test_records_sanitized_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "run.json"
            source.write_text(json.dumps(self._doc()), encoding="utf-8")
            output = record(root, source)
            self.assertTrue(output.is_file())

    def test_rejects_unsanitized_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = self._doc()
            doc["privacy"]["sanitized"] = False
            source = root / "run.json"
            source.write_text(json.dumps(doc), encoding="utf-8")
            with self.assertRaises(ValueError):
                record(root, source)


if __name__ == "__main__":
    unittest.main()
