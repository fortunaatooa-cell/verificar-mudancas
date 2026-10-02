"""Tests for the bank-pilot readiness gate."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_pilot_readiness import REQUIRED, check


class PilotReadinessTests(unittest.TestCase):
    def test_pending_is_blocked_and_complete_record_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pilot.json"
            payload = {
                "questions": [
                    {
                        "id": qid,
                        "answer": "pending",
                        "evidence": "",
                        "responded_by": "",
                        "responded_at": "",
                    }
                    for qid in sorted(REQUIRED)
                ],
                "security_approval": {
                    "status": "pending",
                    "evidence": "",
                    "approved_by": "",
                    "approved_at": "",
                },
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertTrue(check(path))

            for item in payload["questions"]:
                item.update(
                    answer="registrado",
                    evidence="registro-autorizado",
                    responded_by="revisor",
                    responded_at="2026-10-02",
                )
            payload["security_approval"] = {
                "status": "approved",
                "evidence": "registro-autorizado",
                "approved_by": "seguranca",
                "approved_at": "2026-10-02",
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(check(path), [])


if __name__ == "__main__":
    unittest.main()
