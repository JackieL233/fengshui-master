import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "moon_phase.py"


def run_moon_phase(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class MoonPhaseScriptTest(unittest.TestCase):
    def test_known_new_moon_returns_new_moon_symbolism(self):
        data = run_moon_phase("2024-04-08")

        self.assertEqual(data["phase_key"], "new_moon")
        self.assertLess(data["illumination"], 0.05)
        self.assertIn("new beginnings", data["symbolic_guidance"])
        self.assertIn("not a full almanac", data["limitations"][0])

    def test_known_full_moon_returns_full_moon_symbolism(self):
        data = run_moon_phase("2024-04-23")

        self.assertEqual(data["phase_key"], "full_moon")
        self.assertGreater(data["illumination"], 0.95)
        self.assertIn("visibility", data["symbolic_guidance"])
        self.assertIn("release", data["symbolic_guidance"])

    def test_pretty_output_is_valid_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "2024-04-08", "--pretty"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("\n  ", result.stdout)
        self.assertEqual(json.loads(result.stdout)["phase_key"], "new_moon")

