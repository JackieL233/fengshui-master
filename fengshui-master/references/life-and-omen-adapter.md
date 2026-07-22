# Life and Omen Adapter

Use this file when the user asks to apply feng shui, wuxing, bagua, yin-yang, stems/branches, auspiciousness, inauspiciousness, luck, life pattern, personal phase, destiny-adjacent interpretation, or broad Chinese symbolic reasoning to a person, event, decision, year, period, career path, relationship pattern, or life story.

For the general 观气 / 取象 / 辨势 / 吉凶 protocol, load `broad-symbolic-analysis.md` first. Load `proactive-reading-protocol.md` for current-state scans, favorable and friction hypotheses, validation evidence, and action horizons. Use this file for the life, omen, and personal-pattern specialization.

## Table of Contents

- Core Rule
- Intake
- Method Stack
- Life Reading Pattern
- Auspiciousness Pattern
- Five-Phase Personal Lens
- Event and Decision Lens
- Output Pattern
- Proactive Current-State Reading
- Forbidden Claims

## Core Rule

Treat broad feng shui as a traditional symbolic language for reading qi, form, timing, relationship, tendency, and balance. Do not present it as deterministic fate, medical diagnosis, guaranteed prediction, or a complete bazi / zi wei / qimen / liuren engine.

When the user asks about a life, fortune, or omen, answer in layers:

1. Bounded provisional current-posture headline.
2. Real-world facts, constraints, assumptions, and confidence.
3. Favorable conditions plus conditional friction and ordinary manifestations.
4. Evidence that would confirm or refute the inferred pattern.
5. Low-risk actions for "趋吉避凶" (seek favorable conditions and reduce avoidable harm), action horizons, and monitoring.
6. At most three follow-up questions, then concise method and boundary notes.

## Intake

Ask only for what matters to the requested depth:

- Topic: life overview, career, wealth, relationship, health-adjacent environment, year luck, event omen, decision, name/brand, move, opening, negotiation, or investment.
- Available inputs: birth year, gender/sex convention for ming gua if requested, birth date/time only if the user wants broader astrology-like discussion, current age/stage, location/time zone, important dates, floor plan or workspace if environment matters.
- Goal: understand pattern, choose timing, reduce risk, improve environment, compare options, or make a practical plan.
- Constraints: budget, health/safety needs, legal/financial obligations, family constraints, what cannot change.

Do not ask for sensitive identifiers, exact private records, account details, or medical records.

After essential safety-critical inputs are known, proceed with a provisional reading even when optional context is missing. Ask no more than three high-impact validation questions; do not replace the reading with an intake questionnaire.

## Method Stack

Use the lightest adequate method:

| User asks for | Use |
| --- | --- |
| "What does this phase of life feel like?" | yin-yang, five phases, timing cycles, current constraints |
| "Analyze my life using feng shui" | run `scripts/personal_context.py` when birth data and an analysis date are available; disclose that full bazi is not implemented |
| "Is this auspicious?" | auspiciousness pattern: support, timing, balance, leakage, sha, reversibility |
| "What element am I missing?" | five-phase personal lens; do not reduce a person to one element |
| "Which career/industry fits?" | five-phase domain map plus skills, market, evidence, and preferences |
| "Will I get rich / sick / divorced?" | refuse deterministic prediction; reframe to risk, support, and actions |
| "Use feng shui for finance" | `finance-adapter.md` first, then this file if life/luck symbolism is requested |

Use `scripts/ganzhi.py <year>` when a year stem/branch, zodiac, or annual five-phase scaffold would help. It only returns a Gregorian-year scaffold, so confirm li chun or lunar-year boundaries for birth-year or annual-luck questions near year transitions.

Use `scripts/personal_context.py` when the user supplies birth details and asks about current luck, a personal phase, or a one-to-two-year outlook. Read its output in this order: supplied inputs, birth-year/ming-gua scaffolds, current timing layers, real-world constraints, conditional ji/xiong, then reversible actions. Do not derive missing pillars from the output.

## Life Reading Pattern

Read a person through patterns, not fixed destiny:

- **Yin-yang rhythm**: Is the life pattern overexposed and rushed, or hidden and stagnant? Does the person need action, rest, visibility, privacy, discipline, or flow?
- **Five-phase balance**: Which phase is dominant in behavior, work, environment, or timing? Which phase could support balance?
- **Backing and ming tang**: What support exists behind the person, and what open opportunity lies in front?
- **Leakage**: Where do energy, money, attention, reputation, or trust drain away?
- **Sha pressure**: Which sharp pressures are aimed at the person: debt, deadlines, conflict, clutter, overwork, public scrutiny, legal risk, or health stress?
- **Timing**: Is the moment suited for preparation, activation, consolidation, correction, or rest?

