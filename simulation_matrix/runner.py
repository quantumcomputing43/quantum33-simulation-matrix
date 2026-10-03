"""CLI entry point for the generic Simulation Matrix."""
from __future__ import annotations

import json
from pathlib import Path

from simulation_matrix.engine import run


# runner.py lives inside simulation_matrix/, while matrix.json and the
# output directories live at repository root.
ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    try:
        state = run(ROOT)
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "INFRASTRUCTURE_FAILURE",
                    "error": f"{type(exc).__name__}: {exc}",
                },
                indent=2,
            )
        )
        raise SystemExit(2) from exc

    print(json.dumps(state, indent=2))
    if state["status"] != "RESULT":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
