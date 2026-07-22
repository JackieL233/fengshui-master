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

    def test_fund_volatility_and_performance_chasing_route_to_finance(self):
        data = run_router(
            "My funds are volatile and I keep chasing performance after a drawdown"
        )

        self.assertEqual(data["domain"], "finance")
        self.assertIn("references/finance-adapter.md", data["references"])
        self.assertEqual(data["risk_level"], "high")

    def test_recent_fund_performer_language_routes_to_finance(self):
        data = run_router(
            "My funds are volatile and I want to chase the best recent performer"
        )

        self.assertEqual(data["domain"], "finance")
        self.assertIn("references/finance-adapter.md", data["references"])

    def test_chinese_fund_behavior_routes_to_finance(self):
        data = run_router("基金净值回撤后我总想追涨追高，应该怎样调整仓位？")

        self.assertEqual(data["domain"], "finance")
        self.assertIn("references/finance-adapter.md", data["references"])

    def test_brand_routes_to_domain_adapter(self):
        data = run_router("Help me choose brand colors and a launch direction")

        self.assertEqual(data["domain"], "brand")
        self.assertIn("references/domain-adapters.md", data["references"])
        self.assertIn("references/brand-adapter.md", data["references"])

    def test_personal_naming_routes_to_naming_adapter(self):
        data = run_router(
            "Help me choose a personal name using five phases, meaning, pronunciation, and birth context"
        )

        self.assertEqual(data["domain"], "naming")
        self.assertIn("references/naming-adapter.md", data["references"])
        self.assertIn("Do not infer a missing element from year-level data", " ".join(data["guardrails"]))

    def test_chinese_personal_name_routes_to_naming(self):
        data = run_router("结合五行、出生信息、字义和读音帮宝宝取名")

        self.assertEqual(data["domain"], "naming")
        self.assertIn("references/naming-adapter.md", data["references"])

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

    def test_mixed_naming_and_product_request_fuses_both_adapters(self):
        data = run_router(
            "Compare these app names and onboarding flows for meaning, pronunciation, and conversion"
        )

        self.assertIn("naming", data["domains"])
        self.assertIn("product", data["domains"])
        self.assertIn("references/naming-adapter.md", data["references"])
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

    def test_sleeping_poorly_fuses_wellbeing_and_space(self):
        data = run_router(
            "I have been sleeping poorly. Review my bedroom feng shui."
        )

        self.assertIn("wellbeing", data["domains"])
        self.assertIn("space", data["domains"])
        self.assertIn("references/wellbeing-adapter.md", data["references"])
        self.assertIn("references/forms-and-environment.md", data["references"])

    def test_legal_adjacent_routes_to_legal_adapter(self):
        data = run_router("Use feng shui to think about this contract and legal dispute")

        self.assertEqual(data["domain"], "legal_adjacent")
        self.assertIn("references/legal-adjacent-adapter.md", data["references"])
        self.assertIn("Do not provide legal advice.", data["guardrails"])

    def test_space_defaults_to_classic_feng_shui(self):
        data = run_router("Analyze my bedroom layout and mirror placement")

        self.assertEqual(data["domain"], "space")
        self.assertIn("references/foundation.md", data["references"])
        self.assertIn("references/analysis-templates.md", data["references"])

    def test_bagua_wealth_corner_routes_to_space_foundation(self):
        data = run_router("Use bagua to review my southeast wealth corner")

        self.assertEqual(data["domain"], "space")
        self.assertIn("references/foundation.md", data["references"])
        self.assertIn("references/remedies.md", data["references"])

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

    def test_solar_term_question_routes_to_timing(self):
        data = run_router("Use feng shui to compare li chun and the spring equinox for a product launch")

        self.assertEqual(data["domain"], "timing")
        self.assertIn("references/timing-and-date-selection.md", data["references"])
        self.assertIn("solar terms", " ".join(data["guardrails"]))

    def test_full_portfolio_does_not_false_match_timing(self):
        data = run_router("Review my full portfolio and downside risk")

        self.assertEqual(data["domain"], "finance")
        self.assertNotIn("timing", data["domains"])

    def test_all_high_risk_domains_are_preserved(self):
        data = run_router(
            "Review the investment terms, healthcare privacy, and legal contract for this fintech product"
        )

        self.assertIn("finance", data["domains"])
        self.assertIn("wellbeing", data["domains"])
        self.assertIn("legal_adjacent", data["domains"])
        self.assertEqual(data["risk_level"], "high")

    def test_urgent_medical_prompt_suppresses_symbolic_analysis(self):
        data = run_router("I have chest pain in my bedroom; use feng shui to explain it")

        self.assertIn("wellbeing", data["domains"])
        self.assertEqual(data["route_status"], "critical_safety")
        self.assertEqual(data["risk_level"], "critical")
        self.assertFalse(data["symbolic_analysis_allowed"])
        self.assertGreaterEqual(len(data["clarifying_questions"]), 1)

    def test_chinese_urgent_medical_prompt_suppresses_symbolic_analysis(self):
        data = run_router("我现在胸痛和呼吸困难，卧室风水是不是有问题")

        self.assertIn("wellbeing", data["domains"])
        self.assertEqual(data["route_status"], "critical_safety")
        self.assertFalse(data["symbolic_analysis_allowed"])

    def test_critical_fallback_cannot_bypass_safety_suppression(self):
        data = run_router("There is imminent danger right now")

        self.assertEqual(data["route_status"], "critical_safety")
        self.assertEqual(data["risk_level"], "critical")
        self.assertFalse(data["symbolic_analysis_allowed"])
        self.assertIn("before symbolic analysis", " ".join(data["guardrails"]))

    def test_filing_deadline_stops_symbolic_timing_analysis(self):
        data = run_router(
            "A filing deadline is tomorrow, but the auspicious date is next week"
        )

        self.assertIn("legal_adjacent", data["domains"])
        self.assertIn("timing", data["domains"])
        self.assertEqual(data["route_status"], "critical_safety")
        self.assertFalse(data["symbolic_analysis_allowed"])

    def test_exam_money_and_family_pressure_routes_across_reality_domains(self):
        data = run_router(
            "I am preparing for an exam, money is tight, and family pressure distracts me"
        )

        self.assertIn("learning", data["domains"])
        self.assertIn("finance", data["domains"])
        self.assertIn("relationship", data["domains"])
        self.assertEqual(data["risk_level"], "high")

    def test_cybersecurity_uses_high_risk_universal_adaptation(self):
        data = run_router(
            "Use FengShui Master to assess our cybersecurity program and weaknesses"
        )

        self.assertEqual(data["domains"], ["general"])
        self.assertNotIn("cybersecurity", data["domains"])
        self.assertEqual(data["route_status"], "universal_adaptation")
        self.assertEqual(data["risk_level"], "high")
        self.assertIn("references/domain-adapters.md", data["references"])
        self.assertIn("references/five-phase-domain-map.md", data["references"])
        self.assertIn("qualified security review", " ".join(data["guardrails"]))

    def test_founder_decision_overload_routes_to_business(self):
        data = run_router(
            "I am a founder with too many decisions, slow execution, and a team waiting"
        )

        self.assertEqual(data["domain"], "business")
        self.assertIn("references/business-adapter.md", data["references"])

    def test_legal_deadline_is_critical_and_preserves_legal_domain(self):
        data = run_router("I have a legal deadline today; choose an auspicious filing time")

        self.assertIn("legal_adjacent", data["domains"])
        self.assertEqual(data["route_status"], "critical_safety")
        self.assertFalse(data["symbolic_analysis_allowed"])

    def test_fintech_naming_preserves_finance_guardrails(self):
        data = run_router("Help with fintech naming")

        self.assertIn("naming", data["domains"])
        self.assertIn("finance", data["domains"])
        self.assertIn("This is not financial advice.", data["guardrails"])

    def test_chinese_solar_term_question_routes_to_timing(self):
        data = run_router("立春和冬至哪个更适合开业择时")

        self.assertEqual(data["domain"], "timing")
        self.assertIn("references/timing-and-date-selection.md", data["references"])


if __name__ == "__main__":
    unittest.main()
