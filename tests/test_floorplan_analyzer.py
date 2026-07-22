import json
import subprocess
import sys
import tempfile
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


def run_plan(plan):
    with tempfile.TemporaryDirectory() as temporary_directory:
        path = Path(temporary_directory) / "plan.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        return run_analyzer(str(path))


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
        issue = next(item for item in data["issues"] if item["code"] == "front_back_alignment")
        self.assertEqual(issue["source_ids"], ["front-door", "rear-window"])
        recommendation = next(
            item for item in data["recommendations"] if item["issue_code"] == "front_back_alignment"
        )
        self.assertIn("accessible circulation", " ".join(recommendation["constraints"]))

    def test_rejects_invalid_geometry_ids_bearings_and_entries(self):
        plan = json.loads(SAMPLE.read_text(encoding="utf-8"))
        plan["rooms"].append(
            {
                "id": "bedroom",
                "type": "storage",
                "x": 9,
                "y": 7,
                "width": -2,
                "height": 3,
            }
        )
        plan["features"].append(
            {
                "id": "bad-bearing",
                "type": "desk",
                "x": 20,
                "y": 2,
                "facing_degrees": 360,
            }
        )
        plan["features"].append("not-an-object")

        data = run_plan(plan)
        errors = " ".join(data["errors"])

        self.assertFalse(data["valid"])
        self.assertIn("duplicate room id", errors)
        self.assertIn("must be positive", errors)
        self.assertIn("outside plan bounds", errors)
        self.assertIn("finite bearing", errors)
        self.assertIn("must be an object", errors)

    def test_rejects_non_finite_values(self):
        plan = json.loads(SAMPLE.read_text(encoding="utf-8"))
        plan["features"][0]["x"] = float("nan")

        data = run_plan(plan)

        self.assertFalse(data["valid"])
        self.assertIn("finite number", " ".join(data["errors"]))

    def test_door_role_is_required_and_alignment_is_not_assessed_without_it(self):
        plan = json.loads(SAMPLE.read_text(encoding="utf-8"))
        del plan["features"][0]["role"]

        data = run_plan(plan)

        self.assertFalse(data["valid"])
        self.assertIn("role must be main_entrance or interior", " ".join(data["errors"]))

    def test_pixel_plan_without_thresholds_reports_proximity_as_not_assessed(self):
        plan = json.loads(SAMPLE.read_text(encoding="utf-8"))
        plan["units"] = "pixels"

        data = run_plan(plan)
        codes = {item["code"] for item in data["not_assessed"]}

        self.assertTrue(data["valid"])
        self.assertEqual(data["analysis_metadata"]["tolerance_source"], "unavailable")
        self.assertIn("entry_alignment_not_assessed", codes)
        self.assertIn("stove_sink_proximity_not_assessed", codes)

    def test_aligned_interior_window_is_not_treated_as_front_back_leakage(self):
        plan = json.loads(SAMPLE.read_text(encoding="utf-8"))
        plan["features"][1]["role"] = "interior"

        data = run_plan(plan)
        issue_codes = {item["code"] for item in data["issues"]}
        not_assessed_codes = {item["code"] for item in data["not_assessed"]}

        self.assertTrue(data["valid"])
        self.assertNotIn("front_back_alignment", issue_codes)
        self.assertIn("entry_alignment_not_assessed", not_assessed_codes)

    def test_center_gap_is_not_replaced_with_nearest_room(self):
        plan = json.loads(SAMPLE.read_text(encoding="utf-8"))
        plan["rooms"] = [
            {
                "id": "left",
                "type": "living",
                "x": 0,
                "y": 0,
                "width": 4,
                "height": 8,
            },
            {
                "id": "right",
                "type": "living",
                "x": 6,
                "y": 0,
                "width": 4,
                "height": 8,
            },
        ]
        plan["features"] = []

        data = run_plan(plan)
        codes = {item["code"] for item in data["not_assessed"]}

        self.assertTrue(data["valid"])
        self.assertEqual(data["findings"]["center"], [])
        self.assertIn("center_room_not_assessed", codes)

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
