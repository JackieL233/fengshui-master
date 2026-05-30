#!/usr/bin/env python3
"""Generate a Markdown FengShui Master consultation report scaffold."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent


def load_create_brief() -> Any:
    path = SCRIPT_DIR / "create_brief.py"
    spec = importlib.util.spec_from_file_location("create_brief", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


brief_module = load_create_brief()


def heading_for(section: str) -> str:
    if "/" in section:
        return section
    if section.isupper():
        return section
    return section[:1].upper() + section[1:]


def bullet_list(items: list[str]) -> str:
    if not items:
        return "- None supplied.\n"
    return "".join(f"- {item}\n" for item in items)


def render_floorplan_analysis(analysis: dict[str, Any] | None) -> str:
    if not analysis:
        return ""

    lines = ["## Structured Floor-Plan Analysis", ""]
    if not analysis.get("valid"):
        lines.append("The structured floor-plan input is invalid.")
        for error in analysis.get("errors", []):
            lines.append(f"- {error}")
        lines.append("")
        return "\n".join(lines)

    input_data = analysis.get("input", {})
    lines.extend(
        [
            f"- Name: {input_data.get('name')}",
            f"- Type: {input_data.get('type')}",
            f"- Facing degrees: {input_data.get('facing_degrees')}",
            f"- North degrees: {input_data.get('north_degrees')}",
            "",
            "### Findings",
        ]
    )
    findings = analysis.get("findings", {})
    for category, values in findings.items():
        if values:
            lines.append(f"- {category}:")
            for value in values:
                lines.append(f"  - {value}")

    lines.extend(["", "### Issues"])
    issues = analysis.get("issues", [])
    if issues:
        for issue in issues:
            lines.append(
                f"- {issue.get('code')} ({issue.get('severity')}): {issue.get('message')}"
            )
    else:
        lines.append("- No structured issues detected.")

    lines.extend(["", "### Recommendations"])
    for recommendation in analysis.get("recommendations", []):
        lines.append(
            f"- {recommendation.get('priority')}: {recommendation.get('action')}"
        )

    lines.extend(["", f"Method note: {analysis.get('method_note')}", ""])
    return "\n".join(lines)


def generate_report(question: str, floorplan_path: str | None = None) -> str:
    brief = brief_module.create_brief(question, floorplan_path)
    lines = [
        "# FengShui Master Consultation Report",
        "",
        f"Question: {brief['question']}",
        f"Domain: {brief['domain']}",
        "",
        "## References To Load",
        bullet_list(brief["references"]).rstrip(),
        "",
        "## Guardrails",
        bullet_list(brief["guardrails"]).rstrip(),
        "",
        "## Symbolic Lenses",
        bullet_list(brief["lenses"]).rstrip(),
        "",
        "## Missing Inputs",
        bullet_list(brief["missing_inputs"]).rstrip(),
        "",
        "## Answer Contract",
        bullet_list(brief["answer_contract"]).rstrip(),
        "",
    ]

    floorplan_section = render_floorplan_analysis(brief.get("floorplan_analysis"))
    if floorplan_section:
        lines.append(floorplan_section.rstrip())
        lines.append("")

    lines.append("## Report Sections")
    lines.append("")
    for section in brief["report_sections"]:
        lines.append(f"## {heading_for(section)}")
        lines.append("")
        lines.append(
            "Draft this section from supplied evidence. Separate observation, traditional interpretation, and practical action."
        )
        lines.append("")

    lines.append("## Cultural and Professional Boundary")
    lines.append("")
    lines.append(
        "This report is a cultural and symbolic decision-support scaffold. It is not medical, legal, financial, engineering, architectural, tax, psychological, or safety advice."
    )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown FengShui Master consultation report scaffold."
    )
    parser.add_argument("question", help="User question or consultation goal.")
    parser.add_argument("--floorplan", help="Optional structured floor-plan JSON path.")
    parser.add_argument("--output", help="Optional output Markdown path.")
    args = parser.parse_args()

    report = generate_report(args.question, args.floorplan)
    if args.output:
        output = Path(args.output)
        output.write_text(report, encoding="utf-8")
        print(output)
    else:
        print(report)


if __name__ == "__main__":
    main()
