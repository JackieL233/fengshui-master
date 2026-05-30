#!/usr/bin/env python3
"""Map a compass bearing to the 24 mountains used by a luopan."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


MOUNTAINS = [
    ("zi", "子", "north", "water", "rat", "N2"),
    ("gui", "癸", "north-northeast", "water", None, "N3"),
    ("chou", "丑", "north-northeast", "earth", "ox", "NE1"),
    ("gen", "艮", "northeast", "earth", None, "NE2"),
    ("yin", "寅", "east-northeast", "wood", "tiger", "NE3"),
    ("jia", "甲", "east-northeast", "wood", None, "E1"),
    ("mao", "卯", "east", "wood", "rabbit", "E2"),
    ("yi", "乙", "east-southeast", "wood", None, "E3"),
    ("chen", "辰", "east-southeast", "earth", "dragon", "SE1"),
    ("xun", "巽", "southeast", "wood", None, "SE2"),
    ("si", "巳", "south-southeast", "fire", "snake", "SE3"),
    ("bing", "丙", "south-southeast", "fire", None, "S1"),
    ("wu", "午", "south", "fire", "horse", "S2"),
    ("ding", "丁", "south-southwest", "fire", None, "S3"),
    ("wei", "未", "south-southwest", "earth", "goat", "SW1"),
    ("kun", "坤", "southwest", "earth", None, "SW2"),
    ("shen", "申", "west-southwest", "metal", "monkey", "SW3"),
    ("geng", "庚", "west-southwest", "metal", None, "W1"),
    ("you", "酉", "west", "metal", "rooster", "W2"),
    ("xin", "辛", "west-northwest", "metal", None, "W3"),
    ("xu", "戌", "west-northwest", "earth", "dog", "NW1"),
    ("qian", "乾", "northwest", "metal", None, "NW2"),
    ("hai", "亥", "north-northwest", "water", "pig", "NW3"),
    ("ren", "壬", "north-northwest", "water", None, "N1"),
]


@dataclass(frozen=True)
class MountainResult:
    bearing: float
    normalized_bearing: float
    mountain: str
    hanzi: str
    direction: str
    element: str
    branch_animal: str | None
    sector: str
    center_degrees: float
    range_start_degrees: float
    range_end_degrees: float


def normalize_bearing(bearing: float) -> float:
    return bearing % 360.0


def mountain_for_bearing(bearing: float) -> MountainResult:
    normalized = normalize_bearing(bearing)
    index = int(((normalized + 7.5) % 360) // 15)
    mountain, hanzi, direction, element, animal, sector = MOUNTAINS[index]
    center = (index * 15.0) % 360.0
    return MountainResult(
        bearing=bearing,
        normalized_bearing=normalized,
        mountain=mountain,
        hanzi=hanzi,
        direction=direction,
        element=element,
        branch_animal=animal,
        sector=sector,
        center_degrees=center,
        range_start_degrees=(center - 7.5) % 360.0,
        range_end_degrees=(center + 7.5) % 360.0,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Return the 24-mountain luopan sector for a compass bearing."
    )
    parser.add_argument("bearing", type=float, help="Compass bearing in degrees.")
    parser.add_argument(
        "--pretty", action="store_true", help="Print indented JSON for humans."
    )
    args = parser.parse_args()

    data = asdict(mountain_for_bearing(args.bearing))
    print(json.dumps(data, ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
