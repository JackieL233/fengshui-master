# FengShui Master Integration Guide

This guide shows how to adapt FengShui Master to common AI runtimes without making it Codex-only. Use `PORTABLE_SKILL.md` as the behavioral policy, `portable-skill.json` as the manifest, and the files under `fengshui-master/references/` as the knowledge base.

For machine-readable runtime setup, use `examples/runtime-integration-profiles.json` and validate it with `examples/validate_runtime_integration_profiles.py`. The profiles mirror this guide for chat assistants, agent frameworks, RAG systems, local CLI workflows, and Codex. For proactive-first UX regression testing, use `examples/user-journey-evaluation-suite.json` and validate it with `examples/validate_user_journey_evaluation.py`.

## Integration Principles

- Load `PORTABLE_SKILL.md` before task-specific context.
- Keep `fengshui-master/references/ethics-and-limits.md` available for every high-stakes question.
- Select the method and route the user's request before answering. Use `fengshui-master/scripts/method_selector.py` and `fengshui-master/scripts/domain_router.py` when Python tools are available.
- Compose only relevant context and preserve provenance. For naming, load `fengshui-master/references/naming-adapter.md`; add personal context for personal names and brand context for commercial names, but do not infer element deficiency from a year-level scaffold.
- Use `examples/tool-catalog.json` when registering scripts as agent tools or function-call wrappers.
- Retrieve only the relevant reference files for the domain. Avoid injecting the entire knowledge base when a narrow question only needs one adapter.
- Use deterministic scripts for calculations that the host can run. If a tool is unavailable, state the missing calculation and avoid invented precision.
- Keep real-world constraints ahead of symbolic reading, especially for finance, health, law, construction, safety, and relationships.
- Run the urgent safety check first. Unless immediate danger requires triage, give a bounded provisional current-posture headline before any non-urgent question; ask no more than three precision questions, and only after the useful initial reading and action.
- Use `examples/response-contract.json` to enforce final-answer sections, high-stakes disclosures, output modes, and red-line behavior.
- Use `examples/claim-evidence-policy.json` and `schemas/agent-claims.schema.json` to preserve evidence pointers, calculation provenance, confidence, falsifiers, and recommendation verification for material claims.
- Evaluate adapters with `examples/portable-evaluation-suite.json`, run the 20 proactive user journeys in `examples/user-journey-evaluation-suite.json`, and score outputs with `examples/portable-evaluation-rubric.json`.

## Minimal Context Pack

For a lightweight assistant, include:

1. `PORTABLE_SKILL.md`
2. `fengshui-master/references/consultation-brief.md`
3. `fengshui-master/references/proactive-reading-protocol.md`
4. `fengshui-master/references/broad-symbolic-analysis.md`
5. `fengshui-master/references/domain-adapters.md`
6. `fengshui-master/references/ethics-and-limits.md`

Add one specialized adapter when the request is clear:

- Finance: `fengshui-master/references/finance-adapter.md`
- Life, omen, luck, auspiciousness: `fengshui-master/references/life-and-omen-adapter.md`
- Space and floor plans: `fengshui-master/references/foundation.md`, `fengshui-master/references/forms-and-environment.md`, `fengshui-master/references/analysis-templates.md`
- Brand or naming: `fengshui-master/references/brand-adapter.md`
- Product or UX: `fengshui-master/references/product-adapter.md`
- Legal-adjacent risk: `fengshui-master/references/legal-adjacent-adapter.md`

## Chat Assistant Setup

Use this setup for ChatGPT, Claude, Gemini, or similar hosted assistants:

1. Paste the `System Instruction` block from `PORTABLE_SKILL.md` into the system, developer, project, or custom-instructions area.
2. Upload or attach the minimal context pack.
3. Add the specialized adapter file for the user's domain.
4. For repeatable testing, run the prompts in `examples/portable-agent-prompts.md`.
5. Use `examples/response-contract.json` as the final-answer contract.
6. Reject outputs that violate any red line in `examples/portable-evaluation-rubric.json` or `examples/response-contract.json`.
7. Run `python examples/validate_user_journey_evaluation.py`, then execute the user journeys against the configured assistant.

Recommended assistant behavior:

```text
Classify the domain and run an urgent safety and native-domain risk check. Unless immediate danger requires triage, state a bounded provisional current-posture headline before any non-urgent question. Then separate the known basis, favorable factors, possible friction, confirmation and disconfirmation signals, and practical action. Ask at most three precision questions only after that useful initial reading. For finance, law, health, engineering, architecture, or safety, state that the answer is symbolic support only.
```

## Agent Framework Setup

Use this setup for LangChain, LlamaIndex, AutoGen, CrewAI, semantic kernels, or custom agent runtimes:

