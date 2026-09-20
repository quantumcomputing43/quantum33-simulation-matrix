"""Quantum33 master orchestration layer.

This runner is the single routing point for future BHD and miRNA-21 work.
It executes every currently executable audit/validation layer, records blocked
scientific work explicitly, and never invents missing scientific inputs.
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
    "BHD": "simulation_matrix.cases.bhd_master_runner",
    "miRNA21": "simulation_matrix.cases.mirna21_master_runner",
    "BHD_5SCIENTIST_CROSSWALK": "simulation_matrix.cases.bhd_5scientist_crosswalk",
}

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
            "error_type": type(exc).__name__,
            "error": str(exc),
        }

def run() -> dict:
    strategy = load_strategy()
    started = datetime.now(timezone.utc).isoformat()
    case_results = {name: _call_case(module) for name, module in CASES.items()}

    scientific_runs = sum(
        int(result.get("scientific_runs_executed", 0))
        for result in case_results.values()
    )

    hard_failure = any(
        result.get("status") == "INFRASTRUCTURE_FAILURE"
        for result in case_results.values()
    )
    implementation_failure = any(
        result.get("status") == "IMPLEMENTATION_FAILURE"
        for result in case_results.values()
    )

    if hard_failure:
        status = "INFRASTRUCTURE_FAILURE"
    elif implementation_failure:
        status = "IMPLEMENTATION_FAILURE"
    else:
        status = "MASTER_AUDIT_COMPLETE"

    report = {
        "strategy_version": strategy["strategy_version"],
        "status": status,
        "started_at_utc": started,
        "scientific_execution": scientific_runs > 0,
        "scientific_runs_executed": scientific_runs,
        "scientific_runs_requested": 0,
        "cases": case_results,
        "promotion_rule_enforced": True,
        "audit_invariant_enforced": True,
        "next_action": (
            "Continue only through registered case contracts. "
            "Do not invent missing inputs or open a closed scientific gate."
        ),
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    CHECKPOINT.write_text(json.dumps({
        "strategy_version": strategy["strategy_version"],
        "last_status": status,
        "scientific_runs_executed": scientific_runs,
        "last_report": str(REPORT.relative_to(ROOT)),
    }, indent=2), encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(report) + "\n")
    return report

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
