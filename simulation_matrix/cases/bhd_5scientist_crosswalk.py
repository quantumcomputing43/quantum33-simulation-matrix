"""Deterministic BHD 5-scientist methodological crosswalk audit.

This is a validity audit, not a historical-theory simulation. It cannot open
scientific execution and cannot change BHD hypotheses, observables, thresholds,
or controls based on outcomes.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).parents[2]
CONTRACT = ROOT / "simulation_matrix/cases/bhd_5scientist_crosswalk.json"

CURRENT_BHD_STATE = {
    "primary_observable_registered": False,
    "h0_h1_h2_generators_registered": False,
    "independent_forward_map_registered": False,
    "falsification_statistic_registered": False,
    "non_circular_measurement_contract": False,
}

def run() -> dict:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    gates = contract["fixed_gates"]

    route_gate_requirements = {
        "TESLA": {
            "INDEPENDENT_PRIMARY_OBSERVABLE": False,
            "H0_H1_H2_PRESERVATION": True,
            "INDEPENDENT_FORWARD_MAP": False,
            "PRE_REGISTERED_FALSIFICATION": False,
            "NON_CIRCULAR_MEASUREMENT": False,
        },
        "EINSTEIN": {
            "INDEPENDENT_PRIMARY_OBSERVABLE": False,
            "H0_H1_H2_PRESERVATION": True,
            "INDEPENDENT_FORWARD_MAP": False,
            "PRE_REGISTERED_FALSIFICATION": False,
            "NON_CIRCULAR_MEASUREMENT": True,
        },
        "HEISENBERG": {
            "INDEPENDENT_PRIMARY_OBSERVABLE": False,
            "H0_H1_H2_PRESERVATION": True,
            "INDEPENDENT_FORWARD_MAP": False,
            "PRE_REGISTERED_FALSIFICATION": False,
            "NON_CIRCULAR_MEASUREMENT": True,
        },
        "BOHR": {
            "INDEPENDENT_PRIMARY_OBSERVABLE": False,
            "H0_H1_H2_PRESERVATION": True,
            "INDEPENDENT_FORWARD_MAP": False,
            "PRE_REGISTERED_FALSIFICATION": False,
            "NON_CIRCULAR_MEASUREMENT": True,
        },
        "SCHRODINGER": {
            "INDEPENDENT_PRIMARY_OBSERVABLE": False,
            "H0_H1_H2_PRESERVATION": True,
            "INDEPENDENT_FORWARD_MAP": False,
            "PRE_REGISTERED_FALSIFICATION": False,
            "NON_CIRCULAR_MEASUREMENT": False,
        },
    }

    results = {}
    for scientist in [p["id"] for p in contract["principles"]]:
        checks = route_gate_requirements[scientist]
        passed = [g for g in gates if checks[g]]
        failed = [g for g in gates if not checks[g]]
        results[scientist] = {
            "status": "SURVIVED" if not failed else "BLOCKED",
            "passed_gates": passed,
            "failed_gates": failed,
        }

    return {
        "case_id": "bhd.5scientist_crosswalk",
        "strategy_version": contract["strategy_version"],
        "status": "CROSSWALK_AUDIT_COMPLETE",
        "scientific_execution": False,
        "scientific_runs_executed": 0,
        "fixed_gates": gates,
        "results": results,
        "closest_methodological_alignment": [
            "HEISENBERG",
            "BOHR"
        ],
        "alignment_interpretation": (
            "Heisenberg/Bohr align most directly with the current BHD blocker "
            "because the blocker is operational: an independently defined "
            "primary observable and physical measurement contract are missing. "
            "This is methodological alignment, not evidence that BHD is true."
        ),
        "critical_result": "NO_SCIENTIST_ROUTE_SURVIVES_ALL_FIXED_GATES",
        "next_justified_operation": (
            "Use the Heisenberg/Bohr observable-and-measurement route as a "
            "registered design path to attempt ISSUE-001, then independently "
            "audit H0/H1/H2, forward mapping, falsification and identifiability."
        ),
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
