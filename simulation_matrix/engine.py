"""Generic deterministic execution engine with project-isolated state."""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from simulation_matrix.config import ConfigError,load_matrix,load_project_manifest,validate_project_id
from simulation_matrix.contracts import INFRASTRUCTURE_FAILURE,IMPLEMENTATION_FAILURE,METHOD_FAILURE,SCIENTIFIC_FAILURE,RESULT
from simulation_matrix.cases.synthetic import load_case

def _now(): return datetime.now(timezone.utc).isoformat()

def _write(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,sort_keys=True),encoding="utf-8")

def _event(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as f:
        f.write(json.dumps(data,sort_keys=True)+"\n")

def _identity(matrix,adapter,project_id):
    payload={
        "project_id":project_id,
        "matrix":matrix,
        "case_id":adapter.case_id,
        "protocol_version":adapter.protocol_version,
    }
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def _output_path(root:Path,template:str,project_id:str)->Path:
    rendered=template.replace("{project_id}",project_id)
    path=(root/rendered).resolve()
    root_resolved=root.resolve()
    if root_resolved not in path.parents:
        raise ConfigError(f"output path escapes root: {template}")
    return path

def run(root:Path,*,project_id:str,matrix_path:Path|None=None,project_manifest_path:Path|None=None)->dict:
    validate_project_id(project_id)
    matrix_path=matrix_path or (root/"simulation_matrix"/"matrix.json")
    project_manifest_path=project_manifest_path or (root/"simulation_matrix"/"projects"/f"{project_id}.json")
    matrix=load_matrix(matrix_path)
    manifest=load_project_manifest(project_manifest_path)
    if manifest["project_id"]!=project_id:
        raise RuntimeError("INFRASTRUCTURE_FAILURE: project manifest identity mismatch")
    if manifest["case_id"]!=matrix["case_id"]:
        raise RuntimeError("INFRASTRUCTURE_FAILURE: project manifest case_id mismatch")
    adapter=load_case(matrix["case_id"])
    if manifest["protocol_version"]!=adapter.protocol_version:
        raise RuntimeError("INFRASTRUCTURE_FAILURE: project manifest protocol_version mismatch")
    identity=_identity(matrix,adapter,project_id)
    out=matrix["output_contract"]
    checkpoint=_output_path(root,out["checkpoint"],project_id)
    latest=_output_path(root,out["latest_result"],project_id)
    log=_output_path(root,out["event_log"],project_id)
    state={
        "matrix_version":matrix["matrix_version"],
        "project_id":project_id,
        "case_id":adapter.case_id,
        "protocol_version":adapter.protocol_version,
        "seed":matrix["seed"],
        "scientific_experiment":False,
        "execution_identity":identity,
        "status":"RUNNING",
        "stages":[],
        "resumed":False,
        "timestamp":_now(),
    }
    if checkpoint.exists():
        saved=json.loads(checkpoint.read_text(encoding="utf-8"))
        if saved.get("project_id")!=project_id:
            raise RuntimeError("INFRASTRUCTURE_FAILURE: checkpoint belongs to another project")
        if saved.get("execution_identity")!=identity:
            raise RuntimeError("INFRASTRUCTURE_FAILURE: incompatible checkpoint preserved")
        state["stages"]=saved.get("stages",[])
        state["resumed"]=True
    completed={x["stage"] for x in state["stages"]}
    for spec in matrix["pipeline"]:
        stage=spec["stage"]
        if not spec["enabled"] or stage in completed:
            continue
        try:
            result=adapter.run_stage(
                stage,
                seed=matrix["seed"],
                context={"matrix":matrix,"execution_identity":identity,"project_id":project_id},
            )
        except Exception as exc:
            item={"stage":stage,"status":IMPLEMENTATION_FAILURE,"passed":False,"error":f"{type(exc).__name__}: {exc}"}
            state["stages"].append(item); state["status"]=IMPLEMENTATION_FAILURE
            _event(log,{**item,"project_id":project_id,"timestamp":_now()})
            _write(checkpoint,state); _write(latest,state)
            return state
        item={"stage":result.stage,"status":result.status,"passed":result.passed,"details":result.details}
        state["stages"].append(item)
        _event(log,{**item,"project_id":project_id,"timestamp":_now()})
        _write(checkpoint,state)
        if not result.passed:
            failure=result.details.get("failure_status",METHOD_FAILURE)
            state["status"]=failure if failure in {METHOD_FAILURE,SCIENTIFIC_FAILURE} else METHOD_FAILURE
            _write(latest,state); _write(checkpoint,state)
            return state
    enabled={x["stage"] for x in matrix["pipeline"] if x["enabled"]}
    done={x["stage"] for x in state["stages"]}
    survivor=next((x for x in state["stages"] if x["stage"]=="SURVIVOR_CHECK"),None)
    if enabled!=done:
        state["status"]=INFRASTRUCTURE_FAILURE
    elif survivor is None or not survivor["passed"]:
        state["status"]=METHOD_FAILURE
    else:
        state["status"]=RESULT
    state["timestamp"]=_now()
    _write(checkpoint,state); _write(latest,state)
    _event(log,{"event":"RUN_COMPLETE","project_id":project_id,"status":state["status"],"timestamp":_now()})
    return state
