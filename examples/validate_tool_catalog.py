#!/usr/bin/env python3
"""Validate FengShui Master tool metadata catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "portable-skill.json"
CATALOG = ROOT / "examples" / "tool-catalog.json"
SCHEMA = ROOT / "schemas" / "tool-catalog.schema.json"
RISK_LEVELS = {"low", "medium", "high", "critical"}
OUTPUT_FORMATS = {"json", "markdown"}
INPUT_TYPES = {"string", "integer", "number", "boolean", "path", "date"}


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


def main() -> int:
    errors: list[str] = []
    manifest = load_json(errors, MANIFEST)
    catalog = load_json(errors, CATALOG)
    schema = load_json(errors, SCHEMA)

    if catalog.get("name") != "fengshui-master-tool-catalog":
        fail(errors, "catalog name must be fengshui-master-tool-catalog")
    if schema.get("title") != "FengShui Master Tool Catalog":
        fail(errors, "tool catalog schema has wrong title")

    entries = catalog.get("tools", [])
    if not isinstance(entries, list) or not entries:
        fail(errors, "catalog tools must be a non-empty list")
        entries = []

    by_path: dict[str, dict] = {}
    names: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(errors, f"entry #{index + 1} must be an object")
            continue

        path = entry.get("path")
        name = entry.get("name")
        if not isinstance(path, str) or not path:
            fail(errors, f"entry #{index + 1} missing path")
            continue
        if not isinstance(name, str) or not name:
            fail(errors, f"{path} missing name")
        elif name in names:
            fail(errors, f"duplicate tool name: {name}")
        else:
            names.add(name)

        if path in by_path:
            fail(errors, f"duplicate tool path: {path}")
        by_path[path] = entry
        if not (ROOT / path).exists():
            fail(errors, f"tool path does not exist: {path}")

        for field in [
            "category",
            "description",
            "command_template",
            "inputs",
            "output_format",
            "risk_level",
            "required_guardrails",
        ]:
            if field not in entry:
                fail(errors, f"{path} missing {field}")
        if entry.get("risk_level") not in RISK_LEVELS:
            fail(errors, f"{path} has invalid risk_level {entry.get('risk_level')}")
        if entry.get("output_format") not in OUTPUT_FORMATS:
            fail(errors, f"{path} has invalid output_format {entry.get('output_format')}")

        command = entry.get("command_template", "")
        if isinstance(command, str) and path not in command:
            fail(errors, f"{path} command_template must include tool path")

        inputs = entry.get("inputs", [])
        if not isinstance(inputs, list) or not inputs:
            fail(errors, f"{path} inputs must be a non-empty list")
        else:
            input_names: set[str] = set()
            for input_index, item in enumerate(inputs):
                if not isinstance(item, dict):
                    fail(errors, f"{path} input #{input_index + 1} must be an object")
                    continue
                input_name = item.get("name")
                if not isinstance(input_name, str) or not input_name:
                    fail(errors, f"{path} input #{input_index + 1} missing name")
                elif input_name in input_names:
                    fail(errors, f"{path} duplicate input {input_name}")
                else:
                    input_names.add(input_name)
                if item.get("type") not in INPUT_TYPES:
                    fail(errors, f"{path} input {input_name or input_index} has invalid type")
                if not isinstance(item.get("required"), bool):
                    fail(errors, f"{path} input {input_name or input_index} required must be boolean")
                if not item.get("description"):
                    fail(errors, f"{path} input {input_name or input_index} missing description")

        guardrails = entry.get("required_guardrails", [])
        if not isinstance(guardrails, list) or not guardrails:
            fail(errors, f"{path} required_guardrails must be a non-empty list")
        elif len(guardrails) != len(set(guardrails)):
            fail(errors, f"{path} required_guardrails contains duplicates")
        if entry.get("risk_level") in {"high", "critical"} and len(guardrails) < 1:
            fail(errors, f"{path} high-risk tool must include guardrails")

    manifest_tools = set(manifest.get("tools", []))
    catalog_tools = set(by_path)
    missing = sorted(manifest_tools - catalog_tools)
    extra = sorted(catalog_tools - manifest_tools)
    if missing:
        fail(errors, f"catalog missing manifest tools: {', '.join(missing)}")
    if extra:
        fail(errors, f"catalog has tools outside manifest: {', '.join(extra)}")

    required_tool_guardrails = {
        "fengshui-master/scripts/method_selector.py": "do not mix schools silently",
        "fengshui-master/scripts/moon_phase.py": "do not guarantee auspiciousness",
        "fengshui-master/scripts/solar_terms.py": "use approximate dates only",
        "fengshui-master/scripts/bagua_map.py": "do not mix bagua methods silently",
        "fengshui-master/scripts/flying_stars.py": "not a full Xuan Kong natal chart",
        "fengshui-master/scripts/annual_afflictions.py": "not a full almanac",
        "fengshui-master/scripts/ganzhi.py": "do not present year scaffold as complete bazi",
    }
    for path, guardrail in required_tool_guardrails.items():
        entry = by_path.get(path)
        if not entry:
            continue
        if guardrail not in entry.get("required_guardrails", []):
            fail(errors, f"{path} missing guardrail {guardrail}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("Tool catalog is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
