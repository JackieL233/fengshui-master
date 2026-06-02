# Classical Source and School Map

Use this file when extending FengShui Master, explaining where a method comes from, or deciding whether a claim should be labeled as classical, lineage-specific, modern practice, or broad symbolic adaptation.

## Source Tiers

| Tier | Use for | Output posture |
| --- | --- | --- |
| Classical anchors | Core vocabulary such as qi, yin-yang, bagua, five phases, burial qi, image thinking | Say "classical background" or "traditional vocabulary"; avoid claiming one text defines all practice |
| School and lineage methods | Form School, San He, San Yuan, Xuan Kong, Eight Mansions, luopan rings, date-selection systems | Name the school or lineage family and required inputs |
| Modern practice notes | Door-aligned bagua, popular cures, modern interior-design adaptations, cross-domain symbolism | Label as modern symbolic practice or adaptation |
| Practical constraints | Safety, law, engineering, finance, health, accessibility, climate, budget, user agency | Treat as mandatory before symbolic interpretation |

## Classical Anchors

| Anchor | Chinese | Best use in this skill | Caution |
| --- | --- | --- | --- |
| Yijing / Zhouyi | 易经 / 周易 | Yin-yang image thinking, trigrams, change, symbolic reasoning | Do not turn every feng shui judgment into a hexagram claim unless the method actually uses hexagrams |
| Hong Fan | 洪范 | Early five phases / wuxing vocabulary | Do not claim the modern five-phase cure system is directly identical to the classical passage |
| Zang Shu | 葬书 | Burial qi logic, wind-water phrasing, gathering and dispersal of qi | Mostly yin-house and historical vocabulary; do not apply burial-site rules directly to apartments |
| Luopan and later manuals | 罗盘及后世术数文献 | 24 mountains, stems/branches, directional rings, lineage formulas | Rings and formulas vary by school; state the convention used |
| Tong shu / almanac families | 通书 / 黄历体系 | Date-selection attributes, clashes, officers, solar terms, day qualities | This repository does not include a full almanac engine |

## School Map

### Form School

Core concern:

- Mountain/water image, support, embrace, openness, protection, road/water flow, sha qi, light, air, circulation.

Use for:

- Land, houses, rooms, offices, shops, roads, rivers, exterior pressure, entrances, furniture placement.

Required evidence:

- Observed form, photos, floor plan, surrounding roads/buildings/water, user goals.

Boundary:

- Strong first layer, but not a precise date-selection or personal direction formula.

### Compass School

Core concern:

- Bearing, sitting/facing, luopan sectors, bagua directions, 24 mountains.

Use for:

- Direction questions, door/bed/desk facing, sector overlays, precise compass discussion.

Required evidence:

- Clear bearing convention, measurement location, magnetic/true north if precision matters.

Boundary:

- Do not make directional claims from vague "north side" language when a formula requires degrees.

### San He

Core concern:

- Form-direction relationships, 24 mountains, branch trines, water/road approach and exit, land and yin-house context.

Use for:

- Sites, land, water mouths, roads, graves, rural or exterior-heavy analysis.

Boundary:

- Avoid detailed San He formulas without reliable luopan and environmental data.

### San Yuan

Core concern:

- Time cycles, period qi, period-building relationship, long-term timing.

Use for:

- Building period, renovation activation, current period discussion, long-term xuan kong context.

Boundary:

- Requires reliable time and facing data for precise claims.

### Xuan Kong

Core concern:

- Time-space star patterns, period, facing/sitting, nine palace grid, annual/monthly overlays.

Use for:

- Flying-star intake, annual layer, Period 9 discussion, natal chart caveats.

Boundary:

- `scripts/flying_stars.py` is a basic Luo Shu scaffold only. It is not a full natal chart, replacement-star, or lineage-specific engine.

### Eight Mansions

Core concern:

- Personal gua, favorable/unfavorable directions, bed/desk/door relationship.

Use for:

- Personal direction questions when birth year and traditional sex convention are supplied.

Boundary:

- Do not override safety, comfort, severe form problems, or user identity concerns.

### Date Selection and Moon Phase

Core concern:

- Candidate date attributes, solar terms, clashes, annual cautions, event type, and symbolic timing.

Use for:

- Moving, opening, renovation, signing, launch, public release, quiet start, New Moon, Full Moon, Moon phase, 新月, 满月, 朔, 望.

Boundary:

- `scripts/moon_phase.py` gives approximate moon phase only. Moon phase is a secondary symbolic layer, not a full almanac, tong shu, qimen, bazi, or guaranteed auspiciousness method.

## Modern cross-domain extension

FengShui Master intentionally supports modern cross-domain readings: finance, business, brand, product, career, learning, relationships, wellbeing, legal-adjacent risk, and life/omen questions.

These adapters use feng shui as a symbolic language for qi, form, flow, timing, support, leakage, balance, and ji/xiong conditions. They are useful for structured reflection and low-risk planning.

Do not present modern symbolic adapters as classical doctrine.

Correct wording:

```text
Using feng shui as a modern symbolic decision-support lens, this looks like a Water/liquidity and Metal/risk-control question.
```

Incorrect wording:

```text
Classical feng shui proves this stock will rise.
```

## Claim Labeling Rules

Use these labels in final answers when relevant:

- **Classical background**: broad vocabulary such as qi, yin-yang, wuxing, bagua.
- **School-specific method**: Form School, San He, San Yuan, Xuan Kong, Eight Mansions, date selection.
- **Lineage-dependent**: exact facing convention, annual/monthly stars, replacement stars, almanac rules, personal clashes.
- **Modern symbolic extension**: finance, product, brand, career, life pattern, relationship, negotiation, or wellbeing metaphor.
- **Practical constraint**: safety, law, finance, health, engineering, accessibility, evidence, budget, deadlines.

## Maintenance Rules

- Add new formulas only when the required inputs, lineage assumptions, and limitations are documented.
- Prefer summaries over long quotations.
- Keep classical text claims cautious unless a specific passage and translation are named.
- When a modern adapter uses old vocabulary in a new domain, label it as adaptation.
- High-stakes domains must always include their native professional boundary before symbolic reading.
