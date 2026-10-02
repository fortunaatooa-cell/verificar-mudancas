"""Ensure committed Claude native surfaces stay generated from portable sources."""

import json
import unittest
from pathlib import Path

from scripts.claude_native import native_files, render_settings

ROOT = Path(__file__).resolve().parents[1]


class ClaudeNativeTests(unittest.TestCase):
    def test_committed_native_files_match_generator(self):
        generated = native_files(ROOT, installed=False)
        self.assertGreater(len(generated), 30)
        for relative, expected in generated.items():
            path = ROOT / relative
            self.assertTrue(path.is_file(), str(relative))
            self.assertEqual(path.read_text(encoding="utf-8"), expected, str(relative))

    def test_installed_settings_point_to_portable_runtime_bridge(self):
        settings = json.loads(
            render_settings(".verificar-mudancas/scripts/claude_hook_bridge.py")
        )
        encoded = json.dumps(settings)
        self.assertIn(".verificar-mudancas/scripts/claude_hook_bridge.py", encoded)
        self.assertIn("PreToolUse", settings["hooks"])


if __name__ == "__main__":
    unittest.main()
