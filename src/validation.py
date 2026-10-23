"""Numerical validation helpers for the attractive-Hubbard BdG implementation."""
from __future__ import annotations
import numpy as np
from .lattice import square_lattice_hamiltonian
from .gap_equation import uniform_gap
from .solver import solve_bdg

def clean_limit_comparison(L: int = 4, U: float = 2.0, T: float = 0.05,
                          mu: float = -0.5, t: float = 1.0,
                          t_prime: float = 0.0, **solver_options) -> dict[str, float | bool]:
    """Compare the translationally invariant BdG solution to k-space BCS."""
    K = square_lattice_hamiltonian(L, t, t_prime, mu)
    reference = uniform_gap(L, U, T, t, t_prime, mu)
    result = solve_bdg(K, U, T, initial_gap=max(reference, 0.1), **solver_options)
    return {"reference_gap": reference, "bdg_mean_gap": float(result.gap.mean()),
            "spatial_std": float(result.gap.std()),
            "absolute_difference": abs(float(result.gap.mean())-reference),
            "converged": result.converged, "iterations": result.iterations}

def particle_hole_error(eigenvalues: np.ndarray) -> float:
    """Maximum |E_n+E_{-n}| after sorting a BdG spectrum."""
    e = np.sort(np.asarray(eigenvalues))
    return float(np.max(np.abs(e+e[::-1])))
