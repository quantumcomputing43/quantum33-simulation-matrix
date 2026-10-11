"""Generic deterministic execution engine."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from simulation_matrix.config import load_matrix
from simulation_matrix.contracts import (
    IMPLEMENTATION_FAILURE,
    INFRASTRUCTURE_FAILURE,
    METHOD_FAILURE,
    RESULT,
    SCIENTIFIC_FAILURE,
)
from simulation_matrix.cases.synthetic import load_case


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _event(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(data, sort_keys=True) + "\n")


def _identity(matrix: dict, adapter) -> str:
    payload = {
        "matrix": matrix,
        "case_id": adapter.case_id,
        "protocol_version": adapter.protocol_version,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _validate_adapter_identity(matrix: dict, adapter) -> None:
    if not isinstance(getattr(adapter, "case_id", None), str) or not adapter.case_id:
        raise RuntimeError("adapter must declare a non-empty case_id")
    if matrix.get("case_id") != adapter.case_id:
        raise RuntimeError(
            f"case_id mismatch: matrix={matrix.get('case_id')!r}, "
            f"adapter={adapter.case_id!r}"
        )
    if not isinstance(getattr(adapter, "protocol_version", None), str) or not adapter.protocol_version:
        raise RuntimeError("adapter must declare a non-empty protocol_version")
    if not callable(getattr(adapter, "run_stage", None)):
        raise RuntimeError("adapter must implement callable run_stage")


def _validate_stage_result(expected_stage: str, result) -> None:
    if getattr(result, "stage", None) != expected_stage:
        raise TypeError(
            f"adapter returned stage {getattr(result, 'stage', None)!r}; "
            f"expected {expected_stage!r}"
        )
    if not isinstance(getattr(result, "passed", None), bool):
        raise TypeError("stage result passed must be a bool")
    if not isinstance(getattr(result, "status", None), str) or not result.status:
        raise TypeError("stage result status must be a non-empty string")
    if not isinstance(getattr(result, "details", None), dict):
        raise TypeError("stage result details must be a dict")


def run(root: Path) -> dict:
    matrix = load_matrix(root / "matrix.json")
    adapter = load_case()
    _validate_adapter_identity(matrix, adapter)
    identity = _identity(matrix, adapter)

    output = matrix["output_contract"]
    checkpoint = root / output["checkpoint"]
    latest = root / output["latest_result"]
    log = root / output["event_log"]
    state = {
        "matrix_version": matrix["matrix_version"],
        "case_id": adapter.case_id,
        "protocol_version": adapter.protocol_version,
        "seed": matrix["seed"],
        "scientific_experiment": False,
        "execution_identity": identity,
        "status": "RUNNING",
        "stages": [],
        "resumed": False,
        "timestamp": _now(),
    }

    if checkpoint.exists():
        saved = json.loads(checkpoint.read_text(encoding="utf-8"))
        if saved.get("execution_identity") != identity:
            raise RuntimeError("INFRASTRUCTURE_FAILURE: incompatible checkpoint preserved")
        state["stages"] = saved.get("stages", [])
        state["resumed"] = True

    completed = {item["stage"] for item in state["stages"]}
    for spec in matrix["pipeline"]:
        stage = spec["stage"]
        if not spec["enabled"] or stage in completed:
            continue
        try:
            result = adapter.run_stage(
                stage, seed=matrix["seed"],
                context={"matrix": matrix, "execution_identity": identity},
            )
            _validate_stage_result(stage, result)
        except Exception as exc:
            item = {
                "stage": stage,
                "status": IMPLEMENTATION_FAILURE,
                "passed": False,
                "error": f"{type(exc).__name__}: {exc}",
            }
            state["stages"].append(item)
            state["status"] = IMPLEMENTATION_FAILURE
            _event(log, {**item, "timestamp": _now()})
            _write(checkpoint, state)
            _write(latest, state)
            return state

        item = {
            "stage": result.stage,
            "status": result.status,
            "passed": result.passed,
            "details": result.details,
        }
        state["stages"].append(item)
        _event(log, {**item, "timestamp": _now()})
        _write(checkpoint, state)
        if not result.passed:
            failure = result.details.get("failure_status", METHOD_FAILURE)
            state["status"] = (
                failure if failure in {METHOD_FAILURE, SCIENTIFIC_FAILURE}
                else METHOD_FAILURE
            )
            _write(latest, state)
            _write(checkpoint, state)
            return state

    enabled = {item["stage"] for item in matrix["pipeline"] if item["enabled"]}
    done = {item["stage"] for item in state["stages"]}
    survivor = next(
        (item for item in state["stages"] if item["stage"] == "SURVIVOR_CHECK"),
        None,
    )
    if enabled != done:
        state["status"] = INFRASTRUCTURE_FAILURE
    elif survivor is None or not survivor["passed"]:
        state["status"] = METHOD_FAILURE
    else:
        state["status"] = RESULT

    state["timestamp"] = _now()
    _write(checkpoint, state)
    _write(latest, state)
    _event(log, {"event": "RUN_COMPLETE", "status": state["status"], "timestamp": _now()})
    return state
