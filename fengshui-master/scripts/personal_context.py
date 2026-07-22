#!/usr/bin/env python3
"""Build a bounded personal feng shui context pack from existing helpers."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import date, datetime, time
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import annual_afflictions
import ganzhi
import minggua
import moon_phase
import periods
import solar_terms


PROACTIVE_SCAN_CONTRACT = {
    "status_labels": [
        "observed",
        "calculated",
        "inferred",
        "unknown",
        "recommended",
    ],
    "domains": [
        "current timing posture",
        "career and learning",
        "finance and resources",
        "relationships and support",
        "wellbeing and environment",
        "decision load and execution",
    ],
    "required_for_each": [
        "favorable_signals",
        "possible_friction",
        "how_it_may_manifest",
        "confirmation_or_refutation_evidence",
        "immediate_low_risk_action",
    ],
    "action_horizons": ["next_72_hours", "next_30_days", "next_90_days"],
    "selection_rule": "scan only the requested domain and materially relevant adjacent domains",
    "inference_rule": "state possible problems as conditional hypotheses and ask what evidence confirms or refutes them",
}

IANA_REGION_PREFIXES = {
    "Africa",
    "America",
    "Antarctica",
    "Arctic",
    "Asia",
    "Atlantic",
    "Australia",
    "Europe",
    "Indian",
    "Pacific",
}


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD format") from exc


def parse_time(value: str) -> time:
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("time must use 24-hour HH:MM format") from exc


def validate_timezone(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        ZoneInfo(value)
    except ZoneInfoNotFoundError as exc:
        parts = value.split("/")
        structurally_valid = (
            len(parts) >= 2
            and parts[0] in IANA_REGION_PREFIXES
            and all(
                part
                and all(character.isalnum() or character in "_-+" for character in part)
                for part in parts
            )
        )
        if not structurally_valid:
            raise ValueError(f"unknown IANA timezone: {value}") from exc
    return value


def timezone_validation_level(value: str | None) -> str:
    if value is None:
        return "not supplied"
    try:
        ZoneInfo(value)
        return "validated against the runtime IANA timezone database"
    except ZoneInfoNotFoundError:
        return "IANA region syntax validated; runtime timezone database unavailable"


def effective_year_for_date(value: date, boundary_mode: str) -> tuple[int, dict[str, Any]]:
    if boundary_mode == "gregorian":
        return value.year, {
            "mode": "gregorian",
            "effective_year": value.year,
            "boundary": f"{value.year}-01-01",
            "precision": "civil calendar year",
        }
    if boundary_mode != "li_chun_approx":
        raise ValueError("year boundary must be gregorian or li_chun_approx")

    approximate_boundary = date(value.year, 2, 4)
    effective_year = value.year - 1 if value < approximate_boundary else value.year
    return effective_year, {
        "mode": "li_chun_approx",
        "effective_year": effective_year,
        "boundary": approximate_boundary.isoformat(),
        "precision": "common approximate Li Chun date; not the exact local solar-term moment",
    }


def safe_period_context(year: int) -> dict[str, Any]:
    try:
        return asdict(periods.period_for_year(year))
    except ValueError as exc:
        return {
            "status": "unavailable",
            "year": year,
            "reason": str(exc),
        }


def build_personal_context(
    birth_date: date,
    *,
    birth_time: time | None = None,
    sex: str | None = None,
    birth_location: str | None = None,
    timezone: str | None = None,
    as_of: date | None = None,
    year_boundary: str = "gregorian",
) -> dict[str, Any]:
    target = as_of or date.today()
    timezone = validate_timezone(timezone)
    birth_effective_year, birth_boundary = effective_year_for_date(
        birth_date, year_boundary
    )
    current_effective_year, current_boundary = effective_year_for_date(
        target, year_boundary
    )
    birth_year = asdict(ganzhi.ganzhi_for_year(birth_effective_year))
    current_year = asdict(ganzhi.ganzhi_for_year(current_effective_year))
    personal_gua = (
        asdict(minggua.ming_gua(birth_effective_year, sex)) if sex else None
    )

    missing_inputs: list[str] = []
    if birth_time is None:
        missing_inputs.append("birth time for external full-chart work")
    if not sex:
        missing_inputs.append("sex or lineage convention for ming gua")
    if not birth_location:
        missing_inputs.append("birth location for timezone and locality-sensitive work")
    if not timezone:
        missing_inputs.append("timezone for precision calendar or astronomy work")

    return {
        "method": "personal-feng-shui-context-scaffold",
        "inputs": {
            "birth_date": birth_date.isoformat(),
            "birth_time": birth_time.strftime("%H:%M") if birth_time else None,
            "sex": sex,
            "birth_location": birth_location,
            "timezone": timezone,
            "as_of": target.isoformat(),
            "year_boundary": year_boundary,
        },
        "input_usage": {
            "birth_date": "used for the selected year-boundary scaffold and approximate date helpers",
            "birth_time": "recorded for external full-chart or precision-calendar work; not used in the bundled year-level calculations",
            "birth_location": "recorded for external locality-sensitive work; not geocoded or used in the bundled calculations",
            "timezone": "recorded for external precision work; date-only bundled helpers do not use an exact instant",
        },
        "validation_provenance": {
            "timezone": timezone_validation_level(timezone),
        },
        "birth_context": {
            "effective_year": birth_effective_year,
            "year_boundary_provenance": birth_boundary,
            "year_ganzhi": birth_year,
            "ming_gua": personal_gua,
            "approximate_solar_term": solar_terms.solar_terms_for_date(birth_date),
            "approximate_moon_phase": moon_phase.moon_phase(birth_date),
        },
        "current_context": {
            "effective_year": current_effective_year,
            "year_boundary_provenance": current_boundary,
            "year_ganzhi": current_year,
            "san_yuan_period": safe_period_context(current_effective_year),
            "annual_directional_cautions": annual_afflictions.annual_afflictions_for_year(
                current_effective_year
            ),
            "approximate_solar_term": solar_terms.solar_terms_for_date(target),
            "approximate_moon_phase": moon_phase.moon_phase(target),
        },
        "interpretation_order": [
            "state real-world context and the user's actual question first",
            "label each calculation and its convention",
            "separate birth-year and ming-gua scaffolds from full natal systems",
            "treat current timing layers as conditional symbolic context",
            "end with reversible actions and missing data",
        ],
        "proactive_scan_contract": PROACTIVE_SCAN_CONTRACT,
        "missing_inputs": missing_inputs,
        "limitations": [
            "This is not a complete bazi, zi wei, qimen, liuren, or tong shu calculation.",
            "It does not calculate month, day, or hour pillars, true solar time, lunar-calendar conversion, or lineage-specific chart rules.",
            "Birth and current moon phases and solar terms are approximate helper outputs, not precision astronomy.",
            "The li_chun_approx mode uses February 4 as a documented approximation and does not calculate the exact local Li Chun moment.",
            "Birth time, location, and timezone do not turn this year-level scaffold into a full natal chart.",
            "Do not use this context pack for deterministic fate, health, wealth, marriage, disaster, or market predictions.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a bounded personal feng shui context pack."
    )
    parser.add_argument("--birth-date", type=parse_date, required=True)
    parser.add_argument("--birth-time", type=parse_time)
    parser.add_argument("--sex", choices=["male", "female"])
    parser.add_argument("--birth-location")
    parser.add_argument("--timezone")
    parser.add_argument(
        "--year-boundary",
        choices=["gregorian", "li_chun_approx"],
        default="gregorian",
        help="Year boundary convention for year-level ganzhi and ming gua scaffolds.",
    )
    parser.add_argument("--as-of", type=parse_date, default=date.today())
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    try:
        result = build_personal_context(
            args.birth_date,
            birth_time=args.birth_time,
            sex=args.sex,
            birth_location=args.birth_location,
            timezone=args.timezone,
            as_of=args.as_of,
            year_boundary=args.year_boundary,
        )
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(result, ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
