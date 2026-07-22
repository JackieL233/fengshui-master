#!/usr/bin/env python3
"""Create a FengShui Master consultation brief from a question."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent


def load_script_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


domain_router = load_script_module("domain_router", SCRIPT_DIR / "domain_router.py")
floorplan_analyzer = load_script_module("analyze_floorplan", SCRIPT_DIR / "analyze_floorplan.py")


DOMAIN_MISSING_INPUTS = {
    "finance": [
        "decision type",
        "time horizon",
        "risk tolerance",
        "liquidity needs",
        "existing allocation or concentration",
        "financial thesis and downside condition",
    ],
    "life_omen": [
        "topic area",
        "birth year or relevant year",
        "current life stage",
        "goal for the reading",
        "hard real-world constraints",
    ],
    "naming": [
        "name type: personal, baby, adult rename, pen/stage, brand, company, or product",
        "surname, fixed characters, generation character, or required words",
        "candidate names or permission to generate naming directions",
        "language, pronunciation, dialect, transliteration, and target region",
        "desired meaning, impression, identity, and avoided associations",
        "registration, trademark, domain, accessibility, or platform constraints",
        "requested wuxing, stroke, bazi, phonetic, or lineage method",
    ],
    "space": [
        "floor plan or photos",
        "north arrow or compass bearing",
        "main door and facing convention",
        "occupant goals",
        "changes that are allowed or forbidden",
    ],
    "timing": [
        "candidate date or date range",
        "event type",
        "local time zone or location",
        "hard deadlines and practical constraints",
        "whether the user wants moon phase, solar terms, almanac attributes, annual cautions, or lineage-specific date selection",
    ],
    "brand": [
        "audience",
        "brand goal",
        "market constraints",
        "accessibility requirements",
        "legal or trademark constraints",
    ],
    "business": [
        "business model and stage",
        "main business goal",
        "customer path or sales funnel",
        "budget, runway, staffing, and regulatory constraints",
        "current bottleneck or leakage",
    ],
    "product": [
        "product type and target user",
        "main product goal or metric",
        "user journey or funnel",
        "current friction, drop-off, or confusion",
        "engineering, accessibility, privacy, and platform constraints",
    ],
    "career": [
        "career goal",
        "current role and constraints",
        "skills and evidence",
        "timing window",
        "workspace or environment context if relevant",
    ],
    "relationship": [
        "relationship type",
        "goal for the reading",
        "safety or coercion concerns",
        "shared-space context",
        "communication constraints and boundaries",
    ],
    "learning": [
        "subject, level, and deadline",
        "learning goal",
        "current schedule and bottleneck",
        "study environment and distraction context",
        "feedback or practice-test data",
    ],
    "wellbeing": [
        "specific wellbeing concern",
        "sleep, light, air, noise, and ergonomic context",
        "medical or safety issues already identified",
        "professional care constraints",
    ],
    "legal_adjacent": [
        "decision type",
        "hard deadlines and required procedures",
        "stakeholders and incentives",
        "documents or clauses the user can summarize",
        "whether qualified legal help is involved",
    ],
    "general": [
        "native domain",
        "desired outcome",
        "real constraints",
        "whether spatial, timing, or symbolic analysis is wanted",
    ],
}


DOMAIN_SECTIONS = {
    "finance": [
        "Inputs and assumptions",
        "Financial reality check",
        "Risk posture",
        "Feng shui symbolic layer",
        "Practical adjustments",
        "Boundaries and missing data",
    ],
    "life_omen": [
        "Inputs and assumptions",
        "Reality layer",
        "Traditional symbolic layer",
        "Ji/xiong assessment",
        "Actions for seeking favorable conditions",
        "Limits and missing data",
    ],
    "naming": [
        "Inputs and naming type",
        "Native naming constraints",
        "Meaning, sound, form, and cultural review",
        "Available personal or business context",
        "Five-phase symbolic fit",
        "Candidate comparison and conflicts",
        "Verification and boundaries",
    ],
    "space": [
        "Inputs and assumptions",
        "Method",
        "Structured floor-plan findings",
        "Form and flow reading",
        "Recommendations",
        "Missing data",
    ],
    "timing": [
        "Inputs and assumptions",
        "Practical timing constraints",
        "Solar term seasonal qi layer",
        "Moon phase symbolic layer",
        "Traditional date-selection layer",
        "Ji/xiong assessment",
        "Low-risk timing advice",
        "Boundaries and missing data",
    ],
    "brand": [
        "Inputs and assumptions",
        "Audience and domain constraints",
        "Five-phase design lens",
        "Risk and accessibility checks",
        "Recommendations",
        "Missing data",
    ],
    "business": [
        "Inputs and assumptions",
        "Business reality layer",
        "Flow and leakage diagnosis",
        "Feng shui symbolic layer",
        "Operational adjustments",
        "Boundaries and missing data",
    ],
    "product": [
        "Inputs and assumptions",
        "Product reality layer",
        "Flow and leakage diagnosis",
        "Feng shui symbolic layer",
        "Product adjustments",
        "Boundaries and missing data",
    ],
    "career": [
        "Inputs and assumptions",
        "Career reality layer",
        "Feng shui and five-phase lens",
        "Timing and support",
        "Practical next actions",
        "Missing data",
    ],
    "relationship": [
        "Inputs and assumptions",
        "Relationship reality and safety",
        "Environment and communication flow",
        "Feng shui symbolic layer",
        "Low-risk adjustments",
        "Boundaries and missing data",
    ],
    "learning": [
        "Inputs and assumptions",
        "Learning reality layer",
        "Environment and attention flow",
        "Five-phase study balance",
        "Practical learning plan",
        "Boundaries and missing data",
    ],
    "wellbeing": [
        "Inputs and assumptions",
        "Wellbeing reality layer",
        "Environment and rhythm lens",
        "Risk checks",
        "Low-risk adjustments",
        "Medical and safety boundaries",
    ],
    "legal_adjacent": [
        "Inputs and assumptions",
        "Legal reality first",
        "Risk map",
        "Feng shui symbolic layer",
        "Preparation actions",
        "Legal boundary and missing data",
    ],
    "general": [
        "Inputs and assumptions",
        "Domain read",
        "Feng shui symbolic layer",
        "Risks and guardrails",
        "Practical adjustments",
        "Missing data",
    ],
}


PROACTIVE_OPENING_SECTIONS = [
    "Provisional current posture",
    "Known basis and confidence",
    "Favorable conditions",
    "Possible friction and ordinary manifestations",
    "Confirmation and disconfirmation signals",
    "Immediate low-risk action",
    "Cross-domain priorities",
]


PROACTIVE_CLOSING_SECTIONS = [
    "Actions: next 72 hours",
    "Actions: next 30 days",
    "Actions: next 90 days",
    "Monitoring signals",
    "Follow-up questions (maximum 3)",
]


PROACTIVE_REQUIRED_SEQUENCE = [
    "safety_precheck",
    "provisional_current_posture",
    "known_basis",
    "favorable_conditions",
    "possible_friction_and_ordinary_manifestations",
    "confirmation_and_disconfirmation_signals",
    "immediate_low_risk_action",
    "cross_domain_priorities",
    "actions_72_hours",
    "actions_30_days",
    "actions_90_days",
    "monitoring_signals",
    "follow_up_questions",
]


MAX_FOLLOW_UP_QUESTIONS = 3

DOMAIN_PRIORITY_TIERS = {
    "business": 1,
    "product": 1,
    "space": 1,
    "career": 1,
    "learning": 1,
    "relationship": 1,
    "timing": 2,
    "life_omen": 2,
    "general": 2,
    "brand": 3,
    "naming": 3,
}


HIGH_STAKES_ESSENTIAL_INPUTS = {
    "finance": [
        "time horizon",
        "risk tolerance",
        "liquidity needs",
        "existing allocation or concentration",
        "financial thesis and downside condition",
    ],
    "legal_adjacent": [
        "hard deadlines and required procedures",
        "stakeholders and incentives",
        "documents or clauses the user can summarize",
        "whether qualified legal help is involved",
    ],
    "wellbeing": [
        "specific wellbeing concern",
        "medical or safety issues already identified",
        "professional care constraints",
    ],
}


HIGH_STAKES_ACTION_TERMS = {
    "finance": [
        "buy",
        "sell",
        "invest",
        "allocate",
        "rebalance",
        "increase",
        "reduce",
        "hold",
        "borrow",
        "withdraw",
        "买",
        "买入",
        "卖",
        "卖出",
        "投资",
        "加仓",
        "减仓",
        "清仓",
        "调仓",
        "持有",
        "借款",
        "赎回",
    ],
    "legal_adjacent": [
        "sign",
        "file",
        "submit",
        "accept",
        "reject",
        "settle",
        "sue",
        "appeal",
        "terminate",
        "waive",
        "签",
        "签署",
        "提交",
        "备案",
        "接受",
        "拒绝",
        "和解",
        "起诉",
        "上诉",
        "终止",
        "放弃",
    ],
    "wellbeing": [
        "start",
        "stop",
        "take",
        "skip",
        "change",
        "replace",
        "increase",
        "reduce",
        "开始",
        "停止",
        "停用",
        "服用",
        "不用",
        "更换",
        "增加",
        "减少",
    ],
}


def has_high_stakes_action_intent(question: str, domain: str) -> bool:
    terms = HIGH_STAKES_ACTION_TERMS.get(domain, [])
    english_terms = [term for term in terms if term.isascii()]
    chinese_terms = [term for term in terms if not term.isascii()]
    lowered = question.casefold()

    if english_terms:
        verbs = "|".join(re.escape(term) for term in english_terms)
        english_patterns = [
            rf"\b(?:should|can|may|must|do)\s+(?:i|we)\b.{{0,80}}\b(?:{verbs})\b",
            rf"\b(?:i|we)\s+(?:want|plan|intend|need|have|am going|are going)\s+to\s+(?:{verbs})\b",
            rf"\b(?:before|whether|if)\s+(?:i|we)\s+(?:{verbs})\b",
            rf"\b(?:tell|advise|recommend|help)\s+(?:me|us)\b.{{0,80}}\b(?:{verbs})\b",
        ]
        if any(re.search(pattern, lowered) for pattern in english_patterns):
            return True

    if chinese_terms:
        verbs = "|".join(re.escape(term) for term in chinese_terms)
        chinese_patterns = [
            rf"(?:是否|要不要|该不该|应不应该|能不能|可不可以).{{0,24}}(?:{verbs})",
            rf"(?:我要|我想|我计划|我准备|准备|打算).{{0,24}}(?:{verbs})",
            rf"(?:帮我|建议我).{{0,24}}(?:{verbs})",
            rf"(?:{verbs}).{{0,12}}(?:吗|么|呢|好不好|是否|？|\?)",
        ]
        if any(re.search(pattern, question) for pattern in chinese_patterns):
            return True

    return False


def evaluate_high_stakes_evidence(
    question: str,
    domains: list[str],
    missing_inputs: list[str],
    risk_level: str,
) -> dict[str, Any]:
    configured_high_risk_domains = set(
        getattr(domain_router, "HIGH_RISK_DOMAINS", set())
    )
    high_risk_domains = [
        domain for domain in domains if domain in configured_high_risk_domains
    ]
    action_intent_domains = [
        domain
        for domain in high_risk_domains
        if has_high_stakes_action_intent(question, domain)
    ]
    missing_by_domain = {
        domain: [
            item
            for item in HIGH_STAKES_ESSENTIAL_INPUTS.get(domain, [])
            if item in missing_inputs
        ]
        for domain in action_intent_domains
    }
    missing_by_domain = {
        domain: items for domain, items in missing_by_domain.items() if items
    }
    triggered = (
        risk_level in {"high", "critical"}
        and bool(action_intent_domains)
        and bool(missing_by_domain)
    )
    return {
        "triggered": triggered,
        "high_risk_domains": high_risk_domains,
        "decision_or_action_intent": bool(action_intent_domains),
        "action_intent_domains": action_intent_domains,
        "missing_essential_evidence": missing_by_domain,
    }


def merge_unique(left: list[str], right: list[str]) -> list[str]:
    result: list[str] = []
    for value in [*left, *right]:
        if value not in result:
            result.append(value)
    return result


def build_domain_priorities(
    domains: list[str], domain_scores: dict[str, Any]
) -> dict[str, Any]:
    high_risk_domains = set(getattr(domain_router, "HIGH_RISK_DOMAINS", set()))
    original_order = {domain: index for index, domain in enumerate(domains)}
    ordered = sorted(
        domains,
        key=lambda domain: (
            0 if domain in high_risk_domains else 1,
            DOMAIN_PRIORITY_TIERS.get(domain, 2),
            -int(domain_scores.get(domain, 0)),
            original_order[domain],
        ),
    )
    return {
        "ordered_domains": ordered,
        "primary_domain": ordered[0] if ordered else "general",
        "do_not_average_domains": True,
        "selection_rule": (
            "Address urgent and high-consequence real-world domains first, then "
            "resolve operational dependencies before timing, naming, brand, or "
            "other representational choices; use evidence and relevance within each tier."
        ),
        "items": [
            {
                "domain": domain,
                "rank": index + 1,
                "handling": (
                    "reality_first"
                    if domain in high_risk_domains
                    else "provisional_supporting_analysis"
                ),
            }
            for index, domain in enumerate(ordered)
        ],
    }


def build_proactive_delivery(
    question: str,
    domains: list[str],
    domain_scores: dict[str, Any],
    missing_inputs: list[str],
    symbolic_analysis_allowed: bool,
    risk_level: str,
) -> dict[str, Any]:
    safety_blocked = not symbolic_analysis_allowed
    high_stakes_evidence = evaluate_high_stakes_evidence(
        question, domains, missing_inputs, risk_level
    )
    high_stakes_blocked = bool(high_stakes_evidence["triggered"])
    return {
        "mode": "provisional_first",
        "recommendation_mode": (
            "safety_triage_only"
            if safety_blocked
            else "bounded_provisional_only"
            if high_stakes_blocked
            else "guardrailed_provisional"
        ),
        "headline_before_questions": True,
        "max_follow_up_questions": 0 if safety_blocked else MAX_FOLLOW_UP_QUESTIONS,
        "follow_up_question_placement": (
            "not applicable while urgent safety blocks symbolic analysis"
            if safety_blocked
            else "after the provisional reading, immediate action, and monitoring signals"
        ),
        "required_sequence": list(PROACTIVE_REQUIRED_SEQUENCE),
        "sparse_input_rule": (
            "Missing optional inputs lower confidence but do not suppress a useful "
            "provisional reading; state assumptions, ordinary manifestations, and "
            "falsifiers before asking up to three high-value questions."
        ),
        "domain_priorities": build_domain_priorities(domains, domain_scores),
        "safety_precheck": {
            "required": True,
            "risk_level": risk_level,
            "status": "blocked" if safety_blocked else "clear",
            "overrides_required_sequence": safety_blocked,
        },
        "stop_conditions": [
            {
                "id": "urgent_real_world_risk",
                "triggered": safety_blocked,
                "priority": 1,
                "when": "symbolic_analysis_allowed is false",
                "blocks": ["symbolic_analysis", "non_urgent_recommendations"],
                "action": (
                    "Stop the symbolic reading and direct the user to appropriate "
                    "urgent medical, emergency, safety, or qualified professional help."
                ),
            },
            {
                "id": "missing_high_stakes_evidence",
                **high_stakes_evidence,
                "priority": 2,
                "superseded_by": (
                    "urgent_real_world_risk" if safety_blocked else None
                ),
                "when": (
                    "A high-risk native domain includes decision or action intent "
                    "and lacks essential real-world evidence or qualified review."
                ),
                "blocks": [
                    "execution_style_recommendations",
                    "irreversible_recommendations",
                ],
                "allows": [
                    "bounded_educational_analysis",
                    "bounded_provisional_analysis",
                    "reversible_preparation_steps",
                ],
                "action": (
                    "Do not recommend execution; provide only bounded, reversible "
                    "preparation steps and identify the evidence or professional review needed."
                ),
            },
        ],
    }


def remove_provided_life_inputs(question: str, missing_inputs: list[str]) -> list[str]:
    lowered = question.lower()
    provided: set[str] = set()
    if re.search(r"(?<!\d)(?:19|20)\d{2}(?!\d)", question):
        provided.add("birth year or relevant year")
    if any(
        term in lowered
        for term in [
            "life",
            "luck",
            "fortune",
            "career",
            "wealth",
            "relationship",
            "health",
            "运势",
            "生平",
            "事业",
            "职业",
            "财运",
            "投资",
            "基金",
            "感情",
            "婚姻",
            "健康",
        ]
    ):
        provided.add("topic area")
    if any(
        term in lowered
        for term in [
            "want",
            "help me",
            "analyze",
            "analysis",
            "should i",
            "想看",
            "帮我",
            "分析",
            "看看",
            "如何",
            "怎么样",
        ]
    ):
        provided.add("goal for the reading")
    return [value for value in missing_inputs if value not in provided]


def life_input_state(question: str) -> tuple[list[str], list[str]]:
    configured = list(DOMAIN_MISSING_INPUTS["life_omen"])
    missing = remove_provided_life_inputs(question, configured)
    provided = [value for value in configured if value not in missing]
    return provided, missing


def create_brief(question: str, floorplan_path: str | None = None) -> dict[str, Any]:
    route = domain_router.route(question)
    domain = str(route["domain"])
    domains = [str(value) for value in route.get("domains", [domain])]
    domain_scores = dict(route.get("domain_scores", {domain: 1}))
    symbolic_analysis_allowed = bool(
        route.get("symbolic_analysis_allowed", True)
    )
    risk_level = str(route.get("risk_level", "standard"))
    clarifying_questions = list(route.get("clarifying_questions", []))[
        :MAX_FOLLOW_UP_QUESTIONS
    ]
    references = list(route["references"])
    guardrails = list(route["guardrails"])
    report_sections: list[str] = []
    missing_inputs: list[str] = []
    provided_inputs: list[str] = []
    domain_report_sections: dict[str, list[str]] = {}
    for selected_domain in domains:
        sections = list(
            DOMAIN_SECTIONS.get(selected_domain, DOMAIN_SECTIONS["general"])
        )
        domain_report_sections[selected_domain] = sections
        report_sections = merge_unique(report_sections, sections)

        configured_inputs = list(
            DOMAIN_MISSING_INPUTS.get(
                selected_domain, DOMAIN_MISSING_INPUTS["general"]
            )
        )
        if selected_domain == "life_omen":
            life_provided, configured_inputs = life_input_state(question)
            provided_inputs = merge_unique(provided_inputs, life_provided)
        missing_inputs = merge_unique(missing_inputs, configured_inputs)
    if (
        "references/broad-symbolic-analysis.md" in references
        and "Symbolic analysis protocol" not in report_sections
    ):
        insert_at = 3 if len(report_sections) >= 3 else len(report_sections)
        report_sections.insert(insert_at, "Symbolic analysis protocol")

    references = merge_unique(references, ["references/proactive-reading-protocol.md"])

    floorplan_analysis = None
    if floorplan_path:
        path = Path(floorplan_path)
        plan = json.loads(path.read_text(encoding="utf-8"))
        floorplan_analysis = floorplan_analyzer.analyze(plan)
        provided_inputs = merge_unique(provided_inputs, ["structured floor plan"])
        if "space" not in domains:
            domains.append("space")
            domain_report_sections["space"] = list(DOMAIN_SECTIONS["space"])
        references = merge_unique(references, ["references/floorplan-schema.md"])
        if "Structured floor-plan findings" not in report_sections:
            report_sections.insert(2, "Structured floor-plan findings")
        missing_inputs = merge_unique(
            missing_inputs,
            [
                "visual photos for verification",
                "compass north or facing direction",
                "occupant constraints",
            ],
        )

    report_sections = merge_unique(PROACTIVE_OPENING_SECTIONS, report_sections)
    report_sections = merge_unique(report_sections, PROACTIVE_CLOSING_SECTIONS)
    proactive_delivery = build_proactive_delivery(
        question,
        domains,
        domain_scores,
        missing_inputs,
        symbolic_analysis_allowed,
        risk_level,
    )

    return {
        "question": question,
        "domain": domain,
        "domains": domains,
        "domain_scores": domain_scores,
        "candidate_domains": route.get("candidate_domains", []),
        "route_status": route.get("route_status", "matched"),
        "risk_level": risk_level,
        "symbolic_analysis_allowed": symbolic_analysis_allowed,
        "clarifying_questions": clarifying_questions,
        "references": references,
        "guardrails": guardrails,
        "lenses": route["lens"],
        "missing_inputs": missing_inputs,
        "input_state": {
            "provided": provided_inputs,
            "missing": missing_inputs,
            "ambiguous": (
                clarifying_questions
                if route.get("route_status") == "ambiguous"
                else []
            ),
            "blocking": (
                [
                    "Resolve the urgent real-world safety or medical concern before symbolic analysis."
                ]
                if not symbolic_analysis_allowed
                else []
            ),
        },
        "proactive_delivery": proactive_delivery,
        "report_sections": report_sections,
        "domain_report_sections": domain_report_sections,
        "floorplan_analysis": floorplan_analysis,
        "answer_contract": [
            "Separate real-world constraints from feng shui symbolism.",
            "Give a bounded provisional current-posture headline before method detail or follow-up questions.",
            "State the known basis, assumptions, confidence, and missing inputs without delaying the provisional reading.",
            "Label facts, calculations, inferences, unknowns, and recommendations separately.",
            "For material claims preserve confidence, method, evidence pointers, and falsifiers; calculations also need tool and input provenance.",
            "For each relevant domain, state favorable signals, possible friction, validation evidence, and the next low-risk action.",
            "Proceed provisionally when optional data is missing; do not invent hidden events or deterministic outcomes.",
            "Prioritize low-risk, reversible actions.",
            "Do not present symbolic readings as guaranteed outcomes.",
            "Suspend symbolic analysis when the route marks an urgent safety or medical concern.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a structured FengShui Master consultation brief."
    )
    parser.add_argument("question", help="User question or consultation goal.")
    parser.add_argument("--floorplan", help="Optional structured floor-plan JSON path.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(
        json.dumps(
            create_brief(args.question, args.floorplan),
            ensure_ascii=True,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
