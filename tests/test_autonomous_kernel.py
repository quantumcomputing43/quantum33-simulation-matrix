import unittest

from simulation_matrix.cases import autonomous_kernel

class TestAutonomousKernel(unittest.TestCase):
    def test_contract_and_stage_order(self):
        contract = __import__("json").loads(autonomous_kernel.CONTRACT.read_text(encoding="utf-8"))
        ok, errors = autonomous_kernel._contract_ok(contract)
        self.assertTrue(ok, errors)
        self.assertEqual(contract["stages"], autonomous_kernel.STAGES)

    def test_kernel_never_opens_scientific_gate_by_itself(self):
        result = autonomous_kernel.run()
        self.assertEqual(result["execution_gate"], "CLOSED")
        self.assertEqual(result["scientific_runs_executed"], 0)
        self.assertFalse(result["scientific_execution"])

    def test_forbidden_repairs_are_present(self):
        contract = __import__("json").loads(autonomous_kernel.CONTRACT.read_text(encoding="utf-8"))
        forbidden = set(contract["auto_repair_policy"]["forbidden"])
        self.assertIn("invent_primary_observable", forbidden)
        self.assertIn("change_threshold_after_observing_results", forbidden)
        self.assertIn("replace_missing_data_with_synthetic_data", forbidden)

if __name__ == "__main__":
    unittest.main()
