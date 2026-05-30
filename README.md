# FengShui Master

FengShui Master is an open Codex skill for traditional Chinese feng shui and broad wuxing symbolic analysis. It provides structured workflows, reference material, deterministic helpers, and a JSON floor-plan intake format for analyzing homes, offices, shops, rooms, land, floor plans, entrances, beds, desks, kitchens, directions, timing, xuan kong scaffolds, environmental form, life patterns, auspiciousness, inauspiciousness, and cross-domain decisions such as finance, business, brand, career, product, learning, and wellbeing.

The project treats feng shui as a traditional cultural, spatial, and symbolic-analysis system. It does not present symbolic readings as guaranteed predictions.

## What This Skill Covers

- Foundational concepts: qi, yin-yang, five phases, bagua, stems/branches, 24 mountains.
- Broad symbolic feng shui protocol: 观气, 取象, 辨势, conditional 吉凶, 化解, and 复核 for non-spatial readings.
- Broad symbolic analysis: life-pattern reading, auspiciousness/inauspiciousness framing, personal phase balance, event and decision omens, and "趋吉避凶" planning.
- Five-phase domain map: careers, industries, finance, brands, products, learning, relationships, negotiation, and personal behavior.
- Form analysis: landform, roads, water, buildings, entrances, circulation, sha qi, light, air, clutter.
- School selection: form school, compass school, san he, san yuan, xuan kong flying stars, eight mansions, symbolic bagua.
- Scenario workflows: residential, office, retail, restaurant, site selection, bedroom, desk, floor plan, renovation.
- Remedies and adjustments: mirrors, plants, screens, water, color, five-phase balancing, safe intervention ladder.
- Timing: san yuan periods, xuan kong inputs, annual/monthly layer cautions, date-selection intake.
- Xuan Kong Flying Stars: basic Luo Shu flight scaffold, star meanings, period cautions, natal-chart intake.
- Yin house boundaries: cemetery and burial-site intake, conservative form reading, ethics and safety.
- Cross-domain adapters: finance, business, brand, career, product, learning, wellbeing, relationships, and negotiation.
- Finance adapter: symbolic feng shui lens for investing, portfolio, budget, cash flow, and market-timing questions with strong financial guardrails.
- Business, brand, career, relationship, product, learning, wellbeing, and legal-adjacent adapters: specialized non-spatial workflows with native-domain constraints and feng shui symbolism kept separate.
- Consultation brief protocol: route questions, identify references, list missing inputs, apply guardrails, and define report sections before substantial readings.
- Reporting protocol: generate Markdown report scaffolds from briefs for reusable deliverables and examples.
- Structured floor-plan input: JSON schema, sample plan, and analyzer for repeatable room/site intake.
- Glossary and case patterns: Chinese terminology, response templates, comparison matrices.
- Safety and ethics: high-stakes claims, cultural respect, modern building constraints.
- Tooling: compass bearing to 24-mountain conversion, ming gua lookup, Gregorian-year ganzhi scaffold, annual tai sui/sui po/san sha cautions, san yuan period lookup, basic flying-star scaffold.

## Coverage Matrix

