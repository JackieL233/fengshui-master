import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "domain_router.py"


def run_router(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class DomainRouterTest(unittest.TestCase):
    def test_finance_routes_to_finance_adapter_and_ethics(self):
        data = run_router("Should I buy this stock next month?")

        self.assertEqual(data["domain"], "finance")
        self.assertIn("references/finance-adapter.md", data["references"])
        self.assertIn("references/ethics-and-limits.md", data["references"])
        self.assertIn("financial advice", data["guardrails"][0])

    def test_brand_routes_to_domain_adapter(self):
        data = run_router("Help me choose brand colors and a launch direction")

        self.assertEqual(data["domain"], "brand")
        self.assertIn("references/domain-adapters.md", data["references"])

    def test_space_defaults_to_classic_feng_shui(self):
        data = run_router("Analyze my bedroom layout and mirror placement")

        self.assertEqual(data["domain"], "space")
        self.assertIn("references/analysis-templates.md", data["references"])


if __name__ == "__main__":
    unittest.main()
