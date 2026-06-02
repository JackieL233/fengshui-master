#!/usr/bin/env python3
"""Create a FengShui Master consultation brief from a question."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent


def load_script_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


domain_router = load_script_module("domain_router", SCRIPT_DIR / "domain_router.py")
floorplan_analyzer = load_script_module("analyze_floorplan", SCRIPT_DIR / "analyze_floorplan.py")


DOMAIN_MISSING_INPUTS = {
    "finance": [
        "decision type",
        "time horizon",
        "risk tolerance",
        "liquidity needs",
        "existing allocation or concentration",
        "financial thesis and downside condition",
    ],
    "life_omen": [
        "topic area",
        "birth year or relevant year",
        "current life stage",
        "goal for the reading",
        "hard real-world constraints",
    ],
    "space": [
        "floor plan or photos",
        "north arrow or compass bearing",
        "main door and facing convention",
        "occupant goals",
        "changes that are allowed or forbidden",
    ],
    "timing": [
        "candidate date or date range",
        "event type",
        "local time zone or location",
        "hard deadlines and practical constraints",
        "whether the user wants moon phase, almanac attributes, annual cautions, or lineage-specific date selection",
    ],
    "brand": [
        "audience",
        "brand goal",
        "market constraints",
        "accessibility requirements",
        "legal or trademark constraints",
    ],
    "business": [
        "business model and stage",
        "main business goal",
        "customer path or sales funnel",
        "budget, runway, staffing, and regulatory constraints",
        "current bottleneck or leakage",
    ],
    "product": [
        "product type and target user",
        "main product goal or metric",
        "user journey or funnel",
        "current friction, drop-off, or confusion",
        "engineering, accessibility, privacy, and platform constraints",
    ],
    "career": [
        "career goal",
        "current role and constraints",
        "skills and evidence",
        "timing window",
        "workspace or environment context if relevant",
    ],
    "relationship": [
        "relationship type",
        "goal for the reading",
        "safety or coercion concerns",
        "shared-space context",
        "communication constraints and boundaries",
    ],
    "learning": [
        "subject, level, and deadline",
        "learning goal",
        "current schedule and bottleneck",
        "study environment and distraction context",
        "feedback or practice-test data",
    ],
    "wellbeing": [
        "specific wellbeing concern",
        "sleep, light, air, noise, and ergonomic context",
        "medical or safety issues already identified",
        "professional care constraints",
    ],
    "legal_adjacent": [
        "decision type",
        "hard deadlines and required procedures",
        "stakeholders and incentives",
        "documents or clauses the user can summarize",
        "whether qualified legal help is involved",
    ],
    "general": [
        "native domain",
        "desired outcome",
        "real constraints",
        "whether spatial, timing, or symbolic analysis is wanted",
    ],
}


DOMAIN_SECTIONS = {
    "finance": [
        "Inputs and assumptions",
        "Financial reality check",
        "Risk posture",
        "Feng shui symbolic layer",
        "Practical adjustments",
        "Boundaries and missing data",
    ],
    "life_omen": [
        "Inputs and assumptions",
        "Reality layer",
        "Traditional symbolic layer",
        "Ji/xiong assessment",
        "Actions for seeking favorable conditions",
        "Limits and missing data",
    ],
    "space": [
        "Inputs and assumptions",
        "Method",
        "Structured floor-plan findings",
        "Form and flow reading",
        "Recommendations",
        "Missing data",
    ],
    "timing": [
        "Inputs and assumptions",
        "Practical timing constraints",
        "Moon phase symbolic layer",
        "Traditional date-selection layer",
        "Ji/xiong assessment",
        "Low-risk timing advice",
        "Boundaries and missing data",
    ],
    "brand": [
        "Inputs and assumptions",
        "Audience and domain constraints",
        "Five-phase design lens",
        "Risk and accessibility checks",
        "Recommendations",
        "Missing data",
    ],
    "business": [
        "Inputs and assumptions",
        "Business reality layer",
        "Flow and leakage diagnosis",
        "Feng shui symbolic layer",
        "Operational adjustments",
        "Boundaries and missing data",
    ],
    "product": [
        "Inputs and assumptions",
        "Product reality layer",
        "Flow and leakage diagnosis",
        "Feng shui symbolic layer",
        "Product adjustments",
        "Boundaries and missing data",
    ],
    "career": [
        "Inputs and assumptions",
        "Career reality layer",
        "Feng shui and five-phase lens",
        "Timing and support",
        "Practical next actions",
        "Missing data",
    ],
    "relationship": [
        "Inputs and assumptions",
        "Relationship reality and safety",
        "Environment and communication flow",
        "Feng shui symbolic layer",
        "Low-risk adjustments",
        "Boundaries and missing data",
    ],
    "learning": [
        "Inputs and assumptions",
        "Learning reality layer",
        "Environment and attention flow",
        "Five-phase study balance",
        "Practical learning plan",
        "Boundaries and missing data",
    ],
    "wellbeing": [
        "Inputs and assumptions",
        "Wellbeing reality layer",
        "Environment and rhythm lens",
        "Risk checks",
        "Low-risk adjustments",
        "Medical and safety boundaries",
    ],
    "legal_adjacent": [
        "Inputs and assumptions",
        "Legal reality first",
        "Risk map",
        "Feng shui symbolic layer",
        "Preparation actions",
        "Legal boundary and missing data",
    ],
    "general": [
        "Inputs and assumptions",
        "Domain read",
        "Feng shui symbolic layer",
        "Risks and guardrails",
        "Practical adjustments",
        "Missing data",
    ],
}


def merge_unique(left: list[str], right: list[str]) -> list[str]:
    result: list[str] = []
    for value in [*left, *right]:
        if value not in result:
            result.append(value)
    return result


def create_brief(question: str, floorplan_path: str | None = None) -> dict[str, Any]:
    route = domain_router.route(question)
    domain = str(route["domain"])
    references = list(route["references"])
    guardrails = list(route["guardrails"])
    report_sections = list(DOMAIN_SECTIONS.get(domain, DOMAIN_SECTIONS["general"]))
    missing_inputs = list(DOMAIN_MISSING_INPUTS.get(domain, DOMAIN_MISSING_INPUTS["general"]))
    if (
        "references/broad-symbolic-analysis.md" in references
        and "Symbolic analysis protocol" not in report_sections
    ):
        insert_at = 3 if len(report_sections) >= 3 else len(report_sections)
        report_sections.insert(insert_at, "Symbolic analysis protocol")

    floorplan_analysis = None
    if floorplan_path:
        path = Path(floorplan_path)
        plan = json.loads(path.read_text(encoding="utf-8"))
        floorplan_analysis = floorplan_analyzer.analyze(plan)
        references = merge_unique(references, ["references/floorplan-schema.md"])
        if "Structured floor-plan findings" not in report_sections:
            report_sections.insert(2, "Structured floor-plan findings")
        missing_inputs = merge_unique(
            missing_inputs,
            [
                "visual photos for verification",
                "compass north or facing direction",
                "occupant constraints",
            ],
        )

    return {
        "question": question,
        "domain": domain,
        "references": references,
        "guardrails": guardrails,
        "lenses": route["lens"],
        "missing_inputs": missing_inputs,
        "report_sections": report_sections,
        "floorplan_analysis": floorplan_analysis,
        "answer_contract": [
            "Separate real-world constraints from feng shui symbolism.",
            "State method, assumptions, and missing inputs before conclusions.",
            "Prioritize low-risk, reversible actions.",
            "Do not present symbolic readings as guaranteed outcomes.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a structured FengShui Master consultation brief."
    )
    parser.add_argument("question", help="User question or consultation goal.")
    parser.add_argument("--floorplan", help="Optional structured floor-plan JSON path.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(
        json.dumps(
            create_brief(args.question, args.floorplan),
            ensure_ascii=True,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
