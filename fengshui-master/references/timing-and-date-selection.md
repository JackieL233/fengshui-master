# Timing and Date Selection Reference

Use this file when the user asks about san yuan periods, xuan kong period timing, annual stars, moving dates, renovation timing, opening dates, ground-breaking, or date selection. Keep claims cautious and lineage-labeled.

## Table of Contents

- Timing Layers
- San Yuan and Nine Periods
- Xuan Kong Inputs
- Annual and Monthly Layers
- Date Selection Scope
- Safe Timing Advice
- Tooling

## Timing Layers

Traditional timing can refer to several different things:

- **Building period**: when the building was completed, occupied, or substantially renovated.
- **Current period**: the active 20-year san yuan period in common xuan kong practice.
- **Annual/monthly stars**: time-varying symbolic influences.
- **Personal timing**: birth data, zodiac, bazi, or personal gua.
- **Event date selection**: move-in, opening, renovation, signing, burial, wedding, or travel.

Never collapse all of these into one "lucky date" without naming the method.

## San Yuan and Nine Periods

A common modern xuan kong period sequence uses 20-year periods:

| Period | Years | Trigram | Phase |
| --- | --- | --- | --- |
| 1 | 1864-1883 | kan | water |
| 2 | 1884-1903 | kun | earth |
| 3 | 1904-1923 | zhen | wood |
| 4 | 1924-1943 | xun | wood |
| 5 | 1944-1963 | center | earth |
| 6 | 1964-1983 | qian | metal |
| 7 | 1984-2003 | dui | metal |
| 8 | 2004-2023 | gen | earth |
| 9 | 2024-2043 | li | fire |

Use `scripts/periods.py` for this mapping. Verify school-specific boundary conventions before exact flying-star charting.

## Xuan Kong Inputs

For a flying-star reading, ask for:

- Building completion year or major renovation year.
- Occupation or move-in year if the lineage uses it.
- Facing direction in degrees.
- Sitting direction if known.
- Accurate floor plan with north marked.
- Whether the user wants natal chart, annual layer, monthly layer, or renovation timing.

Do not build a precise chart from vague data. If missing, provide a method checklist rather than a judgment.

## Annual and Monthly Layers

Annual/monthly stars are often used for temporary activation or avoidance. Treat them as secondary:

1. Safety and form.
2. Building natal chart if reliable.
3. Annual/monthly layer.
4. Personal timing.

Avoid recommending disruption based only on annual stars. Prefer low-cost caution: reduce noise, avoid major disturbance, keep the sector clean, and schedule renovations with professional constraints.

## Date Selection Scope

Date selection can involve:

- Avoiding days that clash with a person's zodiac branch.
- Choosing days supportive of the event type.
- Considering lunar calendar, 24 solar terms, 12 officers, stars, or lineage calendars.
- Coordinating with construction, legal, business, and family requirements.

This skill does not include a full almanac engine. For exact date selection, state the limitation and ask the user to provide candidate dates or a trusted calendar source.

## Safe Timing Advice

Allowed:

- Explain what data is needed.
- Compare candidate dates if the user provides traditional calendar attributes.
- Suggest avoiding major noisy renovation in a sector the user's chosen school treats as sensitive.
- Remind the user to prioritize permits, contractor availability, weather, budget, and safety.

Avoid:

- Guaranteeing lucky outcomes.
- Telling users to ignore medical, legal, business, or construction deadlines.
- Creating precise almanac claims without a calendar source.

## Tooling

```bash
python fengshui-master/scripts/periods.py 2026 --pretty
```

The tool returns a common 20-year period only. It does not calculate annual stars or date auspiciousness.
