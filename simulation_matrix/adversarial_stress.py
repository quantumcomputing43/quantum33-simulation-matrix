import json
from pathlib import Path

import numpy as np


HBAR = 1.0
MASS = 1.0

STRESS_THRESHOLD = 0.02

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULT_FILE = RESULTS_DIR / "adversarial_stress.json"


def normalize(psi, dx):
    rho = np.abs(psi) ** 2
    norm = np.sum(rho) * dx

    if not np.isfinite(norm) or norm <= 0.0:
        raise ValueError("Invalid wavefunction normalization.")

    return psi / np.sqrt(norm)


def fisher_information(psi, dx):
    rho = np.abs(psi) ** 2

    drho = np.gradient(
        rho,
        dx,
        edge_order=2
    )

    mask = rho > 1e-14

    return np.sum(
        (drho[mask] ** 2) / rho[mask]
    ) * dx


def quantum_potential_expectation(psi, x):
    dx = x[1] - x[0]

    amplitude = np.abs(psi)

    d2_amplitude = np.gradient(
        np.gradient(
            amplitude,
            dx,
            edge_order=2
        ),
        dx,
        edge_order=2
    )

    mask = amplitude > 1e-10

    Q = np.zeros_like(amplitude)

    Q[mask] = (
        -(HBAR ** 2) / (2.0 * MASS)
        * d2_amplitude[mask]
        / amplitude[mask]
    )

    rho = amplitude ** 2

    return np.sum(
        rho * Q
    ) * dx


def fisher_equivalent(psi, dx):
    return (
        (HBAR ** 2) / (8.0 * MASS)
    ) * fisher_information(
        psi,
        dx
    )


def relative_error(a, b):
    denominator = max(
        abs(a),
        abs(b),
        1e-15
    )

    return abs(a - b) / denominator


def profile_gaussian(x):
    return np.exp(
        -(x ** 2) / 2.0
    )


def profile_narrow(x):
    return np.exp(
        -(x ** 2) / 0.20
    )


def profile_broad(x):
    return np.exp(
        -(x ** 2) / 12.0
    )


def profile_high_frequency(x):
    return (
        np.exp(
            -(x ** 2) / 4.0
        )
        * (
            1.0
            + 0.20 * np.cos(8.0 * x)
        )
    )


def profile_skewed(x):
    return (
        np.exp(
            -(x ** 2) / 3.0
        )
        * (
            1.0
            + 0.30 * np.tanh(2.0 * x)
        )
    )


PROFILES = {
    "S1_NARROW": profile_narrow,
    "S2_BROAD": profile_broad,
    "S3_HIGH_FREQUENCY": profile_high_frequency,
    "S4_SKEWED": profile_skewed,
    "S5_BASELINE_GAUSSIAN": profile_gaussian,
}


def run_profile_stress(name, profile):
    x = np.linspace(
        -12.0,
        12.0,
        8193
    )

    dx = x[1] - x[0]

    psi = normalize(
        profile(x),
        dx
    )

    qb = quantum_potential_expectation(
        psi,
        x
    )

    fisher_eq = fisher_equivalent(
        psi,
        dx
    )

    error = relative_error(
        qb,
        fisher_eq
    )

    return {
        "test": name,
        "domain": [
            float(x[0]),
            float(x[-1])
        ],
        "n_points": int(len(x)),
        "quantum_potential_expectation": float(qb),
        "fisher_equivalent": float(fisher_eq),
        "relative_error": float(error),
        "threshold": STRESS_THRESHOLD,
        "status": (
            "PASS"
            if error < STRESS_THRESHOLD
            else "FAIL"
        )
    }


def run_resolution_stress(profile):
    resolutions = [
        2049,
        4097,
        8193
    ]

    values = []

    for n_points in resolutions:
        x = np.linspace(
            -12.0,
            12.0,
            n_points
        )

        dx = x[1] - x[0]

        psi = normalize(
            profile(x),
            dx
        )

        qb = quantum_potential_expectation(
            psi,
            x
        )

        fisher_eq = fisher_equivalent(
            psi,
            dx
        )

        error = relative_error(
            qb,
            fisher_eq
        )

        values.append({
            "n_points": int(n_points),
            "relative_error": float(error),
            "status": (
                "PASS"
                if error < STRESS_THRESHOLD
                else "FAIL"
            )
        })

    return {
        "test": "S6_RESOLUTION_STRESS",
        "resolutions": values,
        "status": (
            "PASS"
            if all(
                item["status"] == "PASS"
                for item in values
            )
            else "FAIL"
        )
    }


def run_domain_stress(profile):
    domains = [
        8.0,
        10.0,
        12.0,
        16.0
    ]

    values = []

    for domain in domains:
        x = np.linspace(
            -domain,
            domain,
            8193
        )

        dx = x[1] - x[0]

        psi = normalize(
            profile(x),
            dx
        )

        qb = quantum_potential_expectation(
            psi,
            x
        )

        fisher_eq = fisher_equivalent(
            psi,
            dx
        )

        error = relative_error(
            qb,
            fisher_eq
        )

        values.append({
            "domain": float(domain),
            "relative_error": float(error),
            "status": (
                "PASS"
                if error < STRESS_THRESHOLD
                else "FAIL"
            )
        })

    return {
        "test": "S7_DOMAIN_STRESS",
        "domains": values,
        "status": (
            "PASS"
            if all(
                item["status"] == "PASS"
                for item in values
            )
            else "FAIL"
        )
    }


def run_adversarial_stress():
    profile_results = []

    for name, profile in PROFILES.items():
        profile_results.append(
            run_profile_stress(
                name,
                profile
            )
        )

    resolution_result = run_resolution_stress(
        profile_gaussian
    )

    domain_result = run_domain_stress(
        profile_gaussian
    )

    all_results = (
        profile_results
        + [
            resolution_result,
            domain_result
        ]
    )

    overall_pass = all(
        result["status"] == "PASS"
        for result in all_results
    )

    return {
        "stage": "ADVERSARIAL_STRESS",
        "claim": (
            "<Q_B> = "
            "(hbar^2 / 8m) I_F[rho]"
        ),
        "threshold": STRESS_THRESHOLD,
        "tests": all_results,
        "status": (
            "PASS"
            if overall_pass
            else "FAIL"
        )
    }


def save_result(result):
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    RESULT_FILE.write_text(
        json.dumps(
            result,
            indent=2
        ),
        encoding="utf-8"
    )


if __name__ == "__main__":
    result = run_adversarial_stress()

    save_result(result)

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    if result["status"] != "PASS":
        raise SystemExit(1)
