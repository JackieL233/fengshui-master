#!/usr/bin/env python3
"""Select appropriate FengShui Master methods and references for a request."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MethodRule:
    key: str
    label: str
    keywords: set[str]
    use_when: str
    required_inputs: list[str]
    references: list[str]
    tools: list[str]
    guardrails: list[str]
    method_notes: list[str]


METHOD_RULES = [
    MethodRule(
        "form_school",
        "Form School / 形势派",
        {
            "form",
            "landform",
            "road",
            "roads",
            "water",
            "mountain",
            "entrance",
            "door",
            "bedroom",
            "office",
            "shop",
            "layout",
            "floorplan",
            "floor",
            "apartment",
            "house",
            "site",
            "形势",
            "峦头",
            "道路",
            "水",
            "山",
            "门",
            "户型",
            "住宅",
            "办公室",
            "商铺",
        },
        "Use observable form, qi flow, support, leakage, sha qi, light, air, access, and usability before formulaic layers.",
        ["photos or floor plan", "entrance and circulation", "room functions", "safety and usability constraints"],
        [
            "references/forms-and-environment.md",
            "references/analysis-templates.md",
            "references/remedies.md",
            "references/ethics-and-limits.md",
        ],
        ["fengshui-master/scripts/analyze_floorplan.py"],
        ["prioritize safety and observable form", "prefer low-risk reversible adjustments"],
        ["Good first layer for most spatial readings.", "Do not make precise directional claims without reliable compass data."],
    ),
    MethodRule(
        "compass_bagua",
        "Compass Bagua / 后天八卦",
        {
            "bagua",
            "trigram",
            "sector",
            "north",
            "south",
            "east",
            "west",
            "southeast",
            "wealth",
            "career",
            "relationship",
            "八卦",
            "方位",
            "卦",
            "财位",
            "事业位",
            "关系位",
        },
        "Use later-heaven bagua when the question asks about directional sectors, trigrams, phase symbolism, or life-area symbolism.",
        ["chosen bagua method", "reliable north or explicit symbolic overlay", "sector or life area", "room or domain context"],
        ["references/foundation.md", "references/schools.md", "references/remedies.md", "references/ethics-and-limits.md"],
        ["fengshui-master/scripts/bagua_map.py"],
        ["do not mix compass and door-aligned bagua silently", "do not guarantee wealth, romance, health, or career outcomes"],
        ["Use compass bagua only with reliable direction data.", "Use symbolic or door-aligned bagua only when explicitly chosen."],
    ),
    MethodRule(
        "eight_mansions",
        "Eight Mansions / 八宅命卦",
        {
            "eight",
            "mansions",
            "ming",
            "gua",
            "personal",
            "bed",
            "desk",
            "direction",
            "birth",
            "八宅",
            "命卦",
            "个人",
            "床",
            "书桌",
            "出生",
        },
        "Use Eight Mansions for personal gua, favorable/unfavorable directions, bed head direction, desk facing, and simple personal-sector compatibility.",
        ["birth year", "traditional sex input if using the common formula", "li chun or lunar boundary convention if near early February", "bed/desk/door direction"],
        ["references/schools.md", "references/foundation.md", "references/analysis-templates.md", "references/ethics-and-limits.md"],
        ["fengshui-master/scripts/minggua.py"],
        ["do not infer gender identity", "do not override severe form or safety issues with personal direction formulas"],
        ["Formula conventions vary by lineage.", "State when using the common Gregorian-year helper."],
    ),
    MethodRule(
        "xuan_kong",
        "Xuan Kong Flying Stars / 玄空飞星",
        {
            "xuan",
            "kong",
            "flying",
            "stars",
            "period",
            "natal",
            "renovation",
            "annual",
            "star",
            "玄空",
            "飞星",
            "九运",
            "三元",
            "宅盘",
            "流年",
            "装修",
        },
        "Use xuan kong when the request asks about time-space star layers, Period 9, building period, facing/sitting, renovation activation, or annual flying-star discussion.",
        ["building completion or major renovation year", "facing and sitting direction", "floor plan with north", "room usage", "lineage assumptions"],
        ["references/xuan-kong-flying-stars.md", "references/timing-and-date-selection.md", "references/schools.md", "references/ethics-and-limits.md"],
        ["fengshui-master/scripts/periods.py", "fengshui-master/scripts/flying_stars.py"],
        ["not a full Xuan Kong natal chart", "do not guarantee wealth or illness outcomes"],
        ["The helper is only a Luo Shu scaffold.", "Full natal charts require lineage-specific formulas and reliable inputs."],
    ),
    MethodRule(
        "san_he",
        "San He / 三合",
        {
            "san",
            "he",
            "water",
            "outlet",
            "land",
            "site",
            "grave",
            "yin",
            "branch",
            "mountain",
            "三合",
            "水口",
            "来水",
            "去水",
            "阴宅",
            "墓地",
            "二十四山",
        },
        "Use San He cautiously for land, water approach/exit, 24 mountains, branch relationships, yin-house, or rural site questions when enough environmental detail exists.",
        ["site context", "water or road approach/exit", "reliable compass sectors", "legal and family constraints for yin-house topics"],
        ["references/schools.md", "references/forms-and-environment.md", "references/yin-house.md", "references/ethics-and-limits.md"],
        ["fengshui-master/scripts/luopan.py"],
        ["respect legal, land, safety, and family constraints", "do not claim descendant wealth, illness, fertility, or death outcomes"],
        ["Avoid applying advanced san he formulas without local lineage data.", "For yin-house topics, keep the response conservative and respectful."],
    ),
    MethodRule(
        "timing",
        "Timing and Date Selection / 择时择日",
        {
            "date",
            "timing",
            "opening",
            "move",
            "moving",
            "launch",
            "renovation",
            "moon",
            "solar",
            "term",
            "lichun",
            "almanac",
            "择日",
            "择时",
            "开业",
            "搬家",
            "装修",
            "动土",
            "新月",
            "满月",
            "节气",
        },
        "Use timing layers for moving, opening, renovation, launch, moon phase, solar terms, annual cautions, san yuan periods, or candidate-date comparison.",
        ["candidate date or date range", "event type", "local time zone or location", "hard deadlines", "calendar attributes or lineage if exact election is requested"],
        ["references/timing-and-date-selection.md", "references/broad-symbolic-analysis.md", "references/ethics-and-limits.md"],
        [
            "fengshui-master/scripts/moon_phase.py",
            "fengshui-master/scripts/solar_terms.py",
            "fengshui-master/scripts/annual_afflictions.py",
            "fengshui-master/scripts/periods.py",
        ],
        ["not a full almanac", "do not guarantee auspiciousness", "practical constraints take priority"],
        ["Treat moon phase, solar terms, and annual cautions as secondary timing layers.", "Exact electional work needs a trusted almanac or lineage calendar."],
    ),
    MethodRule(
        "broad_symbolic",
        "Broad Symbolic Feng Shui / 广义风水象义",
        {
            "life",
            "omen",
            "luck",
            "auspicious",
            "inauspicious",
            "finance",
            "business",
            "brand",
            "career",
            "relationship",
            "product",
            "learning",
            "wellbeing",
            "legal",
            "吉凶",
            "运势",
            "生平",
            "趋吉避凶",
            "金融",
            "商业",
            "品牌",
            "事业",
            "关系",
        },
        "Use broad symbolic analysis when feng shui is used as qi, form, timing, support, leakage, wuxing, and ji/xiong language beyond physical space.",
        ["native domain", "stakes and constraints", "user goal", "evidence and uncertainty", "what kind of symbolic reading is wanted"],
        [
            "references/broad-symbolic-analysis.md",
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
            "references/ethics-and-limits.md",
        ],
        ["fengshui-master/scripts/domain_router.py", "fengshui-master/scripts/create_brief.py"],
        ["native-domain reality comes first", "no deterministic fate claims", "not financial, medical, legal, engineering, tax, or safety advice"],
        ["Good for finance, business, life-pattern, brand, career, relationship, product, learning, wellbeing, and legal-adjacent questions.", "Use specialized adapters after routing."],
    ),
]


def score(question: str, keywords: set[str]) -> int:
    normalized = question.lower()
    tokens = {token.strip(".,?!:;()[]{}\"'").lower() for token in question.split()}
    result = len(tokens & keywords)
    for keyword in keywords:
        if keyword and keyword in normalized and keyword not in tokens:
            result += 1
    return result


def rule_payload(rule: MethodRule, score_value: int) -> dict[str, Any]:
    return {
        "method": rule.key,
        "label": rule.label,
        "score": score_value,
        "use_when": rule.use_when,
        "required_inputs": rule.required_inputs,
        "references": rule.references,
        "tools": rule.tools,
        "guardrails": rule.guardrails,
        "method_notes": rule.method_notes,
    }


def select_methods(question: str, limit: int = 3) -> dict[str, Any]:
    scored = [(score(question, rule.keywords), rule) for rule in METHOD_RULES]
    scored.sort(key=lambda item: (-item[0], item[1].key))
    matches = [item for item in scored if item[0] > 0]
    if not matches:
        matches = [(1, next(rule for rule in METHOD_RULES if rule.key == "broad_symbolic"))]

    selected = matches[: max(1, limit)]
    primary_score, primary_rule = selected[0]
    payloads = [rule_payload(rule, value) for value, rule in selected]

    return {
        "question": question,
        "primary_method": rule_payload(primary_rule, primary_score),
        "candidate_methods": payloads,
        "answer_rules": [
            "Name the selected method before conclusions.",
            "Load the selected references before making method-specific claims.",
            "Ask for required inputs when precision depends on missing data.",
            "Do not mix schools silently; explain conflicts and choose the lightest adequate method.",
            "Use safety, law, finance, medical, engineering, and practical constraints before symbolic interpretation.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Select FengShui Master methods for a request.")
    parser.add_argument("question", help="User question or task.")
    parser.add_argument("--limit", type=int, default=3, help="Maximum candidate methods to return.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(
        json.dumps(
            select_methods(args.question, args.limit),
            ensure_ascii=True,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
