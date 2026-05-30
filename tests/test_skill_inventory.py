import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "fengshui-master"


class SkillInventoryTest(unittest.TestCase):
    def test_expanded_reference_files_exist_and_are_linked(self):
        expected = [
            "foundation.md",
            "forms-and-environment.md",
            "schools.md",
            "analysis-templates.md",
            "remedies.md",
            "timing-and-date-selection.md",
            "xuan-kong-flying-stars.md",
            "yin-house.md",
            "glossary.md",
            "case-patterns.md",
            "sample-readings.md",
            "domain-adapters.md",
            "finance-adapter.md",
            "life-and-omen-adapter.md",
            "five-phase-domain-map.md",
            "floorplan-schema.md",
            "ethics-and-limits.md",
            "sources.md",
        ]
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        for filename in expected:
            with self.subTest(filename=filename):
                self.assertTrue((SKILL / "references" / filename).exists())
                self.assertIn(f"references/{filename}", skill_text)

    def test_scripts_are_documented(self):
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        for filename in [
            "luopan.py",
            "minggua.py",
            "periods.py",
            "flying_stars.py",
            "domain_router.py",
            "analyze_floorplan.py",
        ]:
            with self.subTest(filename=filename):
                self.assertTrue((SKILL / "scripts" / filename).exists())
                self.assertIn(f"scripts/{filename}", skill_text)

    def test_readme_has_coverage_matrix(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## Coverage Matrix", readme)
        self.assertIn("Fully covered", readme)
        self.assertIn("Partially covered", readme)
        self.assertIn("Not covered", readme)


if __name__ == "__main__":
    unittest.main()
