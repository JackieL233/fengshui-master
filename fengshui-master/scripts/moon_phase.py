#!/usr/bin/env python3
"""Approximate moon phase context for FengShui Master timing work."""

from __future__ import annotations

import argparse
import json
import math
from datetime import date, datetime, timezone
from typing import Any


SYNODIC_MONTH_DAYS = 29.530588853
KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)


PHASES = [
    (
        "new_moon",
        "New Moon / 新月 / 朔",
        1.84566,
        "Use as a symbolic layer for new beginnings, seeding intent, quiet planning, reset, concealment, and inward gathering.",
    ),
    (
        "waxing_crescent",
        "Waxing Crescent / 娥眉月",
        5.53699,
        "Use as a symbolic layer for early growth, preparation, first commitments, and cautious activation.",
    ),
    (
        "first_quarter",
        "First Quarter / 上弦",
        9.22831,
        "Use as a symbolic layer for decision, friction, structural adjustment, and visible effort.",
    ),
    (
        "waxing_gibbous",
        "Waxing Gibbous / 盈凸月",
        12.91963,
        "Use as a symbolic layer for refinement, review, accumulation, and preparing to reveal.",
    ),
    (
        "full_moon",
        "Full Moon / 满月 / 望",
        16.61096,
        "Use as a symbolic layer for visibility, culmination, illumination, public release, harvest, and release.",
    ),
    (
        "waning_gibbous",
        "Waning Gibbous / 亏凸月",
        20.30228,
        "Use as a symbolic layer for distribution, teaching, evaluation, and integrating what became visible.",
    ),
    (
        "last_quarter",
        "Last Quarter / 下弦",
        23.99361,
        "Use as a symbolic layer for correction, pruning, simplification, and cutting leakage.",
    ),
    (
        "waning_crescent",
        "Waning Crescent / 残月",
        27.68493,
        "Use as a symbolic layer for rest, closure, hidden repair, clearing, and conserving qi.",
    ),
]


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD format") from exc


def phase_for_age(age: float) -> tuple[str, str, str]:
    for key, label, upper_bound, guidance in PHASES:
        if age < upper_bound:
            return key, label, guidance
    key, label, _, guidance = PHASES[0]
    return key, label, guidance


def distance_to(age: float, target: float) -> float:
    direct = abs(age - target)
    return min(direct, SYNODIC_MONTH_DAYS - direct)


def moon_phase(day: date) -> dict[str, Any]:
    moment = datetime(day.year, day.month, day.day, 12, 0, tzinfo=timezone.utc)
    days_since_known_new = (moment - KNOWN_NEW_MOON).total_seconds() / 86400
    age = days_since_known_new % SYNODIC_MONTH_DAYS
    cycle_fraction = age / SYNODIC_MONTH_DAYS
    illumination = (1 - math.cos(2 * math.pi * cycle_fraction)) / 2
    phase_key, phase_label, symbolic_guidance = phase_for_age(age)

    return {
        "date": day.isoformat(),
        "phase_key": phase_key,
        "phase_label": phase_label,
        "moon_age_days": round(age, 2),
        "cycle_fraction": round(cycle_fraction, 4),
        "illumination": round(illumination, 4),
        "days_from_new_moon": round(distance_to(age, 0.0), 2),
        "days_from_full_moon": round(distance_to(age, SYNODIC_MONTH_DAYS / 2), 2),
        "symbolic_guidance": symbolic_guidance,
        "feng_shui_use": [
            "Treat moon phase as a secondary symbolic timing layer after safety, law, weather, budget, professional constraints, and lineage-specific date selection.",
            "Use new moon / 新月 for intent-setting, quiet starts, preparation, and inward renewal when the event benefits from containment.",
            "Use full moon / 满月 for visibility, culmination, release, review, and public-facing moments when the event benefits from illumination.",
        ],
        "limitations": [
            "This is not a full almanac, precise astronomy engine, or traditional tong shu date-selection calculation.",
            "Moon phase alone does not determine auspiciousness; compare event type, candidate date attributes, local time zone, solar terms, personal constraints, and practical requirements.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Approximate moon phase and symbolic timing context."
    )
    parser.add_argument("date", type=parse_date, help="Gregorian date in YYYY-MM-DD format.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(json.dumps(moon_phase(args.date), ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
