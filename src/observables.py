"""Thermodynamic observables for self-consistent BdG solutions."""
from __future__ import annotations

import numpy as np

from .lattice import square_lattice_hamiltonian
from .solver import solve_hartree_bdg_fixed_density


def mean_field_grand_potential(K: np.ndarray, gap: np.ndarray, U: float,
                               T: float, density: np.ndarray | None = None) -> float:
    r"""Return the BdG grand potential, including Hartree double-counting correction.

    ``K`` is the effective one-spin matrix including chemical potential and,
    when supplied, the local Hartree field. ``density`` is the total local
    density (0..2); pass it for a Hartree-decoupled solution.
    """
    K = np.asarray(K, dtype=complex)
    gap = np.asarray(gap, dtype=complex)
    if K.ndim != 2 or K.shape[0] != K.shape[1] or gap.shape != (len(K),):
        raise ValueError("K must be square and gap must have one value per site")
    if U <= 0 or T < 0 or not np.allclose(K, K.conj().T):
        raise ValueError("Require U>0, T>=0, and Hermitian K")
    H = np.block([[K, -np.diag(gap)],
                  [-np.diag(gap).conj(), -K.T]])
    eig = np.linalg.eigvalsh(H)
    positive = eig[eig > 1e-10]
    value = float(np.trace(K).real + np.sum(np.abs(gap)**2)/U)
    if T == 0:
        value -= float(positive.sum())
    else:
        value -= float(2*T*np.logaddexp(positive/(2*T), -positive/(2*T)).sum())
    if density is not None:
        density = np.asarray(density, dtype=float)
        if density.shape != (len(K),) or np.any((density < -1e-9) | (density > 2+1e-9)):
            raise ValueError("density must have one value per site in [0,2]")
        value += float(U*np.sum(density**2)/4)
    return value


def phase_stiffness_fixed_density_hartree(
        L: int, U: float, T: float, target_density: float, *,
        t: float = 1.0, t_prime: float = 0.0,
        potential: np.ndarray | None = None, delta: float = 0.05,
        phase_seeds: int = 4,
        tolerance: float = 2e-5, density_tolerance: float = 1e-4,
        mixing: float = 0.1, max_iterations: int = 2500) -> dict:
    r"""Estimate 2D helicity modulus from a relaxed boundary-twist response.

    For each total x-boundary twist theta in {-delta, 0, +delta}, this
    re-solves both local density and complex pairing fields and adjusts mu to
    hold the mean density fixed. The canonical mean-field free energy is
    Omega + mu*N. In two dimensions, rho_s = d^2 F/d theta^2 for a square
    torus. This is a finite-difference static mean-field stiffness, not a BKT
    transition temperature.
    """
    if not isinstance(L, (int, np.integer)) or L < 2 or delta <= 0:
        raise ValueError("Require L>=2 and delta>0")
    nsite = L*L
    v = np.zeros(nsite) if potential is None else np.asarray(potential, dtype=float)
    if v.shape != (nsite,) or not np.all(np.isfinite(v)):
        raise ValueError(f"potential must be a finite vector of shape ({nsite},)")
    if phase_seeds < 1:
        raise ValueError("phase_seeds must be positive")
    values = {}
    xcoord = np.repeat(np.arange(L), L)
    phase_guesses = [np.zeros(nsite),
                     2*np.pi*xcoord/L,
                     -2*np.pi*xcoord/L]
    rng = np.random.default_rng(20261023)
    while len(phase_guesses) < phase_seeds:
        phase_guesses.append(rng.uniform(-np.pi, np.pi, nsite))
    phase_guesses = phase_guesses[:phase_seeds]
    for theta in (-delta, 0.0, delta):
        K0 = square_lattice_hamiltonian(L, t, t_prime, 0.0, v,
                                        twist_x=theta)
        candidates = []
        for seed_index, phase in enumerate(phase_guesses):
            guess = 0.25*np.exp(1j*phase)
            solution = solve_hartree_bdg_fixed_density(
                K0, U, T, target_density, initial_gap=guess,
                tolerance=tolerance, density_tolerance=density_tolerance,
                max_iterations=max_iterations, mixing=mixing)
            if not solution.converged:
                continue
            K_eff = K0 - solution.mu*np.eye(nsite) - np.diag(U*solution.density/2)
            omega = mean_field_grand_potential(K_eff, solution.gap, U, T,
                                                density=solution.density)
            free_energy = omega + solution.mu*target_density*nsite
            candidates.append((free_energy, seed_index, solution))
        if not candidates:
            raise RuntimeError(f"all fixed-density phase starts failed at twist {theta:g}")
        free_energy, seed_index, solution = min(candidates, key=lambda item: item[0])
        values[theta] = dict(free_energy=float(free_energy), mu=solution.mu,
                             mean_gap=float(np.mean(np.abs(solution.gap))),
                             mean_density=float(solution.density.mean()),
                             density_residual=solution.density_residual,
                             iterations=solution.iterations, phase_seed=seed_index)
    curvature = (values[delta]["free_energy"] + values[-delta]["free_energy"]
                 - 2*values[0.0]["free_energy"])/(delta**2)
    paired = values[0.0]["mean_gap"] > 1e-7
    return {"rho_s": float(curvature) if paired else None,
            "twist_curvature": float(curvature), "paired_state": bool(paired),
            "delta": float(delta),
            "phase_seeds": int(phase_seeds),
            "target_density": float(target_density), "L": int(L),
            "twists": {str(k): v for k, v in values.items()}}