1. Register `portable-skill.json` as the capability manifest.
2. Load `PORTABLE_SKILL.md` as the top-level policy.
3. Add a retrieval index over `fengshui-master/references/`.
4. Use `examples/tool-catalog.json` for tool names, paths, command templates, input metadata, output formats, risk levels, and required guardrails.
5. Use `examples/response-contract.json` as the final response policy after tool use and retrieval.
6. Expose these Python tools when available:
   - `fengshui-master/scripts/domain_router.py`
   - `fengshui-master/scripts/method_selector.py`
   - `fengshui-master/scripts/create_brief.py`
   - `fengshui-master/scripts/personal_context.py`
   - `fengshui-master/scripts/generate_report.py`
   - `fengshui-master/scripts/analyze_floorplan.py`
   - `fengshui-master/scripts/luopan.py`
   - `fengshui-master/scripts/minggua.py`
   - `fengshui-master/scripts/ganzhi.py`
   - `fengshui-master/scripts/annual_afflictions.py`
   - `fengshui-master/scripts/periods.py`
   - `fengshui-master/scripts/flying_stars.py`
7. Require the agent to call or emulate `method_selector.py` before method-specific claims, then call or emulate `domain_router.py` before selecting references.
8. Run the portable evaluation cases and proactive user journeys after any prompt, retrieval, tool-schema, or response-contract change.

Tool result handling:

- Treat tool outputs as scaffolds, not final authority.
- Preserve guardrails from `create_brief.py` in the final answer.
- Do not let a symbolic output override user safety, legal duties, financial risk controls, or professional evidence.

## RAG Setup

Use this setup for retrieval-augmented generation:

1. Index files under `fengshui-master/references/` as separate documents.
2. Use `examples/reference-catalog.json` for path, title, domain, risk level, tags, and required guardrail metadata.
3. Use `schemas/reference-catalog.schema.json` when the host platform supports JSON Schema validation for retrieval metadata.
4. Keep `PORTABLE_SKILL.md` outside retrieval as a fixed policy.
5. Route first, retrieve second, answer third.
6. Prefer exact adapter files over broad files when the domain is known.
7. Always retrieve `ethics-and-limits.md` for finance, wellbeing, legal-adjacent, building, safety, or life-omen questions.

Suggested metadata:

```json
{
  "path": "fengshui-master/references/finance-adapter.md",
  "domain": "finance",
  "risk_level": "high",
  "required_guardrail": "not financial advice"
}
```

Validate the catalog before publishing integration changes:

```bash
python examples/validate_reference_catalog.py
```

## Local CLI Setup

Use the scripts for repeatable local workflows:

```bash
python fengshui-master/scripts/domain_router.py "Should I buy this stock next month?" --pretty
python fengshui-master/scripts/method_selector.py "Use Xuan Kong flying stars for this Period 9 renovation" --pretty
python fengshui-master/scripts/create_brief.py "Should I buy this stock next month?" --pretty
python fengshui-master/scripts/personal_context.py --birth-date 1998-03-22 --birth-time 18:30 --sex male --birth-location "Tongxiang, Zhejiang, China" --timezone Asia/Shanghai --as-of 2026-07-18 --pretty
python fengshui-master/scripts/generate_report.py "Should I buy this stock next month?"
python examples/validate_portable_manifest.py
python examples/validate_portable_evaluation.py
python examples/validate_user_journey_evaluation.py
python examples/validate_reference_catalog.py
python examples/validate_tool_catalog.py
python examples/validate_response_contract.py
python examples/validate_runtime_integration_profiles.py
```

For structured floor plans:

```bash
python fengshui-master/scripts/analyze_floorplan.py fengshui-master/assets/sample-floorplan.json --pretty
```

## Conversation Context

For opt-in scheduled or event-triggered messages, follow [Proactive Host Integration](proactive-host-integration.md). It specifies source permissions, scheduling, private delivery, freshness, quiet hours, revocation, provider receipts, and a local fake-sender demonstration. The passive skill and brief/report generators are not background services; `proactive_checkin.py` is the decision and acknowledgment layer, not a transport.

The assistant should reuse explicit facts in the current conversation without asking for them again. Apply the latest correction before calling tools. Preserve declined or unknown inputs as unknown; do not fill them with guesses. Follow-ups should explain changes and the next action, not restart the intake. See the manual multi-turn scenarios in `examples/portable-agent-prompts.md` and `conversation_defaults` in `examples/response-contract.json`.

Both `create_brief.py` and `generate_report.py` accept an optional `--known-inputs <path.json>`. The JSON must be an object mapping exact labels from `DOMAIN_MISSING_INPUTS` in `create_brief.py` to nonempty strings. For example:

```json
{
  "decision type": "Review my habit of chasing fund performance; no trade request",
  "time horizon": "Three years",
  "liquidity needs": "Emergency savings are held separately"
}
```

```bash
python fengshui-master/scripts/create_brief.py "Review my fund-investing habits" --known-inputs context.json --pretty
python fengshui-master/scripts/generate_report.py "Review my fund-investing habits" --known-inputs context.json
```

Python callers can pass the object as `known_inputs=` to either function, avoiding a context file. The tools do not remember previous runs or write context files themselves. The report echoes supplied values, so omit sensitive details that should not enter the output. The host remains responsible for context provenance, relevant scope, conflicts, and retention consent. Unknown labels, blank values and non-string values are rejected. Supplying all fields never proves financial suitability, factual accuracy, or professional review. Current urgent risk still overrides prior context.

