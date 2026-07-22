#!/usr/bin/env python3
"""Map a compass bearing to the 24 mountains used by a luopan."""

from __future__ import annotations

import argparse
import json
import math
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
    distance_to_boundary_degrees: float
    uncertainty_degrees: float | None
    boundary_status: str
    north_basis: str
    note: str


def normalize_bearing(bearing: float) -> float:
    return bearing % 360.0


def mountain_for_bearing(
    bearing: float,
    uncertainty_degrees: float | None = None,
    north_basis: str = "unspecified",
) -> MountainResult:
    if not math.isfinite(bearing):
        raise ValueError("bearing must be finite")
    if uncertainty_degrees is not None and (
        not math.isfinite(uncertainty_degrees) or uncertainty_degrees < 0
    ):
        raise ValueError("uncertainty must be a finite non-negative number")
    if north_basis not in {"magnetic", "true", "grid", "unspecified"}:
        raise ValueError("north basis must be magnetic, true, grid, or unspecified")
    normalized = normalize_bearing(bearing)
    index = int(((normalized + 7.5) % 360) // 15)
    mountain, hanzi, direction, element, animal, sector = MOUNTAINS[index]
    center = (index * 15.0) % 360.0
    angular_delta = abs(((normalized - center + 180) % 360) - 180)
    distance_to_boundary = 7.5 - angular_delta
    if uncertainty_degrees is None:
        boundary_status = "measurement_uncertainty_not_supplied"
    elif uncertainty_degrees >= distance_to_boundary:
        boundary_status = "uncertainty_crosses_boundary"
    else:
        boundary_status = "within_sector"
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
        distance_to_boundary_degrees=round(distance_to_boundary, 6),
        uncertainty_degrees=uncertainty_degrees,
        boundary_status=boundary_status,
        north_basis=north_basis,
        note="A 24-mountain lookup is only as reliable as the supplied bearing, uncertainty, north basis, site measurement, and lineage convention.",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Return the 24-mountain luopan sector for a compass bearing."
    )
    parser.add_argument("bearing", type=float, help="Compass bearing in degrees.")
    parser.add_argument(
        "--uncertainty-degrees",
        type=float,
        help="Optional estimated bearing uncertainty in degrees.",
    )
    parser.add_argument(
        "--north-basis",
        choices=["magnetic", "true", "grid", "unspecified"],
        default="unspecified",
        help="Reference north used by the supplied bearing.",
    )
    parser.add_argument(
        "--pretty", action="store_true", help="Print indented JSON for humans."
    )
    args = parser.parse_args()

    try:
        data = asdict(
            mountain_for_bearing(
                args.bearing,
                uncertainty_degrees=args.uncertainty_degrees,
                north_basis=args.north_basis,
            )
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(data, ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
