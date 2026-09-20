import json
from pathlib import Path

import numpy as np

from simulation_matrix.numerics import evaluate_profile


STRESS_THRESHOLD = 0.02

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULT_FILE = RESULTS_DIR / "adversarial_stress.json"


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
    evaluation = evaluate_profile(profile, domain=12.0, n_points=8193)
    error = evaluation["relative_error"]

    return {
        "test": name,
        **evaluation,
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
        evaluation = evaluate_profile(profile, domain=12.0, n_points=n_points)
        error = evaluation["relative_error"]

        values.append({
            "n_points": int(n_points),
            "relative_error": error,
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
        evaluation = evaluate_profile(profile, domain=domain, n_points=8193)
        error = evaluation["relative_error"]

        values.append({
            "domain": float(domain),
            "relative_error": error,
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
