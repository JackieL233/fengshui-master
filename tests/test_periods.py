import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "periods.py"


def run_period(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class PeriodScriptTest(unittest.TestCase):
    def test_period_nine_started_in_2024(self):
        data = run_period("2024")

        self.assertEqual(data["period"], 9)
        self.assertEqual(data["start_year"], 2024)
        self.assertEqual(data["end_year"], 2043)
        self.assertEqual(data["trigram"], "li")

    def test_period_eight_boundaries(self):
        self.assertEqual(run_period("2004")["period"], 8)
        self.assertEqual(run_period("2023")["period"], 8)

    def test_out_of_supported_range_fails(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1800"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("supported range", result.stderr)


if __name__ == "__main__":
    unittest.main()
