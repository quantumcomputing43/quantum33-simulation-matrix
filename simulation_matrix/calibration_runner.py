"""Run the registered five-operation blind calibration case."""
from pathlib import Path
import shutil,tempfile
from simulation_matrix.engine import run
ROOT=Path(__file__).resolve().parent.parent
def main():
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)
        shutil.copy2(ROOT/"simulation_matrix"/"calibration_matrix.json",root/"matrix.json")
        state=run(root)
        print(state)
        if state["status"]!="RESULT": raise SystemExit(1)
if __name__=="__main__": main()
