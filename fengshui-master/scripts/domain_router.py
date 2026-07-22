#!/usr/bin/env python3
"""Route a user question to FengShui Master references."""

from __future__ import annotations

import argparse
import json
import re


def score_question(question: str, keywords: set[str]) -> int:
    normalized = question.casefold()
    return sum(1 for keyword in keywords if keyword_matches(normalized, keyword))


def keyword_matches(normalized_text: str, keyword: str) -> bool:
    """Match CJK text by substring and Latin text by word or phrase boundary."""
    normalized_keyword = keyword.casefold().strip()
    if not normalized_keyword:
        return False
    if any(ord(character) > 127 for character in normalized_keyword):
        return normalized_keyword in normalized_text
    pattern = rf"(?<![a-z0-9_]){re.escape(normalized_keyword)}(?![a-z0-9_])"
    return re.search(pattern, normalized_text) is not None


DOMAIN_RULES = [
    (
        "timing",
        {
            "moon",
            "lunar",
            "solar",
            "term",
            "terms",
            "season",
            "seasonal",
            "jieqi",
            "lichun",
            "equinox",
            "solstice",
            "newmoon",
            "fullmoon",
            "auspicious date",
            "auspicious time",
            "launch",
            "move",
            "moving",
            "opening",
            "renovation",
            "月相",
            "新月",
            "满月",
            "节气",
            "二十四节气",
            "立春",
            "春分",
            "夏至",
            "秋分",
            "冬至",
            "朔",
            "望",
            "朔望",
            "择日",
            "择时",
            "日期",
            "开业",
            "搬家",
            "装修",
            "动土",
        },
        [
            "references/timing-and-date-selection.md",
            "references/broad-symbolic-analysis.md",
            "references/ethics-and-limits.md",
        ],
        [
            "moon phase and solar terms are secondary symbolic timing layers, not a full almanac or guaranteed auspiciousness method.",
            "Do not guarantee outcomes from new moon, full moon, lunar phase, solar term, seasonal qi, or any single timing marker.",
            "Use event type, candidate dates, local time zone, practical constraints, and lineage-specific calendar attributes before symbolic timing.",
        ],
    ),
    (
        "naming",
        {
            "name",
            "names",
            "naming",
            "rename",
            "renaming",
            "given name",
            "baby name",
            "personal name",
            "stage name",
            "pen name",
            "pseudonym",
            "company name",
            "brand name",
            "product name",
            "meaning",
            "pronunciation",
            "homophone",
            "取名",
            "起名",
            "改名",
            "姓名",
            "名字",
            "宝宝取名",
            "艺名",
            "笔名",
            "公司名",
            "品牌名",
            "产品名",
            "字义",
            "读音",
            "谐音",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/naming-adapter.md",
            "references/five-phase-domain-map.md",
            "references/foundation.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not infer a missing element from year-level data or an approximate personal context scaffold.",
            "Do not claim that a name guarantees luck, wealth, health, relationships, status, or business success.",
            "Prioritize meaning, pronunciation, cultural fit, registration or trademark constraints, and user intent before symbolic mapping.",
            "Name the character-element, stroke, phonetic, bazi, or lineage method instead of silently mixing systems.",
        ],
    ),
    (
        "life_omen",
        {
            "auspicious",
            "inauspicious",
            "omen",
            "omens",
            "luck",
            "lucky",
            "unlucky",
            "fortune",
            "destiny",
            "fate",
            "life",
            "lifepath",
            "biography",
            "person",
            "personal",
            "bazi",
            "birth",
            "year",
            "everything feels blocked",
            "凶",
            "吉凶",
            "不吉",
            "运势",
            "运气",
            "命",
            "命运",
            "命理",
            "生平",
            "人生",
            "个人",
            "财运",
            "趋吉避凶",
            "八字",
            "出生",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/life-and-omen-adapter.md",
            "references/proactive-reading-protocol.md",
            "references/five-phase-domain-map.md",
            "references/foundation.md",
            "references/ethics-and-limits.md",
            "references/timing-and-date-selection.md",
        ],
        [
            "Do not make deterministic fate, health, death, wealth, marriage, or disaster claims.",
            "Use feng shui, yin-yang, wuxing, bagua, and timing as symbolic analysis, not guaranteed prediction.",
            "Disclose when full bazi, zi wei, qimen, liuren, or almanac calculation is not implemented.",
        ],
    ),
    (
        "finance",
        {
            "stock",
            "stocks",
            "bond",
            "portfolio",
            "investment",
            "invest",
            "trading",
            "crypto",
            "bitcoin",
            "fund",
            "funds",
            "mutual fund",
            "index fund",
            "etf",
            "money",
            "money is tight",
            "volatile",
            "volatility",
            "recent performer",
            "drawdown",
            "performance chasing",
            "chasing performance",
            "fomo",
            "financial",
            "finance",
            "market",
            "risk",
            "fintech",
            "cash",
            "budget",
            "wealth",
            "股票",
            "投资",
            "理财",
            "基金",
            "净值",
            "回撤",
            "定投",
            "仓位",
            "追涨",
            "追高",
            "债券",
            "加密",
            "比特币",
            "市场",
            "财运",
            "财富",
            "现金",
            "预算",
            "风险",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/finance-adapter.md",
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
            "references/ethics-and-limits.md",
            "references/timing-and-date-selection.md",
        ],
        [
            "This is not financial advice.",
            "Do not guarantee profit, timing, or risk-free outcomes.",
            "Use feng shui as a symbolic decision-support lens alongside real financial analysis.",
        ],
    ),
    (
        "product",
        {
            "product",
            "onboarding",
            "ux",
            "user",
            "users",
            "feature",
            "features",
            "roadmap",
            "activation",
            "retention",
            "conversion",
            "funnel",
            "app",
            "software",
            "产品",
            "用户",
            "体验",
            "功能",
            "路线图",
            "激活",
            "留存",
            "转化",
            "漏斗",
            "应用",
            "软件",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/product-adapter.md",
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not replace user research, accessibility, security, privacy, analytics, or engineering review.",
            "Use feng shui as a metaphor for user flow, support, friction, and leakage.",
        ],
    ),
    (
        "brand",
        {
            "brand",
            "branding",
            "logo",
            "color",
            "colors",
            "launch",
            "naming",
            "marketing",
            "campaign",
            "品牌",
            "标志",
            "颜色",
            "命名",
            "营销",
            "发布",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/brand-adapter.md",
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
            "references/foundation.md",
            "references/remedies.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not replace market research, accessibility, or legal trademark review.",
            "Use five phases and yin-yang as symbolic design constraints.",
        ],
    ),
    (
        "business",
        {
            "business",
            "strategy",
            "operations",
            "revenue",
            "customers",
            "customer",
            "sales",
            "startup",
            "founder",
            "company",
            "retail",
            "shop",
            "decision",
            "decisions",
            "execution",
            "partnership",
            "fundraising",
            "hiring",
            "商业",
            "生意",
            "业务",
            "战略",
            "运营",
            "收入",
            "客户",
            "销售",
            "创业",
            "公司",
            "合伙",
            "融资",
            "招聘",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/business-adapter.md",
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not guarantee revenue, growth, funding, or market outcomes.",
            "Use business fundamentals first: customers, margins, cash flow, team, and constraints.",
        ],
    ),
    (
        "career",
        {
            "career",
            "job",
            "promotion",
            "interview",
            "negotiation",
            "team",
            "leadership",
            "boss",
            "work",
            "职业",
            "事业",
            "工作",
            "升职",
            "面试",
            "谈判",
            "领导",
            "团队",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/career-adapter.md",
            "references/domain-adapters.md",
            "references/life-and-omen-adapter.md",
            "references/five-phase-domain-map.md",
            "references/analysis-templates.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not promise career outcomes.",
            "Combine symbolic timing and environment advice with practical preparation.",
        ],
    ),
    (
        "relationship",
        {
            "relationship",
            "relationships",
            "romance",
            "romantic",
            "marriage",
            "partner",
            "family",
            "friendship",
            "conflict",
            "violence",
            "abuse",
            "communication",
            "roommate",
            "关系",
            "感情",
            "恋爱",
            "婚姻",
            "伴侣",
            "家庭",
            "家人",
            "朋友",
            "冲突",
            "沟通",
            "室友",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/relationship-adapter.md",
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not predict marriage, divorce, pregnancy, affairs, reconciliation, or another person's feelings.",
            "Prioritize consent, communication, privacy, and safety.",
        ],
    ),
    (
        "learning",
        {
            "learning",
            "study",
            "studying",
            "exam",
            "exams",
            "memory",
            "practice",
            "focus",
            "course",
            "school",
            "education",
            "certification",
            "学习",
            "读书",
            "考试",
            "记忆",
            "练习",
            "专注",
            "课程",
            "学校",
            "教育",
            "证书",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/learning-adapter.md",
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not guarantee exam success, admission, memory, or mastery.",
            "Use feng shui as an environment, rhythm, attention, and review-cycle support lens.",
        ],
    ),
    (
        "legal_adjacent",
        {
            "legal",
            "law",
            "contract",
            "contracts",
            "dispute",
            "court",
            "lawsuit",
            "compliance",
            "lease",
            "inheritance",
            "filing",
            "clause",
            "clauses",
            "privacy",
            "legal deadline",
            "court deadline",
            "法律",
            "合同",
            "契约",
            "纠纷",
            "争议",
            "法院",
            "诉讼",
            "合规",
            "租约",
            "继承",
            "条款",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/legal-adjacent-adapter.md",
            "references/domain-adapters.md",
            "references/five-phase-domain-map.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not provide legal advice.",
            "Legal rights, obligations, deadlines, evidence, jurisdiction, and counsel take priority.",
        ],
    ),
    (
        "wellbeing",
        {
            "health",
            "healthcare",
            "medical",
            "patient",
            "chest pain",
            "difficulty breathing",
            "trouble breathing",
            "self-harm",
            "suicide",
            "emergency",
            "胸痛",
            "呼吸困难",
            "自残",
            "自杀",
            "紧急情况",
            "sleep",
            "sleeping",
            "sleeping poorly",
            "poor sleep",
            "stress",
            "wellbeing",
            "wellness",
            "anxiety",
            "focus",
            "energy",
            "健康",
            "睡眠",
            "压力",
            "焦虑",
            "专注",
            "精力",
        },
        [
            "references/broad-symbolic-analysis.md",
            "references/wellbeing-adapter.md",
            "references/domain-adapters.md",
            "references/life-and-omen-adapter.md",
            "references/analysis-templates.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Do not diagnose or treat medical conditions.",
            "Prioritize light, air, sleep, ergonomics, and professional care where needed.",
        ],
    ),
    (
        "space",
        {
            "home",
            "house",
            "apartment",
            "bedroom",
            "office",
            "desk",
            "kitchen",
            "bathroom",
            "mirror",
            "bagua",
            "trigram",
            "wealth corner",
            "wealth sector",
            "career corner",
            "career sector",
            "relationship corner",
            "relationship sector",
            "helpful people",
            "door",
            "floor",
            "layout",
            "room",
            "shop",
            "store",
            "land",
            "site",
            "structural danger",
            "gas leak",
            "fire emergency",
            "住宅",
            "房子",
            "公寓",
            "卧室",
            "办公室",
            "书桌",
            "厨房",
            "卫生间",
            "镜子",
            "门",
            "八卦",
            "财位",
            "事业位",
            "桃花位",
            "贵人位",
            "户型",
            "布局",
            "商铺",
            "店铺",
            "土地",
            "墓地",
        },
        [
            "references/foundation.md",
            "references/analysis-templates.md",
            "references/forms-and-environment.md",
            "references/remedies.md",
            "references/ethics-and-limits.md",
        ],
        [
            "Use observable form and safety before symbolic judgments.",
        ],
    ),
]


