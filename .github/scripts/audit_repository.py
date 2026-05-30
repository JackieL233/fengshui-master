#!/usr/bin/env python3
"""Audit FengShui Master repository consistency for CI."""

from __future__ import annotations

import re
import sys
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


def audit_referenced_files_exist(errors: list[str]) -> None:
    searchable = [
        ROOT / "README.md",
        ROOT / "CONTRIBUTING.md",
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
    ]
    for path in required:
        if not path.exists():
            fail(errors, f"missing {path.relative_to(ROOT)}")


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


def main() -> int:
    errors: list[str] = []
    audit_skill_inventory(errors)
    audit_referenced_files_exist(errors)
    audit_github_files(errors)
    audit_guardrails(errors)

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Repository audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
