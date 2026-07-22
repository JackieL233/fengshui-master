import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "create_brief.py"
SAMPLE_PLAN = ROOT / "fengshui-master" / "assets" / "sample-floorplan.json"
SAMPLE_FINANCE_BRIEF = ROOT / "fengshui-master" / "assets" / "sample-finance-brief.json"


def run_brief(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def stop_condition(data, condition_id):
    return next(
        condition
        for condition in data["proactive_delivery"]["stop_conditions"]
        if condition["id"] == condition_id
    )


class CreateBriefScriptTest(unittest.TestCase):
    def test_finance_question_creates_guardrailed_brief(self):
        data = run_brief("Should I buy this stock next month using feng shui?")

        self.assertEqual(data["question"], "Should I buy this stock next month using feng shui?")
        self.assertEqual(data["domain"], "finance")
        self.assertIn("references/finance-adapter.md", data["references"])
        self.assertIn("This is not financial advice.", data["guardrails"])
        self.assertIn("Financial reality check", data["report_sections"])
        self.assertIn("Feng shui symbolic layer", data["report_sections"])
        self.assertIn("time horizon", data["missing_inputs"])
        self.assertIn("references/broad-symbolic-analysis.md", data["references"])
        self.assertIn("Symbolic analysis protocol", data["report_sections"])
        self.assertEqual(
            data["report_sections"][0], "Provisional current posture"
        )
        self.assertIn("Known basis and confidence", data["report_sections"])
        self.assertIn("Favorable conditions", data["report_sections"])
        self.assertIn(
            "Possible friction and ordinary manifestations",
            data["report_sections"],
        )
        self.assertIn(
            "Confirmation and disconfirmation signals", data["report_sections"]
        )
        self.assertIn("Immediate low-risk action", data["report_sections"])
        self.assertIn("Actions: next 72 hours", data["report_sections"])
        self.assertIn("Actions: next 30 days", data["report_sections"])
        self.assertIn("Actions: next 90 days", data["report_sections"])
        self.assertIn("Monitoring signals", data["report_sections"])
        self.assertEqual(
            data["report_sections"][-1], "Follow-up questions (maximum 3)"
        )
        self.assertIn(
            "Label facts, calculations, inferences, unknowns, and recommendations separately.",
            data["answer_contract"],
        )

    def test_chinese_life_omen_question_creates_life_brief(self):
        data = run_brief("帮我用风水分析一个人的生平五行吉凶和运势")

        self.assertEqual(data["domain"], "life_omen")
        self.assertIn("references/life-and-omen-adapter.md", data["references"])
        self.assertIn("Do not make deterministic fate, health, death, wealth, marriage, or disaster claims.", data["guardrails"])
        self.assertIn("birth year or relevant year", data["missing_inputs"])
        self.assertIn("Ji/xiong assessment", data["report_sections"])
        self.assertIn("references/broad-symbolic-analysis.md", data["references"])
        self.assertIn("Symbolic analysis protocol", data["report_sections"])

    def test_life_omen_brief_does_not_report_inputs_already_provided(self):
        data = run_brief(
            "I was born in 1998 and want an analysis of my recent luck and career."
        )

        self.assertEqual(data["domain"], "life_omen")
        self.assertNotIn("birth year or relevant year", data["missing_inputs"])
        self.assertNotIn("topic area", data["missing_inputs"])
        self.assertNotIn("goal for the reading", data["missing_inputs"])

    def test_chinese_birth_date_counts_as_provided_birth_year(self):
        data = run_brief(
            "1998年3月22日18:30左右出生，男，浙江桐乡。主动分析我最近的运势和事业。"
        )

        self.assertEqual(data["domain"], "life_omen")
        self.assertNotIn("birth year or relevant year", data["missing_inputs"])
        self.assertNotIn("topic area", data["missing_inputs"])
        self.assertNotIn("goal for the reading", data["missing_inputs"])

    def test_floorplan_path_adds_space_analysis(self):
        data = run_brief(
            "Review this apartment layout",
            "--floorplan",
            str(SAMPLE_PLAN),
        )

        self.assertEqual(data["domain"], "space")
        self.assertEqual(data["floorplan_analysis"]["valid"], True)
        self.assertIn("Structured floor-plan findings", data["report_sections"])
        self.assertIn("floorplan-schema.md", " ".join(data["references"]))

    def test_pretty_output_is_valid_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "Use feng shui for my career phase", "--pretty"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("\n  ", result.stdout)
        self.assertEqual(json.loads(result.stdout)["domain"], "career")

    def test_sample_finance_brief_preserves_legacy_generator_fields(self):
        generated = run_brief("Should I buy this stock next month using feng shui?")
        sample = json.loads(SAMPLE_FINANCE_BRIEF.read_text(encoding="utf-8"))

        changed_contract_fields = {
            "proactive_delivery",
            "report_sections",
            "answer_contract",
        }
        for key, value in sample.items():
            if key not in changed_contract_fields:
                self.assertEqual(value, generated[key])

    def test_finance_action_without_native_evidence_blocks_execution_only(self):
        data = run_brief("Should I buy this stock next month using feng shui?")
        condition = stop_condition(data, "missing_high_stakes_evidence")

        self.assertTrue(condition["triggered"])
        self.assertEqual(condition["action_intent_domains"], ["finance"])
        self.assertIn("risk tolerance", condition["missing_essential_evidence"]["finance"])
        self.assertIn("execution_style_recommendations", condition["blocks"])
        self.assertIn("irreversible_recommendations", condition["blocks"])
        self.assertIn("bounded_educational_analysis", condition["allows"])
        self.assertIn("bounded_provisional_analysis", condition["allows"])
        self.assertEqual(
            data["proactive_delivery"]["recommendation_mode"],
            "bounded_provisional_only",
        )

    def test_legal_action_without_native_evidence_blocks_execution_only(self):
        data = run_brief(
            "Should I sign this contract using an auspicious feng shui date?"
        )
        condition = stop_condition(data, "missing_high_stakes_evidence")

        self.assertIn("legal_adjacent", data["domains"])
        self.assertTrue(condition["triggered"])
        self.assertIn("legal_adjacent", condition["action_intent_domains"])
        self.assertIn(
            "hard deadlines and required procedures",
            condition["missing_essential_evidence"]["legal_adjacent"],
        )
        self.assertIn("reversible_preparation_steps", condition["allows"])

    def test_high_risk_informational_request_does_not_trigger_evidence_stop(self):
        data = run_brief(
            "Explain how the five phases can be used as a symbolic lens in finance."
        )
        condition = stop_condition(data, "missing_high_stakes_evidence")

        self.assertEqual(data["risk_level"], "high")
        self.assertIn("finance", condition["high_risk_domains"])
        self.assertFalse(condition["decision_or_action_intent"])
        self.assertFalse(condition["triggered"])
        self.assertEqual(condition["missing_essential_evidence"], {})
        self.assertEqual(
            data["proactive_delivery"]["recommendation_mode"],
            "guardrailed_provisional",
        )

    def test_proactive_delivery_is_machine_readable_and_provisional_first(self):
        data = run_brief("Everything feels blocked lately")
        contract = data["proactive_delivery"]

        self.assertEqual(contract["mode"], "provisional_first")
        self.assertTrue(contract["headline_before_questions"])
        self.assertEqual(contract["max_follow_up_questions"], 3)
        self.assertEqual(contract["required_sequence"][0], "safety_precheck")
        self.assertEqual(
            contract["required_sequence"][1], "provisional_current_posture"
        )
        self.assertLess(
            contract["required_sequence"].index("provisional_current_posture"),
            contract["required_sequence"].index("follow_up_questions"),
        )
        self.assertIn("lower confidence", contract["sparse_input_rule"])
        self.assertLessEqual(len(data["clarifying_questions"]), 3)
        self.assertEqual(
            data["report_sections"][-1], "Follow-up questions (maximum 3)"
        )

    def test_cross_domain_priorities_put_reality_first_domains_first(self):
        data = run_brief(
            "Compare product naming, onboarding, investment risk, and privacy terms"
        )
        priorities = data["proactive_delivery"]["domain_priorities"]

        self.assertTrue(priorities["do_not_average_domains"])
        self.assertEqual(priorities["ordered_domains"][0], "finance")
        self.assertEqual(priorities["items"][0]["handling"], "reality_first")
        self.assertLess(
            priorities["ordered_domains"].index("legal_adjacent"),
            priorities["ordered_domains"].index("naming"),
        )

    def test_cross_domain_priorities_put_business_before_naming(self):
        data = run_brief(
            "My startup is uncertain, my fund portfolio is down, and I am choosing a new company name"
        )
        ordered = data["proactive_delivery"]["domain_priorities"]["ordered_domains"]

        self.assertEqual(ordered[0], "finance")
        self.assertLess(ordered.index("business"), ordered.index("naming"))

    def test_moon_phase_question_creates_timing_brief(self):
        data = run_brief("Should I launch on the new moon or full moon?")

        self.assertEqual(data["domain"], "timing")
        self.assertIn("references/timing-and-date-selection.md", data["references"])
        self.assertIn("candidate date or date range", data["missing_inputs"])
        self.assertIn("Moon phase symbolic layer", data["report_sections"])

    def test_solar_term_question_creates_timing_brief(self):
        data = run_brief("Should I open my shop around li chun or winter solstice?")

        self.assertEqual(data["domain"], "timing")
        self.assertIn("references/timing-and-date-selection.md", data["references"])
        self.assertIn(
            "whether the user wants moon phase, solar terms, almanac attributes, annual cautions, or lineage-specific date selection",
            data["missing_inputs"],
        )
        self.assertIn("Solar term seasonal qi layer", data["report_sections"])

    def test_naming_question_creates_multilayer_brief(self):
        data = run_brief(
            "Help me choose a personal name using five phases, meaning, and pronunciation"
        )

        self.assertEqual(data["domain"], "naming")
        self.assertIn("references/naming-adapter.md", data["references"])
        self.assertIn(
            "name type: personal, baby, adult rename, pen/stage, brand, company, or product",
            data["missing_inputs"],
        )
        self.assertIn("Native naming constraints", data["report_sections"])
        self.assertIn("Five-phase symbolic fit", data["report_sections"])

    def test_cross_domain_brief_merges_inputs_sections_and_guardrails(self):
        data = run_brief(
            "Compare fintech product names, onboarding, investment risk, and privacy terms"
        )

        self.assertIn("naming", data["domains"])
        self.assertIn("product", data["domains"])
        self.assertIn("finance", data["domains"])
        self.assertIn("legal_adjacent", data["domains"])
        self.assertIn("risk tolerance", data["missing_inputs"])
        self.assertIn("product type and target user", data["missing_inputs"])
        self.assertIn("Legal reality first", data["report_sections"])
        self.assertIn("Product reality layer", data["report_sections"])
        self.assertIn("This is not financial advice.", data["guardrails"])
        self.assertEqual(data["input_state"]["missing"], data["missing_inputs"])

    def test_critical_safety_route_blocks_symbolic_analysis(self):
        data = run_brief(
            "I have chest pain in my bedroom; should I stop taking my medication because of feng shui?"
        )

        self.assertFalse(data["symbolic_analysis_allowed"])
        self.assertEqual(data["route_status"], "critical_safety")
        self.assertTrue(data["input_state"]["blocking"])
        safety = data["proactive_delivery"]["safety_precheck"]
        self.assertEqual(safety["status"], "blocked")
        self.assertTrue(safety["overrides_required_sequence"])
        self.assertTrue(
            data["proactive_delivery"]["stop_conditions"][0]["triggered"]
        )
        evidence_stop = stop_condition(data, "missing_high_stakes_evidence")
        self.assertTrue(evidence_stop["triggered"])
        self.assertEqual(evidence_stop["superseded_by"], "urgent_real_world_risk")
        self.assertEqual(
            data["proactive_delivery"]["recommendation_mode"],
            "safety_triage_only",
        )
        self.assertEqual(data["proactive_delivery"]["max_follow_up_questions"], 0)


if __name__ == "__main__":
    unittest.main()
