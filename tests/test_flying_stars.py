import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "flying_stars.py"


def run_flying_stars(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class FlyingStarsScriptTest(unittest.TestCase):
    def test_forward_loshu_chart_from_period_nine(self):
        data = run_flying_stars("--period", "9")

        self.assertEqual(data["period"], 9)
        self.assertEqual(data["center"], 9)
        self.assertEqual(data["palaces"]["center"]["star"], 9)
        self.assertEqual(data["palaces"]["northwest"]["star"], 1)
        self.assertEqual(data["palaces"]["west"]["star"], 2)
        self.assertEqual(data["palaces"]["northeast"]["star"], 3)

    def test_reverse_loshu_chart_from_period_nine(self):
        data = run_flying_stars("--period", "9", "--direction", "reverse")

        self.assertEqual(data["palaces"]["center"]["star"], 9)
        self.assertEqual(data["palaces"]["northwest"]["star"], 8)
        self.assertEqual(data["palaces"]["north"]["star"], 4)
        self.assertEqual(data["palaces"]["southeast"]["star"], 1)

    def test_period_lookup_from_year(self):
        data = run_flying_stars("--year", "2026")

        self.assertEqual(data["period"], 9)
        self.assertEqual(data["period_year_range"], "2024-2043")


if __name__ == "__main__":
    unittest.main()
