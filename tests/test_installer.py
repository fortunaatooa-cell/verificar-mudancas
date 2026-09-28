import tempfile
import unittest
from pathlib import Path

from scripts.install import install

ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def test_full_generic_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"; target.mkdir(); operations = install(ROOT, target, "generic", "full")
            self.assertTrue(operations); self.assertTrue((target / ".agents/skills/verificar-mudancas/SKILL.md").is_file()); self.assertTrue((target / ".agents/skills/investigar/SKILL.md").is_file()); self.assertTrue((target / ".agents/rules/evidence-first.md").is_file()); self.assertTrue((target / ".verificar-mudancas/scripts/run_hook.py").is_file()); self.assertTrue((target / ".verificar-mudancas/scripts/create_regression_eval.py").is_file()); self.assertTrue((target / ".verificar-mudancas/adapter/adapter.json").is_file()); self.assertTrue((target / "memory/project").is_dir()); self.assertTrue((target / "memory/index/index.json").is_file())

    def test_existing_file_is_preserved_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"; skill = target / ".agents/skills/verificar-mudancas/SKILL.md"; skill.parent.mkdir(parents=True); skill.write_text("local", encoding="utf-8"); install(ROOT, target, "generic", "skill", force=False); self.assertEqual(skill.read_text(encoding="utf-8"), "local")


if __name__ == "__main__": unittest.main()
