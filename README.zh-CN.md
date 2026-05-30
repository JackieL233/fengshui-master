# FengShui Master

[English README](README.md)

FengShui Master 是一个通用 AI Skill 和智能体能力包，目标是把中国传统风水、五行、阴阳、八卦、干支、吉凶、趋吉避凶与现代跨领域决策支持结合起来。它通过 `fengshui-master/SKILL.md` 兼容 Codex，但知识库、工作流、脚本、样例和安全边界都按平台无关方式设计，可用于任意智能体、LLM 助手、本地自动化或 RAG 系统。

它既能做住宅、办公室、商铺、土地、户型、门、床、书桌、厨房、方位、玄空飞星等空间分析，也能把风水作为广义象义语言，用于人生阶段、生平、运势、金融、商业、品牌、职业、产品、学习、关系与健康相邻环境等问题。

本项目把风水定位为传统文化、空间分析与象义决策支持系统，不把任何象义判断包装成确定预测。

## GitHub 仓库信息

建议仓库名：

```text
fengshui-master
```

英文简介：

```text
Portable AI skill and Codex-compatible capability pack for traditional Chinese feng shui, wuxing, auspiciousness, spatial analysis, and cross-domain symbolic decision support.
```

中文简介：

```text
通用 AI Skill 与兼容 Codex 的风水智能体能力包，覆盖传统风水、五行、吉凶、空间分析与跨领域象义决策支持。
```

建议 Topics：

```text
feng-shui, fengshui, wuxing, five-elements, bagua, chinese-metaphysics, traditional-chinese-culture, ai-skill, agent-skill, portable-skill, codex-skill, symbolic-analysis, spatial-analysis, cultural-analysis, auspiciousness
```

## 覆盖范围

- 基础理论：气、阴阳、五行、八卦、天干地支、二十四山。
- 广义风水象义协议：观气、取象、辨势、条件式吉凶、化解、复核。
- 生平与运势：人生阶段、五行偏性、吉凶条件、趋吉避凶行动建议。
- 空间风水：住宅、办公室、商铺、房间、土地、户型、门、床、桌、厨房、卫生间。
- 形势派与环境：道路、水、山、建筑形体、明堂、煞气、采光、通风、动线。
- 理气与时空：八宅命卦、三元九运、玄空飞星基础脚手架、太岁、岁破、三煞。
- 跨领域分析：金融、商业、品牌、职业、关系、产品、学习、健康相邻环境、法律相邻风险。
- 命名与品牌：品牌命名、颜色、标志、视觉气质与五行象义约束。
- 工具脚本：罗盘二十四山、命卦、干支年、年度方位注意、三元运、飞星脚手架、领域路由、咨询 brief、报告生成、结构化户型分析。
- 开源工程：GitHub Actions、仓库一致性审计、Issue/PR 模板、测试与样例报告。

## 重要边界

FengShui Master 不是医疗、法律、金融、工程、建筑、税务、心理或安全建议。

它不会声称：

- 风水可以保证财富、婚姻、健康、怀孕、升职、市场收益或灾祸结果。
- 一个名字、颜色、方位、户型或日期可以决定命运。
- 简化的命卦、干支年或飞星脚手架可以替代完整八字、紫微斗数、奇门、六壬或通书择日。
- 风水象义可以覆盖专业检查、法律义务、金融风控或医学判断。

推荐使用方式是：先看真实约束，再看风水象义，最后给出低风险、可逆、可验证的行动。

## 目录结构

```text
PORTABLE_SKILL.md
README.md
README.zh-CN.md
fengshui-master/
  SKILL.md
  agents/openai.yaml
  references/
    foundation.md
    forms-and-environment.md
    schools.md
    analysis-templates.md
    remedies.md
    timing-and-date-selection.md
    xuan-kong-flying-stars.md
    yin-house.md
    glossary.md
    case-patterns.md
    sample-readings.md
    consultation-brief.md
    reporting-protocol.md
    broad-symbolic-analysis.md
    domain-adapters.md
    finance-adapter.md
    business-adapter.md
    brand-adapter.md
    career-adapter.md
    relationship-adapter.md
    product-adapter.md
    learning-adapter.md
    wellbeing-adapter.md
    legal-adjacent-adapter.md
    life-and-omen-adapter.md
    five-phase-domain-map.md
    floorplan-schema.md
    ethics-and-limits.md
    sources.md
  scripts/
    luopan.py
    minggua.py
    ganzhi.py
    annual_afflictions.py
    create_brief.py
    generate_report.py
    periods.py
    flying_stars.py
    domain_router.py
    analyze_floorplan.py
  assets/
    sample-floorplan.json
    sample-finance-brief.json
    sample-finance-report.md
    sample-life-omen-report.md
    sample-product-report.md
    sample-floorplan-report.md
```

## 通用使用方式

