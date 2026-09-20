import unittest
import numpy as np

from simulation_matrix.cases.bhd_preexperiment import (
    H_VALUES,
    EPS_VALUES,
    qfi_metric,
    convergence_row,
    benchmark_mismatch_audit,
)


class BHDPreExperimentTests(unittest.TestCase):
    def test_metric_is_finite_symmetric_psd(self):
        for h in H_VALUES:
            g = qfi_metric(1.0, h, 1e-5)
            self.assertTrue(np.all(np.isfinite(g)))
            self.assertTrue(np.allclose(g, g.T, atol=1e-10))
            self.assertGreaterEqual(float(np.min(np.linalg.eigvalsh(g))), -1e-9)

    def test_finite_difference_convergence_is_stable(self):
        for h in H_VALUES:
            row = convergence_row(h)
            self.assertTrue(row["numerically_stable"])
            self.assertEqual(set(row["metrics"]), {f"{e:.0e}" for e in EPS_VALUES})

    def test_historical_benchmark_is_not_a_pass_target(self):
        for h in H_VALUES:
            audit = benchmark_mismatch_audit(h)
            self.assertTrue(audit["historical_values_used_as_audit_target_only"])
            self.assertEqual(audit["decision"], "MODEL_DEFINITION_MISMATCH")
            self.assertFalse(audit["match"])


if __name__ == "__main__":
    unittest.main()
