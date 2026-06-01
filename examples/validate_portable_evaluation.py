#!/usr/bin/env python3
"""Validate the portable FengShui Master evaluation suite."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "examples" / "portable-evaluation-suite.json"
SCHEMA = ROOT / "schemas" / "portable-evaluation-suite.schema.json"
REQUIRED_DOMAINS = {"finance", "life_omen", "space", "brand_product", "legal_adjacent"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    if not SUITE.exists():
        fail(errors, f"missing {SUITE.relative_to(ROOT)}")
    else:
        try:
            suite = json.loads(SUITE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"invalid JSON: {exc}")
            suite = {}

        if suite.get("name") != "fengshui-master-portable-evaluation-suite":
            fail(errors, "suite name must be fengshui-master-portable-evaluation-suite")

        if not SCHEMA.exists():
            fail(errors, f"missing {SCHEMA.relative_to(ROOT)}")
        else:
            try:
                schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                fail(errors, f"invalid schema JSON: {exc}")
                schema = {}
            if schema.get("title") != "FengShui Master Portable Evaluation Suite":
                fail(errors, "portable evaluation schema has wrong title")

        cases = suite.get("cases", [])
        if not isinstance(cases, list) or len(cases) < 5:
            fail(errors, "suite must include at least five cases")
            cases = []

        domains = {case.get("domain") for case in cases if isinstance(case, dict)}
        missing_domains = sorted(REQUIRED_DOMAINS - domains)
        if missing_domains:
            fail(errors, f"missing domains: {', '.join(missing_domains)}")

        ids: set[str] = set()
        for index, case in enumerate(cases):
            if not isinstance(case, dict):
                fail(errors, f"case #{index + 1} must be an object")
                continue

            case_id = case.get("id")
            if not case_id:
                fail(errors, f"case #{index + 1} missing id")
            elif case_id in ids:
                fail(errors, f"duplicate case id: {case_id}")
            else:
                ids.add(case_id)

            if not case.get("prompt"):
                fail(errors, f"{case_id or index}: missing prompt")
            if not case.get("boundary_focus"):
                fail(errors, f"{case_id or index}: missing boundary_focus")

            references = case.get("expected_references", [])
            if len(references) < 2:
                fail(errors, f"{case_id or index}: expected_references must include at least two files")
            for rel in references:
                target = ROOT / rel
                if not target.exists():
                    fail(errors, f"{case_id or index}: missing expected reference {rel}")

            for field in ["must_include", "must_not_include"]:
                values = case.get(field, [])
                if len(values) < 3:
                    fail(errors, f"{case_id or index}: {field} must include at least three checks")
                if len(values) != len(set(values)):
                    fail(errors, f"{case_id or index}: {field} contains duplicate checks")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Portable evaluation suite is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
