import unittest
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
QUICK_VALIDATE = ROOT / ".github" / "scripts" / "quick_validate.py"
AUDIT_REPOSITORY = ROOT / ".github" / "scripts" / "audit_repository.py"
ISSUE_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md"
BUG_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md"
PR_TEMPLATE = ROOT / ".github" / "pull_request_template.md"
README_ZH = ROOT / "README.zh-CN.md"


class RepositoryQualityTest(unittest.TestCase):
    def test_github_ci_workflow_exists(self):
        self.assertTrue(WORKFLOW.exists())

    def test_ci_is_single_authoritative_workflow(self):
        workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))

        self.assertEqual([path.name for path in workflows], ["ci.yml"])

    def test_github_ci_runs_tests_and_skill_validation(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("python -m unittest discover -s tests", workflow)
        self.assertIn("quick_validate.py fengshui-master", workflow)
        self.assertIn("python fengshui-master/scripts/domain_router.py", workflow)
        self.assertIn("python fengshui-master/scripts/create_brief.py", workflow)
        self.assertIn("python fengshui-master/scripts/generate_report.py", workflow)
        self.assertIn("python .github/scripts/audit_repository.py", workflow)

    def test_portable_skill_validator_exists_for_ci(self):
        self.assertTrue(QUICK_VALIDATE.exists())

    def test_repository_audit_script_exists_for_ci(self):
        self.assertTrue(AUDIT_REPOSITORY.exists())

    def test_repository_audit_script_passes(self):
        result = subprocess.run(
            [sys.executable, str(AUDIT_REPOSITORY)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("Repository audit passed", result.stdout)

    def test_readme_mentions_ci(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("GitHub Actions", readme)
        self.assertIn(".github/workflows/ci.yml", readme)
        self.assertIn(".github/scripts/audit_repository.py", readme)

    def test_bilingual_readme_and_github_metadata_are_present(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("README.zh-CN.md", readme)
        self.assertIn("GitHub Repository Metadata", readme)

        for phrase in [
            "traditional-chinese-culture",
            "feng-shui",
            "wuxing",
            "codex-skill",
            "symbolic-analysis",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, readme)

        self.assertTrue(README_ZH.exists())
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        for phrase in ["FengShui Master", "风水", "五行", "金融", "免责声明", "GitHub Actions"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, chinese_readme)

    def test_open_source_templates_exist(self):
        for path in [ISSUE_TEMPLATE, BUG_TEMPLATE, PR_TEMPLATE]:
            with self.subTest(path=path):
                self.assertTrue(path.exists())

    def test_templates_preserve_safety_boundaries(self):
        template_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [ISSUE_TEMPLATE, BUG_TEMPLATE, PR_TEMPLATE]
        )

        for phrase in ["feng shui school", "guardrails", "not financial advice"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, template_text)


if __name__ == "__main__":
    unittest.main()
