import unittest
from simulation_matrix.cases.bhd_master_verify import run

class BHDMasterStrategyTests(unittest.TestCase):
    def test_master_strategy_is_complete_and_gated(self):
        r = run()
        self.assertEqual(r["status"], "PASS")
        self.assertTrue(r["strategy_order_valid"])
        self.assertTrue(r["legacy_steps_complete"])
        self.assertTrue(r["million_run_capacity_registered"])
        self.assertEqual(r["scientific_gate"], "CLOSED")

if __name__ == "__main__":
    unittest.main()
