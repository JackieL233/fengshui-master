#!/usr/bin/env python3
"""Validate FengShui Master source quality and citation policy."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
POLICY = ROOT / "examples" / "source-quality-policy.json"
SCHEMA = ROOT / "schemas" / "source-quality-policy.schema.json"
REQUIRED_TIERS = {
    "classical_anchor",
    "scholarly_reference",
    "lineage_practice",
    "modern_adaptation",
    "practical_constraint",
}
REQUIRED_CLAIMS = {
    "classical_vocabulary",
    "school_overview",
    "lineage_formula",
    "modern_cross_domain_adapter",
    "high_stakes_domain_claim",
    "full_bazi_or_almanac_claim",
    "calendar_or_timing_claim",
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


def validate_string_list(errors: list[str], context: str, field: str, values: object) -> None:
    if not isinstance(values, list) or not values:
        fail(errors, f"{context} {field} must be a non-empty list")
        return
    if len(values) != len(set(values)):
        fail(errors, f"{context} {field} contains duplicates")
    for value in values:
        if not isinstance(value, str) or not value:
            fail(errors, f"{context} {field} contains invalid value")


def main() -> int:
    errors: list[str] = []
    manifest = load_json(errors, MANIFEST)
    policy = load_json(errors, POLICY)
    schema = load_json(errors, SCHEMA)

    if schema.get("title") != "FengShui Master Source Quality Policy":
        fail(errors, "source quality policy schema has wrong title")
    if policy.get("name") != "fengshui-master-source-quality-policy":
        fail(errors, "policy name must be fengshui-master-source-quality-policy")

    manifest_eval = set(manifest.get("evaluation", []))
    if "examples/source-quality-policy.json" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/source-quality-policy.json")
    if "examples/validate_source_quality_policy.py" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/validate_source_quality_policy.py")
    if manifest.get("schemas", {}).get("source_quality_policy") != "schemas/source-quality-policy.schema.json":
        fail(errors, "manifest schemas missing schemas/source-quality-policy.schema.json")

    tiers = policy.get("source_tiers", [])
    if not isinstance(tiers, list) or len(tiers) < 5:
        fail(errors, "source_tiers must contain at least 5 entries")
        tiers = []
    tiers_by_id: dict[str, dict] = {}
    for index, tier in enumerate(tiers):
        if not isinstance(tier, dict):
            fail(errors, f"source tier #{index + 1} must be an object")
            continue
        tier_id = tier.get("id")
        if not isinstance(tier_id, str) or not tier_id:
            fail(errors, f"source tier #{index + 1} missing id")
            continue
        if tier_id in tiers_by_id:
            fail(errors, f"duplicate source tier id: {tier_id}")
        tiers_by_id[tier_id] = tier
        for field in ["best_for", "acceptable_evidence", "limitations"]:
            validate_string_list(errors, tier_id, field, tier.get(field))
        if not isinstance(tier.get("output_posture"), str) or not tier.get("output_posture"):
            fail(errors, f"{tier_id} missing output_posture")

    missing_tiers = sorted(REQUIRED_TIERS - set(tiers_by_id))
    if missing_tiers:
        fail(errors, f"missing source tiers: {', '.join(missing_tiers)}")

    claims = policy.get("claim_policies", [])
    if not isinstance(claims, list) or len(claims) < 6:
        fail(errors, "claim_policies must contain at least 6 entries")
        claims = []
    claims_by_type: dict[str, dict] = {}
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            fail(errors, f"claim policy #{index + 1} must be an object")
            continue
        claim_type = claim.get("claim_type")
        if not isinstance(claim_type, str) or not claim_type:
            fail(errors, f"claim policy #{index + 1} missing claim_type")
            continue
        if claim_type in claims_by_type:
            fail(errors, f"duplicate claim policy: {claim_type}")
        claims_by_type[claim_type] = claim
        for field in ["minimum_sources", "required_labels", "required_checks", "red_lines"]:
            validate_string_list(errors, claim_type, field, claim.get(field))
        for tier_id in claim.get("minimum_sources", []):
            if tier_id not in tiers_by_id:
                fail(errors, f"{claim_type} references missing source tier {tier_id}")

    missing_claims = sorted(REQUIRED_CLAIMS - set(claims_by_type))
    if missing_claims:
        fail(errors, f"missing claim policies: {', '.join(missing_claims)}")

    modern = claims_by_type.get("modern_cross_domain_adapter", {})
    if "label as modern symbolic adaptation" not in modern.get("required_labels", []):
        fail(errors, "modern adapter policy missing adaptation label")
    if "do not present modern adapters as classical doctrine" not in modern.get("red_lines", []):
        fail(errors, "modern adapter policy missing classical doctrine red line")

    high_stakes = claims_by_type.get("high_stakes_domain_claim", {})
    if "professional boundary first" not in high_stakes.get("required_labels", []):
        fail(errors, "high-stakes policy missing professional boundary label")
    if "do not use feng shui as the deciding authority" not in high_stakes.get("red_lines", []):
        fail(errors, "high-stakes policy missing deciding authority red line")

    bazi = claims_by_type.get("full_bazi_or_almanac_claim", {})
    if bazi.get("support_level") != "out_of_scope_without_external_source":
        fail(errors, "full bazi or almanac policy must be out_of_scope_without_external_source")
    if "do not invent missing calculations" not in bazi.get("red_lines", []):
        fail(errors, "full bazi or almanac policy missing calculation red line")

    validate_string_list(errors, "policy", "citation_rules", policy.get("citation_rules"))
    validate_string_list(errors, "policy", "red_lines", policy.get("red_lines"))

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Source quality policy is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
