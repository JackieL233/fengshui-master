#!/usr/bin/env python3
"""Validate FengShui Master capability and limitation matrix."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
MATRIX = ROOT / "examples" / "capability-matrix.json"
SCHEMA = ROOT / "schemas" / "capability-matrix.schema.json"
STATUSES = {"fully_covered", "partially_covered", "not_covered"}
REQUIRED_IDS = {
    "space-form-analysis",
    "bagua-compass-sector",
    "life-omen-symbolic-analysis",
    "finance-symbolic-decision-support",
    "new-moon-full-moon-timing",
    "portable-agent-integration",
    "full-bazi-four-pillars",
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


def validate_string_list(errors: list[str], entry_id: str, field: str, values: object, allow_empty: bool = False) -> None:
    if not isinstance(values, list):
        fail(errors, f"{entry_id} {field} must be a list")
        return
    if not values and not allow_empty:
        fail(errors, f"{entry_id} {field} must be non-empty")
        return
    if len(values) != len(set(values)):
        fail(errors, f"{entry_id} {field} contains duplicates")
    for value in values:
        if not isinstance(value, str) or not value:
            fail(errors, f"{entry_id} {field} contains invalid value")


def main() -> int:
    errors: list[str] = []
    manifest = load_json(errors, MANIFEST)
    matrix = load_json(errors, MATRIX)
    schema = load_json(errors, SCHEMA)

    if schema.get("title") != "FengShui Master Capability Matrix":
        fail(errors, "capability matrix schema has wrong title")
    if matrix.get("name") != "fengshui-master-capability-matrix":
        fail(errors, "matrix name must be fengshui-master-capability-matrix")
    if set(matrix.get("statuses", [])) != STATUSES:
        fail(errors, "matrix statuses must include fully_covered, partially_covered, and not_covered")

    manifest_eval = set(manifest.get("evaluation", []))
    if "examples/capability-matrix.json" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/capability-matrix.json")
    if "examples/validate_capability_matrix.py" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/validate_capability_matrix.py")
    if manifest.get("schemas", {}).get("capability_matrix") != "schemas/capability-matrix.schema.json":
        fail(errors, "manifest schemas missing schemas/capability-matrix.schema.json")

    capabilities = matrix.get("capabilities", [])
    if not isinstance(capabilities, list) or len(capabilities) < 12:
        fail(errors, "matrix capabilities must contain at least 12 entries")
        capabilities = []

    by_id: dict[str, dict] = {}
    manifest_refs = set(manifest.get("references", []))
    manifest_tools = set(manifest.get("tools", []))
    manifest_eval_tools = set(manifest.get("evaluation", []))
    extra_allowed_refs = {"PORTABLE_SKILL.md", "docs/integration-guide.md"}

    for index, entry in enumerate(capabilities):
        if not isinstance(entry, dict):
            fail(errors, f"capability #{index + 1} must be an object")
            continue
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            fail(errors, f"capability #{index + 1} missing id")
            continue
        if entry_id in by_id:
            fail(errors, f"duplicate capability id: {entry_id}")
        by_id[entry_id] = entry

        if entry.get("status") not in STATUSES:
            fail(errors, f"{entry_id} has invalid status {entry.get('status')}")
        for field in ["domains", "supported_questions", "required_inputs", "guardrails", "limitations", "adaptation_notes"]:
            validate_string_list(errors, entry_id, field, entry.get(field))
        validate_string_list(errors, entry_id, "references", entry.get("references"), allow_empty=entry.get("status") == "not_covered")
        validate_string_list(errors, entry_id, "optional_tools", entry.get("optional_tools"), allow_empty=True)

        for rel in entry.get("references", []):
            if rel not in manifest_refs and rel not in manifest_eval_tools and rel not in extra_allowed_refs:
                fail(errors, f"{entry_id} references path outside manifest/evaluation: {rel}")
            if not (ROOT / rel).exists():
                fail(errors, f"{entry_id} references missing path: {rel}")
        for rel in entry.get("optional_tools", []):
            if rel not in manifest_tools and rel not in manifest_eval_tools:
                fail(errors, f"{entry_id} optional tool outside manifest/evaluation: {rel}")
            if not (ROOT / rel).exists():
                fail(errors, f"{entry_id} optional tool missing path: {rel}")

    missing_ids = sorted(REQUIRED_IDS - set(by_id))
    if missing_ids:
        fail(errors, f"matrix missing required capabilities: {', '.join(missing_ids)}")

    expected_statuses = {
        "space-form-analysis": "fully_covered",
        "life-omen-symbolic-analysis": "fully_covered",
        "finance-symbolic-decision-support": "partially_covered",
        "new-moon-full-moon-timing": "partially_covered",
        "full-bazi-four-pillars": "not_covered",
    }
    for entry_id, status in expected_statuses.items():
        entry = by_id.get(entry_id)
        if entry and entry.get("status") != status:
            fail(errors, f"{entry_id} must be {status}")

    finance = by_id.get("finance-symbolic-decision-support", {})
    for guardrail in ["not financial advice", "do not issue buy/sell commands"]:
        if guardrail not in finance.get("guardrails", []):
            fail(errors, f"finance-symbolic-decision-support missing guardrail {guardrail}")

    moon = by_id.get("new-moon-full-moon-timing", {})
    if "fengshui-master/scripts/moon_phase.py" not in moon.get("optional_tools", []):
        fail(errors, "new-moon-full-moon-timing missing moon_phase.py tool")
    if "not a full almanac" not in moon.get("guardrails", []):
        fail(errors, "new-moon-full-moon-timing missing not a full almanac guardrail")

    bazi = by_id.get("full-bazi-four-pillars", {})
    if "complete four-pillar charting is outside current scope" not in bazi.get("limitations", []):
        fail(errors, "full-bazi-four-pillars missing explicit scope limitation")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Capability matrix is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
