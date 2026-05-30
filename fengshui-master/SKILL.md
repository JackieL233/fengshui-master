---
name: fengshui-master
description: "Use when applying traditional Chinese feng shui and broad wuxing symbolic analysis to spaces, people, life patterns, auspiciousness, luck, decisions, finance, investing, business, brand, career, wellbeing, relationships, homes, offices, shops, land, floor plans, date selection, luopan bearings, ming gua, xuan kong flying stars, yin house, bagua, five phases, form school, compass school, eight mansions, san he, san yuan, or culturally grounded feng shui explanations."
---

# FengShui Master

## Overview

Use FengShui Master to provide culturally grounded feng shui and broad Chinese symbolic analysis without presenting symbolic judgments as guaranteed outcomes. Combine traditional frameworks, observable spatial facts, life/event context, user intent, and modern safety constraints.

Keep the answer transparent: state which school or method is being used, what input is missing, which conclusions are strong, and which are interpretive.

## First Move

Ask for only the missing inputs needed for the requested analysis. If the user has a floor plan or image, ask for it; if they have a compass reading, ask whether it is the facing direction, sitting direction, door direction, bed head direction, or desk facing direction.

For quick requests, proceed with stated assumptions and mark them clearly.

For substantial readings, cross-domain decisions, finance, life/omen questions, or structured floor-plan reviews, create a consultation brief first:

```bash
python fengshui-master/scripts/create_brief.py "<question>" --pretty
```

Load `references/consultation-brief.md` if the brief needs interpretation or adaptation.

When the user wants a reusable written deliverable, generate a Markdown report scaffold:

```bash
python fengshui-master/scripts/generate_report.py "<question>"
```

Load `references/reporting-protocol.md` before turning a scaffold into a final answer.

## Workflow

1. Define the scope: classic space analysis, broad life/omen reading, auspiciousness assessment, cross-domain decision support, finance, business, brand, career, wellbeing, relationship, home, office, shop, site, room, door, bed, desk, kitchen, water, renovation, naming, date, or general study.
2. Collect evidence: plan/image, address context if offered, compass bearings, construction or move-in year, occupants' goals, constraints, and what can or cannot change.
3. Choose frameworks:
   - Use `references/consultation-brief.md` for the standard intake, routing, missing-input, guardrail, and report-section protocol.
   - Use `references/reporting-protocol.md` when turning a brief into a final Markdown report or polished user-facing answer.
   - Use `scripts/domain_router.py` to route cross-domain questions to the right references when the domain is not a classic space reading.
   - Use `references/life-and-omen-adapter.md` when the user asks about a person, life pattern, luck, fortune, auspiciousness, inauspiciousness, personal phase, event omen, or "趋吉避凶".
   - Use `references/five-phase-domain-map.md` when translating wuxing into careers, industries, finance, brand, product, relationships, negotiation, learning, or personal patterns.
   - Use `references/domain-adapters.md` when applying feng shui to finance, business, brand, career, product, learning, wellbeing, relationships, negotiation, or other non-spatial domains.
   - Use `references/finance-adapter.md` for investment, trading, portfolio, budgeting, wealth, cash flow, business finance, market timing, or crypto questions.
   - Use `references/business-adapter.md` for business strategy, operations, customer flow, revenue, partnerships, hiring, fundraising, and organizational decisions.
   - Use `references/brand-adapter.md` for brand strategy, naming, logo, colors, tone, launch identity, campaigns, and product positioning.
   - Use `references/career-adapter.md` for career direction, promotion, interviews, leadership, negotiation, job search, and work environment support.
   - Use `references/relationship-adapter.md` for romantic, family, friendship, team, roommate, communication, shared-space, and conflict questions.
   - Use `references/floorplan-schema.md` when the user can provide structured room/site annotations or wants repeatable plan analysis.
   - Use `references/foundation.md` for yin-yang, qi, five phases, bagua, stems/branches, and 24 mountains.
   - Use `references/forms-and-environment.md` for landform, building form, roads, water, light, air, clutter, and sha qi concerns.
   - Use `references/schools.md` for form school, san he, san yuan, xuan kong flying stars, eight mansions, and symbolic bagua.
   - Use `references/analysis-templates.md` for residential, office, retail, site, room, and floor-plan workflows.
   - Use `references/remedies.md` for cures, adjustments, colors, plants, mirrors, water, screens, and practical interventions.
   - Use `references/timing-and-date-selection.md` for san yuan periods, xuan kong timing, annual layers, moving, renovation, and opening dates.
   - Use `references/xuan-kong-flying-stars.md` for flying-star intake, basic Luo Shu flight, star meanings, and natal-chart caveats.
   - Use `references/yin-house.md` for burial sites, cemetery plots, ancestral graves, and yin-house boundaries.
   - Use `references/glossary.md` for Chinese terms, translations, and quick definitions.
   - Use `references/case-patterns.md` for reusable response structures and comparison matrices.
   - Use `references/sample-readings.md` for compact examples of tone and structure.
   - Use `references/sources.md` when extending historical, classical, or lineage-specific claims.
   - Use `references/ethics-and-limits.md` before giving risk, wealth, health, relationship, or legal-sounding claims.
