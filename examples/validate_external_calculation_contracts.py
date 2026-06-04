#!/usr/bin/env python3
"""Validate FengShui Master external calculation contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
CONTRACTS = ROOT / "examples" / "external-calculation-contracts.json"
SCHEMA = ROOT / "schemas" / "external-calculation-contracts.schema.json"
REQUIRED_SYSTEMS = {
    "full_bazi_four_pillars",
    "zi_wei_dou_shu",
    "qi_men_dun_jia",
    "liu_ren",
    "tong_shu_date_selection",
    "precision_astronomy_calendar",
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


def validate_string_list(errors: list[str], owner: str, field: str, values: object) -> None:
    if not isinstance(values, list) or not values:
        fail(errors, f"{owner} {field} must be a non-empty list")
        return
    if len(values) != len(set(values)):
        fail(errors, f"{owner} {field} contains duplicates")
    for value in values:
        if not isinstance(value, str) or not value:
            fail(errors, f"{owner} {field} contains invalid value")


def main() -> int:
    errors: list[str] = []
    manifest = load_json(errors, MANIFEST)
    contracts = load_json(errors, CONTRACTS)
    schema = load_json(errors, SCHEMA)

    if schema.get("title") != "FengShui Master External Calculation Contracts":
        fail(errors, "external calculation contracts schema has wrong title")
    if contracts.get("name") != "fengshui-master-external-calculation-contracts":
        fail(errors, "contracts name must be fengshui-master-external-calculation-contracts")

    manifest_eval = set(manifest.get("evaluation", []))
    if "examples/external-calculation-contracts.json" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/external-calculation-contracts.json")
    if "examples/validate_external_calculation_contracts.py" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/validate_external_calculation_contracts.py")
    if manifest.get("schemas", {}).get("external_calculation_contracts") != "schemas/external-calculation-contracts.schema.json":
        fail(errors, "manifest schemas missing schemas/external-calculation-contracts.schema.json")

    entries = contracts.get("systems", [])
    if not isinstance(entries, list) or len(entries) < 6:
        fail(errors, "systems must contain at least 6 entries")
        entries = []

    by_id: dict[str, dict] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(errors, f"system #{index + 1} must be an object")
            continue
        system_id = entry.get("id")
        if not isinstance(system_id, str) or not system_id:
            fail(errors, f"system #{index + 1} missing id")
            continue
        if system_id in by_id:
            fail(errors, f"duplicate system contract: {system_id}")
        by_id[system_id] = entry
        if entry.get("status") not in {"external_required", "external_or_user_supplied_source_required"}:
            fail(errors, f"{system_id} invalid status")
        for field in [
            "required_inputs",
            "required_source_proof",
            "required_outputs",
            "allowed_use",
            "red_lines",
        ]:
            validate_string_list(errors, system_id, field, entry.get(field))
        if not isinstance(entry.get("fallback_without_engine"), str) or not entry.get("fallback_without_engine"):
            fail(errors, f"{system_id} missing fallback_without_engine")

    missing_systems = sorted(REQUIRED_SYSTEMS - set(by_id))
    if missing_systems:
        fail(errors, f"missing systems: {', '.join(missing_systems)}")

    bazi = by_id.get("full_bazi_four_pillars", {})
    for required in ["birth date", "birth time", "calendar conversion convention"]:
        if required not in bazi.get("required_inputs", []):
            fail(errors, f"bazi missing required input {required}")
    if "do not invent missing pillars" not in bazi.get("red_lines", []):
        fail(errors, "bazi missing missing-pillars red line")

    ziwei = by_id.get("zi_wei_dou_shu", {})
    if "lunar calendar conversion" not in ziwei.get("required_inputs", []):
        fail(errors, "zi wei missing lunar calendar conversion input")
    if "do not fabricate stars" not in ziwei.get("red_lines", []):
        fail(errors, "zi wei missing fabricated-stars red line")

    qimen = by_id.get("qi_men_dun_jia", {})
    if "do not invent a qi men plate" not in qimen.get("red_lines", []):
        fail(errors, "qimen missing no-invent-plate red line")

    liuren = by_id.get("liu_ren", {})
    if "do not invent transmissions or lessons" not in liuren.get("red_lines", []):
        fail(errors, "liu ren missing no-invent-transmissions red line")

    almanac = by_id.get("tong_shu_date_selection", {})
    if "trusted almanac source" not in almanac.get("required_inputs", []):
        fail(errors, "tong shu missing trusted almanac source input")
    if "do not invent tong shu attributes" not in almanac.get("red_lines", []):
        fail(errors, "tong shu missing no-invent-attributes red line")

    astronomy = by_id.get("precision_astronomy_calendar", {})
    if astronomy.get("status") != "external_required":
        fail(errors, "precision astronomy must require an external engine")
    if "do not present approximate helper output as precision astronomy" not in astronomy.get("red_lines", []):
        fail(errors, "precision astronomy missing approximate-helper red line")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("External calculation contracts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
