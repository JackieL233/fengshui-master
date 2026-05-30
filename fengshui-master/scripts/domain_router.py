#!/usr/bin/env python3
"""Route a user question to FengShui Master references."""

from __future__ import annotations

import argparse
import json


def score_question(question: str, keywords: set[str]) -> int:
    normalized = question.lower()
    words = {token.strip(".,?!:;()[]{}\"'").lower() for token in question.split()}
    score = len(words & keywords)

    for keyword in keywords:
        if keyword and keyword in normalized and keyword not in words:
            score += 1

    return score


DOMAIN_RULES = [
    (
        "life_omen",
        {
            "auspicious",
            "inauspicious",
            "omen",
            "omens",
            "luck",
            "lucky",
            "unlucky",
            "fortune",
            "destiny",
            "fate",
            "life",
            "lifepath",
            "biography",
            "person",
            "personal",
            "bazi",
            "birth",
            "year",
            "凶",
            "吉凶",
            "不吉",
            "运势",
            "运气",
            "命",
            "命运",
            "命理",
            "生平",
            "人生",
            "个人",
            "财运",
            "趋吉避凶",
            "八字",
            "出生",
        },
        [
            "references/life-and-omen-adapter.md",
            "references/five-phase-domain-map.md",
            "references/foundation.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not make deterministic fate, health, death, wealth, marriage, or disaster claims.",
            "Use feng shui, yin-yang, wuxing, bagua, and timing as symbolic analysis, not guaranteed prediction.",
            "Disclose when full bazi, zi wei, qimen, liuren, or almanac calculation is not implemented.",
        ],
    ),
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
            "股票",
            "投资",
            "理财",
            "基金",
            "债券",
            "加密",
            "比特币",
            "市场",
            "财运",
            "财富",
            "现金",
            "预算",
            "风险",
        },
        [
            "references/finance-adapter.md",
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
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
            "品牌",
            "标志",
            "颜色",
            "命名",
            "营销",
            "发布",
            "产品",
        },
        [
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
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
            "职业",
            "事业",
            "工作",
            "升职",
            "面试",
            "谈判",
            "领导",
            "团队",
        },
        [
            "references/domain-adapters.md",
            "references/life-and-omen-adapter.md",
            "references/five-phase-domain-map.md",
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
            "健康",
            "睡眠",
            "压力",
            "焦虑",
            "专注",
            "精力",
        },
        [
            "references/domain-adapters.md",
            "references/life-and-omen-adapter.md",
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
            "住宅",
            "房子",
            "公寓",
            "卧室",
            "办公室",
            "书桌",
            "厨房",
            "卫生间",
            "镜子",
            "门",
            "户型",
            "布局",
            "商铺",
            "店铺",
            "土地",
            "墓地",
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
    best = None
    best_score = 0
    for domain, keywords, references, guardrails in DOMAIN_RULES:
        score = score_question(question, keywords)
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
