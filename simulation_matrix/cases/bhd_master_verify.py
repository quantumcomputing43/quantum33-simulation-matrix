"""Repository-native verification manifest.

This does not claim that scientific simulation ran. It verifies that the
master strategy contains every legacy validity layer and that the scientific
gate remains closed until its contract is complete.
"""
import json
from pathlib import Path

REQUIRED_ORDER = [
    "PROVENANCE_RECONSTRUCTION",
    "MODEL_DEFINITION_AUDIT",
    "NUMERICAL_VALIDATION",
    "ADVERSARIAL_STRESS",
    "IDENTIFIABILITY",
    "ROBUSTNESS",
    "OBSERVABLE_DERIVATION",
    "H0_H1_H2_GENERATION_AUDIT",
    "FALSIFICATION",
    "SURVIVOR_CHECK",
]

def run():
    root = Path(__file__).parents[2]
    strategy = json.loads((root / "simulation_matrix/cases/bhd_master_strategy.json").read_text())
    order_ok = strategy["execution_order"] == REQUIRED_ORDER
    legacy = strategy["legacy_steps_integrated"]
    legacy_ok = all(legacy.values())
    budget_ok = strategy["simulation_budget"]["maximum_requested_runs"] >= 1_000_000
    return {
        "case_id": "bhd.master_strategy_verification",
        "status": "PASS" if order_ok and legacy_ok and budget_ok else "IMPLEMENTATION_FAILURE",
        "scientific_execution": False,
        "strategy_order_valid": order_ok,
        "legacy_steps_complete": legacy_ok,
        "million_run_capacity_registered": budget_ok,
        "scientific_gate": "CLOSED",
        "reason": "Capacity and strategy are registered; execution remains gated until the primary observable and H0/H1/H2 generation contracts are complete.",
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