如果不使用 Codex，请先阅读 [`PORTABLE_SKILL.md`](PORTABLE_SKILL.md)。它提供可复制到任意智能体的系统指令、工作流、输出结构、领域路由、安全边界和中英文说明。

常见接入方式：

- **ChatGPT、Claude、Gemini、本地 LLM 或自定义智能体**：复制 `PORTABLE_SKILL.md` 中的 “System Instruction”，再把相关 `fengshui-master/references/` 文件作为上下文或检索资料。
- **Agent 框架**：把 `fengshui-master/scripts/` 暴露为工具，让智能体按 `PORTABLE_SKILL.md` 和路由结果读取参考文件。
- **RAG 系统**：索引 `fengshui-master/references/`，把 `PORTABLE_SKILL.md` 作为顶层行为规范，并保留 `fengshui-master/SKILL.md` 作为 Codex 适配入口。
- **手动使用**：先运行 `create_brief.py`、`domain_router.py`、`generate_report.py` 生成结构化脚手架，再撰写最终分析。

## Codex 安装

把 `fengshui-master/` 文件夹复制或链接到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R fengshui-master ~/.codex/skills/
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force $HOME\.codex\skills
Copy-Item -Recurse -Force .\fengshui-master $HOME\.codex\skills\
```

然后在 Codex 中使用：

```text
Use $fengshui-master to analyze ...
```

## 示例提示词

- `Use $fengshui-master to review this apartment floor plan from a form-school perspective.`
- `Use $fengshui-master to analyze my career phase through five phases and 趋吉避凶 planning.`
- `Use $fengshui-master to review this investment decision through finance-first analysis and feng shui symbolism.`
- `Use $fengshui-master to analyze a person's life pattern, 五行 balance, 吉凶 conditions, and practical next steps.`
- `Use $fengshui-master to review this product onboarding flow through form, flow, leakage, and symbolic lenses.`
- `Use $fengshui-master to compare brand names and colors through wuxing and audience constraints.`

## 常用命令

创建咨询 brief：

```bash
python fengshui-master/scripts/create_brief.py "Should I buy this stock next month using feng shui?" --pretty
```

生成 Markdown 报告脚手架：

```bash
python fengshui-master/scripts/generate_report.py "Use feng shui to review this product onboarding flow"
```

结构化户型分析：

```bash
python fengshui-master/scripts/analyze_floorplan.py fengshui-master/assets/sample-floorplan.json --pretty
```

罗盘二十四山：

```bash
python fengshui-master/scripts/luopan.py 187 --pretty
```

命卦：

```bash
python fengshui-master/scripts/minggua.py 1990 --sex male --pretty
```

干支年：

```bash
python fengshui-master/scripts/ganzhi.py 2026 --pretty
```

年度太岁、岁破、三煞方位注意：

```bash
python fengshui-master/scripts/annual_afflictions.py 2026 --pretty
```

跨领域路由：

```bash
python fengshui-master/scripts/domain_router.py "用风水五行分析这个股票投资是否吉利" --pretty
```

## 样例资产

- `fengshui-master/assets/sample-finance-report.md`：金融优先、风水象义辅助的投资决策样例。
- `fengshui-master/assets/sample-life-omen-report.md`：生平、五行、吉凶、趋吉避凶样例。
- `fengshui-master/assets/sample-product-report.md`：产品 onboarding 流程的形、势、泄漏与象义样例。
- `fengshui-master/assets/sample-floorplan-report.md`：结构化户型 JSON 与空间风水样例。
- `fengshui-master/assets/sample-floorplan.json`：可重复使用的户型输入。
- `fengshui-master/assets/sample-finance-brief.json`：咨询 brief 示例。

## 验证

运行测试：

```bash
python -m unittest discover -s tests
```

运行便携 Skill 元数据验证：

```bash
python .github/scripts/quick_validate.py fengshui-master
```

运行仓库一致性审计：

```bash
python .github/scripts/audit_repository.py
```

## GitHub Actions

仓库包含 `.github/workflows/ci.yml`。push 和 pull request 会自动运行：

- `python -m unittest discover -s tests`
- `.github/scripts/quick_validate.py`
- `.github/scripts/audit_repository.py`
- 主要 CLI 工具 smoke tests

## 贡献

欢迎贡献：

- 有来源说明的风水概念、流派或术语解释。
- 更完整的空间、金融、事业、品牌、产品、关系、学习等样例。
- 可测试的 deterministic helper scripts。
- 更安全的高风险问题表达方式。
- 更清晰的中英文术语、拼音、翻译和流派边界。

贡献时请说明相关风水流派、来源或现代适配方式，并保留安全边界。

## 免责声明

FengShui Master 仅用于传统文化、教育、空间设计支持与象义决策辅助。它不是医疗、法律、金融、工程、建筑、税务、心理或安全建议。任何涉及投资、健康、法律、安全、建筑结构、税务或重大人生选择的问题，都应以专业意见和现实证据为先。
