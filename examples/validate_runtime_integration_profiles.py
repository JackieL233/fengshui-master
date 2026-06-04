#!/usr/bin/env python3
"""Validate FengShui Master runtime integration profiles."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
PROFILES = ROOT / "examples" / "runtime-integration-profiles.json"
SCHEMA = ROOT / "schemas" / "runtime-integration-profiles.schema.json"
REQUIRED_PROFILES = {"chat_assistant", "agent_framework", "rag", "local_cli", "codex"}


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
    profiles = load_json(errors, PROFILES)
    schema = load_json(errors, SCHEMA)

    if schema.get("title") != "FengShui Master Runtime Integration Profiles":
        fail(errors, "runtime integration profiles schema has wrong title")
    if profiles.get("name") != "fengshui-master-runtime-integration-profiles":
        fail(errors, "profiles name must be fengshui-master-runtime-integration-profiles")

    manifest_eval = set(manifest.get("evaluation", []))
    if "examples/runtime-integration-profiles.json" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/runtime-integration-profiles.json")
    if "examples/validate_runtime_integration_profiles.py" not in manifest_eval:
        fail(errors, "manifest evaluation missing examples/validate_runtime_integration_profiles.py")
    if manifest.get("schemas", {}).get("runtime_integration_profiles") != "schemas/runtime-integration-profiles.schema.json":
        fail(errors, "manifest schemas missing schemas/runtime-integration-profiles.schema.json")

    entries = profiles.get("profiles", [])
    if not isinstance(entries, list) or len(entries) < len(REQUIRED_PROFILES):
        fail(errors, f"profiles must contain at least {len(REQUIRED_PROFILES)} entries")
        entries = []

    by_id: dict[str, dict] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(errors, f"profile #{index + 1} must be an object")
            continue
        profile_id = entry.get("id")
        if not isinstance(profile_id, str) or not profile_id:
            fail(errors, f"profile #{index + 1} missing id")
            continue
        if profile_id in by_id:
            fail(errors, f"duplicate profile: {profile_id}")
        by_id[profile_id] = entry
        for field in ["required_assets", "required_steps", "tooling", "validation_commands", "red_lines"]:
            validate_string_list(errors, profile_id, field, entry.get(field))
        for required in ["PORTABLE_SKILL.md", "examples/response-contract.json"]:
            if required not in entry.get("required_assets", []):
                fail(errors, f"{profile_id} missing required asset {required}")
        if "python examples/validate_runtime_integration_profiles.py" not in entry.get("validation_commands", []):
            fail(errors, f"{profile_id} missing runtime profile validator")

    missing = sorted(REQUIRED_PROFILES - set(by_id))
    if missing:
        fail(errors, f"missing profiles: {', '.join(missing)}")

    agent = by_id.get("agent_framework", {})
    if "examples/tool-catalog.json" not in agent.get("required_assets", []):
        fail(errors, "agent framework profile missing tool catalog")
    if "register tools from examples/tool-catalog.json" not in agent.get("required_steps", []):
        fail(errors, "agent framework profile missing tool registration step")

    rag = by_id.get("rag", {})
    if "examples/reference-catalog.json" not in rag.get("required_assets", []):
        fail(errors, "rag profile missing reference catalog")
    if "route first, retrieve second, answer third" not in rag.get("required_steps", []):
        fail(errors, "rag profile missing route-retrieve-answer step")

    codex = by_id.get("codex", {})
    if "fengshui-master/SKILL.md" not in codex.get("required_assets", []):
        fail(errors, "codex profile missing Codex entrypoint")
    if "do not make the portable assets Codex-only" not in codex.get("red_lines", []):
        fail(errors, "codex profile missing portable red line")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Runtime integration profiles are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