Keep the reading useful: convert symbolism into a practical next step.

## Auspiciousness Pattern

Use "吉/凶" as a conditional reading, not a verdict.

| Traditional term | Practical translation | Response posture |
| --- | --- | --- |
| ji / auspicious | supported, timely, balanced, low-friction, enough backing | "favorable if these conditions hold" |
| xiong / inauspicious | exposed, rushed, leaking, unsupported, conflicted, unsafe | "risk is elevated; reduce or delay if possible" |
| ban ji ban xiong / mixed | benefits and risks are both visible | "split the decision and add controls" |
| hua jie / remedy | reduce pressure, add support, change timing, simplify path | "use low-risk adjustments first" |

Do not call a person, birth, home, name, illness, relationship, or investment "doomed."

## Five-Phase Personal Lens

Use phases as behavioral and situational tendencies:

| Phase | Personal expression | Shadow when excessive | Balancing support |
| --- | --- | --- | --- |
| Wood | growth, learning, planning, initiative | impatience, overexpansion, rigidity of ambition | water research, metal boundaries, earth pacing |
| Fire | visibility, charisma, joy, launch energy | impulsiveness, drama, burnout, speculation | water cooling, earth routine, metal rules |
| Earth | trust, care, stability, responsibility | stagnation, worry, overburdening, inertia | wood movement, metal simplification |
| Metal | standards, discipline, precision, justice | harshness, perfectionism, isolation | fire warmth, water flexibility |
| Water | wisdom, research, networks, adaptability | fear, secrecy, indecision, drift | earth grounding, wood direction |

Do not say a person "is" only one phase. Say a situation, habit, environment, or decision is showing a phase pattern.

## Event and Decision Lens

For events, launches, negotiations, purchases, moves, investments, or relationship choices, inspect:

- **Support**: people, cash, documents, preparation, physical backing.
- **Timing**: whether the action is premature, stale, well-prepared, or overdue.
- **Flow**: whether resources and communication can move without blockage.
- **Containment**: whether gains are kept or leak away through fees, conflict, waste, or distraction.
- **Exposure**: whether attention is helpful fire or harmful overheat.
- **Reversibility**: whether the decision can be tested before full commitment.

## Output Pattern

Use this structure for substantial non-spatial life/omen readings:

1. **Provisional current posture**: narrow conditional headline before questions.
2. **Known basis**: concrete facts, constraints, assumptions, confidence, and unknowns.
3. **Favorable and friction scan**: likely ordinary manifestations and confirm/refute evidence.
4. **Immediate action and priorities**: practical first, symbolic second, ranked by safety and reversibility.
5. **Action horizons and monitoring**: 72 hours, 30 days, 90 days, review signals, and stop conditions.
6. **Follow-up questions**: at most three precision questions.
7. **Method and limits**: named traditional layer and what is not being calculated.

## Proactive Current-State Reading

For current luck, recent conditions, or a one-to-two-year outlook, use the five evidence labels in `proactive-reading-protocol.md`: `observed`, `calculated`, `inferred`, `unknown`, and `recommended`.

Scan only relevant areas among timing posture, career/learning, finance/resources, relationships/support, wellbeing/environment, and decision load. For each scanned area include favorable signals, possible friction, how it may manifest, what would confirm or refute it, and one immediate low-risk action. Finish with actions for the next 72 hours, 30 days, and 90 days plus observable review signals.

Possible difficulties are hypotheses, not discovered facts. Say "this may show up as scattered effort; check whether that is present" rather than "you are currently failing because your energy is scattered."

## Forbidden Claims

Do not claim:

- Guaranteed wealth, illness, marriage, divorce, pregnancy, promotion, disaster, death, or market movement.
- A complete bazi, zi wei, qimen, liuren, or almanac result unless a real engine/source is present.
- That a feng shui reading overrides medical, legal, financial, psychological, engineering, or safety advice.
- That a person is unlucky, cursed, doomed, or inherently harmful.
- That an unreported conflict, loss, illness, betrayal, dismissal, or hidden person is currently present.

Allowed:

- "Traditionally this pattern is read as more favorable when support and timing are present."
- "The symbolic risk is leakage: money/attention may drain unless you add rules."
- "Use this as a reflection and planning lens, not a deterministic prediction."
