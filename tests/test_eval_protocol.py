"""Regression tests for the independent oracle-review gate."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.eval_protocol import canonical_sha256, review_template, verify_review


class EvalProtocolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eval-protocol-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cases = self.root / "cases.json"
        self.oracle = self.root / "oracle.json"
        self.review = self.root / "review.json"
        self.cases.write_text(
            '{"version":1,"cases":[{"id":"case-a","domain":"x","mode":"snippet","prompt":"p","evidence":"e"}]}\n',
            encoding="utf-8",
        )
        self.oracle.write_text(
            '{"version":1,"oracles":[{"id":"case-a","expected":["x"],"forbidden":["y"]}]}\n',
            encoding="utf-8",
        )

    def approved_review(self):
        payload = review_template(self.cases, self.oracle, ["case-a"])
        payload.update({
            "reviewer": "second-reviewer",
            "reviewed_at": "2026-10-01T23:00:00-03:00",
            "independent": True,
        })
        payload["reviews"][0]["status"] = "approved"
        payload["reviews"][0]["method"] = "fixture + item-by-item oracle review"
        self.review.write_text(json.dumps(payload), encoding="utf-8")
        return payload

    def test_approved_current_review_passes(self):
        self.approved_review()
        result = verify_review(self.review, self.cases, self.oracle, ["case-a"])
        self.assertTrue(result["verified"])
        self.assertEqual(result["reviewed_case_ids"], ["case-a"])

    def test_stale_oracle_hash_is_rejected(self):
        self.approved_review()
        self.oracle.write_text(self.oracle.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "oracle_sha256"):
            verify_review(self.review, self.cases, self.oracle, ["case-a"])

    def test_missing_independent_review_is_rejected(self):
        payload = review_template(self.cases, self.oracle, ["case-a"])
        self.review.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "independent"):
            verify_review(self.review, self.cases, self.oracle, ["case-a"])

    def test_line_endings_do_not_change_protocol_hash(self):
        lf = self.root / "lf.txt"
        crlf = self.root / "crlf.txt"
        lf.write_bytes(b"a\nb\n")
        crlf.write_bytes(b"a\r\nb\r\n")
        self.assertEqual(canonical_sha256(lf), canonical_sha256(crlf))


if __name__ == "__main__":
    unittest.main()
