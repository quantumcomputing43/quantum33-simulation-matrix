from pathlib import Path
from datetime import datetime, timezone
import json
import time

ROOT = Path(__file__).resolve().parent

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


if CHECKPOINT.exists():
    state = json.loads(
        CHECKPOINT.read_text(encoding="utf-8")
    )
    resumed = True
else:
    state = {
        "run_id": f"matrix-{int(time.time())}",
        "seed": 42,
        "stage": "INIT",
        "status": "RUNNING",
        "checkpoint": 0,
        "timestamp": now()
    }
    resumed = False


checks = {
    "state_directory": STATE.exists(),
    "results_directory": RESULTS.exists(),
    "logs_directory": LOGS.exists(),
    "checkpoint_write": False,
    "checkpoint_reload": False,
    "deterministic_seed": state["seed"] == 42
}


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


state["stage"] = (
    "MATRIX_READY"
    if passed
    else "INFRASTRUCTURE_FAILURE"
)

state["status"] = "PASS" if passed else "FAIL"
state["checks"] = checks
state["resumed"] = resumed
state["timestamp"] = now()


save(state)


print(json.dumps(state, indent=2))


if not passed:
    raise SystemExit(1)
