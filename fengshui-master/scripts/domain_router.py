#!/usr/bin/env python3
"""Route a user question to FengShui Master references."""

from __future__ import annotations

import argparse
import json


DOMAIN_RULES = [
    (
        "finance",
        {
            "stock",
            "stocks",
            "bond",
            "portfolio",
            "investment",
            "invest",
            "trading",
            "crypto",
            "bitcoin",
            "fund",
            "financial",
            "finance",
            "market",
            "risk",
            "cash",
            "budget",
            "wealth",
        },
        [
            "references/finance-adapter.md",
            "references/domain-adapters.md",
            "references/ethics-and-limits.md",
            "references/timing-and-date-selection.md",
        ],
        [
            "This is not financial advice.",
            "Do not guarantee profit, timing, or risk-free outcomes.",
            "Use feng shui as a symbolic decision-support lens alongside real financial analysis.",
        ],
    ),
    (
        "brand",
        {
            "brand",
            "branding",
            "logo",
            "color",
            "colors",
            "launch",
            "naming",
            "marketing",
            "campaign",
            "product",
        },
        [
            "references/domain-adapters.md",
            "references/foundation.md",
            "references/remedies.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not replace market research, accessibility, or legal trademark review.",
            "Use five phases and yin-yang as symbolic design constraints.",
        ],
    ),
    (
        "career",
        {
            "career",
            "job",
            "promotion",
            "interview",
            "negotiation",
            "team",
            "leadership",
            "boss",
            "work",
        },
        [
            "references/domain-adapters.md",
            "references/analysis-templates.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not promise career outcomes.",
            "Combine symbolic timing and environment advice with practical preparation.",
        ],
    ),
    (
        "wellbeing",
        {
            "health",
            "sleep",
            "stress",
            "wellbeing",
            "wellness",
            "anxiety",
            "focus",
            "energy",
        },
        [
            "references/domain-adapters.md",
            "references/analysis-templates.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not diagnose or treat medical conditions.",
            "Prioritize light, air, sleep, ergonomics, and professional care where needed.",
        ],
    ),
    (
        "space",
        {
            "home",
            "house",
            "apartment",
            "bedroom",
            "office",
            "desk",
            "kitchen",
            "bathroom",
            "mirror",
            "door",
            "floor",
            "layout",
            "room",
            "shop",
            "store",
            "land",
            "site",
        },
        [
            "references/analysis-templates.md",
            "references/forms-and-environment.md",
            "references/remedies.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Use observable form and safety before symbolic judgments.",
        ],
    ),
]


def route(question: str) -> dict[str, object]:
    words = {token.strip(".,?!:;()[]{}\"'").lower() for token in question.split()}
    best = None
    best_score = 0
    for domain, keywords, references, guardrails in DOMAIN_RULES:
        score = len(words & keywords)
        if score > best_score:
            best = (domain, references, guardrails)
            best_score = score

    if best is None:
        best = (
            "general",
            [
                "references/domain-adapters.md",
                "references/foundation.md",
                "references/ethics-and-limits.md",
            ],
            [
                "Identify the domain first, then apply feng shui as an auxiliary symbolic lens.",
            ],
        )

    domain, references, guardrails = best
    return {
        "domain": domain,
        "references": references,
        "guardrails": guardrails,
        "lens": [
            "yin-yang balance",
            "five-phase relationships",
            "timing and activation",
            "form, flow, and containment",
            "risk and remedy hierarchy",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Route a cross-domain question to FengShui Master references."
    )
    parser.add_argument("question", help="User question or short task description.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(json.dumps(route(args.question), ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
