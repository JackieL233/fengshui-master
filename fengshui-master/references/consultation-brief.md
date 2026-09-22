# Consultation Brief Protocol

Use this file when starting any substantial FengShui Master reading, especially cross-domain questions, finance decisions, life/omen readings, or structured floor-plan reviews.

## Purpose

A consultation brief prevents the answer from jumping straight to symbolic claims. It records the user's question, routes the domain, names the references to load, lists guardrails, identifies missing inputs, and defines the report sections before analysis begins.

Run:

```bash
python fengshui-master/scripts/create_brief.py "<question>" --pretty
```

For structured plans:

```bash
python fengshui-master/scripts/create_brief.py "Review this apartment" --floorplan fengshui-master/assets/sample-floorplan.json --pretty
```

## Brief Fields

For follow-ups, reuse explicit current-conversation inputs with `--known-inputs <path.json>` (or Python `known_inputs=`). Supply an object whose keys are exact labels in `DOMAIN_MISSING_INPUTS` in `create_brief.py` and whose values are nonblank strings. For example, `{"time horizon": "Three years"}` removes that input from the missing list. Values are unverified supplied context, may appear in the output, and are never stored automatically. Update corrected values before calling; do not encode guesses or declined inputs as facts. The current question still determines routing, so include its already-known topic in elliptical follow-ups.

| Field | Meaning |
| --- | --- |
| question | User's consultation goal |
| domain | Routed domain: space, finance, life_omen, brand, career, wellbeing, or general |
| references | Skill references to load before answering, including `broad-symbolic-analysis.md` for broad 吉凶, 运势, 生平, finance-symbolic, or other non-spatial readings |
| guardrails | Claims or behaviors to avoid |
| lenses | Symbolic lenses to consider |
| missing_inputs | Inputs that would improve confidence |
| input_state | Provided and missing labels; optional supplied values and provenance when known-input context is passed |
| proactive_delivery | Provisional-first order, safety stops, domain priorities, and follow-up question budget |
| report_sections | Suggested final answer structure |
| floorplan_analysis | Structured plan intake result when supplied |
| answer_contract | Non-negotiable response rules |

The generated reference set also includes `proactive-reading-protocol.md`, and the report sections include a current-state scan, favorable conditions, possible friction with validation questions, three action horizons, and monitoring signals.

## How to Use

1. Generate the brief for non-trivial requests.
2. Load only the references named by the brief.
3. Handle urgent safety stops immediately; otherwise give a provisional reading with explicit assumptions before asking questions.
4. After useful findings, actions, and monitoring, ask at most three missing-input questions that materially change precision or responsible action. Skip known and declined inputs; zero questions is valid. The host must omit declined questions from the final answer because the CLI does not store refusal history.
5. Follow the report sections, but keep the final answer proportional to the user's request.

## Domain Notes

- **Finance**: Native financial constraints and guardrails always come first; use `broad-symbolic-analysis.md` for 观气, 取象, 辨势, and conditional 吉凶.
- **Life/omen**: Use `broad-symbolic-analysis.md` plus symbolic ji/xiong assessment without deterministic fate claims.
- **Space**: Use floor-plan or form evidence before compass formulas.
- **Brand/career/product**: Use five phases as design or strategy lenses, not as proof.
- **Wellbeing**: Prioritize light, air, sleep, ergonomics, and professional care boundaries.

## Common Mistakes

- Do not treat the brief as the final answer.
- Do not load every reference just because the skill has many files.
- Do not ignore guardrails when the symbolic reading feels strong.
- Do not call missing data a conclusion.
- Do not use floor-plan JSON output as a substitute for visual confirmation.
