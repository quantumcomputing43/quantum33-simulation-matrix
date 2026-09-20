import numpy as np

from simulation_matrix.numerics import evaluate_profile


RELATIVE_ERROR_THRESHOLD = 0.02

X_MIN = -12.0
X_MAX = 12.0
N_POINTS = 8193


def gaussian(x):
    return np.exp(
        -(x ** 2) / 2.0
    )


def non_gaussian(x):
    return np.exp(
        -(x ** 4) / 4.0
    )


def multi_peak(x):
    return (
        np.exp(
            -((x - 2.0) ** 2) / 1.5
        )
        + 0.7 * np.exp(
            -((x + 2.0) ** 2) / 2.0
        )
    )


def asymmetric(x):
    return (
        np.exp(
            -(x ** 2) / 2.0
        )
        * (
            1.0
            + 0.20 * np.tanh(x)
        )
    )


def boundary_stress(x):
    return (
        np.exp(
            -(x ** 2) / 5.0
        )
        * (
            1.0
            + 0.15 * np.cos(2.0 * x)
        )
    )


PROFILES = {
    "F1_GAUSSIAN": gaussian,
    "F2_NON_GAUSSIAN": non_gaussian,
    "F3_MULTI_PEAK": multi_peak,
    "F4_ASYMMETRIC": asymmetric,
    "F5_BOUNDARY_STRESS": boundary_stress,
}


def run_test(name, profile):
    evaluation = evaluate_profile(profile, domain=X_MAX, n_points=N_POINTS)
    error = evaluation["relative_error"]

    return {
        "test": name,
        "quantum_potential_expectation": evaluation["quantum_potential_expectation"],
        "fisher_equivalent": evaluation["fisher_equivalent"],
        "relative_error": error,
        "threshold": RELATIVE_ERROR_THRESHOLD,
        "status": (
            "PASS"
            if error < RELATIVE_ERROR_THRESHOLD
            else "FAIL"
        ),
    }


def run_falsification():
    results = []

    for name, profile in PROFILES.items():
        results.append(
            run_test(
                name,
                profile
            )
        )

    overall_pass = all(
        result["status"] == "PASS"
        for result in results
    )

    return {
        "stage": "FALSIFICATION",
        "claim": (
            "<Q_B> = "
            "(hbar^2 / 8m) I_F[rho]"
        ),
        "threshold": RELATIVE_ERROR_THRESHOLD,
        "tests": results,
        "status": (
            "PASS"
            if overall_pass
            else "FAIL"
        ),
    }


if __name__ == "__main__":
    import json

    print(
        json.dumps(
            run_falsification(),
            indent=2
        )
    )
