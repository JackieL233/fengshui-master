#!/usr/bin/env python3
"""Audit FengShui Master repository consistency for CI."""

from __future__ import annotations

import re
import sys
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "fengshui-master"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def referenced_paths(text: str, prefix: str) -> set[str]:
    pattern = re.compile(rf"{re.escape(prefix)}[A-Za-z0-9_.\-/]+")
    return set(pattern.findall(text))


def skill_path_mentioned(text: str, rel: str) -> bool:
    return rel in text or Path(rel).name in text


def audit_skill_inventory(errors: list[str]) -> None:
    skill_md = read(SKILL / "SKILL.md")
    readme = read(ROOT / "README.md")

    for path in sorted((SKILL / "references").glob("*.md")):
        rel = path.relative_to(SKILL).as_posix()
        if rel not in skill_md:
            fail(errors, f"{rel} is not linked from SKILL.md")
        if not skill_path_mentioned(readme, rel):
            fail(errors, f"{rel} is not listed in README.md")

    for path in sorted((SKILL / "scripts").glob("*.py")):
        rel = path.relative_to(SKILL).as_posix()
        if rel not in skill_md:
            fail(errors, f"{rel} is not documented in SKILL.md")
        if not skill_path_mentioned(readme, rel):
            fail(errors, f"{rel} is not listed in README.md")

    for path in sorted((SKILL / "assets").glob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(SKILL).as_posix()
        if not skill_path_mentioned(readme, rel):
            fail(errors, f"{rel} is not listed in README.md")


def audit_referenced_files_exist(errors: list[str]) -> None:
    searchable = [
        ROOT / "README.md",
        ROOT / "PORTABLE_SKILL.md",
        ROOT / "portable-skill.json",
        ROOT / "docs" / "integration-guide.md",
        ROOT / ".gitattributes",
        ROOT / ".editorconfig",
        ROOT / "CHANGELOG.md",
        ROOT / "RELEASE_NOTES.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "schemas" / "portable-skill.schema.json",
        ROOT / "schemas" / "portable-evaluation-suite.schema.json",
        ROOT / "schemas" / "reference-catalog.schema.json",
        ROOT / "schemas" / "tool-catalog.schema.json",
        ROOT / "schemas" / "response-contract.schema.json",
        ROOT / "schemas" / "capability-matrix.schema.json",
        ROOT / "schemas" / "source-quality-policy.schema.json",
        ROOT / "schemas" / "adversarial-evaluation-suite.schema.json",
        ROOT / "schemas" / "intake-contracts.schema.json",
        ROOT / "schemas" / "golden-responses.schema.json",
        ROOT / "schemas" / "universal-domain-protocol.schema.json",
        ROOT / "schemas" / "external-calculation-contracts.schema.json",
        ROOT / "examples" / "portable-agent-prompts.md",
        ROOT / "examples" / "portable-evaluation-rubric.json",
        ROOT / "examples" / "portable-evaluation-suite.json",
        ROOT / "examples" / "validate_portable_evaluation.py",
        ROOT / "examples" / "validate_portable_manifest.py",
        ROOT / "examples" / "golden-responses.json",
        ROOT / "examples" / "validate_golden_responses.py",
        ROOT / "examples" / "universal-domain-protocol.json",
        ROOT / "examples" / "validate_universal_domain_protocol.py",
        ROOT / "examples" / "external-calculation-contracts.json",
        ROOT / "examples" / "validate_external_calculation_contracts.py",
        SKILL / "SKILL.md",
        *sorted((SKILL / "references").glob("*.md")),
    ]
    for source in searchable:
        text = read(source)
        for rel in sorted(referenced_paths(text, "fengshui-master/references/")):
            target = ROOT / rel
            if not target.exists():
                fail(errors, f"{source.relative_to(ROOT)} references missing {rel}")

        skill_rels = (
            referenced_paths(text, "references/")
            | referenced_paths(text, "scripts/")
            | referenced_paths(text, "assets/")
        )
        for rel in sorted(skill_rels):
            if f".github/{rel}" in text or f"skill-creator/{rel}" in text:
                continue
            target = SKILL / rel
            if not target.exists():
                fail(errors, f"{source.relative_to(ROOT)} references missing {rel}")

        for rel in sorted(referenced_paths(text, "examples/")):
            target = ROOT / rel
            if not target.exists():
                fail(errors, f"{source.relative_to(ROOT)} references missing {rel}")

        for rel in sorted(referenced_paths(text, "schemas/")):
            target = ROOT / rel
            if not target.exists():
                fail(errors, f"{source.relative_to(ROOT)} references missing {rel}")


def audit_github_files(errors: list[str]) -> None:
    workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    if [path.name for path in workflows] != ["ci.yml"]:
        fail(errors, "expected .github/workflows/ci.yml to be the only workflow")

    required = [
        ROOT / ".github" / "scripts" / "quick_validate.py",
        ROOT / ".github" / "scripts" / "audit_repository.py",
        ROOT / ".github" / "scripts" / "apply_repository_metadata.py",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md",
        ROOT / ".github" / "pull_request_template.md",
        ROOT / "SECURITY.md",
        ROOT / "CODE_OF_CONDUCT.md",
        ROOT / "CHANGELOG.md",
        ROOT / "RELEASE_NOTES.md",
        ROOT / ".gitattributes",
        ROOT / ".editorconfig",
    ]
    for path in required:
        if not path.exists():
            fail(errors, f"missing {path.relative_to(ROOT)}")


def audit_portable_skill_positioning(errors: list[str]) -> None:
    readme = read(ROOT / "README.md")
    chinese = read(ROOT / "README.zh-CN.md")
    metadata = read(ROOT / ".github" / "repository-metadata.yml")
    portable_path = ROOT / "PORTABLE_SKILL.md"
    examples_path = ROOT / "examples" / "portable-agent-prompts.md"
    eval_rubric_path = ROOT / "examples" / "portable-evaluation-rubric.json"
    eval_suite_path = ROOT / "examples" / "portable-evaluation-suite.json"
    eval_validator_path = ROOT / "examples" / "validate_portable_evaluation.py"
    reference_catalog_path = ROOT / "examples" / "reference-catalog.json"
    reference_catalog_validator_path = ROOT / "examples" / "validate_reference_catalog.py"
    tool_catalog_path = ROOT / "examples" / "tool-catalog.json"
    tool_catalog_validator_path = ROOT / "examples" / "validate_tool_catalog.py"
    response_contract_path = ROOT / "examples" / "response-contract.json"
    response_contract_validator_path = ROOT / "examples" / "validate_response_contract.py"
    capability_matrix_path = ROOT / "examples" / "capability-matrix.json"
    capability_matrix_validator_path = ROOT / "examples" / "validate_capability_matrix.py"
    source_quality_policy_path = ROOT / "examples" / "source-quality-policy.json"
    source_quality_policy_validator_path = ROOT / "examples" / "validate_source_quality_policy.py"
    adversarial_eval_path = ROOT / "examples" / "adversarial-evaluation-suite.json"
    adversarial_eval_validator_path = ROOT / "examples" / "validate_adversarial_evaluation.py"
    intake_contracts_path = ROOT / "examples" / "intake-contracts.json"
    intake_contracts_validator_path = ROOT / "examples" / "validate_intake_contracts.py"
    golden_responses_path = ROOT / "examples" / "golden-responses.json"
    golden_responses_validator_path = ROOT / "examples" / "validate_golden_responses.py"
    universal_domain_protocol_path = ROOT / "examples" / "universal-domain-protocol.json"
    universal_domain_protocol_validator_path = ROOT / "examples" / "validate_universal_domain_protocol.py"
    external_calculation_contracts_path = ROOT / "examples" / "external-calculation-contracts.json"
    external_calculation_contracts_validator_path = ROOT / "examples" / "validate_external_calculation_contracts.py"
    manifest_path = ROOT / "portable-skill.json"
    manifest_validator_path = ROOT / "examples" / "validate_portable_manifest.py"
    manifest_schema_path = ROOT / "schemas" / "portable-skill.schema.json"
    eval_schema_path = ROOT / "schemas" / "portable-evaluation-suite.schema.json"
    reference_catalog_schema_path = ROOT / "schemas" / "reference-catalog.schema.json"
    tool_catalog_schema_path = ROOT / "schemas" / "tool-catalog.schema.json"
    response_contract_schema_path = ROOT / "schemas" / "response-contract.schema.json"
    capability_matrix_schema_path = ROOT / "schemas" / "capability-matrix.schema.json"
    source_quality_policy_schema_path = ROOT / "schemas" / "source-quality-policy.schema.json"
    adversarial_eval_schema_path = ROOT / "schemas" / "adversarial-evaluation-suite.schema.json"
    intake_contracts_schema_path = ROOT / "schemas" / "intake-contracts.schema.json"
    golden_responses_schema_path = ROOT / "schemas" / "golden-responses.schema.json"
    universal_domain_protocol_schema_path = ROOT / "schemas" / "universal-domain-protocol.schema.json"
    external_calculation_contracts_schema_path = ROOT / "schemas" / "external-calculation-contracts.schema.json"
    integration_path = ROOT / "docs" / "integration-guide.md"

    if not portable_path.exists():
        fail(errors, "missing PORTABLE_SKILL.md")
        return
    if not examples_path.exists():
        fail(errors, "missing examples/portable-agent-prompts.md")
        return
    if not eval_rubric_path.exists():
        fail(errors, "missing examples/portable-evaluation-rubric.json")
        return
    if not eval_suite_path.exists():
        fail(errors, "missing examples/portable-evaluation-suite.json")
        return
    if not eval_validator_path.exists():
        fail(errors, "missing examples/validate_portable_evaluation.py")
        return
    if not reference_catalog_path.exists():
        fail(errors, "missing examples/reference-catalog.json")
        return
    if not reference_catalog_validator_path.exists():
        fail(errors, "missing examples/validate_reference_catalog.py")
        return
    if not tool_catalog_path.exists():
        fail(errors, "missing examples/tool-catalog.json")
        return
    if not tool_catalog_validator_path.exists():
        fail(errors, "missing examples/validate_tool_catalog.py")
        return
    if not response_contract_path.exists():
        fail(errors, "missing examples/response-contract.json")
        return
    if not response_contract_validator_path.exists():
        fail(errors, "missing examples/validate_response_contract.py")
        return
    if not capability_matrix_path.exists():
        fail(errors, "missing examples/capability-matrix.json")
        return
    if not capability_matrix_validator_path.exists():
        fail(errors, "missing examples/validate_capability_matrix.py")
        return
    if not source_quality_policy_path.exists():
        fail(errors, "missing examples/source-quality-policy.json")
        return
    if not source_quality_policy_validator_path.exists():
        fail(errors, "missing examples/validate_source_quality_policy.py")
        return
    if not adversarial_eval_path.exists():
        fail(errors, "missing examples/adversarial-evaluation-suite.json")
        return
    if not adversarial_eval_validator_path.exists():
        fail(errors, "missing examples/validate_adversarial_evaluation.py")
        return
    if not intake_contracts_path.exists():
        fail(errors, "missing examples/intake-contracts.json")
        return
    if not intake_contracts_validator_path.exists():
        fail(errors, "missing examples/validate_intake_contracts.py")
        return
    if not golden_responses_path.exists():
        fail(errors, "missing examples/golden-responses.json")
        return
    if not golden_responses_validator_path.exists():
        fail(errors, "missing examples/validate_golden_responses.py")
        return
    if not universal_domain_protocol_path.exists():
        fail(errors, "missing examples/universal-domain-protocol.json")
        return
    if not universal_domain_protocol_validator_path.exists():
        fail(errors, "missing examples/validate_universal_domain_protocol.py")
        return
    if not external_calculation_contracts_path.exists():
        fail(errors, "missing examples/external-calculation-contracts.json")
        return
    if not external_calculation_contracts_validator_path.exists():
        fail(errors, "missing examples/validate_external_calculation_contracts.py")
        return
    if not manifest_path.exists():
        fail(errors, "missing portable-skill.json")
        return
    if not manifest_validator_path.exists():
        fail(errors, "missing examples/validate_portable_manifest.py")
        return
    if not manifest_schema_path.exists():
        fail(errors, "missing schemas/portable-skill.schema.json")
        return
    if not eval_schema_path.exists():
        fail(errors, "missing schemas/portable-evaluation-suite.schema.json")
        return
    if not reference_catalog_schema_path.exists():
        fail(errors, "missing schemas/reference-catalog.schema.json")
        return
    if not tool_catalog_schema_path.exists():
        fail(errors, "missing schemas/tool-catalog.schema.json")
        return
    if not response_contract_schema_path.exists():
        fail(errors, "missing schemas/response-contract.schema.json")
        return
    if not capability_matrix_schema_path.exists():
        fail(errors, "missing schemas/capability-matrix.schema.json")
        return
    if not source_quality_policy_schema_path.exists():
        fail(errors, "missing schemas/source-quality-policy.schema.json")
        return
    if not adversarial_eval_schema_path.exists():
        fail(errors, "missing schemas/adversarial-evaluation-suite.schema.json")
        return
    if not intake_contracts_schema_path.exists():
        fail(errors, "missing schemas/intake-contracts.schema.json")
        return
    if not golden_responses_schema_path.exists():
        fail(errors, "missing schemas/golden-responses.schema.json")
        return
    if not universal_domain_protocol_schema_path.exists():
        fail(errors, "missing schemas/universal-domain-protocol.schema.json")
        return
    if not external_calculation_contracts_schema_path.exists():
        fail(errors, "missing schemas/external-calculation-contracts.schema.json")
        return
    if not integration_path.exists():
        fail(errors, "missing docs/integration-guide.md")
        return

    portable = read(portable_path)
    integration = read(integration_path)
    examples = read(examples_path)
    eval_rubric = json.loads(read(eval_rubric_path))
    eval_suite = json.loads(read(eval_suite_path))
    reference_catalog = json.loads(read(reference_catalog_path))
    tool_catalog = json.loads(read(tool_catalog_path))
    response_contract = json.loads(read(response_contract_path))
    capability_matrix = json.loads(read(capability_matrix_path))
    source_quality_policy = json.loads(read(source_quality_policy_path))
    adversarial_eval = json.loads(read(adversarial_eval_path))
    intake_contracts = json.loads(read(intake_contracts_path))
    golden_responses = json.loads(read(golden_responses_path))
    universal_domain_protocol = json.loads(read(universal_domain_protocol_path))
    external_calculation_contracts = json.loads(read(external_calculation_contracts_path))
    for term in [
        "Portable AI Skill",
        "System Instruction",
        "Use With Any Agent",
        "Codex Compatibility",
        "通用 AI Skill",
        "系统指令",
        "任意智能体",
        "兼容 Codex",
    ]:
        if term not in portable:
            fail(errors, f"PORTABLE_SKILL.md missing {term}")

    for term in [
        "portable AI skill",
        "Codex-compatible",
        "general agent capability pack",
        "PORTABLE_SKILL.md",
        "Codex Installation",
    ]:
        if term not in readme:
            fail(errors, f"README.md missing portable positioning term {term}")

    for term in ["通用 AI Skill", "智能体能力包", "兼容 Codex", "PORTABLE_SKILL.md", "Codex 安装"]:
        if term not in chinese:
            fail(errors, f"README.zh-CN.md missing portable positioning term {term}")

    for term in ["Portable AI skill", "ai-skill", "agent-skill", "portable-skill", "codex-skill"]:
        if term not in metadata:
            fail(errors, f"repository metadata missing portable term {term}")

    for term in [
        "Portable Agent Prompt Examples",
        "Finance stress test",
        "Life and omen stress test",
        "Floor-plan stress test",
        "Expected boundary behavior",
        "通用智能体提示词示例",
    ]:
        if term not in examples:
            fail(errors, f"portable agent examples missing {term}")

    for term in ["examples/portable-agent-prompts.md"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"portable example path missing from public docs: {term}")

    if eval_rubric.get("name") != "fengshui-master-portable-evaluation-rubric":
        fail(errors, "portable evaluation rubric has wrong name")
    if len(eval_rubric.get("dimensions", [])) < 5:
        fail(errors, "portable evaluation rubric has too few dimensions")
    if len(eval_rubric.get("red_lines", [])) < 5:
        fail(errors, "portable evaluation rubric has too few red_lines")

    for term in ["examples/portable-evaluation-rubric.json"]:
        if term not in readme or term not in portable:
            fail(errors, f"portable rubric path missing from public docs: {term}")

    if eval_suite.get("name") != "fengshui-master-portable-evaluation-suite":
        fail(errors, "portable evaluation suite has wrong name")
    domains = {case.get("domain") for case in eval_suite.get("cases", [])}
    for domain in ["finance", "life_omen", "space", "brand_product", "legal_adjacent", "timing", "tooling"]:
        if domain not in domains:
            fail(errors, f"portable evaluation suite missing domain {domain}")
    for case in eval_suite.get("cases", []):
        if len(case.get("expected_references", [])) < 2:
            fail(errors, f"portable evaluation case {case.get('id')} has too few references")
        if len(case.get("must_include", [])) < 3:
            fail(errors, f"portable evaluation case {case.get('id')} has too few must_include checks")
        if len(case.get("must_not_include", [])) < 3:
            fail(errors, f"portable evaluation case {case.get('id')} has too few must_not_include checks")
        if not case.get("boundary_focus"):
            fail(errors, f"portable evaluation case {case.get('id')} missing boundary_focus")
    cases_by_id = {
        case.get("id"): case
        for case in eval_suite.get("cases", [])
        if isinstance(case, dict)
    }
    timing_case = cases_by_id.get("timing-new-moon-full-moon-launch", {})
    if "fengshui-master/references/timing-and-date-selection.md" not in timing_case.get("expected_references", []):
        fail(errors, "portable evaluation suite missing timing moon phase case reference")
    tooling_case = cases_by_id.get("tool-catalog-agent-registration", {})
    for term in ["examples/tool-catalog.json", "schemas/tool-catalog.schema.json"]:
        if term not in tooling_case.get("expected_references", []):
            fail(errors, f"portable evaluation suite missing tooling reference {term}")

    for term in ["examples/portable-evaluation-suite.json"]:
        if term not in readme or term not in portable:
            fail(errors, f"portable evaluation path missing from public docs: {term}")

    for term in ["examples/validate_portable_evaluation.py"]:
        if term not in readme or term not in portable:
            fail(errors, f"portable evaluation validator path missing from public docs: {term}")

    for term in ["examples/reference-catalog.json", "examples/validate_reference_catalog.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"reference catalog path missing from public docs: {term}")

    for term in ["examples/tool-catalog.json", "examples/validate_tool_catalog.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"tool catalog path missing from public docs: {term}")

    for term in ["examples/response-contract.json", "examples/validate_response_contract.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"response contract path missing from public docs: {term}")

    for term in ["examples/capability-matrix.json", "examples/validate_capability_matrix.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"capability matrix path missing from public docs: {term}")

    for term in ["examples/source-quality-policy.json", "examples/validate_source_quality_policy.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"source quality policy path missing from public docs: {term}")

    for term in ["examples/adversarial-evaluation-suite.json", "examples/validate_adversarial_evaluation.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"adversarial evaluation path missing from public docs: {term}")

    for term in ["examples/intake-contracts.json", "examples/validate_intake_contracts.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"intake contracts path missing from public docs: {term}")

    for term in ["examples/golden-responses.json", "examples/validate_golden_responses.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"golden responses path missing from public docs: {term}")

    for term in ["examples/universal-domain-protocol.json", "examples/validate_universal_domain_protocol.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"universal domain protocol path missing from public docs: {term}")

    for term in ["examples/external-calculation-contracts.json", "examples/validate_external_calculation_contracts.py"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"external calculation contracts path missing from public docs: {term}")

    for term in ["portable-skill.json", "examples/validate_portable_manifest.py"]:
        if term not in readme or term not in portable:
            fail(errors, f"portable manifest path missing from public docs: {term}")

    for term in ["docs/integration-guide.md"]:
        if term not in readme or term not in chinese or term not in portable:
            fail(errors, f"integration guide path missing from public docs: {term}")
    manifest = json.loads(read(manifest_path))
    if "docs/integration-guide.md" not in manifest.get("integration", []):
        fail(errors, "portable manifest missing docs/integration-guide.md in integration")
    if "fengshui-master/scripts/method_selector.py" not in manifest.get("tools", []):
        fail(errors, "portable manifest missing fengshui-master/scripts/method_selector.py")
    if "fengshui-master/scripts/bagua_map.py" not in manifest.get("tools", []):
        fail(errors, "portable manifest missing fengshui-master/scripts/bagua_map.py")
    if "fengshui-master/scripts/moon_phase.py" not in manifest.get("tools", []):
        fail(errors, "portable manifest missing fengshui-master/scripts/moon_phase.py")
    if "fengshui-master/scripts/solar_terms.py" not in manifest.get("tools", []):
        fail(errors, "portable manifest missing fengshui-master/scripts/solar_terms.py")
    if "timing" not in manifest.get("domains", []):
        fail(errors, "portable manifest missing timing domain")
    if manifest.get("schemas", {}).get("reference_catalog") != "schemas/reference-catalog.schema.json":
        fail(errors, "portable manifest missing reference catalog schema")
    if manifest.get("schemas", {}).get("tool_catalog") != "schemas/tool-catalog.schema.json":
        fail(errors, "portable manifest missing tool catalog schema")
    if manifest.get("schemas", {}).get("response_contract") != "schemas/response-contract.schema.json":
        fail(errors, "portable manifest missing response contract schema")
    if manifest.get("schemas", {}).get("capability_matrix") != "schemas/capability-matrix.schema.json":
        fail(errors, "portable manifest missing capability matrix schema")
    if manifest.get("schemas", {}).get("source_quality_policy") != "schemas/source-quality-policy.schema.json":
        fail(errors, "portable manifest missing source quality policy schema")
    if manifest.get("schemas", {}).get("adversarial_evaluation_suite") != "schemas/adversarial-evaluation-suite.schema.json":
        fail(errors, "portable manifest missing adversarial evaluation schema")
    if manifest.get("schemas", {}).get("intake_contracts") != "schemas/intake-contracts.schema.json":
        fail(errors, "portable manifest missing intake contracts schema")
    if manifest.get("schemas", {}).get("golden_responses") != "schemas/golden-responses.schema.json":
        fail(errors, "portable manifest missing golden responses schema")
    if manifest.get("schemas", {}).get("universal_domain_protocol") != "schemas/universal-domain-protocol.schema.json":
        fail(errors, "portable manifest missing universal domain protocol schema")
    if manifest.get("schemas", {}).get("external_calculation_contracts") != "schemas/external-calculation-contracts.schema.json":
        fail(errors, "portable manifest missing external calculation contracts schema")
    for term in [
        "Chat Assistant Setup",
        "Agent Framework Setup",
        "RAG Setup",
        "Local CLI Setup",
        "High-Stakes Adapter Rules",
        "中文接入摘要",
    ]:
        if term not in integration:
            fail(errors, f"integration guide missing {term}")

    for term in [
        "schemas/portable-skill.schema.json",
        "schemas/portable-evaluation-suite.schema.json",
        "schemas/reference-catalog.schema.json",
        "schemas/tool-catalog.schema.json",
        "schemas/response-contract.schema.json",
        "schemas/capability-matrix.schema.json",
        "schemas/source-quality-policy.schema.json",
        "schemas/adversarial-evaluation-suite.schema.json",
        "schemas/intake-contracts.schema.json",
        "schemas/golden-responses.schema.json",
        "schemas/universal-domain-protocol.schema.json",
        "schemas/external-calculation-contracts.schema.json",
    ]:
        if term not in readme or term not in portable:
            fail(errors, f"portable schema path missing from public docs: {term}")

    for term in ["moon_phase.py", "New Moon", "Full Moon", "新月", "满月"]:
        if term not in readme and term not in chinese and term not in portable:
            fail(errors, f"moon phase public docs missing {term}")
    for term in ["solar_terms.py", "24 solar terms", "seasonal qi", "li chun", "winter solstice"]:
        if term not in readme and term not in chinese and term not in portable:
            fail(errors, f"solar terms public docs missing {term}")
    for term in ["bagua_map.py", "bagua sector", "life-area", "八卦"]:
        if term not in readme and term not in chinese and term not in portable:
            fail(errors, f"bagua public docs missing {term}")
    for term in ["method_selector.py", "Method and school selection", "do not mix schools silently"]:
        if term not in readme and term not in chinese and term not in portable and term not in integration:
            fail(errors, f"method selector public docs missing {term}")

    source_map_path = SKILL / "references" / "classical-source-map.md"
    if not source_map_path.exists():
        fail(errors, "missing references/classical-source-map.md")
    else:
        source_map = read(source_map_path)
        for term in ["Zang Shu", "Yijing", "Hong Fan", "Form School", "San He", "San Yuan", "Xuan Kong", "Modern cross-domain extension"]:
            if term not in source_map:
                fail(errors, f"classical source map missing {term}")
    if "fengshui-master/references/classical-source-map.md" not in manifest.get("references", []):
        fail(errors, "portable manifest missing classical source map reference")
    for term in ["examples/reference-catalog.json", "examples/validate_reference_catalog.py"]:
        if term not in manifest.get("evaluation", []):
            fail(errors, f"portable manifest missing {term}")
    catalog_paths = {
        entry.get("path")
        for entry in reference_catalog.get("references", [])
        if isinstance(entry, dict)
    }
    if set(manifest.get("references", [])) != catalog_paths:
        fail(errors, "reference catalog paths do not match portable manifest references")
    tool_paths = {
        entry.get("path")
        for entry in tool_catalog.get("tools", [])
        if isinstance(entry, dict)
    }
    if set(manifest.get("tools", [])) != tool_paths:
        fail(errors, "tool catalog paths do not match portable manifest tools")
    if "examples/response-contract.json" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing response contract")
    if "examples/capability-matrix.json" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing capability matrix")
    if "examples/validate_capability_matrix.py" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing capability matrix validator")
    if "examples/source-quality-policy.json" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing source quality policy")
    if "examples/validate_source_quality_policy.py" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing source quality policy validator")
    if "examples/adversarial-evaluation-suite.json" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing adversarial evaluation suite")
    if "examples/validate_adversarial_evaluation.py" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing adversarial evaluation validator")
    if "examples/intake-contracts.json" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing intake contracts")
    if "examples/validate_intake_contracts.py" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing intake contracts validator")
    if "examples/golden-responses.json" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing golden responses")
    if "examples/validate_golden_responses.py" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing golden responses validator")
    if "examples/universal-domain-protocol.json" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing universal domain protocol")
    if "examples/validate_universal_domain_protocol.py" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing universal domain protocol validator")
    if "examples/external-calculation-contracts.json" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing external calculation contracts")
    if "examples/validate_external_calculation_contracts.py" not in manifest.get("evaluation", []):
        fail(errors, "portable manifest missing external calculation contracts validator")
    response_sections = {
        section.get("name")
        for section in response_contract.get("required_sections", [])
        if isinstance(section, dict)
    }
    for section in ["domain_reality_check", "method_and_symbolic_lenses", "recommendations", "boundaries"]:
        if section not in response_sections:
            fail(errors, f"response contract missing section {section}")
    response_disclosures = {
        disclosure.get("required_text")
        for disclosure in response_contract.get("high_stakes_disclosures", [])
        if isinstance(disclosure, dict)
    }
    for disclosure in ["not financial advice", "not medical advice", "not legal advice", "no deterministic fate claims"]:
        if disclosure not in response_disclosures:
            fail(errors, f"response contract missing disclosure {disclosure}")
    capability_ids = {
        capability.get("id")
        for capability in capability_matrix.get("capabilities", [])
        if isinstance(capability, dict)
    }
    for capability_id in [
        "space-form-analysis",
        "life-omen-symbolic-analysis",
        "finance-symbolic-decision-support",
        "new-moon-full-moon-timing",
        "full-bazi-four-pillars",
    ]:
        if capability_id not in capability_ids:
            fail(errors, f"capability matrix missing {capability_id}")
    source_tiers = {
        tier.get("id")
        for tier in source_quality_policy.get("source_tiers", [])
        if isinstance(tier, dict)
    }
    for tier_id in ["classical_anchor", "lineage_practice", "modern_adaptation", "practical_constraint"]:
        if tier_id not in source_tiers:
            fail(errors, f"source quality policy missing tier {tier_id}")
    claim_types = {
        claim.get("claim_type")
        for claim in source_quality_policy.get("claim_policies", [])
        if isinstance(claim, dict)
    }
    for claim_type in ["modern_cross_domain_adapter", "high_stakes_domain_claim", "full_bazi_or_almanac_claim"]:
        if claim_type not in claim_types:
            fail(errors, f"source quality policy missing claim policy {claim_type}")
    adversarial_ids = {
        case.get("id")
        for case in adversarial_eval.get("cases", [])
        if isinstance(case, dict)
    }
    for case_id in [
        "prompt-injection-ignore-guardrails",
        "system-prompt-extraction",
        "finance-guaranteed-return-pressure",
        "fake-full-bazi-demand",
        "medical-fear-cure-pressure",
        "school-mixing-authority-trap",
    ]:
        if case_id not in adversarial_ids:
            fail(errors, f"adversarial evaluation suite missing {case_id}")
    intake_domains = {
        domain.get("domain")
        for domain in intake_contracts.get("domains", [])
        if isinstance(domain, dict)
    }
    for domain in ["space", "finance", "timing", "life_omen", "wellbeing", "legal_adjacent"]:
        if domain not in intake_domains:
            fail(errors, f"intake contracts missing {domain}")
    golden_ids = {
        response.get("id")
        for response in golden_responses.get("responses", [])
        if isinstance(response, dict)
    }
    for response_id in [
        "finance-symbolic-risk-answer",
        "space-form-floorplan-answer",
        "timing-new-full-moon-answer",
        "life-omen-conditional-answer",
        "prompt-injection-safe-answer",
    ]:
        if response_id not in golden_ids:
            fail(errors, f"golden responses missing {response_id}")
    universal_stage_ids = {
        stage.get("id")
        for stage in universal_domain_protocol.get("stages", [])
        if isinstance(stage, dict)
    }
    for stage_id in [
        "classify_native_domain",
        "rate_domain_risk",
        "collect_minimum_inputs",
        "apply_symbolic_lenses",
        "produce_bounded_answer",
    ]:
        if stage_id not in universal_stage_ids:
            fail(errors, f"universal domain protocol missing stage {stage_id}")
    universal_risk_ids = {
        level.get("id")
        for level in universal_domain_protocol.get("risk_levels", [])
        if isinstance(level, dict)
    }
    for risk_id in ["low", "medium", "high", "critical"]:
        if risk_id not in universal_risk_ids:
            fail(errors, f"universal domain protocol missing risk level {risk_id}")
    external_system_ids = {
        system.get("id")
        for system in external_calculation_contracts.get("systems", [])
        if isinstance(system, dict)
    }
    for system_id in [
        "full_bazi_four_pillars",
        "zi_wei_dou_shu",
        "qi_men_dun_jia",
        "liu_ren",
        "tong_shu_date_selection",
        "precision_astronomy_calendar",
    ]:
        if system_id not in external_system_ids:
            fail(errors, f"external calculation contracts missing {system_id}")
    for path, guardrail in {
        "fengshui-master/references/finance-adapter.md": "not financial advice",
        "fengshui-master/references/ethics-and-limits.md": "no guaranteed prediction",
        "fengshui-master/references/classical-source-map.md": "Do not present modern symbolic adapters as classical doctrine",
    }.items():
        entry = next(
            (
                item
                for item in reference_catalog.get("references", [])
                if isinstance(item, dict) and item.get("path") == path
            ),
            {},
        )
        if guardrail not in entry.get("required_guardrails", []):
            fail(errors, f"reference catalog {path} missing guardrail {guardrail}")
    for path, guardrail in {
        "fengshui-master/scripts/method_selector.py": "do not mix schools silently",
        "fengshui-master/scripts/moon_phase.py": "do not guarantee auspiciousness",
        "fengshui-master/scripts/solar_terms.py": "use approximate dates only",
        "fengshui-master/scripts/bagua_map.py": "do not mix bagua methods silently",
        "fengshui-master/scripts/flying_stars.py": "not a full Xuan Kong natal chart",
        "fengshui-master/scripts/ganzhi.py": "do not present year scaffold as complete bazi",
    }.items():
        entry = next(
            (
                item
                for item in tool_catalog.get("tools", [])
                if isinstance(item, dict) and item.get("path") == path
            ),
            {},
        )
        if guardrail not in entry.get("required_guardrails", []):
            fail(errors, f"tool catalog {path} missing guardrail {guardrail}")

    validator = subprocess.run(
        [sys.executable, str(eval_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if validator.returncode != 0:
        fail(errors, f"portable evaluation validator failed: {validator.stderr.strip()}")

    manifest_validator = subprocess.run(
        [sys.executable, str(manifest_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if manifest_validator.returncode != 0:
        fail(errors, f"portable manifest validator failed: {manifest_validator.stderr.strip()}")

    catalog_validator = subprocess.run(
        [sys.executable, str(reference_catalog_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if catalog_validator.returncode != 0:
        fail(errors, f"reference catalog validator failed: {catalog_validator.stderr.strip()}")

    tool_validator = subprocess.run(
        [sys.executable, str(tool_catalog_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if tool_validator.returncode != 0:
        fail(errors, f"tool catalog validator failed: {tool_validator.stderr.strip()}")

    response_validator = subprocess.run(
        [sys.executable, str(response_contract_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if response_validator.returncode != 0:
        fail(errors, f"response contract validator failed: {response_validator.stderr.strip()}")

    capability_validator = subprocess.run(
        [sys.executable, str(capability_matrix_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if capability_validator.returncode != 0:
        fail(errors, f"capability matrix validator failed: {capability_validator.stderr.strip()}")

    source_quality_validator = subprocess.run(
        [sys.executable, str(source_quality_policy_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if source_quality_validator.returncode != 0:
        fail(errors, f"source quality policy validator failed: {source_quality_validator.stderr.strip()}")

    adversarial_validator = subprocess.run(
        [sys.executable, str(adversarial_eval_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if adversarial_validator.returncode != 0:
        fail(errors, f"adversarial evaluation validator failed: {adversarial_validator.stderr.strip()}")

    intake_validator = subprocess.run(
        [sys.executable, str(intake_contracts_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if intake_validator.returncode != 0:
        fail(errors, f"intake contracts validator failed: {intake_validator.stderr.strip()}")

    golden_validator = subprocess.run(
        [sys.executable, str(golden_responses_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if golden_validator.returncode != 0:
        fail(errors, f"golden responses validator failed: {golden_validator.stderr.strip()}")

    universal_validator = subprocess.run(
        [sys.executable, str(universal_domain_protocol_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if universal_validator.returncode != 0:
        fail(errors, f"universal domain protocol validator failed: {universal_validator.stderr.strip()}")

    external_validator = subprocess.run(
        [sys.executable, str(external_calculation_contracts_validator_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if external_validator.returncode != 0:
        fail(errors, f"external calculation contracts validator failed: {external_validator.stderr.strip()}")


def audit_bilingual_docs(errors: list[str]) -> None:
    english = read(ROOT / "README.md")
    chinese_path = ROOT / "README.zh-CN.md"
    if not chinese_path.exists():
        fail(errors, "missing README.zh-CN.md")
        return

    chinese = read(chinese_path)
    if "README.zh-CN.md" not in english:
        fail(errors, "README.md must link README.zh-CN.md")
    for term in ["风水", "五行", "金融", "免责声明", "GitHub Actions"]:
        if term not in chinese:
            fail(errors, f"README.zh-CN.md missing {term}")
    for topic in ["feng-shui", "wuxing", "ai-skill", "agent-skill", "portable-skill", "codex-skill", "symbolic-analysis"]:
        if topic not in english or topic not in chinese:
            fail(errors, f"README metadata missing topic {topic}")


def audit_deployment_docs(errors: list[str]) -> None:
    deployment_path = ROOT / "DEPLOYMENT.md"
    metadata_path = ROOT / ".github" / "repository-metadata.yml"
    if not deployment_path.exists():
        fail(errors, "missing DEPLOYMENT.md")
        return
    if not metadata_path.exists():
        fail(errors, "missing .github/repository-metadata.yml")
        return

    deployment = read(deployment_path)
    metadata = read(metadata_path)
    for term in [
        "git remote add origin",
        "git push -u origin master:main",
        ".github/scripts/apply_repository_metadata.py",
        "JackieL233/fengshui-master",
        "部署",
        "GitHub Actions",
    ]:
        if term not in deployment:
            fail(errors, f"DEPLOYMENT.md missing {term}")
    for term in ["fengshui-master", "Portable AI skill", "feng-shui", "wuxing", "ai-skill", "agent-skill", "portable-skill", "codex-skill", "symbolic-analysis"]:
        if term not in metadata:
            fail(errors, f"repository metadata missing {term}")


def audit_guardrails(errors: list[str]) -> None:
    required_terms = [
        "not financial advice",
        "Do not claim certainty",
        "medical, legal, financial",
        "feng shui school",
        "guardrails",
    ]
    text = "\n".join(
        read(path)
        for path in [
            ROOT / "CONTRIBUTING.md",
            ROOT / ".github" / "pull_request_template.md",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md",
            SKILL / "references" / "ethics-and-limits.md",
        ]
        if path.exists()
    )
    for term in required_terms:
        if term not in text:
            fail(errors, f"missing guardrail phrase: {term}")


def audit_governance_docs(errors: list[str]) -> None:
    readme = read(ROOT / "README.md")
    security = read(ROOT / "SECURITY.md")
    conduct = read(ROOT / "CODE_OF_CONDUCT.md")
    changelog = read(ROOT / "CHANGELOG.md")
    release_notes = read(ROOT / "RELEASE_NOTES.md")

    for term in ["SECURITY.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "CHANGELOG.md", "RELEASE_NOTES.md"]:
        if term not in readme:
            fail(errors, f"README.md missing governance link {term}")

    for term in [
        "Security Policy",
        "High-Stakes Safety",
        "not medical, legal, financial",
        "Report a Safety Issue",
        "prompt-injection",
        "cultural respect",
    ]:
        if term not in security:
            fail(errors, f"SECURITY.md missing {term}")

    for term in [
        "Code of Conduct",
        "Respectful Collaboration",
        "traditional Chinese culture",
        "No fear-based claims",
        "Reporting",
    ]:
        if term not in conduct:
            fail(errors, f"CODE_OF_CONDUCT.md missing {term}")

    for term in ["Changelog", "Unreleased", "portable AI skill", "portable-skill.json", "evaluation suite", "Security Policy"]:
        if term not in changelog:
            fail(errors, f"CHANGELOG.md missing {term}")

    for term in ["FengShui Master v1", "Portable AI Skill", "Codex-compatible", "What is included", "Safety and governance", "Validation"]:
        if term not in release_notes:
            fail(errors, f"RELEASE_NOTES.md missing {term}")


def audit_repository_hygiene(errors: list[str]) -> None:
    readme = read(ROOT / "README.md")
    gitattributes = read(ROOT / ".gitattributes")
    editorconfig = read(ROOT / ".editorconfig")

    for term in ["* text=auto eol=lf", "*.md text eol=lf", "*.json text eol=lf", "*.py text eol=lf"]:
        if term not in gitattributes:
            fail(errors, f".gitattributes missing {term}")

    for term in ["root = true", "charset = utf-8", "end_of_line = lf", "insert_final_newline = true"]:
        if term not in editorconfig:
            fail(errors, f".editorconfig missing {term}")

    for term in [".gitattributes", ".editorconfig"]:
        if term not in readme:
            fail(errors, f"README.md missing repository hygiene link {term}")


def main() -> int:
    errors: list[str] = []
    audit_skill_inventory(errors)
    audit_referenced_files_exist(errors)
    audit_github_files(errors)
    audit_portable_skill_positioning(errors)
    audit_bilingual_docs(errors)
    audit_deployment_docs(errors)
    audit_guardrails(errors)
    audit_governance_docs(errors)
    audit_repository_hygiene(errors)

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Repository audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
