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
            "consultation-brief.md",
            "reporting-protocol.md",
            "broad-symbolic-analysis.md",
            "domain-adapters.md",
            "finance-adapter.md",
            "business-adapter.md",
            "brand-adapter.md",
            "career-adapter.md",
            "relationship-adapter.md",
            "product-adapter.md",
            "learning-adapter.md",
            "wellbeing-adapter.md",
            "legal-adjacent-adapter.md",
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
            "ganzhi.py",
            "annual_afflictions.py",
            "create_brief.py",
            "generate_report.py",
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

    def test_core_chinese_terms_are_readable(self):
        reference_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (SKILL / "references").glob("*.md")
        )

        for term in ["风水", "气", "阴阳", "五行", "八卦", "甲", "辰", "趋吉避凶"]:
            with self.subTest(term=term):
                self.assertIn(term, reference_text)

    def test_broad_symbolic_protocol_covers_non_spatial_readings(self):
        protocol = (SKILL / "references" / "broad-symbolic-analysis.md").read_text(
            encoding="utf-8"
        )

        for phrase in ["观气", "取象", "辨势", "吉凶", "生平", "金融"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, protocol)

    def test_multi_domain_sample_reports_exist_and_are_documented(self):
        expected = {
            "sample-finance-report.md": "Domain: finance",
            "sample-life-omen-report.md": "Domain: life_omen",
            "sample-product-report.md": "Domain: product",
            "sample-floorplan-report.md": "Domain: space",
        }
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for filename, marker in expected.items():
            with self.subTest(filename=filename):
                path = SKILL / "assets" / filename
                self.assertTrue(path.exists())
                text = path.read_text(encoding="utf-8")
                self.assertIn(marker, text)
                self.assertIn("FengShui Master Consultation Report", text)
                self.assertIn(filename, readme)


if __name__ == "__main__":
    unittest.main()
