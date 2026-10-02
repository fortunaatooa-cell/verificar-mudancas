import tempfile
import unittest
from pathlib import Path

from scripts.install import install

ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def test_full_generic_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"; target.mkdir(); operations = install(ROOT, target, "generic", "full")
            self.assertTrue(operations); self.assertTrue((target / ".agents/skills/verificar-mudancas/SKILL.md").is_file()); self.assertTrue((target / ".agents/skills/investigar/SKILL.md").is_file()); self.assertTrue((target / ".agents/skills/desenho-tecnico/SKILL.md").is_file()); self.assertTrue((target / ".agents/agents/analista-desenhos-tecnicos.md").is_file()); self.assertTrue((target / ".agents/rules/visual-evidence.md").is_file()); self.assertTrue((target / ".verificar-mudancas/scripts/run_hook.py").is_file()); self.assertTrue((target / ".verificar-mudancas/scripts/create_regression_eval.py").is_file()); self.assertTrue((target / ".verificar-mudancas/adapter/adapter.json").is_file()); self.assertTrue((target / "memory/project").is_dir()); self.assertTrue((target / "memory/index/index.json").is_file())

    def test_full_claude_install_adds_native_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"
            target.mkdir()
            operations = install(ROOT, target, "claude", "full")
            self.assertTrue(operations)
            self.assertTrue((target / "CLAUDE.md").is_file())
            self.assertTrue((target / ".claude/settings.json").is_file())
            self.assertTrue((target / ".claude/skills/verificar-mudancas/SKILL.md").is_file())
            self.assertTrue((target / ".claude/skills/investigar/SKILL.md").is_file())
            self.assertTrue((target / ".claude/skills/depurar-jogo/SKILL.md").is_file())
            self.assertTrue((target / ".claude/agents/investigador.md").is_file())
            self.assertTrue((target / ".claude/agents/investigador-gameplay.md").is_file())
            self.assertTrue((target / ".claude/rules/evidence-first.md").is_file())
            self.assertTrue((target / ".verificar-mudancas/scripts/claude_hook_bridge.py").is_file())
            settings = (target / ".claude/settings.json").read_text(encoding="utf-8")
            self.assertIn(".verificar-mudancas/scripts/claude_hook_bridge.py", settings)
            self.assertIn("PreToolUse", settings)

    def test_claude_existing_claude_md_is_preserved_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"
            target.mkdir()
            claude = target / "CLAUDE.md"
            claude.write_text("local instructions", encoding="utf-8")
            install(ROOT, target, "claude", "full", force=False)
            self.assertEqual(claude.read_text(encoding="utf-8"), "local instructions")

    def test_claude_skill_mode_exposes_native_core_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"
            target.mkdir()
            install(ROOT, target, "claude", "skill")
            self.assertTrue((target / ".claude/skills/verificar-mudancas/SKILL.md").is_file())
            self.assertFalse((target / "CLAUDE.md").exists())
            self.assertFalse((target / ".claude/agents/investigador.md").exists())

    def test_existing_file_is_preserved_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"; skill = target / ".agents/skills/verificar-mudancas/SKILL.md"; skill.parent.mkdir(parents=True); skill.write_text("local", encoding="utf-8"); install(ROOT, target, "generic", "skill", force=False); self.assertEqual(skill.read_text(encoding="utf-8"), "local")


if __name__ == "__main__": unittest.main()
