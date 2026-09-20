import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from simulation_matrix import adversarial_stress, falsification
from simulation_matrix.numerics import evaluate_profile, normalize
from simulation_matrix.runner import ROOT, run_matrix


class SimulationMatrixTests(unittest.TestCase):
    def test_stages_pass_with_shared_numerics(self):
        self.assertEqual(falsification.run_falsification()["status"], "PASS")
        self.assertEqual(adversarial_stress.run_adversarial_stress()["status"], "PASS")

    def test_evaluate_profile_rejects_invalid_grids(self):
        with self.assertRaises(ValueError):
            evaluate_profile(falsification.gaussian, domain=0.0, n_points=8193)
        with self.assertRaises(ValueError):
            evaluate_profile(falsification.gaussian, domain=12.0, n_points=2)
        with self.assertRaises(ValueError):
            normalize(np.zeros(3), 1.0)

    def test_runner_persists_and_resumes_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "matrix.json").write_text(
                (ROOT / "matrix.json").read_text(encoding="utf-8"), encoding="utf-8"
            )
            first = run_matrix(root)
            second = run_matrix(root)
            self.assertEqual(first["status"], "PASS")
            self.assertTrue(second["resumed"])
            self.assertEqual(
                json.loads((root / "results" / "latest_V1.1.json").read_text())["status"],
                "PASS",
            )


if __name__ == "__main__":
    unittest.main()
