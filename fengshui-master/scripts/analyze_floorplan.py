#!/usr/bin/env python3
"""Analyze a structured FengShui Master floor-plan JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {"name", "type", "bounds", "rooms", "features"}
SUPPORTED_TYPES = {"residential", "office", "retail", "restaurant", "site", "room"}


def center_of(item: dict[str, Any]) -> tuple[float, float]:
    if "width" in item and "height" in item:
        return (float(item["x"]) + float(item["width"]) / 2, float(item["y"]) + float(item["height"]) / 2)
    return (float(item["x"]), float(item["y"]))


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def validate_plan(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_TOP_LEVEL - set(plan)
    if missing:
        errors.append(f"missing top-level fields: {', '.join(sorted(missing))}")
    if plan.get("type") not in SUPPORTED_TYPES:
        errors.append("type must be one of: " + ", ".join(sorted(SUPPORTED_TYPES)))
    bounds = plan.get("bounds", {})
    if not isinstance(bounds.get("width"), (int, float)) or not isinstance(bounds.get("height"), (int, float)):
        errors.append("bounds.width and bounds.height must be numeric")
    rooms = plan.get("rooms", [])
    if not isinstance(rooms, list) or not rooms:
        errors.append("rooms must be a non-empty list")
    features = plan.get("features", [])
    if not isinstance(features, list):
        errors.append("features must be a list")

    room_ids = {room.get("id") for room in rooms if isinstance(room, dict)}
    for room in rooms:
        for field in ["id", "type", "x", "y", "width", "height"]:
            if field not in room:
                errors.append(f"room {room.get('id', '<unknown>')} missing {field}")
    for feature in features:
        for field in ["id", "type", "x", "y"]:
            if field not in feature:
                errors.append(f"feature {feature.get('id', '<unknown>')} missing {field}")
        if "room" in feature and feature["room"] not in room_ids:
            errors.append(f"feature {feature.get('id', '<unknown>')} references missing room {feature['room']}")
    return errors


def find_features(plan: dict[str, Any], feature_type: str) -> list[dict[str, Any]]:
    return [feature for feature in plan.get("features", []) if feature.get("type") == feature_type]


def find_rooms(plan: dict[str, Any], room_type: str) -> list[dict[str, Any]]:
    return [room for room in plan.get("rooms", []) if room.get("type") == room_type]


def aligned(a: dict[str, Any], b: dict[str, Any], tolerance: float = 0.35) -> bool:
    ax, ay = center_of(a)
    bx, by = center_of(b)
    return abs(ax - bx) <= tolerance or abs(ay - by) <= tolerance


def analyze(plan: dict[str, Any]) -> dict[str, Any]:
    errors = validate_plan(plan)
    if errors:
        return {"valid": False, "errors": errors}

    issues: list[dict[str, str]] = []
    recommendations: list[dict[str, str]] = []
    findings: dict[str, list[str]] = {
        "entry": [],
        "center": [],
        "bedroom": [],
        "desk": [],
        "kitchen": [],
    }

    doors = find_features(plan, "door")
    windows = find_features(plan, "window")
    beds = find_features(plan, "bed")
    desks = find_features(plan, "desk")
    stoves = find_features(plan, "stove")
    sinks = find_features(plan, "sink")
    bathrooms = find_rooms(plan, "bathroom")

    if doors:
        findings["entry"].append("Main door is present; confirm whether it is the main qi mouth or only the unit door.")
    else:
        issues.append({"code": "missing_entry", "severity": "high", "message": "No door feature was supplied."})

    for door in doors:
        for window in windows:
            if aligned(door, window):
                issues.append(
                    {
                        "code": "front_back_alignment",
                        "severity": "medium",
                        "message": "A door and window appear aligned; traditionally this can read as qi passing through too quickly.",
                    }
                )
                recommendations.append(
                    {
                        "priority": "high",
                        "action": "Create a pause point between the aligned door and window with lighting, rug, plant, screen, or furniture that does not block circulation.",
                    }
                )
                break

    bounds = plan["bounds"]
    plan_center = (float(bounds["width"]) / 2, float(bounds["height"]) / 2)
    center_room = min(plan["rooms"], key=lambda room: distance(center_of(room), plan_center))
    findings["center"].append(f"The plan center is closest to {center_room.get('name', center_room['id'])}. Keep this area clear, stable, dry, and usable.")
    if center_room.get("type") == "bathroom":
        issues.append(
            {
                "code": "bathroom_near_center",
                "severity": "medium",
                "message": "The bathroom is closest to the plan center; prioritize ventilation, dryness, and repair.",
            }
        )

    if beds:
        findings["bedroom"].append("Bed feature supplied; review door line, backing, mirror, beam, and head direction before symbolic remedies.")
        recommendations.append(
            {
                "priority": "medium",
                "action": "For the bed, prefer solid head support and a view of the door without direct door-line exposure.",
            }
        )
    if desks:
        findings["desk"].append("Desk feature supplied; command position and back support should outrank personal direction if they conflict.")
    if stoves:
        findings["kitchen"].append("Stove feature supplied; check ventilation, workflow, and water-fire relationship.")
    if stoves and sinks:
        for stove in stoves:
            for sink in sinks:
                if stove.get("room") == sink.get("room") and distance(center_of(stove), center_of(sink)) < 1.5:
                    issues.append(
                        {
                            "code": "stove_sink_close",
                            "severity": "low",
                            "message": "Stove and sink are close; some traditions read this as fire-water tension.",
                        }
                    )
                    recommendations.append(
                        {
                            "priority": "low",
                            "action": "Improve kitchen workflow and consider a practical wood/earth bridge such as a prep surface, mat, or neutral material between stove and sink.",
                        }
                    )
                    break

    if bathrooms:
        recommendations.append(
            {
                "priority": "medium",
                "action": "For bathrooms, prioritize ventilation, dry surfaces, working drains, and a door that closes properly.",
            }
        )

    if not recommendations:
        recommendations.append(
            {
                "priority": "medium",
                "action": "Provide photos, north arrow, and more feature annotations for a deeper reading.",
            }
        )

    return {
        "valid": True,
        "input": {
            "name": plan["name"],
            "type": plan["type"],
            "facing_degrees": plan.get("facing_degrees"),
            "north_degrees": plan.get("north_degrees"),
        },
        "findings": findings,
        "issues": issues,
        "recommendations": recommendations,
        "method_note": "This is a structured intake and form-analysis scaffold. It does not replace visual review, compass verification, or lineage-specific formulas.",
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
