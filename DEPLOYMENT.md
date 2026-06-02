# Deployment / 开源部署

This checklist is the release playbook for publishing FengShui Master to GitHub as a portable AI skill, general agent capability pack, and Codex-compatible skill.

本文件是 FengShui Master 发布到 GitHub 的中英双语部署清单。

## Repository URL

Create an empty public GitHub repository first:

```text
https://github.com/<owner>/fengshui-master
```

创建公开空仓库后，把实际 Repository URL 填到这里或发给维护者继续推送。

## GitHub Metadata

Use `.github/repository-metadata.yml` as the source of truth.
Use `.github/scripts/apply_repository_metadata.py` to apply the About description, homepage, and topics through the GitHub API when a GitHub token is available.

Repository name:

```text
fengshui-master
```

Description:

```text
Portable AI skill and Codex-compatible capability pack for traditional Chinese feng shui, wuxing, auspiciousness, spatial analysis, and cross-domain symbolic decision support.
```

中文简介：

```text
通用 AI Skill 与兼容 Codex 的风水智能体能力包，覆盖传统风水、五行、吉凶、空间分析与跨领域象义决策支持。
```

Topics:

```text
feng-shui, fengshui, wuxing, five-elements, bagua, chinese-metaphysics, traditional-chinese-culture, ai-skill, agent-skill, portable-skill, codex-skill, symbolic-analysis, spatial-analysis, cultural-analysis, auspiciousness
```

## Before Push / 推送前检查

Run:

```bash
python -m unittest discover -s tests
python .github/scripts/quick_validate.py fengshui-master
python .github/scripts/audit_repository.py
```

Expected:

```text
Ran ... tests OK
Skill is valid!
Repository audit passed
```

## Create GitHub Repository / 创建 GitHub 仓库

Recommended browser settings:

- Owner: your GitHub account or organization.
- Repository name: `fengshui-master`.
- Visibility: Public.
- Do not initialize with README, `.gitignore`, or license because this repository already contains them.
- Description: use the metadata description above.
- Topics: include `ai-skill`, `agent-skill`, `portable-skill`, and `codex-skill`.

## Push / 推送

After the empty GitHub repository exists, run:

```bash
git remote add origin <repository-url>
git push -u origin master:main
```

The local branch is currently `master`. The push command publishes it as remote `main`.

如果本地分支仍是 `master`，上面的命令会把它推送成远程 `main`。

## After Push / 推送后检查

Open the repository page and verify:

- README renders in English and links to `README.zh-CN.md`.
- `PORTABLE_SKILL.md` is visible and explains platform-independent use.
- Chinese README renders correctly.
- License is visible.
- GitHub Actions starts and passes.
- Topics match `.github/repository-metadata.yml`.
- About description matches the English description.
- Sample assets are visible:
  - `fengshui-master/assets/sample-finance-report.md`
  - `fengshui-master/assets/sample-life-omen-report.md`
  - `fengshui-master/assets/sample-product-report.md`
  - `fengshui-master/assets/sample-floorplan-report.md`

To update the GitHub About area from the local metadata file:

```bash
GITHUB_TOKEN=<token-with-repo-permission> python .github/scripts/apply_repository_metadata.py --repo JackieL233/fengshui-master
```

Dry-run mode prints the exact payload without changing GitHub:

```bash
python .github/scripts/apply_repository_metadata.py --repo JackieL233/fengshui-master --dry-run
```

## Release Boundary / 发布边界

FengShui Master is for cultural, educational, spatial-analysis, and symbolic decision-support use. It is not medical, legal, financial, engineering, architectural, tax, psychological, or safety advice.
