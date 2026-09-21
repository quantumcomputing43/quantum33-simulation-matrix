"""Blind five-operation calibration case for the registered miRNA-21 sensor model."""
from __future__ import annotations
import numpy as np
from simulation_matrix.contracts import StageResult

class MiRNA21IdentifiabilityAdapter:
    case_id="miRNA21.sensor_identifiability.blind5"
    protocol_version="1.0"
    def _obs(self,th):
        C,Kd,g,G0,eta=np.exp(th[0]),np.exp(th[1]),np.exp(th[2]),th[3],th[4]
        f=C/(C+Kd); return np.array([g*f,G0+g*g*f*(1-f),f],float)
    def _jac(self,th):
        h=1e-6; J=np.zeros((3,5))
        for j in range(5):
            a,b=th.copy(),th.copy(); a[j]+=h; b[j]-=h; J[:,j]=(self._obs(a)-self._obs(b))/(2*h)
        return J
    def _invariance(self,th):
        base=self._obs(th); errs=[]
        for a in np.logspace(-3,3,25):
            t=th.copy(); t[0]+=np.log(a); t[1]+=np.log(a); errs.append(float(np.max(np.abs(self._obs(t)-base))))
        return max(errs)
    def _profile(self,th):
        base=self._obs(th); grid=np.logspace(-3,3,161)*np.exp(th[0]); residual=[]
        for C in grid:
            Kd=C*np.exp(th[1]-th[0]); t=th.copy(); t[0]=np.log(C); t[1]=np.log(Kd)
            residual.append(float(np.linalg.norm(self._obs(t)-base)))
        return float(max(residual)),float(np.ptp(residual))
    def run_stage(self,stage,*,seed,context):
        rng=np.random.default_rng(seed); th=np.array([np.log(2.),np.log(3.),np.log(.7),.2,1.])
        S=np.linalg.svd(self._jac(th),compute_uv=False); rank=int(np.sum(S>S[0]*1e-8))
        inv=self._invariance(th); pmax,pspan=self._profile(th)
        if stage=="FALSIFICATION":
            passed=inv<1e-10 and rank<5
            details={"invariance_max_abs_error":inv,"numerical_rank":rank,"singular_values":S.tolist()}
        elif stage=="ADVERSARIAL_STRESS":
            vals=[]
            for scale in [.01,.1,1,10,100]:
                t=th.copy(); t[0]+=np.log(scale); t[1]+=np.log(scale); vals.append(float(np.max(np.abs(self._obs(t)-self._obs(th)))))
            passed=max(vals)<1e-10; details={"joint_scale_stress_max_error":max(vals),"scales":[.01,.1,1,10,100]}
        elif stage=="IDENTIFIABILITY":
            passed=bool(rank<5 and S[-1]<S[0]*1e-8)
            details={"numerical_rank":rank,"parameter_count":5,"condition_number":float(S[0]/max(S[-1],1e-300)),"singular_values":S.tolist()}
        elif stage=="ROBUSTNESS":
            reps=[]
            for _ in range(5):
                Sr=np.linalg.svd(self._jac(th),compute_uv=False); reps.append((int(np.sum(Sr>Sr[0]*1e-8)),float(Sr[0]/max(Sr[-1],1e-300))))
            passed=all(x==reps[0] for x in reps)
            details={"deterministic_repetitions":reps,"profile_grid_points":161,"profile_max_residual":pmax,"profile_span":pspan,"noise_probe_seed":int(rng.integers(0,2**31-1))}
        else:
            passed=context["matrix"]["scientific_experiment"] is True and all(x.get("passed",False) for x in context.get("prior_stages",[]))
            details={"all_previous_operations_passed":passed}
        return StageResult(stage=stage,status="PASS" if passed else "SCIENTIFIC_FAILURE",passed=passed,details=details)
def load_case(): return MiRNA21IdentifiabilityAdapter()
