# FengShui Master v1 Release Notes

FengShui Master v1 is a Portable AI Skill and Codex-compatible capability pack for traditional Chinese feng shui, wuxing, auspiciousness, spatial analysis, and cross-domain symbolic decision support.

## What is included

- Codex entrypoint: `fengshui-master/SKILL.md`
- Portable entrypoint: `PORTABLE_SKILL.md`
- Machine-readable manifest: `portable-skill.json`
- JSON Schemas for portable platform integrations:
  - `schemas/portable-skill.schema.json`
  - `schemas/portable-evaluation-suite.schema.json`
- Reference knowledge base for:
  - foundational feng shui concepts
  - form and environment analysis
  - schools and method selection
  - remedies and safe adjustments
  - timing and date-selection intake
  - xuan kong flying-star scaffolds
  - yin house boundaries
  - broad symbolic analysis beyond space
  - finance, business, brand, career, relationship, product, learning, wellbeing, legal-adjacent, and life/omen adapters
- Deterministic helper scripts for:
  - domain routing
  - consultation brief generation
  - Markdown report scaffolds
  - structured floor-plan JSON analysis
  - luopan 24-mountain mapping
  - ming gua lookup
  - Gregorian-year ganzhi scaffold
  - annual tai sui / sui po / san sha cautions
  - san yuan period lookup
  - basic flying-star scaffold
- Sample floor plan, sample briefs, and sample reports.

## Safety and governance

FengShui Master treats feng shui as traditional cultural, spatial, and symbolic analysis. It is not medical, legal, financial, engineering, architectural, tax, psychological, or safety advice.

The release includes:

- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- GitHub issue templates
- Pull request template
- Guardrails for high-stakes topics, prompt-injection, cultural respect, and professional-boundary separation.

## Validation

Before release, run:

```bash
python -m unittest discover -s tests
python .github/scripts/quick_validate.py fengshui-master
python .github/scripts/audit_repository.py
python examples/validate_portable_evaluation.py
python examples/validate_portable_manifest.py
```

Expected result:

```text
All unit tests pass
Skill is valid!
Repository audit passed
Portable evaluation suite is valid
Portable skill manifest is valid
```

## Recommended GitHub About

Description:

```text
Portable AI skill and Codex-compatible capability pack for traditional Chinese feng shui, wuxing, auspiciousness, spatial analysis, and cross-domain symbolic decision support.
```

Topics:

```text
feng-shui, fengshui, wuxing, five-elements, bagua, chinese-metaphysics, traditional-chinese-culture, ai-skill, agent-skill, portable-skill, codex-skill, symbolic-analysis, spatial-analysis, cultural-analysis, auspiciousness
```
