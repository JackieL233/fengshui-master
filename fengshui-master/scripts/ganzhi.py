#!/usr/bin/env python3
"""Return a simple Gregorian-year ganzhi scaffold."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


STEMS = [
    ("jia", "甲", "wood", "yang"),
    ("yi", "乙", "wood", "yin"),
    ("bing", "丙", "fire", "yang"),
    ("ding", "丁", "fire", "yin"),
    ("wu", "戊", "earth", "yang"),
    ("ji", "己", "earth", "yin"),
    ("geng", "庚", "metal", "yang"),
    ("xin", "辛", "metal", "yin"),
    ("ren", "壬", "water", "yang"),
    ("gui", "癸", "water", "yin"),
]

BRANCHES = [
    ("zi", "子", "rat", "water"),
    ("chou", "丑", "ox", "earth"),
    ("yin", "寅", "tiger", "wood"),
    ("mao", "卯", "rabbit", "wood"),
    ("chen", "辰", "dragon", "earth"),
    ("si", "巳", "snake", "fire"),
    ("wu", "午", "horse", "fire"),
    ("wei", "未", "goat", "earth"),
    ("shen", "申", "monkey", "metal"),
    ("you", "酉", "rooster", "metal"),
    ("xu", "戌", "dog", "earth"),
    ("hai", "亥", "pig", "water"),
]


@dataclass(frozen=True)
class GanzhiYear:
    year: int
    stem: str
    stem_hanzi: str
    stem_phase: str
    stem_yin_yang: str
    branch: str
    branch_hanzi: str
    zodiac: str
    branch_phase: str
    ganzhi: str
    ganzhi_hanzi: str
    cycle_position: int
    boundary_note: str
    scope_note: str


def ganzhi_for_year(year: int) -> GanzhiYear:
    cycle_index = (year - 4) % 60
    stem = STEMS[cycle_index % 10]
    branch = BRANCHES[cycle_index % 12]
    stem_name, stem_hanzi, stem_phase, stem_yin_yang = stem
    branch_name, branch_hanzi, zodiac, branch_phase = branch
    return GanzhiYear(
        year=year,
        stem=stem_name,
        stem_hanzi=stem_hanzi,
        stem_phase=stem_phase,
        stem_yin_yang=stem_yin_yang,
        branch=branch_name,
        branch_hanzi=branch_hanzi,
        zodiac=zodiac,
        branch_phase=branch_phase,
        ganzhi=f"{stem_name}-{branch_name}",
        ganzhi_hanzi=f"{stem_hanzi}{branch_hanzi}",
        cycle_position=cycle_index + 1,
        boundary_note=(
            "This helper uses the Gregorian year label. For birth-year or annual feng shui "
            "work near late January or early February, confirm the li chun or lunar-year boundary "
            "used by the chosen lineage."
        ),
        scope_note=(
            "This is a year-pillar scaffold only. It is not a complete bazi, zi wei, qimen, "
            "liuren, or almanac calculation."
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Return the heavenly stem and earthly branch scaffold for a Gregorian year."
    )
    parser.add_argument("year", type=int, help="Gregorian year label.")
    parser.add_argument(
        "--pretty", action="store_true", help="Print indented JSON for humans."
    )
    args = parser.parse_args()

    print(
        json.dumps(
            asdict(ganzhi_for_year(args.year)),
            ensure_ascii=True,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
