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
- Follow substantial proactive reports with next-72-hour, next-30-day, and next-90-day actions plus observable monitoring signals, then optionally ask zero to three high-value questions; three is a ceiling and zero is valid.

## Multi-turn Reports

Treat a follow-up report as a delta over the current conversation, not a new intake. Reuse explicit facts, constraints, corrections, and already recorded refusals; do not re-ask known facts or re-request declined inputs. The latest user correction supersedes the earlier value: retract dependent inferences and recalculate only affected outputs, leaving unrelated conclusions unchanged.

Lead a follow-up with any material change or unchanged context and the next step when useful, in the user's language; do not require literal headings. If there is no material update, say so and do not invent one. Keep only the sections that help answer the follow-up; a short continuation need not fill every heading or repeat the full intake. Adapt the immediate action horizon to the user's actual deadline rather than forcing fixed planning bands. Honor an explicit "do not ask" request by asking zero questions unless urgent safety requires a necessary clarification; keep any safety guidance concise. Before keyword routing, resolve current-turn corrections and negation, preserve the user's actual current topic, and reject any route triggered only by a denied, quoted, or stale fact.

For live calculations, use the actual host/user as-of date and timezone; dates in examples are illustrative only. Keep birth location distinct from present location and analysis timezone. Respond in the user's language. Do not imply persistence, reminders, or external actions without an explicit user request. A symbolic mapping is an interpretive lens, never evidence that an event occurred or will occur. Preserve useful cultural interpretation when concrete basis exists; otherwise label the point `unknown` and state what would verify it. Treat adapter "Ask for" lists as optional precision inventories, not mandatory questionnaires; they cannot override the zero-to-three ceiling or declined fields. Stay within requested scope and do not promise complete charts or universal predictions.

Improvement after a recommendation is not causal proof. Track the action, start date or time, outcome measure, and plausible alternatives or parallel changes; do not infer "luck cured" or "remedy succeeded" from timing alone.

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
| Follow-up questions | Zero to three questions that materially change confidence or action; three is a ceiling, zero is valid, and place any questions after monitoring |
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
