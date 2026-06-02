# Timing and Date Selection Reference

Use this file when the user asks about san yuan periods, xuan kong period timing, annual stars, moon phases, new moon, full moon, moving dates, renovation timing, opening dates, ground-breaking, or date selection. Keep claims cautious and lineage-labeled.

## Table of Contents

- Timing Layers
- San Yuan and Nine Periods
- Xuan Kong Inputs
- Annual and Monthly Layers
- Moon Phase / 新月满月
- Date Selection Scope
- Safe Timing Advice
- Tooling

## Timing Layers

Traditional timing can refer to several different things:

- **Building period**: when the building was completed, occupied, or substantially renovated.
- **Current period**: the active 20-year san yuan period in common xuan kong practice.
- **Annual/monthly stars**: time-varying symbolic influences.
- **Moon phase / 月相**: new moon / 新月 / 朔, full moon / 满月 / 望, waxing, and waning symbolic timing.
- **Annual directional cautions**: tai sui, sui po, san sha, and other lineage-specific yearly concerns.
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

### Common Annual Directional Cautions

Use `scripts/annual_afflictions.py` for common tai sui, sui po, and san sha directional cautions:

```bash
python fengshui-master/scripts/annual_afflictions.py 2026 --pretty
```

Use these cautions conservatively:

- **Tai sui** follows the year branch in many common systems.
- **Sui po** is opposite the year branch.
- **San sha** is often assigned by year-branch trine group.

Practical posture:

- Treat these as secondary to safety, form, permits, contractor constraints, and structural needs.
- Prefer quiet, cleanliness, maintenance, and reduced disturbance before costly cures.
- Do not declare a direction impossible to use for the whole year.
- Confirm li chun/lunar-year boundary conventions when the date is near year transition.

## Moon Phase / 新月满月

Moon phase is not a complete feng shui formula by itself, but it can be used as a secondary symbolic timing layer in broad feng shui, date-selection discussion, ritual planning, and cross-domain decision support.

Use the terms carefully:

- **New Moon / 新月 / 朔**: traditionally useful as a symbolic image of hidden beginning, seed intent, quiet reset, inward gathering, planning, and starting with containment.
- **Waxing Moon / 上行月相**: useful as a symbolic image of growth, accumulation, activation, and increasing visibility.
- **Full Moon / 满月 / 望**: useful as a symbolic image of illumination, visibility, culmination, public release, review, harvest, and release.
- **Waning Moon / 下行月相**: useful as a symbolic image of clearing, simplification, pruning, repair, and conserving qi.

Do not say that new moon is always lucky or full moon is always lucky/unlucky. Match the phase to the event type:

| Event type | Moon-phase posture |
| --- | --- |
| Quiet planning, intention-setting, private reset, research | New Moon / 新月 can be symbolically supportive |
| Launch preparation, gradual activation, habit building | Waxing moon can be symbolically supportive |
| Public launch, announcement, review, culmination, release | Full Moon / 满月 can be symbolically supportive if visibility is desired |
| Decluttering, ending a cycle, reducing leakage, simplifying | Waning moon can be symbolically supportive |

Required cautions:

- Moon phase is secondary to safety, law, medical needs, financial risk, weather, contractor availability, family constraints, and deadlines.
- For precise electional work, ask for candidate dates, local time zone/location, event type, and the calendar or lineage attributes the user wants to use.
- Moon phase does not replace tong shu / 通书, 24 solar terms, 12 officers, personal clashes, bazi, qimen, xuan kong, or lineage-specific date selection.

Use `scripts/moon_phase.py` for approximate phase context:

```bash
python fengshui-master/scripts/moon_phase.py 2024-04-08 --pretty
```

The tool returns approximate moon age, phase, illumination, days from new moon, days from full moon, symbolic guidance, and limitations. It is not a precise astronomy engine or full almanac.

## Date Selection Scope

Date selection can involve:

- Avoiding days that clash with a person's zodiac branch.
- Choosing days supportive of the event type.
- Considering lunar calendar, 24 solar terms, 12 officers, stars, or lineage calendars.
- Considering moon phase as a secondary symbolic layer when the user asks about 新月, 满月, 朔, 望, or lunar timing.
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

```bash
python fengshui-master/scripts/annual_afflictions.py 2026 --pretty
```

The tool returns common annual directional cautions only. It is not a full almanac or date-selection engine.

```bash
python fengshui-master/scripts/moon_phase.py 2024-04-08 --pretty
```

The tool returns approximate moon phase context only. It is useful for new moon / full moon symbolism, not full date selection.
