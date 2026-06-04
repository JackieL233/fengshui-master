#!/usr/bin/env python3
"""Validate FengShui Master domain intake contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
CONTRACTS = ROOT / "examples" / "intake-contracts.json"
SCHEMA = ROOT / "schemas" / "intake-contracts.schema.json"
REQUIRED_DOMAINS = {
    "space",
    "finance",
    "timing",
    "life_omen",
    "business",
    "brand",
    "product",
    "relationship",
    "learning",
    "wellbeing",
    "legal_adjacent",
    "general",
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


def validate_string_list(errors: list[str], domain: str, field: str, values: object) -> None:
    if not isinstance(values, list) or not values:
        fail(errors, f"{domain} {field} must be a non-empty list")
        return
    if len(values) != len(set(values)):
        fail(errors, f"{domain} {field} contains duplicates")
    for value in values:
        if not isinstance(value, str) or not value:
            fail(errors, f"{domain} {field} contains invalid value")


def main() -> int:
    errors: list[str] = []
    manifest = load_json(errors, MANIFEST)
    contracts = load_json(errors, CONTRACTS)
    schema = load_json(errors, SCHEMA)

    if schema.get("title") != "FengShui Master Intake Contracts":
        fail(errors, "intake contracts schema has wrong title")
    if contracts.get("name") != "fengshui-master-intake-contracts":
        fail(errors, "contracts name must be fengshui-master-intake-contracts")

    manifest_eval = set(manifest.get("evaluation", []))
    if "examples/intake-contracts.json" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/intake-contracts.json")
    if "examples/validate_intake_contracts.py" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/validate_intake_contracts.py")
    if manifest.get("schemas", {}).get("intake_contracts") != "schemas/intake-contracts.schema.json":
        fail(errors, "manifest schemas missing schemas/intake-contracts.schema.json")

    entries = contracts.get("domains", [])
    if not isinstance(entries, list) or len(entries) < 10:
        fail(errors, "domains must contain at least 10 entries")
        entries = []

    by_domain: dict[str, dict] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(errors, f"domain #{index + 1} must be an object")
            continue
        domain = entry.get("domain")
        if not isinstance(domain, str) or not domain:
            fail(errors, f"domain #{index + 1} missing domain")
            continue
        if domain in by_domain:
            fail(errors, f"duplicate domain contract: {domain}")
        by_domain[domain] = entry
        for field in [
            "required_inputs",
            "optional_inputs",
            "ask_first_if_missing",
            "blocking_missing_inputs",
            "assumption_allowed_inputs",
            "boundary_disclosures",
            "red_lines",
            "routing_hints",
        ]:
            validate_string_list(errors, domain, field, entry.get(field))
        if len(entry.get("required_inputs", [])) < 3:
            fail(errors, f"{domain} required_inputs must include at least 3 items")
        if not isinstance(entry.get("summary"), str) or not entry.get("summary"):
            fail(errors, f"{domain} missing summary")

    missing_domains = sorted(REQUIRED_DOMAINS - set(by_domain))
    if missing_domains:
        fail(errors, f"missing domain contracts: {', '.join(missing_domains)}")

    finance = by_domain.get("finance", {})
    if "risk tolerance" not in finance.get("required_inputs", []):
        fail(errors, "finance missing risk tolerance required input")
    if "financial advice boundary" not in finance.get("boundary_disclosures", []):
        fail(errors, "finance missing financial advice boundary")
    if "do not issue buy/sell commands" not in finance.get("red_lines", []):
        fail(errors, "finance missing buy/sell red line")

    space = by_domain.get("space", {})
    if "floor plan or photos" not in space.get("required_inputs", []):
        fail(errors, "space missing floor plan or photos required input")
    if "north arrow or compass bearing" not in space.get("ask_first_if_missing", []):
        fail(errors, "space missing compass ask-first input")

    timing = by_domain.get("timing", {})
    if "candidate date or date range" not in timing.get("required_inputs", []):
        fail(errors, "timing missing candidate date input")
    if "event type" not in timing.get("blocking_missing_inputs", []):
        fail(errors, "timing missing event type blocking input")

    wellbeing = by_domain.get("wellbeing", {})
    if "not medical advice" not in wellbeing.get("boundary_disclosures", []):
        fail(errors, "wellbeing missing medical boundary")
    legal = by_domain.get("legal_adjacent", {})
    if "not legal advice" not in legal.get("boundary_disclosures", []):
        fail(errors, "legal_adjacent missing legal boundary")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Intake contracts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
