import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "method_selector.py"


def run_selector(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class MethodSelectorTest(unittest.TestCase):
    def test_form_school_for_floorplan_layout(self):
        data = run_selector("Review my apartment floorplan, entrance, bedroom, road, and water flow")

        primary = data["primary_method"]
        self.assertEqual(primary["method"], "form_school")
        self.assertIn("references/forms-and-environment.md", primary["references"])
        self.assertIn("fengshui-master/scripts/analyze_floorplan.py", primary["tools"])

    def test_eight_mansions_for_personal_bed_direction(self):
        data = run_selector("Use eight mansions ming gua to choose my bed and desk direction")

        primary = data["primary_method"]
        self.assertEqual(primary["method"], "eight_mansions")
        self.assertIn("birth year", primary["required_inputs"])
        self.assertIn("fengshui-master/scripts/minggua.py", primary["tools"])

    def test_xuan_kong_for_period_natal_flying_stars(self):
        data = run_selector("Use Xuan Kong flying stars, Period 9, and natal chart for this renovation")

        primary = data["primary_method"]
        self.assertEqual(primary["method"], "xuan_kong")
        self.assertIn("references/xuan-kong-flying-stars.md", primary["references"])
        self.assertIn("not a full Xuan Kong natal chart", primary["guardrails"])

    def test_timing_for_solar_terms_and_moon_phase(self):
        data = run_selector("Choose an opening date using solar terms, new moon, and annual cautions")

        primary = data["primary_method"]
        self.assertEqual(primary["method"], "timing")
        self.assertIn("fengshui-master/scripts/solar_terms.py", primary["tools"])
        self.assertIn("not a full almanac", primary["guardrails"])

    def test_broad_symbolic_for_finance_luck(self):
        data = run_selector("Use feng shui to analyze finance luck and business auspiciousness")

        primary = data["primary_method"]
        self.assertEqual(primary["method"], "broad_symbolic")
        self.assertIn("native-domain reality comes first", primary["guardrails"])

    def test_compass_bagua_for_wealth_corner(self):
        data = run_selector("Review the southeast bagua wealth corner")

        primary = data["primary_method"]
        self.assertEqual(primary["method"], "compass_bagua")
        self.assertIn("fengshui-master/scripts/bagua_map.py", primary["tools"])
        self.assertIn("do not mix compass and door-aligned bagua silently", primary["guardrails"])

    def test_fallback_uses_broad_symbolic(self):
        data = run_selector("I need general FengShui Master guidance")

        self.assertEqual(data["primary_method"]["method"], "broad_symbolic")
        self.assertIn("Name the selected method before conclusions.", data["answer_rules"])


if __name__ == "__main__":
    unittest.main()
