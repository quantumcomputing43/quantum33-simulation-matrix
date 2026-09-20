"""CLI entry point for the generic Simulation Matrix."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from simulation_matrix.engine import run

ROOT=Path(__file__).resolve().parent.parent

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--project-id",required=True,help="Explicit project namespace; never inferred from prior state.")
    args=parser.parse_args()
    try:
        state=run(ROOT,project_id=args.project_id)
    except Exception as exc:
        print(json.dumps({"status":"INFRASTRUCTURE_FAILURE","error":f"{type(exc).__name__}: {exc}","project_id":args.project_id},indent=2))
        raise SystemExit(2) from exc
    print(json.dumps(state,indent=2))
    if state["status"]!="RESULT":
        raise SystemExit(1)

if __name__=="__main__":
    main()
