import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "generate_report.py"
SAMPLE_PLAN = ROOT / "fengshui-master" / "assets" / "sample-floorplan.json"


def run_report(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


def section_body(report, heading):
    marker = f"## {heading}\n"
    start = report.index(marker) + len(marker)
    end = report.find("\n## ", start)
    return report[start:] if end == -1 else report[start:end]


class GenerateReportScriptTest(unittest.TestCase):
    def test_proactive_sections_precede_method_and_follow_required_order(self):
        report = run_report("I feel blocked lately. What is my current feng shui?")
        headings = [
            "## Provisional Current Posture",
            "## Known Basis",
            "## Favorable Now",
            "## Possible Friction and Ordinary Manifestations",
            "## Confirm or Refute Signals",
            "## Immediate Low-Risk Action",
            "## Prioritized Cross-Domain Concerns",
            "## Actions: Next 72 Hours",
            "## Actions: Next 30 Days",
            "## Actions: Next 90 Days",
            "## Monitoring",
            "## Follow-Up Prompts (Maximum 3)",
        ]

        positions = [report.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        for heading in headings:
            self.assertEqual(report.count(heading), 1, heading)
        self.assertLess(
            report.index("## Provisional Current Posture"),
            report.index("## Supporting Method and Boundaries"),
        )
        self.assertIn("provisional and conditional", report)
        self.assertIn("ordinary", report.lower())
        self.assertIn("strengthen", report)
        self.assertIn("refute", report)

    def test_follow_up_prompts_are_after_monitoring_and_capped_at_three(self):
        report = run_report("Should I buy this stock next month using feng shui?")
        body = section_body(report, "Follow-Up Prompts (Maximum 3)")
        prompts = [line for line in body.splitlines() if line.startswith("- ")]

        self.assertEqual(len(prompts), 3)
        self.assertEqual(
            prompts,
            [
                "- What specific decision are you making, and which options are you comparing?",
                "- What is the decision deadline and intended holding or review horizon?",
                "- How much loss or volatility can you tolerate without jeopardizing essential goals?",
            ],
        )
        self.assertTrue(all(prompt.endswith("?") for prompt in prompts))
        self.assertNotIn("- decision type", body)
        self.assertNotIn("- time horizon", body)
        self.assertNotIn("- risk tolerance", body)
        self.assertNotIn("liquidity needs", body)
        self.assertLess(
            report.index("## Monitoring"), report.index("## Follow-Up Prompts")
        )

    def test_router_clarifying_questions_take_priority_over_missing_inputs(self):
        report = run_report("Help me with feng shui")
        body = section_body(report, "Follow-Up Prompts (Maximum 3)")
        prompts = [line for line in body.splitlines() if line.startswith("- ")]

        self.assertEqual(
            prompts,
            [
                "- What real-world domain and decision should the reading support?",
                "- Do you want spatial, timing, personal-context, or broad symbolic analysis?",
                "- What real-world domain should lead this analysis?",
            ],
        )

    def test_cross_domain_concerns_are_explicitly_prioritized(self):
        report = run_report(
            "Compare fintech product names, onboarding, investment risk, and privacy terms"
        )
        body = section_body(report, "Prioritized Cross-Domain Concerns")

        priorities = [line for line in body.splitlines() if line.startswith("- Priority")]
        self.assertEqual(
            priorities,
            [
                "- Priority 1: finance",
                "- Priority 2: legal_adjacent",
                "- Priority 3: product",
                "- Priority 4: timing",
                "- Priority 5: naming",
            ],
        )
        self.assertIn("do not average conflicts", body)

    def test_cross_domain_follow_up_does_not_ask_user_to_redo_prioritization(self):
        report = run_report(
            "My startup is uncertain, my fund portfolio is down, and I am choosing a new company name"
        )
        body = section_body(report, "Follow-Up Prompts (Maximum 3)")

        self.assertNotIn("Which domain should lead", body)
        self.assertIn("What concrete outcome", body)
        self.assertIn("What specific decision", body)

    def test_critical_safety_report_suspends_symbolic_analysis_first(self):
        report = run_report(
            "I have chest pain in my bedroom; tell me the feng shui cause"
        )
        self.assertIn("Chest pain or trouble breathing may be a medical emergency.", report)
        self.assertIn("Contact local emergency services now.", report)
        self.assertIn("Do not delay for feng shui analysis", report)
        self.assertIn("Feng shui cannot diagnose", report)
        self.assertEqual(report.count("## Provisional Current Posture"), 1)
        self.assertEqual(report.count("## Cultural and Professional Boundary"), 1)
        self.assertNotIn("## Known Basis", report)
        self.assertNotIn("## Immediate Low-Risk Action", report)
        self.assertNotIn("## Follow-Up Prompts", report)
        self.assertNotIn("## Supporting Method and Boundaries", report)
        self.assertNotIn("## Symbolic Lenses", report)
        self.assertNotIn("## Report Sections", report)
        self.assertNotIn("- specific wellbeing concern", report)

    def test_finance_report_contains_guardrails_and_sections(self):
        report = run_report("Should I buy this stock next month using feng shui?")

        self.assertIn("# FengShui Master Consultation Report", report)
        self.assertIn("Domain: finance", report)
        self.assertIn("This is not financial advice.", report)
        self.assertIn("## Financial reality check", report)
        self.assertIn("## Feng shui symbolic layer", report)
        self.assertIn("## Symbolic analysis protocol", report)
        self.assertIn(
            "What is the decision deadline and intended holding or review horizon?",
            report,
        )
        self.assertIn("references/broad-symbolic-analysis.md", report)
        self.assertIn("references/finance-adapter.md", report)

    def test_chinese_life_omen_report_contains_jixiong_section(self):
        report = run_report("帮我用风水分析一个人的生平五行吉凶和运势")

        self.assertIn("Domain: life_omen", report)
        self.assertIn("## Ji/xiong assessment", report)
        self.assertIn("## Symbolic analysis protocol", report)
        self.assertIn("Do not make deterministic fate", report)
        self.assertIn("birth year or relevant year", report)

    def test_floorplan_report_includes_structured_analysis(self):
        report = run_report("Review this apartment layout", "--floorplan", str(SAMPLE_PLAN))

        self.assertIn("Domain: space", report)
        self.assertIn("## Structured Floor-Plan Analysis", report)
        self.assertIn("front_back_alignment", report)
        self.assertIn("Create a visual or circulation pause", report)
        self.assertIn("accessible egress route", report)

    def test_product_report_uses_broad_symbolic_protocol(self):
        report = run_report("Use feng shui to review this product onboarding flow")

        self.assertIn("Domain: product", report)
        self.assertIn("references/broad-symbolic-analysis.md", report)
        self.assertIn("## Symbolic analysis protocol", report)

    def test_report_can_be_written_to_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "finance-report.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "Should I buy this stock next month using feng shui?",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )

            self.assertEqual(result.stdout.strip(), str(output))
            self.assertTrue(output.exists())
            self.assertIn("Domain: finance", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
