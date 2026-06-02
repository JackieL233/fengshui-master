import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "solar_terms.py"


def run_solar_terms(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class SolarTermsTest(unittest.TestCase):
    def test_lichun_returns_spring_gate_context(self):
        data = run_solar_terms("2026-02-04")

        self.assertEqual(data["current_term"]["key"], "lichun")
        self.assertEqual(data["current_term"]["name_zh"], "立春")
        self.assertEqual(data["current_term"]["five_phase"], "wood")
        self.assertIn("annual-boundary", data["current_term"]["symbolic_guidance"])

    def test_xiazhi_returns_peak_yang_context(self):
        data = run_solar_terms("2026-06-21")

        self.assertEqual(data["current_term"]["key"], "xiazhi")
        self.assertIn("yang peaks", data["current_term"]["yin_yang"])
        self.assertEqual(data["current_term"]["five_phase"], "fire")

    def test_qiufen_returns_balance_context(self):
        data = run_solar_terms("2026-09-23")

        self.assertEqual(data["current_term"]["key"], "qiufen")
        self.assertEqual(data["current_term"]["name_zh"], "秋分")
        self.assertIn("balanced", data["current_term"]["yin_yang"])

    def test_dongzhi_returns_peak_yin_context(self):
        data = run_solar_terms("2026-12-22")

        self.assertEqual(data["current_term"]["key"], "dongzhi")
        self.assertIn("yin peaks", data["current_term"]["yin_yang"])
        self.assertEqual(data["current_term"]["five_phase"], "water")

    def test_nearby_date_reports_next_term_and_limitations(self):
        data = run_solar_terms("2026-04-10")

        self.assertEqual(data["current_term"]["key"], "qingming")
        self.assertEqual(data["next_term"]["key"], "guyu")
        self.assertGreater(data["days_until_next_term"], 0)
        self.assertIn("not a full tong shu", " ".join(data["limitations"]))

    def test_pretty_cli_outputs_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "2026-02-04", "--pretty"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertEqual(json.loads(result.stdout)["current_term"]["key"], "lichun")


if __name__ == "__main__":
    unittest.main()
