import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "analyze_floorplan.py"
SAMPLE = ROOT / "fengshui-master" / "assets" / "sample-floorplan.json"


def run_analyzer(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class FloorplanAnalyzerTest(unittest.TestCase):
    def test_sample_floorplan_produces_structured_findings(self):
        data = run_analyzer(str(SAMPLE))

        self.assertEqual(data["input"]["type"], "residential")
        self.assertEqual(data["input"]["facing_degrees"], 180)
        self.assertIn("entry", data["findings"])
        self.assertIn("bedroom", data["findings"])
        self.assertIn("center", data["findings"])
        self.assertGreaterEqual(len(data["recommendations"]), 3)

    def test_detects_door_window_alignment(self):
        data = run_analyzer(str(SAMPLE))
        issue_codes = {item["code"] for item in data["issues"]}

        self.assertIn("front_back_alignment", issue_codes)

    def test_inventory_links_schema_and_script(self):
        skill = (ROOT / "fengshui-master" / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue((ROOT / "fengshui-master" / "references" / "floorplan-schema.md").exists())
        self.assertTrue(SAMPLE.exists())
        self.assertIn("references/floorplan-schema.md", skill)
        self.assertIn("scripts/analyze_floorplan.py", skill)
        self.assertIn("sample-floorplan.json", readme)


if __name__ == "__main__":
    unittest.main()
