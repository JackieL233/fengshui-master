import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "ganzhi.py"


def run_ganzhi(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class GanzhiScriptTest(unittest.TestCase):
    def test_period_nine_opening_year_is_jia_chen(self):
        data = run_ganzhi("2024")

        self.assertEqual(data["year"], 2024)
        self.assertEqual(data["stem"], "jia")
        self.assertEqual(data["stem_hanzi"], "甲")
        self.assertEqual(data["branch"], "chen")
        self.assertEqual(data["branch_hanzi"], "辰")
        self.assertEqual(data["ganzhi"], "jia-chen")
        self.assertEqual(data["ganzhi_hanzi"], "甲辰")
        self.assertEqual(data["zodiac"], "dragon")
        self.assertEqual(data["stem_phase"], "wood")
        self.assertEqual(data["stem_yin_yang"], "yang")

    def test_current_year_is_bing_wu(self):
        data = run_ganzhi("2026")

        self.assertEqual(data["ganzhi"], "bing-wu")
        self.assertEqual(data["ganzhi_hanzi"], "丙午")
        self.assertEqual(data["zodiac"], "horse")
        self.assertEqual(data["branch_phase"], "fire")

    def test_cli_output_is_ascii_safe_by_default(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "2024", "--pretty"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn('"ganzhi_hanzi": "\\u7532\\u8fb0"', result.stdout)
        self.assertEqual(json.loads(result.stdout)["ganzhi_hanzi"], "甲辰")

    def test_boundary_note_warns_about_li_chun(self):
        data = run_ganzhi("2024")

        self.assertIn("li chun", data["boundary_note"])


if __name__ == "__main__":
    unittest.main()
