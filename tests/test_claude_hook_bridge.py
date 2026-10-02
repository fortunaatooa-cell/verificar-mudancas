"""Tests for Claude Code native hook bridge."""

import os
import unittest
from unittest.mock import patch

from scripts.claude_hook_bridge import pre_tool


class ClaudeHookBridgeTests(unittest.TestCase):
    def test_safe_bash_is_allowed(self):
        blocked, reason = pre_tool({
            "tool_name": "Bash",
            "tool_input": {"command": "python -m unittest"},
        })
        self.assertFalse(blocked)
        self.assertEqual(reason, "")

    def test_destructive_bash_is_blocked_without_approval(self):
        blocked, reason = pre_tool({
            "tool_name": "Bash",
            "tool_input": {"command": "git reset --hard HEAD~1"},
        })
        self.assertTrue(blocked)
        self.assertIn("aprovação humana", reason)

    def test_destructive_bash_can_proceed_after_explicit_approval(self):
        with patch.dict(os.environ, {"VM_HUMAN_APPROVED": "true"}):
            blocked, reason = pre_tool({
                "tool_name": "Bash",
                "tool_input": {"command": "git reset --hard HEAD~1"},
            })
        self.assertFalse(blocked)
        self.assertIn("autorizado", reason)

    def test_investigation_only_blocks_edit(self):
        with patch.dict(os.environ, {"VM_MODE": "investigation-only"}):
            blocked, reason = pre_tool({
                "tool_name": "Edit",
                "tool_input": {"file_path": "app.py"},
            })
        self.assertTrue(blocked)
        self.assertIn("investigation-only", reason)


if __name__ == "__main__":
    unittest.main()
