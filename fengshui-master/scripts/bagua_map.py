#!/usr/bin/env python3
"""Return bagua sector symbolism for FengShui Master analysis."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BaguaSector:
    key: str
    trigram: str
    trigram_zh: str
    direction: str
    center_degrees: int | None
    phase: str
    family_role: str
    image: str
    life_area: str
    domain_symbolism: str
    supportive_actions: list[str]
    cautions: list[str]


SECTORS = [
    BaguaSector(
        "kan",
        "kan",
        "坎",
        "north",
        0,
        "water",
        "middle son",
        "water, depth, movement, hidden flow",
        "career, path, flow, networks",
        "Use for career direction, research, communication flow, liquidity, adaptability, and hidden information.",
        ["clarify direction", "improve flow", "support quiet research", "reduce blocked circulation"],
        ["avoid excessive drift", "do not use water features where unsafe or impractical"],
    ),
    BaguaSector(
        "gen",
        "gen",
        "艮",
        "northeast",
        45,
        "earth",
        "youngest son",
        "mountain, stillness, boundary, study",
        "knowledge, learning, self-cultivation, pause",
        "Use for study, reflection, skill-building, boundaries, and disciplined pauses before action.",
        ["create quiet study support", "reduce distraction", "stabilize routines", "mark clear boundaries"],
        ["avoid turning stillness into stagnation", "do not block safe access or ventilation"],
    ),
    BaguaSector(
        "zhen",
        "zhen",
        "震",
        "east",
        90,
        "wood",
        "eldest son",
        "thunder, arousal, initiative, movement",
        "family, growth, renewal, initiative",
        "Use for growth, family systems, health-adjacent routines, starting motion, and restoring momentum.",
        ["add healthy movement", "repair family flow", "support morning routines", "prune overgrowth"],
        ["avoid noisy activation during rest needs", "do not promise health outcomes"],
    ),
    BaguaSector(
        "xun",
        "xun",
        "巽",
        "southeast",
        135,
        "wood",
        "eldest daughter",
        "wind, penetration, gradual influence",
        "wealth, resources, reputation flow, refinement",
        "Use for resource growth, brand reach, learning diffusion, savings habits, and gradual influence.",
        ["support steady growth", "reduce financial leakage", "improve reputation flow", "keep records clear"],
        ["do not treat southeast as guaranteed wealth", "finance decisions still require real risk analysis"],
    ),
    BaguaSector(
        "li",
        "li",
        "离",
        "south",
        180,
        "fire",
        "middle daughter",
        "fire, clarity, visibility, attachment",
        "fame, recognition, visibility, clarity",
        "Use for visibility, reputation, public launch, storytelling, evaluation, and clear presentation.",
        ["improve lighting", "clarify message", "prepare public proof", "cool excess urgency"],
        ["avoid hype, burnout, glare, or exposure without substance", "do not guarantee recognition"],
    ),
    BaguaSector(
        "kun",
        "kun",
        "坤",
        "southwest",
        225,
        "earth",
        "mother",
        "earth, receptivity, support, nourishment",
        "relationships, partnership, receiving support",
        "Use for partnership, shared responsibility, stability, care, and support systems.",
        ["strengthen mutual support", "reduce cluttered obligations", "create stable shared space", "clarify agreements"],
        ["do not predict romance or another person's feelings", "prioritize consent and safety"],
    ),
    BaguaSector(
        "dui",
        "dui",
        "兑",
        "west",
        270,
        "metal",
        "youngest daughter",
        "lake, joy, speech, exchange",
        "children, creativity, joy, communication",
        "Use for creative output, speech, social exchange, delight, and feedback loops.",
        ["support creative review", "improve communication hygiene", "make feedback visible", "contain scattered pleasure"],
        ["avoid gossip, overpromising, or careless speech", "do not force family or fertility claims"],
    ),
    BaguaSector(
        "qian",
        "qian",
        "乾",
        "northwest",
        315,
        "metal",
        "father",
        "heaven, authority, leadership, structure",
        "helpful people, mentors, leadership, travel",
        "Use for mentors, leadership, governance, decision rights, travel support, and external allies.",
        ["clarify authority", "ask for support", "strengthen standards", "organize travel or mentor channels"],
        ["avoid rigid control or savior claims", "do not replace legal, HR, or governance review"],
    ),
    BaguaSector(
        "center",
        "center",
        "中宫",
        "center",
        None,
        "earth",
        "center",
        "center, integration, stability",
        "health-adjacent balance, grounding, integration",
        "Use for integration, household coherence, operations, stability, and reducing central clutter or pressure.",
        ["keep center open", "support circulation", "stabilize routines", "reduce central clutter"],
        ["do not diagnose health", "do not overload the center with heavy symbolic cures"],
    ),
]


DIRECTION_ALIASES = {
    "n": "north",
    "north": "north",
    "ne": "northeast",
    "northeast": "northeast",
    "e": "east",
    "east": "east",
    "se": "southeast",
    "southeast": "southeast",
    "s": "south",
    "south": "south",
    "sw": "southwest",
    "southwest": "southwest",
    "w": "west",
    "west": "west",
    "nw": "northwest",
    "northwest": "northwest",
    "center": "center",
    "middle": "center",
}

LIFE_AREA_ALIASES = {
    "career": "kan",
    "path": "kan",
    "flow": "kan",
    "knowledge": "gen",
    "learning": "gen",
    "study": "gen",
    "family": "zhen",
    "growth": "zhen",
    "renewal": "zhen",
    "wealth": "xun",
    "resources": "xun",
    "money": "xun",
    "reputation": "li",
    "fame": "li",
    "visibility": "li",
    "relationship": "kun",
    "relationships": "kun",
    "partnership": "kun",
    "creativity": "dui",
    "children": "dui",
    "communication": "dui",
    "helpful_people": "qian",
    "mentors": "qian",
    "leadership": "qian",
    "travel": "qian",
    "health": "center",
    "wellbeing": "center",
    "center": "center",
}


def normalize(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def sector_to_payload(sector: BaguaSector, method: str) -> dict[str, Any]:
    return {
        "key": sector.key,
        "trigram": sector.trigram,
        "trigram_zh": sector.trigram_zh,
        "direction": sector.direction,
        "center_degrees": sector.center_degrees,
        "phase": sector.phase,
        "family_role": sector.family_role,
        "image": sector.image,
        "life_area": sector.life_area,
        "domain_symbolism": sector.domain_symbolism,
        "supportive_actions": sector.supportive_actions,
        "cautions": sector.cautions,
        "method": method,
    }


def sector_by_key(key: str) -> BaguaSector:
    normalized = normalize(key)
    for sector in SECTORS:
        if normalized in {
            sector.key,
            sector.trigram,
            normalize(sector.trigram_zh),
            normalize(sector.direction),
        }:
            return sector
    if normalized in DIRECTION_ALIASES:
        direction = DIRECTION_ALIASES[normalized]
        return next(sector for sector in SECTORS if sector.direction == direction)
    if normalized in LIFE_AREA_ALIASES:
        mapped = LIFE_AREA_ALIASES[normalized]
        return next(sector for sector in SECTORS if sector.key == mapped)
    raise ValueError(f"unsupported bagua lookup: {key}")


def sector_by_degrees(degrees: float) -> BaguaSector:
    bearing = degrees % 360
    if 337.5 <= bearing or bearing < 22.5:
        direction = "north"
    elif bearing < 67.5:
        direction = "northeast"
    elif bearing < 112.5:
        direction = "east"
    elif bearing < 157.5:
        direction = "southeast"
    elif bearing < 202.5:
        direction = "south"
    elif bearing < 247.5:
        direction = "southwest"
    elif bearing < 292.5:
        direction = "west"
    else:
        direction = "northwest"
    return next(sector for sector in SECTORS if sector.direction == direction)


def bagua_lookup(
    *,
    direction: str | None = None,
    degrees: float | None = None,
    trigram: str | None = None,
    life_area: str | None = None,
    method: str = "compass",
) -> dict[str, Any]:
    supplied = [value is not None for value in [direction, degrees, trigram, life_area]].count(True)
    if supplied != 1:
        raise ValueError("provide exactly one of direction, degrees, trigram, or life_area")
    if method not in {"compass", "door_aligned", "symbolic"}:
        raise ValueError("method must be compass, door_aligned, or symbolic")

    if degrees is not None:
        sector = sector_by_degrees(degrees)
    elif direction is not None:
        sector = sector_by_key(direction)
    elif trigram is not None:
        sector = sector_by_key(trigram)
    else:
        assert life_area is not None
        sector = sector_by_key(life_area)

    return {
        "query": {
            "direction": direction,
            "degrees": degrees,
            "trigram": trigram,
            "life_area": life_area,
            "method": method,
        },
        "sector": sector_to_payload(sector, method),
        "feng_shui_use": [
            "Use compass bagua only when a reliable north/facing convention is available.",
            "Use door-aligned or symbolic bagua only when that modern overlay is explicitly chosen or no reliable compass data exists.",
            "Use bagua as a symbolic map for qi, direction, phase, role, and life-area emphasis; verify against form, safety, and practical constraints.",
        ],
        "limitations": [
            "Bagua mapping alone does not determine auspiciousness, wealth, relationship success, health, or career outcomes.",
            "Do not mix compass bagua, door-aligned bagua, eight mansions, and flying stars without naming the method and conflict.",
            "High-stakes finance, medical, legal, engineering, and safety questions require native-domain evidence and qualified support first.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Return bagua sector symbolism.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--direction", help="Direction such as north, southeast, or NW.")
    group.add_argument("--degrees", type=float, help="Compass bearing in degrees.")
    group.add_argument("--trigram", help="Trigram key such as qian, kan, li, or xun.")
    group.add_argument("--life-area", help="Life area such as wealth, career, relationship, or helpful_people.")
    parser.add_argument(
        "--method",
        default="compass",
        choices=["compass", "door_aligned", "symbolic"],
        help="Bagua method label.",
    )
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(
        json.dumps(
            bagua_lookup(
                direction=args.direction,
                degrees=args.degrees,
                trigram=args.trigram,
                life_area=args.life_area,
                method=args.method,
            ),
            ensure_ascii=True,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
