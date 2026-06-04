#!/usr/bin/env python3
"""Validate the platform-neutral FengShui Master skill manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
MANIFEST_SCHEMA = ROOT / "schemas" / "portable-skill.schema.json"
EVALUATION_SCHEMA = ROOT / "schemas" / "portable-evaluation-suite.schema.json"
REFERENCE_CATALOG_SCHEMA = ROOT / "schemas" / "reference-catalog.schema.json"
TOOL_CATALOG_SCHEMA = ROOT / "schemas" / "tool-catalog.schema.json"
RESPONSE_CONTRACT_SCHEMA = ROOT / "schemas" / "response-contract.schema.json"
CAPABILITY_MATRIX_SCHEMA = ROOT / "schemas" / "capability-matrix.schema.json"
SOURCE_QUALITY_POLICY_SCHEMA = ROOT / "schemas" / "source-quality-policy.schema.json"
ADVERSARIAL_EVALUATION_SCHEMA = ROOT / "schemas" / "adversarial-evaluation-suite.schema.json"
INTAKE_CONTRACTS_SCHEMA = ROOT / "schemas" / "intake-contracts.schema.json"
GOLDEN_RESPONSES_SCHEMA = ROOT / "schemas" / "golden-responses.schema.json"
UNIVERSAL_DOMAIN_PROTOCOL_SCHEMA = ROOT / "schemas" / "universal-domain-protocol.schema.json"
EXTERNAL_CALCULATION_CONTRACTS_SCHEMA = ROOT / "schemas" / "external-calculation-contracts.schema.json"
CONTRIBUTION_QUALITY_GATES_SCHEMA = ROOT / "schemas" / "contribution-quality-gates.schema.json"
REQUIRED_TOP_LEVEL = {
    "name",
    "type",
    "version",
    "title",
    "description",
    "languages",
    "entrypoints",
    "references",
    "tools",
    "evaluation",
    "integration",
    "governance",
    "guardrails",
    "domains",
    "schemas",
}
REQUIRED_DOMAINS = {"space", "life_omen", "finance", "brand", "product", "legal_adjacent", "timing"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def require_paths(errors: list[str], manifest: dict, field: str) -> None:
    values = manifest.get(field, [])
    if not isinstance(values, list) or not values:
        fail(errors, f"{field} must be a non-empty list")
        return

    for rel in values:
        if not isinstance(rel, str):
            fail(errors, f"{field} contains a non-string path")
            continue
        if not (ROOT / rel).exists():
            fail(errors, f"{field} references missing path: {rel}")


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.exists():
        fail(errors, "missing portable-skill.json")
        manifest = {}
    else:
        try:
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"invalid JSON: {exc}")
            manifest = {}

    schema_titles = {
        MANIFEST_SCHEMA: "FengShui Master Portable Skill Manifest",
        EVALUATION_SCHEMA: "FengShui Master Portable Evaluation Suite",
        REFERENCE_CATALOG_SCHEMA: "FengShui Master Reference Catalog",
        TOOL_CATALOG_SCHEMA: "FengShui Master Tool Catalog",
        RESPONSE_CONTRACT_SCHEMA: "FengShui Master Response Contract",
        CAPABILITY_MATRIX_SCHEMA: "FengShui Master Capability Matrix",
        SOURCE_QUALITY_POLICY_SCHEMA: "FengShui Master Source Quality Policy",
        ADVERSARIAL_EVALUATION_SCHEMA: "FengShui Master Adversarial Evaluation Suite",
        INTAKE_CONTRACTS_SCHEMA: "FengShui Master Intake Contracts",
        GOLDEN_RESPONSES_SCHEMA: "FengShui Master Golden Responses",
        UNIVERSAL_DOMAIN_PROTOCOL_SCHEMA: "FengShui Master Universal Domain Protocol",
        EXTERNAL_CALCULATION_CONTRACTS_SCHEMA: "FengShui Master External Calculation Contracts",
        CONTRIBUTION_QUALITY_GATES_SCHEMA: "FengShui Master Contribution Quality Gates",
    }
    for path, title in schema_titles.items():
        if not path.exists():
            fail(errors, f"missing {path.relative_to(ROOT)}")
            continue
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"invalid schema JSON {path.relative_to(ROOT)}: {exc}")
            continue
        if schema.get("title") != title:
            fail(errors, f"{path.relative_to(ROOT)} has wrong title")

    missing_keys = sorted(REQUIRED_TOP_LEVEL - set(manifest))
    if missing_keys:
        fail(errors, f"manifest missing keys: {', '.join(missing_keys)}")

    if manifest.get("name") != "fengshui-master":
        fail(errors, "name must be fengshui-master")
    if manifest.get("type") != "portable-ai-skill":
        fail(errors, "type must be portable-ai-skill")
    if "zh-CN" not in manifest.get("languages", []):
        fail(errors, "languages must include zh-CN")

    for field in ["entrypoints", "references", "tools", "evaluation", "integration", "governance"]:
        require_paths(errors, manifest, field)

    schemas = manifest.get("schemas", {})
    if schemas.get("manifest") != "schemas/portable-skill.schema.json":
        fail(errors, "schemas.manifest must point to schemas/portable-skill.schema.json")
    if schemas.get("evaluation_suite") != "schemas/portable-evaluation-suite.schema.json":
        fail(errors, "schemas.evaluation_suite must point to schemas/portable-evaluation-suite.schema.json")
    if schemas.get("reference_catalog") != "schemas/reference-catalog.schema.json":
        fail(errors, "schemas.reference_catalog must point to schemas/reference-catalog.schema.json")
    if schemas.get("tool_catalog") != "schemas/tool-catalog.schema.json":
        fail(errors, "schemas.tool_catalog must point to schemas/tool-catalog.schema.json")
    if schemas.get("response_contract") != "schemas/response-contract.schema.json":
        fail(errors, "schemas.response_contract must point to schemas/response-contract.schema.json")
    if schemas.get("capability_matrix") != "schemas/capability-matrix.schema.json":
        fail(errors, "schemas.capability_matrix must point to schemas/capability-matrix.schema.json")
    if schemas.get("source_quality_policy") != "schemas/source-quality-policy.schema.json":
        fail(errors, "schemas.source_quality_policy must point to schemas/source-quality-policy.schema.json")
    if schemas.get("adversarial_evaluation_suite") != "schemas/adversarial-evaluation-suite.schema.json":
        fail(errors, "schemas.adversarial_evaluation_suite must point to schemas/adversarial-evaluation-suite.schema.json")
    if schemas.get("intake_contracts") != "schemas/intake-contracts.schema.json":
        fail(errors, "schemas.intake_contracts must point to schemas/intake-contracts.schema.json")
    if schemas.get("golden_responses") != "schemas/golden-responses.schema.json":
        fail(errors, "schemas.golden_responses must point to schemas/golden-responses.schema.json")
    if schemas.get("universal_domain_protocol") != "schemas/universal-domain-protocol.schema.json":
        fail(errors, "schemas.universal_domain_protocol must point to schemas/universal-domain-protocol.schema.json")
    if schemas.get("external_calculation_contracts") != "schemas/external-calculation-contracts.schema.json":
        fail(errors, "schemas.external_calculation_contracts must point to schemas/external-calculation-contracts.schema.json")
    if schemas.get("contribution_quality_gates") != "schemas/contribution-quality-gates.schema.json":
        fail(errors, "schemas.contribution_quality_gates must point to schemas/contribution-quality-gates.schema.json")
    for rel in schemas.values() if isinstance(schemas, dict) else []:
        if not (ROOT / rel).exists():
            fail(errors, f"schemas references missing path: {rel}")

    for required in ["PORTABLE_SKILL.md", "fengshui-master/SKILL.md"]:
        if required not in manifest.get("entrypoints", []):
            fail(errors, f"entrypoints missing {required}")
    if "docs/integration-guide.md" not in manifest.get("integration", []):
        fail(errors, "integration missing docs/integration-guide.md")
    if "fengshui-master/scripts/method_selector.py" not in manifest.get("tools", []):
        fail(errors, "tools missing fengshui-master/scripts/method_selector.py")
    if "fengshui-master/scripts/moon_phase.py" not in manifest.get("tools", []):
        fail(errors, "tools missing fengshui-master/scripts/moon_phase.py")
    if "fengshui-master/scripts/solar_terms.py" not in manifest.get("tools", []):
        fail(errors, "tools missing fengshui-master/scripts/solar_terms.py")
    if "fengshui-master/scripts/bagua_map.py" not in manifest.get("tools", []):
        fail(errors, "tools missing fengshui-master/scripts/bagua_map.py")
    if "examples/capability-matrix.json" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/capability-matrix.json")
    if "examples/validate_capability_matrix.py" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/validate_capability_matrix.py")
    if "examples/source-quality-policy.json" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/source-quality-policy.json")
    if "examples/validate_source_quality_policy.py" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/validate_source_quality_policy.py")
    if "examples/adversarial-evaluation-suite.json" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/adversarial-evaluation-suite.json")
    if "examples/validate_adversarial_evaluation.py" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/validate_adversarial_evaluation.py")
    if "examples/intake-contracts.json" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/intake-contracts.json")
    if "examples/validate_intake_contracts.py" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/validate_intake_contracts.py")
    if "examples/golden-responses.json" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/golden-responses.json")
    if "examples/validate_golden_responses.py" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/validate_golden_responses.py")
    if "examples/universal-domain-protocol.json" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/universal-domain-protocol.json")
    if "examples/validate_universal_domain_protocol.py" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/validate_universal_domain_protocol.py")
    if "examples/external-calculation-contracts.json" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/external-calculation-contracts.json")
    if "examples/validate_external_calculation_contracts.py" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/validate_external_calculation_contracts.py")
    if "examples/contribution-quality-gates.json" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/contribution-quality-gates.json")
    if "examples/validate_contribution_quality_gates.py" not in manifest.get("evaluation", []):
        fail(errors, "evaluation missing examples/validate_contribution_quality_gates.py")

    domains = set(manifest.get("domains", []))
    missing_domains = sorted(REQUIRED_DOMAINS - domains)
    if missing_domains:
        fail(errors, f"domains missing: {', '.join(missing_domains)}")

    guardrails = " ".join(manifest.get("guardrails", [])).lower()
    for term in ["not financial advice", "not legal advice", "no guaranteed prediction"]:
        if term not in guardrails:
            fail(errors, f"guardrails missing {term}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Portable skill manifest is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
