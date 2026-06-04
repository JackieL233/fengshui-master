#!/usr/bin/env python3
"""Validate FengShui Master contribution quality gates."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
GATES = ROOT / "examples" / "contribution-quality-gates.json"
SCHEMA = ROOT / "schemas" / "contribution-quality-gates.schema.json"
REQUIRED_GATES = {
    "reference_addition",
    "tool_addition",
    "domain_adapter_addition",
    "external_calculation_integration",
    "evaluation_fixture_addition",
    "security_or_high_stakes_change",
    "documentation_or_metadata_change",
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
    gates = load_json(errors, GATES)
    schema = load_json(errors, SCHEMA)

    if schema.get("title") != "FengShui Master Contribution Quality Gates":
        fail(errors, "contribution quality gates schema has wrong title")
    if gates.get("name") != "fengshui-master-contribution-quality-gates":
        fail(errors, "gates name must be fengshui-master-contribution-quality-gates")

    manifest_eval = set(manifest.get("evaluation", []))
    if "examples/contribution-quality-gates.json" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/contribution-quality-gates.json")
    if "examples/validate_contribution_quality_gates.py" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/validate_contribution_quality_gates.py")
    if manifest.get("schemas", {}).get("contribution_quality_gates") != "schemas/contribution-quality-gates.schema.json":
        fail(errors, "manifest schemas missing schemas/contribution-quality-gates.schema.json")

    entries = gates.get("gates", [])
    if not isinstance(entries, list) or len(entries) < len(REQUIRED_GATES):
        fail(errors, f"gates must contain at least {len(REQUIRED_GATES)} entries")
        entries = []

    by_id: dict[str, dict] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(errors, f"gate #{index + 1} must be an object")
            continue
        gate_id = entry.get("id")
        if not isinstance(gate_id, str) or not gate_id:
            fail(errors, f"gate #{index + 1} missing id")
            continue
        if gate_id in by_id:
            fail(errors, f"duplicate gate: {gate_id}")
        by_id[gate_id] = entry
        for field in ["applies_to", "required_artifacts", "required_checks", "required_validation", "red_lines"]:
            validate_string_list(errors, gate_id, field, entry.get(field))

    missing = sorted(REQUIRED_GATES - set(by_id))
    if missing:
        fail(errors, f"missing gates: {', '.join(missing)}")

    external = by_id.get("external_calculation_integration", {})
    if "examples/external-calculation-contracts.json" not in external.get("required_artifacts", []):
        fail(errors, "external calculation gate missing external contract artifact")
    if "do not invent missing calculations" not in external.get("red_lines", []):
        fail(errors, "external calculation gate missing no-invent-calculations red line")

    tool = by_id.get("tool_addition", {})
    if "tests/test_<tool>.py" not in tool.get("required_artifacts", []):
        fail(errors, "tool gate missing tests artifact")
    if "python -m unittest discover -s tests" not in tool.get("required_validation", []):
        fail(errors, "tool gate missing unit test validation")

    security = by_id.get("security_or_high_stakes_change", {})
    if "examples/adversarial-evaluation-suite.json" not in security.get("required_artifacts", []):
        fail(errors, "security gate missing adversarial suite")
    if "do not weaken professional boundaries" not in security.get("red_lines", []):
        fail(errors, "security gate missing professional boundary red line")

    docs = by_id.get("documentation_or_metadata_change", {})
    if "README.zh-CN.md" not in docs.get("required_artifacts", []):
        fail(errors, "documentation gate missing Chinese README")
    if "python examples/validate_portable_manifest.py" not in docs.get("required_validation", []):
        fail(errors, "documentation gate missing manifest validation")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Contribution quality gates are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
