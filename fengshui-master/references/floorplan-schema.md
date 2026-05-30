# Floor Plan and Site Schema

Use this file when the user provides a floor plan, room layout, shop plan, office plan, land parcel, cemetery plot, or annotated map and wants a structured feng shui analysis.

## Table of Contents

- Purpose
- JSON Shape
- Coordinate Convention
- Required Fields
- Feature Types
- Analysis Workflow
- Example
- Tooling

## Purpose

Natural-language descriptions are useful but inconsistent. A structured JSON annotation lets FengShui Master:

- Detect missing inputs.
- Identify doors, windows, beds, desks, stove, sink, bathroom, stairs, water, roads, and open areas.
- Produce repeatable intake findings.
- Separate geometric observations from symbolic interpretation.
- Support future image/GIS/manual annotation workflows.

## JSON Shape

Top-level fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Human-readable plan name |
| `type` | yes | `residential`, `office`, `retail`, `restaurant`, `site`, or `room` |
| `facing_degrees` | optional | Building/unit/shop/site facing direction |
| `north_degrees` | optional | North direction in the coordinate system |
| `units` | optional | `meters`, `feet`, `pixels`, or other stated unit |
| `bounds` | yes | Overall width and height |
| `rooms` | yes | Rectangular room or zone annotations |
| `features` | yes | Doors, windows, furniture, fixtures, roads, water, etc. |
| `notes` | optional | Assumptions and caveats |

## Coordinate Convention

Use a simple 2D coordinate plane:

- `x`: distance from left edge.
- `y`: distance from front/top edge in the provided drawing convention.
- `width` and `height`: rectangle size for rooms/zones.
- Features can use point coordinates.
- Compass bearings are degrees where 0 is north, 90 east, 180 south, 270 west.

If the plan image has a different orientation, state it in `north_degrees` and notes.

## Required Fields

Room object:

```json
{
  "id": "bedroom",
  "type": "bedroom",
  "name": "Bedroom",
  "x": 0,
  "y": 4.4,
  "width": 4.8,
  "height": 3.6
}
```

Feature object:

```json
{
  "id": "front-door",
  "type": "door",
  "room": "entry",
  "x": 5,
  "y": 0,
  "facing_degrees": 180
}
```

## Feature Types

Common features:

- `door`
- `window`
- `bed`
- `desk`
- `stove`
- `sink`
- `toilet`
- `bath`
- `mirror`
- `stair`
- `elevator`
- `water`
- `plant`
- `sofa`
- `cashier`
- `altar`
- `road`
- `path`
- `tree`
- `pole`
- `corner`

Use additional feature types when needed, but explain them in `notes`.

## Analysis Workflow

1. Validate the JSON shape.
2. Identify plan type and facing/north data.
3. Find main entrance and first-view path.
4. Check front-back door/window alignment.
5. Locate center and the room closest to center.
6. Check key placements: bed, desk, stove, bathroom, stairs, water.
7. Produce findings, issues, and prioritized recommendations.
8. State missing data for deeper compass, flying-star, or lineage analysis.

## Example

See `assets/sample-floorplan.json`.

## Tooling

Run:

```bash
python fengshui-master/scripts/analyze_floorplan.py fengshui-master/assets/sample-floorplan.json --pretty
```

The analyzer is a structured intake and form-analysis scaffold. It does not replace human visual review, exact compass work, or lineage-specific formulas.
