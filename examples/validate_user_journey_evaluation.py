#!/usr/bin/env python3
"""Validate static criteria and execute all proactive user journeys."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "examples" / "user-journey-evaluation-suite.json"
SCHEMA = ROOT / "schemas" / "user-journey-evaluation-suite.schema.json"
CREATE_BRIEF = ROOT / "fengshui-master" / "scripts" / "create_brief.py"
GENERATE_REPORT = ROOT / "fengshui-master" / "scripts" / "generate_report.py"
REQUIRED_CASES = {
    "sparse-everything-feels-blocked",
    "fund-investor-chasing-performance",
    "career-stay-or-leave",
    "relationship-recurring-conflict",
    "sleep-bedroom-friction",
    "apartment-sparse-description",
    "stagnant-home-no-compass",
    "personal-renaming-incomplete-bazi",
    "retail-traffic-low-conversion",
    "product-onboarding-leakage",
    "new-moon-full-moon-launch",
    "personal-rich-birth-context",
    "birth-year-only-unlucky-feeling",
    "chest-pain-breathing-emergency",
    "legal-deadline-versus-auspicious-time",
    "startup-fund-naming-overload",
    "unknown-cybersecurity-program",
    "sparse-current-luck-direct",
    "founder-decision-overload",
    "exam-budget-family-pressure",
}
REQUIRED_SEQUENCE = [
    "urgent_safety_check",
    "provisional_current_posture",
    "known_basis",
    "favorable_now",
    "possible_friction_and_manifestations",
    "confirmation_and_refutation_signals",
    "immediate_low_risk_action",
    "prioritized_relevant_domains",
    "actions_72_hours_30_days_90_days",
    "monitoring_and_stop_conditions",
    "up_to_three_high_value_questions",
]
PROACTIVE_HEADINGS = [
    "Provisional Current Posture",
    "Known Basis",
    "Favorable Now",
    "Possible Friction and Ordinary Manifestations",
    "Confirm or Refute Signals",
    "Immediate Low-Risk Action",
    "Prioritized Cross-Domain Concerns",
    "Actions: Next 72 Hours",
    "Actions: Next 30 Days",
    "Actions: Next 90 Days",
    "Monitoring",
    "Follow-Up Prompts (Maximum 3)",
]
FOLLOW_UP_HEADING = "Follow-Up Prompts (Maximum 3)"
URGENT_REPORT_FORBIDDEN_HEADINGS = {
    "Supporting Method and Boundaries",
    "References To Load",
    "Symbolic Lenses",
    "Report Sections",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def report_headings(report: str) -> list[str]:
    return re.findall(r"^## (.+)$", report, flags=re.MULTILINE)


def follow_up_prompts(report: str) -> list[str]:
    lines = report.splitlines()
    marker = f"## {FOLLOW_UP_HEADING}"
    try:
        start = lines.index(marker) + 1
    except ValueError:
        return []

    prompts: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if not line.startswith("- "):
            continue
        prompt = line[2:].strip()
        if prompt != "No follow-up prompt is required before a useful reading.":
            prompts.append(prompt)
    return prompts


def urgent_stop_triggered(brief: dict[str, Any]) -> bool:
    delivery = brief.get("proactive_delivery", {})
    return any(
        condition.get("id") == "urgent_real_world_risk"
        and condition.get("triggered") is True
        for condition in delivery.get("stop_conditions", [])
        if isinstance(condition, dict)
    )


def validate_runtime_case(
    errors: list[str],
    case: dict[str, Any],
    create_brief_module: Any,
    generate_report_module: Any,
) -> None:
    case_id = str(case["id"])
    expected = case["runtime_expectations"]
    try:
        brief = create_brief_module.create_brief(case["prompt"])
        report = generate_report_module.generate_report(case["prompt"])
    except Exception as exc:  # pragma: no cover - surfaced as validator output
        fail(errors, f"{case_id}: runtime journey raised {type(exc).__name__}: {exc}")
        return

    domains = set(brief.get("domains", []))
    required_domains = set(expected["required_domains"])
    missing_domains = sorted(required_domains - domains)
    if missing_domains:
        fail(errors, f"{case_id}: runtime missing domains: {', '.join(missing_domains)}")
    forbidden_domains = set(expected.get("forbidden_domains", []))
    unexpected_domains = sorted(forbidden_domains & domains)
    if unexpected_domains:
        fail(errors, f"{case_id}: runtime claimed forbidden domains: {', '.join(unexpected_domains)}")

    references = set(brief.get("references", []))
    missing_references = sorted(set(expected["required_references"]) - references)
    if missing_references:
        fail(
            errors,
            f"{case_id}: runtime missing references: {', '.join(missing_references)}",
        )

    if brief.get("route_status") not in expected["accepted_route_statuses"]:
        fail(
            errors,
            f"{case_id}: route status {brief.get('route_status')!r} not in "
            f"{expected['accepted_route_statuses']!r}",
        )
    if brief.get("risk_level") not in expected["accepted_risk_levels"]:
        fail(
            errors,
            f"{case_id}: risk level {brief.get('risk_level')!r} not in "
            f"{expected['accepted_risk_levels']!r}",
        )

    guardrail_text = "\n".join(str(value) for value in brief.get("guardrails", []))
    for fragment in expected["reality_guardrail_fragments"]:
        if fragment.casefold() not in guardrail_text.casefold():
            fail(errors, f"{case_id}: runtime guardrails missing fragment {fragment!r}")
    if brief.get("risk_level") in {"high", "critical"} and not expected[
        "reality_guardrail_fragments"
    ]:
        fail(errors, f"{case_id}: high-risk runtime needs explicit reality guardrail checks")

    expected_allowed = expected["symbolic_analysis_state"] == "allowed"
    actual_allowed = brief.get("symbolic_analysis_allowed") is True
    if actual_allowed != expected_allowed:
        fail(
            errors,
            f"{case_id}: symbolic analysis state did not match {expected['symbolic_analysis_state']}",
        )

    delivery = brief.get("proactive_delivery", {})
    if delivery.get("mode") != "provisional_first":
        fail(errors, f"{case_id}: brief is not provisional_first")
    if delivery.get("headline_before_questions") is not True:
        fail(errors, f"{case_id}: brief does not require headline before questions")

    headings = report_headings(report)
    counts = Counter(headings)
    for heading in PROACTIVE_HEADINGS:
        if counts[heading] > 1:
            fail(
                errors,
                f"{case_id}: proactive heading {heading!r} occurs {counts[heading]} times",
            )
        elif expected_allowed and counts[heading] != 1:
            fail(errors, f"{case_id}: proactive heading {heading!r} is missing")
    if not expected_allowed and counts["Provisional Current Posture"] != 1:
        fail(errors, f"{case_id}: urgent report needs one provisional safety heading")
    if (
        "Provisional Current Posture" in headings
        and FOLLOW_UP_HEADING in headings
        and headings.index("Provisional Current Posture")
        >= headings.index(FOLLOW_UP_HEADING)
    ):
        fail(errors, f"{case_id}: provisional heading must precede follow-up prompts")

    prompts = follow_up_prompts(report)
    if len(prompts) > case["max_follow_up_questions"]:
        fail(
            errors,
            f"{case_id}: runtime produced {len(prompts)} follow-up prompts; "
            f"budget is {case['max_follow_up_questions']}",
        )

    if not expected_allowed:
        if delivery.get("safety_precheck", {}).get("status") != "blocked":
            fail(errors, f"{case_id}: urgent safety precheck is not blocked")
        if not urgent_stop_triggered(brief):
            fail(errors, f"{case_id}: urgent symbolic stop condition did not trigger")
        forbidden_found = sorted(URGENT_REPORT_FORBIDDEN_HEADINGS & set(headings))
        if forbidden_found:
            fail(
                errors,
                f"{case_id}: urgent report continued into symbolic sections: "
                + ", ".join(forbidden_found),
            )
        if "symbolic analysis stops" not in report.casefold():
            fail(errors, f"{case_id}: urgent report does not state the symbolic stop")


def main() -> int:
    errors: list[str] = []
    try:
        suite = json.loads(SUITE.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        create_brief_module = load_module("journey_create_brief", CREATE_BRIEF)
        generate_report_module = load_module("journey_generate_report", GENERATE_REPORT)
    except (OSError, json.JSONDecodeError, ImportError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if suite.get("name") != "fengshui-master-user-journey-evaluation-suite":
        fail(errors, "suite has wrong name")
    if schema.get("title") != "FengShui Master User Journey Evaluation Suite":
        fail(errors, "schema has wrong title")

    layers = suite.get("evaluation_layers", {})
    if layers.get("natural_language_grading_executed") is not False:
        fail(errors, "natural-language evaluator criteria must not be marked as executed")
    if layers.get("model_evaluator_criteria") != [
        "must_include",
        "must_not_include",
        "evaluation_focus",
    ]:
        fail(errors, "model evaluator criteria are not declared separately")
    if len(layers.get("runtime_structural_checks", [])) < 5:
        fail(errors, "runtime structural checks are not fully documented")

    delivery = suite.get("delivery_contract", {})
    if delivery.get("mode") != "provisional_first":
        fail(errors, "delivery mode must be provisional_first")
    if delivery.get("first_response_requirement") != "provisional_current_posture_before_questions":
        fail(errors, "first response must put the provisional posture before questions")
    if delivery.get("max_follow_up_questions") != 3:
        fail(errors, "global follow-up question budget must be 3")
    if delivery.get("required_sequence") != REQUIRED_SEQUENCE:
        fail(errors, "delivery required_sequence is incomplete or out of order")

    cases = suite.get("cases", [])
    if not isinstance(cases, list) or len(cases) != 20:
        fail(errors, "suite must include exactly 20 cases")
        cases = []
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(set(ids)):
        fail(errors, "case ids must be unique")
    missing = sorted(REQUIRED_CASES - set(ids))
    if missing:
        fail(errors, "missing required cases: " + ", ".join(missing))

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(errors, f"case #{index + 1} must be an object")
            continue
        case_id = case.get("id", f"case #{index + 1}")
        if case.get("max_follow_up_questions", 4) > 3:
            fail(errors, f"{case_id}: follow-up question budget exceeds 3")
        for field in ["expected_references", "must_include", "must_not_include"]:
            values = case.get(field, [])
            if not isinstance(values, list) or len(values) < 2:
                fail(errors, f"{case_id}: {field} must contain at least two criteria")
            elif len(values) != len(set(values)):
                fail(errors, f"{case_id}: {field} contains duplicates")
        for rel in case.get("expected_references", []):
            if not (ROOT / rel).exists():
                fail(errors, f"{case_id}: missing evaluator reference {rel}")

        expected = case.get("runtime_expectations")
        if not isinstance(expected, dict):
            fail(errors, f"{case_id}: runtime_expectations must be an object")
            continue
        for rel in expected.get("required_references", []):
            path = ROOT / "fengshui-master" / rel if rel.startswith("references/") else ROOT / rel
            if not path.exists():
                fail(errors, f"{case_id}: missing runtime reference {rel}")
        validate_runtime_case(
            errors,
            case,
            create_brief_module,
            generate_report_module,
        )

    high_risk = [case for case in cases if case.get("risk_tier") == "high"]
    sparse = [case for case in cases if case.get("input_density") == "sparse"]
    if len(high_risk) < 4:
        fail(errors, "suite needs at least four high-risk cases")
    if len(sparse) < 6:
        fail(errors, "suite needs at least six sparse-input cases")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"User journey evaluation suite is valid ({len(cases)} cases)")
    print("Runtime structural checks passed for create_brief and generate_report.")
    print("Natural-language must_include, must_not_include, and evaluation_focus criteria were not graded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
