# Contributing

Thanks for helping improve FengShui Master.

## Contribution Principles

- Name the feng shui school, lineage, or source family behind specialized rules.
- Separate classical concepts, later lineage practice, modern adaptations, and personal interpretation.
- Prefer practical, low-risk recommendations before symbolic cures.
- Avoid fear-based or guaranteed claims about health, wealth, marriage, pregnancy, death, or disaster.
- Keep `SKILL.md` concise; put detailed knowledge in `fengshui-master/references/`.
- Add tests for deterministic scripts.

## Good Contributions

- A sourced explanation of a concept.
- A new scenario template.
- A deterministic helper script with tests.
- A correction to terminology, transliteration, or school boundaries.
- A safer wording pattern for high-stakes topics.

## Avoid

- Unsourced universal rules.
- Long copied passages from copyrighted books or websites.
- Claims that feng shui guarantees outcomes.
- Remedies that create safety, accessibility, legal, or maintenance problems.

## Validation

Before opening a pull request, run:

```bash
python -m unittest discover -s tests
```

If you have the Codex skill-creator tools installed, also run:

```bash
python C:/Users/Administrator/.codex/skills/.system/skill-creator/scripts/quick_validate.py fengshui-master
```

Run the portable repository audit before opening a pull request:

```bash
python .github/scripts/audit_repository.py
```

GitHub Actions also runs the CI workflow in `.github/workflows/ci.yml` for pushes and pull requests. It executes the unit test suite, portable skill metadata validation, repository consistency audit, and smoke tests for the main CLI helpers.
