"""Shared numerical primitives for simulation-matrix checks.

The functions in this module deliberately contain no stage-specific policy.  A
stage supplies its profile, grid, and acceptance threshold; this module only
computes the quantities needed to evaluate that policy.
"""

from __future__ import annotations

from typing import Callable

import numpy as np


HBAR = 1.0
MASS = 1.0
MIN_DENSITY = 1e-14
MIN_AMPLITUDE = 1e-10


def normalize(psi: np.ndarray, dx: float) -> np.ndarray:
    """Return ``psi`` normalized with respect to the supplied grid spacing."""
    norm = np.sum(np.abs(psi) ** 2) * dx
    if not np.isfinite(norm) or norm <= 0.0:
        raise ValueError("Invalid wavefunction normalization.")
    return psi / np.sqrt(norm)


def fisher_information(psi: np.ndarray, dx: float) -> float:
    """Calculate the Fisher information of the density represented by ``psi``."""
    density = np.abs(psi) ** 2
    density_gradient = np.gradient(density, dx, edge_order=2)
    mask = density > MIN_DENSITY
    return float(np.sum((density_gradient[mask] ** 2) / density[mask]) * dx)


def quantum_potential_expectation(psi: np.ndarray, x: np.ndarray) -> float:
    """Calculate the expectation of the one-dimensional quantum potential."""
    dx = x[1] - x[0]
    amplitude = np.abs(psi)
    second_derivative = np.gradient(
        np.gradient(amplitude, dx, edge_order=2),
        dx,
        edge_order=2,
    )
    mask = amplitude > MIN_AMPLITUDE
    potential = np.zeros_like(amplitude)
    potential[mask] = -(HBAR**2) * second_derivative[mask] / (2.0 * MASS * amplitude[mask])
    return float(np.sum((amplitude**2) * potential) * dx)


def fisher_equivalent(psi: np.ndarray, dx: float) -> float:
    """Return the Fisher-information form of the quantum-potential expectation."""
    return (HBAR**2 / (8.0 * MASS)) * fisher_information(psi, dx)


def relative_error(first: float, second: float) -> float:
    """Return a symmetric relative error with a non-zero denominator."""
    denominator = max(abs(first), abs(second), 1e-15)
    return abs(first - second) / denominator


def evaluate_profile(
    profile: Callable[[np.ndarray], np.ndarray],
    *,
    domain: float,
    n_points: int,
) -> dict[str, float | int | list[float]]:
    """Evaluate both formulations for a profile on a symmetric grid."""
    if domain <= 0.0:
        raise ValueError("Domain must be positive.")
    if n_points < 3:
        raise ValueError("At least three grid points are required.")

    x = np.linspace(-domain, domain, n_points)
    dx = x[1] - x[0]
    psi = normalize(profile(x), dx)
    quantum_expectation = quantum_potential_expectation(psi, x)
    equivalent = fisher_equivalent(psi, dx)

    return {
        "domain": [float(x[0]), float(x[-1])],
        "n_points": int(n_points),
        "quantum_potential_expectation": quantum_expectation,
        "fisher_equivalent": equivalent,
        "relative_error": relative_error(quantum_expectation, equivalent),
    }
