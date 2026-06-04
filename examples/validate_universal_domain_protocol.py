#!/usr/bin/env python3
"""Validate FengShui Master universal domain adaptation protocol."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
PROTOCOL = ROOT / "examples" / "universal-domain-protocol.json"
SCHEMA = ROOT / "schemas" / "universal-domain-protocol.schema.json"
REQUIRED_STAGE_IDS = {
    "classify_native_domain",
    "rate_domain_risk",
    "collect_minimum_inputs",
    "apply_symbolic_lenses",
    "produce_bounded_answer",
}
REQUIRED_RISK_IDS = {"low", "medium", "high", "critical"}
REQUIRED_RULE_IDS = {
    "native_domain_first",
    "symbolic_layer_second",
    "wuxing_bridge",
    "unsupported_calculation_boundary",
}
REQUIRED_EXAMPLE_DOMAINS = {"technology", "sports", "education", "finance", "unknown"}


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
    protocol = load_json(errors, PROTOCOL)
    schema = load_json(errors, SCHEMA)

    if schema.get("title") != "FengShui Master Universal Domain Protocol":
        fail(errors, "universal domain protocol schema has wrong title")
    if protocol.get("name") != "fengshui-master-universal-domain-protocol":
        fail(errors, "protocol name must be fengshui-master-universal-domain-protocol")

    manifest_eval = set(manifest.get("evaluation", []))
    if "examples/universal-domain-protocol.json" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/universal-domain-protocol.json")
    if "examples/validate_universal_domain_protocol.py" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/validate_universal_domain_protocol.py")
    if manifest.get("schemas", {}).get("universal_domain_protocol") != "schemas/universal-domain-protocol.schema.json":
        fail(errors, "manifest schemas missing schemas/universal-domain-protocol.schema.json")

    stages = protocol.get("stages", [])
    if not isinstance(stages, list) or len(stages) < 5:
        fail(errors, "stages must contain at least 5 entries")
        stages = []
    stage_ids: set[str] = set()
    for stage in stages:
        if not isinstance(stage, dict):
            fail(errors, "stage entries must be objects")
            continue
        stage_id = stage.get("id")
        if not isinstance(stage_id, str) or not stage_id:
            fail(errors, "stage missing id")
            continue
        stage_ids.add(stage_id)
        validate_string_list(errors, stage_id, "required_actions", stage.get("required_actions"))
        if not stage.get("goal") or not stage.get("output"):
            fail(errors, f"{stage_id} missing goal or output")
    for stage_id in sorted(REQUIRED_STAGE_IDS - stage_ids):
        fail(errors, f"protocol missing stage {stage_id}")

    risk_levels = protocol.get("risk_levels", [])
    risk_ids: set[str] = set()
    for level in risk_levels if isinstance(risk_levels, list) else []:
        if not isinstance(level, dict):
            fail(errors, "risk level entries must be objects")
            continue
        risk_id = level.get("id")
        if not isinstance(risk_id, str) or not risk_id:
            fail(errors, "risk level missing id")
            continue
        risk_ids.add(risk_id)
        for field in ["required_posture", "must_include", "must_not_do"]:
            validate_string_list(errors, risk_id, field, level.get(field))
    for risk_id in sorted(REQUIRED_RISK_IDS - risk_ids):
        fail(errors, f"protocol missing risk level {risk_id}")
    critical = next((level for level in risk_levels if isinstance(level, dict) and level.get("id") == "critical"), {})
    if "professional authority first" not in critical.get("required_posture", []):
        fail(errors, "critical risk level missing professional authority first posture")
    high = next((level for level in risk_levels if isinstance(level, dict) and level.get("id") == "high"), {})
    if "not professional advice" not in high.get("must_include", []):
        fail(errors, "high risk level missing not professional advice requirement")

    adapter_rules = protocol.get("adapter_rules", [])
    rule_ids: set[str] = set()
    for rule in adapter_rules if isinstance(adapter_rules, list) else []:
        if not isinstance(rule, dict):
            fail(errors, "adapter rule entries must be objects")
            continue
        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not rule_id:
            fail(errors, "adapter rule missing id")
            continue
        rule_ids.add(rule_id)
        for field in ["required_checks", "red_lines"]:
            validate_string_list(errors, rule_id, field, rule.get(field))
    for rule_id in sorted(REQUIRED_RULE_IDS - rule_ids):
        fail(errors, f"protocol missing adapter rule {rule_id}")

    examples = protocol.get("examples", [])
    example_domains: set[str] = set()
    for example in examples if isinstance(examples, list) else []:
        if not isinstance(example, dict):
            fail(errors, "example entries must be objects")
            continue
        domain = example.get("domain")
        if not isinstance(domain, str) or not domain:
            fail(errors, "example missing domain")
            continue
        example_domains.add(domain)
        if example.get("risk_level") not in REQUIRED_RISK_IDS:
            fail(errors, f"{domain} example has invalid risk level")
        for field in ["native_evidence_first", "symbolic_lenses", "safe_output_shape"]:
            validate_string_list(errors, domain, field, example.get(field))
    for domain in sorted(REQUIRED_EXAMPLE_DOMAINS - example_domains):
        fail(errors, f"protocol missing example domain {domain}")

    finance = next((example for example in examples if isinstance(example, dict) and example.get("domain") == "finance"), {})
    if finance.get("risk_level") != "high":
        fail(errors, "finance example must be high risk")
    if "do not issue buy or sell commands" not in finance.get("safe_output_shape", []):
        fail(errors, "finance example missing buy/sell boundary")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Universal domain protocol is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
