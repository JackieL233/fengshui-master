#!/usr/bin/env python3
"""Build a bounded personal feng shui context pack from existing helpers."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import date, datetime, time
from typing import Any

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


def build_personal_context(
    birth_date: date,
    *,
    birth_time: time | None = None,
    sex: str | None = None,
    birth_location: str | None = None,
    timezone: str | None = None,
    as_of: date | None = None,
) -> dict[str, Any]:
    target = as_of or date.today()
    birth_year = asdict(ganzhi.ganzhi_for_year(birth_date.year))
    current_year = asdict(ganzhi.ganzhi_for_year(target.year))
    personal_gua = asdict(minggua.ming_gua(birth_date.year, sex)) if sex else None

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
        },
        "birth_context": {
            "year_ganzhi": birth_year,
            "ming_gua": personal_gua,
            "approximate_solar_term": solar_terms.solar_terms_for_date(birth_date),
            "approximate_moon_phase": moon_phase.moon_phase(birth_date),
        },
        "current_context": {
            "year_ganzhi": current_year,
            "san_yuan_period": asdict(periods.period_for_year(target.year)),
            "annual_directional_cautions": annual_afflictions.annual_afflictions_for_year(
                target.year
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
    parser.add_argument("--as-of", type=parse_date, default=date.today())
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(
        json.dumps(
            build_personal_context(
                args.birth_date,
                birth_time=args.birth_time,
                sex=args.sex,
                birth_location=args.birth_location,
                timezone=args.timezone,
                as_of=args.as_of,
            ),
            ensure_ascii=True,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
