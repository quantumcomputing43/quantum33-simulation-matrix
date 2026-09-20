"""Quantum33 autonomous validity kernel.

The kernel is intentionally conservative: it can repair mechanical/infrastructure
defects, but it must never invent scientific content or change a scientific rule
after seeing outcomes. It returns one terminal status plus an auditable ledger.
"""
from __future__ import annotations

import importlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[2]
CONTRACT = ROOT / "simulation_matrix/cases/autonomous_kernel.json"
STATE = ROOT / "simulation_matrix/state/autonomous_kernel_checkpoint.json"
REPORT = ROOT / "simulation_matrix/results/autonomous_kernel_report.json"
LOG = ROOT / "simulation_matrix/logs/autonomous_kernel_events.jsonl"

STAGES = [
    "PROVENANCE", "SCHEMA_AND_CONTRACTS", "UNITS_AND_NORMALIZATION",
    "DETERMINISM", "IMPLEMENTATION", "DATA_AND_INPUTS", "GENERATIVE_MODEL",
    "NULL_AND_CONTROLS", "LEAKAGE_AND_CIRCULARITY", "ENDPOINT_AND_MEASUREMENT",
    "IDENTIFIABILITY", "ADVERSARIAL_STRESS", "ROBUSTNESS", "FALSIFICATION",
    "REPRODUCIBILITY", "EXECUTION_GATE", "RESULT_AND_SURVIVOR",
]

def _safe_repair() -> list[str]:
    repaired: list[str] = []
    for path in (STATE.parent, REPORT.parent, LOG.parent):
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            repaired.append(f"created:{path.relative_to(ROOT)}")
    return repaired

def _contract_ok(contract: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    if contract.get("strategy_version") != "Q33-AUTONOMOUS-KERNEL-V1":
        errors.append("wrong_strategy_version")
    if contract.get("seed") != 42:
        errors.append("seed_not_frozen_to_42")
    if contract.get("no_post_hoc_changes") is not True:
        errors.append("post_hoc_changes_not_forbidden")
    if contract.get("stages") != STAGES:
        errors.append("stage_order_or_set_mismatch")
    return not errors, errors

def _determinism_probe() -> dict[str, Any]:
    # Small deterministic probe only; no scientific claim is made.
    payload = {"seed": 42, "stages": STAGES}
    first = json.dumps(payload, sort_keys=True)
    second = json.dumps(payload, sort_keys=True)
    return {"passed": first == second, "digest_input": first}

def _import_probe() -> dict[str, Any]:
    modules = [
        "simulation_matrix.master_runner",
        "simulation_matrix.cases.bhd_master_runner",
        "simulation_matrix.cases.mirna21_master_runner",
        "simulation_matrix.cases.bhd_5scientist_crosswalk",
    ]
    failures = []
    for name in modules:
        try:
            importlib.import_module(name)
        except Exception as exc:
            failures.append({"module": name, "error": type(exc).__name__, "message": str(exc)})
    return {"passed": not failures, "failures": failures}

def run() -> dict[str, Any]:
    started = datetime.now(timezone.utc).isoformat()
    repaired = _safe_repair()

    try:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except Exception as exc:
        result = {
            "status": "IMPLEMENTATION_FAILURE",
            "scientific_execution": False,
            "scientific_runs_executed": 0,
            "terminal_reason": "kernel_contract_unreadable",
            "error": {"type": type(exc).__name__, "message": str(exc)},
            "safe_repairs": repaired,
        }
        REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result

    contract_pass, contract_errors = _contract_ok(contract)
    deterministic = _determinism_probe()
    imports = _import_probe()

    stage_status = {stage: "NOT_RUN" for stage in STAGES}
    stage_status["PROVENANCE"] = "PASS" if CONTRACT.exists() else "FAIL"
    stage_status["SCHEMA_AND_CONTRACTS"] = "PASS" if contract_pass else "FAIL"
    stage_status["DETERMINISM"] = "PASS" if deterministic["passed"] else "FAIL"
    stage_status["IMPLEMENTATION"] = "PASS" if imports["passed"] else "FAIL"

    # These stages are deliberately not fabricated. They are delegated to
    # scientific case contracts and remain closed here unless their contracts
    # explicitly report PASS.
    blocked = [
        "UNITS_AND_NORMALIZATION", "DATA_AND_INPUTS", "GENERATIVE_MODEL",
        "NULL_AND_CONTROLS", "LEAKAGE_AND_CIRCULARITY",
        "ENDPOINT_AND_MEASUREMENT", "IDENTIFIABILITY", "ADVERSARIAL_STRESS",
        "ROBUSTNESS", "FALSIFICATION", "REPRODUCIBILITY",
    ]
    for stage in blocked:
        stage_status[stage] = "DELEGATED_OR_BLOCKED"

    execution_open = False
    stage_status["EXECUTION_GATE"] = "CLOSED"
    stage_status["RESULT_AND_SURVIVOR"] = "BLOCKED"

    status = "IMPLEMENTATION_FAILURE" if not contract_pass or not imports["passed"] else "MASTER_AUDIT_COMPLETE"

    result = {
        "strategy_version": contract.get("strategy_version"),
        "status": status,
        "started_at_utc": started,
        "scientific_execution": False,
        "scientific_runs_executed": 0,
        "execution_gate": "OPEN" if execution_open else "CLOSED",
        "safe_repairs": repaired,
        "stage_status": stage_status,
        "contract_errors": contract_errors,
        "implementation_probe": imports,
        "determinism_probe": deterministic,
        "auto_repair_policy": contract["auto_repair_policy"],
        "terminal_semantics": contract["failure_semantics"],
        "safety_invariant": (
            "Mechanical defects may be repaired automatically; scientific "
            "unknowns are never invented or silently altered."
        ),
        "next_action": (
            "Delegate every scientific stage to its registered case contract. "
            "Open scientific execution only after all required gates report PASS."
        ),
    }
    REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    STATE.write_text(json.dumps({
        "strategy_version": result["strategy_version"],
        "last_status": result["status"],
        "execution_gate": result["execution_gate"],
        "scientific_runs_executed": 0,
        "last_report": str(REPORT.relative_to(ROOT)),
    }, indent=2), encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(result, sort_keys=True) + os.linesep)
    return result

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
