#!/usr/bin/env python3
"""Generate a Markdown FengShui Master consultation report scaffold."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent


def load_create_brief() -> Any:
    path = SCRIPT_DIR / "create_brief.py"
    spec = importlib.util.spec_from_file_location("create_brief", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


brief_module = load_create_brief()


PROACTIVE_SECTIONS = [
    (
        "Provisional Current Posture",
        "State a concise, useful judgment about the user's current conditions from "
        "the known evidence. Label it provisional and conditional, lower confidence "
        "when input is sparse, and do not explain the method or ask questions here.",
    ),
    (
        "Known Basis",
        "List only supplied observations, deterministic calculations, and explicit "
        "assumptions. Keep unknowns distinct from facts.",
    ),
    (
        "Favorable Now",
        "Identify the conditions that currently support progress, including ordinary "
        "real-world signs the user can recognize.",
    ),
    (
        "Possible Friction and Ordinary Manifestations",
        "Describe only bounded hypotheses about what may be difficult and how each "
        "could appear in everyday behavior or outcomes. Do not use cold reading or "
        "claim hidden events as facts.",
    ),
    (
        "Confirm or Refute Signals",
        "For every material inference, give observable evidence that would strengthen "
        "it and evidence that would weaken or refute it.",
    ),
    (
        "Immediate Low-Risk Action",
        "Give one safe, low-cost, reversible, domain-native action the user can take "
        "now. Reality-based safety and professional constraints override symbolism.",
    ),
    (
        "Prioritized Cross-Domain Concerns",
        "Rank relevant domains by urgency, dependency, evidence, and reversibility. "
        "Explain what to address first; do not average conflicts or give every domain "
        "equal weight.",
    ),
    (
        "Actions: Next 72 Hours",
        "Give the smallest concrete actions that stabilize the situation and produce "
        "useful evidence.",
    ),
    (
        "Actions: Next 30 Days",
        "Give a short execution and review plan tied to the highest-priority concerns.",
    ),
    (
        "Actions: Next 90 Days",
        "Give conditional longer-horizon actions and state when the plan should be "
        "revised rather than extended.",
    ),
    (
        "Monitoring",
        "Name a small set of observable indicators, review dates, and stop conditions "
        "that show whether the situation is improving.",
    ),
]

MAX_FOLLOW_UP_PROMPTS = 3

PROACTIVE_BRIEF_SECTIONS = {
    "Provisional current posture",
    "Known basis and confidence",
    "Favorable conditions",
    "Possible friction and ordinary manifestations",
    "Confirmation and disconfirmation signals",
    "Immediate low-risk action",
    "Cross-domain priorities",
    "Actions: next 72 hours",
    "Actions: next 30 days",
    "Actions: next 90 days",
    "Monitoring signals",
    "Follow-up questions (maximum 3)",
}

MISSING_INPUT_QUESTIONS = {
    "decision type": (
        "What specific decision are you making, and which options are you comparing?"
    ),
    "time horizon": (
        "What is the decision deadline and intended holding or review horizon?"
    ),
    "risk tolerance": (
        "How much loss or volatility can you tolerate without jeopardizing essential goals?"
    ),
    "liquidity needs": (
        "What money must remain liquid for living costs, emergencies, or near-term commitments?"
    ),
    "existing allocation or concentration": (
        "What is your current allocation, including any concentrated positions?"
    ),
    "financial thesis and downside condition": (
        "What evidence supports the financial thesis, and what downside condition would invalidate it?"
    ),
    "native domain": "What real-world domain should lead this analysis?",
    "desired outcome": "What concrete outcome should this analysis support?",
    "real constraints": "What deadlines, budgets, obligations, or other real constraints apply?",
}

# These keys intentionally cover only categories emitted by the router or the
# canonical missing-input labels. Unknown questions continue to use exact-text
# deduplication instead of speculative natural-language matching.
INPUT_QUESTION_CATEGORIES = {
    "decision type": "decision",
    "time horizon": "time_horizon",
    "risk tolerance": "risk_tolerance",
    "liquidity needs": "liquidity",
    "existing allocation or concentration": "allocation",
    "financial thesis and downside condition": "financial_thesis",
    "native domain": "domain",
    "desired outcome": "desired_outcome",
    "real constraints": "constraints",
    "whether spatial, timing, or symbolic analysis is wanted": "analysis_mode",
}

CLARIFYING_QUESTION_CATEGORIES = {
    "what real-world domain and decision should the reading support": {
        "domain",
        "decision",
    },
    "do you want spatial, timing, personal-context, or broad symbolic analysis": {
        "analysis_mode",
    },
    "what concrete outcome, time horizon, and constraints matter most": {
        "desired_outcome",
        "time_horizon",
        "constraints",
    },
}


def heading_for(section: str) -> str:
    if "/" in section:
        return section
    if section.isupper():
        return section
    return section[:1].upper() + section[1:]


def bullet_list(items: list[str]) -> str:
    if not items:
        return "- None supplied.\n"
    return "".join(f"- {item}\n" for item in items)


def ordered_domains(brief: dict[str, Any]) -> list[str]:
    priorities = brief.get("proactive_delivery", {}).get("domain_priorities", {})
    configured = priorities.get("ordered_domains", [])
    if isinstance(configured, list) and configured:
        return [str(value) for value in configured]
    return [str(value) for value in brief.get("domains", [brief["domain"]])]


def normalize_question_text(value: str) -> str:
    return " ".join(value.strip().casefold().rstrip(".?!").split())


def input_question_category(label: str) -> str:
    normalized = normalize_question_text(label)
    return INPUT_QUESTION_CATEGORIES.get(normalized, f"input:{normalized}")


def question_categories(prompt: str) -> set[str]:
    normalized = normalize_question_text(prompt)
    known_categories = CLARIFYING_QUESTION_CATEGORIES.get(normalized)
    if known_categories is not None:
        return set(known_categories)

    if normalized.startswith("which domain should lead the analysis:"):
        return {"domain"}

    for label, question in MISSING_INPUT_QUESTIONS.items():
        if normalized == normalize_question_text(question):
            return {input_question_category(label)}
    return set()


def provided_input_values(brief: dict[str, Any]) -> dict[str, str]:
    input_state = brief.get("input_state", {})
    raw_values = input_state.get("provided_values", {})
    if not isinstance(raw_values, dict):
        return {}
    return {str(label): str(value) for label, value in raw_values.items()}


def provided_input_provenance(brief: dict[str, Any]) -> dict[str, str]:
    input_state = brief.get("input_state", {})
    raw_provenance = input_state.get("provenance", {})
    if not isinstance(raw_provenance, dict):
        return {}
    return {str(label): str(value) for label, value in raw_provenance.items()}


def provided_input_labels(brief: dict[str, Any]) -> list[str]:
    input_state = brief.get("input_state", {})
    raw_provided = input_state.get("provided", [])
    labels: list[str] = []
    if isinstance(raw_provided, dict):
        labels.extend(str(label) for label in raw_provided)
    elif isinstance(raw_provided, list):
        labels.extend(str(label) for label in raw_provided)

    for label in provided_input_values(brief):
        if normalize_question_text(label) not in {
            normalize_question_text(value) for value in labels
        }:
            labels.append(label)
    return labels


def render_known_basis(brief: dict[str, Any]) -> list[str]:
    domains = ", ".join(ordered_domains(brief))
    provided = provided_input_labels(brief)
    values = {
        normalize_question_text(label): value
        for label, value in provided_input_values(brief).items()
    }
    provenance = provided_input_provenance(brief)
    provided_values_source = provenance.get("provided_values")
    lines = [
        f"- User-supplied question: {brief['question']}",
        f"- Routed domain priority: {domains or brief['domain']}",
    ]
    if provided:
        lines.append("- Explicitly provided inputs:")
        for label in provided:
            value = values.get(normalize_question_text(label))
            if value is None:
                lines.append(
                    f"  - {label} (source: user-supplied; value not captured)"
                )
            else:
                source = (
                    provided_values_source
                    or "user-supplied; not independently verified"
                )
                lines.append(
                    f"  - {label}: {value} "
                    f"(source: {source})"
                )
    else:
        lines.append(
            "- Explicit structured inputs: none beyond the question; keep the reading low-confidence and provisional."
        )
    return lines


def render_domain_priorities(brief: dict[str, Any]) -> list[str]:
    domains = ordered_domains(brief)
    return [
        f"- Priority {index}: {domain}"
        for index, domain in enumerate(domains, start=1)
    ]


def prioritized_missing_inputs(brief: dict[str, Any]) -> list[str]:
    missing = [str(value) for value in brief.get("missing_inputs", [])]
    configured_by_domain = getattr(brief_module, "DOMAIN_MISSING_INPUTS", {})
    prioritized: list[str] = []
    for domain in ordered_domains(brief):
        for value in configured_by_domain.get(domain, []):
            if value in missing and value not in prioritized:
                prioritized.append(value)
    return [*prioritized, *(value for value in missing if value not in prioritized)]


def prioritized_high_risk_inputs(
    brief: dict[str, Any], missing: list[str]
) -> list[str]:
    proactive = brief.get("proactive_delivery", {})
    stop_conditions = proactive.get("stop_conditions", [])
    essential_by_domain: dict[str, list[str]] = {}
    if isinstance(stop_conditions, list):
        for condition in stop_conditions:
            if not isinstance(condition, dict):
                continue
            if condition.get("id") != "missing_high_stakes_evidence":
                continue
            evidence = condition.get("missing_essential_evidence", {})
            if not isinstance(evidence, dict):
                continue
            for domain, values in evidence.items():
                if not isinstance(values, list):
                    continue
                essential_by_domain.setdefault(str(domain), []).extend(
                    str(value) for value in values
                )

    missing_by_key = {normalize_question_text(value): value for value in missing}
    ordered: list[str] = []
    domains = [*ordered_domains(brief), *essential_by_domain]
    for domain in domains:
        for value in essential_by_domain.get(domain, []):
            canonical = missing_by_key.get(normalize_question_text(value))
            if canonical is not None and canonical not in ordered:
                ordered.append(canonical)
    return ordered


def phrase_missing_input(value: str) -> str:
    normalized = value.strip().rstrip(".?!")
    if normalized in MISSING_INPUT_QUESTIONS:
        return MISSING_INPUT_QUESTIONS[normalized]
    if normalized.casefold().startswith("whether "):
        return f"Should the analysis account for {normalized[8:]}?"
    return f"What should the analysis assume about {normalized}?"


def follow_up_prompts(brief: dict[str, Any]) -> list[str]:
    if not brief.get("symbolic_analysis_allowed", True):
        return []
    configured_max = brief.get("proactive_delivery", {}).get(
        "max_follow_up_questions", MAX_FOLLOW_UP_PROMPTS
    )
    try:
        question_budget = min(MAX_FOLLOW_UP_PROMPTS, max(0, int(configured_max)))
    except (TypeError, ValueError):
        question_budget = MAX_FOLLOW_UP_PROMPTS
    if question_budget == 0:
        return []

    clarifying_questions = [
        str(value) for value in brief.get("clarifying_questions", [])
    ]
    if len(ordered_domains(brief)) > 1:
        clarifying_questions = [
            value
            for value in clarifying_questions
            if not normalize_question_text(value).startswith(
                "which domain should lead the analysis:"
            )
        ]

    provided_labels = provided_input_labels(brief)
    provided_categories = {
        input_question_category(label) for label in provided_labels
    }
    missing = [str(value) for value in brief.get("missing_inputs", [])]
    missing = [
        value
        for value in missing
        if normalize_question_text(value)
        not in {normalize_question_text(label) for label in provided_labels}
    ]
    high_risk_inputs = prioritized_high_risk_inputs(brief, missing)
    regular_missing_inputs = prioritized_missing_inputs(brief)
    missing_candidates: list[str] = []
    seen_missing: set[str] = set()
    for value in [*high_risk_inputs, *regular_missing_inputs]:
        value_key = normalize_question_text(value)
        if value_key in seen_missing or value_key not in {
            normalize_question_text(item) for item in missing
        }:
            continue
        seen_missing.add(value_key)
        missing_candidates.append(value)

    prompts: list[str] = []
    selected_categories: set[str] = set()
    seen_prompts: set[str] = set()
    candidates = [
        *((phrase_missing_input(value), {input_question_category(value)})
          for value in high_risk_inputs),
        *((value, question_categories(value)) for value in clarifying_questions),
        *((phrase_missing_input(value), {input_question_category(value)})
          for value in missing_candidates
          if value not in high_risk_inputs),
    ]
    for candidate, categories in candidates:
        prompt = candidate.strip()
        if not prompt:
            continue
        if prompt[-1] not in "?!":
            prompt = f"{prompt}?"
        prompt_key = normalize_question_text(prompt)
        if prompt_key in seen_prompts:
            continue
        if categories and categories & provided_categories:
            continue
        if categories and categories & selected_categories:
            continue
        prompts.append(prompt)
        seen_prompts.add(prompt_key)
        selected_categories.update(categories)
        if len(prompts) == question_budget:
            break
    return prompts


def render_emergency_response(brief: dict[str, Any]) -> list[str]:
    question = str(brief.get("question", "")).casefold()
    medical_emergency = any(
        phrase in question
        for phrase in ("chest pain", "trouble breathing", "difficulty breathing")
    )
    if medical_emergency:
        guidance = (
            "Chest pain or trouble breathing may be a medical emergency. Contact "
            "local emergency services now. Do not delay for feng shui analysis, "
            "additional questions, or changes to the room. Feng shui cannot diagnose "
            "these symptoms or determine their cause."
        )
    else:
        guidance = (
            "This may be an urgent real-world safety issue. Contact the appropriate "
            "local emergency or qualified professional service now. Do not delay for "
            "feng shui analysis or additional questions. Feng shui cannot establish "
            "safety or replace qualified professional judgment."
        )
    return [
        "## Provisional Current Posture",
        "",
        guidance,
        "",
        "## Cultural and Professional Boundary",
        "",
        "Symbolic analysis stops here until the urgent concern has been addressed.",
        "",
    ]


def render_proactive_sections(brief: dict[str, Any]) -> list[str]:
    lines: list[str] = []

    for heading, instruction in PROACTIVE_SECTIONS:
        lines.extend([f"## {heading}", ""])
        if heading == "Known Basis":
            lines.extend(render_known_basis(brief))
            lines.append("")
            lines.append(instruction)
        elif heading == "Prioritized Cross-Domain Concerns":
            lines.extend(render_domain_priorities(brief))
            lines.append("")
            lines.append(instruction)
        else:
            lines.append(instruction)
        lines.append("")

    lines.extend(["## Follow-Up Prompts (Maximum 3)", ""])
    prompts = follow_up_prompts(brief)
    if prompts:
        lines.extend(f"- {prompt}" for prompt in prompts)
    else:
        lines.append("- No follow-up prompt is required before a useful reading.")
    lines.extend(
        [
            "",
            "Ask these only after delivering the provisional reading. Do not add more than three follow-up prompts.",
            "",
        ]
    )
    return lines


def render_floorplan_analysis(analysis: dict[str, Any] | None) -> str:
    if not analysis:
        return ""

    lines = ["## Structured Floor-Plan Analysis", ""]
    if not analysis.get("valid"):
        lines.append("The structured floor-plan input is invalid.")
        for error in analysis.get("errors", []):
            lines.append(f"- {error}")
        lines.append("")
        return "\n".join(lines)

    input_data = analysis.get("input", {})
    lines.extend(
        [
            f"- Name: {input_data.get('name')}",
            f"- Type: {input_data.get('type')}",
            f"- Facing degrees: {input_data.get('facing_degrees')}",
            f"- North degrees: {input_data.get('north_degrees')}",
            "",
            "### Findings",
        ]
    )
    findings = analysis.get("findings", {})
    for category, values in findings.items():
        if values:
            lines.append(f"- {category}:")
            for value in values:
                lines.append(f"  - {value}")

    lines.extend(["", "### Issues"])
    issues = analysis.get("issues", [])
    if issues:
        for issue in issues:
            lines.append(
                f"- {issue.get('code')} ({issue.get('severity')}): {issue.get('message')}"
            )
    else:
        lines.append("- No structured issues detected.")

    lines.extend(["", "### Recommendations"])
    for recommendation in analysis.get("recommendations", []):
        lines.append(
            f"- {recommendation.get('priority')}: {recommendation.get('action')}"
        )

    lines.extend(["", f"Method note: {analysis.get('method_note')}", ""])
    return "\n".join(lines)


def generate_report(
    question: str,
    floorplan_path: str | None = None,
    known_inputs: dict[str, str] | None = None,
) -> str:
    if known_inputs is None:
        brief = brief_module.create_brief(question, floorplan_path)
    else:
        brief = brief_module.create_brief(
            question, floorplan_path, known_inputs=known_inputs
        )
    lines = [
        "# FengShui Master Consultation Report",
        "",
        f"Question: {brief['question']}",
        f"Domain: {brief['domain']}",
        "",
    ]
    if not brief.get("symbolic_analysis_allowed", True):
        lines.extend(render_emergency_response(brief))
        return "\n".join(lines)
    lines.extend(render_proactive_sections(brief))

    lines.extend(
        [
            "## Supporting Method and Boundaries",
            "",
            "## References To Load",
            bullet_list(brief["references"]).rstrip(),
            "",
            "## Guardrails",
            bullet_list(brief["guardrails"]).rstrip(),
            "",
            "## Symbolic Lenses",
            bullet_list(brief["lenses"]).rstrip(),
            "",
            "## Answer Contract",
            bullet_list(brief["answer_contract"]).rstrip(),
            "",
        ]
    )

    floorplan_section = render_floorplan_analysis(brief.get("floorplan_analysis"))
    if floorplan_section:
        lines.append(floorplan_section.rstrip())
        lines.append("")

    lines.append("## Report Sections")
    lines.append("")
    for section in brief["report_sections"]:
        if section.casefold() in {
            proactive_section.casefold()
            for proactive_section in PROACTIVE_BRIEF_SECTIONS
        }:
            continue
        lines.append(f"## {heading_for(section)}")
        lines.append("")
        lines.append(
            "Draft this section from supplied evidence. Separate observation, traditional interpretation, and practical action."
        )
        lines.append("")

    lines.append("## Cultural and Professional Boundary")
    lines.append("")
    lines.append(
        "This report is a cultural and symbolic decision-support scaffold. It is not medical, legal, financial, engineering, architectural, tax, psychological, or safety advice."
    )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown FengShui Master consultation report scaffold."
    )
    parser.add_argument("question", help="User question or consultation goal.")
    parser.add_argument("--floorplan", help="Optional structured floor-plan JSON path.")
    parser.add_argument(
        "--known-inputs", help="Optional JSON object of canonical input labels to values."
    )
    parser.add_argument("--output", help="Optional output Markdown path.")
    args = parser.parse_args()

    known_inputs = None
    if args.known_inputs is not None:
        try:
            known_inputs = json.loads(
                Path(args.known_inputs).read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as error:
            parser.error(f"could not read --known-inputs JSON: {error}")
        if not isinstance(known_inputs, dict):
            parser.error("--known-inputs must contain a JSON object")

    try:
        if known_inputs is None:
            report = generate_report(args.question, args.floorplan)
        else:
            report = generate_report(args.question, args.floorplan, known_inputs)
    except (TypeError, ValueError) as error:
        parser.error(str(error))
    if args.output:
        output = Path(args.output)
        output.write_text(report, encoding="utf-8")
        print(output)
    else:
        print(report)


if __name__ == "__main__":
    main()
