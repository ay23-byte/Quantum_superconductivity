"""Self-consistent finite-temperature onsite spin-singlet BdG solver."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .hamiltonian import positive_eigensystem, bdg_hamiltonian

@dataclass
class BdGResult:
    gap: np.ndarray
    energies: np.ndarray
    all_energies: np.ndarray
    residual_history: list[float]
    converged: bool
    iterations: int

def solve_bdg(K: np.ndarray, U: float, T: float, initial_gap: float | np.ndarray = 0.2,
              tolerance: float = 1e-8, max_iterations: int = 500,
              mixing: float = 0.35) -> BdGResult:
    """Solve Delta_i=U<c_down c_up> using damped fixed-point iteration.

    Energies and T are in the same units (k_B=1). U>0 is the magnitude of
    attraction. No Hartree term is included. A non-converged result is returned
    with converged=False; callers must not interpret it as a solution.
    """
    K = np.asarray(K, dtype=complex)
    if K.ndim != 2 or K.shape[0] != K.shape[1] or not np.allclose(K, K.conj().T):
        raise ValueError("K must be a Hermitian square matrix")
    n = len(K)
    if U <= 0 or T < 0 or tolerance <= 0 or max_iterations < 1 or not (0 < mixing <= 1):
        raise ValueError("Require U>0, T>=0, tolerance>0, max_iterations>=1, 0<mixing<=1")
    gap = np.full(n, float(initial_gap)) if np.isscalar(initial_gap) else np.array(initial_gap, dtype=float, copy=True)
    if gap.shape != (n,):
        raise ValueError(f"initial_gap must be scalar or shape ({n},)")
    hist: list[float] = []
    energies = all_e = np.empty(0)
    for _ in range(max_iterations):
        energies, vecs, all_e = positive_eigensystem(K, gap)
        # Exact zero modes are omitted from the anomalous update because their
        # finite-temperature tanh(E/2T) factor is zero. At T=0 the convention
        # is the zero-temperature limit; a strictly zero mode contributes no
        # well-defined anomalous amplitude without a symmetry-breaking field.
        uvec, vvec = vecs[:n], vecs[n:]
        thermal = np.ones_like(energies) if T == 0 else np.tanh(energies/(2*T))
        updated = -U*np.sum(uvec*np.conjugate(vvec)*thermal[None, :], axis=1)
        updated = np.real_if_close(updated, tol=1000)
        residual = float(np.max(np.abs(updated-gap)))
        hist.append(residual)
        if residual < tolerance:
            gap = updated
            energies, _, all_e = positive_eigensystem(K, gap)
            return BdGResult(gap, energies, all_e, hist, True, len(hist))
        gap = (1-mixing)*gap + mixing*updated
    energies, _, all_e = positive_eigensystem(K, gap)
    return BdGResult(gap, energies, all_e, hist, False, len(hist))

def density_from_result(K: np.ndarray, result: BdGResult, T: float) -> np.ndarray:
    """Return total (up+down) site density, 0..2, for the result eigenvectors.

    Re-diagonalizes at the final gap. This is a pairing-only mean-field density.
    """
    from .hamiltonian import positive_eigensystem
    n = len(K)
    from .hamiltonian import bdg_hamiltonian
    e, q = np.linalg.eigh(bdg_hamiltonian(K, result.gap))
    pos = e > 1e-10
    zero = np.abs(e) <= 1e-10
    u, v = q[:n, pos], q[n:, pos]
    f = np.zeros(np.count_nonzero(pos)) if T == 0 else 1/(np.exp(np.clip(e[pos]/T, -700, 700))+1)
    density = 2*np.sum(np.abs(u)**2*f[None, :] + np.abs(v)**2*(1-f)[None, :], axis=1)
    # A zero-energy state has half occupation at finite T (and by the symmetric
    # zero-temperature limiting convention adopted here).
    if np.any(zero):
        density += np.sum(np.abs(q[:n, zero])**2, axis=1)
    return density


@dataclass
class HartreeBdGResult:
    """Converged balanced Hartree+pairing BdG solution."""
    gap: np.ndarray
    density: np.ndarray
    energies: np.ndarray
    all_energies: np.ndarray
    residual_history: list[float]
    converged: bool
    iterations: int
    mu: float
    density_residual: float


def solve_hartree_bdg(K0: np.ndarray, U: float, T: float, mu: float,
                      initial_gap: float | np.ndarray = 0.2,
                      initial_density: float | np.ndarray = 1.0,
                      tolerance: float = 1e-7, max_iterations: int = 800,
                      mixing: float = 0.2) -> HartreeBdGResult:
    r"""Solve balanced attractive-Hubbard BdG with local Hartree feedback.

    ``K0`` contains hopping and onsite disorder but no chemical potential or
    Hartree field. The effective one-spin matrix is
    ``K0 - mu*I - diag(U*n_i/2)`` where ``n_i`` is the total local density.
    Both density and complex pairing fields are iterated self-consistently.
    """
    K0 = np.asarray(K0, dtype=complex)
    if K0.ndim != 2 or K0.shape[0] != K0.shape[1] or not np.allclose(K0, K0.conj().T):
        raise ValueError("K0 must be a Hermitian square matrix")
    n = len(K0)
    if U <= 0 or T < 0 or tolerance <= 0 or max_iterations < 1 or not (0 < mixing <= 1):
        raise ValueError("Require U>0, T>=0, tolerance>0, max_iterations>=1, 0<mixing<=1")
    gap = np.full(n, complex(initial_gap)) if np.isscalar(initial_gap) else np.asarray(initial_gap, dtype=complex).copy()
    density = np.full(n, float(initial_density)) if np.isscalar(initial_density) else np.asarray(initial_density, dtype=float).copy()
    if gap.shape != (n,) or density.shape != (n,) or not np.all(np.isfinite(density)):
        raise ValueError(f"initial fields must have shape ({n},) and finite density")
    history: list[float] = []
    energies = all_e = np.empty(0)
    density_residual = np.inf
    for _ in range(max_iterations):
        K = K0 - mu*np.eye(n) - np.diag(U*density/2)
        H = bdg_hamiltonian(K, gap)
        all_e, vecs = np.linalg.eigh(H)
        positive = all_e > 1e-10
        energies = all_e[positive]
        q = vecs[:, positive]
        u, v = q[:n], q[n:]
        thermal = np.ones_like(energies) if T == 0 else np.tanh(energies/(2*T))
        updated_gap = -U*np.sum(u*np.conjugate(v)*thermal[None, :], axis=1)
        updated_gap = np.real_if_close(updated_gap, tol=1000)
        f = np.zeros_like(energies) if T == 0 else 1/(np.exp(np.clip(energies/T, -700, 700))+1)
        updated_density = 2*np.sum(np.abs(u)**2*f[None, :] + np.abs(v)**2*(1-f)[None, :], axis=1)
        zero = np.abs(all_e) <= 1e-10
        if np.any(zero):
            updated_density += np.sum(np.abs(vecs[:n, zero])**2, axis=1)
        gap_residual = float(np.max(np.abs(updated_gap-gap)))
        density_residual = float(np.max(np.abs(updated_density-density)))
        residual = max(gap_residual, density_residual)
        history.append(residual)
        if residual < tolerance:
            gap, density = updated_gap, updated_density
            K = K0 - mu*np.eye(n) - np.diag(U*density/2)
            energies, _, all_e = positive_eigensystem(K, gap)
            return HartreeBdGResult(gap, density, energies, all_e, history, True,
                                    len(history), float(mu), density_residual)
        gap = (1-mixing)*gap + mixing*updated_gap
        density = (1-mixing)*density + mixing*updated_density
    K = K0 - mu*np.eye(n) - np.diag(U*density/2)
    energies, _, all_e = positive_eigensystem(K, gap)
    return HartreeBdGResult(gap, density, energies, all_e, history, False,
                            len(history), float(mu), density_residual)


def solve_hartree_bdg_fixed_density(
        K0: np.ndarray, U: float, T: float, target_density: float,
        initial_gap: float | np.ndarray = 0.2,
        tolerance: float = 1e-5, density_tolerance: float = 1e-5,
        max_iterations: int = 3000, mixing: float = 0.15) -> HartreeBdGResult:
    """Solve Hartree+pairing BdG while adjusting mu to fix mean total density.

    Chemical potential is updated inside the self-consistency loop. This avoids
    assuming that a separate fixed-mu root search follows a single branch near
    finite-size mean-field transitions.
    """
    K0 = np.asarray(K0, dtype=complex)
    if K0.ndim != 2 or K0.shape[0] != K0.shape[1] or not np.allclose(K0, K0.conj().T):
        raise ValueError("K0 must be a Hermitian square matrix")
    n = len(K0)
    if (U <= 0 or T < 0 or not (0 < target_density < 2) or density_tolerance <= 0
            or tolerance <= 0 or max_iterations < 1 or not (0 < mixing <= 1)):
        raise ValueError("Require U>0, T>=0, 0<target_density<2, positive tolerances, "
                         "max_iterations>=1, and 0<mixing<=1")
    eig = np.linalg.eigvalsh(K0)
    mu = float(np.quantile(eig, target_density/2)-U*target_density/2)
    gap = np.full(n, complex(initial_gap)) if np.isscalar(initial_gap) else np.asarray(initial_gap, dtype=complex).copy()
    density = np.full(n, target_density, dtype=float)
    if gap.shape != (n,):
        raise ValueError(f"initial_gap must be scalar or shape ({n},)")
    mu_mixing = 0.5
    max_mu_step = 0.25
    history: list[float] = []
    energies = all_e = np.empty(0)
    density_residual = np.inf
    for _ in range(max_iterations):
        K = K0 - mu*np.eye(n) - np.diag(U*density/2)
        H = bdg_hamiltonian(K, gap)
        all_e, vecs = np.linalg.eigh(H)
        positive = all_e > 1e-10
        energies = all_e[positive]
        q = vecs[:, positive]
        u, v = q[:n], q[n:]
        thermal = np.ones_like(energies) if T == 0 else np.tanh(energies/(2*T))
        updated_gap = -U*np.sum(u*np.conjugate(v)*thermal[None, :], axis=1)
        updated_gap = np.real_if_close(updated_gap, tol=1000)
        f = np.zeros_like(energies) if T == 0 else 1/(np.exp(np.clip(energies/T, -700, 700))+1)
        updated_density = 2*np.sum(np.abs(u)**2*f[None, :] + np.abs(v)**2*(1-f)[None, :], axis=1)
        zero = np.abs(all_e) <= 1e-10
        if np.any(zero):
            updated_density += np.sum(np.abs(vecs[:n, zero])**2, axis=1)
        density_residual = abs(float(updated_density.mean()-target_density))
        gap_residual = float(np.max(np.abs(updated_gap-gap)))
        local_density_residual = float(np.max(np.abs(updated_density-density)))
        history.append(max(gap_residual, local_density_residual, density_residual))
        if (gap_residual < tolerance and local_density_residual < tolerance
                and density_residual < density_tolerance):
            gap, density = updated_gap, updated_density
            K = K0 - mu*np.eye(n) - np.diag(U*density/2)
            energies, _, all_e = positive_eigensystem(K, gap)
            return HartreeBdGResult(gap, density, energies, all_e, history, True,
                                    len(history), float(mu), density_residual)
        mu_step = np.clip(mu_mixing*(target_density-updated_density.mean()),
                          -max_mu_step, max_mu_step)
        mu += float(mu_step)
        gap = (1-mixing)*gap + mixing*updated_gap
        density = (1-mixing)*density + mixing*updated_density
    K = K0 - mu*np.eye(n) - np.diag(U*density/2)
    energies, _, all_e = positive_eigensystem(K, gap)
    return HartreeBdGResult(gap, density, energies, all_e, history, False,
                            len(history), float(mu), density_residual)