4. Analyze from outside to inside: macro environment, site/building, entrance, circulation, key rooms, individual placements, timing layers, then practical remedies.
5. Separate observations from interpretations. Prefer "this layout is traditionally read as..." over certainty.
6. Give prioritized actions: low-cost fixes first, reversible changes before renovations, and safety/code/comfort before symbolic adjustments.

## Quick Reference

| User asks about | Load |
| --- | --- |
| Person, life pattern, luck, fortune, omen, auspiciousness, inauspiciousness, 趋吉避凶, 吉凶, 运势, 生平 | `references/life-and-omen-adapter.md` plus `references/five-phase-domain-map.md` and `references/ethics-and-limits.md` |
| Five phases for careers, industries, finance, brand, products, relationships, personal behavior | `references/five-phase-domain-map.md` |
| Finance, investing, trading, budgeting, wealth, cash flow | `references/finance-adapter.md` plus `references/ethics-and-limits.md` |
| Business strategy, operations, customer flow, revenue, partnerships | `references/business-adapter.md` plus `references/domain-adapters.md` |
| Brand, naming, logo, colors, launch, campaign, product positioning | `references/brand-adapter.md` plus `references/five-phase-domain-map.md` |
| Career, promotion, job search, interview, negotiation, leadership | `references/career-adapter.md` plus `references/life-and-omen-adapter.md` if symbolic timing is requested |
| Relationship, family, romance, friendship, roommate, communication, conflict | `references/relationship-adapter.md` plus `references/ethics-and-limits.md` |
| Business, brand, career, product, learning, wellbeing, relationships, negotiation | `references/domain-adapters.md` |
| Substantial consultation, cross-domain question, finance/life/space brief | `references/consultation-brief.md`; run `python fengshui-master/scripts/create_brief.py "<question>"` |
| Markdown report scaffold or reusable deliverable | `references/reporting-protocol.md`; run `python fengshui-master/scripts/generate_report.py "<question>"` |
| Cross-domain routing | Run `python fengshui-master/scripts/domain_router.py "<question>"` |
| Structured floor-plan, office, shop, room, or site JSON | `references/floorplan-schema.md`; run `python fengshui-master/scripts/analyze_floorplan.py <json>` |
| Basic terms, bagua, five phases, qi, yin-yang, 24 mountains | `references/foundation.md` |
| Roads, rivers, mountains, building shapes, external sha, landscape | `references/forms-and-environment.md` |
| Which feng shui school to apply | `references/schools.md` |
| Home, office, shop, room, floor plan, desk, bed, kitchen | `references/analysis-templates.md` |
| Remedies, cures, colors, mirrors, plants, water, screens | `references/remedies.md` |
| Moving date, opening date, renovation timing, annual stars, tai sui, sui po, san sha, nine periods | `references/timing-and-date-selection.md`; run `python fengshui-master/scripts/annual_afflictions.py <year>` for common annual directional cautions |
| Xuan kong, flying stars, Period 9, Luo Shu flight, star meanings | `references/xuan-kong-flying-stars.md` |
| Yin house, burial sites, cemetery plots, ancestral graves | `references/yin-house.md` |
| Chinese terms, pronunciation, glossary, translation cautions | `references/glossary.md` |
| Example response structures, comparisons, intake templates | `references/case-patterns.md` |
| Finished answer examples and tone samples | `references/sample-readings.md` |
| Claims about luck, health, money, relationships, pregnancy, disasters | `references/ethics-and-limits.md` |
| Classical sources, research posture, adding new references | `references/sources.md` |
| Compass bearing to 24 mountains | Run `python fengshui-master/scripts/luopan.py <degrees>` |
| Birth-year ming gua / eight mansions personal directions | Run `python fengshui-master/scripts/minggua.py <year> --sex <male|female>` |
| Gregorian year to heavenly stem / earthly branch scaffold | Run `python fengshui-master/scripts/ganzhi.py <year>` |
| Annual tai sui / sui po / san sha directional cautions | Run `python fengshui-master/scripts/annual_afflictions.py <year>` |
| San yuan / xuan kong 20-year period | Run `python fengshui-master/scripts/periods.py <year>` |
| Basic Luo Shu flying-star scaffold | Run `python fengshui-master/scripts/flying_stars.py --period <1-9>` |

## Response Pattern

Structure substantial readings as:

1. **Inputs and assumptions**: what was provided and what is inferred.
2. **Method**: the schools or reference frames used.
3. **Findings**: outside environment, entrance, circulation, major rooms, personal placements, timing if relevant.
4. **Recommendations**: ranked actions with reason, difficulty, and trade-offs.
5. **Missing data**: what would improve confidence.
6. **Cultural note**: when a claim is symbolic, school-specific, or contested.

