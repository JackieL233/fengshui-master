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

    def test_chinese_life_omen_question_creates_life_brief(self):
        data = run_brief("帮我用风水分析一个人的生平五行吉凶和运势")

        self.assertEqual(data["domain"], "life_omen")
        self.assertIn("references/life-and-omen-adapter.md", data["references"])
        self.assertIn("Do not make deterministic fate, health, death, wealth, marriage, or disaster claims.", data["guardrails"])
        self.assertIn("birth year or relevant year", data["missing_inputs"])
        self.assertIn("Ji/xiong assessment", data["report_sections"])

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

    def test_sample_finance_brief_matches_generator(self):
        generated = run_brief("Should I buy this stock next month using feng shui?")
        sample = json.loads(SAMPLE_FINANCE_BRIEF.read_text(encoding="utf-8"))

        self.assertEqual(sample, generated)


if __name__ == "__main__":
    unittest.main()
