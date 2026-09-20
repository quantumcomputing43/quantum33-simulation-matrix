import unittest

from simulation_matrix.cases.mirna21_master_runner import run

class TestMiRNA21MasterRunner(unittest.TestCase):
    def test_scientific_execution_is_closed_until_contracts_pass(self):
        result = run()
        self.assertFalse(result["scientific_execution"])
        self.assertEqual(result["scientific_runs_executed"], 0)
        self.assertIn("leakage_audit", result["required_next_contracts"])
        self.assertIn("null_and_control_generation", result["required_next_contracts"])

if __name__ == "__main__":
    unittest.main()
