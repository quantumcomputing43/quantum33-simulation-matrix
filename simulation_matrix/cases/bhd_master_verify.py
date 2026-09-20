"""Repository-native BHD master-strategy verification."""
from __future__ import annotations
import json
from pathlib import Path

REQUIRED_ORDER = [
    "PROVENANCE_RECONSTRUCTION", "MODEL_DEFINITION_AUDIT", "NUMERICAL_VALIDATION",
    "ADVERSARIAL_STRESS", "IDENTIFIABILITY", "ROBUSTNESS", "OBSERVABLE_DERIVATION",
    "H0_H1_H2_GENERATION_AUDIT", "FALSIFICATION", "SURVIVOR_CHECK",
]
REQUIRED_LEGACY_FLAGS = (
    "TFIM_N4_open_chain", "pure_state_QFI", "historical_benchmark_audit",
    "finite_difference_convergence", "metric_PSD_check", "OBS_C_R2_diagnostic_only",
    "H0_epsilon_zero", "H1_epsilon_nonzero", "H2_classical_nuisance",
    "primary_observable_gate", "no_post_hoc_changes",
)

def run():
    root = Path(__file__).parents[2]
    strategy = json.loads((root / "simulation_matrix/cases/bhd_master_strategy.json").read_text(encoding="utf-8"))
    protocol = json.loads((root / "simulation_matrix/cases/bhd_protocol.json").read_text(encoding="utf-8"))

    order_ok = strategy.get("execution_order") == REQUIRED_ORDER
    legacy = strategy.get("legacy_steps_integrated", {})
    legacy_ok = all(bool(legacy.get(name)) for name in REQUIRED_LEGACY_FLAGS)
    budget_ok = strategy.get("simulation_budget", {}).get("maximum_requested_runs", 0) >= 1_000_000
    protocol_version_ok = protocol.get("protocol_version") == "BHD-P1.3"
    scientific_gate_closed = protocol.get("execution_gate", {}).get("allow_scientific_execution") is False
    primary_observable_unset = protocol.get("model_scope", {}).get("observable_signature") == "TBD"

    structural_ok = order_ok and legacy_ok and budget_ok and protocol_version_ok and scientific_gate_closed and primary_observable_unset
    return {
        "case_id": "bhd.master_strategy_verification",
        "status": "PASS" if structural_ok else "IMPLEMENTATION_FAILURE",
        "strategy_order_valid": order_ok,
        "legacy_steps_complete": legacy_ok,
        "million_run_capacity_registered": budget_ok,
        "protocol_version_valid": protocol_version_ok,
        "scientific_gate_closed": scientific_gate_closed,
        "primary_observable_unset": primary_observable_unset,
        "scientific_execution": False,
        "scientific_gate": "CLOSED",
        "interpretation": "PASS means structural/audit integrity only; it is not scientific evidence.",
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
