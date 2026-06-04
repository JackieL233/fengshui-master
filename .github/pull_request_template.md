## Summary

Describe the change and the user-facing scenario it improves.

## Area

Check all that apply:

- [ ] Skill instructions
- [ ] Reference material
- [ ] Deterministic script
- [ ] Tests
- [ ] Sample asset or report
- [ ] GitHub/open-source maintenance

## Feng shui school or source basis

Name the feng shui school, lineage, source family, or modern adaptation behind any traditional claim. If this is a cross-domain change, explain how the symbolism is mapped to the native domain.

## Safety guardrails

Confirm the change preserves boundaries:

- [ ] Separates real-world constraints from feng shui symbolism.
- [ ] Avoids deterministic fate, wealth, health, marriage, pregnancy, death, disaster, or market predictions.
- [ ] Keeps high-stakes answers visible as not financial advice, not medical advice, and not legal advice where relevant.
- [ ] Preserves the medical, legal, financial, engineering, architectural, tax, psychological, and safety boundary when relevant.
- [ ] Avoids unsafe, inaccessible, illegal, or irreversible remedies.

## Contribution quality gates

- [ ] I checked `examples/contribution-quality-gates.json` for the required artifacts, checks, validations, and red lines for this change type.
- [ ] I ran `python examples/validate_contribution_quality_gates.py`.

## Validation

```bash
python -m unittest discover -s tests
python .github/scripts/quick_validate.py fengshui-master
python .github/scripts/audit_repository.py
python examples/validate_contribution_quality_gates.py
```
