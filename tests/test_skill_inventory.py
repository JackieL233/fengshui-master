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
            "classical-source-map.md",
        ]
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        for filename in expected:
            with self.subTest(filename=filename):
                self.assertTrue((SKILL / "references" / filename).exists())
                self.assertIn(f"references/{filename}", skill_text)

    def test_scripts_are_documented(self):
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        for filename in [
            "method_selector.py",
            "bagua_map.py",
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
            "moon_phase.py",
            "solar_terms.py",
        ]:
            with self.subTest(filename=filename):
                self.assertTrue((SKILL / "scripts" / filename).exists())
                self.assertIn(f"scripts/{filename}", skill_text)

    def test_timing_reference_covers_new_and_full_moon(self):
        timing = (SKILL / "references" / "timing-and-date-selection.md").read_text(
            encoding="utf-8"
        )

        for phrase in ["New Moon", "Full Moon", "新月", "满月", "scripts/moon_phase.py"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, timing)

    def test_moon_phase_covers_cross_domain_rhythm(self):
        timing = (SKILL / "references" / "timing-and-date-selection.md").read_text(
            encoding="utf-8"
        )
        adapters = (SKILL / "references" / "domain-adapters.md").read_text(
            encoding="utf-8"
        )

        for phrase in ["Finance", "Product", "Career", "Life pattern", "Moon phase is secondary"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, timing)

        for phrase in ["Moon Phase Across Domains", "Finance", "Product", "New Moon", "Full Moon", "Waning"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, adapters)

    def test_timing_reference_covers_solar_terms(self):
        timing = (SKILL / "references" / "timing-and-date-selection.md").read_text(
            encoding="utf-8"
        )

        for phrase in ["24 Solar Terms", "二十四节气", "立春", "夏至", "冬至", "scripts/solar_terms.py"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, timing)

    def test_foundation_reference_covers_bagua_helper(self):
        foundation = (SKILL / "references" / "foundation.md").read_text(encoding="utf-8")

        for phrase in ["scripts/bagua_map.py", "Compass bagua", "Door-aligned", "life-area symbolism"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, foundation)

    def test_schools_reference_covers_method_selector(self):
        schools = (SKILL / "references" / "schools.md").read_text(encoding="utf-8")

        for phrase in ["scripts/method_selector.py", "recommended method", "required inputs", "silent school mixing"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, schools)

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

    def test_classical_source_map_covers_schools_and_boundaries(self):
        source_map = (SKILL / "references" / "classical-source-map.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        manifest = (ROOT / "portable-skill.json").read_text(encoding="utf-8")

        for phrase in [
            "Zang Shu",
            "葬书",
            "Yijing",
            "Hong Fan",
            "Form School",
            "San He",
            "San Yuan",
            "Xuan Kong",
            "Eight Mansions",
            "Moon phase",
            "Modern cross-domain extension",
            "Do not present modern symbolic adapters as classical doctrine",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, source_map)

        self.assertIn("classical-source-map.md", readme)
        self.assertIn("fengshui-master/references/classical-source-map.md", manifest)

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
