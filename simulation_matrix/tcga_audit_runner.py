"""Run the registered blind TCGA-BRCA integrity audit."""
from pathlib import Path
import json,shutil,tempfile
from simulation_matrix.engine import run
ROOT=Path(__file__).resolve().parent.parent
def main():
    with tempfile.TemporaryDirectory() as d:
        root=Path(d);shutil.copy2(ROOT/"simulation_matrix"/"tcga_audit_matrix.json",root/"matrix.json")
        if (ROOT/"data").exists():shutil.copytree(ROOT/"data",root/"data")
        state=run(root);print(json.dumps(state,indent=2,sort_keys=True))
        if state["status"] not in ("RESULT","BLOCKED"):raise SystemExit(1)
if __name__=="__main__":main()
