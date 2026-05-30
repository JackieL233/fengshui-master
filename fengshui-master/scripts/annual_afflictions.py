#!/usr/bin/env python3
"""Return common annual feng shui directional cautions."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent


def load_ganzhi() -> Any:
    path = SCRIPT_DIR / "ganzhi.py"
    spec = importlib.util.spec_from_file_location("ganzhi", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ganzhi = load_ganzhi()


BRANCH_DIRECTIONS = {
    "zi": ("子", "north", 0),
    "chou": ("丑", "north-northeast", 30),
    "yin": ("寅", "east-northeast", 60),
    "mao": ("卯", "east", 90),
    "chen": ("辰", "east-southeast", 120),
    "si": ("巳", "south-southeast", 150),
    "wu": ("午", "south", 180),
    "wei": ("未", "south-southwest", 210),
    "shen": ("申", "west-southwest", 240),
    "you": ("酉", "west", 270),
    "xu": ("戌", "west-northwest", 300),
    "hai": ("亥", "north-northwest", 330),
}

BRANCH_ORDER = list(BRANCH_DIRECTIONS)

SAN_SHA_BY_TRIAD = {
    frozenset({"shen", "zi", "chen"}): {
        "direction": "south",
        "branches": ["si", "wu", "wei"],
        "center_degrees": 180,
    },
    frozenset({"yin", "wu", "xu"}): {
        "direction": "north",
        "branches": ["hai", "zi", "chou"],
        "center_degrees": 0,
    },
    frozenset({"hai", "mao", "wei"}): {
        "direction": "west",
        "branches": ["shen", "you", "xu"],
        "center_degrees": 270,
    },
    frozenset({"si", "you", "chou"}): {
        "direction": "east",
        "branches": ["yin", "mao", "chen"],
        "center_degrees": 90,
    },
}


def branch_info(branch: str) -> dict[str, Any]:
    hanzi, direction, center = BRANCH_DIRECTIONS[branch]
    return {
        "branch": branch,
        "hanzi": hanzi,
        "direction": direction,
        "center_degrees": center,
    }


def opposite_branch(branch: str) -> str:
    index = BRANCH_ORDER.index(branch)
    return BRANCH_ORDER[(index + 6) % 12]


def san_sha_for_branch(branch: str) -> dict[str, Any]:
    for triad, data in SAN_SHA_BY_TRIAD.items():
        if branch in triad:
            branches = list(data["branches"])
            return {
                "direction": data["direction"],
                "branches": branches,
                "hanzi": [BRANCH_DIRECTIONS[item][0] for item in branches],
                "center_degrees": data["center_degrees"],
            }
    raise ValueError(f"unsupported branch: {branch}")


def annual_afflictions_for_year(year: int) -> dict[str, Any]:
    gz = ganzhi.ganzhi_for_year(year)
    branch = gz.branch
    return {
        "year": year,
        "ganzhi": gz.ganzhi,
        "ganzhi_hanzi": gz.ganzhi_hanzi,
        "year_branch": branch,
        "tai_sui": branch_info(branch),
        "sui_po": branch_info(opposite_branch(branch)),
        "san_sha": san_sha_for_branch(branch),
        "use_guidance": [
            "Use annual cautions as a secondary timing layer after safety, form, permits, and practical constraints.",
            "For sensitive sectors, prefer quiet, cleanliness, repair, and low-disturbance behavior before costly cures.",
            "Avoid major noisy renovation or ground-breaking in a cautioned sector unless professional and practical constraints require it.",
        ],
        "method_note": (
            "This uses a common rule: tai sui follows the year branch, sui po is opposite the year branch, "
            "and san sha is assigned by the branch trine group. Lineages may vary in details and application."
        ),
        "scope_note": (
            "This is not a full almanac, flying-star, bazi, qimen, or date-selection engine. "
            "Confirm li chun/lunar-year boundaries and candidate-date attributes for exact timing work."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Return common annual feng shui directional cautions for a Gregorian year."
    )
    parser.add_argument("year", type=int, help="Gregorian year label.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(
        json.dumps(
            annual_afflictions_for_year(args.year),
            ensure_ascii=True,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
