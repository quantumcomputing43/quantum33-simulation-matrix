import unittest

from simulation_matrix.cases.bhd_master_runner import run


class BHDMasterRunnerTests(unittest.TestCase):
    def test_master_runner_never_executes_science_when_gate_is_closed(self):
        result = run()
        self.assertFalse(result["scientific_execution"])
        self.assertEqual(result["scientific_runs_executed"], 0)
        self.assertEqual(result["status"], "PREEXPERIMENT_VALIDATION_COMPLETE_GATE_CLOSED")
        self.assertTrue(result["promotion_rule_enforced"])
        self.assertEqual(
            result["stage_results"]["OBSERVABLE_DERIVATION"],
            "NO_PRIMARY_OBSERVABLE_YET",
        )
        self.assertEqual(result["stage_results"]["AUDIT_INPUT_VALIDATION"], "PASS")
        self.assertGreaterEqual(result["audit_input"]["finding_count"], 9)
        self.assertTrue(result["audit_input"]["scientific_execution_forced_closed"])


if __name__ == "__main__":
    unittest.main()
