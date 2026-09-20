"""BHD pre-experiment model-validation matrix.

This is a deterministic mathematical validation run, not a scientific execution.
It checks the previously used N=4 transverse-field Ising information metric
near (lambda,h)=(1,0) and records whether the implementation reproduces the
declared benchmark values within a fixed numerical tolerance.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

SEED=42
N=4
LAMBDA=1.0
BENCHMARKS={
    0.1: np.array([[3.4028,-7.3136],[-7.3136,20.5808]]),
    0.01: np.array([[1.8032,-9.4046],[-9.4046,275.6538]]),
}

def pauli():
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],complex)
    Z=np.array([[1,0],[0,-1]],complex)
    return I,X,Z

def kron_all(xs):
    out=xs[0]
    for x in xs[1:]: out=np.kron(out,x)
    return out

def H(lam,h):
    I,X,Z=pauli(); dim=2**N
    out=np.zeros((dim,dim),complex)
    for i in range(N-1):
        xs=[I]*N; xs[i]=Z; xs[i+1]=Z
        out += -lam*kron_all(xs)
    for i in range(N):
        xs=[I]*N; xs[i]=X
        out += -h*kron_all(xs)
    return out

def ground(lam,h):
    vals,vecs=np.linalg.eigh(H(lam,h))
    return vecs[:,0]

def qfi_metric(lam,h,eps=1e-5):
    # Pure-state QFI metric: 4 Re(<d_i psi|d_j psi>-<d_i psi|psi><psi|d_j psi>)
    p=ground(lam,h)
    dl=(ground(lam+eps,h)-ground(lam-eps,h))/(2*eps)
    dh=(ground(lam,h+eps)-ground(lam,h-eps))/(2*eps)
    ds=[dl,dh]
    g=np.zeros((2,2))
    for i in range(2):
        for j in range(2):
            g[i,j]=4*np.real(np.vdot(ds[i],ds[j])-np.vdot(ds[i],p)*np.vdot(p,ds[j]))
    return g

def run(tol=0.08):
    rows=[]
    for h,ref in BENCHMARKS.items():
        got=qfi_metric(LAMBDA,h)
        err=float(np.max(np.abs(got-ref)))
        rows.append({"h":h,"metric":got.tolist(),"max_abs_error":err,"pass":err<=tol})
    return {"case_id":"bhd.preexperiment.tfim_qfi","seed":SEED,
            "scientific_execution":False,"status":"PASS" if all(r["pass"] for r in rows) else "IMPLEMENTATION_FAILURE",
            "tolerance":tol,"benchmarks":rows}

if __name__=="__main__":
    root=Path(__file__).parents[2]
    out=root/"results"/"bhd_preexperiment_validation.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(run(),indent=2),encoding="utf-8")
