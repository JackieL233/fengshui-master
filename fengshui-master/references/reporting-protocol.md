# Reporting Protocol

Use this file when turning a FengShui Master consultation brief into a final answer or reusable Markdown report.

## Purpose

The report protocol keeps readings consistent across spaces, finance, life/omen questions, career, brand, wellbeing, and other domains. It ensures every safe answer leads with a bounded provisional current-posture headline, separates evidence from symbolism, names guardrails, and delays follow-up questions until after useful actions and monitoring.

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
- After urgent safety triage, lead with a bounded provisional current-posture headline before method detail, missing-data lists, or non-urgent questions.
- Keep report sections proportional to the user's request.
- Use the generated Markdown as a scaffold; fill sections only with known facts, transparent assumptions, and clearly labeled traditional interpretations.
- Do not invent missing data.
- Do not convert guardrails into tiny disclaimers; keep them visible when the domain is high-stakes.
- Give low-risk, reversible next actions before asking follow-up questions.
- Label material content as observed, calculated, inferred, unknown, or recommended.
- For each relevant domain, include favorable signals, possible friction, ordinary manifestations, evidence that would confirm or refute the inference, and an immediate low-risk action.
- Follow substantial proactive reports with next-72-hour, next-30-day, and next-90-day actions plus observable monitoring signals, then ask at most three high-value questions.

## Section Guidance

| Section type | What to include |
| --- | --- |
| Provisional current posture | Narrow, conditional headline supported by the available evidence |
| Known basis | User-provided facts, assumptions, confidence, and uncertainty |
| Favorable now | Current support, opportunity, backing, or useful momentum |
| Possible friction | Bounded hypotheses and ordinary ways they may manifest |
| Confirm or refute | Observable evidence that would strengthen or weaken each material inference |
| Immediate action | One low-risk, reversible, native-domain action |
| Cross-domain priorities | Ranked concerns by safety, deadline, downside, dependency, and leverage |
| Action horizons and monitoring | Actions for 72 hours, 30 days, and 90 days; indicators, review point, and stop conditions |
| Follow-up questions | At most three questions that materially change confidence or action; place them after monitoring |
| Reality layer | Native domain constraints before symbolism |
| Symbolic analysis protocol | 观气, 取象, 辨势, 吉凶, 化解, and 复核 summary for broad non-spatial readings |
| Symbolic layer | Yin-yang, five phases, form/flow, timing, bagua, or ji/xiong interpretation |
| Structured floor-plan analysis | JSON findings, issues, and recommendations, with visual-verification caveats |
| Recommendations | Prioritized, practical, reversible actions |
| Missing data | Inputs that would materially change precision; do not place this before the provisional headline |
| Boundary | Professional and cultural limits |

## Common Mistakes

- Do not leave generated placeholder text in a final user-facing answer.
- Do not present the generated scaffold as a completed reading.
- Do not use feng shui symbolism to override domain evidence.
- Do not flatten all traditions into one universal method.
- Do not remove guardrails for finance, health, legal, relationship, death, pregnancy, disaster, or major life decisions.
