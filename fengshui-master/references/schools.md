# Feng Shui Schools Reference

Use this file to choose and explain a method. The goal is not to force one school to dominate, but to avoid mixing incompatible assumptions without disclosure.

## Table of Contents

- Method Selection
- Form School
- Compass School
- San He
- San Yuan
- Xuan Kong Flying Stars
- Eight Mansions
- Personal Ming Gua
- Symbolic or Door-Aligned Bagua
- Combining Methods

## Method Selection

| Situation | Prefer |
| --- | --- |
| No compass data, only photos or description | Form school and practical environment |
| Land, roads, water, external environment | Form school, san he if precise bearings exist |
| House or office with compass and build/move-in year | Form school plus xuan kong or san yuan layer |
| Personal bed/desk direction | Eight mansions if birth year/gender convention is supplied |
| Quick room adjustment without precise data | Form school, yin-yang, five phases, symbolic bagua |
| User asks about time periods, annual stars, renovation timing | Xuan kong / san yuan, with caveats |
| User asks about exact luopan sectors | 24 mountains, san he/san yuan context |

## Form School

Focus:

- Landform and environmental support.
- Mountains, water, roads, building massing.
- Four emblems: back support, front openness, left/right balance.
- Sha qi, circulation, light, air, and threshold quality.

Strength:

- Works with observation and images.
- Good first layer for almost every reading.

Limit:

- Less precise for time-based or personal direction analysis.

## Compass School

Focus:

- Directional sectors, luopan rings, trigrams, 24 mountains.
- Interaction between facing/sitting direction and formulas.

Ask:

- What bearing was measured?
- Was the reading taken outside, at the door, in the unit center, or from a map?
- Is the building's active facing different from the main door?

Limit:

- Different lineages define facing and sitting differently. State the convention used.

## San He

San he methods often emphasize landform, water, 24 mountains, stems/branches, trines, and how qi enters, gathers, and exits.

Use when:

- The user asks about land, water exits, road/water approach, graves, rural sites, or precise luopan sectors.
- There is enough environmental and compass detail to discuss form-direction relationships.

Avoid when:

- Only a small apartment interior is available and no exterior/facing data exists.

## San Yuan

San yuan methods emphasize cycles of time, space, and directional qi across periods.

Use when:

- The user asks about period timing, building completion year, move-in year, renovation activation, or long-term cycles.
- The building orientation and time data are reliable.

Limit:

- Without construction/occupation/renovation dates and reliable facing direction, avoid precise claims.

## Xuan Kong Flying Stars

Flying stars are a san yuan-related method using time period, facing/sitting direction, and a nine-grid chart.

Inputs:

- Building facing direction and sitting direction.
- Completion or major renovation period.
- Current period/year if annual/monthly layer is requested.
- Accurate floor plan with directional overlay.

Responsible output:

- Explain chart assumptions before judging.
- Treat star combinations as symbolic risk/opportunity patterns, not guaranteed outcomes.
- Prioritize form: a "good" star in a bad physical location may not help; a "bad" star in a calm unused area may be lower priority.
- Use `references/xuan-kong-flying-stars.md` before giving star meanings or chart workflow.
- Use `scripts/flying_stars.py` only for a basic Luo Shu flight scaffold, not a complete natal chart.

Current-period caution:

- If discussing current xuan kong period rules, verify dates and lineage assumptions before presenting exact period-based claims.

## Eight Mansions

Eight mansions, or ba zhai, relates personal gua numbers and house sectors/directions.

Inputs:

- Birth year.
- Gender convention used by the lineage, if relevant.
- Whether using solar year boundary around li chun or lunar new year; ask if precision matters.
- Door, bed, and desk directions.

Use for:

- Bed head direction.
- Desk facing direction.
- Personal favorable/unfavorable sectors.
- Simple home compatibility discussions.

Limit:

- Do not use eight mansions alone to override severe form issues, safety, or functional needs.

## Personal Ming Gua

Use ming gua for personal favorable and unfavorable directions in eight mansions.

Tool:

```bash
python fengshui-master/scripts/minggua.py 1990 --sex male --pretty
```

Important cautions:

- The common simple formula uses Gregorian birth year.
- Some lineages use li chun as the year boundary; ask when the birthday is near early February.
- Gua 5 is usually converted to gua 2 for male and gua 8 for female in common practice.
- Do not infer gender identity. If the user does not want a sex-based convention, explain that this particular formula requires a traditional binary convention and offer non-personal analysis instead.

## Symbolic or Door-Aligned Bagua

Some modern practices align the bagua to the entrance rather than compass north.

Use when:

- The user requests a quick symbolic room or life-area reading.
- No reliable compass data exists.
- The user explicitly follows this modern school.

Say clearly:

- This is a symbolic overlay, not the same as compass bagua.

## Combining Methods

Use this order for robust advice:

1. Safety and practical function.
2. Form school observations.
3. Compass or personal direction method if data supports it.
4. Timing method if data supports it.
5. Symbolic remedies.

When methods conflict:

- Prefer safety and form.
- Explain the conflict.
- Offer a practical compromise.
- Avoid claiming one formula cancels all others.
