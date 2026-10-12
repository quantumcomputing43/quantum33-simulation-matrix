"""Deterministic unit-economics sensitivity check; inputs are illustrative, not market facts."""
from __future__ import annotations
import json
from pathlib import Path

SCENARIOS = {
    "optimistic_illustrative": {
        "sale_price_mad": 249.0, "supplier_cost_mad": 100.0,
        "shipping_mad": 25.0, "platform_fee_mad": 0.0,
        "payment_fee_rate": 0.03, "return_reserve_mad": 5.0,
        "upfront_cash_required_mad": 0.0,
    },
    "base_illustrative": {
        "sale_price_mad": 249.0, "supplier_cost_mad": 140.0,
        "shipping_mad": 35.0, "platform_fee_mad": 0.0,
        "payment_fee_rate": 0.03, "return_reserve_mad": 20.0,
        "upfront_cash_required_mad": 140.0,
    },
    "stress_illustrative": {
        "sale_price_mad": 199.0, "supplier_cost_mad": 150.0,
        "shipping_mad": 50.0, "platform_fee_mad": 10.0,
        "payment_fee_rate": 0.04, "return_reserve_mad": 35.0,
        "upfront_cash_required_mad": 150.0,
    },
}

def evaluate(inputs: dict[str, float]) -> dict:
    price = float(inputs["sale_price_mad"])
    costs = sum(float(inputs[k]) for k in (
        "supplier_cost_mad", "shipping_mad", "platform_fee_mad",
        "return_reserve_mad"))
    payment_fee = price * float(inputs["payment_fee_rate"])
    contribution = round(price - costs - payment_fee, 2)
    upfront = float(inputs["upfront_cash_required_mad"])
    return {
        "contribution_mad": contribution,
        "upfront_cash_required_mad": round(upfront, 2),
        "positive_contribution": contribution > 0,
        "zero_upfront_cash_feasible": upfront <= 0,
        "passes_illustrative_zero_budget_gate": contribution > 0 and upfront <= 0,
        "evidence_status": "ILLUSTRATIVE_ONLY_NOT_MARKET_VALIDATION",
    }

def run() -> dict:
    results = {name: evaluate(values) for name, values in SCENARIOS.items()}
    return {
        "project_id": "Q33_DROPSHIPPING_ZERO_BUDGET",
        "status": "SENSITIVITY_COMPLETE_NOT_MARKET_VALIDATION",
        "market_validated": False,
        "real_supplier_verified": False,
        "real_payment_route_verified": False,
        "real_orders": 0,
        "revenue_mad": 0,
        "scenarios": results,
        "interpretation": (
            "Illustrative sensitivity only. Do not launch until real supplier, "
            "Morocco eligibility, fees, payout, returns, and zero-upfront terms are verified."
        ),
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
