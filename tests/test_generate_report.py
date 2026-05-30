import subprocess
import sys
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


class GenerateReportScriptTest(unittest.TestCase):
    def test_finance_report_contains_guardrails_and_sections(self):
        report = run_report("Should I buy this stock next month using feng shui?")

        self.assertIn("# FengShui Master Consultation Report", report)
        self.assertIn("Domain: finance", report)
        self.assertIn("This is not financial advice.", report)
        self.assertIn("## Financial reality check", report)
        self.assertIn("## Feng shui symbolic layer", report)
        self.assertIn("- time horizon", report)
        self.assertIn("references/finance-adapter.md", report)

    def test_chinese_life_omen_report_contains_jixiong_section(self):
        report = run_report("帮我用风水分析一个人的生平五行吉凶和运势")

        self.assertIn("Domain: life_omen", report)
        self.assertIn("## Ji/xiong assessment", report)
        self.assertIn("Do not make deterministic fate", report)
        self.assertIn("birth year or relevant year", report)

    def test_floorplan_report_includes_structured_analysis(self):
        report = run_report("Review this apartment layout", "--floorplan", str(SAMPLE_PLAN))

        self.assertIn("Domain: space", report)
        self.assertIn("## Structured Floor-Plan Analysis", report)
        self.assertIn("front_back_alignment", report)
        self.assertIn("Create a pause point", report)

    def test_report_can_be_written_to_file(self):
        output = ROOT / "fengshui-master" / "assets" / "sample-finance-report.md"
        if output.exists():
            output.unlink()

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
