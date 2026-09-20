"""Automatic pre-experiment audit for BHD observable candidates."""
from __future__ import annotations
import json
from pathlib import Path

CANDIDATES = (
    "trace_g_info",
    "det_g_info",
    "principal_eigenvalue_g_info",
    "directional_qfi_fixed_path",
)

REQUIRED_FOR_PRIMARY = (
    "explicit_forward_map",
    "h0_generation_rule",
    "h1_generation_rule",
    "h2_generation_rule",
    "units_normalization",
    "independent_null_generation",
    "fixed_falsification_statistic",
)

def audit_candidate(name: str) -> dict:
    if name in {"trace_g_info", "det_g_info", "principal_eigenvalue_g_info"}:
        reason = "Metric scalar is computable, but no registered measurement/epsilon forward map."
    else:
        reason = "A fixed perturbation direction is not yet a registered physical measurement map."
    return {
        "candidate": name,
        "status": "DIAGNOSTIC_ONLY",
        "primary_observable": False,
        "missing_contract_items": list(REQUIRED_FOR_PRIMARY),
        "reason": reason,
    }

def run() -> dict:
    audits = [audit_candidate(c) for c in CANDIDATES]
    return {
        "case_id": "bhd.preexperiment.observable_audit",
        "scientific_execution": False,
        "status": "PASS",
        "primary_observable_selected": False,
        "audits": audits,
        "gate": {
            "scientific_execution_allowed": False,
            "decision": "NO_PRIMARY_OBSERVABLE_YET",
            "reason": "All current metric-derived candidates remain diagnostics until H0/H1/H2 observable generation rules are independently registered.",
        },
    }

if __name__ == "__main__":
    root = Path(__file__).parents[2]
    out = root / "results" / "bhd_observable_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    result = run()
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
