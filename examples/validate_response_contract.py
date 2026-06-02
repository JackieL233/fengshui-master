#!/usr/bin/env python3
"""Validate FengShui Master portable response contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "examples" / "response-contract.json"
RUBRIC = ROOT / "examples" / "portable-evaluation-rubric.json"
SCHEMA = ROOT / "schemas" / "response-contract.schema.json"
REQUIRED_SECTIONS = {
    "inputs_and_assumptions",
    "domain_reality_check",
    "method_and_symbolic_lenses",
    "observations_and_interpretations",
    "conditional_ji_xiong_assessment",
    "recommendations",
    "confidence_and_missing_data",
    "boundaries",
}
REQUIRED_DISCLOSURES = {
    "not financial advice",
    "not medical advice",
    "not legal advice",
    "not engineering, architectural, or safety advice",
    "no deterministic fate claims",
}
REQUIRED_RULE_TERMS = {
    "real-world constraints",
    "deterministic scripts",
    "moon phase",
    "reversible",
    "final authority",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(errors: list[str], path: Path) -> dict:
    if not path.exists():
        fail(errors, f"missing {path.relative_to(ROOT)}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}


def main() -> int:
    errors: list[str] = []
    contract = load_json(errors, CONTRACT)
    rubric = load_json(errors, RUBRIC)
    schema = load_json(errors, SCHEMA)

    if contract.get("name") != "fengshui-master-response-contract":
        fail(errors, "contract name must be fengshui-master-response-contract")
    if schema.get("title") != "FengShui Master Response Contract":
        fail(errors, "response contract schema has wrong title")

    sections = contract.get("required_sections", [])
    if not isinstance(sections, list) or not sections:
        fail(errors, "required_sections must be a non-empty list")
        sections = []
    section_names = {section.get("name") for section in sections if isinstance(section, dict)}
    missing_sections = sorted(REQUIRED_SECTIONS - section_names)
    if missing_sections:
        fail(errors, f"missing required sections: {', '.join(missing_sections)}")
    for section in sections:
        if not isinstance(section, dict):
            fail(errors, "required_sections entries must be objects")
            continue
        if section.get("required") is not True:
            fail(errors, f"section {section.get('name')} must be required")
        if not section.get("purpose"):
            fail(errors, f"section {section.get('name')} missing purpose")
        applies_to = section.get("applies_to", [])
        if not isinstance(applies_to, list) or not applies_to:
            fail(errors, f"section {section.get('name')} applies_to must be non-empty")

    disclosures = contract.get("high_stakes_disclosures", [])
    disclosure_texts = {
        disclosure.get("required_text")
        for disclosure in disclosures
        if isinstance(disclosure, dict)
    }
    missing_disclosures = sorted(REQUIRED_DISCLOSURES - disclosure_texts)
    if missing_disclosures:
        fail(errors, f"missing disclosures: {', '.join(missing_disclosures)}")
    for disclosure in disclosures:
        if not isinstance(disclosure, dict):
            fail(errors, "high_stakes_disclosures entries must be objects")
            continue
        for field in ["trigger", "required_text", "professional_priority"]:
            if not disclosure.get(field):
                fail(errors, f"disclosure missing {field}")

    answer_rules = contract.get("answer_rules", [])
    rules_text = " ".join(answer_rules).lower() if isinstance(answer_rules, list) else ""
    for term in REQUIRED_RULE_TERMS:
        if term not in rules_text:
            fail(errors, f"answer_rules missing {term}")

    red_lines = contract.get("red_lines", [])
    rubric_red_lines = rubric.get("red_lines", []) if isinstance(rubric, dict) else []
    if not isinstance(red_lines, list) or len(red_lines) < len(rubric_red_lines):
        fail(errors, "contract red_lines must cover at least the rubric red line count")
    red_line_text = " ".join(red_lines).lower() if isinstance(red_lines, list) else ""
    for term in ["guaranteed", "buy/sell", "doomed", "safety", "complete bazi"]:
        if term not in red_line_text:
            fail(errors, f"red_lines missing {term}")

    output_modes = contract.get("output_modes", [])
    mode_names = {mode.get("name") for mode in output_modes if isinstance(mode, dict)}
    for mode in ["brief_answer", "full_report"]:
        if mode not in mode_names:
            fail(errors, f"output_modes missing {mode}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Response contract is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