## Deterministic Tools

Use `scripts/create_brief.py` to create a structured consultation brief before substantial readings:

```bash
python fengshui-master/scripts/create_brief.py "Should I buy this stock next month using feng shui?" --pretty
```

With structured floor-plan JSON:

```bash
python fengshui-master/scripts/create_brief.py "Review this apartment layout" --floorplan fengshui-master/assets/sample-floorplan.json --pretty
```

Treat the brief as an intake contract, not the final answer.

Use `scripts/generate_report.py` to turn a consultation brief into a Markdown report scaffold:

```bash
python fengshui-master/scripts/generate_report.py "Should I buy this stock next month using feng shui?"
```

Write a sample file:

```bash
python fengshui-master/scripts/generate_report.py "Should I buy this stock next month using feng shui?" --output fengshui-master/assets/sample-finance-report.md
```

Use the generated report as a scaffold. Remove placeholder text and fill sections only with supplied evidence, transparent assumptions, and clearly labeled traditional interpretations.

Use `scripts/luopan.py` when converting a compass degree into one of the 24 mountains. Example:

```bash
python fengshui-master/scripts/luopan.py 187 --pretty
```

Do not use the script as proof of auspiciousness by itself. It only maps a bearing to a traditional sector.

Use `scripts/minggua.py` for a common eight mansions personal gua calculation:

```bash
python fengshui-master/scripts/minggua.py 1990 --sex male --pretty
```

Clarify that exact year boundaries may vary by lineage, especially around li chun.

Use `scripts/ganzhi.py` for a simple Gregorian-year heavenly stem and earthly branch scaffold:

```bash
python fengshui-master/scripts/ganzhi.py 2026 --pretty
```

Treat this as year-level symbolic context only. For birth years or annual luck near late January or early February, confirm the li chun or lunar-year boundary used by the chosen lineage. Do not present it as a complete bazi, zi wei, qimen, liuren, or almanac calculation.

Use `scripts/annual_afflictions.py` for common annual directional cautions such as tai sui, sui po, and san sha:

```bash
python fengshui-master/scripts/annual_afflictions.py 2026 --pretty
```

Treat annual cautions as a secondary timing layer for renovation, moving, opening, and disturbance questions. Do not use them as a full almanac, flying-star, bazi, qimen, or date-selection engine.

Use `scripts/periods.py` for common san yuan / xuan kong 20-year periods:

```bash
python fengshui-master/scripts/periods.py 2026 --pretty
```

Do not treat period lookup as a complete flying-star chart.

Use `scripts/flying_stars.py` for a basic Luo Shu flight scaffold:

```bash
python fengshui-master/scripts/flying_stars.py --year 2026 --pretty
```

Do not present this as a full natal flying-star chart. For complete xuan kong work, collect facing/sitting direction, period, floor plan, active rooms, and lineage assumptions.

Use `scripts/domain_router.py` when a request is not a classic space reading:

```bash
python fengshui-master/scripts/domain_router.py "Should I buy this stock next month?" --pretty
```

For finance, always use the domain's real constraints first and feng shui as a symbolic support lens only.

Use `scripts/analyze_floorplan.py` when the user provides a structured floor-plan JSON:

```bash
python fengshui-master/scripts/analyze_floorplan.py fengshui-master/assets/sample-floorplan.json --pretty
```

Treat the result as an intake and form-analysis scaffold. Continue with visual evidence, compass verification, and user constraints when needed.

## Common Mistakes

- Do not mix schools silently. If using eight mansions for personal directions and flying stars for time-space analysis, say so.
- Do not treat decorative bagua overlays as interchangeable with compass-based analysis.
- Do not recommend unsafe changes: blocked exits, poor ventilation, overloaded circuits, unstable water features, inaccessible paths, or illegal renovations.
- Do not claim guaranteed wealth, health, pregnancy, romance, or disaster outcomes.
- Do not overfit without bearings, plans, dates, or occupant goals.
- Do not erase regional variation. Name the method and uncertainty when traditions differ.
- Do not recommend a "cure" without explaining the observed issue and safer alternative.
- Do not calculate exact date auspiciousness without a calendar source or candidate-date attributes.
- Do not apply yang-house rules directly to yin-house burial sites.
- Do not present the basic flying-star helper as a full replacement-star or lineage-specific xuan kong engine.
- Do not treat cross-domain feng shui as a substitute for finance, medical, legal, engineering, tax, or other professional analysis.
- Do not present broad life, luck, omen, or auspiciousness readings as deterministic fate, complete bazi, guaranteed wealth, illness, marriage, disaster, or market prediction.

## Source Posture

Use this skill as a structured cultural and design-analysis aid. When making historical or textual claims, prefer primary classics or reputable reference works, and distinguish them from later popular practice.
