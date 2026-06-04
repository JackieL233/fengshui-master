# FengShui Master

[中文说明](README.zh-CN.md)

FengShui Master is a portable AI skill and general agent capability pack for traditional Chinese feng shui and broad wuxing symbolic analysis. It is Codex-compatible through `fengshui-master/SKILL.md`, but the knowledge base, workflows, scripts, examples, and guardrails are designed to work with any capable LLM, agent framework, assistant, or local automation environment.

It provides structured workflows, reference material, deterministic helpers, portable system instructions, and a JSON floor-plan intake format for analyzing homes, offices, shops, rooms, land, floor plans, entrances, beds, desks, kitchens, directions, timing, xuan kong scaffolds, environmental form, life patterns, auspiciousness, inauspiciousness, and cross-domain decisions such as finance, business, brand, career, product, learning, and wellbeing.

The project treats feng shui as a traditional cultural, spatial, and symbolic-analysis system. It does not present symbolic readings as guaranteed predictions.

## GitHub Repository Metadata

Suggested repository name:

```text
fengshui-master
```

Suggested short description:

```text
Portable AI skill and Codex-compatible capability pack for traditional Chinese feng shui, wuxing, auspiciousness, spatial analysis, and cross-domain symbolic decision support.
```

Suggested Chinese description:

```text
通用 AI Skill 与兼容 Codex 的风水智能体能力包，覆盖传统风水、五行、吉凶、空间分析与跨领域象义决策支持。
```

Suggested topics:

```text
feng-shui, fengshui, wuxing, five-elements, bagua, chinese-metaphysics, traditional-chinese-culture, ai-skill, agent-skill, portable-skill, codex-skill, symbolic-analysis, spatial-analysis, cultural-analysis, auspiciousness
```

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
- Consultation brief protocol: select methods, route questions, identify references, list missing inputs, apply guardrails, and define report sections before substantial readings.
- Reporting protocol: generate Markdown report scaffolds from briefs for reusable deliverables and examples.
- Structured floor-plan input: JSON schema, sample plan, and analyzer for repeatable room/site intake.
- Glossary and case patterns: Chinese terminology, response templates, comparison matrices.
- Safety and ethics: high-stakes claims, cultural respect, modern building constraints.
- Source and school mapping: classical anchors, Form School, San He, San Yuan, Xuan Kong, Eight Mansions, date selection, 24 solar terms, moon phase, and modern cross-domain extension boundaries.
- Tooling: bagua sector mapping, compass bearing to 24-mountain conversion, ming gua lookup, Gregorian-year ganzhi scaffold, annual tai sui/sui po/san sha cautions, 24 solar terms / seasonal qi lookup, san yuan period lookup, basic flying-star scaffold.

## Coverage Matrix

