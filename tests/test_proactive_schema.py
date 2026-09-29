"""Keep the portable notification schema usable by third-party hosts."""

import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


class ProactiveSchemaTests(unittest.TestCase):
    def setUp(self):
        self.job = json.loads((ROOT / "examples/proactive-checkin-job.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/proactive-checkin.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.validator = Draft202012Validator(schema, format_checker=FormatChecker())

    def test_example_and_timezone_alias_shapes(self):
        for zone in ["Asia/Shanghai", "UTC", "GMT", "America/New_York"]:
            with self.subTest(zone=zone):
                self.job["subscription"]["timezone"] = zone
                self.validator.validate(self.job)

    def test_high_stakes_domains_require_native_basis(self):
        for domain in ["finance", "wellbeing", "legal_adjacent", "health", "medical", "safety"]:
            job = copy.deepcopy(self.job)
            job["event"]["domain"] = domain
            with self.subTest(domain=domain):
                self.assertFalse(self.validator.is_valid(job))
                job["event"]["native_basis"] = "User-supplied reality constraints; not verified by this schema."
                self.validator.validate(job)

    def test_due_time_required_and_must_have_offset(self):
        self.job["event"]["trigger"] = "review_due"
        self.assertFalse(self.validator.is_valid(self.job))
        self.job["event"]["due_at"] = "2026-09-29T09:30:00"
        self.assertFalse(self.validator.is_valid(self.job))
        self.job["event"]["due_at"] += "+08:00"
        self.validator.validate(self.job)
        for value in ["2026-09-29T09:30:00+08:60", "2026-09-29T09:30:00.0000009Z"]:
            with self.subTest(value=value):
                self.job["event"]["due_at"] = value
                self.assertFalse(self.validator.is_valid(self.job))

    def test_whitespace_boolean_quotas_and_extra_sensitive_ledger_data_rejected(self):
        for section, key, value in [
            ("event", "assessment", "   "),
            ("subscription", "max_per_day", True),
            ("state", "birth_date", "1998-03-22"),
        ]:
            with self.subTest(key=key):
                job = copy.deepcopy(self.job)
                job[section][key] = value
                self.assertFalse(self.validator.is_valid(job))


if __name__ == "__main__":
    unittest.main()
