#!/usr/bin/env python3
"""Create a basic Luo Shu flying-star chart from a period or year."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


PERIODS = [
    (1, 1864, 1883),
    (2, 1884, 1903),
    (3, 1904, 1923),
    (4, 1924, 1943),
    (5, 1944, 1963),
    (6, 1964, 1983),
    (7, 1984, 2003),
    (8, 2004, 2023),
    (9, 2024, 2043),
]

FLIGHT_PATH = [
    "center",
    "northwest",
    "west",
    "northeast",
    "south",
    "north",
    "southwest",
    "east",
    "southeast",
]

PALACE_INFO = {
    "center": ("center", "earth"),
    "northwest": ("qian", "metal"),
    "west": ("dui", "metal"),
    "northeast": ("gen", "earth"),
    "south": ("li", "fire"),
    "north": ("kan", "water"),
    "southwest": ("kun", "earth"),
    "east": ("zhen", "wood"),
    "southeast": ("xun", "wood"),
}


@dataclass(frozen=True)
class FlyingStarsChart:
    period: int
    center: int
    direction: str
    period_year_range: str | None
    palaces: dict[str, dict[str, int | str]]
    note: str


def wrap_star(value: int) -> int:
    return ((value - 1) % 9) + 1


def period_for_year(year: int) -> tuple[int, int, int]:
    for period, start, end in PERIODS:
        if start <= year <= end:
            return period, start, end
    raise ValueError("supported year range is 1864-2043")


def flying_chart(period: int, direction: str = "forward") -> FlyingStarsChart:
    if period < 1 or period > 9:
        raise ValueError("period must be 1-9")
    if direction not in {"forward", "reverse"}:
        raise ValueError("direction must be forward or reverse")

    palaces: dict[str, dict[str, int | str]] = {}
    step = 1 if direction == "forward" else -1
    for offset, palace in enumerate(FLIGHT_PATH):
        star = wrap_star(period + (offset * step))
        trigram, element = PALACE_INFO[palace]
        palaces[palace] = {
            "star": star,
            "trigram": trigram,
            "element": element,
        }

    return FlyingStarsChart(
        period=period,
        center=period,
        direction=direction,
        period_year_range=None,
        palaces=palaces,
        note="Basic Luo Shu flight only. This is not a full Xuan Kong natal chart; mountain/wealth stars, replacement stars, facing/sitting, and lineage rules are not calculated.",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a basic Luo Shu flying-star chart from a period or year."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--period", type=int, help="San Yuan period number, 1-9.")
    group.add_argument("--year", type=int, help="Gregorian year, 1864-2043.")
    parser.add_argument(
        "--direction",
        choices=["forward", "reverse"],
        default="forward",
        help="Flight direction for the basic Luo Shu sequence.",
    )
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    period_year_range = None
    period = args.period
    if args.year is not None:
        try:
            period, start, end = period_for_year(args.year)
        except ValueError as exc:
            parser.error(str(exc))
        period_year_range = f"{start}-{end}"

    try:
        chart = flying_chart(period, args.direction)
    except ValueError as exc:
        parser.error(str(exc))

    data = asdict(chart)
    data["period_year_range"] = period_year_range
    print(json.dumps(data, ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
