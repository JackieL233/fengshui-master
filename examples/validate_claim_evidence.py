#!/usr/bin/env python3
"""Validate the claim-evidence policy and optional agent-claims JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "examples" / "claim-evidence-policy.json"
SCHEMA_PATH = ROOT / "schemas" / "agent-claims.schema.json"
STATUSES = {"observed", "calculated", "inferred", "unknown", "recommended"}
CONFIDENCE_LEVELS = {"high", "medium", "low", "not_applicable"}
POINTER_PREFIXES = ("user:", "artifact:", "tool:", "source:", "claim:")
HIGH_STAKES = {"finance", "medical", "legal", "engineering", "safety"}
COMMON_FIELDS = {"id", "text", "status", "confidence", "method", "evidence_refs", "falsifiers"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def non_empty_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def validate_policy(policy: Any, schema: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(policy, dict):
        return ["policy must be an object"]
    if policy.get("name") != "fengshui-master-claim-evidence-policy":
        errors.append("policy has wrong name")
    if schema.get("title") != "FengShui Master Agent Claims":
        errors.append("agent-claims schema has wrong title")
    if set(policy.get("statuses", {})) != STATUSES:
        errors.append("policy statuses are incomplete")
    if set(policy.get("required_common_fields", [])) != COMMON_FIELDS:
        errors.append("required_common_fields are incomplete")
    if tuple(policy.get("evidence_pointer_prefixes", [])) != POINTER_PREFIXES:
        errors.append("evidence pointer prefixes are incomplete or out of order")
    if not policy.get("cold_reading_rule") or not policy.get("high_stakes_rule"):
        errors.append("policy must define cold-reading and high-stakes rules")
    example = policy.get("valid_example")
    errors.extend(validate_claim_document(example, prefix="valid_example"))
    return errors


def validate_claim_document(payload: Any, prefix: str = "document") -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict) or not isinstance(payload.get("claims"), list):
        return [f"{prefix}.claims must be a list"]

    seen_ids: set[str] = set()
    for index, claim in enumerate(payload["claims"]):
        label = f"{prefix}.claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = sorted(COMMON_FIELDS - set(claim))
        if missing:
            errors.append(f"{label} missing common fields: {', '.join(missing)}")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            errors.append(f"{label}.id must be a non-empty string")
        elif claim_id in seen_ids:
            errors.append(f"duplicate claim id: {claim_id}")
        else:
            seen_ids.add(claim_id)
        if not isinstance(claim.get("text"), str) or not claim["text"].strip():
            errors.append(f"{label}.text must be a non-empty string")
        status = claim.get("status")
        if status not in STATUSES:
            errors.append(f"{label}.status is invalid")
            continue
        if claim.get("confidence") not in CONFIDENCE_LEVELS:
            errors.append(f"{label}.confidence is invalid")
        if not isinstance(claim.get("method"), str) or not claim["method"].strip():
            errors.append(f"{label}.method must be a non-empty string")
        evidence_refs = claim.get("evidence_refs")
        falsifiers = claim.get("falsifiers")
        if not non_empty_strings(evidence_refs):
            errors.append(f"{label}.evidence_refs must be a string list")
            evidence_refs = []
        elif any(not item.startswith(POINTER_PREFIXES) for item in evidence_refs):
            errors.append(f"{label}.evidence_refs contains an unsupported pointer")
        if not non_empty_strings(falsifiers):
            errors.append(f"{label}.falsifiers must contain at least one testable condition")

        if status == "observed" and not any(
            item.startswith(("user:", "artifact:")) for item in evidence_refs
        ):
            errors.append(f"{label} observed claim requires a user: or artifact: pointer")
        if status == "calculated":
            calculation = claim.get("calculation")
            if not isinstance(calculation, dict) or not all(
                field in calculation for field in ["tool", "inputs", "method"]
            ):
                errors.append(f"{label} calculated claim requires tool, inputs, and method provenance")
            if not any(item.startswith("tool:") for item in evidence_refs):
                errors.append(f"{label} calculated claim requires a tool: pointer")
        if status == "inferred" and not non_empty_strings(claim.get("basis_refs")):
            errors.append(f"{label} inferred claim requires concrete basis_refs")
        if status == "unknown" and not non_empty_strings(claim.get("missing_inputs")):
            errors.append(f"{label} unknown claim requires missing_inputs")
        if status == "recommended":
            if not non_empty_strings(claim.get("based_on")):
                errors.append(f"{label} recommendation requires based_on")
            if claim.get("reversibility") not in {
                "reversible",
                "partly_reversible",
                "irreversible",
            }:
                errors.append(f"{label} recommendation requires reversibility")
            if not isinstance(claim.get("verification"), str) or not claim["verification"].strip():
                errors.append(f"{label} recommendation requires verification")
        if claim.get("high_stakes_domain") in HIGH_STAKES and not claim.get("boundary_ref"):
            errors.append(f"{label} high-stakes claim requires boundary_ref")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate claim-evidence policy and an optional agent-claims JSON document."
    )
    parser.add_argument("path", nargs="?", help="Optional JSON document containing a claims array.")
    args = parser.parse_args()

    try:
        policy = load_json(POLICY_PATH)
        schema = load_json(SCHEMA_PATH)
        errors = validate_policy(policy, schema)
        if args.path:
            errors.extend(validate_claim_document(load_json(Path(args.path))))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Claim-evidence policy and claims are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
