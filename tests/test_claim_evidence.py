import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "examples" / "validate_claim_evidence.py"
POLICY = ROOT / "examples" / "claim-evidence-policy.json"
SCHEMA = ROOT / "schemas" / "agent-claims.schema.json"


def run_validator(payload=None):
    if payload is None:
        return subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
    with tempfile.TemporaryDirectory() as temporary_directory:
        path = Path(temporary_directory) / "claims.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )


class ClaimEvidencePolicyTest(unittest.TestCase):
    def test_policy_schema_and_validator_pass(self):
        result = run_validator()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Claim-evidence policy and claims are valid", result.stdout)
        self.assertTrue(POLICY.exists())
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["title"], "FengShui Master Agent Claims")

        manifest = json.loads((ROOT / "portable-skill.json").read_text(encoding="utf-8"))
        self.assertIn("examples/claim-evidence-policy.json", manifest["evaluation"])
        self.assertIn("examples/validate_claim_evidence.py", manifest["evaluation"])
        self.assertIn("examples/validate_json_schemas.py", manifest["evaluation"])
        self.assertEqual(manifest["schemas"]["agent_claims"], "schemas/agent-claims.schema.json")

        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("python examples/validate_claim_evidence.py", workflow)
        self.assertIn("python examples/validate_json_schemas.py", workflow)

    def test_observed_claim_requires_user_or_artifact_pointer(self):
        payload = {
            "claims": [
                {
                    "id": "c1",
                    "text": "The user has a hidden conflict.",
                    "status": "observed",
                    "confidence": "high",
                    "method": "symbolic reading",
                    "evidence_refs": ["source:general-symbolism"],
                    "falsifiers": ["The user denies it."],
                    "high_stakes_domain": "none",
                }
            ]
        }

        result = run_validator(payload)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("observed claim requires a user: or artifact: pointer", result.stderr)

    def test_calculated_claim_requires_tool_input_and_method_provenance(self):
        payload = {
            "claims": [
                {
                    "id": "c1",
                    "text": "The period is nine.",
                    "status": "calculated",
                    "confidence": "high",
                    "method": "period lookup",
                    "evidence_refs": ["tool:periods.py"],
                    "falsifiers": ["A different documented boundary convention applies."],
                    "high_stakes_domain": "none",
                }
            ]
        }

        result = run_validator(payload)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires tool, inputs, and method provenance", result.stderr)

    def test_personalized_inference_requires_basis_and_falsifiers(self):
        payload = {
            "claims": [
                {
                    "id": "c1",
                    "text": "You may be under resource pressure.",
                    "status": "inferred",
                    "confidence": "low",
                    "method": "five-phase symbolic hypothesis",
                    "evidence_refs": ["user:request"],
                    "falsifiers": ["Cash flow and workload are both stable."],
                    "high_stakes_domain": "finance",
                    "boundary_ref": "examples/response-contract.json#finance",
                }
            ]
        }

        result = run_validator(payload)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires concrete basis_refs", result.stderr)


if __name__ == "__main__":
    unittest.main()
