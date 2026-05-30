#!/usr/bin/env python3
"""Return the San Yuan / Xuan Kong 20-year period for a supported year."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


PERIODS = [
    (1, 1864, 1883, "kan", "坎", "water"),
    (2, 1884, 1903, "kun", "坤", "earth"),
    (3, 1904, 1923, "zhen", "震", "wood"),
    (4, 1924, 1943, "xun", "巽", "wood"),
    (5, 1944, 1963, "center", "中", "earth"),
    (6, 1964, 1983, "qian", "乾", "metal"),
    (7, 1984, 2003, "dui", "兑", "metal"),
    (8, 2004, 2023, "gen", "艮", "earth"),
    (9, 2024, 2043, "li", "离", "fire"),
]


@dataclass(frozen=True)
class PeriodResult:
    year: int
    period: int
    start_year: int
    end_year: int
    trigram: str
    hanzi: str
    element: str
    note: str


def period_for_year(year: int) -> PeriodResult:
    for period, start, end, trigram, hanzi, element in PERIODS:
        if start <= year <= end:
            return PeriodResult(
                year=year,
                period=period,
                start_year=start,
                end_year=end,
                trigram=trigram,
                hanzi=hanzi,
                element=element,
                note="Uses the common 1864-2043 San Yuan 20-year period sequence; verify lineage and calendar boundary before exact flying-star work.",
            )
    raise ValueError("supported range is 1864-2043")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Return the common San Yuan / Xuan Kong 20-year period for a year."
    )
    parser.add_argument("year", type=int, help="Gregorian year, 1864-2043.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    try:
        data = asdict(period_for_year(args.year))
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(data, ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
