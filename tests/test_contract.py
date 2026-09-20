"""Contract tests for the generic Simulation Matrix."""
from pathlib import Path
import unittest
from simulation_matrix.config import load_matrix
from simulation_matrix.cases.synthetic import load_case
from simulation_matrix import runner

ROOT=Path(__file__).resolve().parents[1]

class MatrixContractTests(unittest.TestCase):
    def test_matrix_loads_from_repository_path(self):
        matrix=load_matrix(ROOT/"simulation_matrix"/"matrix.json")
        self.assertEqual(matrix["matrix_version"],"V2.1")
        self.assertEqual(matrix["seed"],42)
        self.assertFalse(matrix["scientific_experiment"])

    def test_runner_uses_repository_root(self):
        self.assertEqual(runner.ROOT,ROOT)

    def test_synthetic_adapter_requires_explicit_case(self):
        adapter=load_case("synthetic.contract")
        matrix=load_matrix(ROOT/"simulation_matrix"/"matrix.json")
        for spec in matrix["pipeline"]:
            if not spec["enabled"]:
                continue
            result=adapter.run_stage(spec["stage"],seed=matrix["seed"],context={"matrix":matrix,"project_id":"CONTRACT_TEST"})
            self.assertTrue(result.passed,spec["stage"])
            self.assertEqual(result.status,"PASS")
            self.assertEqual(result.details["project_id"],"CONTRACT_TEST")

if __name__=="__main__": unittest.main()
