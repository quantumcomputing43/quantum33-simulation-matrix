"""Generic deterministic execution engine with registered case adapters."""
from __future__ import annotations
import hashlib,json,importlib
from datetime import datetime,timezone
from pathlib import Path
from simulation_matrix.config import load_matrix
from simulation_matrix.contracts import INFRASTRUCTURE_FAILURE,IMPLEMENTATION_FAILURE,METHOD_FAILURE,SCIENTIFIC_FAILURE,RESULT

def _now(): return datetime.now(timezone.utc).isoformat()
def _write(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,indent=2,sort_keys=True),encoding="utf-8")
def _event(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as f: f.write(json.dumps(data,sort_keys=True)+"\n")
def _load_case(case_id:str):
    if case_id=="synthetic.contract":
        module="simulation_matrix.cases.synthetic"
    elif case_id=="miRNA21.sensor_identifiability.blind5":
        module="simulation_matrix.cases.mirna21_identifiability"
    else:
        raise RuntimeError(f"INFRASTRUCTURE_FAILURE: unregistered case_id {case_id}")
    return importlib.import_module(module).load_case()
def _identity(matrix,adapter):
    payload={"matrix":matrix,"case_id":adapter.case_id,"protocol_version":adapter.protocol_version}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def run(root:Path)->dict:
    matrix=load_matrix(root/"matrix.json")
    adapter=_load_case(matrix["case_id"])
    identity=_identity(matrix,adapter)
    out=matrix["output_contract"]
    checkpoint=root/out["checkpoint"]; latest=root/out["latest_result"]; log=root/out["event_log"]
    state={"matrix_version":matrix["matrix_version"],"case_id":adapter.case_id,"protocol_version":adapter.protocol_version,
           "seed":matrix["seed"],"scientific_experiment":matrix["scientific_experiment"],
           "execution_identity":identity,"status":"RUNNING","stages":[],"resumed":False,"timestamp":_now()}
    if checkpoint.exists():
        saved=json.loads(checkpoint.read_text(encoding="utf-8"))
        if saved.get("execution_identity")!=identity: raise RuntimeError("INFRASTRUCTURE_FAILURE: incompatible checkpoint preserved")
        state["stages"]=saved.get("stages",[]); state["resumed"]=True
    completed={x["stage"] for x in state["stages"]}
    for spec in matrix["pipeline"]:
        stage=spec["stage"]
        if not spec["enabled"] or stage in completed: continue
        try:
            result=adapter.run_stage(stage,seed=matrix["seed"],context={"matrix":matrix,"execution_identity":identity,"prior_stages":state["stages"]})
        except Exception as exc:
            item={"stage":stage,"status":IMPLEMENTATION_FAILURE,"passed":False,"error":f"{type(exc).__name__}: {exc}"}
            state["stages"].append(item); state["status"]=IMPLEMENTATION_FAILURE; _event(log,{**item,"timestamp":_now()}); _write(checkpoint,state); _write(latest,state); return state
        item={"stage":result.stage,"status":result.status,"passed":result.passed,"details":result.details}
        state["stages"].append(item); _event(log,{**item,"timestamp":_now()}); _write(checkpoint,state)
        if not result.passed:
            failure=result.details.get("failure_status",SCIENTIFIC_FAILURE if matrix["scientific_experiment"] else METHOD_FAILURE)
            state["status"]=failure if failure in {METHOD_FAILURE,SCIENTIFIC_FAILURE} else METHOD_FAILURE
            _write(latest,state); return state
    enabled={x["stage"] for x in matrix["pipeline"] if x["enabled"]}; done={x["stage"] for x in state["stages"]}
    survivor=next((x for x in state["stages"] if x["stage"]=="SURVIVOR_CHECK"),None)
    state["status"]=INFRASTRUCTURE_FAILURE if enabled!=done else (RESULT if survivor and survivor["passed"] else METHOD_FAILURE)
    state["timestamp"]=_now(); _write(checkpoint,state); _write(latest,state); _event(log,{"event":"RUN_COMPLETE","status":state["status"],"timestamp":_now()})
    return state
