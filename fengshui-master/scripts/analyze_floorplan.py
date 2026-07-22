#!/usr/bin/env python3
"""Analyze a validated, structured FengShui Master floor-plan JSON file."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {"name", "type", "bounds", "rooms", "features"}
SUPPORTED_TYPES = {"residential", "office", "retail", "restaurant", "site", "room"}
ANALYZED_FEATURE_TYPES = {"door", "window", "bed", "desk", "stove", "sink"}
KNOWN_UNANALYZED_FEATURE_TYPES = {
    "toilet",
    "bath",
    "mirror",
    "stair",
    "elevator",
    "water",
    "plant",
    "sofa",
    "cashier",
    "altar",
    "road",
    "path",
    "tree",
    "pole",
    "corner",
}
DEFAULT_TOLERANCES = {
    "meters": {"alignment": 0.35, "stove_sink": 1.5},
    "feet": {"alignment": 1.15, "stove_sink": 5.0},
}
BEARING_FIELDS = {"facing_degrees", "north_degrees", "head_degrees"}


def is_finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def center_of(item: dict[str, Any]) -> tuple[float, float]:
    if "width" in item and "height" in item:
        return (
            float(item["x"]) + float(item["width"]) / 2,
            float(item["y"]) + float(item["height"]) / 2,
        )
    return (float(item["x"]), float(item["y"]))


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def point_in_rectangle(point: tuple[float, float], rectangle: dict[str, Any]) -> bool:
    x, y = point
    return (
        float(rectangle["x"]) <= x <= float(rectangle["x"]) + float(rectangle["width"])
        and float(rectangle["y"]) <= y <= float(rectangle["y"]) + float(rectangle["height"])
    )


def validate_bearing(errors: list[str], owner: str, field: str, value: Any) -> None:
    if not is_finite_number(value) or not 0 <= float(value) < 360:
        errors.append(f"{owner}.{field} must be a finite bearing from 0 (inclusive) to 360 (exclusive)")


def validate_rectangle(
    errors: list[str],
    owner: str,
    item: dict[str, Any],
    bounds_width: float | None,
    bounds_height: float | None,
) -> None:
    for field in ["x", "y", "width", "height"]:
        if not is_finite_number(item.get(field)):
            errors.append(f"{owner}.{field} must be a finite number")
    if not all(is_finite_number(item.get(field)) for field in ["x", "y", "width", "height"]):
        return
    x = float(item["x"])
    y = float(item["y"])
    width = float(item["width"])
    height = float(item["height"])
    if width <= 0 or height <= 0:
        errors.append(f"{owner}.width and {owner}.height must be positive")
    if x < 0 or y < 0:
        errors.append(f"{owner} coordinates must be within plan bounds")
    if bounds_width is not None and bounds_height is not None:
        if x + width > bounds_width or y + height > bounds_height:
            errors.append(f"{owner} extends outside plan bounds")


def validate_point(
    errors: list[str],
    owner: str,
    item: dict[str, Any],
    bounds_width: float | None,
    bounds_height: float | None,
) -> None:
    for field in ["x", "y"]:
        if not is_finite_number(item.get(field)):
            errors.append(f"{owner}.{field} must be a finite number")
    if not all(is_finite_number(item.get(field)) for field in ["x", "y"]):
        return
    x = float(item["x"])
    y = float(item["y"])
    if x < 0 or y < 0:
        errors.append(f"{owner} coordinates must be within plan bounds")
    if bounds_width is not None and bounds_height is not None:
        if x > bounds_width or y > bounds_height:
            errors.append(f"{owner} lies outside plan bounds")


def validate_plan(plan: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["plan must be a JSON object"]

    missing = REQUIRED_TOP_LEVEL - set(plan)
    if missing:
        errors.append(f"missing top-level fields: {', '.join(sorted(missing))}")
    if not isinstance(plan.get("name"), str) or not plan.get("name", "").strip():
        errors.append("name must be a non-empty string")
    if plan.get("type") not in SUPPORTED_TYPES:
        errors.append("type must be one of: " + ", ".join(sorted(SUPPORTED_TYPES)))

    bounds = plan.get("bounds")
    bounds_width: float | None = None
    bounds_height: float | None = None
    if not isinstance(bounds, dict):
        errors.append("bounds must be an object")
    else:
        if not is_finite_number(bounds.get("width")) or not is_finite_number(bounds.get("height")):
            errors.append("bounds.width and bounds.height must be finite numbers")
        elif float(bounds["width"]) <= 0 or float(bounds["height"]) <= 0:
            errors.append("bounds.width and bounds.height must be positive")
        else:
            bounds_width = float(bounds["width"])
            bounds_height = float(bounds["height"])

    for field in ["facing_degrees", "north_degrees"]:
        if field in plan:
            validate_bearing(errors, "plan", field, plan[field])

    units = plan.get("units")
    if units is not None and (not isinstance(units, str) or not units.strip()):
        errors.append("units must be a non-empty string when supplied")
    tolerances = plan.get("analysis_tolerances")
    if tolerances is not None:
        if not isinstance(tolerances, dict):
            errors.append("analysis_tolerances must be an object")
        else:
            for field in ["alignment", "stove_sink"]:
                if field in tolerances and (
                    not is_finite_number(tolerances[field]) or float(tolerances[field]) <= 0
                ):
                    errors.append(f"analysis_tolerances.{field} must be a positive finite number")

    rooms = plan.get("rooms", [])
    if not isinstance(rooms, list) or not rooms:
        errors.append("rooms must be a non-empty list")
        rooms = []
    features = plan.get("features", [])
    if not isinstance(features, list):
        errors.append("features must be a list")
        features = []

    room_ids: set[str] = set()
    for index, room in enumerate(rooms):
        owner = f"room[{index}]"
        if not isinstance(room, dict):
            errors.append(f"{owner} must be an object")
            continue
        room_id = room.get("id")
        if not isinstance(room_id, str) or not room_id.strip():
            errors.append(f"{owner}.id must be a non-empty string")
        elif room_id in room_ids:
            errors.append(f"duplicate room id: {room_id}")
        else:
            room_ids.add(room_id)
        if not isinstance(room.get("type"), str) or not room.get("type", "").strip():
            errors.append(f"{owner}.type must be a non-empty string")
        validate_rectangle(errors, owner, room, bounds_width, bounds_height)

    feature_ids: set[str] = set()
    main_entrance_count = 0
    for index, feature in enumerate(features):
        owner = f"feature[{index}]"
        if not isinstance(feature, dict):
            errors.append(f"{owner} must be an object")
            continue
        feature_id = feature.get("id")
        if not isinstance(feature_id, str) or not feature_id.strip():
            errors.append(f"{owner}.id must be a non-empty string")
        elif feature_id in feature_ids:
            errors.append(f"duplicate feature id: {feature_id}")
        else:
            feature_ids.add(feature_id)
        if not isinstance(feature.get("type"), str) or not feature.get("type", "").strip():
            errors.append(f"{owner}.type must be a non-empty string")
        validate_point(errors, owner, feature, bounds_width, bounds_height)
        if "width" in feature or "height" in feature:
            validate_rectangle(errors, owner, feature, bounds_width, bounds_height)
        if "room" in feature and feature["room"] not in room_ids:
            errors.append(f"{owner} references missing room {feature['room']}")
        for field in BEARING_FIELDS:
            if field in feature:
                validate_bearing(errors, owner, field, feature[field])
        if feature.get("type") == "door":
            if feature.get("role") not in {"main_entrance", "interior"}:
                errors.append(f"{owner}.role must be main_entrance or interior for door features")
            elif feature["role"] == "main_entrance":
                main_entrance_count += 1
        if feature.get("type") == "window" and "role" in feature:
            if feature["role"] not in {"rear_exterior", "exterior", "interior"}:
                errors.append(
                    f"{owner}.role must be rear_exterior, exterior, or interior for window features"
                )

    if main_entrance_count > 1:
        errors.append("only one door may have role main_entrance in this analyzer")
    return errors


def find_features(plan: dict[str, Any], feature_type: str) -> list[dict[str, Any]]:
    return [
        feature
        for feature in plan.get("features", [])
        if isinstance(feature, dict) and feature.get("type") == feature_type
    ]


def find_rooms(plan: dict[str, Any], room_type: str) -> list[dict[str, Any]]:
    return [
        room
        for room in plan.get("rooms", [])
        if isinstance(room, dict) and room.get("type") == room_type
    ]


def analysis_tolerances(plan: dict[str, Any]) -> tuple[dict[str, float], str]:
    explicit = plan.get("analysis_tolerances", {})
    if isinstance(explicit, dict) and all(
        is_finite_number(explicit.get(field)) and float(explicit[field]) > 0
        for field in ["alignment", "stove_sink"]
    ):
        return (
            {field: float(explicit[field]) for field in ["alignment", "stove_sink"]},
            "explicit",
        )
    units = str(plan.get("units", "")).casefold()
    if units in DEFAULT_TOLERANCES:
        return dict(DEFAULT_TOLERANCES[units]), f"default_{units}"
    return {}, "unavailable"


def aligned(a: dict[str, Any], b: dict[str, Any], tolerance: float) -> bool:
    ax, ay = center_of(a)
    bx, by = center_of(b)
    return abs(ax - bx) <= tolerance or abs(ay - by) <= tolerance


def analyze(plan: Any) -> dict[str, Any]:
    errors = validate_plan(plan)
    if errors:
        return {"valid": False, "errors": errors}

    assert isinstance(plan, dict)
    issues: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []
    not_assessed: list[dict[str, Any]] = []
    findings: dict[str, list[str]] = {
        "entry": [],
        "center": [],
        "bedroom": [],
        "desk": [],
        "kitchen": [],
    }

    doors = find_features(plan, "door")
    main_entrances = [door for door in doors if door.get("role") == "main_entrance"]
    windows = find_features(plan, "window")
    rear_openings = [window for window in windows if window.get("role") == "rear_exterior"]
    beds = find_features(plan, "bed")
    desks = find_features(plan, "desk")
    stoves = find_features(plan, "stove")
    sinks = find_features(plan, "sink")
    bathrooms = find_rooms(plan, "bathroom")
    tolerances, tolerance_source = analysis_tolerances(plan)

    if main_entrances:
        findings["entry"].append(
            f"Main entrance {main_entrances[0]['id']} is explicitly identified as the qi-mouth candidate."
        )
    else:
        issues.append(
            {
                "code": "main_entrance_not_identified",
                "severity": "high",
                "source_ids": [door["id"] for door in doors],
                "message": "No door is explicitly marked role=main_entrance.",
                "verification": "Confirm which supplied door is the primary exterior entrance.",
            }
        )
        not_assessed.append(
            {
                "code": "entry_alignment_not_assessed",
                "reason": "main entrance is not identified",
                "required_inputs": ["one door with role=main_entrance"],
            }
        )

    if main_entrances and rear_openings and "alignment" in tolerances:
        entrance = main_entrances[0]
        for window in rear_openings:
            if aligned(entrance, window, tolerances["alignment"]):
                source_ids = [entrance["id"], window["id"]]
                issues.append(
                    {
                        "code": "front_back_alignment",
                        "severity": "medium",
                        "source_ids": source_ids,
                        "message": "The explicitly identified main entrance and a window are axis-aligned within the configured tolerance; some traditions read this as flow passing through too quickly.",
                        "verification": "Verify the opening geometry, sightline, normal circulation, and whether both openings are used simultaneously.",
                    }
                )
                recommendations.append(
                    {
                        "priority": "high",
                        "issue_code": "front_back_alignment",
                        "source_ids": source_ids,
                        "action": "Create a visual or circulation pause only if it preserves a clear, accessible egress route.",
                        "constraints": [
                            "do not narrow required egress or accessible circulation",
                            "do not block doors, windows, ventilation, sprinklers, or emergency equipment",
                        ],
                        "verification": "Re-check clear widths, door swing, ventilation, daylight, and the actual walking path after any change.",
                    }
                )
                break
    elif main_entrances and rear_openings:
        not_assessed.append(
            {
                "code": "entry_alignment_not_assessed",
                "reason": "units do not have a safe default alignment tolerance",
                "required_inputs": ["units=meters or units=feet", "or explicit analysis_tolerances.alignment"],
            }
        )
    elif main_entrances and windows:
        not_assessed.append(
            {
                "code": "entry_alignment_not_assessed",
                "reason": "no window is explicitly marked role=rear_exterior",
                "source_ids": [window["id"] for window in windows],
                "required_inputs": ["window role and verified exterior opening path"],
            }
        )

    bounds = plan["bounds"]
    plan_center = (float(bounds["width"]) / 2, float(bounds["height"]) / 2)
    center_rooms = [room for room in plan["rooms"] if point_in_rectangle(plan_center, room)]
    if center_rooms:
        room_names = [room.get("name", room["id"]) for room in center_rooms]
        findings["center"].append(
            f"The geometric plan center falls within: {', '.join(room_names)}. Keep the actual center area clear, stable, dry, and usable."
        )
        for room in center_rooms:
            if room.get("type") == "bathroom":
                issues.append(
                    {
                        "code": "bathroom_at_center",
                        "severity": "medium",
                        "source_ids": [room["id"]],
                        "message": "A bathroom annotation contains the geometric plan center; prioritize ventilation, dryness, drainage, and repair.",
                        "verification": "Confirm the usable building outline and center calculation rather than the drawing canvas alone.",
                    }
                )
    else:
        not_assessed.append(
            {
                "code": "center_room_not_assessed",
                "reason": "the geometric plan center falls in an unannotated gap",
                "required_inputs": ["complete room or zone coverage", "confirmation of the usable building outline"],
            }
        )

    if beds:
        findings["bedroom"].append(
            "Bed feature supplied; review door line, backing, mirror, beam, and head direction before symbolic remedies."
        )
        recommendations.append(
            {
                "priority": "medium",
                "issue_code": "bed_position_review",
                "source_ids": [bed["id"] for bed in beds],
                "action": "Prefer solid head support and a view of the door without direct door-line exposure when comfort and access allow.",
                "constraints": ["preserve accessible circulation", "do not obstruct exits, windows, heating, or ventilation"],
                "verification": "Confirm comfort, door swing, walking clearance, and sleep conditions after repositioning.",
            }
        )
    if desks:
        findings["desk"].append(
            "Desk feature supplied; command position and back support should outrank personal direction if they conflict."
        )
    if stoves:
        findings["kitchen"].append(
            "Stove feature supplied; check ventilation, workflow, fire safety, and water-fire symbolism in that order."
        )
    if stoves and sinks and "stove_sink" in tolerances:
        for stove in stoves:
            for sink in sinks:
                if (
                    stove.get("room") == sink.get("room")
                    and distance(center_of(stove), center_of(sink)) < tolerances["stove_sink"]
                ):
                    source_ids = [stove["id"], sink["id"]]
                    issues.append(
                        {
                            "code": "stove_sink_close",
                            "severity": "low",
                            "source_ids": source_ids,
                            "message": "Stove and sink are close within the configured unit-aware threshold; some traditions read this as fire-water tension.",
                            "verification": "Measure edge-to-edge clearance and review the actual prep workflow, heat, splash, electrical, and fire-safety conditions.",
                        }
                    )
                    recommendations.append(
                        {
                            "priority": "low",
                            "issue_code": "stove_sink_close",
                            "source_ids": source_ids,
                            "action": "Improve practical prep separation first; treat any material or color bridge as secondary symbolism.",
                            "constraints": ["follow fire, electrical, plumbing, hygiene, and appliance-clearance requirements"],
                            "verification": "Confirm safe clearances and a dry, unobstructed workflow with a qualified professional where required.",
                        }
                    )
                    break
    elif stoves and sinks:
        not_assessed.append(
            {
                "code": "stove_sink_proximity_not_assessed",
                "reason": "units do not have a safe default proximity threshold",
                "required_inputs": ["units=meters or units=feet", "or explicit analysis_tolerances.stove_sink"],
            }
        )

    if bathrooms:
        recommendations.append(
            {
                "priority": "medium",
                "issue_code": "bathroom_maintenance",
                "source_ids": [room["id"] for room in bathrooms],
                "action": "Prioritize ventilation, dry surfaces, working drains, leak repair, and doors that operate safely.",
                "constraints": ["do not disable ventilation or alter plumbing without qualified review"],
                "verification": "Check moisture, odor, drainage, leaks, and ventilation under normal use.",
            }
        )

    for feature in plan["features"]:
        if feature["type"] not in ANALYZED_FEATURE_TYPES:
            not_assessed.append(
                {
                    "code": "feature_type_not_assessed",
                    "source_ids": [feature["id"]],
                    "reason": (
                        "recognized feature type is not evaluated by this helper"
                        if feature["type"] in KNOWN_UNANALYZED_FEATURE_TYPES
                        else "custom feature type has no bundled analysis rule"
                    ),
                    "required_inputs": ["manual visual and domain-specific review"],
                }
            )

    if not recommendations:
        recommendations.append(
            {
                "priority": "medium",
                "issue_code": "deeper_review",
                "source_ids": [],
                "action": "Provide photos, a verified north arrow, and relevant feature annotations for a deeper reading.",
                "constraints": ["protect privacy and remove unnecessary personal information"],
                "verification": "Confirm that images, bearings, units, and annotations describe the same plan version.",
            }
        )

    return {
        "valid": True,
        "input": {
            "name": plan["name"],
            "type": plan["type"],
            "units": plan.get("units"),
            "facing_degrees": plan.get("facing_degrees"),
            "north_degrees": plan.get("north_degrees"),
        },
        "analysis_metadata": {
            "tolerances": tolerances,
            "tolerance_source": tolerance_source,
            "main_entrance_id": main_entrances[0]["id"] if main_entrances else None,
        },
        "findings": findings,
        "issues": issues,
        "recommendations": recommendations,
        "not_assessed": not_assessed,
        "method_note": "This is a validated structured-intake and limited form-analysis scaffold. It does not replace visual review, code and accessibility review, compass verification, or lineage-specific formulas.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a FengShui Master floor-plan JSON file.")
    parser.add_argument("path", help="Path to floor-plan JSON.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    plan = json.loads(Path(args.path).read_text(encoding="utf-8"))
    result = analyze(plan)
    print(json.dumps(result, ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