| Area | Status | Notes |
| --- | --- | --- |
| Core concepts, terms, five phases, bagua, 24 mountains | Fully covered | Reference material and luopan helper included |
| Bagua sector / trigram / life-area mapping | Fully covered | Bagua helper maps direction, bearing, trigram, and life area; does not prove auspiciousness |
| Broad symbolic protocol beyond space | Fully covered | 观气, 取象, 辨势, 吉凶, 生平, 金融, and decision-support protocol included |
| Broad life / omen / auspiciousness analysis | Fully covered | Symbolic life-pattern and ji/xiong adapter included; not deterministic fate-telling |
| Ganzhi year scaffold | Fully covered | Heavenly stem, earthly branch, zodiac, phase, and yin-yang helper included; not complete bazi |
| Five-phase cross-domain mapping | Fully covered | Careers, industries, finance, brand, product, relationship, learning, and negotiation mappings included |
| Form school for homes, offices, shops, land, rooms | Fully covered | Practical outside-to-inside workflow included |
| Remedies and adjustments | Fully covered | Prioritizes repair, safety, reversibility, and symbolic clarity |
| Eight Mansions / ming gua | Fully covered | Common birth-year helper included; lineage year-boundary cautions documented |
| San Yuan 20-year periods | Fully covered | Period helper covers 1864-2043 |
| Annual tai sui / sui po / san sha cautions | Fully covered | Common annual directional helper included; not a full almanac |
| New moon / full moon / moon phase timing | Partially covered | Approximate moon-phase helper and symbolic timing guidance included; not a full almanac or precision astronomy engine |
| 24 solar terms / seasonal qi timing | Partially covered | Approximate solar-term helper and symbolic timing guidance included; not a full almanac or precision astronomy engine |
| Xuan Kong Flying Stars | Partially covered | Basic Luo Shu scaffold and intake included; full natal chart, replacement stars, and lineage variants are future work |
| Date selection | Partially covered | Intake and safety framework included; no full almanac engine |
| Yin house / burial sites | Partially covered | Boundaries and conservative form reading included; advanced lineage formulas not automated |
| Cross-domain application | Fully covered | General adapter plus life/omen and five-phase maps included for non-spatial questions |
| Finance / investing lens | Partially covered | Symbolic decision-support framework included; no investment recommendation engine |
| Business / brand / career / relationship adapters | Fully covered | Specialized references cover strategy, identity, work path, communication, and shared-space questions |
| Product / learning / wellbeing / legal-adjacent adapters | Fully covered | Specialized references cover UX flow, study planning, health-adjacent environment, and legal-risk preparation |
| Method and school selection | Fully covered | Method selector distinguishes form school, compass bagua, eight mansions, xuan kong, san he, timing, and broad symbolic analysis |
| Consultation brief generation | Fully covered | JSON brief generator combines domain routing, guardrails, missing inputs, and optional floor-plan analysis |
| Markdown report generation | Fully covered | Report scaffold generator creates reusable Markdown outputs from consultation briefs |
| Structured floor-plan JSON | Fully covered | Schema, sample, and intake analyzer included |
| Image, map, or floor-plan auto parsing | Partially covered | Structured JSON is supported; raw computer-vision or GIS parsing is not included |
| Full bazi / four pillars | Not covered | Life-pattern symbolism and ming gua are included; complete bazi charting is intentionally outside current scope |

## Repository Layout

```text
PORTABLE_SKILL.md
portable-skill.json
README.md
README.zh-CN.md
CHANGELOG.md
RELEASE_NOTES.md
SECURITY.md
CODE_OF_CONDUCT.md
.gitattributes
.editorconfig
docs/
  integration-guide.md
schemas/
  portable-skill.schema.json
  portable-evaluation-suite.schema.json
  reference-catalog.schema.json
  tool-catalog.schema.json
  response-contract.schema.json
  capability-matrix.schema.json
  source-quality-policy.schema.json
  adversarial-evaluation-suite.schema.json
  intake-contracts.schema.json
  golden-responses.schema.json
  universal-domain-protocol.schema.json
examples/
  portable-agent-prompts.md
  portable-evaluation-rubric.json
  portable-evaluation-suite.json
  reference-catalog.json
  tool-catalog.json
  response-contract.json
  capability-matrix.json
  source-quality-policy.json
  adversarial-evaluation-suite.json
  intake-contracts.json
  golden-responses.json
  universal-domain-protocol.json
  validate_portable_evaluation.py
  validate_portable_manifest.py
  validate_reference_catalog.py
  validate_tool_catalog.py
  validate_response_contract.py
  validate_capability_matrix.py
  validate_source_quality_policy.py
  validate_adversarial_evaluation.py
  validate_intake_contracts.py
  validate_golden_responses.py
  validate_universal_domain_protocol.py
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
    classical-source-map.md
    sources.md
  scripts/
    method_selector.py
    bagua_map.py
    luopan.py
    minggua.py
    ganzhi.py
    annual_afflictions.py
    moon_phase.py
    solar_terms.py
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
    sample-life-omen-report.md
    sample-product-report.md
    sample-floorplan-report.md
tests/
  test_luopan.py
  test_minggua.py
  test_periods.py
  test_flying_stars.py
  test_skill_inventory.py
```

## Portable Usage

Use [`PORTABLE_SKILL.md`](PORTABLE_SKILL.md) when you want FengShui Master outside Codex. It contains a copyable system instruction, required operating rules, report structure, domain routing guidance, and Chinese instructions for any AI agent or assistant.

Use [`portable-skill.json`](portable-skill.json) when an agent platform needs a machine-readable manifest of entrypoints, references, tools, evaluation files, governance files, domains, and guardrails.

Use [`docs/integration-guide.md`](docs/integration-guide.md) for concrete ChatGPT, Claude, Gemini, local LLM, agent-framework, RAG, CLI, and Codex integration patterns.

Schema files are provided for platform integrations:

