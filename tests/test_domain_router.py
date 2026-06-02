import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "domain_router.py"


def run_router(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class DomainRouterTest(unittest.TestCase):
    def test_finance_routes_to_finance_adapter_and_ethics(self):
        data = run_router("Should I buy this stock next month?")

        self.assertEqual(data["domain"], "finance")
        self.assertIn("references/finance-adapter.md", data["references"])
        self.assertIn("references/ethics-and-limits.md", data["references"])
        self.assertIn("financial advice", data["guardrails"][0])

    def test_brand_routes_to_domain_adapter(self):
        data = run_router("Help me choose brand colors and a launch direction")

        self.assertEqual(data["domain"], "brand")
        self.assertIn("references/domain-adapters.md", data["references"])
        self.assertIn("references/brand-adapter.md", data["references"])

    def test_business_routes_to_business_adapter(self):
        data = run_router("Use feng shui to review my business strategy and customer flow")

        self.assertEqual(data["domain"], "business")
        self.assertIn("references/business-adapter.md", data["references"])

    def test_career_routes_to_career_adapter(self):
        data = run_router("Use feng shui to review my career promotion timing")

        self.assertEqual(data["domain"], "career")
        self.assertIn("references/career-adapter.md", data["references"])

    def test_relationship_routes_to_relationship_adapter(self):
        data = run_router("Use feng shui and five phases to improve this relationship conflict")

        self.assertEqual(data["domain"], "relationship")
        self.assertIn("references/relationship-adapter.md", data["references"])

    def test_product_routes_to_product_adapter(self):
        data = run_router("Use feng shui to improve this product onboarding flow")

        self.assertEqual(data["domain"], "product")
        self.assertIn("references/product-adapter.md", data["references"])

    def test_learning_routes_to_learning_adapter(self):
        data = run_router("Use feng shui and five phases to improve my study plan")

        self.assertEqual(data["domain"], "learning")
        self.assertIn("references/learning-adapter.md", data["references"])

    def test_wellbeing_routes_to_wellbeing_adapter(self):
        data = run_router("Use feng shui to improve my sleep and stress")

        self.assertEqual(data["domain"], "wellbeing")
        self.assertIn("references/wellbeing-adapter.md", data["references"])
        self.assertIn("Do not diagnose or treat medical conditions.", data["guardrails"])

    def test_legal_adjacent_routes_to_legal_adapter(self):
        data = run_router("Use feng shui to think about this contract and legal dispute")

        self.assertEqual(data["domain"], "legal_adjacent")
        self.assertIn("references/legal-adjacent-adapter.md", data["references"])
        self.assertIn("Do not provide legal advice.", data["guardrails"])

    def test_space_defaults_to_classic_feng_shui(self):
        data = run_router("Analyze my bedroom layout and mirror placement")

        self.assertEqual(data["domain"], "space")
        self.assertIn("references/analysis-templates.md", data["references"])

    def test_life_omen_routes_to_life_adapter(self):
        data = run_router("Use feng shui and five phases to analyze a person's life, luck, and auspicious risks")

        self.assertEqual(data["domain"], "life_omen")
        self.assertIn("references/life-and-omen-adapter.md", data["references"])
        self.assertIn("references/ethics-and-limits.md", data["references"])

    def test_chinese_life_omen_question_routes_without_spaces(self):
        data = run_router("帮我用风水分析一个人的生平五行吉凶和运势")

        self.assertEqual(data["domain"], "life_omen")
        self.assertIn("references/broad-symbolic-analysis.md", data["references"])
        self.assertIn("references/life-and-omen-adapter.md", data["references"])

    def test_chinese_biography_wealth_career_question_routes_to_life_omen(self):
        data = run_router("用风水五行分析这个人的一生财运事业吉凶")

        self.assertEqual(data["domain"], "life_omen")
        self.assertIn("references/broad-symbolic-analysis.md", data["references"])
        self.assertIn("references/life-and-omen-adapter.md", data["references"])

    def test_chinese_finance_question_routes_without_spaces(self):
        data = run_router("用风水五行分析这个股票投资是否吉利")

        self.assertEqual(data["domain"], "finance")
        self.assertIn("references/finance-adapter.md", data["references"])

    def test_moon_phase_question_routes_to_timing(self):
        data = run_router("Use feng shui to choose between the new moon and full moon for launching this project")

        self.assertEqual(data["domain"], "timing")
        self.assertIn("references/timing-and-date-selection.md", data["references"])
        self.assertIn("moon phase", " ".join(data["guardrails"]))

    def test_chinese_new_full_moon_question_routes_to_timing(self):
        data = run_router("新月和满月哪个更适合搬家开业择时")

        self.assertEqual(data["domain"], "timing")
        self.assertIn("references/timing-and-date-selection.md", data["references"])


if __name__ == "__main__":
    unittest.main()
