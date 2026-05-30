import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "annual_afflictions.py"


def run_annual(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class AnnualAfflictionsScriptTest(unittest.TestCase):
    def test_2026_bing_wu_has_tai_sui_south_and_sui_po_north(self):
        data = run_annual("2026")

        self.assertEqual(data["year"], 2026)
        self.assertEqual(data["ganzhi_hanzi"], "丙午")
        self.assertEqual(data["year_branch"], "wu")
        self.assertEqual(data["tai_sui"]["branch"], "wu")
        self.assertEqual(data["tai_sui"]["direction"], "south")
        self.assertEqual(data["sui_po"]["branch"], "zi")
        self.assertEqual(data["sui_po"]["direction"], "north")

    def test_2024_jia_chen_common_san_sha_is_south(self):
        data = run_annual("2024")

        self.assertEqual(data["ganzhi_hanzi"], "甲辰")
        self.assertEqual(data["san_sha"]["direction"], "south")
        self.assertEqual(data["san_sha"]["branches"], ["si", "wu", "wei"])
        self.assertIn("common rule", data["method_note"])

    def test_pretty_output_is_ascii_safe(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "2026", "--pretty"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn('"ganzhi_hanzi": "\\u4e19\\u5348"', result.stdout)
        self.assertEqual(json.loads(result.stdout)["ganzhi_hanzi"], "丙午")

    def test_scope_note_warns_against_precise_date_selection(self):
        data = run_annual("2026")

        self.assertIn("not a full almanac", data["scope_note"])


if __name__ == "__main__":
    unittest.main()