- [`schemas/portable-skill.schema.json`](schemas/portable-skill.schema.json)
- [`schemas/portable-evaluation-suite.schema.json`](schemas/portable-evaluation-suite.schema.json)
- [`schemas/reference-catalog.schema.json`](schemas/reference-catalog.schema.json)
- [`schemas/tool-catalog.schema.json`](schemas/tool-catalog.schema.json)
- [`schemas/response-contract.schema.json`](schemas/response-contract.schema.json)
- [`schemas/capability-matrix.schema.json`](schemas/capability-matrix.schema.json)
- [`schemas/source-quality-policy.schema.json`](schemas/source-quality-policy.schema.json)
- [`schemas/adversarial-evaluation-suite.schema.json`](schemas/adversarial-evaluation-suite.schema.json)
- [`schemas/intake-contracts.schema.json`](schemas/intake-contracts.schema.json)
- [`schemas/golden-responses.schema.json`](schemas/golden-responses.schema.json)
- [`schemas/universal-domain-protocol.schema.json`](schemas/universal-domain-protocol.schema.json)

Common integration patterns:

- **ChatGPT, Claude, Gemini, local LLMs, or custom agents**: paste the "System Instruction" from `PORTABLE_SKILL.md`, then provide the relevant files from `fengshui-master/references/` as retrieval context.
- **Agent frameworks**: expose `fengshui-master/scripts/` as tools and let the agent read `PORTABLE_SKILL.md` plus the routed reference files.
- **RAG systems**: index `fengshui-master/references/`, keep `PORTABLE_SKILL.md` as the top-level behavior policy, and keep `fengshui-master/SKILL.md` as the Codex adapter.
- **Manual use**: run `method_selector.py`, `create_brief.py`, `domain_router.py`, and `generate_report.py` from the command line to create structured analysis scaffolds before writing the final answer.

For portable agent smoke tests and copyable prompts, see [`examples/portable-agent-prompts.md`](examples/portable-agent-prompts.md). For machine-readable adaptation checks, use [`examples/portable-evaluation-suite.json`](examples/portable-evaluation-suite.json). For adversarial red-team prompts, prompt-injection checks, and scope-inflation checks, use [`examples/adversarial-evaluation-suite.json`](examples/adversarial-evaluation-suite.json). For domain intake and missing-input rules, use [`examples/intake-contracts.json`](examples/intake-contracts.json). For compact golden response fixtures, use [`examples/golden-responses.json`](examples/golden-responses.json). For adapting FengShui Master to domains beyond the built-in list, use [`examples/universal-domain-protocol.json`](examples/universal-domain-protocol.json). For output-quality scoring, use [`examples/portable-evaluation-rubric.json`](examples/portable-evaluation-rubric.json). For final-answer structure and red-line behavior, use [`examples/response-contract.json`](examples/response-contract.json). For RAG metadata and reference routing, use [`examples/reference-catalog.json`](examples/reference-catalog.json). For script metadata and agent tool registration, use [`examples/tool-catalog.json`](examples/tool-catalog.json). For capability, limitation, and roadmap routing, use [`examples/capability-matrix.json`](examples/capability-matrix.json). For source tiers, citation posture, and claim-quality rules, use [`examples/source-quality-policy.json`](examples/source-quality-policy.json). For deployment across non-Codex platforms, follow [`docs/integration-guide.md`](docs/integration-guide.md).

Validate the portable evaluation suite:

```bash
python examples/validate_portable_evaluation.py
```

Validate the portable manifest:

```bash
python examples/validate_portable_manifest.py
```

Validate the reference catalog:

```bash
python examples/validate_reference_catalog.py
```

Validate the tool catalog:

```bash
python examples/validate_tool_catalog.py
```

Validate the response contract:

```bash
python examples/validate_response_contract.py
```

Validate the capability matrix:

```bash
python examples/validate_capability_matrix.py
```

Validate the source quality policy:

```bash
python examples/validate_source_quality_policy.py
```

Validate the adversarial evaluation suite:

```bash
python examples/validate_adversarial_evaluation.py
```

Validate the intake contracts:

```bash
python examples/validate_intake_contracts.py
```

Validate the golden responses:

```bash
python examples/validate_golden_responses.py
```

Validate the universal domain protocol:

```bash
python examples/validate_universal_domain_protocol.py
```

## Codex Installation

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

