#!/usr/bin/env python3
"""Portable skill metadata validator for CI."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter must be closed with ---")

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_md} does not exist"]

    try:
        fields = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [str(exc)]

    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name:
        errors.append("frontmatter missing name")
    elif not NAME_RE.match(name):
        errors.append("name must use lowercase letters, digits, and hyphens only")

    if not description:
        errors.append("frontmatter missing description")

    extra = set(fields) - {"name", "description"}
    if extra:
        errors.append("frontmatter must only include name and description")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: quick_validate.py <skill-folder>", file=sys.stderr)
        return 2

    errors = validate_skill(Path(sys.argv[1]))
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Skill is valid!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
