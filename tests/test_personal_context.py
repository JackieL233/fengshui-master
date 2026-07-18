import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "personal_context.py"


def run_context(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class PersonalContextScriptTest(unittest.TestCase):
    def test_complete_birth_input_builds_bounded_context_pack(self):
        data = run_context(
            "--birth-date",
            "1998-03-22",
            "--birth-time",
            "18:30",
            "--sex",
            "male",
            "--birth-location",
            "Tongxiang, Jiaxing, Zhejiang, China",
            "--timezone",
            "Asia/Shanghai",
            "--as-of",
            "2026-07-18",
        )

        self.assertEqual(data["method"], "personal-feng-shui-context-scaffold")
        self.assertEqual(data["inputs"]["birth_date"], "1998-03-22")
        self.assertEqual(data["birth_context"]["year_ganzhi"]["ganzhi_hanzi"], "戊寅")
        self.assertEqual(data["birth_context"]["ming_gua"]["gua_number"], 2)
        self.assertEqual(data["current_context"]["year_ganzhi"]["ganzhi_hanzi"], "丙午")
        self.assertEqual(data["current_context"]["san_yuan_period"]["period"], 9)
        self.assertEqual(data["missing_inputs"], [])
        self.assertIn("not a complete bazi", " ".join(data["limitations"]))

        proactive = data["proactive_scan_contract"]
        self.assertEqual(
            proactive["status_labels"],
            ["observed", "calculated", "inferred", "unknown", "recommended"],
        )
        self.assertIn("finance and resources", proactive["domains"])
        self.assertIn("possible_friction", proactive["required_for_each"])
        self.assertIn(
            "confirmation_or_refutation_evidence", proactive["required_for_each"]
        )
        self.assertEqual(
            proactive["action_horizons"],
            ["next_72_hours", "next_30_days", "next_90_days"],
        )

    def test_missing_sex_omits_ming_gua_without_inventing_it(self):
        data = run_context(
            "--birth-date",
            "1998-03-22",
            "--as-of",
            "2026-07-18",
        )

        self.assertIsNone(data["birth_context"]["ming_gua"])
        self.assertIn("sex or lineage convention for ming gua", data["missing_inputs"])
        self.assertEqual(data["birth_context"]["year_ganzhi"]["year"], 1998)

    def test_invalid_birth_time_is_rejected(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--birth-date", "1998-03-22", "--birth-time", "25:99"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("HH:MM", result.stderr)


if __name__ == "__main__":
    unittest.main()
