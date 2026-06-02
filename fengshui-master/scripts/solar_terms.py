#!/usr/bin/env python3
"""Approximate 24 solar terms context for FengShui Master timing work."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class SolarTerm:
    key: str
    name_en: str
    name_zh: str
    month: int
    day: int
    season_gate: str
    yin_yang: str
    five_phase: str
    symbolic_guidance: str


SOLAR_TERMS = [
    SolarTerm(
        "xiaohan",
        "Minor Cold",
        "小寒",
        1,
        6,
        "deep winter consolidation",
        "yin is deep, yang is hidden",
        "water with stored earth",
        "Use for conserving resources, quiet repair, winter review, and reducing leakage.",
    ),
    SolarTerm(
        "dahan",
        "Major Cold",
        "大寒",
        1,
        20,
        "winter completion",
        "yin reaches completion before spring stirring",
        "water transforming toward wood",
        "Use for closure, final review, preparation, and protecting the root before new growth.",
    ),
    SolarTerm(
        "lichun",
        "Beginning of Spring",
        "立春",
        2,
        4,
        "spring gate",
        "yang begins to rise",
        "wood",
        "Use for intention, direction setting, renewal, gentle starts, and annual-boundary questions.",
    ),
    SolarTerm(
        "yushui",
        "Rain Water",
        "雨水",
        2,
        19,
        "spring moisture",
        "yang rises through softening yin",
        "water nourishing wood",
        "Use for relationship repair, soft activation, learning, communication, and gradual growth.",
    ),
    SolarTerm(
        "jingzhe",
        "Awakening of Insects",
        "惊蛰",
        3,
        6,
        "spring stirring",
        "yang becomes active",
        "wood with thunder fire",
        "Use for activation, announcements, restarting stalled work, and confronting inertia carefully.",
    ),
    SolarTerm(
        "chunfen",
        "Spring Equinox",
        "春分",
        3,
        21,
        "spring balance",
        "yin and yang are balanced",
        "wood in balance",
        "Use for negotiation, calibration, partnership review, and balancing expansion with restraint.",
    ),
    SolarTerm(
        "qingming",
        "Clear and Bright",
        "清明",
        4,
        5,
        "clear spring",
        "yang is clear and ascending",
        "wood with clear fire",
        "Use for clearing, memorial respect, visibility, transparent planning, and removing clutter.",
    ),
    SolarTerm(
        "guyu",
        "Grain Rain",
        "谷雨",
        4,
        20,
        "spring nourishment",
        "yang expands through nourishment",
        "wood nourished by water and earth",
        "Use for cultivation, education, growth systems, planting effort, and resource support.",
    ),
    SolarTerm(
        "lixia",
        "Beginning of Summer",
        "立夏",
        5,
        6,
        "summer gate",
        "yang becomes outward",
        "fire",
        "Use for visibility, momentum, public activity, and moving from preparation into action.",
    ),
    SolarTerm(
        "xiaoman",
        "Grain Buds",
        "小满",
        5,
        21,
        "summer filling",
        "yang fills but is not complete",
        "fire with earth",
        "Use for measured growth, capacity checks, early harvest review, and avoiding overextension.",
    ),
    SolarTerm(
        "mangzhong",
        "Grain in Ear",
        "芒种",
        6,
        6,
        "summer work",
        "yang is busy and productive",
        "fire supporting earth",
        "Use for focused execution, operational discipline, time-sensitive work, and planting before delay.",
    ),
    SolarTerm(
        "xiazhi",
        "Summer Solstice",
        "夏至",
        6,
        21,
        "peak yang",
        "yang peaks and yin begins to return",
        "fire",
        "Use for culmination, visibility, celebration, release, and reviewing what peak exposure reveals.",
    ),
    SolarTerm(
        "xiaoshu",
        "Minor Heat",
        "小暑",
        7,
        7,
        "rising heat",
        "yang remains strong, yin is returning quietly",
        "fire with damp earth",
        "Use for pacing, heat management, workload balance, and preventing burnout or conflict.",
    ),
    SolarTerm(
        "dashu",
        "Major Heat",
        "大暑",
        7,
        23,
        "great heat",
        "yang heat is intense",
        "fire and earth",
        "Use for endurance planning, cooling remedies, risk control, and avoiding impulsive excess.",
    ),
    SolarTerm(
        "liqiu",
        "Beginning of Autumn",
        "立秋",
        8,
        8,
        "autumn gate",
        "yin begins to gather",
        "metal",
        "Use for review, pruning, discipline, standards, and shifting from expansion to refinement.",
    ),
    SolarTerm(
        "chushu",
        "End of Heat",
        "处暑",
        8,
        23,
        "heat withdrawal",
        "yang heat recedes, yin gathers",
        "metal with residual fire",
        "Use for cooling conflict, simplifying, handoff planning, and converting activity into order.",
    ),
    SolarTerm(
        "bailu",
        "White Dew",
        "白露",
        9,
        8,
        "autumn clarity",
        "yin becomes visible",
        "metal with moisture",
        "Use for clarity, boundary setting, relationship tone, documentation, and subtle risk detection.",
    ),
    SolarTerm(
        "qiufen",
        "Autumn Equinox",
        "秋分",
        9,
        23,
        "autumn balance",
        "yin and yang are balanced",
        "metal in balance",
        "Use for fair comparison, audit, negotiation, settlement, and balancing gain with cost.",
    ),
    SolarTerm(
        "hanlu",
        "Cold Dew",
        "寒露",
        10,
        8,
        "cooling autumn",
        "yin coolness strengthens",
        "metal turning toward water",
        "Use for risk review, quiet focus, preservation, and reducing exposed weaknesses.",
    ),
    SolarTerm(
        "shuangjiang",
        "Frost Descent",
        "霜降",
        10,
        23,
        "late autumn contraction",
        "yin condenses",
        "metal and water",
        "Use for decisive pruning, closing weak loops, protection, and preparing for winter storage.",
    ),
    SolarTerm(
        "lidong",
        "Beginning of Winter",
        "立冬",
        11,
        7,
        "winter gate",
        "yin becomes dominant",
        "water",
        "Use for storage, rest cycles, treasury review, internal work, and conserving qi.",
    ),
    SolarTerm(
        "xiaoxue",
        "Minor Snow",
        "小雪",
        11,
        22,
        "early winter stillness",
        "yin settles",
        "water with metal",
        "Use for quiet repair, reducing exposure, knowledge storage, and low-noise maintenance.",
    ),
    SolarTerm(
        "daxue",
        "Major Snow",
        "大雪",
        12,
        7,
        "deepening winter",
        "yin is strong and covering",
        "water with stored earth",
        "Use for consolidation, retreat, archives, reserves, and strengthening hidden support.",
    ),
    SolarTerm(
        "dongzhi",
        "Winter Solstice",
        "冬至",
        12,
        22,
        "peak yin",
        "yin peaks and yang begins to return",
        "water",
        "Use for reset, ancestral respect, long-horizon planning, root repair, and quiet renewal.",
    ),
]


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD format") from exc


def term_date(term: SolarTerm, year: int) -> date:
    return date(year, term.month, term.day)


def term_payload(term: SolarTerm, year: int, target: date) -> dict[str, Any]:
    day = term_date(term, year)
    return {
        "key": term.key,
        "name_en": term.name_en,
        "name_zh": term.name_zh,
        "approx_date": day.isoformat(),
        "days_from_target": (day - target).days,
        "season_gate": term.season_gate,
        "yin_yang": term.yin_yang,
        "five_phase": term.five_phase,
        "symbolic_guidance": term.symbolic_guidance,
    }


def solar_terms_for_date(target: date) -> dict[str, Any]:
    dated_terms = []
    for year in [target.year - 1, target.year, target.year + 1]:
        for term in SOLAR_TERMS:
            dated_terms.append((term_date(term, year), term, year))
    dated_terms.sort(key=lambda item: item[0])

    previous_items = [item for item in dated_terms if item[0] <= target]
    next_items = [item for item in dated_terms if item[0] > target]
    previous_day, previous_term, previous_year = previous_items[-1]
    next_day, next_term, next_year = next_items[0]
    nearest_day, nearest_term, nearest_year = min(
        dated_terms,
        key=lambda item: (abs((item[0] - target).days), item[0]),
    )

    return {
        "date": target.isoformat(),
        "current_term": term_payload(previous_term, previous_year, target),
        "next_term": term_payload(next_term, next_year, target),
        "nearest_term": term_payload(nearest_term, nearest_year, target),
        "days_until_next_term": (next_day - target).days,
        "days_since_current_term": (target - previous_day).days,
        "feng_shui_use": [
            "Treat solar terms as a seasonal qi and yin-yang timing layer, not as a complete almanac.",
            "Use spring terms for renewal and growth, summer terms for visibility and activity, autumn terms for refinement and pruning, and winter terms for storage and root repair.",
            "Use equinoxes for balance and comparison, solstices for peak-turning points, and the four beginnings for seasonal gate changes.",
        ],
        "limitations": [
            "This helper uses common approximate Gregorian dates; exact solar-term moments vary by year and time zone.",
            "Solar terms alone do not determine auspiciousness; compare event type, candidate-date attributes, moon phase, annual cautions, personal constraints, local conditions, and lineage-specific date selection.",
            "This is not a full tong shu, bazi, qimen, liuren, or precise astronomy engine.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Approximate 24 solar terms and symbolic timing context."
    )
    parser.add_argument("date", type=parse_date, help="Gregorian date in YYYY-MM-DD format.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(
        json.dumps(
            solar_terms_for_date(args.date),
            ensure_ascii=True,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
