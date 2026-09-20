"""BHD master pre-experiment orchestrator.

Runs the registered BHD validity layers plus the formal audit-input contract.
The audit input is immutable: it records problems to test and can never open
scientific execution by itself.
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
        return {"load_status": "PASS", "execution_ready": bool(execution_ready(protocol)),
                "scientific_execution_allowed": bool(execution_ready(protocol))}
    except BHDProtocolIncomplete as exc:
        return {"load_status": "IMPLEMENTATION_FAILURE", "execution_ready": False,
                "scientific_execution_allowed": False, "error": str(exc)}


def _audit_input():
    try:
        data = json.loads(AUDIT_INPUT_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"status": "INPUT_FAILURE", "error": "Missing BHD audit input contract."}
    except json.JSONDecodeError as exc:
        return {"status": "IMPLEMENTATION_FAILURE", "error": f"Invalid audit input JSON: {exc}"}

    required = ["audit_input_version", "case_id", "mission", "frozen_rules", "known_state",
                "known_findings_to_audit", "required_audit_order", "adversarial_requirements",
                "decision_policy", "required_output"]
    missing = [key for key in required if key not in data]
    findings = data.get("known_findings_to_audit", [])
    ids = [item.get("id") for item in findings]
    duplicate_ids = sorted({x for x in ids if ids.count(x) > 1 and x is not None})
    malformed = [item.get("id", "<missing-id>") for item in findings
                 if not item.get("problem") or not item.get("audit_question") or not item.get("pass_condition")]
    invalid_severity = [item.get("id", "<missing-id>") for item in findings
                        if item.get("severity") not in {"CRITICAL", "HIGH", "MEDIUM", "LOW"}]
    valid = not missing and bool(findings) and not duplicate_ids and not malformed and not invalid_severity
    return {
        "status": "PASS" if valid else "INPUT_FAILURE",
        "version": data.get("audit_input_version"), "case_id": data.get("case_id"),
        "finding_count": len(findings), "finding_ids": ids,
        "critical_findings": [x["id"] for x in findings if x.get("severity") == "CRITICAL"],
        "duplicate_ids": duplicate_ids, "malformed_findings": malformed,
        "invalid_severity": invalid_severity,
        "scientific_execution_requested_by_input": bool(data.get("scientific_execution", {}).get("allow", False)),
        "scientific_execution_forced_closed": True,
        "findings": findings, "required_audit_order": data.get("required_audit_order", []),
    }


def _audit_findings(audit_input: dict, tfim: dict, observable: dict) -> dict:
    results = {}
    for item in audit_input.get("findings", []):
        fid = item["id"]
        if fid == "BHD-ISSUE-001":
            passed = bool(observable.get("primary_observable_selected"))
            reason = "Primary observable contract is registered." if passed else "No independently registered primary observable."
        elif fid == "BHD-ISSUE-002":
            passed, reason = False, "H0/H1/H2 independent generators are not registered."
        elif fid == "BHD-ISSUE-003":
            passed, reason = False, "No independently testable g_info to physical hidden-sector/spacetime forward map is registered."
        elif fid == "BHD-ISSUE-004":
            passed, reason = False, "All current metric-derived candidates remain diagnostic-only."
        elif fid == "BHD-ISSUE-005":
            passed = tfim.get("historical_benchmark", {}).get("status") == "MATCH"
            reason = "Historical benchmark conventions match." if passed else "Historical benchmark convention mismatch remains unresolved."
        elif fid == "BHD-ISSUE-006":
            passed, reason = True, "Numerical checks are explicitly separated from physical scientific validity."
        elif fid == "BHD-ISSUE-007":
            passed, reason = False, "Identifiability has not been demonstrated for a final primary observable against the declared nuisance model."
        elif fid == "BHD-ISSUE-008":
            passed, reason = False, "No pre-registered falsification statistic and threshold exists."
        elif fid == "BHD-ISSUE-009":
            passed, reason = True, "No scientific batches are executed while the validity gate is closed."
        else:
            passed, reason = False, "Finding is not mapped to an implemented audit check."
        results[fid] = {"status": "PASS" if passed else "FAIL", "severity": item["severity"],
                        "problem": item["problem"], "audit_question": item["audit_question"],
                        "pass_condition": item["pass_condition"], "reason": reason}
    blocking = [fid for fid, r in results.items() if r["status"] == "FAIL" and r["severity"] == "CRITICAL"]
    return {"status": "PASS" if not blocking else "FAIL", "results": results,
            "blocking_issues": blocking,
            "passed_issues": [fid for fid, r in results.items() if r["status"] == "PASS"]}


def run() -> dict:
    strategy, tfim, observable, protocol = verify_strategy(), tfim_audit(), observable_audit(), _protocol_gate()
    audit_input = _audit_input()
    finding_audit = (_audit_findings(audit_input, tfim, observable) if audit_input["status"] == "PASS"
                     else {"status": "BLOCKED", "results": {}, "blocking_issues": ["AUDIT_INPUT_INVALID"], "passed_issues": []})
    gate_open = (strategy["status"] == "PASS" and tfim["status"] == "PASS" and observable["status"] == "PASS"
                 and protocol["execution_ready"] and audit_input["status"] == "PASS" and finding_audit["status"] == "PASS")
    stages = {
        "PROVENANCE_RECONSTRUCTION": "REGISTERED_ONLY", "MODEL_DEFINITION_AUDIT": tfim["status"],
        "NUMERICAL_VALIDATION": tfim["status"], "OBSERVABLE_DERIVATION": observable["gate"]["decision"],
        "AUDIT_INPUT_VALIDATION": audit_input["status"],
        "H0_H1_H2_GENERATION_AUDIT": "NOT_REGISTERED", "LEAKAGE_AND_CIRCULARITY": "PENDING_PRIMARY_OBSERVABLE",
        "IDENTIFIABILITY": "DIAGNOSTIC_ONLY", "ADVERSARIAL_STRESS": "NOT_EXECUTED_SCIENTIFIC_GATE_CLOSED",
        "ROBUSTNESS": "NOT_EXECUTED_SCIENTIFIC_GATE_CLOSED", "FALSIFICATION": "NOT_EXECUTED_SCIENTIFIC_GATE_CLOSED",
        "SURVIVOR_CHECK": "BLOCKED",
    }
    report = {
        "case_id": "bhd.master_preexperiment",
        "status": "READY_FOR_SCIENTIFIC_EXECUTION" if gate_open else "PREEXPERIMENT_VALIDATION_COMPLETE_GATE_CLOSED",
        "scientific_execution": False, "strategy_verification": strategy, "tfim_qfi_validation": tfim,
        "observable_audit": observable, "protocol_gate": protocol, "audit_input": audit_input,
        "finding_audit": finding_audit, "stage_results": stages, "promotion_rule_enforced": True,
        "scientific_runs_requested": 0, "scientific_runs_executed": 0,
        "next_gate_condition": "Resolve all critical audit findings, independently register the primary observable and H0/H1/H2 generators, then pass leakage, identifiability, robustness and falsification gates.",
    }
    out = ROOT / "results" / "bhd_master_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
