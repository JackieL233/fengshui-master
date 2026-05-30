# Xuan Kong Flying Stars Reference

Use this file when the user asks about xuan kong, flying stars, period charts, natal charts, annual stars, star combinations, facing/sitting, or time-space feng shui.

## Table of Contents

- Scope
- Required Inputs
- Basic Luo Shu Flight
- Natal Chart Caution
- Star Meanings
- Reading Order
- Responsible Output
- Tooling

## Scope

This reference supports responsible xuan kong discussion and basic Luo Shu flight. It does not claim to implement every lineage rule.

Covered:

- Common 20-year periods.
- Basic forward/reverse Luo Shu flight.
- Intake requirements for natal charts.
- Responsible interpretation of star combinations.

Not fully covered:

- Replacement stars / ti gua.
- Complex兼向 and line-specific rules.
- Full mountain star and facing star derivation across all lineages.
- Annual/monthly star engines.
- Date selection almanac logic.

## Required Inputs

Ask for:

- Building completion year or major renovation year.
- Move-in year if the user's lineage uses occupation timing.
- Facing direction in degrees.
- Sitting direction or opposite direction.
- Reliable floor plan with north arrow.
- Main door, bedroom, kitchen, office, and active water locations.
- Whether the user wants natal chart, annual chart, renovation timing, or general explanation.

If these are missing, give an intake checklist rather than a confident chart.

## Basic Luo Shu Flight

The Luo Shu flight path used by the helper is:

```text
center -> northwest -> west -> northeast -> south -> north -> southwest -> east -> southeast
```

Forward flight increments star numbers by one; reverse flight decrements by one. Star numbers wrap 1-9.

Use the helper only for the basic grid:

```bash
python fengshui-master/scripts/flying_stars.py --period 9 --pretty
python fengshui-master/scripts/flying_stars.py --year 2026 --direction reverse --pretty
```

## Natal Chart Caution

A full xuan kong natal chart usually needs:

- Period star at center.
- Facing star and mountain star.
- Direction-dependent flight.
- A lineage rule for determining flight direction.
- Replacement-star handling in some cases.

Do not present the basic helper output as a full natal chart. It is a scaffold for explanation and early intake.

## Star Meanings

Keep meanings short and context-dependent.

| Star | Common image | Phase | Interpretive notes |
| --- | --- | --- | --- |
| 1 | water/kan | water | learning, communication, movement, career symbolism |
| 2 | kun | earth | illness symbolism in many modern readings; also mother/earth |
| 3 | zhen | wood | disputes, growth, agitation, action |
| 4 | xun | wood | study, romance, arts, writing |
| 5 | center | earth | instability or obstruction in many modern readings |
| 6 | qian | metal | authority, leadership, discipline |
| 7 | dui | metal | speech, loss, cutting, exchange |
| 8 | gen | earth | stability, property, support; period-specific prosperity in Period 8 readings |
| 9 | li | fire | visibility, future prosperity, celebration; especially emphasized in Period 9 |

These meanings shift by period, form, room use, star pairing, and lineage.

## Reading Order

1. Confirm data quality.
2. Check form and safety first.
3. Establish period and facing/sitting convention.
4. Build chart or explain why not enough data exists.
5. Overlay chart on the plan.
6. Prioritize active areas: main door, bedroom, kitchen, desk, water, stairs, noisy renovation zones.
7. Treat star combinations as symbolic tendencies, not guarantees.
8. Recommend practical, reversible remedies.

## Responsible Output

Say:

- "This is a basic Luo Shu flight scaffold, not a complete natal chart."
- "This interpretation depends on the facing and period assumptions."
- "The physical form may outweigh the star reading."

Avoid:

- "This sector will cause illness."
- "This star guarantees wealth."
- "Period 9 makes all south-facing properties good."

## Tooling

Use:

```bash
python fengshui-master/scripts/periods.py 2026 --pretty
python fengshui-master/scripts/flying_stars.py --year 2026 --pretty
```

The period helper identifies the common 20-year cycle. The flying-star helper produces only the basic Luo Shu flight.
