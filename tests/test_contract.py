"""Contract tests for the generic Simulation Matrix."""
from pathlib import Path
import unittest

from simulation_matrix.config import load_matrix
from simulation_matrix.cases.synthetic import load_case
from simulation_matrix import runner


ROOT = Path(__file__).resolve().parents[1]


class MatrixContractTests(unittest.TestCase):
    def test_matrix_loads_from_repository_root(self):
        matrix = load_matrix(ROOT / "matrix.json")
        self.assertEqual(matrix["matrix_version"], "V2.0")
        self.assertEqual(matrix["seed"], 42)
        self.assertFalse(matrix["scientific_experiment"])

    def test_runner_uses_repository_root(self):
        self.assertEqual(runner.ROOT, ROOT)
        self.assertTrue((runner.ROOT / "matrix.json").is_file())

    def test_synthetic_adapter_passes_all_declared_stages(self):
        adapter = load_case()
        matrix = load_matrix(ROOT / "matrix.json")
        for spec in matrix["pipeline"]:
            if not spec["enabled"]:
                continue
            result = adapter.run_stage(
                spec["stage"],
                seed=matrix["seed"],
                context={"matrix": matrix},
            )
            self.assertTrue(result.passed, spec["stage"])
            self.assertEqual(result.status, "PASS")


if __name__ == "__main__":
    unittest.main()
