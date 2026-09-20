import json
import unittest
from pathlib import Path

from simulation_matrix.master_runner import load_strategy, run

class TestMasterStrategy(unittest.TestCase):
    def test_strategy_is_frozen_to_seed_42_and_million_capacity(self):
        strategy = load_strategy()
        self.assertEqual(strategy["seed"], 42)
        self.assertEqual(strategy["maximum_total_simulation_runs"], 1000000)
        self.assertTrue(strategy["checkpoint_every_batch"])
        self.assertTrue(strategy["never_change_protocol_from_results"])

    def test_both_cases_are_routed(self):
        strategy = load_strategy()
        self.assertIn("BHD", strategy["case_pipelines"])
        self.assertIn("miRNA21", strategy["case_pipelines"])

    def test_master_runner_never_invents_science(self):
        report = run()
        self.assertTrue(report["promotion_rule_enforced"])
        self.assertTrue(report["audit_invariant_enforced"])
        self.assertEqual(report["scientific_runs_executed"], 0)
        self.assertFalse(report["scientific_execution"])
        self.assertIn(report["status"], {"MASTER_AUDIT_COMPLETE", "INPUT_FAILURE", "IMPLEMENTATION_FAILURE", "INFRASTRUCTURE_FAILURE"})

if __name__ == "__main__":
    unittest.main()
