# Cross-Domain Adapters

Use this file when the user asks for feng shui guidance outside classic spatial analysis: finance, business, brand, career, product, negotiation, learning, health-adjacent wellbeing, relationships, creative work, life choices, auspiciousness, or decision-making.

For any non-spatial reading that centers on 观气, 取象, 辨势, 吉凶, 运势, 生平, or 趋吉避凶, load `broad-symbolic-analysis.md` first, then load the specialized adapter for the native domain.

## Table of Contents

- Core Rule
- Adapter Workflow
- Domain Map
- Translation Lenses
- Output Pattern
- Boundaries

## Core Rule

Feng shui can be used outside architecture as a symbolic decision-support lens, but it must not replace the native discipline. In every cross-domain answer, combine:

1. The domain's real constraints.
2. Feng shui / yin-yang / five-phase / bagua / timing symbolism.
3. Practical next actions.
4. Explicit safety or professional boundaries.

Do not pretend feng shui alone can price assets, diagnose illness, win negotiations, guarantee romance, or predict markets.

## Adapter Workflow

1. Identify the native domain: finance, career, brand, product, wellbeing, relationship, education, life/omen, legal-adjacent, or general decision.
2. Ask what outcome the user wants and what constraints are real.
3. Apply the broad symbolic protocol from `broad-symbolic-analysis.md`: 定域, 观气, 取象, 辨势, 断吉凶, 化解, 复核.
4. Choose a feng shui lens:
   - **Yin-yang**: balance, pace, exposure, risk posture, contraction/expansion.
   - **Five phases**: growth, visibility, stability, precision, liquidity.
   - **Form and flow**: bottlenecks, leakage, support, pathways, friction.
   - **Timing**: preparation, activation, rest, launch, review cycles.
   - **Moon phase rhythm**: hidden seeding, growth, visibility, review, release, pruning, and conservation when the user asks about new moon, full moon, lunar rhythm, timing symbolism, or broad ji/xiong cycles.
   - **Remedies**: low-risk adjustments, environment, process changes, symbolic anchors.
   - **Ji/xiong**: favorable or unfavorable conditions based on support, timing, leakage, and risk.
5. Give domain-first advice and label feng shui symbolism separately.
6. Include guardrails for high-stakes domains.

For deeper common domains, load the specialized adapter:

| Domain | Specialized reference |
| --- | --- |
| Finance | `finance-adapter.md` |
| Business | `business-adapter.md` |
| Brand | `brand-adapter.md` |
| Career | `career-adapter.md` |
| Relationships | `relationship-adapter.md` |
| Product | `product-adapter.md` |
| Learning | `learning-adapter.md` |
| Wellbeing | `wellbeing-adapter.md` |
| Legal-adjacent | `legal-adjacent-adapter.md` |
| Life pattern / omen | `life-and-omen-adapter.md` |

## Domain Map

| Domain | Feng shui translation | Native constraints |
| --- | --- | --- |
| Finance | risk balance, liquidity as water, growth as wood, discipline as metal, timing cycles | valuation, diversification, liquidity, regulation, tax, risk tolerance |
| Business strategy | market flow, bottlenecks, support, timing, resource balance | customers, unit economics, competition, operations |
| Brand/design | five-phase palette, yin-yang tone, visibility, memorability | accessibility, audience research, trademark, usability |
| Career | command position, backing, timing, relationship sectors as metaphor | skills, evidence, network, labor market, negotiation |
| Product | user flow, friction, center of gravity, activation | user research, metrics, technical feasibility |
| Learning | qi flow as attention, yin rest and yang practice, phased review | curriculum, spaced repetition, feedback |
| Wellbeing | sleep, light, air, clutter, rhythm | medical care, ergonomics, mental health support |
| Relationships | balance, privacy, shared space, communication flow | consent, communication, safety, counseling |
| Negotiation | position, backing, timing, channels, leakage | BATNA, facts, incentives, legal terms |
| Life pattern / omen | yin-yang rhythm, five-phase balance, support, leakage, timing | lived facts, choices, health/safety, family/work constraints |

## Moon Phase Across Domains

Use `timing-and-date-selection.md` and `scripts/moon_phase.py` when a non-spatial question asks about New Moon, Full Moon, moon phase, lunar rhythm, timing symbolism, auspiciousness, inauspiciousness, or a cycle of starting, revealing, pruning, and resting.

Moon phase is a secondary symbolic rhythm layer:

| Phase posture | Cross-domain meaning | Example use |
| --- | --- | --- |
| New Moon | hidden beginning, intent, reset, quiet preparation | research before investing, private beta planning, study reset, relationship repair intent |
| Waxing | growth, accumulation, activation | staged product rollout, habit building, pipeline development, gradual negotiation |
| Full Moon | visibility, culmination, illumination, review | public launch, portfolio exposure review, presentation, clear conversation |
| Waning | release, simplification, pruning, leakage repair | reduce risk, declutter commitments, close old tasks, simplify spending |

Do not use moon phase to predict market direction, diagnose a person, guarantee luck, force a launch, or override safety, financial, legal, medical, or operational evidence.

## Translation Lenses

### Yin-Yang

- Too yang: overexposed, overtrading, overlaunching, rushing, public pressure.
- Too yin: hidden, stagnant, undercommunicated, delayed, avoidant.
- Balance through pacing, review cycles, privacy/publicity, rest/action.

### Five Phases

| Phase | Cross-domain meaning | Useful for |
| --- | --- | --- |
| Wood | growth, exploration, pipeline, learning | expansion plans, early ideas, education |
| Fire | visibility, attention, launch, persuasion | marketing, leadership, public moments |
| Earth | stability, trust, process, reserves | savings, governance, operations |
| Metal | discipline, rules, precision, cutting excess | budgeting, compliance, editing |
| Water | liquidity, research, networks, adaptability | finance, discovery, negotiation |

### Form and Flow

Look for:

- Support: who/what backs the decision?
- Ming tang: is there enough open opportunity before action?
- Sha qi: what sharp pressure, deadline, conflict, or hidden risk is aimed at the user?
- Leakage: where do money, attention, time, or trust drain away?
- Stagnation: where is there no movement, feedback, or use?

## Output Pattern

Use this structure:

1. **Domain read**: practical situation and constraints.
2. **Feng shui lens**: symbolic interpretation.
3. **Risks**: what could leak, rush, stagnate, or overheat.
4. **Adjustments**: low-risk actions.
5. **What not to infer**: limits and professional boundary.

## Boundaries

- High-stakes domains require `references/ethics-and-limits.md`.
- Finance questions require `references/finance-adapter.md`.
- Do not use feng shui symbolism to override evidence, law, medicine, safety, or fiduciary duties.
- If the user asks for a yes/no high-stakes decision, provide a decision framework rather than a prediction.