| Area | Status | Notes |
| --- | --- | --- |
| Core concepts, terms, five phases, bagua, 24 mountains | Fully covered | Reference material and luopan helper included |
| Broad symbolic protocol beyond space | Fully covered | 观气, 取象, 辨势, 吉凶, 生平, 金融, and decision-support protocol included |
| Broad life / omen / auspiciousness analysis | Fully covered | Symbolic life-pattern and ji/xiong adapter included; not deterministic fate-telling |
| Ganzhi year scaffold | Fully covered | Heavenly stem, earthly branch, zodiac, phase, and yin-yang helper included; not complete bazi |
| Five-phase cross-domain mapping | Fully covered | Careers, industries, finance, brand, product, relationship, learning, and negotiation mappings included |
| Form school for homes, offices, shops, land, rooms | Fully covered | Practical outside-to-inside workflow included |
| Remedies and adjustments | Fully covered | Prioritizes repair, safety, reversibility, and symbolic clarity |
| Eight Mansions / ming gua | Fully covered | Common birth-year helper included; lineage year-boundary cautions documented |
| San Yuan 20-year periods | Fully covered | Period helper covers 1864-2043 |
| Annual tai sui / sui po / san sha cautions | Fully covered | Common annual directional helper included; not a full almanac |
| Xuan Kong Flying Stars | Partially covered | Basic Luo Shu scaffold and intake included; full natal chart, replacement stars, and lineage variants are future work |
| Date selection | Partially covered | Intake and safety framework included; no full almanac engine |
| Yin house / burial sites | Partially covered | Boundaries and conservative form reading included; advanced lineage formulas not automated |
| Cross-domain application | Fully covered | General adapter plus life/omen and five-phase maps included for non-spatial questions |
| Finance / investing lens | Partially covered | Symbolic decision-support framework included; no investment recommendation engine |
| Business / brand / career / relationship adapters | Fully covered | Specialized references cover strategy, identity, work path, communication, and shared-space questions |
| Product / learning / wellbeing / legal-adjacent adapters | Fully covered | Specialized references cover UX flow, study planning, health-adjacent environment, and legal-risk preparation |
| Consultation brief generation | Fully covered | JSON brief generator combines domain routing, guardrails, missing inputs, and optional floor-plan analysis |
| Markdown report generation | Fully covered | Report scaffold generator creates reusable Markdown outputs from consultation briefs |
| Structured floor-plan JSON | Fully covered | Schema, sample, and intake analyzer included |
| Image, map, or floor-plan auto parsing | Partially covered | Structured JSON is supported; raw computer-vision or GIS parsing is not included |
| Full bazi / four pillars | Not covered | Life-pattern symbolism and ming gua are included; complete bazi charting is intentionally outside current scope |

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
    consultation-brief.md
    reporting-protocol.md
    broad-symbolic-analysis.md
    domain-adapters.md
    finance-adapter.md
    business-adapter.md
    brand-adapter.md
    career-adapter.md
    relationship-adapter.md
    product-adapter.md
    learning-adapter.md
    wellbeing-adapter.md
    legal-adjacent-adapter.md
    life-and-omen-adapter.md
    five-phase-domain-map.md
    floorplan-schema.md
    ethics-and-limits.md
    sources.md
  scripts/
    luopan.py
    minggua.py
    ganzhi.py
    annual_afflictions.py
    create_brief.py
    generate_report.py
    periods.py
    flying_stars.py
    domain_router.py
    analyze_floorplan.py
  assets/
    sample-floorplan.json
    sample-finance-brief.json
    sample-finance-report.md
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
- `Use $fengshui-master to analyze my career phase through five phases and 趋吉避凶 planning.`
- `Use $fengshui-master to review this investment decision through finance-first analysis and feng shui symbolism.`
- `Use $fengshui-master to explain the difference between san he, san yuan, xuan kong, and ba zhai.`

## Luopan Helper

Create a consultation brief for substantial readings:

```bash
python fengshui-master/scripts/create_brief.py "Should I buy this stock next month using feng shui?" --pretty
```

Attach a structured floor plan when available:

```bash
python fengshui-master/scripts/create_brief.py "Review this apartment layout" --floorplan fengshui-master/assets/sample-floorplan.json --pretty
```

The brief defines references, guardrails, missing inputs, and report sections. It is not the final reading.

Generate a Markdown report scaffold:

```bash
python fengshui-master/scripts/generate_report.py "Should I buy this stock next month using feng shui?"
```

Write the scaffold to a file:

```bash
python fengshui-master/scripts/generate_report.py "Should I buy this stock next month using feng shui?" --output fengshui-master/assets/sample-finance-report.md
```

Convert a compass bearing into a 24-mountain sector:

```bash
python fengshui-master/scripts/luopan.py 187 --pretty
```

The helper only maps bearings. It does not judge auspiciousness by itself.

Calculate a common Eight Mansions ming gua:

```bash
python fengshui-master/scripts/minggua.py 1990 --sex male --pretty
```

Look up a Gregorian-year heavenly stem / earthly branch scaffold:

```bash
python fengshui-master/scripts/ganzhi.py 2026 --pretty
```

This helper is year-level symbolic context only. It is not a complete bazi chart and requires li chun or lunar-year boundary confirmation near year transitions.

Look up common annual tai sui, sui po, and san sha directional cautions:

```bash
python fengshui-master/scripts/annual_afflictions.py 2026 --pretty
```

This helper is an annual timing caution layer only. It is not a full almanac or date-selection engine.

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

Run the portable repository consistency audit:

```bash
python .github/scripts/audit_repository.py
```

## GitHub Actions

The repository includes [`.github/workflows/ci.yml`](.github/workflows/ci.yml). On pushes and pull requests, GitHub Actions runs:

- `python -m unittest discover -s tests`
- portable skill metadata validation via `.github/scripts/quick_validate.py`
- repository consistency audit via `.github/scripts/audit_repository.py`
- smoke tests for the domain router, consultation brief generator, and report generator

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