- `Use FengShui Master to review this apartment floor plan from a form-school perspective.`
- `Use FengShui Master to analyze my desk placement. The desk faces 92 degrees and the door is behind my left side.`
- `Use FengShui Master to compare two retail storefronts for customer flow and entrance quality.`
- `Use FengShui Master to analyze my career phase through five phases and 趋吉避凶 planning.`
- `Use FengShui Master to review this investment decision through finance-first analysis and feng shui symbolism.`
- `Use FengShui Master to explain the difference between san he, san yuan, xuan kong, and ba zhai.`

In Codex, the same prompts can use `$fengshui-master`.

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

Map a bagua sector, trigram, direction, or life-area symbolism:

```bash
python fengshui-master/scripts/bagua_map.py --direction southeast --pretty
python fengshui-master/scripts/bagua_map.py --life-area wealth --method symbolic --pretty
```

This helper maps later-heaven bagua symbolism and method labels. It does not prove wealth, relationship, health, or career outcomes.

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

Look up approximate New Moon / Full Moon / moon phase context:

```bash
python fengshui-master/scripts/moon_phase.py 2024-04-08 --pretty
```

This helper supports moon-phase symbolism for timing questions. It is not a full almanac, precise astronomy engine, or guarantee of auspiciousness.

Look up approximate 24 solar terms / seasonal qi context:

```bash
python fengshui-master/scripts/solar_terms.py 2026-02-04 --pretty
```

This helper supports solar-term symbolism for timing questions, including li chun, equinox, summer solstice, and winter solstice context. It is not a full almanac, precise astronomy engine, exact solar-term ephemeris, or guarantee of auspiciousness.

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

Select the appropriate feng shui method or school:

```bash
python fengshui-master/scripts/method_selector.py "Use Xuan Kong flying stars for this Period 9 renovation" --pretty
```

The selector returns recommended methods, required inputs, references, tools, guardrails, and method notes. Use it to avoid silent school mixing: do not mix schools silently.

Analyze a structured floor-plan JSON:

```bash
python fengshui-master/scripts/analyze_floorplan.py fengshui-master/assets/sample-floorplan.json --pretty
```

The JSON format is documented in `fengshui-master/references/floorplan-schema.md`.

## Sample Assets

GitHub-readable samples are included for quick evaluation:

- `fengshui-master/assets/sample-finance-report.md`: finance-first decision support with feng shui symbolism.
- `fengshui-master/assets/sample-life-omen-report.md`: broad life, 五行, 吉凶, and 趋吉避凶 scaffold.
- `fengshui-master/assets/sample-product-report.md`: product onboarding flow analyzed through form, flow, leakage, and symbolic lenses.
- `fengshui-master/assets/sample-floorplan-report.md`: structured floor-plan intake and form-analysis scaffold.
- `fengshui-master/assets/sample-floorplan.json`: repeatable floor-plan JSON input.
- `fengshui-master/assets/sample-finance-brief.json`: generated consultation brief fixture.

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
- portable evaluation-suite validation via `examples/validate_portable_evaluation.py`
- portable manifest validation via `examples/validate_portable_manifest.py`
- smoke tests for the domain router, consultation brief generator, and report generator

## Project Status

This is a comprehensive v1 skill with clear boundaries. Contributions are welcome for:

- Primary-source references and careful summaries.
- Additional lineage-specific notes with school labels.
- More deterministic tools, such as full natal flying-star charting, almanac-backed date selection, or floor-plan annotation.
- Additional sample floor plans for residential, office, retail, restaurant, site, and yin-house cases.
- Additional domain adapters for law-adjacent decisions, education, health-adjacent wellbeing, and product strategy.
- Example analyses and test fixtures.

## Governance

- See [`CHANGELOG.md`](CHANGELOG.md) for release history and notable changes.
- See [`RELEASE_NOTES.md`](RELEASE_NOTES.md) for the v1 release summary.
- See [`SECURITY.md`](SECURITY.md) for high-stakes safety, prompt-injection, and cultural-respect reporting.
- See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for respectful collaboration expectations.
- See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution principles and validation commands.
- `.gitattributes` and `.editorconfig` keep line endings, encoding, and indentation stable across platforms.

## Disclaimer

FengShui Master is for cultural, educational, and design-support purposes. It is not medical, legal, financial, engineering, architectural, or safety advice.
