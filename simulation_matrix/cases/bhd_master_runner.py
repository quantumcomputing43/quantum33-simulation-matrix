"""BHD master pre-experiment orchestrator.

Runs the registered BHD validity layers plus the formal audit-input contract.
The audit input is read and validated as an immutable audit specification; it
does not open scientific execution by itself.
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
AUDIT_INPUT_PATH = ROOT / "simulation_matrix/cases/bhd_audit_input_v1.json"


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


def _audit_input():
    try:
        data = json.loads(AUDIT_INPUT_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"status": "INPUT_FAILURE", "error": "Missing BHD audit input contract."}
    except json.JSONDecodeError as exc:
        return {"status": "IMPLEMENTATION_FAILURE", "error": f"Invalid audit input JSON: {exc}"}

    required = [
        "audit_input_version",
        "case_id",
        "mission",
        "frozen_rules",
        "known_state",
        "known_findings_to_audit",
        "required_audit_order",
        "adversarial_requirements",
        "decision_policy",
        "required_output",
    ]
    missing = [key for key in required if key not in data]
    findings = data.get("known_findings_to_audit", [])
    if missing or not findings:
        return {
            "status": "INPUT_FAILURE",
            "error": "Audit input contract is incomplete.",
            "missing_fields": missing,
            "finding_count": len(findings),
        }

    ids = [item.get("id") for item in findings]
    duplicate_ids = sorted({x for x in ids if ids.count(x) > 1 and x is not None})
    malformed = [
        item.get("id", "<missing-id>")
        for item in findings
        if not item.get("problem") or not item.get("audit_question") or not item.get("pass_condition")
    ]
    return {
        "status": "PASS" if not duplicate_ids and not malformed else "INPUT_FAILURE",
        "version": data["audit_input_version"],
        "case_id": data["case_id"],
        "finding_count": len(findings),
        "finding_ids": ids,
        "critical_findings": [x["id"] for x in findings if x.get("severity") == "CRITICAL"],
        "duplicate_ids": duplicate_ids,
        "malformed_findings": malformed,
        "scientific_execution_requested_by_input": bool(
            data.get("scientific_execution", {}).get("allow", False)
        ),
        "scientific_execution_forced_closed": True,
    }


def run() -> dict:
    strategy = verify_strategy()
    tfim = tfim_audit()
    observable = observable_audit()
    protocol = _protocol_gate()
    audit_input = _audit_input()

    gate_open = (
        strategy["status"] == "PASS"
        and tfim["status"] == "PASS"
        and observable["status"] == "PASS"
        and protocol["execution_ready"]
        and audit_input["status"] == "PASS"
    )

    stages = {
        "PROVENANCE_RECONSTRUCTION": "REGISTERED_ONLY",
        "MODEL_DEFINITION_AUDIT": tfim["status"],
        "NUMERICAL_VALIDATION": tfim["status"],
        "OBSERVABLE_DERIVATION": observable["gate"]["decision"],
        "AUDIT_INPUT_VALIDATION": audit_input["status"],
        "H0_H1_H2_GENERATION_AUDIT": "NOT_REGISTERED",
        "LEAKAGE_AND_CIRCULARITY": "PENDING_PRIMARY_OBSERVABLE",
        "IDENTIFIABILITY": "DIAGNOSTIC_ONLY",
        "ADVERSARIAL_STRESS": "NOT_EXECUTED_SCIENTIFIC_GATE_CLOSED",
        "ROBUSTNESS": "NOT_EXECUTED_SCIENTIFIC_GATE_CLOSED",
        "FALSIFICATION": "NOT_EXECUTED_SCIENTIFIC_GATE_CLOSED",
        "SURVIVOR_CHECK": "BLOCKED",
    }

    status = (
        "READY_FOR_SCIENTIFIC_EXECUTION"
        if gate_open
        else "PREEXPERIMENT_AUDIT_COMPLETE_GATE_CLOSED"
    )

    report = {
        "case_id": "bhd.master_preexperiment",
        "status": status,
        "scientific_execution": False,
        "strategy_verification": strategy,
        "tfim_qfi_validation": tfim,
        "observable_audit": observable,
        "protocol_gate": protocol,
        "audit_input": audit_input,
        "stage_results": stages,
        "promotion_rule_enforced": True,
        "scientific_runs_requested": 0,
        "scientific_runs_executed": 0,
        "next_gate_condition": (
            "Resolve all critical audit findings, independently register the primary "
            "observable and H0/H1/H2 generators, then pass leakage, identifiability, "
            "robustness and falsification gates."
        ),
    }

    out = ROOT / "results" / "bhd_master_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