HIGH_RISK_DOMAINS = {"finance", "legal_adjacent", "wellbeing"}
UNIVERSAL_ADAPTATION_PATTERNS = {
    "cybersecurity",
    "cyber security",
    "security program",
    "security controls",
    "information security",
}
CRITICAL_SAFETY_PATTERNS = {
    "chest pain",
    "difficulty breathing",
    "trouble breathing",
    "self-harm",
    "suicide",
    "medical emergency",
    "imminent danger",
    "violence",
    "legal deadline",
    "court deadline",
    "filing deadline",
    "structural danger",
    "gas leak",
    "fire emergency",
    "胸痛",
    "呼吸困难",
    "自残",
    "自杀",
    "紧急情况",
    "燃气泄漏",
    "火灾",
    "结构危险",
    "暴力",
    "法律截止日期",
}


def clarification_questions(domains: list[str], status: str) -> list[str]:
    if status == "critical_safety":
        return [
            "Is anyone in immediate danger or experiencing urgent medical symptoms?",
            "Which qualified emergency or professional service can you contact now?",
        ]
    if status == "needs_clarification":
        return [
            "What real-world domain and decision should the reading support?",
            "Do you want spatial, timing, personal-context, or broad symbolic analysis?",
        ]
    if status == "ambiguous":
        return [
            f"Which domain should lead the analysis: {', '.join(domains[:3])}?",
            "What concrete outcome, time horizon, and constraints matter most?",
        ]
    return []


