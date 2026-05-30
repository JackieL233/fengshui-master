# Reporting Protocol

Use this file when turning a FengShui Master consultation brief into a final answer or reusable Markdown report.

## Purpose

The report protocol keeps readings consistent across spaces, finance, life/omen questions, career, brand, wellbeing, and other domains. It ensures every answer separates evidence from symbolism, names guardrails, lists missing inputs, and ends with practical next actions.

Run:

```bash
python fengshui-master/scripts/generate_report.py "<question>"
```

Write a sample file:

```bash
python fengshui-master/scripts/generate_report.py "<question>" --output fengshui-master/assets/sample-finance-report.md
```

Attach structured floor-plan JSON when available:

```bash
python fengshui-master/scripts/generate_report.py "Review this apartment" --floorplan fengshui-master/assets/sample-floorplan.json
```

## Report Rules

- Start from a consultation brief, not from intuition alone.
- Keep report sections proportional to the user's request.
- Use the generated Markdown as a scaffold; fill sections only with known facts, transparent assumptions, and clearly labeled traditional interpretations.
- Do not invent missing data.
- Do not convert guardrails into tiny disclaimers; keep them visible when the domain is high-stakes.
- End with low-risk, reversible next actions where possible.

## Section Guidance

| Section type | What to include |
| --- | --- |
| Inputs and assumptions | User-provided facts, inferred facts, and uncertainty |
| Reality layer | Native domain constraints before symbolism |
| Symbolic layer | Yin-yang, five phases, form/flow, timing, bagua, or ji/xiong interpretation |
| Structured floor-plan analysis | JSON findings, issues, and recommendations, with visual-verification caveats |
| Recommendations | Prioritized, practical, reversible actions |
| Missing data | Inputs that would materially change confidence |
| Boundary | Professional and cultural limits |

## Common Mistakes

- Do not leave generated placeholder text in a final user-facing answer.
- Do not present the generated scaffold as a completed reading.
- Do not use feng shui symbolism to override domain evidence.
- Do not flatten all traditions into one universal method.
- Do not remove guardrails for finance, health, legal, relationship, death, pregnancy, disaster, or major life decisions.
