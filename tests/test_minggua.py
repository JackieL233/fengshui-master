import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "fengshui-master" / "scripts" / "minggua.py"


def run_minggua(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class MingGuaScriptTest(unittest.TestCase):
    def test_common_1900s_examples(self):
        male = run_minggua("1990", "--sex", "male")
        female = run_minggua("1990", "--sex", "female")

        self.assertEqual(male["gua_number"], 1)
        self.assertEqual(male["group"], "east")
        self.assertEqual(male["directions"]["sheng_qi"], "southeast")
        self.assertEqual(female["gua_number"], 8)
        self.assertEqual(female["group"], "west")
        self.assertEqual(female["directions"]["fu_wei"], "northeast")

    def test_2000_boundary_examples(self):
        self.assertEqual(run_minggua("2000", "--sex", "male")["gua_number"], 9)
        self.assertEqual(run_minggua("2000", "--sex", "female")["gua_number"], 6)

    def test_gua_five_is_mapped_by_sex(self):
        self.assertEqual(run_minggua("1995", "--sex", "male")["gua_number"], 2)
        self.assertEqual(run_minggua("1999", "--sex", "female")["gua_number"], 8)


if __name__ == "__main__":
    unittest.main()
