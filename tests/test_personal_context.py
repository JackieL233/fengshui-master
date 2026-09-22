import importlib.util
import json
import subprocess
import sys
import unittest
from unittest.mock import patch
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "personal_context.py"


def load_context_module():
    sys.path.insert(0, str(SCRIPT.parent))
    try:
        spec = importlib.util.spec_from_file_location("personal_context_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


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
        self.assertEqual(data["inputs"]["as_of_source"], "explicit_analysis_date")
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

    def test_proactive_scan_contract_delivers_current_reading_before_questions(self):
        data = run_context(
            "--birth-date",
            "1998-03-22",
            "--as-of",
            "2026-07-18",
        )

        proactive = data["proactive_scan_contract"]
        self.assertEqual(proactive["delivery_mode"], "provisional_first")
        self.assertTrue(proactive["headline_before_questions"])
        self.assertEqual(proactive["max_follow_up_questions"], 3)
        self.assertEqual(
            proactive["provisional_reading_fields"],
            [
                "headline_current_posture",
                "current_favorable",
                "current_friction",
                "ordinary_manifestations",
                "confirmation_and_refutation_signals",
                "immediate_low_risk_action",
            ],
        )

        sequence = proactive["required_sequence"]
        self.assertEqual(
            sequence,
            [
                "urgent_safety_check",
                "headline_current_posture",
                "known_basis",
                "current_favorable",
                "current_friction",
                "ordinary_manifestations",
                "confirmation_and_refutation_signals",
                "immediate_low_risk_action",
                "domain_priorities",
                "action_horizons",
                "monitoring_signals",
                "follow_up_questions",
            ],
        )
        self.assertEqual(
            sequence[-3:],
            ["action_horizons", "monitoring_signals", "follow_up_questions"],
        )

        monitoring = proactive["monitoring_contract"]
        self.assertEqual(
            list(monitoring),
            ["observable_signals", "review_point", "stop_conditions"],
        )
        self.assertEqual(
            monitoring["observable_signals"],
            [
                "user-visible outcomes tied to the highest-priority domain",
                "whether favorable conditions strengthen and friction signals weaken",
                "adverse effects or evidence that refutes the provisional reading",
            ],
        )
        self.assertEqual(
            monitoring["review_point"],
            "review after 72 hours, then at 30 and 90 days when applicable",
        )
        self.assertEqual(
            monitoring["stop_conditions"],
            [
                "stop or reverse an adjustment if real-world risk or harm increases",
                "stop relying on a hypothesis when observable evidence repeatedly refutes it",
                "escalate urgent or high-stakes concerns to the appropriate qualified professional",
            ],
        )

    def test_sparse_input_contract_lowers_confidence_and_prioritizes_domains(self):
        data = run_context(
            "--birth-date",
            "1998-03-22",
            "--as-of",
            "2026-07-18",
        )

        proactive = data["proactive_scan_contract"]
        sparse = proactive["sparse_input_behavior"]
        self.assertEqual(
            sparse["confidence_rule"], "lower_confidence_not_suppress_reading"
        )
        self.assertTrue(sparse["provisional_reading_required"])
        self.assertFalse(sparse["invent_missing_facts"])
        self.assertFalse(sparse["questions_before_reading"])

        prioritization = proactive["domain_prioritization"]
        self.assertEqual(prioritization["mode"], "material_relevance")
        self.assertEqual(
            prioritization["priority_order"],
            [
                "requested_domain",
                "materially_relevant_adjacent_domains",
                "deferred_domains",
            ],
        )
        self.assertIn("do not expand every domain equally", prioritization["rule"])

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

    def test_li_chun_approx_uses_previous_effective_year_before_february_fourth(self):
        data = run_context(
            "--birth-date",
            "1998-01-20",
            "--sex",
            "male",
            "--as-of",
            "2026-01-20",
            "--year-boundary",
            "li_chun_approx",
        )

        self.assertEqual(data["birth_context"]["effective_year"], 1997)
        self.assertEqual(data["current_context"]["effective_year"], 2025)
        self.assertEqual(
            data["birth_context"]["year_boundary_provenance"]["mode"],
            "li_chun_approx",
        )
        self.assertIn(
            "not the exact local solar-term moment",
            data["birth_context"]["year_boundary_provenance"]["precision"],
        )
        for context in ["birth_context", "current_context"]:
            self.assertIn("Li Chun", data[context]["year_ganzhi"]["boundary_note"])
            self.assertNotIn("uses the Gregorian year label", data[context]["year_ganzhi"]["boundary_note"])

    def test_current_timezone_clock_handles_cross_date_boundary(self):
        module = load_context_module()

        class FixedDatetime(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime(2026, 9, 22, 12, tzinfo=timezone.utc).astimezone(tz)

        with patch.object(module, "datetime", FixedDatetime):
            with patch.object(module, "ZoneInfo", return_value=timezone(timedelta(hours=14))):
                east = module.build_personal_context(date(1998, 3, 22), current_timezone="Pacific/Kiritimati")
            with patch.object(module, "ZoneInfo", return_value=timezone(timedelta(hours=-4))):
                west = module.build_personal_context(date(1998, 3, 22), current_timezone="America/New_York")
        self.assertEqual(east["inputs"]["as_of"], "2026-09-23")
        self.assertEqual(west["inputs"]["as_of"], "2026-09-22")
        self.assertEqual(east["inputs"]["as_of_source"], "current_timezone_clock")

    def test_explicit_date_overrides_clock_and_birth_timezone_is_not_current(self):
        module = load_context_module()
        with patch.object(module, "datetime") as clock:
            data = module.build_personal_context(date(1998, 3, 22), timezone="Asia/Shanghai", as_of=date(2026, 1, 1))
        clock.now.assert_not_called()
        self.assertIsNone(data["inputs"]["current_timezone"])
        self.assertEqual(data["inputs"]["as_of"], "2026-01-01")
        self.assertEqual(data["inputs"]["as_of_source"], "explicit_analysis_date")

    def test_host_date_fallback_is_disclosed(self):
        module = load_context_module()
        data = module.build_personal_context(date(1998, 3, 22))
        self.assertEqual(data["inputs"]["as_of_source"], "host_local_date_no_current_timezone")

    def test_unavailable_current_timezone_does_not_silently_use_host_date(self):
        module = load_context_module()
        with patch.object(module, "ZoneInfo", side_effect=module.ZoneInfoNotFoundError("unavailable")):
            with self.assertRaisesRegex(ValueError, "localized --as-of"):
                module.build_personal_context(date(1998, 3, 22), current_timezone="Pacific/Kiritimati")

    def test_invalid_timezone_is_rejected(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--birth-date",
                "1998-03-22",
                "--timezone",
                "Mars/Olympus",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown IANA timezone", result.stderr)

    def test_period_outside_helper_range_is_reported_without_crashing(self):
        data = run_context(
            "--birth-date",
            "1998-03-22",
            "--as-of",
            "2050-07-18",
        )

        self.assertEqual(data["current_context"]["san_yuan_period"]["status"], "unavailable")
        self.assertIn("1864-2043", data["current_context"]["san_yuan_period"]["reason"])


if __name__ == "__main__":
    unittest.main()
