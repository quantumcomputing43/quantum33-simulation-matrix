"""Quantum33 master orchestration layer.

Single routing point for BHD and miRNA-21. The autonomous kernel runs first,
then registered scientific cases. Mechanical failures are surfaced; scientific
gates remain closed unless every registered contract explicitly passes.
"""
from __future__ import annotations
import importlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parents[1]
STRATEGY = ROOT / "simulation_matrix" / "master_strategy.json"
REPORT = ROOT / "results" / "quantum33_master_report.json"
CHECKPOINT = ROOT / "state" / "master_checkpoint.json"
LOG = ROOT / "logs" / "master_event_log.jsonl"

CASES = {
    "AUTONOMOUS_KERNEL": "simulation_matrix.cases.autonomous_kernel",
    "BHD": "simulation_matrix.cases.bhd_master_runner",
    "miRNA21": "simulation_matrix.cases.mirna21_master_runner",
    "BHD_5SCIENTIST_CROSSWALK": "simulation_matrix.cases.bhd_5scientist_crosswalk",
}

TERMINAL_PRIORITY = [
    "INFRASTRUCTURE_FAILURE",
    "IMPLEMENTATION_FAILURE",
    "INPUT_FAILURE",
    "METHOD_FAILURE",
    "SCIENTIFIC_FAILURE",
    "INCONCLUSIVE",
]

def load_strategy() -> dict:
    with STRATEGY.open("r", encoding="utf-8") as f:
        return json.load(f)

def _call_case(module_name: str) -> dict:
    try:
        module = importlib.import_module(module_name)
        return module.run()
    except Exception as exc:
        return {
            "status": "IMPLEMENTATION_FAILURE",
            "scientific_execution": False,
            "scientific_runs_executed": 0,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }

def _aggregate_status(case_results: dict) -> str:
    statuses = {result.get("status") for result in case_results.values()}
    for status in TERMINAL_PRIORITY:
        if status in statuses:
            return status
    return "MASTER_AUDIT_COMPLETE"

def run() -> dict:
    strategy = load_strategy()
    started = datetime.now(timezone.utc).isoformat()
    case_results = {name: _call_case(module) for name, module in CASES.items()}

    scientific_runs = sum(
        int(result.get("scientific_runs_executed", 0))
        for result in case_results.values()
    )
    status = _aggregate_status(case_results)

    # The master never opens the scientific gate merely because infrastructure
    # passed. A scientific run is permitted only when every case says so.
    execution_open = all(
        result.get("execution_gate") == "OPEN"
        for name, result in case_results.items()
        if name != "AUTONOMOUS_KERNEL"
    ) and status == "RESULT"

    report = {
        "strategy_version": strategy["strategy_version"],
        "status": status,
        "started_at_utc": started,
        "scientific_execution": bool(scientific_runs > 0 and execution_open),
        "scientific_runs_executed": scientific_runs,
        "scientific_runs_requested": 0,
        "execution_gate": "OPEN" if execution_open else "CLOSED",
        "cases": case_results,
        "promotion_rule_enforced": True,
        "audit_invariant_enforced": True,
        "auto_repair_scope": (
            "Mechanical/infrastructure defects only. No scientific assumption, "
            "hypothesis, observable, threshold, control, exclusion rule, or "
            "stopping rule may be invented or changed after results."
        ),
        "next_action": (
            "If CLOSED, inspect the highest-priority blocking contract and "
            "repair only registered mechanical defects; then rerun the full "
            "audit chain from the beginning."
        ),
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    CHECKPOINT.write_text(json.dumps({
        "strategy_version": strategy["strategy_version"],
        "last_status": status,
        "execution_gate": report["execution_gate"],
        "scientific_runs_executed": scientific_runs,
        "last_report": str(REPORT.relative_to(ROOT)),
    }, indent=2), encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(report, sort_keys=True) + "\n")
    return report

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
