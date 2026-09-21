"""Generic contracts and status taxonomy."""
from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any,Protocol

INFRASTRUCTURE_FAILURE="INFRASTRUCTURE_FAILURE"
IMPLEMENTATION_FAILURE="IMPLEMENTATION_FAILURE"
METHOD_FAILURE="METHOD_FAILURE"
SCIENTIFIC_FAILURE="SCIENTIFIC_FAILURE"
RESULT="RESULT"
BLOCKED="BLOCKED"

@dataclass
class StageResult:
    stage:str
    status:str
    passed:bool
    details:dict[str,Any]=field(default_factory=dict)

class CaseAdapter(Protocol):
    case_id:str
    protocol_version:str
    def run_stage(self,stage:str,*,seed:int,context:dict[str,Any])->StageResult: ...
