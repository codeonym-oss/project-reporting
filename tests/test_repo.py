"""Repo consistency: the manifests, the skills and the references agree."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).parent.parent


class RepoTest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((REPO / ".claude-plugin/plugin.json").read_text())
        self.portable = json.loads((REPO / "plugin.json").read_text())

    def test_the_listed_skills_are_the_skills(self):
        on_disk = {p.parent.name for p in (REPO / "skills").glob("*/SKILL.md")}
        self.assertEqual({Path(entry).name for entry in self.manifest["skills"]}, on_disk)
        for name in on_disk:
            lines = (REPO / "skills" / name / "SKILL.md").read_text().splitlines()
            self.assertEqual(lines[1], f"name: {name}")
            self.assertTrue(lines[2].startswith("description: "))
            self.assertLess(len(lines), 100)

    def test_versions_agree(self):
        version = (REPO / "VERSION").read_text().strip()
        released = json.loads((REPO / ".release-please-manifest.json").read_text())["."]
        self.assertEqual({self.manifest["version"], self.portable["version"], released}, {version})

    def test_the_manifests_agree(self):
        for field in ("name", "description", "author", "homepage", "repository", "license", "keywords"):
            self.assertEqual(self.portable[field], self.manifest[field], field)
        self.assertTrue((REPO / self.portable["extensions"]["com.openai"]["onboardingSkill"]).is_file())

    def test_named_files_exist(self):
        for path in [*REPO.glob("skills/*/SKILL.md"), *REPO.glob("references/*.md")]:
            text = path.read_text()
            for target in re.findall(r"<skill-dir>/\.\./\.\./([\w./-]+\.(?:md|py))", text):
                self.assertTrue((REPO / target).is_file(), f"{path.name}: {target}")

    def test_the_shipped_template_has_its_limits(self):
        header = (REPO / "templates/client.md").read_text().split("---")[1]
        for limit in ("item-words", "max-items", "glance-lines"):
            self.assertRegex(header, rf"{limit}: \d+")


if __name__ == "__main__":
    unittest.main()
