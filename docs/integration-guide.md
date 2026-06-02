# FengShui Master Integration Guide

This guide shows how to adapt FengShui Master to common AI runtimes without making it Codex-only. Use `PORTABLE_SKILL.md` as the behavioral policy, `portable-skill.json` as the manifest, and the files under `fengshui-master/references/` as the knowledge base.

## Integration Principles

- Load `PORTABLE_SKILL.md` before task-specific context.
- Keep `fengshui-master/references/ethics-and-limits.md` available for every high-stakes question.
- Route the user's request before answering. Use `fengshui-master/scripts/domain_router.py` when Python tools are available.
- Retrieve only the relevant reference files for the domain. Avoid injecting the entire knowledge base when a narrow question only needs one adapter.
- Use deterministic scripts for calculations that the host can run. If a tool is unavailable, state the missing calculation and avoid invented precision.
- Keep real-world constraints ahead of symbolic reading, especially for finance, health, law, construction, safety, and relationships.
- Evaluate adapters with `examples/portable-evaluation-suite.json` and score outputs with `examples/portable-evaluation-rubric.json`.

## Minimal Context Pack

For a lightweight assistant, include:

1. `PORTABLE_SKILL.md`
2. `fengshui-master/references/consultation-brief.md`
3. `fengshui-master/references/broad-symbolic-analysis.md`
4. `fengshui-master/references/domain-adapters.md`
5. `fengshui-master/references/ethics-and-limits.md`

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
5. Reject outputs that violate any red line in `examples/portable-evaluation-rubric.json`.

Recommended assistant behavior:

```text
First classify the domain, then ask only for missing inputs that materially change the reading. Separate observations, traditional symbolism, and practical advice. For finance, law, health, engineering, architecture, or safety, state that the answer is symbolic support only.
```

## Agent Framework Setup

Use this setup for LangChain, LlamaIndex, AutoGen, CrewAI, semantic kernels, or custom agent runtimes:

1. Register `portable-skill.json` as the capability manifest.
2. Load `PORTABLE_SKILL.md` as the top-level policy.
3. Add a retrieval index over `fengshui-master/references/`.
4. Expose these Python tools when available:
   - `fengshui-master/scripts/domain_router.py`
   - `fengshui-master/scripts/create_brief.py`
   - `fengshui-master/scripts/generate_report.py`
   - `fengshui-master/scripts/analyze_floorplan.py`
   - `fengshui-master/scripts/luopan.py`
   - `fengshui-master/scripts/minggua.py`
   - `fengshui-master/scripts/ganzhi.py`
   - `fengshui-master/scripts/annual_afflictions.py`
   - `fengshui-master/scripts/periods.py`
   - `fengshui-master/scripts/flying_stars.py`
5. Require the agent to call or emulate `domain_router.py` before selecting references.
6. Run portable evaluation cases after any prompt, retrieval, or tool-schema change.

Tool result handling:

- Treat tool outputs as scaffolds, not final authority.
- Preserve guardrails from `create_brief.py` in the final answer.
- Do not let a symbolic output override user safety, legal duties, financial risk controls, or professional evidence.

## RAG Setup

Use this setup for retrieval-augmented generation:

1. Index files under `fengshui-master/references/` as separate documents.
2. Store path, title, domain, and risk level metadata for each file.
3. Keep `PORTABLE_SKILL.md` outside retrieval as a fixed policy.
4. Route first, retrieve second, answer third.
5. Prefer exact adapter files over broad files when the domain is known.
6. Always retrieve `ethics-and-limits.md` for finance, wellbeing, legal-adjacent, building, safety, or life-omen questions.

Suggested metadata:

```json
{
  "path": "fengshui-master/references/finance-adapter.md",
  "domain": "finance",
  "risk_level": "high",
  "required_guardrail": "not financial advice"
}
```

## Local CLI Setup

Use the scripts for repeatable local workflows:

```bash
python fengshui-master/scripts/domain_router.py "Should I buy this stock next month?" --pretty
python fengshui-master/scripts/create_brief.py "Should I buy this stock next month?" --pretty
python fengshui-master/scripts/generate_report.py "Should I buy this stock next month?"
python examples/validate_portable_manifest.py
python examples/validate_portable_evaluation.py
```

For structured floor plans:

```bash
python fengshui-master/scripts/analyze_floorplan.py fengshui-master/assets/sample-floorplan.json --pretty
```

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
- The assistant uses high-stakes disclaimers in the correct domains.
- The assistant refuses deterministic fortune, medical, legal, financial, engineering, architectural, or safety claims.
- The assistant passes `examples/portable-evaluation-suite.json`.
- Human reviewers can score outputs with `examples/portable-evaluation-rubric.json`.

## 中文接入摘要

通用接入时，把 `PORTABLE_SKILL.md` 作为顶层行为规范，把 `fengshui-master/references/` 作为知识库，把 `fengshui-master/scripts/` 作为可选工具。复杂问题先路由领域，再读取对应 adapter，最后生成 brief 或报告。金融、健康、法律、建筑、安全、生平吉凶等问题必须先处理现实约束，再使用风水象义，不做确定预测或专业替代建议。
