"""Deterministic infrastructure fixture; not a scientific experiment."""
from __future__ import annotations
import hashlib,json
from simulation_matrix.contracts import StageResult

class SyntheticAdapter:
    case_id="synthetic.contract"
    protocol_version="1.0"

    def run_stage(self,stage:str,*,seed:int,context:dict)->StageResult:
        payload=json.dumps({
            "project_id":context["project_id"],
            "case":self.case_id,
            "stage":stage,
            "seed":seed,
        },sort_keys=True).encode()
        digest=hashlib.sha256(payload).hexdigest()
        return StageResult(stage=stage,status="PASS",passed=True,details={
            "fixture":True,
            "deterministic_digest":digest,
            "scientific_experiment":False,
            "project_id":context["project_id"],
        })

def load_case(case_id:str)->SyntheticAdapter:
    if case_id != SyntheticAdapter.case_id:
        raise ValueError(f"no adapter registered for case_id={case_id}")
    return SyntheticAdapter()
