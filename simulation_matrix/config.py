"""Strict configuration loading for the Simulation Matrix."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

REQUIRED_TOP={"matrix_version","case_id","seed","scientific_experiment","execution_policy","pipeline","validity_rules","output_contract"}
REQUIRED_STAGE={"stage","enabled","purpose","pass_condition"}
ALLOWED_STAGES={"FALSIFICATION","ADVERSARIAL_STRESS","IDENTIFIABILITY","ROBUSTNESS","SURVIVOR_CHECK"}

class ConfigError(ValueError): pass

def _reject_duplicates(pairs:list[tuple[str,Any]])->dict[str,Any]:
    out={}
    for key,value in pairs:
        if key in out: raise ConfigError(f"duplicate JSON key: {key}")
        out[key]=value
    return out

def load_matrix(path:Path)->dict[str,Any]:
    with path.open("r",encoding="utf-8") as f:
        data=json.load(f,object_pairs_hook=_reject_duplicates)
    validate_matrix(data)
    return data

def validate_matrix(data:dict[str,Any])->None:
    missing=REQUIRED_TOP-data.keys()
    if missing: raise ConfigError(f"missing fields: {sorted(missing)}")
    if not isinstance(data["seed"],int): raise ConfigError("seed must be an integer")
    if data["execution_policy"].get("case_adapter_required") is not True: raise ConfigError("case_adapter_required must be true")
    if data["validity_rules"].get("record_all_failures") is not True: raise ConfigError("record_all_failures must be true")
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
