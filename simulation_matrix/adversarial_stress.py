import numpy as np


HBAR = 1.0
MASS = 1.0

X_MIN = -12.0
X_MAX = 12.0
N_POINTS = 8193

STRESS_THRESHOLD = 0.02


def normalize(psi, dx):
    rho = np.abs(psi) ** 2
    norm = np.sum(rho) * dx
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


def run_test(name, profile):
    x = np.linspace(
        X_MIN,
        X_MAX,
        N_POINTS
    )

    dx = x[1] - x[0]

    psi = normalize(
        profile(x),
        dx
    )

    fisher = fisher_information(
        psi,
        dx
    )

    qb_expectation = quantum_potential_expectation(
        psi,
        x
    )

    fisher_equivalent = (
        (HBAR ** 2) / (8.0 * MASS)
    ) * fisher

    error = relative_error(
        qb_expectation,
        fisher_equivalent
    )

    passed = (
        error < STRESS_THRESHOLD
    )

    return {
        "test": name,
        "quantum_potential_expectation": float(
            qb_expectation
        ),
        "fisher_equivalent": float(
            fisher_equivalent
        ),
        "relative_error": float(
            error
        ),
        "threshold": STRESS_THRESHOLD,
        "status": (
            "PASS"
            if passed
            else "FAIL"
        ),
    }


def run_adversarial_stress():
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
        "stage": "ADVERSARIAL_STRESS",
        "claim": (
            "<Q_B> = "
            "(hbar^2 / 8m) I_F[rho]"
        ),
        "threshold": STRESS_THRESHOLD,
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
            run_adversarial_stress(),
            indent=2
        )
  )