The current question determines domain routing. For elliptical follow-ups such as "what next?", the host should state the relevant already-known topic in the tool's question, without inventing new facts. The dictionary does not route topics or parse chat history. A declined field is not a supplied fact: hosts must suppress that optional question in the final answer instead of encoding a fabricated value. Three questions is a ceiling, not a target.

For "now", use the actual analysis date and relevant current timezone; never reuse dates from examples. Birthplace does not establish current residence. Brief/report tools are still scaffolds, not full language-model readings or automatic monitoring services.

`personal_context.py --current-timezone America/New_York` resolves today's date in that zone when `--as-of` is omitted. The legacy `--timezone` flag records birth-context provenance only. Output records `as_of_source`; an explicit `--as-of` wins, and no current timezone means a disclosed host-local fallback. If the runtime lacks IANA data, provide the already-localized `--as-of` and omit `--current-timezone`. Moon/solar-term helpers remain approximate date-only scaffolds, not exact local astronomy.

Windows development dependencies include `tzdata`; portable Python hosts without a system IANA database can install it with `python -m pip install tzdata`. Other script features can still run without it when an explicit analysis date is supplied.

中文接入要点：把本轮对话中用户已明确的信息传给 `known_inputs`，不要自动保存敏感资料。纠正信息后更新输入并撤回受影响的旧结论；用户拒绝提供的信息继续标为未知，不重复追问。追问先说判断变化和下一步，三个问题只是上限。工具会在输出中显示传入值，宿主应控制隐私；“最近/现在”必须绑定真实分析日期，而不是示例日期。

## Codex Setup

For Codex, copy `fengshui-master/` into the local skills directory and invoke `$fengshui-master`. Codex uses `fengshui-master/SKILL.md`, but the underlying references, scripts, evaluation files, and guardrails are the same portable assets described here.

## High-Stakes Adapter Rules

| Domain | Required first layer | Feng shui layer | Never do |
| --- | --- | --- | --- |
| Finance | risk tolerance, diversification, liquidity, time horizon | Water/liquidity, Wood/growth, Fire/market heat, Earth/reserves, Metal/risk control | buy/sell commands, guaranteed returns |
| Wellbeing | medical care, sleep, ventilation, ergonomics, stress load | qi flow, light, clutter, support, phase balance | diagnosis or treatment |
| Legal-adjacent | jurisdiction, contracts, deadlines, counsel, evidence | timing, support, leakage, conflict posture | legal advice or outcome prediction |
| Space/building | safety, code, structure, budget, accessibility | form, flow, sha qi, command position, direction | engineering or architectural claims |
| Life/omen | user agency, context, uncertainty, practical next steps | five phases, ji/xiong conditions, timing, support/leakage | deterministic fate claims |

## Acceptance Checklist

An integration is ready when:

- The assistant can identify the domain before answering.
- The assistant retrieves or loads the correct adapter files.
- The assistant keeps observations, symbolism, and practical recommendations separate.
- The assistant runs urgent safety triage first and, when no immediate danger blocks interpretation, leads with a bounded provisional current-posture headline rather than a questionnaire.
- The assistant asks no more than three high-value precision questions, and only after the initial reading, immediate action, and monitoring guidance.
- The assistant scans only relevant domains and labels observed, calculated, inferred, unknown, and recommended content.
- The assistant includes favorable signals, possible friction, confirmation/refutation evidence, 72-hour / 30-day / 90-day actions, and monitoring signals.
- The assistant never states an unverified hidden event as fact or uses cold-reading agreement as proof.
- The assistant uses high-stakes disclaimers in the correct domains.
- The assistant refuses deterministic fortune, medical, legal, financial, engineering, architectural, or safety claims.
- The assistant follows `examples/response-contract.json` for final-answer sections and red-line behavior.
- The assistant passes `examples/portable-evaluation-suite.json`.
- The assistant passes all scenarios in `examples/user-journey-evaluation-suite.json`, validated by `examples/validate_user_journey_evaluation.py`.
- Human reviewers can score outputs with `examples/portable-evaluation-rubric.json`.
- The selected runtime profile in `examples/runtime-integration-profiles.json` is satisfied.

## 中文接入摘要

通用接入时，把 `PORTABLE_SKILL.md` 作为顶层行为规范，把 `fengshui-master/references/` 作为知识库，把 `fengshui-master/scripts/` 作为可选工具。复杂问题先路由领域，再读取对应 adapter 与 `proactive-reading-protocol.md`，最后生成 brief 或报告。默认顺序是：先做紧急安全检查；除即时危险必须优先处置外，先给有边界的当前态势初判，再说明依据、有利面、潜在阻力、核验信号和行动，最后最多提出三个会实质提高精度的问题。信息稀疏只降低置信度，不得把回答变成问卷。金融、健康、法律、建筑、安全、生平吉凶等问题必须先处理现实约束，不做确定预测、冷读断言或专业替代建议。用 `examples/user-journey-evaluation-suite.json` 做主动式体验回归，并运行 `python examples/validate_user_journey_evaluation.py` 验证评测文件。
