import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
QUICK_VALIDATE = ROOT / ".github" / "scripts" / "quick_validate.py"


class RepositoryQualityTest(unittest.TestCase):
    def test_github_ci_workflow_exists(self):
        self.assertTrue(WORKFLOW.exists())

    def test_github_ci_runs_tests_and_skill_validation(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("python -m unittest discover -s tests", workflow)
        self.assertIn("quick_validate.py fengshui-master", workflow)
        self.assertIn("python fengshui-master/scripts/domain_router.py", workflow)
        self.assertIn("python fengshui-master/scripts/create_brief.py", workflow)
        self.assertIn("python fengshui-master/scripts/generate_report.py", workflow)

    def test_portable_skill_validator_exists_for_ci(self):
        self.assertTrue(QUICK_VALIDATE.exists())

    def test_readme_mentions_ci(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("GitHub Actions", readme)
        self.assertIn(".github/workflows/ci.yml", readme)


if __name__ == "__main__":
    unittest.main()
