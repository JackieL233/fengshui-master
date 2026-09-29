#!/usr/bin/env python3
"""Validate machine-readable FengShui Master artifacts against JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print(
        "error: jsonschema is required; install development dependencies with "
        "python -m pip install -r requirements-dev.txt",
        file=sys.stderr,
    )
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = {
    "examples/proactive-checkin-job.json": "schemas/proactive-checkin.schema.json",
    "portable-skill.json": "schemas/portable-skill.schema.json",
    "examples/portable-evaluation-suite.json": "schemas/portable-evaluation-suite.schema.json",
    "examples/user-journey-evaluation-suite.json": "schemas/user-journey-evaluation-suite.schema.json",
    "examples/reference-catalog.json": "schemas/reference-catalog.schema.json",
    "examples/tool-catalog.json": "schemas/tool-catalog.schema.json",
    "examples/response-contract.json": "schemas/response-contract.schema.json",
    "examples/capability-matrix.json": "schemas/capability-matrix.schema.json",
    "examples/source-quality-policy.json": "schemas/source-quality-policy.schema.json",
    "examples/adversarial-evaluation-suite.json": "schemas/adversarial-evaluation-suite.schema.json",
    "examples/intake-contracts.json": "schemas/intake-contracts.schema.json",
    "examples/golden-responses.json": "schemas/golden-responses.schema.json",
    "examples/universal-domain-protocol.json": "schemas/universal-domain-protocol.schema.json",
    "examples/external-calculation-contracts.json": "schemas/external-calculation-contracts.schema.json",
    "examples/contribution-quality-gates.json": "schemas/contribution-quality-gates.schema.json",
    "examples/runtime-integration-profiles.json": "schemas/runtime-integration-profiles.schema.json",
}


def load_json(relative_path: str) -> Any:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def format_path(parts: Any) -> str:
    values = [str(part) for part in parts]
    return ".".join(values) if values else "<root>"


def validate_instance(
    errors: list[str], instance: Any, schema: dict[str, Any], label: str
) -> None:
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema-error subclasses
        errors.append(f"{label} uses an invalid schema: {exc}")
        return
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        errors.append(f"{label} at {format_path(error.path)}: {error.message}")


def main() -> int:
    errors: list[str] = []
    try:
        for artifact_path, schema_path in ARTIFACTS.items():
            validate_instance(
                errors,
                load_json(artifact_path),
                load_json(schema_path),
                artifact_path,
            )

        policy = load_json("examples/claim-evidence-policy.json")
        validate_instance(
            errors,
            policy.get("valid_example"),
            load_json("schemas/agent-claims.schema.json"),
            "examples/claim-evidence-policy.json#valid_example",
        )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"JSON Schema validation passed for {len(ARTIFACTS) + 1} artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
