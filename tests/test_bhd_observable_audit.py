import unittest
from simulation_matrix.cases.bhd_observable_audit import run

class BHDObservableAuditTests(unittest.TestCase):
    def test_no_unregistered_candidate_becomes_primary(self):
        result = run()
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["primary_observable_selected"])
        self.assertEqual(result["gate"]["decision"], "NO_PRIMARY_OBSERVABLE_YET")
        for item in result["audits"]:
            self.assertFalse(item["primary_observable"])
            self.assertTrue(item["missing_contract_items"])

if __name__ == "__main__":
    unittest.main()
