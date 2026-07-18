# Changelog

All notable changes to FengShui Master are documented here.

## Unreleased

### Added

- Positioned FengShui Master as a portable AI skill and Codex-compatible capability pack.
- Added `PORTABLE_SKILL.md` for platform-independent agent instructions.
- Added `portable-skill.json` as a machine-readable manifest for entrypoints, references, tools, evaluation assets, governance files, domains, and guardrails.
- Added JSON Schemas:
  - `schemas/portable-skill.schema.json`
  - `schemas/portable-evaluation-suite.schema.json`
- Added portable evaluation suite assets:
  - `examples/portable-agent-prompts.md`
  - `examples/portable-evaluation-suite.json`
  - `examples/validate_portable_evaluation.py`
  - `examples/validate_portable_manifest.py`
- Added Security Policy and Code of Conduct for high-stakes safety, prompt-injection, cultural respect, and collaboration boundaries.
- Added cross-domain adapters for finance, business, brand, career, relationship, product, learning, wellbeing, legal-adjacent risk, and life/omen readings.
- Added deterministic helpers for domain routing, consultation briefs, report scaffolds, floor-plan JSON analysis, luopan bearings, ming gua, ganzhi year scaffolds, annual directional cautions, san yuan periods, and flying-star scaffolds.
- Added `personal_context.py` to combine supplied birth data with bounded year-ganzhi, ming-gua, san-yuan, annual-direction, solar-term, and moon-phase context without claiming a complete natal chart.
- Added a dedicated naming domain and `naming-adapter.md` for personal, baby, adult-renaming, pen/stage, brand, company, shop, and product names, with native naming checks separated from method-dependent wuxing symbolism.
- Added context-fusion priority rules so relevant personal, spatial, timing, business, deterministic, traditional, and symbolic layers are linked with provenance instead of silently mixed or reduced to a fake score.
- Added `proactive-reading-protocol.md` and a machine-readable proactive scan contract so current-state readings identify favorable signals, conditional friction, validation evidence, immediate actions, and 72-hour / 30-day / 90-day horizons without cold-reading claims.
- Improved life/omen consultation briefs so birth year, topic, and reading goal are not reported missing when the question already supplies them.
- Added bilingual README files, GitHub repository metadata, CI, issue templates, pull request template, deployment checklist, sample reports, and repository audit tooling.

### Safety

- High-stakes topics must start with real-world constraints before symbolic interpretation.
- Feng shui readings must not be presented as medical, legal, financial, engineering, tax, psychological, architectural, or safety advice.
- The skill must not claim guaranteed outcomes, deterministic fate, certain market timing, unavoidable illness, doomed relationships, or certain disaster.

### Validation

- Unit tests cover scripts, inventory, repository quality, portable positioning, governance files, evaluation suite, and manifest checks.
- CI runs:
  - `python -m unittest discover -s tests`
  - `python .github/scripts/quick_validate.py fengshui-master`
  - `python .github/scripts/audit_repository.py`
  - `python examples/validate_portable_evaluation.py`
  - `python examples/validate_portable_manifest.py`

## v1.0.0

Initial comprehensive open-source release target for FengShui Master as a portable AI skill and Codex-compatible traditional Chinese feng shui capability pack.
