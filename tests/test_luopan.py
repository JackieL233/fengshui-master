import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "luopan.py"


def run_luopan(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class LuopanScriptTest(unittest.TestCase):
    def test_cardinal_bearings_map_to_expected_twenty_four_mountains(self):
        self.assertEqual(run_luopan("0")["mountain"], "zi")
        self.assertEqual(run_luopan("90")["mountain"], "mao")
        self.assertEqual(run_luopan("180")["mountain"], "wu")
        self.assertEqual(run_luopan("270")["mountain"], "you")

    def test_edge_bearing_wraps_across_north(self):
        data = run_luopan("359")

        self.assertEqual(data["mountain"], "zi")
        self.assertEqual(data["direction"], "north")

    def test_cli_output_is_ascii_safe_by_default(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "180", "--pretty"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn('"hanzi": "\\u5348"', result.stdout)
        self.assertEqual(json.loads(result.stdout)["hanzi"], "午")


if __name__ == "__main__":
    unittest.main()
