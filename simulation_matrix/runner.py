from pathlib import Path
from datetime import datetime, timezone
import json
import time


ROOT = Path(__file__).resolve().parent

MATRIX_FILE = ROOT / "matrix.json"

STATE = ROOT / "state"
RESULTS = ROOT / "results"
LOGS = ROOT / "logs"

for directory in (STATE, RESULTS, LOGS):
    directory.mkdir(parents=True, exist_ok=True)

CHECKPOINT = STATE / "checkpoint.json"
LATEST = RESULTS / "latest.json"
LOGFILE = LOGS / "matrix.jsonl"


def now():
    return datetime.now(timezone.utc).isoformat()


def load_matrix():
    with MATRIX_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save(state):
    CHECKPOINT.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8"
    )

    LATEST.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8"
    )

    with LOGFILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(state) + "\n")


def validate_matrix(matrix):
    required_top = {
        "matrix_version",
        "seed",
        "scientific_experiment",
        "execution_policy",
        "pipeline",
        "validity_rules",
        "output_contract"
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

    for stage in matrix["pipeline"]:
        required_stage = {
            "stage",
            "enabled",
            "purpose",
            "pass_condition"
        }

        if not required_stage.issubset(stage.keys()):
            return False, f"Invalid stage definition: {stage}"

    return True, None


def initialize_state(matrix):
    return {
        "run_id": f"matrix-{int(time.time())}",
        "matrix_version": matrix["matrix_version"],
        "seed": matrix["seed"],
        "stage": "INIT",
        "status": "RUNNING",
        "checkpoint": 0,
        "scientific_experiment": False,
        "timestamp": now()
    }


matrix = load_matrix()

matrix_valid, matrix_error = validate_matrix(matrix)

if CHECKPOINT.exists():
    state = json.loads(
        CHECKPOINT.read_text(encoding="utf-8")
    )
    resumed = True
else:
    state = initialize_state(matrix)
    resumed = False


checks = {
    "matrix_file": MATRIX_FILE.exists(),
    "matrix_schema": matrix_valid,
    "state_directory": STATE.exists(),
    "results_directory": RESULTS.exists(),
    "logs_directory": LOGS.exists(),
    "checkpoint_write": False,
    "checkpoint_reload": False,
    "deterministic_seed": state["seed"] == 42,
    "scientific_experiment_disabled": (
        state["scientific_experiment"] is False
    ),
    "pipeline_defined": (
        isinstance(matrix.get("pipeline"), list)
        and len(matrix["pipeline"]) > 0
    )
}


if matrix_error:
    state["matrix_error"] = matrix_error


save(state)

checks["checkpoint_write"] = CHECKPOINT.exists()


if CHECKPOINT.exists():
    reloaded = json.loads(
        CHECKPOINT.read_text(encoding="utf-8")
    )

    checks["checkpoint_reload"] = (
        reloaded["run_id"] == state["run_id"]
        and reloaded["seed"] == state["seed"]
    )


passed = all(checks.values())


stage_results = []

if passed:
    for index, stage in enumerate(matrix["pipeline"], start=1):

        if stage["enabled"]:
            stage_status = "READY"
        else:
            stage_status = "DISABLED"

        stage_results.append({
            "checkpoint": index,
            "stage": stage["stage"],
            "status": stage_status,
            "purpose": stage["purpose"],
            "pass_condition": stage["pass_condition"]
        })

    state["stage"] = "MATRIX_SPEC_VALIDATED"
    state["status"] = "PASS"

else:
    state["stage"] = "INFRASTRUCTURE_FAILURE"
    state["status"] = "FAIL"


state["checks"] = checks
state["pipeline"] = stage_results
state["resumed"] = resumed
state["timestamp"] = now()

save(state)

print(json.dumps(state, indent=2))


if not passed:
    raise SystemExit(1)
