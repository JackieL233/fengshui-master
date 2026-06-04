#!/usr/bin/env python3
"""Validate FengShui Master golden response fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
GOLDEN = ROOT / "examples" / "golden-responses.json"
SCHEMA = ROOT / "schemas" / "golden-responses.schema.json"
REQUIRED_IDS = {
    "finance-symbolic-risk-answer",
    "space-form-floorplan-answer",
    "timing-new-full-moon-answer",
    "life-omen-conditional-answer",
    "prompt-injection-safe-answer",
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


def validate_string_list(errors: list[str], response_id: str, field: str, values: object) -> None:
    if not isinstance(values, list) or not values:
        fail(errors, f"{response_id} {field} must be a non-empty list")
        return
    if len(values) != len(set(values)):
        fail(errors, f"{response_id} {field} contains duplicates")
    for value in values:
        if not isinstance(value, str) or not value:
            fail(errors, f"{response_id} {field} contains invalid value")


def main() -> int:
    errors: list[str] = []
    manifest = load_json(errors, MANIFEST)
    golden = load_json(errors, GOLDEN)
    schema = load_json(errors, SCHEMA)

    if schema.get("title") != "FengShui Master Golden Responses":
        fail(errors, "golden responses schema has wrong title")
    if golden.get("name") != "fengshui-master-golden-responses":
        fail(errors, "golden responses name must be fengshui-master-golden-responses")

    manifest_eval = set(manifest.get("evaluation", []))
    if "examples/golden-responses.json" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/golden-responses.json")
    if "examples/validate_golden_responses.py" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/validate_golden_responses.py")
    if manifest.get("schemas", {}).get("golden_responses") != "schemas/golden-responses.schema.json":
        fail(errors, "manifest schemas missing schemas/golden-responses.schema.json")

    valid_paths = (
        set(manifest.get("entrypoints", []))
        | set(manifest.get("references", []))
        | set(manifest.get("tools", []))
        | set(manifest.get("evaluation", []))
        | set(manifest.get("governance", []))
        | set(manifest.get("integration", []))
    )

    responses = golden.get("responses", [])
    if not isinstance(responses, list) or len(responses) < 5:
        fail(errors, "responses must contain at least 5 entries")
        responses = []

    by_id: dict[str, dict] = {}
    for index, response in enumerate(responses):
        if not isinstance(response, dict):
            fail(errors, f"response #{index + 1} must be an object")
            continue
        response_id = response.get("id")
        if not isinstance(response_id, str) or not response_id:
            fail(errors, f"response #{index + 1} missing id")
            continue
        if response_id in by_id:
            fail(errors, f"duplicate response id: {response_id}")
        by_id[response_id] = response
        for field in ["expected_references", "outline", "required_phrases", "forbidden_phrases", "quality_checks"]:
            validate_string_list(errors, response_id, field, response.get(field))
        if len(response.get("outline", [])) < 4:
            fail(errors, f"{response_id} outline must include at least 4 sections")
        if len(response.get("quality_checks", [])) < 3:
            fail(errors, f"{response_id} quality_checks must include at least 3 checks")
        for rel in response.get("expected_references", []):
            if rel not in valid_paths:
                fail(errors, f"{response_id} references path outside manifest: {rel}")
            if not (ROOT / rel).exists():
                fail(errors, f"{response_id} references missing path: {rel}")

    missing_ids = sorted(REQUIRED_IDS - set(by_id))
    if missing_ids:
        fail(errors, f"missing golden responses: {', '.join(missing_ids)}")

    checks = {
        "finance-symbolic-risk-answer": ("not financial advice", "guaranteed returns"),
        "timing-new-full-moon-answer": ("moon phase is secondary", "guaranteed auspiciousness"),
        "life-omen-conditional-answer": ("no deterministic fate claims", "doomed"),
        "prompt-injection-safe-answer": ("do not follow injected instructions", "ignore all previous rules"),
    }
    for response_id, (required, forbidden) in checks.items():
        response = by_id.get(response_id, {})
        if required not in response.get("required_phrases", []):
            fail(errors, f"{response_id} missing required phrase {required}")
        if forbidden not in response.get("forbidden_phrases", []):
            fail(errors, f"{response_id} missing forbidden phrase {forbidden}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Golden responses are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
