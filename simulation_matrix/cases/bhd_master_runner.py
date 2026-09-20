"""BHD master pre-experiment orchestrator.

Runs every currently executable validity layer, aggregates their outputs, and
never opens scientific execution when the protocol contract is incomplete.
"""
from __future__ import annotations
import json
from pathlib import Path

from simulation_matrix.cases.bhd import BHDProtocolIncomplete, execution_ready, load_protocol
from simulation_matrix.cases.bhd_master_verify import run as verify_strategy
from simulation_matrix.cases.bhd_observable_audit import run as observable_audit
from simulation_matrix.cases.bhd_preexperiment import run as tfim_audit

ROOT = Path(__file__).parents[2]
PROTOCOL_PATH = ROOT / "simulation_matrix/cases/bhd_protocol.json"


def _protocol_gate():
    try:
        protocol = load_protocol(PROTOCOL_PATH)
        return {
            "load_status": "PASS",
            "execution_ready": bool(execution_ready(protocol)),
            "scientific_execution_allowed": bool(execution_ready(protocol)),
        }
    except BHDProtocolIncomplete as exc:
        return {
            "load_status": "IMPLEMENTATION_FAILURE",
            "execution_ready": False,
            "scientific_execution_allowed": False,
            "error": str(exc),
        }


def run() -> dict:
    strategy = verify_strategy()
    tfim = tfim_audit()
    observable = observable_audit()
    protocol = _protocol_gate()

    gate_open = (
        strategy["status"] == "PASS"
        and tfim["status"] == "PASS"
        and observable["status"] == "PASS"
        and protocol["execution_ready"]
    )

    stages = {
        "PROVENANCE_RECONSTRUCTION": "REGISTERED_ONLY",
        "MODEL_DEFINITION_AUDIT": tfim["status"],
        "NUMERICAL_VALIDATION": tfim["status"],
        "ADVERSARIAL_STRESS": "NOT_EXECUTED_SCIENTIFIC_GATE_CLOSED",
        "IDENTIFIABILITY": "DIAGNOSTIC_ONLY",
        "ROBUSTNESS": "NOT_EXECUTED_SCIENTIFIC_GATE_CLOSED",
        "OBSERVABLE_DERIVATION": observable["gate"]["decision"],
        "H0_H1_H2_GENERATION_AUDIT": "NOT_REGISTERED",
        "FALSIFICATION": "NOT_EXECUTED_SCIENTIFIC_GATE_CLOSED",
        "SURVIVOR_CHECK": "BLOCKED",
    }

    status = "READY_FOR_SCIENTIFIC_EXECUTION" if gate_open else "PREEXPERIMENT_VALIDATION_COMPLETE_GATE_CLOSED"

    report = {
        "case_id": "bhd.master_preexperiment",
        "status": status,
        "scientific_execution": False,
        "strategy_verification": strategy,
        "tfim_qfi_validation": tfim,
        "observable_audit": observable,
        "protocol_gate": protocol,
        "stage_results": stages,
        "promotion_rule_enforced": True,
        "scientific_runs_requested": 0,
        "scientific_runs_executed": 0,
        "next_gate_condition": "Complete and independently audit the primary observable plus H0/H1/H2 generation contracts before any scientific batch.",
    }

    out = ROOT / "results" / "bhd_master_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
