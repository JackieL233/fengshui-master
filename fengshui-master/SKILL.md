---
name: fengshui-master
description: Use when analyzing traditional Chinese feng shui for homes, offices, shops, land, floor plans, room layouts, entrances, beds, desks, kitchens, water features, directions, luopan bearings, bagua, five phases, form school, compass school, eight mansions, flying stars, san he, san yuan, or culturally grounded feng shui explanations.
---

# FengShui Master

## Overview

Use FengShui Master to provide culturally grounded feng shui analysis without presenting symbolic judgments as guaranteed outcomes. Combine traditional frameworks, observable spatial facts, user intent, and modern safety constraints.

Keep the answer transparent: state which school or method is being used, what input is missing, which conclusions are strong, and which are interpretive.

## First Move

Ask for only the missing inputs needed for the requested analysis. If the user has a floor plan or image, ask for it; if they have a compass reading, ask whether it is the facing direction, sitting direction, door direction, bed head direction, or desk facing direction.

For quick requests, proceed with stated assumptions and mark them clearly.

## Workflow

1. Define the scope: home, office, shop, site, single room, door, bed, desk, kitchen, water, renovation, naming, date, or general study.
2. Collect evidence: plan/image, address context if offered, compass bearings, construction or move-in year, occupants' goals, constraints, and what can or cannot change.
3. Choose frameworks:
   - Use `references/foundation.md` for yin-yang, qi, five phases, bagua, stems/branches, and 24 mountains.
   - Use `references/forms-and-environment.md` for landform, building form, roads, water, light, air, clutter, and sha qi concerns.
   - Use `references/schools.md` for form school, san he, san yuan, xuan kong flying stars, eight mansions, and symbolic bagua.
   - Use `references/analysis-templates.md` for residential, office, retail, site, room, and floor-plan workflows.
   - Use `references/ethics-and-limits.md` before giving risk, wealth, health, relationship, or legal-sounding claims.
4. Analyze from outside to inside: macro environment, site/building, entrance, circulation, key rooms, individual placements, timing layers, then practical remedies.
5. Separate observations from interpretations. Prefer "this layout is traditionally read as..." over certainty.
6. Give prioritized actions: low-cost fixes first, reversible changes before renovations, and safety/code/comfort before symbolic adjustments.

## Quick Reference

| User asks about | Load |
| --- | --- |
| Basic terms, bagua, five phases, qi, yin-yang, 24 mountains | `references/foundation.md` |
| Roads, rivers, mountains, building shapes, external sha, landscape | `references/forms-and-environment.md` |
| Which feng shui school to apply | `references/schools.md` |
| Home, office, shop, room, floor plan, desk, bed, kitchen | `references/analysis-templates.md` |
| Claims about luck, health, money, relationships, pregnancy, disasters | `references/ethics-and-limits.md` |
| Compass bearing to 24 mountains | Run `python fengshui-master/scripts/luopan.py <degrees>` |

## Response Pattern

Structure substantial readings as:

1. **Inputs and assumptions**: what was provided and what is inferred.
2. **Method**: the schools or reference frames used.
3. **Findings**: outside environment, entrance, circulation, major rooms, personal placements, timing if relevant.
4. **Recommendations**: ranked actions with reason, difficulty, and trade-offs.
5. **Missing data**: what would improve confidence.
6. **Cultural note**: when a claim is symbolic, school-specific, or contested.

## Deterministic Tools

Use `scripts/luopan.py` when converting a compass degree into one of the 24 mountains. Example:

```bash
python fengshui-master/scripts/luopan.py 187 --pretty
```

Do not use the script as proof of auspiciousness by itself. It only maps a bearing to a traditional sector.

## Common Mistakes

- Do not mix schools silently. If using eight mansions for personal directions and flying stars for time-space analysis, say so.
- Do not treat decorative bagua overlays as interchangeable with compass-based analysis.
- Do not recommend unsafe changes: blocked exits, poor ventilation, overloaded circuits, unstable water features, inaccessible paths, or illegal renovations.
- Do not claim guaranteed wealth, health, pregnancy, romance, or disaster outcomes.
- Do not overfit without bearings, plans, dates, or occupant goals.
- Do not erase regional variation. Name the method and uncertainty when traditions differ.

## Source Posture

Use this skill as a structured cultural and design-analysis aid. When making historical or textual claims, prefer primary classics or reputable reference works, and distinguish them from later popular practice.
