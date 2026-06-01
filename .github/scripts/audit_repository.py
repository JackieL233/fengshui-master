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
        ROOT / "CHANGELOG.md",
        ROOT / "RELEASE_NOTES.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "schemas" / "portable-skill.schema.json",
        ROOT / "schemas" / "portable-evaluation-suite.schema.json",
        ROOT / "examples" / "portable-agent-prompts.md",
        ROOT / "examples" / "portable-evaluation-suite.json",
        ROOT / "examples" / "validate_portable_evaluation.py",
        ROOT / "examples" / "validate_portable_manifest.py",
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
        ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md",
        ROOT / ".github" / "pull_request_template.md",
        ROOT / "SECURITY.md",
        ROOT / "CODE_OF_CONDUCT.md",
        ROOT / "CHANGELOG.md",
        ROOT / "RELEASE_NOTES.md",
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
    eval_suite_path = ROOT / "examples" / "portable-evaluation-suite.json"
    eval_validator_path = ROOT / "examples" / "validate_portable_evaluation.py"
    manifest_path = ROOT / "portable-skill.json"
    manifest_validator_path = ROOT / "examples" / "validate_portable_manifest.py"
    manifest_schema_path = ROOT / "schemas" / "portable-skill.schema.json"
    eval_schema_path = ROOT / "schemas" / "portable-evaluation-suite.schema.json"

    if not portable_path.exists():
        fail(errors, "missing PORTABLE_SKILL.md")
        return
    if not examples_path.exists():
        fail(errors, "missing examples/portable-agent-prompts.md")
        return
    if not eval_suite_path.exists():
        fail(errors, "missing examples/portable-evaluation-suite.json")
        return
    if not eval_validator_path.exists():
        fail(errors, "missing examples/validate_portable_evaluation.py")
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

    portable = read(portable_path)
    examples = read(examples_path)
    eval_suite = json.loads(read(eval_suite_path))
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

    if eval_suite.get("name") != "fengshui-master-portable-evaluation-suite":
        fail(errors, "portable evaluation suite has wrong name")
    domains = {case.get("domain") for case in eval_suite.get("cases", [])}
    for domain in ["finance", "life_omen", "space", "brand_product", "legal_adjacent"]:
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

    for term in ["examples/portable-evaluation-suite.json"]:
        if term not in readme or term not in portable:
            fail(errors, f"portable evaluation path missing from public docs: {term}")

    for term in ["examples/validate_portable_evaluation.py"]:
        if term not in readme or term not in portable:
            fail(errors, f"portable evaluation validator path missing from public docs: {term}")

    for term in ["portable-skill.json", "examples/validate_portable_manifest.py"]:
        if term not in readme or term not in portable:
            fail(errors, f"portable manifest path missing from public docs: {term}")

    for term in ["schemas/portable-skill.schema.json", "schemas/portable-evaluation-suite.schema.json"]:
        if term not in readme or term not in portable:
            fail(errors, f"portable schema path missing from public docs: {term}")

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
    for term in ["git remote add origin", "git push -u origin master:main", "部署", "GitHub Actions"]:
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

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Repository audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
