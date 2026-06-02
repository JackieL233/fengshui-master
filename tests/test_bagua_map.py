import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "bagua_map.py"


def run_bagua(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class BaguaMapTest(unittest.TestCase):
    def test_direction_southeast_maps_to_xun_wealth(self):
        data = run_bagua("--direction", "southeast")

        sector = data["sector"]
        self.assertEqual(sector["key"], "xun")
        self.assertEqual(sector["trigram_zh"], "巽")
        self.assertEqual(sector["phase"], "wood")
        self.assertIn("wealth", sector["life_area"])
        self.assertIn("guaranteed wealth", " ".join(sector["cautions"]))

    def test_degrees_maps_to_later_heaven_direction(self):
        data = run_bagua("--degrees", "181")

        self.assertEqual(data["sector"]["key"], "li")
        self.assertEqual(data["sector"]["direction"], "south")
        self.assertEqual(data["sector"]["phase"], "fire")

    def test_trigram_lookup_maps_to_qian(self):
        data = run_bagua("--trigram", "qian")

        self.assertEqual(data["sector"]["direction"], "northwest")
        self.assertEqual(data["sector"]["phase"], "metal")
        self.assertIn("leadership", data["sector"]["life_area"])

    def test_life_area_lookup_maps_relationship_to_kun(self):
        data = run_bagua("--life-area", "relationship", "--method", "symbolic")

        self.assertEqual(data["sector"]["key"], "kun")
        self.assertEqual(data["sector"]["method"], "symbolic")
        self.assertIn("partnership", data["sector"]["life_area"])

    def test_center_lookup_has_no_degrees(self):
        data = run_bagua("--direction", "center")

        self.assertEqual(data["sector"]["key"], "center")
        self.assertIsNone(data["sector"]["center_degrees"])
        self.assertEqual(data["sector"]["phase"], "earth")

    def test_requires_one_lookup_argument(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--direction", "north", "--life-area", "career"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
