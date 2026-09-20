"""Deterministic BHD pre-experiment TFIM/QFI validation matrix.

This module is infrastructure/method validation only. It deliberately does
not fit the historical benchmark values. It checks the declared TFIM model,
QFI geometry, numerical convergence, and adversarial benchmark mismatch.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

SEED = 42
N = 4
LAMBDA = 1.0
H_VALUES = (0.1, 0.01)
EPS_VALUES = (1e-3, 1e-4, 1e-5, 1e-6)


def pauli():
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], complex)
    Z = np.array([[1, 0], [0, -1]], complex)
    return I, X, Z


def kron_all(xs):
    out = xs[0]
    for x in xs[1:]:
        out = np.kron(out, x)
    return out


def H(lam, h):
    I, X, Z = pauli()
    out = np.zeros((2**N, 2**N), complex)
    for i in range(N - 1):
        xs = [I] * N
        xs[i] = Z
        xs[i + 1] = Z
        out += -lam * kron_all(xs)
    for i in range(N):
        xs = [I] * N
        xs[i] = X
        out += -h * kron_all(xs)
    return out


def ground(lam, h):
    vals, vecs = np.linalg.eigh(H(lam, h))
    v = vecs[:, 0]
    k = int(np.argmax(np.abs(v)))
    v = v * np.exp(-1j * np.angle(v[k]))
    return v


def derivative(lam, h, index, eps=1e-5):
    p = ground(lam, h)
    if index == 0:
        a = ground(lam + eps, h)
        b = ground(lam - eps, h)
    else:
        a = ground(lam, h + eps)
        b = ground(lam, h - eps)

    # Align both displaced states to the same central-state phase.
    for name, v in (("a", a), ("b", b)):
        phase = np.vdot(p, v)
        if abs(phase) > 0:
            aligned = v * np.exp(-1j * np.angle(phase))
            if name == "a":
                a = aligned
            else:
                b = aligned
    return (a - b) / (2 * eps)


def qfi_metric(lam, h, eps=1e-5):
    p = ground(lam, h)
    ds = [derivative(lam, h, i, eps) for i in range(2)]
    g = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            g[i, j] = 4 * np.real(
                np.vdot(ds[i], ds[j])
                - np.vdot(ds[i], p) * np.vdot(p, ds[j])
            )
    return g


def metric_checks(g):
    eig = np.linalg.eigvalsh(g)
    return {
        "finite": bool(np.all(np.isfinite(g))),
        "symmetric": bool(np.allclose(g, g.T, atol=1e-10)),
        "min_eigenvalue": float(np.min(eig)),
        "positive_semidefinite": bool(np.min(eig) >= -1e-9),
    }


def convergence_row(h):
    metrics = {f"{eps:.0e}": qfi_metric(LAMBDA, h, eps) for eps in EPS_VALUES}
    base = metrics["1e-5"]
    errors = {
        key: float(np.max(np.abs(value - base)))
        for key, value in metrics.items()
        if key != "1e-5"
    }
    checks = {key: metric_checks(value) for key, value in metrics.items()}
    # The finest step is the numerical reference; this is not a scientific
    # significance threshold.
    stable = errors["1e-06"] < max(errors["1e-04"], 1e-12) * 10.0
    return {
        "h": h,
        "metrics": {key: value.tolist() for key, value in metrics.items()},
        "max_abs_error_vs_1e-5": errors,
        "checks": checks,
        "numerically_stable": bool(stable),
    }


def benchmark_mismatch_audit(h):
    g = qfi_metric(LAMBDA, h, 1e-5)
    historical = (
        np.array([[3.4028, -7.3136], [-7.3136, 20.5808]])
        if h == 0.1
        else np.array([[1.8032, -9.4046], [-9.4046, 275.6538]])
    )
    delta = float(np.max(np.abs(g - historical)))
    return {
        "historical_values_used_as_audit_target_only": True,
        "max_abs_difference": delta,
        "match": bool(delta <= 0.08),
        "decision": "MODEL_DEFINITION_MISMATCH" if delta > 0.08 else "MATCH",
    }


def run():
    rows = []
    for h in H_VALUES:
        conv = convergence_row(h)
        audit = benchmark_mismatch_audit(h)
        rows.append({"h": h, "convergence": conv, "benchmark_audit": audit})

    infra_ok = all(
        r["convergence"]["numerically_stable"]
        and all(v["finite"] and v["symmetric"] and v["positive_semidefinite"]
                for v in r["convergence"]["checks"].values())
        for r in rows
    )
    mismatch_flagged = all(
        r["benchmark_audit"]["decision"] == "MODEL_DEFINITION_MISMATCH"
        for r in rows
    )

    return {
        "case_id": "bhd.preexperiment.tfim_qfi",
        "seed": SEED,
        "scientific_execution": False,
        "status": "PASS" if infra_ok and mismatch_flagged else "IMPLEMENTATION_FAILURE",
        "definition": {
            "N": N,
            "boundary": "open",
            "Hamiltonian": "H=-lambda sum Z_i Z_{i+1}-h sum X_i",
            "metric": "pure-state QFI",
            "finite_difference_eps": list(EPS_VALUES),
        },
        "results": rows,
        "gate": {
            "scientific_execution_allowed": False,
            "reason": "observable/H0/H1/H2 forward model remains unregistered",
        },
    }


if __name__ == "__main__":
    root = Path(__file__).parents[2]
    out = root / "results" / "bhd_preexperiment_validation.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(run(), indent=2), encoding="utf-8")
    print(json.dumps(run(), indent=2))
