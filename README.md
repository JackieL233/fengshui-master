# FengShui Master

FengShui Master is an open Codex skill for traditional Chinese feng shui analysis. It provides structured workflows, reference material, and a small deterministic luopan helper for analyzing homes, offices, shops, rooms, land, floor plans, entrances, beds, desks, kitchens, directions, and environmental form.

The project treats feng shui as a traditional cultural and spatial-analysis system. It does not present symbolic readings as guaranteed predictions.

## What This Skill Covers

- Foundational concepts: qi, yin-yang, five phases, bagua, stems/branches, 24 mountains.
- Form analysis: landform, roads, water, buildings, entrances, circulation, sha qi, light, air, clutter.
- School selection: form school, compass school, san he, san yuan, xuan kong flying stars, eight mansions, symbolic bagua.
- Scenario workflows: residential, office, retail, restaurant, site selection, bedroom, desk, floor plan, renovation.
- Remedies and adjustments: mirrors, plants, screens, water, color, five-phase balancing, safe intervention ladder.
- Timing: san yuan periods, xuan kong inputs, annual/monthly layer cautions, date-selection intake.
- Glossary and case patterns: Chinese terminology, response templates, comparison matrices.
- Safety and ethics: high-stakes claims, cultural respect, modern building constraints.
- Tooling: compass bearing to 24-mountain conversion, ming gua lookup, san yuan period lookup.

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
    glossary.md
    case-patterns.md
    ethics-and-limits.md
    sources.md
  scripts/
    luopan.py
    minggua.py
    periods.py
tests/
  test_luopan.py
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

This is an initial comprehensive skeleton. Contributions are welcome for:

- Primary-source references and careful summaries.
- Additional lineage-specific notes with school labels.
- More deterministic tools, such as gua-number calculation or flying-star chart scaffolding.
- Example analyses and test fixtures.

## Disclaimer

FengShui Master is for cultural, educational, and design-support purposes. It is not medical, legal, financial, engineering, architectural, or safety advice.
