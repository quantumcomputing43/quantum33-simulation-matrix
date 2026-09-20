"""miRNA-21 pre-experiment master adapter.

This adapter centralizes the already-registered miRNA-21 analysis family.
It does not fabricate missing data or silently reopen previously failed
identifiability assumptions.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).parents[2]

REQUIRED_INPUTS = [
    "TCGA_BRCA_694_JOINED_OS.csv",
    "TCGA_BRCA_694_miR21_5p_OS_ANALYSIS.csv",
    "GSE147126_series_matrix (1).txt.gz",
]

FROZEN = {
    "seed": 42,
    "primary_feature": "hsa-mir-21.MIMAT0000076",
    "secondary_feature": "hsa-mir-21.MIMAT0004494",
    "theta": ["ln_C", "ln_Kd", "ln_g", "Gamma0", "eta"],
    "binding_model": "f=C/(C+Kd)",
    "transduction": "delta_omega=g*f",
    "identifiability_audit": {
        "fim_rank": "3/5",
        "condition_number": 2.3021e17,
        "scale_invariance_direction": [0.707, 0.707, 0.0, 0.0, 0.0],
        "profile_likelihood_C_points": 161,
    },
    "cox_checkpoint": {
        "model": "statsmodels PHReg",
        "feature": "mir21_5p_log2",
        "duration": "OS.time",
        "event": "OS",
        "beta": 0.07682606,
        "se": 0.17890758,
        "hr": 1.0799,
        "wald_p": 0.66761935,
    },
    "controls": [
        "Full",
        "PCA25",
        "R3_miR21_only",
        "frozen_R8D",
        "randomized_shuffled_R8D",
    ],
}

def _locate_inputs() -> dict:
    library_hint = "External Library/attached inputs are not visible to GitHub CI."
    found = []
    missing = []
    for name in REQUIRED_INPUTS:
        candidates = [
            ROOT / name,
            ROOT / "data" / name,
            ROOT / "inputs" / name,
        ]
        if any(p.exists() for p in candidates):
            found.append(name)
        else:
            missing.append(name)
    return {"found": found, "missing": missing, "note": library_hint}

def run() -> dict:
    inputs = _locate_inputs()
    # Missing files are an INPUT_FAILURE for executable analysis, not a
    # scientific failure and never a reason to invent or substitute data.
    if inputs["missing"]:
        status = "INPUT_FAILURE"
        gate = "CLOSED"
        scientific_runs = 0
    else:
        # The full scientific execution remains contract-gated. Presence of
        # files alone is insufficient to open analysis.
        status = "PREEXPERIMENT_INPUT_AUDIT_PASS"
        gate = "CLOSED_PENDING_METHOD_AND_NULL_AUDIT"
        scientific_runs = 0

    return {
        "case_id": "mirna21.quantum33",
        "status": status,
        "scientific_execution": False,
        "scientific_runs_requested": 0,
        "scientific_runs_executed": scientific_runs,
        "gate": gate,
        "inputs": inputs,
        "frozen_contract": FROZEN,
        "required_next_contracts": [
            "data_provenance_and_freeze",
            "generative_model_registration",
            "null_and_control_generation",
            "leakage_audit",
            "pre_registered_metrics_and_thresholds",
            "independent_repetition_plan",
            "survivor_check",
        ],
        "principle": "Experiment validity precedes result significance.",
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
