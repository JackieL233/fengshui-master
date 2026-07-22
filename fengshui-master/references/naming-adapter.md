# Naming Adapter

Use this file for personal names, baby names, adult renaming, courtesy or generation names, pen names, stage names, pseudonyms, brands, companies, products, shops, domains, and other naming decisions that request feng shui, wuxing, yin-yang, auspiciousness, birth context, or timing symbolism.

## Table of Contents

- Core Rule
- Naming Type
- Intake
- Context Fusion
- Five-Phase Naming Lens
- Candidate Review
- Personal Names
- Commercial Names
- Output Pattern
- Forbidden Claims

## Core Rule

Treat naming as a multilayer decision. Combine native naming quality, supplied personal or business context, language and culture, legal and technical constraints, and clearly labeled symbolic interpretation. Never let one stroke count, radical, sound, element label, birth-year scaffold, or lucky date decide the result alone.

Do not infer that a person "lacks" an element from a Gregorian birth year, ming gua, zodiac, approximate solar term, or moon phase. A complete bazi balance claim requires a trusted chart engine or lineage source under `examples/external-calculation-contracts.json`.

## Naming Type

Classify before analysis:

| Type | Native priority |
| --- | --- |
| Personal or baby name | surname fit, meaning, pronunciation, family values, identity, registration usability |
| Adult rename | current identity, social continuity, reason for change, administrative burden |
| Generation or courtesy name | family convention, generation character, lineage and cultural context |
| Pen, stage, or creator name | memorability, audience, voice, discoverability, channel fit |
| Brand, company, shop, or product | audience, positioning, category, trademark, domain, conversion and accessibility |

## Intake

Ask only for relevant fields:

- Name type and purpose.
- Surname, fixed characters, generation character, or words that must remain.
- Candidate names, or permission to generate directions rather than final names.
- Language, script, pronunciation, tones, dialect, transliteration, and target region.
- Desired meanings, associations, impression, gender expression, and cultural boundaries.
- Avoided characters, sounds, homophones, family names, taboos, or negative associations.
- For personal names: optional birth details and a `scripts/personal_context.py` result.
- For commercial names: audience, category, positioning, competitors, trademark/domain constraints, and channels.
- Whether the user explicitly wants a named stroke-count, five-grid, phonetic-element, radical-element, bazi, or lineage method.

Do not request identity documents, account credentials, or unnecessary private records.

## Context Fusion

Use available information in this priority order:

1. Safety, law, registration, trademark, accessibility, and platform constraints.
2. Native naming evidence: meaning, pronunciation, ambiguity, memorability, cultural and dialect fit.
3. Verified deterministic context with provenance: supplied personal context, dates, business category, audience, or spatial use.
4. Named traditional or lineage method with its inputs and limitations.
5. Modern wuxing, yin-yang, timing, and feng shui symbolism.
6. Aesthetic preference and reversible experimentation.

When layers disagree, show the disagreement. Do not average them into a fake precise score. A legally usable, meaningful, pronounceable name outranks a symbolic elemental preference.

## Five-Phase Naming Lens

Use five phases as relational symbolism:

| Phase | Naming impression | Common risk |
| --- | --- | --- |
| Wood | growth, learning, direction, vitality | scattered or overly ambitious |
| Fire | visibility, warmth, charisma, speed | hype, harshness, overexposure |
| Earth | trust, stability, care, continuity | heaviness or dullness |
| Metal | precision, clarity, discipline, premium restraint | coldness or rigidity |
| Water | depth, adaptability, intelligence, connection | vagueness or weak anchoring |

State how the phase was assigned. Character radical, semantic image, pronunciation, stroke system, and lineage tables can disagree. Do not silently combine them or call one universal.

## Candidate Review

Review each candidate across separate dimensions:

| Dimension | Check |
| --- | --- |
| Meaning | literal meaning, compound meaning, historical and contemporary associations |
| Sound | rhythm, tones, surname flow, common mispronunciation, dialect and homophones |
| Form | legibility, handwriting, visual balance, rare characters, input-method and font support |
| Identity | age fit, gender expression, family fit, dignity, unwanted stereotypes |
| Practical use | registration, trademark, domain, searchability, social handles, international use |
| Symbolic fit | named wuxing/yin-yang method, desired posture, personal or brand context |
| Risk | ambiguity, ridicule, cultural misuse, false promises, deterministic claims |

Use qualitative ratings such as strong, mixed, or weak with reasons. Do not present arbitrary numerology as scientific measurement.

## Personal Names

When birth data is supplied:

1. Run `scripts/personal_context.py` for bounded context.
2. Separate year-ganzhi, ming-gua, period, solar-term, and moon-phase scaffolds.
3. Do not infer month/day/hour pillars or a missing element.
4. Use the context to discuss symbolic posture, not destiny repair.
5. Keep family meaning, pronunciation, identity, and registration usability primary.

If the user supplies a trusted full chart, record its source, timezone, calendar conversion, and lineage before applying any balancing theory.

## Commercial Names

Load `brand-adapter.md` for brands, companies, shops, products, campaigns, or apps. Check audience, category, trademark, domain, accessibility, searchability, and conversion evidence before wuxing symbolism. A name cannot guarantee revenue, virality, funding, or business survival.

## Output Pattern

1. **Provisional naming posture**: narrow conditional headline on what currently looks strong, mixed, or weak.
2. **Known basis**: naming type, fixed characters, candidates, audience/person, language, constraints, and confidence.
3. **Favorable qualities and possible friction**: meaning, sound, form, cultural/practical fit, and ordinary use problems.
4. **Confirm or refute**: registration, trademark, dialect, accessibility, search, and user-testing evidence.
5. **Immediate action and priorities**: one reversible next step and ranked decision criteria.
6. **Candidate comparison and symbolic layer**: strengths, conflicts, named wuxing method, and uncertainty.
7. **Monitoring and follow-up**: test results and at most three precision questions.
8. **Method and boundaries**: context provenance, missing precision, and no guaranteed fate or business outcome.

## Forbidden Claims

Do not claim:

- A name guarantees luck, wealth, health, marriage, fertility, status, exam success, revenue, or protection.
- A character necessarily belongs to one element across all naming systems.
- A birth-year, zodiac, ming gua, moon phase, or approximate solar term proves an element deficiency.
- Stroke count or five-grid numerology is objective science or a complete fate calculation.
- Renaming can replace medical, legal, financial, psychological, educational, or business action.
