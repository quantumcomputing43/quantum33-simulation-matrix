"""Validate and record the generic simulation-matrix specification."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import time
from typing import Any


ROOT = Path(__file__).resolve().parent


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_matrix(matrix: dict[str, Any]) -> tuple[bool, str | None]:
    required_top = {
        "matrix_version", "seed", "scientific_experiment", "execution_policy",
        "pipeline", "validity_rules", "output_contract",
    }
    missing = required_top - matrix.keys()
    if missing:
        return False, f"Missing matrix fields: {sorted(missing)}"
    if matrix["scientific_experiment"] is not False:
        return False, "Scientific experiment must remain disabled."
    if matrix["seed"] != 42:
        return False, "Seed must remain 42."
    if not isinstance(matrix["pipeline"], list):
        return False, "Pipeline must be a list."

    required_stage = {"stage", "enabled", "purpose", "pass_condition"}
    for stage in matrix["pipeline"]:
        if not isinstance(stage, dict) or not required_stage.issubset(stage):
            return False, f"Invalid stage definition: {stage}"
    return True, None


def _paths(root: Path, matrix_version: str) -> tuple[Path, Path, Path]:
    safe_version = matrix_version.replace("/", "_")
    return (
        root / "state" / f"checkpoint_{safe_version}.json",
        root / "results" / f"latest_{safe_version}.json",
        root / "logs" / f"matrix_{safe_version}.jsonl",
    )


def _save(state: dict[str, Any], paths: tuple[Path, Path, Path]) -> None:
    checkpoint, latest, logfile = paths
    serialized = json.dumps(state, indent=2)
    checkpoint.write_text(serialized, encoding="utf-8")
    latest.write_text(serialized, encoding="utf-8")
    with logfile.open("a", encoding="utf-8") as file:
        file.write(json.dumps(state) + "\n")


def _initialize_state(matrix: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": f"matrix-{int(time.time())}",
        "matrix_version": matrix["matrix_version"],
        "seed": matrix["seed"],
        "stage": "INIT",
        "status": "RUNNING",
        "checkpoint": 0,
        "scientific_experiment": False,
        "timestamp": now(),
    }


def run_matrix(root: Path = ROOT) -> dict[str, Any]:
    """Run infrastructure validation and return its persisted state."""
    matrix_file = root / "matrix.json"
    matrix = json.loads(matrix_file.read_text(encoding="utf-8"))
    matrix_valid, matrix_error = validate_matrix(matrix)

    for directory in (root / "state", root / "results", root / "logs"):
        directory.mkdir(parents=True, exist_ok=True)

    paths = _paths(root, matrix["matrix_version"])
    checkpoint, _, _ = paths
    if checkpoint.exists():
        state = json.loads(checkpoint.read_text(encoding="utf-8"))
        compatible = (
            state.get("matrix_version") == matrix["matrix_version"]
            and state.get("seed") == matrix["seed"]
            and state.get("scientific_experiment") is False
        )
    else:
        compatible = False

    resumed = compatible
    if not compatible:
        state = _initialize_state(matrix)

    checks = {
        "matrix_file": matrix_file.exists(),
        "matrix_schema": matrix_valid,
        "state_directory": (root / "state").exists(),
        "results_directory": (root / "results").exists(),
        "logs_directory": (root / "logs").exists(),
        "checkpoint_write": False,
        "checkpoint_reload": False,
        "checkpoint_isolated": state.get("matrix_version") == matrix["matrix_version"],
        "deterministic_seed": state["seed"] == 42,
        "scientific_experiment_disabled": state["scientific_experiment"] is False,
        "pipeline_defined": bool(matrix.get("pipeline")),
    }
    if matrix_error:
        state["matrix_error"] = matrix_error

    _save(state, paths)
    checks["checkpoint_write"] = checkpoint.exists()
    reloaded = json.loads(checkpoint.read_text(encoding="utf-8"))
    checks["checkpoint_reload"] = (
        reloaded["run_id"] == state["run_id"]
        and reloaded["matrix_version"] == matrix["matrix_version"]
        and reloaded["seed"] == state["seed"]
    )

    passed = all(checks.values())
    state.update({
        "stage": "MATRIX_SPEC_VALIDATED" if passed else "INFRASTRUCTURE_FAILURE",
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
        "pipeline": [
            {
                "checkpoint": index,
                "stage": stage["stage"],
                "status": "READY" if stage["enabled"] else "DISABLED",
                "purpose": stage["purpose"],
                "pass_condition": stage["pass_condition"],
            }
            for index, stage in enumerate(matrix["pipeline"], start=1)
        ] if passed else [],
        "resumed": resumed,
        "timestamp": now(),
    })
    _save(state, paths)
    return state


def main() -> None:
    state = run_matrix()
    print(json.dumps(state, indent=2))
    if state["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
