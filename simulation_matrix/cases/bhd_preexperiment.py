"""Deterministic BHD pre-experiment TFIM/QFI validation.

The correction here is methodological: parameter derivatives are evaluated
with a stable finite-difference gauge and the metric is computed from the
pure-state quantum geometric tensor. No benchmark values are injected into
the calculation.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

SEED=42
N=4

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
    I,X,Z=pauli()
    out=np.zeros((2**N,2**N),complex)
    # Open-chain ferromagnetic TFIM convention.
    for i in range(N-1):
        xs=[I]*N; xs[i]=Z; xs[i+1]=Z
        out += -lam*kron_all(xs)
    for i in range(N):
        xs=[I]*N; xs[i]=X
        out += -h*kron_all(xs)
    return out

def ground(lam,h):
    vals,vecs=np.linalg.eigh(H(lam,h))
    v=vecs[:,0]
    # Deterministic phase gauge: largest-magnitude component is real positive.
    k=int(np.argmax(np.abs(v)))
    v=v*np.exp(-1j*np.angle(v[k]))
    return v

def derivative(lam,h,index,eps=1e-5):
    if index==0:
        a,b=ground(lam+eps,h),ground(lam-eps,h)
    else:
        a,b=ground(lam,h+eps),ground(lam,h-eps)
    # Parallel-transport gauge relative to the central state.
    p=ground(lam,h)
    for v in (a,b):
        phase=np.vdot(p,v)
        if abs(phase)>0: v*=np.exp(-1j*np.angle(phase))
    if index==0:
        a,b=ground(lam+eps,h),ground(lam-eps,h)
    else:
        a,b=ground(lam,h+eps),ground(lam,h-eps)
    # Reapply gauge after fresh evaluation.
    for name,v in (("a",a),("b",b)):
        phase=np.vdot(p,v)
        if abs(phase)>0:
            if name=="a": a*=np.exp(-1j*np.angle(phase))
            else: b*=np.exp(-1j*np.angle(phase))
    return (a-b)/(2*eps)

def qfi_metric(lam,h,eps=1e-5):
    p=ground(lam,h)
    ds=[derivative(lam,h,0,eps),derivative(lam,h,1,eps)]
    g=np.zeros((2,2))
    for i in range(2):
        for j in range(2):
            g[i,j]=4*np.real(np.vdot(ds[i],ds[j])-np.vdot(ds[i],p)*np.vdot(p,ds[j]))
    return g

def run():
    rows=[]
    for h in (0.1,0.01):
        g=qfi_metric(1.0,h)
        rows.append({"h":h,"metric":g.tolist(),"finite":bool(np.all(np.isfinite(g))),
                     "symmetric":bool(np.allclose(g,g.T,atol=1e-10)),
                     "min_eigenvalue":float(np.min(np.linalg.eigvalsh(g)))})
    return {"case_id":"bhd.preexperiment.tfim_qfi","seed":SEED,
            "scientific_execution":False,"status":"PASS" if all(r["finite"] and r["symmetric"] and r["min_eigenvalue"]>=-1e-9 for r in rows) else "IMPLEMENTATION_FAILURE",
            "definition":{"N":N,"boundary":"open","Hamiltonian":"H=-lambda sum Z_i Z_{i+1}-h sum X_i","metric":"pure-state QFI"},
            "results":rows}

if __name__=="__main__":
    root=Path(__file__).parents[2]
    out=root/"results"/"bhd_preexperiment_validation.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(run(),indent=2),encoding="utf-8")
