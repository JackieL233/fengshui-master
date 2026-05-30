#!/usr/bin/env python3
"""Calculate a simple Eight Mansions personal ming gua number."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


DIRECTIONS = {
    1: {
        "trigram": "kan",
        "hanzi": "坎",
        "group": "east",
        "element": "water",
        "sheng_qi": "southeast",
        "tian_yi": "east",
        "yan_nian": "south",
        "fu_wei": "north",
        "jue_ming": "southwest",
        "wu_gui": "northeast",
        "liu_sha": "northwest",
        "huo_hai": "west",
    },
    2: {
        "trigram": "kun",
        "hanzi": "坤",
        "group": "west",
        "element": "earth",
        "sheng_qi": "northeast",
        "tian_yi": "west",
        "yan_nian": "northwest",
        "fu_wei": "southwest",
        "jue_ming": "north",
        "wu_gui": "southeast",
        "liu_sha": "south",
        "huo_hai": "east",
    },
    3: {
        "trigram": "zhen",
        "hanzi": "震",
        "group": "east",
        "element": "wood",
        "sheng_qi": "south",
        "tian_yi": "north",
        "yan_nian": "southeast",
        "fu_wei": "east",
        "jue_ming": "west",
        "wu_gui": "northwest",
        "liu_sha": "northeast",
        "huo_hai": "southwest",
    },
    4: {
        "trigram": "xun",
        "hanzi": "巽",
        "group": "east",
        "element": "wood",
        "sheng_qi": "north",
        "tian_yi": "south",
        "yan_nian": "east",
        "fu_wei": "southeast",
        "jue_ming": "northeast",
        "wu_gui": "southwest",
        "liu_sha": "west",
        "huo_hai": "northwest",
    },
    6: {
        "trigram": "qian",
        "hanzi": "乾",
        "group": "west",
        "element": "metal",
        "sheng_qi": "west",
        "tian_yi": "northeast",
        "yan_nian": "southwest",
        "fu_wei": "northwest",
        "jue_ming": "south",
        "wu_gui": "east",
        "liu_sha": "north",
        "huo_hai": "southeast",
    },
    7: {
        "trigram": "dui",
        "hanzi": "兑",
        "group": "west",
        "element": "metal",
        "sheng_qi": "northwest",
        "tian_yi": "southwest",
        "yan_nian": "northeast",
        "fu_wei": "west",
        "jue_ming": "east",
        "wu_gui": "south",
        "liu_sha": "southeast",
        "huo_hai": "north",
    },
    8: {
        "trigram": "gen",
        "hanzi": "艮",
        "group": "west",
        "element": "earth",
        "sheng_qi": "southwest",
        "tian_yi": "northwest",
        "yan_nian": "west",
        "fu_wei": "northeast",
        "jue_ming": "southeast",
        "wu_gui": "north",
        "liu_sha": "east",
        "huo_hai": "south",
    },
    9: {
        "trigram": "li",
        "hanzi": "离",
        "group": "east",
        "element": "fire",
        "sheng_qi": "east",
        "tian_yi": "southeast",
        "yan_nian": "north",
        "fu_wei": "south",
        "jue_ming": "northwest",
        "wu_gui": "west",
        "liu_sha": "southwest",
        "huo_hai": "northeast",
    },
}

EAST_GROUP = {1, 3, 4, 9}
WEST_GROUP = {2, 6, 7, 8}


@dataclass(frozen=True)
class MingGuaResult:
    year: int
    sex: str
    gua_number: int
    trigram: str
    hanzi: str
    group: str
    element: str
    directions: dict[str, str]
    note: str


def digital_root(number: int) -> int:
    while number > 9:
        number = sum(int(digit) for digit in str(number))
    return number


def ming_gua(year: int, sex: str) -> MingGuaResult:
    if year < 1900 or year > 2099:
        raise ValueError("supported range is 1900-2099")

    root = digital_root(year % 100)
    if year < 2000:
        raw = 10 - root if sex == "male" else 5 + root
    else:
        raw = 9 - root if sex == "male" else 6 + root

    gua = digital_root(raw)
    if gua == 0:
        gua = 9
    if gua == 5:
        gua = 2 if sex == "male" else 8

    info = DIRECTIONS[gua]
    directions = {
        "sheng_qi": info["sheng_qi"],
        "tian_yi": info["tian_yi"],
        "yan_nian": info["yan_nian"],
        "fu_wei": info["fu_wei"],
        "jue_ming": info["jue_ming"],
        "wu_gui": info["wu_gui"],
        "liu_sha": info["liu_sha"],
        "huo_hai": info["huo_hai"],
    }
    return MingGuaResult(
        year=year,
        sex=sex,
        gua_number=gua,
        trigram=info["trigram"],
        hanzi=info["hanzi"],
        group=info["group"],
        element=info["element"],
        directions=directions,
        note="Uses a common Eight Mansions formula by Gregorian birth year; adjust for li chun or lineage-specific year boundary if precision matters.",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate a common Eight Mansions personal ming gua number."
    )
    parser.add_argument("year", type=int, help="Gregorian birth year, 1900-2099.")
    parser.add_argument("--sex", choices=["male", "female"], required=True)
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    try:
        data = asdict(ming_gua(args.year, args.sex))
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(data, ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
