"""Unit tests for the spec-driven A/B semantics."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.analyze_ab_results import determine_winner, normalized_score
from scripts.run_agent_eval import detect_skill_read


class ABSpecTests(unittest.TestCase):
    def test_detect_skill_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            path.write_text(
                json.dumps({
                    "type": "item.completed",
                    "item": {
                        "type": "file_read",
                        "path": "C:\\x\\.agents\\skills\\verificar-mudancas\\SKILL.md",
                    },
                }) + "\n",
                encoding="utf-8",
            )
            self.assertTrue(detect_skill_read(path))
            path.write_text(
                json.dumps({"type": "item.completed", "item": {"type": "agent_message"}}) + "\n",
                encoding="utf-8",
            )
            self.assertFalse(detect_skill_read(path))

    def test_fixed_denominator_keeps_applicable_na(self):
        score, missing = normalized_score(
            {"causa": "2", "experimento": "N/A"},
            ["causa", "experimento"],
        )
        self.assertEqual(score, 0.5)
        self.assertEqual(missing, ["experimento"])

    def test_effect_and_violations_gate(self):
        self.assertEqual(determine_winner(0.01, 0.15, 0, 0, False), "tie")
        self.assertEqual(determine_winner(0.20, 0.15, 0, 1, False), "baseline")
        self.assertEqual(determine_winner(0.20, 0.15, 0, 0, True), "baseline")
        self.assertEqual(determine_winner(0.20, 0.15, 1, 1, False), "with_skill")


if __name__ == "__main__":
    unittest.main()
