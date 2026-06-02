#!/usr/bin/env python3
"""Validate FengShui Master reference metadata catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
CATALOG = ROOT / "examples" / "reference-catalog.json"
RISK_LEVELS = {"low", "medium", "high", "critical"}


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
    manifest = load_json(errors, MANIFEST)
    catalog = load_json(errors, CATALOG)

    if catalog.get("name") != "fengshui-master-reference-catalog":
        fail(errors, "catalog name must be fengshui-master-reference-catalog")

    entries = catalog.get("references", [])
    if not isinstance(entries, list) or not entries:
        fail(errors, "catalog references must be a non-empty list")
        entries = []

    by_path: dict[str, dict] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(errors, f"entry #{index + 1} must be an object")
            continue

        path = entry.get("path")
        if not isinstance(path, str) or not path:
            fail(errors, f"entry #{index + 1} missing path")
            continue
        if path in by_path:
            fail(errors, f"duplicate catalog path: {path}")
        by_path[path] = entry
        if not (ROOT / path).exists():
            fail(errors, f"catalog path does not exist: {path}")

        for field in ["title", "primary_domain", "risk_level", "tags", "required_guardrails"]:
            if field not in entry:
                fail(errors, f"{path} missing {field}")
        if entry.get("risk_level") not in RISK_LEVELS:
            fail(errors, f"{path} has invalid risk_level {entry.get('risk_level')}")
        for field in ["tags", "required_guardrails"]:
            values = entry.get(field, [])
            if not isinstance(values, list) or not values:
                fail(errors, f"{path} {field} must be a non-empty list")
            elif len(values) != len(set(values)):
                fail(errors, f"{path} {field} contains duplicates")

    manifest_refs = set(manifest.get("references", []))
    catalog_refs = set(by_path)
    missing = sorted(manifest_refs - catalog_refs)
    extra = sorted(catalog_refs - manifest_refs)
    if missing:
        fail(errors, f"catalog missing manifest references: {', '.join(missing)}")
    if extra:
        fail(errors, f"catalog has references outside manifest: {', '.join(extra)}")

    required_high_guardrails = {
        "fengshui-master/references/finance-adapter.md": "not financial advice",
        "fengshui-master/references/wellbeing-adapter.md": "not medical advice",
        "fengshui-master/references/legal-adjacent-adapter.md": "not legal advice",
        "fengshui-master/references/life-and-omen-adapter.md": "no deterministic fate claims",
        "fengshui-master/references/ethics-and-limits.md": "no guaranteed prediction",
    }
    for path, guardrail in required_high_guardrails.items():
        entry = by_path.get(path)
        if not entry:
            continue
        if entry.get("risk_level") not in {"high", "critical"}:
            fail(errors, f"{path} must be high or critical risk")
        if guardrail not in entry.get("required_guardrails", []):
            fail(errors, f"{path} missing guardrail {guardrail}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Reference catalog is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
