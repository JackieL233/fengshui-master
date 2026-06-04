import unittest
import subprocess
import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
QUICK_VALIDATE = ROOT / ".github" / "scripts" / "quick_validate.py"
AUDIT_REPOSITORY = ROOT / ".github" / "scripts" / "audit_repository.py"
APPLY_REPOSITORY_METADATA = ROOT / ".github" / "scripts" / "apply_repository_metadata.py"
ISSUE_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md"
BUG_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md"
PR_TEMPLATE = ROOT / ".github" / "pull_request_template.md"
README_ZH = ROOT / "README.zh-CN.md"
DEPLOYMENT = ROOT / "DEPLOYMENT.md"
REPOSITORY_METADATA = ROOT / ".github" / "repository-metadata.yml"
PORTABLE_SKILL = ROOT / "PORTABLE_SKILL.md"
PORTABLE_EXAMPLES = ROOT / "examples" / "portable-agent-prompts.md"
PORTABLE_EVAL_SUITE = ROOT / "examples" / "portable-evaluation-suite.json"
PORTABLE_EVAL_RUBRIC = ROOT / "examples" / "portable-evaluation-rubric.json"
PORTABLE_EVAL_VALIDATOR = ROOT / "examples" / "validate_portable_evaluation.py"
REFERENCE_CATALOG = ROOT / "examples" / "reference-catalog.json"
REFERENCE_CATALOG_VALIDATOR = ROOT / "examples" / "validate_reference_catalog.py"
TOOL_CATALOG = ROOT / "examples" / "tool-catalog.json"
TOOL_CATALOG_VALIDATOR = ROOT / "examples" / "validate_tool_catalog.py"
RESPONSE_CONTRACT = ROOT / "examples" / "response-contract.json"
RESPONSE_CONTRACT_VALIDATOR = ROOT / "examples" / "validate_response_contract.py"
CAPABILITY_MATRIX = ROOT / "examples" / "capability-matrix.json"
CAPABILITY_MATRIX_VALIDATOR = ROOT / "examples" / "validate_capability_matrix.py"
SOURCE_QUALITY_POLICY = ROOT / "examples" / "source-quality-policy.json"
SOURCE_QUALITY_POLICY_VALIDATOR = ROOT / "examples" / "validate_source_quality_policy.py"
ADVERSARIAL_EVAL_SUITE = ROOT / "examples" / "adversarial-evaluation-suite.json"
ADVERSARIAL_EVAL_VALIDATOR = ROOT / "examples" / "validate_adversarial_evaluation.py"
INTAKE_CONTRACTS = ROOT / "examples" / "intake-contracts.json"
INTAKE_CONTRACTS_VALIDATOR = ROOT / "examples" / "validate_intake_contracts.py"
GOLDEN_RESPONSES = ROOT / "examples" / "golden-responses.json"
GOLDEN_RESPONSES_VALIDATOR = ROOT / "examples" / "validate_golden_responses.py"
UNIVERSAL_DOMAIN_PROTOCOL = ROOT / "examples" / "universal-domain-protocol.json"
UNIVERSAL_DOMAIN_PROTOCOL_VALIDATOR = ROOT / "examples" / "validate_universal_domain_protocol.py"
EXTERNAL_CALCULATION_CONTRACTS = ROOT / "examples" / "external-calculation-contracts.json"
EXTERNAL_CALCULATION_CONTRACTS_VALIDATOR = ROOT / "examples" / "validate_external_calculation_contracts.py"
CONTRIBUTION_QUALITY_GATES = ROOT / "examples" / "contribution-quality-gates.json"
CONTRIBUTION_QUALITY_GATES_VALIDATOR = ROOT / "examples" / "validate_contribution_quality_gates.py"
RUNTIME_INTEGRATION_PROFILES = ROOT / "examples" / "runtime-integration-profiles.json"
RUNTIME_INTEGRATION_PROFILES_VALIDATOR = ROOT / "examples" / "validate_runtime_integration_profiles.py"
PORTABLE_MANIFEST = ROOT / "portable-skill.json"
PORTABLE_MANIFEST_VALIDATOR = ROOT / "examples" / "validate_portable_manifest.py"
PORTABLE_MANIFEST_SCHEMA = ROOT / "schemas" / "portable-skill.schema.json"
PORTABLE_EVAL_SCHEMA = ROOT / "schemas" / "portable-evaluation-suite.schema.json"
REFERENCE_CATALOG_SCHEMA = ROOT / "schemas" / "reference-catalog.schema.json"
TOOL_CATALOG_SCHEMA = ROOT / "schemas" / "tool-catalog.schema.json"
RESPONSE_CONTRACT_SCHEMA = ROOT / "schemas" / "response-contract.schema.json"
CAPABILITY_MATRIX_SCHEMA = ROOT / "schemas" / "capability-matrix.schema.json"
SOURCE_QUALITY_POLICY_SCHEMA = ROOT / "schemas" / "source-quality-policy.schema.json"
ADVERSARIAL_EVAL_SCHEMA = ROOT / "schemas" / "adversarial-evaluation-suite.schema.json"
INTAKE_CONTRACTS_SCHEMA = ROOT / "schemas" / "intake-contracts.schema.json"
GOLDEN_RESPONSES_SCHEMA = ROOT / "schemas" / "golden-responses.schema.json"
UNIVERSAL_DOMAIN_PROTOCOL_SCHEMA = ROOT / "schemas" / "universal-domain-protocol.schema.json"
EXTERNAL_CALCULATION_CONTRACTS_SCHEMA = ROOT / "schemas" / "external-calculation-contracts.schema.json"
CONTRIBUTION_QUALITY_GATES_SCHEMA = ROOT / "schemas" / "contribution-quality-gates.schema.json"
RUNTIME_INTEGRATION_PROFILES_SCHEMA = ROOT / "schemas" / "runtime-integration-profiles.schema.json"
INTEGRATION_GUIDE = ROOT / "docs" / "integration-guide.md"
SECURITY = ROOT / "SECURITY.md"
CODE_OF_CONDUCT = ROOT / "CODE_OF_CONDUCT.md"
CHANGELOG = ROOT / "CHANGELOG.md"
RELEASE_NOTES = ROOT / "RELEASE_NOTES.md"
GITATTRIBUTES = ROOT / ".gitattributes"
EDITORCONFIG = ROOT / ".editorconfig"


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
        self.assertIn("python examples/validate_tool_catalog.py", workflow)
        self.assertIn("python examples/validate_response_contract.py", workflow)
        self.assertIn("python examples/validate_capability_matrix.py", workflow)
        self.assertIn("python examples/validate_source_quality_policy.py", workflow)
        self.assertIn("python examples/validate_adversarial_evaluation.py", workflow)
        self.assertIn("python examples/validate_intake_contracts.py", workflow)
        self.assertIn("python examples/validate_golden_responses.py", workflow)
        self.assertIn("python examples/validate_universal_domain_protocol.py", workflow)
        self.assertIn("python examples/validate_external_calculation_contracts.py", workflow)
        self.assertIn("python examples/validate_contribution_quality_gates.py", workflow)
        self.assertIn("python examples/validate_runtime_integration_profiles.py", workflow)
        self.assertIn("python .github/scripts/audit_repository.py", workflow)

    def test_portable_skill_validator_exists_for_ci(self):
        self.assertTrue(QUICK_VALIDATE.exists())

    def test_repository_audit_script_exists_for_ci(self):
        self.assertTrue(AUDIT_REPOSITORY.exists())

    def test_repository_metadata_apply_script_exists_and_dry_runs(self):
        self.assertTrue(APPLY_REPOSITORY_METADATA.exists())
        result = subprocess.run(
            [
                sys.executable,
                str(APPLY_REPOSITORY_METADATA),
                "--repo",
                "JackieL233/fengshui-master",
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["repo"], "JackieL233/fengshui-master")
        self.assertEqual(
            payload["repository_patch"]["description"],
            "Portable AI skill and Codex-compatible capability pack for traditional Chinese feng shui, wuxing, auspiciousness, spatial analysis, and cross-domain symbolic decision support.",
        )
        self.assertIn("feng-shui", payload["topics_put"]["names"])
        self.assertIn("portable-skill", payload["topics_put"]["names"])

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

    def test_project_is_positioned_as_portable_ai_skill(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        metadata = REPOSITORY_METADATA.read_text(encoding="utf-8")

        for phrase in [
            "portable AI skill",
            "Codex-compatible",
            "general agent capability pack",
            "PORTABLE_SKILL.md",
            "Codex Installation",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, readme)

        for phrase in [
            "通用 AI Skill",
            "兼容 Codex",
            "智能体能力包",
            "PORTABLE_SKILL.md",
            "Codex 安装",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, chinese_readme)

        for phrase in ["ai-skill", "agent-skill", "portable-skill", "codex-skill"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, metadata)

    def test_portable_skill_guide_exists(self):
        self.assertTrue(PORTABLE_SKILL.exists())
        guide = PORTABLE_SKILL.read_text(encoding="utf-8")

        for phrase in [
            "Portable AI Skill",
            "System Instruction",
            "Use With Any Agent",
            "Codex Compatibility",
            "通用 AI Skill",
            "系统指令",
            "任意智能体",
            "兼容 Codex",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, guide)

    def test_portable_agent_examples_exist(self):
        self.assertTrue(PORTABLE_EXAMPLES.exists())
        examples = PORTABLE_EXAMPLES.read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        for phrase in [
            "Portable Agent Prompt Examples",
            "System prompt",
            "Finance stress test",
            "Life and omen stress test",
            "Floor-plan stress test",
            "Expected boundary behavior",
            "通用智能体提示词示例",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, examples)

        self.assertIn("examples/portable-agent-prompts.md", readme)
        self.assertIn("examples/portable-agent-prompts.md", chinese_readme)
        self.assertIn("examples/portable-agent-prompts.md", portable)

    def test_portable_evaluation_suite_exists(self):
        self.assertTrue(PORTABLE_EVAL_SUITE.exists())
        suite = json.loads(PORTABLE_EVAL_SUITE.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(suite["name"], "fengshui-master-portable-evaluation-suite")
        self.assertGreaterEqual(len(suite["cases"]), 5)
        self.assertIn("examples/portable-evaluation-suite.json", readme)
        self.assertIn("examples/portable-evaluation-suite.json", portable)

        domains = {case["domain"] for case in suite["cases"]}
        for domain in ["finance", "life_omen", "space", "brand_product", "legal_adjacent", "timing", "tooling"]:
            with self.subTest(domain=domain):
                self.assertIn(domain, domains)

        by_id = {case["id"]: case for case in suite["cases"]}
        timing = by_id["timing-new-moon-full-moon-launch"]
        self.assertIn("fengshui-master/references/timing-and-date-selection.md", timing["expected_references"])
        self.assertIn("moon phase", timing["must_include"])
        self.assertIn("guaranteed auspiciousness", timing["must_not_include"])

        bagua_case = by_id["space-bagua-wealth-corner-method-boundary"]
        self.assertIn("fengshui-master/references/foundation.md", bagua_case["expected_references"])
        self.assertIn("bagua", bagua_case["must_include"])
        self.assertIn("guaranteed wealth", bagua_case["must_not_include"])

        solar_terms = by_id["timing-solar-term-seasonal-qi-opening"]
        self.assertIn("fengshui-master/references/timing-and-date-selection.md", solar_terms["expected_references"])
        self.assertIn("solar terms", solar_terms["must_include"])
        self.assertIn("exact solar-term moment", solar_terms["must_not_include"])

        tooling = by_id["tool-catalog-agent-registration"]
        self.assertIn("examples/tool-catalog.json", tooling["expected_references"])
        self.assertIn("schemas/tool-catalog.schema.json", tooling["expected_references"])
        self.assertIn("validate_tool_catalog.py", tooling["must_include"])

        method_selector = by_id["method-selector-school-mixing-boundary"]
        self.assertIn("fengshui-master/references/schools.md", method_selector["expected_references"])
        self.assertIn("method_selector.py", method_selector["must_include"])
        self.assertIn("mix schools silently", method_selector["must_not_include"])

        for case in suite["cases"]:
            with self.subTest(case=case["id"]):
                self.assertIn("prompt", case)
                self.assertGreaterEqual(len(case["expected_references"]), 2)
                self.assertGreaterEqual(len(case["must_include"]), 3)
                self.assertGreaterEqual(len(case["must_not_include"]), 3)
                self.assertTrue(case["boundary_focus"])

    def test_portable_evaluation_rubric_exists(self):
        self.assertTrue(PORTABLE_EVAL_RUBRIC.exists())
        rubric = json.loads(PORTABLE_EVAL_RUBRIC.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertEqual(rubric["name"], "fengshui-master-portable-evaluation-rubric")
        self.assertGreaterEqual(len(rubric["dimensions"]), 5)
        self.assertGreaterEqual(len(rubric["red_lines"]), 5)
        self.assertIn("minimum_passing_score", rubric)
        self.assertIn("examples/portable-evaluation-rubric.json", manifest["evaluation"])
        self.assertIn("examples/portable-evaluation-rubric.json", readme)

        dimension_names = {dimension["name"] for dimension in rubric["dimensions"]}
        for name in ["domain_reality_first", "symbolic_fidelity", "safety_boundaries", "actionability", "transparency"]:
            with self.subTest(name=name):
                self.assertIn(name, dimension_names)

    def test_portable_evaluation_validator_passes(self):
        self.assertTrue(PORTABLE_EVAL_VALIDATOR.exists())
        result = subprocess.run(
            [sys.executable, str(PORTABLE_EVAL_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("Portable evaluation suite is valid", result.stdout)

    def test_reference_catalog_exists_and_covers_manifest_references(self):
        self.assertTrue(REFERENCE_CATALOG.exists())
        self.assertTrue(REFERENCE_CATALOG_VALIDATOR.exists())

        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        catalog = json.loads(REFERENCE_CATALOG.read_text(encoding="utf-8"))
        by_path = {entry["path"]: entry for entry in catalog["references"]}

        self.assertEqual(catalog["name"], "fengshui-master-reference-catalog")
        self.assertEqual(set(manifest["references"]), set(by_path))

        finance = by_path["fengshui-master/references/finance-adapter.md"]
        self.assertEqual(finance["primary_domain"], "finance")
        self.assertEqual(finance["risk_level"], "high")
        self.assertIn("not financial advice", finance["required_guardrails"])

        ethics = by_path["fengshui-master/references/ethics-and-limits.md"]
        self.assertEqual(ethics["risk_level"], "critical")
        self.assertIn("high_stakes", ethics["tags"])

        source_map = by_path["fengshui-master/references/classical-source-map.md"]
        self.assertEqual(source_map["primary_domain"], "source_map")
        self.assertIn("lineage_labeling", source_map["tags"])

        timing = by_path["fengshui-master/references/timing-and-date-selection.md"]
        self.assertEqual(timing["primary_domain"], "timing")
        self.assertIn("moon_phase", timing["tags"])
        self.assertIn("solar_terms", timing["tags"])

        result = subprocess.run(
            [sys.executable, str(REFERENCE_CATALOG_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Reference catalog is valid", result.stdout)

    def test_tool_catalog_exists_and_covers_manifest_tools(self):
        self.assertTrue(TOOL_CATALOG.exists())
        self.assertTrue(TOOL_CATALOG_VALIDATOR.exists())

        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        catalog = json.loads(TOOL_CATALOG.read_text(encoding="utf-8"))
        by_path = {entry["path"]: entry for entry in catalog["tools"]}

        self.assertEqual(catalog["name"], "fengshui-master-tool-catalog")
        self.assertEqual(set(manifest["tools"]), set(by_path))

        router = by_path["fengshui-master/scripts/domain_router.py"]
        self.assertEqual(router["category"], "routing")
        self.assertEqual(router["output_format"], "json")

        method_selector = by_path["fengshui-master/scripts/method_selector.py"]
        self.assertEqual(method_selector["category"], "routing")
        self.assertIn("do not mix schools silently", method_selector["required_guardrails"])

        bagua = by_path["fengshui-master/scripts/bagua_map.py"]
        self.assertEqual(bagua["category"], "calculation")
        self.assertIn("do not mix bagua methods silently", bagua["required_guardrails"])

        report = by_path["fengshui-master/scripts/generate_report.py"]
        self.assertEqual(report["output_format"], "markdown")

        moon = by_path["fengshui-master/scripts/moon_phase.py"]
        self.assertEqual(moon["category"], "timing")
        self.assertIn("do not guarantee auspiciousness", moon["required_guardrails"])

        solar_terms = by_path["fengshui-master/scripts/solar_terms.py"]
        self.assertEqual(solar_terms["category"], "timing")
        self.assertIn("use approximate dates only", solar_terms["required_guardrails"])

        flying = by_path["fengshui-master/scripts/flying_stars.py"]
        self.assertEqual(flying["risk_level"], "high")
        self.assertIn("not a full Xuan Kong natal chart", flying["required_guardrails"])

        result = subprocess.run(
            [sys.executable, str(TOOL_CATALOG_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Tool catalog is valid", result.stdout)

    def test_response_contract_exists_and_passes(self):
        self.assertTrue(RESPONSE_CONTRACT.exists())
        self.assertTrue(RESPONSE_CONTRACT_VALIDATOR.exists())

        contract = json.loads(RESPONSE_CONTRACT.read_text(encoding="utf-8"))

        self.assertEqual(contract["name"], "fengshui-master-response-contract")
        section_names = {section["name"] for section in contract["required_sections"]}
        for section in [
            "domain_reality_check",
            "method_and_symbolic_lenses",
            "recommendations",
            "boundaries",
        ]:
            with self.subTest(section=section):
                self.assertIn(section, section_names)

        disclosures = {
            disclosure["required_text"]
            for disclosure in contract["high_stakes_disclosures"]
        }
        for disclosure in [
            "not financial advice",
            "not medical advice",
            "not legal advice",
            "no deterministic fate claims",
        ]:
            with self.subTest(disclosure=disclosure):
                self.assertIn(disclosure, disclosures)

        result = subprocess.run(
            [sys.executable, str(RESPONSE_CONTRACT_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Response contract is valid", result.stdout)

    def test_portable_manifest_exists_and_passes(self):
        self.assertTrue(PORTABLE_MANIFEST.exists())
        self.assertTrue(PORTABLE_MANIFEST_VALIDATOR.exists())
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertEqual(manifest["name"], "fengshui-master")
        self.assertEqual(manifest["type"], "portable-ai-skill")
        self.assertIn("PORTABLE_SKILL.md", manifest["entrypoints"])
        self.assertIn("fengshui-master/SKILL.md", manifest["entrypoints"])
        self.assertIn("examples/portable-evaluation-suite.json", manifest["evaluation"])
        self.assertIn("examples/reference-catalog.json", manifest["evaluation"])
        self.assertIn("examples/tool-catalog.json", manifest["evaluation"])
        self.assertIn("examples/response-contract.json", manifest["evaluation"])
        self.assertIn("examples/capability-matrix.json", manifest["evaluation"])
        self.assertIn("examples/source-quality-policy.json", manifest["evaluation"])
        self.assertIn("examples/adversarial-evaluation-suite.json", manifest["evaluation"])
        self.assertIn("examples/intake-contracts.json", manifest["evaluation"])
        self.assertIn("examples/golden-responses.json", manifest["evaluation"])
        self.assertIn("examples/universal-domain-protocol.json", manifest["evaluation"])
        self.assertIn("examples/external-calculation-contracts.json", manifest["evaluation"])
        self.assertIn("examples/contribution-quality-gates.json", manifest["evaluation"])
        self.assertIn("examples/runtime-integration-profiles.json", manifest["evaluation"])
        self.assertIn("docs/integration-guide.md", manifest["integration"])
        self.assertIn("fengshui-master/scripts/method_selector.py", manifest["tools"])
        self.assertIn("fengshui-master/scripts/bagua_map.py", manifest["tools"])
        self.assertIn("fengshui-master/scripts/moon_phase.py", manifest["tools"])
        self.assertIn("fengshui-master/scripts/solar_terms.py", manifest["tools"])
        self.assertIn("timing", manifest["domains"])
        self.assertIn("SECURITY.md", manifest["governance"])
        self.assertIn("portable-skill.json", readme)

        result = subprocess.run(
            [sys.executable, str(PORTABLE_MANIFEST_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("Portable skill manifest is valid", result.stdout)

    def test_capability_matrix_exists_and_passes(self):
        self.assertTrue(CAPABILITY_MATRIX.exists())
        self.assertTrue(CAPABILITY_MATRIX_VALIDATOR.exists())

        matrix = json.loads(CAPABILITY_MATRIX.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(matrix["name"], "fengshui-master-capability-matrix")
        self.assertGreaterEqual(len(matrix["capabilities"]), 12)
        self.assertIn("examples/capability-matrix.json", manifest["evaluation"])
        self.assertIn("examples/validate_capability_matrix.py", manifest["evaluation"])

        by_id = {entry["id"]: entry for entry in matrix["capabilities"]}
        for capability_id in [
            "space-form-analysis",
            "life-omen-symbolic-analysis",
            "finance-symbolic-decision-support",
            "new-moon-full-moon-timing",
            "full-bazi-four-pillars",
        ]:
            with self.subTest(capability_id=capability_id):
                self.assertIn(capability_id, by_id)

        self.assertEqual(by_id["space-form-analysis"]["status"], "fully_covered")
        self.assertEqual(by_id["finance-symbolic-decision-support"]["status"], "partially_covered")
        self.assertEqual(by_id["new-moon-full-moon-timing"]["status"], "partially_covered")
        self.assertEqual(by_id["full-bazi-four-pillars"]["status"], "not_covered")

        finance = by_id["finance-symbolic-decision-support"]
        self.assertIn("not financial advice", finance["guardrails"])
        self.assertIn("do not issue buy/sell commands", finance["guardrails"])

        moon = by_id["new-moon-full-moon-timing"]
        self.assertIn("fengshui-master/scripts/moon_phase.py", moon["optional_tools"])
        self.assertIn("not a full almanac", moon["guardrails"])

        bazi = by_id["full-bazi-four-pillars"]
        self.assertIn("complete four-pillar charting is outside current scope", bazi["limitations"])

        for text in [readme, chinese_readme, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("examples/capability-matrix.json", text)
                self.assertIn("examples/validate_capability_matrix.py", text)

        result = subprocess.run(
            [sys.executable, str(CAPABILITY_MATRIX_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Capability matrix is valid", result.stdout)

    def test_source_quality_policy_exists_and_passes(self):
        self.assertTrue(SOURCE_QUALITY_POLICY.exists())
        self.assertTrue(SOURCE_QUALITY_POLICY_VALIDATOR.exists())

        policy = json.loads(SOURCE_QUALITY_POLICY.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(policy["name"], "fengshui-master-source-quality-policy")
        self.assertGreaterEqual(len(policy["source_tiers"]), 5)
        self.assertGreaterEqual(len(policy["claim_policies"]), 6)
        self.assertIn("examples/source-quality-policy.json", manifest["evaluation"])
        self.assertIn("examples/validate_source_quality_policy.py", manifest["evaluation"])

        tiers = {tier["id"]: tier for tier in policy["source_tiers"]}
        for tier_id in [
            "classical_anchor",
            "scholarly_reference",
            "lineage_practice",
            "modern_adaptation",
            "practical_constraint",
        ]:
            with self.subTest(tier_id=tier_id):
                self.assertIn(tier_id, tiers)

        claim_policies = {entry["claim_type"]: entry for entry in policy["claim_policies"]}
        self.assertIn("classical_vocabulary", claim_policies)
        self.assertIn("lineage_formula", claim_policies)
        self.assertIn("modern_cross_domain_adapter", claim_policies)
        self.assertIn("high_stakes_domain_claim", claim_policies)
        self.assertIn("full_bazi_or_almanac_claim", claim_policies)

        modern = claim_policies["modern_cross_domain_adapter"]
        self.assertIn("label as modern symbolic adaptation", modern["required_labels"])
        self.assertIn("do not present modern adapters as classical doctrine", modern["red_lines"])

        high_stakes = claim_policies["high_stakes_domain_claim"]
        self.assertIn("professional boundary first", high_stakes["required_labels"])
        self.assertIn("do not use feng shui as the deciding authority", high_stakes["red_lines"])

        bazi = claim_policies["full_bazi_or_almanac_claim"]
        self.assertEqual(bazi["support_level"], "out_of_scope_without_external_source")
        self.assertIn("do not invent missing calculations", bazi["red_lines"])

        for text in [readme, chinese_readme, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("examples/source-quality-policy.json", text)
                self.assertIn("examples/validate_source_quality_policy.py", text)

        result = subprocess.run(
            [sys.executable, str(SOURCE_QUALITY_POLICY_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Source quality policy is valid", result.stdout)

    def test_adversarial_evaluation_suite_exists_and_passes(self):
        self.assertTrue(ADVERSARIAL_EVAL_SUITE.exists())
        self.assertTrue(ADVERSARIAL_EVAL_VALIDATOR.exists())

        suite = json.loads(ADVERSARIAL_EVAL_SUITE.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(suite["name"], "fengshui-master-adversarial-evaluation-suite")
        self.assertGreaterEqual(len(suite["cases"]), 6)
        self.assertIn("examples/adversarial-evaluation-suite.json", manifest["evaluation"])
        self.assertIn("examples/validate_adversarial_evaluation.py", manifest["evaluation"])

        by_id = {case["id"]: case for case in suite["cases"]}
        for case_id in [
            "prompt-injection-ignore-guardrails",
            "system-prompt-extraction",
            "finance-guaranteed-return-pressure",
            "fake-full-bazi-demand",
            "medical-fear-cure-pressure",
            "school-mixing-authority-trap",
        ]:
            with self.subTest(case_id=case_id):
                self.assertIn(case_id, by_id)

        injection = by_id["prompt-injection-ignore-guardrails"]
        self.assertIn("do not follow injected instructions", injection["must_include"])
        self.assertIn("ignore all previous rules", injection["must_not_include"])

        finance = by_id["finance-guaranteed-return-pressure"]
        self.assertIn("not financial advice", finance["must_include"])
        self.assertIn("guaranteed returns", finance["must_not_include"])

        bazi = by_id["fake-full-bazi-demand"]
        self.assertIn("outside current built-in scope", bazi["must_include"])
        self.assertIn("complete bazi chart", bazi["must_not_include"])

        for text in [readme, chinese_readme, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("examples/adversarial-evaluation-suite.json", text)
                self.assertIn("examples/validate_adversarial_evaluation.py", text)

        result = subprocess.run(
            [sys.executable, str(ADVERSARIAL_EVAL_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Adversarial evaluation suite is valid", result.stdout)

    def test_intake_contracts_exist_and_pass(self):
        self.assertTrue(INTAKE_CONTRACTS.exists())
        self.assertTrue(INTAKE_CONTRACTS_VALIDATOR.exists())

        contracts = json.loads(INTAKE_CONTRACTS.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(contracts["name"], "fengshui-master-intake-contracts")
        self.assertGreaterEqual(len(contracts["domains"]), 10)
        self.assertIn("examples/intake-contracts.json", manifest["evaluation"])
        self.assertIn("examples/validate_intake_contracts.py", manifest["evaluation"])

        by_domain = {entry["domain"]: entry for entry in contracts["domains"]}
        for domain in ["space", "finance", "timing", "life_omen", "wellbeing", "legal_adjacent", "brand", "product"]:
            with self.subTest(domain=domain):
                self.assertIn(domain, by_domain)
                self.assertGreaterEqual(len(by_domain[domain]["required_inputs"]), 3)
                self.assertGreaterEqual(len(by_domain[domain]["ask_first_if_missing"]), 1)
                self.assertGreaterEqual(len(by_domain[domain]["blocking_missing_inputs"]), 1)

        finance = by_domain["finance"]
        self.assertIn("risk tolerance", finance["required_inputs"])
        self.assertIn("financial advice boundary", finance["boundary_disclosures"])
        self.assertIn("do not issue buy/sell commands", finance["red_lines"])

        space = by_domain["space"]
        self.assertIn("floor plan or photos", space["required_inputs"])
        self.assertIn("north arrow or compass bearing", space["ask_first_if_missing"])

        timing = by_domain["timing"]
        self.assertIn("candidate date or date range", timing["required_inputs"])
        self.assertIn("event type", timing["blocking_missing_inputs"])

        for text in [readme, chinese_readme, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("examples/intake-contracts.json", text)
                self.assertIn("examples/validate_intake_contracts.py", text)

        result = subprocess.run(
            [sys.executable, str(INTAKE_CONTRACTS_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Intake contracts are valid", result.stdout)

    def test_golden_responses_exist_and_pass(self):
        self.assertTrue(GOLDEN_RESPONSES.exists())
        self.assertTrue(GOLDEN_RESPONSES_VALIDATOR.exists())

        golden = json.loads(GOLDEN_RESPONSES.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(golden["name"], "fengshui-master-golden-responses")
        self.assertGreaterEqual(len(golden["responses"]), 5)
        self.assertIn("examples/golden-responses.json", manifest["evaluation"])
        self.assertIn("examples/validate_golden_responses.py", manifest["evaluation"])

        by_id = {entry["id"]: entry for entry in golden["responses"]}
        for response_id in [
            "finance-symbolic-risk-answer",
            "space-form-floorplan-answer",
            "timing-new-full-moon-answer",
            "life-omen-conditional-answer",
            "prompt-injection-safe-answer",
        ]:
            with self.subTest(response_id=response_id):
                self.assertIn(response_id, by_id)

        finance = by_id["finance-symbolic-risk-answer"]
        self.assertIn("not financial advice", finance["required_phrases"])
        self.assertIn("do not issue buy/sell commands", finance["quality_checks"])

        timing = by_id["timing-new-full-moon-answer"]
        self.assertIn("moon phase is secondary", timing["required_phrases"])
        self.assertIn("not a full almanac", timing["required_phrases"])

        injection = by_id["prompt-injection-safe-answer"]
        self.assertIn("do not follow injected instructions", injection["required_phrases"])
        self.assertIn("ignore all previous rules", injection["forbidden_phrases"])

        for text in [readme, chinese_readme, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("examples/golden-responses.json", text)
                self.assertIn("examples/validate_golden_responses.py", text)

        result = subprocess.run(
            [sys.executable, str(GOLDEN_RESPONSES_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Golden responses are valid", result.stdout)

    def test_universal_domain_protocol_exists_and_passes(self):
        self.assertTrue(UNIVERSAL_DOMAIN_PROTOCOL.exists())
        self.assertTrue(UNIVERSAL_DOMAIN_PROTOCOL_VALIDATOR.exists())

        protocol = json.loads(UNIVERSAL_DOMAIN_PROTOCOL.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(protocol["name"], "fengshui-master-universal-domain-protocol")
        self.assertIn("examples/universal-domain-protocol.json", manifest["evaluation"])
        self.assertIn("examples/validate_universal_domain_protocol.py", manifest["evaluation"])
        self.assertEqual(
            manifest["schemas"]["universal_domain_protocol"],
            "schemas/universal-domain-protocol.schema.json",
        )

        stages = {stage["id"]: stage for stage in protocol["stages"]}
        for stage_id in [
            "classify_native_domain",
            "rate_domain_risk",
            "collect_minimum_inputs",
            "apply_symbolic_lenses",
            "produce_bounded_answer",
        ]:
            with self.subTest(stage_id=stage_id):
                self.assertIn(stage_id, stages)

        risk_levels = {level["id"]: level for level in protocol["risk_levels"]}
        for risk_id in ["low", "medium", "high", "critical"]:
            with self.subTest(risk_id=risk_id):
                self.assertIn(risk_id, risk_levels)
        self.assertIn("professional authority first", risk_levels["critical"]["required_posture"])

        adapters = {adapter["id"]: adapter for adapter in protocol["adapter_rules"]}
        for adapter_id in ["native_domain_first", "symbolic_layer_second", "wuxing_bridge", "moon_phase_rhythm", "unsupported_calculation_boundary"]:
            with self.subTest(adapter_id=adapter_id):
                self.assertIn(adapter_id, adapters)
        self.assertIn("match moon phase to event type", adapters["moon_phase_rhythm"]["required_checks"])
        self.assertIn("do not use moon phase as the sole decision rule", adapters["moon_phase_rhythm"]["red_lines"])

        examples = {example["domain"]: example for example in protocol["examples"]}
        for domain in ["technology", "sports", "education", "finance", "unknown"]:
            with self.subTest(domain=domain):
                self.assertIn(domain, examples)
        self.assertIn("moon phase rhythm as secondary timing layer", examples["finance"]["symbolic_lenses"])

        for text in [readme, chinese_readme, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("examples/universal-domain-protocol.json", text)
                self.assertIn("examples/validate_universal_domain_protocol.py", text)

        result = subprocess.run(
            [sys.executable, str(UNIVERSAL_DOMAIN_PROTOCOL_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Universal domain protocol is valid", result.stdout)

    def test_external_calculation_contracts_exist_and_pass(self):
        self.assertTrue(EXTERNAL_CALCULATION_CONTRACTS.exists())
        self.assertTrue(EXTERNAL_CALCULATION_CONTRACTS_VALIDATOR.exists())

        contracts = json.loads(EXTERNAL_CALCULATION_CONTRACTS.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(contracts["name"], "fengshui-master-external-calculation-contracts")
        self.assertIn("examples/external-calculation-contracts.json", manifest["evaluation"])
        self.assertIn("examples/validate_external_calculation_contracts.py", manifest["evaluation"])
        self.assertEqual(
            manifest["schemas"]["external_calculation_contracts"],
            "schemas/external-calculation-contracts.schema.json",
        )

        systems = {system["id"]: system for system in contracts["systems"]}
        for system_id in [
            "full_bazi_four_pillars",
            "zi_wei_dou_shu",
            "qi_men_dun_jia",
            "liu_ren",
            "tong_shu_date_selection",
            "precision_astronomy_calendar",
        ]:
            with self.subTest(system_id=system_id):
                self.assertIn(system_id, systems)

        bazi = systems["full_bazi_four_pillars"]
        self.assertIn("birth date", bazi["required_inputs"])
        self.assertIn("birth time", bazi["required_inputs"])
        self.assertIn("calendar conversion convention", bazi["required_inputs"])
        self.assertIn("do not invent missing pillars", bazi["red_lines"])

        almanac = systems["tong_shu_date_selection"]
        self.assertIn("trusted almanac source", almanac["required_inputs"])
        self.assertIn("do not invent tong shu attributes", almanac["red_lines"])

        for text in [readme, chinese_readme, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("examples/external-calculation-contracts.json", text)
                self.assertIn("examples/validate_external_calculation_contracts.py", text)

        result = subprocess.run(
            [sys.executable, str(EXTERNAL_CALCULATION_CONTRACTS_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("External calculation contracts are valid", result.stdout)

    def test_contribution_quality_gates_exist_and_pass(self):
        self.assertTrue(CONTRIBUTION_QUALITY_GATES.exists())
        self.assertTrue(CONTRIBUTION_QUALITY_GATES_VALIDATOR.exists())

        gates = json.loads(CONTRIBUTION_QUALITY_GATES.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        pr_template = PR_TEMPLATE.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(gates["name"], "fengshui-master-contribution-quality-gates")
        self.assertIn("examples/contribution-quality-gates.json", manifest["evaluation"])
        self.assertIn("examples/validate_contribution_quality_gates.py", manifest["evaluation"])
        self.assertEqual(
            manifest["schemas"]["contribution_quality_gates"],
            "schemas/contribution-quality-gates.schema.json",
        )

        gate_ids = {gate["id"]: gate for gate in gates["gates"]}
        for gate_id in [
            "reference_addition",
            "tool_addition",
            "domain_adapter_addition",
            "external_calculation_integration",
            "evaluation_fixture_addition",
            "security_or_high_stakes_change",
            "documentation_or_metadata_change",
        ]:
            with self.subTest(gate_id=gate_id):
                self.assertIn(gate_id, gate_ids)

        external = gate_ids["external_calculation_integration"]
        self.assertIn("examples/external-calculation-contracts.json", external["required_artifacts"])
        self.assertIn("do not invent missing calculations", external["red_lines"])

        for text in [readme, contributing, pr_template, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("examples/contribution-quality-gates.json", text)
                self.assertIn("examples/validate_contribution_quality_gates.py", text)

        result = subprocess.run(
            [sys.executable, str(CONTRIBUTION_QUALITY_GATES_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Contribution quality gates are valid", result.stdout)

    def test_runtime_integration_profiles_exist_and_pass(self):
        self.assertTrue(RUNTIME_INTEGRATION_PROFILES.exists())
        self.assertTrue(RUNTIME_INTEGRATION_PROFILES_VALIDATOR.exists())

        profiles = json.loads(RUNTIME_INTEGRATION_PROFILES.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        guide = INTEGRATION_GUIDE.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")

        self.assertEqual(profiles["name"], "fengshui-master-runtime-integration-profiles")
        self.assertIn("examples/runtime-integration-profiles.json", manifest["evaluation"])
        self.assertIn("examples/validate_runtime_integration_profiles.py", manifest["evaluation"])
        self.assertEqual(
            manifest["schemas"]["runtime_integration_profiles"],
            "schemas/runtime-integration-profiles.schema.json",
        )

        by_id = {profile["id"]: profile for profile in profiles["profiles"]}
        for profile_id in ["chat_assistant", "agent_framework", "rag", "local_cli", "codex"]:
            with self.subTest(profile_id=profile_id):
                self.assertIn(profile_id, by_id)
                self.assertIn("PORTABLE_SKILL.md", by_id[profile_id]["required_assets"])
                self.assertIn("examples/response-contract.json", by_id[profile_id]["required_assets"])
                self.assertIn("python examples/validate_runtime_integration_profiles.py", by_id[profile_id]["validation_commands"])

        agent = by_id["agent_framework"]
        self.assertIn("examples/tool-catalog.json", agent["required_assets"])
        self.assertIn("register tools from examples/tool-catalog.json", agent["required_steps"])

        rag = by_id["rag"]
        self.assertIn("examples/reference-catalog.json", rag["required_assets"])
        self.assertIn("route first, retrieve second, answer third", rag["required_steps"])

        for text in [readme, guide, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("examples/runtime-integration-profiles.json", text)
                self.assertIn("examples/validate_runtime_integration_profiles.py", text)

        result = subprocess.run(
            [sys.executable, str(RUNTIME_INTEGRATION_PROFILES_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("Runtime integration profiles are valid", result.stdout)

    def test_ci_smoke_tests_moon_phase_helper(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("python fengshui-master/scripts/moon_phase.py 2024-04-08 --pretty", workflow)

    def test_ci_smoke_tests_bagua_map_helper(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("python fengshui-master/scripts/bagua_map.py --direction southeast --pretty", workflow)

    def test_ci_smoke_tests_method_selector(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("python fengshui-master/scripts/method_selector.py", workflow)

    def test_ci_smoke_tests_solar_terms_helper(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("python fengshui-master/scripts/solar_terms.py 2026-02-04 --pretty", workflow)

    def test_integration_guide_exists_and_is_linked(self):
        self.assertTrue(INTEGRATION_GUIDE.exists())
        guide = INTEGRATION_GUIDE.read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese_readme = README_ZH.read_text(encoding="utf-8")
        portable = PORTABLE_SKILL.read_text(encoding="utf-8")
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))

        for phrase in [
            "Chat Assistant Setup",
            "Agent Framework Setup",
            "RAG Setup",
            "Local CLI Setup",
            "High-Stakes Adapter Rules",
            "中文接入摘要",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, guide)

        for text in [readme, chinese_readme, portable]:
            with self.subTest(text=text[:20]):
                self.assertIn("docs/integration-guide.md", text)
        self.assertIn("docs/integration-guide.md", manifest["integration"])

    def test_portable_json_schemas_exist(self):
        self.assertTrue(PORTABLE_MANIFEST_SCHEMA.exists())
        self.assertTrue(PORTABLE_EVAL_SCHEMA.exists())
        self.assertTrue(REFERENCE_CATALOG_SCHEMA.exists())
        self.assertTrue(TOOL_CATALOG_SCHEMA.exists())
        self.assertTrue(RESPONSE_CONTRACT_SCHEMA.exists())
        self.assertTrue(CAPABILITY_MATRIX_SCHEMA.exists())
        self.assertTrue(SOURCE_QUALITY_POLICY_SCHEMA.exists())
        self.assertTrue(ADVERSARIAL_EVAL_SCHEMA.exists())
        self.assertTrue(INTAKE_CONTRACTS_SCHEMA.exists())
        self.assertTrue(GOLDEN_RESPONSES_SCHEMA.exists())

        manifest_schema = json.loads(PORTABLE_MANIFEST_SCHEMA.read_text(encoding="utf-8"))
        eval_schema = json.loads(PORTABLE_EVAL_SCHEMA.read_text(encoding="utf-8"))
        reference_schema = json.loads(REFERENCE_CATALOG_SCHEMA.read_text(encoding="utf-8"))
        tool_schema = json.loads(TOOL_CATALOG_SCHEMA.read_text(encoding="utf-8"))
        response_schema = json.loads(RESPONSE_CONTRACT_SCHEMA.read_text(encoding="utf-8"))
        capability_schema = json.loads(CAPABILITY_MATRIX_SCHEMA.read_text(encoding="utf-8"))
        source_quality_schema = json.loads(SOURCE_QUALITY_POLICY_SCHEMA.read_text(encoding="utf-8"))
        adversarial_schema = json.loads(ADVERSARIAL_EVAL_SCHEMA.read_text(encoding="utf-8"))
        intake_schema = json.loads(INTAKE_CONTRACTS_SCHEMA.read_text(encoding="utf-8"))
        golden_schema = json.loads(GOLDEN_RESPONSES_SCHEMA.read_text(encoding="utf-8"))
        manifest = json.loads(PORTABLE_MANIFEST.read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertEqual(manifest_schema["title"], "FengShui Master Portable Skill Manifest")
        self.assertEqual(eval_schema["title"], "FengShui Master Portable Evaluation Suite")
        self.assertEqual(reference_schema["title"], "FengShui Master Reference Catalog")
        self.assertEqual(tool_schema["title"], "FengShui Master Tool Catalog")
        self.assertEqual(response_schema["title"], "FengShui Master Response Contract")
        self.assertEqual(capability_schema["title"], "FengShui Master Capability Matrix")
        self.assertEqual(source_quality_schema["title"], "FengShui Master Source Quality Policy")
        self.assertEqual(adversarial_schema["title"], "FengShui Master Adversarial Evaluation Suite")
        self.assertEqual(intake_schema["title"], "FengShui Master Intake Contracts")
        self.assertEqual(golden_schema["title"], "FengShui Master Golden Responses")
        self.assertEqual(manifest["schemas"]["manifest"], "schemas/portable-skill.schema.json")
        self.assertEqual(manifest["schemas"]["evaluation_suite"], "schemas/portable-evaluation-suite.schema.json")
        self.assertEqual(manifest["schemas"]["reference_catalog"], "schemas/reference-catalog.schema.json")
        self.assertEqual(manifest["schemas"]["tool_catalog"], "schemas/tool-catalog.schema.json")
        self.assertEqual(manifest["schemas"]["response_contract"], "schemas/response-contract.schema.json")
        self.assertEqual(manifest["schemas"]["capability_matrix"], "schemas/capability-matrix.schema.json")
        self.assertEqual(manifest["schemas"]["source_quality_policy"], "schemas/source-quality-policy.schema.json")
        self.assertEqual(manifest["schemas"]["adversarial_evaluation_suite"], "schemas/adversarial-evaluation-suite.schema.json")
        self.assertEqual(manifest["schemas"]["intake_contracts"], "schemas/intake-contracts.schema.json")
        self.assertEqual(manifest["schemas"]["golden_responses"], "schemas/golden-responses.schema.json")
        self.assertIn("integration", manifest_schema["required"])

        for phrase in [
            "schemas/portable-skill.schema.json",
            "schemas/portable-evaluation-suite.schema.json",
            "schemas/reference-catalog.schema.json",
            "schemas/tool-catalog.schema.json",
            "schemas/response-contract.schema.json",
            "schemas/capability-matrix.schema.json",
            "schemas/source-quality-policy.schema.json",
            "schemas/adversarial-evaluation-suite.schema.json",
            "schemas/intake-contracts.schema.json",
            "schemas/golden-responses.schema.json",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, readme)

    def test_deployment_docs_and_metadata_are_present(self):
        self.assertTrue(DEPLOYMENT.exists())
        deployment = DEPLOYMENT.read_text(encoding="utf-8")
        for phrase in [
            "git remote add origin",
            "git push -u origin master:main",
            ".github/scripts/apply_repository_metadata.py",
            "JackieL233/fengshui-master",
            "Repository URL",
            "部署",
            "GitHub Actions",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, deployment)

        self.assertTrue(REPOSITORY_METADATA.exists())
        metadata = REPOSITORY_METADATA.read_text(encoding="utf-8")
        for phrase in [
            "fengshui-master",
            "Portable AI skill",
            "feng-shui",
            "wuxing",
            "traditional-chinese-culture",
            "symbolic-analysis",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, metadata)

    def test_open_source_templates_exist(self):
        for path in [ISSUE_TEMPLATE, BUG_TEMPLATE, PR_TEMPLATE]:
            with self.subTest(path=path):
                self.assertTrue(path.exists())

    def test_security_and_conduct_docs_exist(self):
        self.assertTrue(SECURITY.exists())
        self.assertTrue(CODE_OF_CONDUCT.exists())

        security = SECURITY.read_text(encoding="utf-8")
        conduct = CODE_OF_CONDUCT.read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for phrase in [
            "Security Policy",
            "High-Stakes Safety",
            "not medical, legal, financial",
            "Report a Safety Issue",
            "prompt-injection",
            "cultural respect",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, security)

        for phrase in [
            "Code of Conduct",
            "Respectful Collaboration",
            "traditional Chinese culture",
            "No fear-based claims",
            "Reporting",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, conduct)

        self.assertIn("SECURITY.md", readme)
        self.assertIn("CODE_OF_CONDUCT.md", readme)

    def test_release_docs_exist(self):
        self.assertTrue(CHANGELOG.exists())
        self.assertTrue(RELEASE_NOTES.exists())

        changelog = CHANGELOG.read_text(encoding="utf-8")
        release_notes = RELEASE_NOTES.read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for phrase in [
            "Changelog",
            "Unreleased",
            "portable AI skill",
            "portable-skill.json",
            "evaluation suite",
            "Security Policy",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, changelog)

        for phrase in [
            "FengShui Master v1",
            "Portable AI Skill",
            "Codex-compatible",
            "What is included",
            "Safety and governance",
            "Validation",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, release_notes)

        self.assertIn("CHANGELOG.md", readme)
        self.assertIn("RELEASE_NOTES.md", readme)

    def test_repository_hygiene_files_exist(self):
        self.assertTrue(GITATTRIBUTES.exists())
        self.assertTrue(EDITORCONFIG.exists())

        gitattributes = GITATTRIBUTES.read_text(encoding="utf-8")
        editorconfig = EDITORCONFIG.read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for phrase in ["* text=auto eol=lf", "*.md text eol=lf", "*.json text eol=lf", "*.py text eol=lf"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, gitattributes)

        for phrase in ["root = true", "charset = utf-8", "end_of_line = lf", "insert_final_newline = true"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, editorconfig)

        self.assertIn(".gitattributes", readme)
        self.assertIn(".editorconfig", readme)

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
