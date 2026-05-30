# FengShui Master

FengShui Master is an open Codex skill for traditional Chinese feng shui analysis. It provides structured workflows, reference material, deterministic helpers, and a JSON floor-plan intake format for analyzing homes, offices, shops, rooms, land, floor plans, entrances, beds, desks, kitchens, directions, timing, xuan kong scaffolds, environmental form, and cross-domain decisions such as finance, business, brand, career, product, learning, and wellbeing.

The project treats feng shui as a traditional cultural and spatial-analysis system. It does not present symbolic readings as guaranteed predictions.

## What This Skill Covers

- Foundational concepts: qi, yin-yang, five phases, bagua, stems/branches, 24 mountains.
- Form analysis: landform, roads, water, buildings, entrances, circulation, sha qi, light, air, clutter.
- School selection: form school, compass school, san he, san yuan, xuan kong flying stars, eight mansions, symbolic bagua.
- Scenario workflows: residential, office, retail, restaurant, site selection, bedroom, desk, floor plan, renovation.
- Remedies and adjustments: mirrors, plants, screens, water, color, five-phase balancing, safe intervention ladder.
- Timing: san yuan periods, xuan kong inputs, annual/monthly layer cautions, date-selection intake.
- Xuan Kong Flying Stars: basic Luo Shu flight scaffold, star meanings, period cautions, natal-chart intake.
- Yin house boundaries: cemetery and burial-site intake, conservative form reading, ethics and safety.
- Cross-domain adapters: finance, business, brand, career, product, learning, wellbeing, relationships, and negotiation.
- Finance adapter: symbolic feng shui lens for investing, portfolio, budget, cash flow, and market-timing questions with strong financial guardrails.
- Structured floor-plan input: JSON schema, sample plan, and analyzer for repeatable room/site intake.
- Glossary and case patterns: Chinese terminology, response templates, comparison matrices.
- Safety and ethics: high-stakes claims, cultural respect, modern building constraints.
- Tooling: compass bearing to 24-mountain conversion, ming gua lookup, san yuan period lookup, basic flying-star scaffold.

## Coverage Matrix

| Area | Status | Notes |
| --- | --- | --- |
| Core concepts, terms, five phases, bagua, 24 mountains | Fully covered | Reference material and luopan helper included |
| Form school for homes, offices, shops, land, rooms | Fully covered | Practical outside-to-inside workflow included |
| Remedies and adjustments | Fully covered | Prioritizes repair, safety, reversibility, and symbolic clarity |
| Eight Mansions / ming gua | Fully covered | Common birth-year helper included; lineage year-boundary cautions documented |
| San Yuan 20-year periods | Fully covered | Period helper covers 1864-2043 |
| Xuan Kong Flying Stars | Partially covered | Basic Luo Shu scaffold and intake included; full natal chart, replacement stars, and lineage variants are future work |
| Date selection | Partially covered | Intake and safety framework included; no full almanac engine |
| Yin house / burial sites | Partially covered | Boundaries and conservative form reading included; advanced lineage formulas not automated |
| Cross-domain application | Partially covered | Finance, business, brand, career, product, learning, wellbeing, relationships, and negotiation adapter included |
| Finance / investing lens | Partially covered | Symbolic decision-support framework included; no investment recommendation engine |
| Structured floor-plan JSON | Fully covered | Schema, sample, and intake analyzer included |
| Image, map, or floor-plan auto parsing | Partially covered | Structured JSON is supported; raw computer-vision or GIS parsing is not included |
| Full bazi / four pillars | Not covered | Only ming gua is included; bazi is intentionally outside current scope |

## Repository Layout

```text
fengshui-master/
  SKILL.md
  agents/openai.yaml
  references/
    foundation.md
    forms-and-environment.md
    schools.md
    analysis-templates.md
    remedies.md
    timing-and-date-selection.md
    xuan-kong-flying-stars.md
    yin-house.md
    glossary.md
    case-patterns.md
    sample-readings.md
    domain-adapters.md
    finance-adapter.md
    floorplan-schema.md
    ethics-and-limits.md
    sources.md
  scripts/
    luopan.py
    minggua.py
    periods.py
    flying_stars.py
    domain_router.py
    analyze_floorplan.py
  assets/
    sample-floorplan.json
tests/
  test_luopan.py
  test_minggua.py
  test_periods.py
  test_flying_stars.py
  test_skill_inventory.py
```

## Install as a Local Codex Skill

Copy or symlink the `fengshui-master/` folder into your Codex skills directory.

```bash
mkdir -p ~/.codex/skills
cp -R fengshui-master ~/.codex/skills/
```

On Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force $HOME\.codex\skills
Copy-Item -Recurse -Force .\fengshui-master $HOME\.codex\skills\
```

Then ask Codex to use `$fengshui-master`.

## Example Prompts

- `Use $fengshui-master to review this apartment floor plan from a form-school perspective.`
- `Use $fengshui-master to analyze my desk placement. The desk faces 92 degrees and the door is behind my left side.`
- `Use $fengshui-master to compare two retail storefronts for customer flow and entrance quality.`
- `Use $fengshui-master to explain the difference between san he, san yuan, xuan kong, and ba zhai.`

## Luopan Helper

Convert a compass bearing into a 24-mountain sector:

```bash
python fengshui-master/scripts/luopan.py 187 --pretty
```

The helper only maps bearings. It does not judge auspiciousness by itself.

Calculate a common Eight Mansions ming gua:

```bash
python fengshui-master/scripts/minggua.py 1990 --sex male --pretty
```

Look up a common San Yuan / Xuan Kong 20-year period:

```bash
python fengshui-master/scripts/periods.py 2026 --pretty
```

Create a basic Luo Shu flying-star scaffold:

```bash
python fengshui-master/scripts/flying_stars.py --year 2026 --pretty
```

This helper is not a complete natal flying-star engine.

Route a cross-domain question:

```bash
python fengshui-master/scripts/domain_router.py "Should I buy this stock next month?" --pretty
```

The router points Codex to the correct references and guardrails; it does not make the decision.

Analyze a structured floor-plan JSON:

```bash
python fengshui-master/scripts/analyze_floorplan.py fengshui-master/assets/sample-floorplan.json --pretty
```

The JSON format is documented in `fengshui-master/references/floorplan-schema.md`.

## Validate

Run the standard-library tests:

```bash
python -m unittest discover -s tests
```

Run the Codex skill validator if available:

```bash
python C:/Users/Administrator/.codex/skills/.system/skill-creator/scripts/quick_validate.py fengshui-master
```

## Project Status

This is a comprehensive v1 skill with clear boundaries. Contributions are welcome for:

- Primary-source references and careful summaries.
- Additional lineage-specific notes with school labels.
- More deterministic tools, such as full natal flying-star charting, almanac-backed date selection, or floor-plan annotation.
- Additional sample floor plans for residential, office, retail, restaurant, site, and yin-house cases.
- Additional domain adapters for law-adjacent decisions, education, health-adjacent wellbeing, and product strategy.
- Example analyses and test fixtures.

## Disclaimer

FengShui Master is for cultural, educational, and design-support purposes. It is not medical, legal, financial, engineering, architectural, or safety advice.
