import unittest
from dropshipping.simulate import evaluate, run

class ZeroBudgetSimulationTests(unittest.TestCase):
    def test_upfront_payment_blocks_zero_budget_even_if_margin_positive(self):
        result = evaluate({
            "sale_price_mad": 249, "supplier_cost_mad": 100,
            "shipping_mad": 25, "platform_fee_mad": 0,
            "payment_fee_rate": 0.03, "return_reserve_mad": 5,
            "upfront_cash_required_mad": 100,
        })
        self.assertTrue(result["positive_contribution"])
        self.assertFalse(result["zero_upfront_cash_feasible"])
        self.assertFalse(result["passes_illustrative_zero_budget_gate"])

    def test_positive_margin_and_zero_upfront_passes_illustrative_gate(self):
        result = evaluate({
            "sale_price_mad": 249, "supplier_cost_mad": 100,
            "shipping_mad": 25, "platform_fee_mad": 0,
            "payment_fee_rate": 0.03, "return_reserve_mad": 5,
            "upfront_cash_required_mad": 0,
        })
        self.assertTrue(result["positive_contribution"])
        self.assertTrue(result["passes_illustrative_zero_budget_gate"])

    def test_stress_case_is_not_silently_called_success(self):
        result = run()
        self.assertFalse(result["market_validated"])
        self.assertFalse(result["real_supplier_verified"])
        self.assertEqual(result["real_orders"], 0)
        self.assertEqual(result["revenue_mad"], 0)
        self.assertFalse(result["scenarios"]["stress_illustrative"]["passes_illustrative_zero_budget_gate"])

if __name__ == "__main__":
    unittest.main()
