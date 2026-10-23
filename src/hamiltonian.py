"""Spin-singlet Nambu Hamiltonian and spectral observables."""
from __future__ import annotations
import numpy as np

def bdg_hamiltonian(K: np.ndarray, gap: np.ndarray) -> np.ndarray:
    r"""BdG matrix in basis (c_up, c_down^dagger): [[K,-D],[-D*,-K^T]].

    The convention is Delta_i = U <c_{i down} c_{i up}> for U>0. K may be
    complex Hermitian, for example when a boundary twist is applied.
    """
    K = np.asarray(K, dtype=complex)
    gap = np.asarray(gap, dtype=complex)
    n = K.shape[0]
    if K.shape != (n, n) or gap.shape != (n,):
        raise ValueError("K must be square and gap must have one value per site")
    if not np.allclose(K, K.conj().T, atol=1e-12):
        raise ValueError("K must be Hermitian")
    D = np.diag(gap)
    return np.block([[K, -D], [-D.conj(), -K.T]])

def positive_eigensystem(K: np.ndarray, gap: np.ndarray, zero_tol: float = 1e-10):
    """Return all positive-energy eigenpairs of the Hermitian BdG matrix."""
    e, q = np.linalg.eigh(bdg_hamiltonian(K, gap))
    mask = e > zero_tol
    return e[mask], q[:, mask], e

def gaussian_dos(energies: np.ndarray, grid: np.ndarray, eta: float,
                 normalize: bool = True) -> np.ndarray:
    """Gaussian-broadened DOS; eta is the Gaussian standard deviation."""
    if eta <= 0:
        raise ValueError("eta must be positive")
    e = np.asarray(energies).ravel()
    dos = np.exp(-0.5*((grid[:, None]-e[None, :])/eta)**2).sum(axis=1)
    dos /= eta*np.sqrt(2*np.pi)
    return dos / len(e) if normalize and len(e) else dos

def electron_ldos(K: np.ndarray, gap: np.ndarray, grid: np.ndarray, eta: float) -> np.ndarray:
    """Spin-resolved electron LDOS A_i(E), normalized per site and per spin.

    Each positive BdG mode contributes |u_i|^2 at +E and |v_i|^2 at -E.
    Gaussian broadening has standard deviation eta, and the output has shape
    (n_sites, len(grid)) in states/(site energy).
    """
    if eta <= 0:
        raise ValueError("eta must be positive")
    H = bdg_hamiltonian(K, gap)
    energies, vectors = np.linalg.eigh(H)
    n = len(K)
    positive = np.flatnonzero(energies > 1e-10)
    if len(positive) != n:
        raise RuntimeError("LDOS requires exactly N positive BdG states (no exact zero modes)")
    E = energies[positive]
    u2 = np.abs(vectors[:n, positive])**2
    v2 = np.abs(vectors[n:, positive])**2
    x = np.asarray(grid)[:, None]
    plus = np.exp(-0.5*((x-E[None,:])/eta)**2)/(eta*np.sqrt(2*np.pi))
    minus = np.exp(-0.5*((x+E[None,:])/eta)**2)/(eta*np.sqrt(2*np.pi))
    return u2 @ plus.T + v2 @ minus.T