def route(question: str) -> dict[str, object]:
    critical_safety = any(
        keyword_matches(question.casefold(), pattern)
        for pattern in CRITICAL_SAFETY_PATTERNS
    )
    scored: list[tuple[int, int, str, list[str], list[str]]] = []
    for index, (domain, keywords, references, guardrails) in enumerate(DOMAIN_RULES):
        score = score_question(question, keywords)
        if score > 0:
            scored.append((score, index, domain, references, guardrails))

    if not scored:
        universal_adaptation = any(
            keyword_matches(question.casefold(), pattern)
            for pattern in UNIVERSAL_ADAPTATION_PATTERNS
        )
        fallback_status = (
            "critical_safety"
            if critical_safety
            else "universal_adaptation"
            if universal_adaptation
            else "needs_clarification"
        )
        fallback_references = [
            "references/broad-symbolic-analysis.md",
            "references/domain-adapters.md",
            "references/proactive-reading-protocol.md",
            "references/foundation.md",
            "references/ethics-and-limits.md",
        ]
        fallback_guardrails = [
            (
                "Address urgent safety, emergency, medical, or legal-deadline needs before symbolic analysis."
                if critical_safety
                else "Use the universal domain protocol: establish domain-native evidence and controls before any symbolic mapping."
                if universal_adaptation
                else "Identify the domain first, then apply feng shui as an auxiliary symbolic lens."
            ),
        ]
        if universal_adaptation:
            fallback_references.append("references/five-phase-domain-map.md")
            fallback_guardrails.extend(
                [
                    "Do not treat cybersecurity as a traditional feng shui domain or invent security facts.",
                    "Security controls, threat evidence, testing, and qualified security review take priority over symbolism.",
                ]
            )
        return {
            "domain": "general",
            "domains": ["general"],
            "domain_scores": {"general": 1},
            "candidate_domains": [{"domain": "general", "score": 1}],
            "route_status": fallback_status,
            "risk_level": (
                "critical"
                if critical_safety
                else "high"
                if universal_adaptation
                else "standard"
            ),
            "symbolic_analysis_allowed": not critical_safety,
            "clarifying_questions": clarification_questions([], fallback_status),
            "references": fallback_references,
            "guardrails": fallback_guardrails,
            "lens": [
                "yin-yang balance",
                "five-phase relationships",
                "timing and activation",
                "form, flow, and containment",
                "risk and remedy hierarchy",
            ],
        }

    scored.sort(key=lambda item: (-item[0], item[1]))
    _, _, primary_domain, _, _ = scored[0]
    selected = scored[:5]

    selected_domains = {item[2] for item in selected}
    for item in scored:
        if item[2] in HIGH_RISK_DOMAINS and item[2] not in selected_domains:
            selected.append(item)
            selected_domains.add(item[2])

    top_score = scored[0][0]
    top_domains = [item[2] for item in scored if item[0] == top_score]
    if critical_safety:
        route_status = "critical_safety"
    elif len(top_domains) > 1:
        route_status = "ambiguous"
    else:
        route_status = "matched"

    references: list[str] = []
    guardrails: list[str] = []
    domains: list[str] = []
    domain_scores: dict[str, int] = {}
    for score, _, domain, domain_references, domain_guardrails in selected:
        domains.append(domain)
        domain_scores[domain] = score
        for value in domain_references:
            if value not in references:
                references.append(value)
        for value in domain_guardrails:
            if value not in guardrails:
                guardrails.append(value)

    if critical_safety:
        guardrails.insert(
            0,
            "Address urgent safety, emergency, medical, or legal-deadline needs before symbolic analysis.",
        )

    return {
        "domain": primary_domain,
        "domains": domains,
        "domain_scores": domain_scores,
        "candidate_domains": [
            {"domain": domain, "score": score}
            for score, _, domain, _, _ in scored[:5]
        ],
        "route_status": route_status,
        "risk_level": (
            "critical"
            if critical_safety
            else "high"
            if any(domain in HIGH_RISK_DOMAINS for domain in domains)
            else "standard"
        ),
        "symbolic_analysis_allowed": not critical_safety,
        "clarifying_questions": clarification_questions(top_domains, route_status),
        "references": references,
        "guardrails": guardrails,
        "lens": [
            "yin-yang balance",
            "five-phase relationships",
            "timing and activation",
            "form, flow, and containment",
            "risk and remedy hierarchy",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Route a cross-domain question to FengShui Master references."
    )
    parser.add_argument("question", help="User question or short task description.")
    parser.add_argument("--pretty", action="store_true", help="Print indented JSON.")
    args = parser.parse_args()

    print(json.dumps(route(args.question), ensure_ascii=True, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
