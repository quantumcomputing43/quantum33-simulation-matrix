"""Strict configuration and project-identity validation for the generic Simulation Matrix."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

REQUIRED_TOP={"matrix_version","case_id","seed","scientific_experiment","execution_policy","pipeline","validity_rules","output_contract"}
REQUIRED_STAGE={"stage","enabled","purpose","pass_condition"}
ALLOWED_STAGES={"FALSIFICATION","ADVERSARIAL_STRESS","IDENTIFIABILITY","ROBUSTNESS","SURVIVOR_CHECK"}
PROJECT_ID_RE=re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")

class ConfigError(ValueError):
    pass

def _reject_duplicates(pairs:list[tuple[str,Any]])->dict[str,Any]:
    out={}
    for key,value in pairs:
        if key in out:
            raise ConfigError(f"duplicate JSON key: {key}")
        out[key]=value
    return out

def validate_project_id(project_id:str)->None:
    if not isinstance(project_id,str) or not PROJECT_ID_RE.fullmatch(project_id):
        raise ConfigError("project_id must match ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")

def load_matrix(path:Path)->dict[str,Any]:
    with path.open("r",encoding="utf-8") as f:
        data=json.load(f,object_pairs_hook=_reject_duplicates)
    validate_matrix(data)
    return data

def load_project_manifest(path:Path)->dict[str,Any]:
    with path.open("r",encoding="utf-8") as f:
        data=json.load(f,object_pairs_hook=_reject_duplicates)
    required={"project_id","case_id","protocol_version","execution_enabled"}
    missing=required-data.keys()
    if missing: raise ConfigError(f"project manifest missing fields: {sorted(missing)}")
    validate_project_id(data["project_id"])
    if not isinstance(data["case_id"],str) or not data["case_id"]:
        raise ConfigError("project manifest case_id must be non-empty")
    if not isinstance(data["protocol_version"],str) or not data["protocol_version"]:
        raise ConfigError("project manifest protocol_version must be non-empty")
    if data["execution_enabled"] is not True:
        raise ConfigError(f"project {data['project_id']} is not enabled for execution")
    return data

def validate_matrix(data:dict[str,Any])->None:
    missing=REQUIRED_TOP-data.keys()
    if missing: raise ConfigError(f"missing fields: {sorted(missing)}")
    if data["seed"]!=42: raise ConfigError("seed must be exactly 42")
    if data["scientific_experiment"] is not False: raise ConfigError("scientific_experiment must remain false")
    if data["execution_policy"].get("case_adapter_required") is not True: raise ConfigError("case_adapter_required must be true")
    if data["validity_rules"].get("record_all_failures") is not True: raise ConfigError("record_all_failures must be true")
    if data["validity_rules"].get("project_isolation_required") is not True: raise ConfigError("project_isolation_required must be true")
    if data["validity_rules"].get("explicit_project_id_required") is not True: raise ConfigError("explicit_project_id_required must be true")
    seen=set()
    for item in data["pipeline"]:
        if not REQUIRED_STAGE.issubset(item): raise ConfigError(f"invalid stage: {item!r}")
        name=item["stage"]
        if name not in ALLOWED_STAGES: raise ConfigError(f"unknown stage: {name}")
        if name in seen: raise ConfigError(f"duplicate stage: {name}")
        seen.add(name)
    if "SURVIVOR_CHECK" not in seen: raise ConfigError("SURVIVOR_CHECK is required")
    if not {"checkpoint","latest_result","event_log"}.issubset(data["output_contract"]):
        raise ConfigError("incomplete output contract")
    for key in ("checkpoint","latest_result","event_log"):
        value=data["output_contract"][key]
        if not isinstance(value,str) or "{project_id}" not in value:
            raise ConfigError(f"output_contract.{key} must contain {{project_id}}")
