"""Regression checks for the portable multi-turn interaction contract."""

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_response_contract", ROOT / "examples/validate_response_contract.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class DialogueContractTests(unittest.TestCase):
    def setUp(self):
        contract = json.loads((ROOT / "examples/response-contract.json").read_text(encoding="utf-8"))
        self.defaults = contract["conversation_defaults"]

    def test_bundled_contract_is_valid(self):
        self.assertEqual(validator.validate_conversation_defaults(self.defaults), [])

    def test_missing_or_non_object_contract_is_rejected(self):
        for value in [None, [], "", False]:
            with self.subTest(value=value):
                self.assertTrue(validator.validate_conversation_defaults(value))

    def test_repeated_question_and_memory_regressions_are_rejected(self):
        for field, bad in {
            "repeat_known_questions": True,
            "repeat_declined_questions": True,
            "question_budget_is_target": True,
            "context_scope": "permanent_memory",
            "follow_up_mode": "restart_intake",
        }.items():
            with self.subTest(field=field):
                self.assertTrue(validator.validate_conversation_defaults({**self.defaults, field: bad}))

    def test_numeric_zero_does_not_satisfy_boolean_contract(self):
        self.assertTrue(validator.validate_conversation_defaults(
            {**self.defaults, "repeat_known_questions": 0}
        ))

    def test_empty_correction_freshness_and_consent_rules_are_rejected(self):
        for field in ["correction_policy", "freshness_policy", "no_new_evidence_policy", "consent_policy", "response_depth"]:
            with self.subTest(field=field):
                self.assertTrue(validator.validate_conversation_defaults({**self.defaults, field: " "}))


class ConversationContextIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "dialogue_report", ROOT / "fengshui-master/scripts/generate_report.py"
        )
        cls.report = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.report)

    def test_supplied_context_flows_from_brief_to_report_without_reasking(self):
        known = {
            "time horizon": "Three years",
            "risk tolerance": "A loss must not affect essential expenses",
            "liquidity needs": "Emergency savings are separate",
        }
        brief = self.report.brief_module.create_brief("Review my fund investing habits", known_inputs=known)
        questions = self.report.follow_up_prompts(brief)
        for label in known:
            self.assertNotIn(self.report.phrase_missing_input(label), questions)
        report = self.report.generate_report("Review my fund investing habits", known_inputs=known)
        for value in known.values():
            self.assertIn(value, report)

    def test_correction_replaces_value_without_implicit_memory(self):
        brief = self.report.brief_module
        first = brief.create_brief("Review my fund investing habits", known_inputs={"time horizon": "Five years"})
        corrected = brief.create_brief("Review my fund investing habits", known_inputs={"time horizon": "Six months"})
        self.assertEqual(first["input_state"]["provided_values"]["time horizon"], "Five years")
        self.assertEqual(corrected["input_state"]["provided_values"]["time horizon"], "Six months")
        fresh = brief.create_brief("Review my fund investing habits")
        self.assertIn("time horizon", fresh["missing_inputs"])
        self.assertNotIn("provided_values", fresh["input_state"])


if __name__ == "__main__":
    unittest.main()
