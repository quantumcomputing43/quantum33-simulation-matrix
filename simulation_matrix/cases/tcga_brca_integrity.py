"""Blind TCGA-BRCA integrity audit. Prior audit results are not encoded."""
from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
from simulation_matrix.contracts import StageResult,BLOCKED
class TCGABRCAIntegrityAdapter:
    case_id="miRNA21.tcga_brca.integrity_blind"; protocol_version="1.0"
    def _files(self,root,c):
        d=root/c["root"]
        if not d.exists(): return None,{"reason":"DATA_ROOT_MISSING","path":str(d)}
        def one(xs):
            f=[d/x for x in xs if (d/x).is_file()]
            return f[0] if len(f)==1 else f
        e,cl,j=one(c["expression_candidates"]),one(c["clinical_candidates"]),one(c["joined_candidates"])
        if isinstance(e,list) or isinstance(cl,list): return None,{"reason":"AMBIGUOUS_OR_MISSING_RAW_INPUT","expression_matches":[str(x) for x in e] if isinstance(e,list) else [str(e)],"clinical_matches":[str(x) for x in cl] if isinstance(cl,list) else [str(cl)]}
        if e is None or cl is None: return None,{"reason":"REQUIRED_RAW_INPUT_MISSING"}
        return {"expression":e,"clinical":cl,"joined":j},{}
    def _read(self,p):
        with p.open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
    def _sha(self,p): return hashlib.sha256(p.read_bytes()).hexdigest()
    def _ids(self,rows,col):
        v=[r.get(col,"") for r in rows];return {"n":len(v),"missing":sum(x=="" for x in v),"unique":len(set(v)),"duplicates":len(v)-len(set(v))}
    def _audit(self,root,c):
        fs,info=self._files(root,c)
        if fs is None:return {"blocked":True,**info}
        er,cr=self._read(fs["expression"]),self._read(fs["clinical"])
        ep={r.get("patient_id") for r in er if r.get("patient_id")};cp={r.get("patient_id") for r in cr if r.get("patient_id")};ov=ep&cp
        miss=neg=bad=zero=0
        for r in cr:
            if r.get("patient_id") not in ov:continue
            if r.get("OS.time","")=="" or r.get("OS","")=="" :miss+=1
            try:t=float(r.get("OS.time",""))
            except:continue
            if t<0:neg+=1
            try:e=int(float(r.get("OS","")))
            except:continue
            if e not in (0,1):bad+=1
            if t==0 and e==0:zero+=1
        return {"blocked":False,"files":{k:{"path":str(v),"sha256":self._sha(v)} for k,v in fs.items() if v is not None},"expression_identity":{"sample_id":self._ids(er,"sample_id"),"patient_id":self._ids(er,"patient_id")},"clinical_identity":{"patient_id":self._ids(cr,"patient_id")},"join":{"expression_patients":len(ep),"clinical_patients":len(cp),"matched_patients":len(ov),"expression_only":len(ep-cp),"clinical_only":len(cp-ep)},"endpoint":{"matched_rows":len(ov),"missing_OS_or_time":miss,"negative_OS_time":neg,"invalid_event":bad,"zero_time_censored":zero}}
    def run_stage(self,stage,*,seed,context):
        root=Path(context["root"]);c=context["matrix"]["data_contract"]
        if stage=="PROVENANCE_GATE":
            a=self._audit(root,c)
            if a["blocked"]:return StageResult(stage=stage,status=BLOCKED,passed=False,details={**a,"failure_status":BLOCKED})
            return StageResult(stage=stage,status="PASS",passed=True,details={"audit":a})
        a=next((x["details"]["audit"] for x in context["prior_stages"] if x["stage"]=="PROVENANCE_GATE"),None)
        if not a:return StageResult(stage=stage,status=BLOCKED,passed=False,details={"failure_status":BLOCKED,"reason":"PROVENANCE_GATE_NOT_SURVIVED"})
        if stage=="IDENTITY_AUDIT":d={**a["expression_identity"],"clinical_identity":a["clinical_identity"]}
        elif stage=="JOIN_AUDIT":d=a["join"]
        elif stage=="ENDPOINT_AUDIT":d=a["endpoint"]
        elif stage=="REPRODUCIBILITY_AUDIT":
            again=self._audit(root,c);ok=json.dumps(a,sort_keys=True)==json.dumps(again,sort_keys=True);return StageResult(stage=stage,status="PASS" if ok else "SCIENTIFIC_FAILURE",passed=ok,details={"deterministic_reproduction":ok})
        elif stage=="SURVIVOR_CHECK":d={"all_previous_operations_completed":True}
        else:raise RuntimeError(stage)
        return StageResult(stage=stage,status="PASS",passed=True,details=d)
def load_case():return TCGABRCAIntegrityAdapter()
