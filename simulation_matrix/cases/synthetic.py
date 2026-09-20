"""Deterministic infrastructure fixture; not a scientific experiment."""
from __future__ import annotations
import hashlib,json
from simulation_matrix.contracts import StageResult

class SyntheticAdapter:
    case_id="synthetic.contract"
    protocol_version="1.0"

    def run_stage(self,stage:str,*,seed:int,context:dict)->StageResult:
        payload=json.dumps({"case":self.case_id,"stage":stage,"seed":seed},sort_keys=True).encode()
        digest=hashlib.sha256(payload).hexdigest()
        return StageResult(stage=stage,status="PASS",passed=True,details={
            "fixture":True,"deterministic_digest":digest,"scientific_experiment":False
        })

def load_case()->SyntheticAdapter:
    return SyntheticAdapter()
