"""Independent finite-grid uniform BCS reference calculation."""
from __future__ import annotations
import numpy as np
from scipy.optimize import brentq
from .lattice import momentum_grid, square_lattice_dispersion

def uniform_gap(L: int, U: float, T: float, t: float = 1.0,
               t_prime: float = 0.0, mu: float = 0.0,
               samples: int | None = None) -> float:
    r"""Solve 1=(U/2N_k) sum_k tanh(E_k/2T)/E_k on a periodic k grid.

    This is the pairing-only, fixed chemical potential finite-bandwidth model;
    it has no Debye cutoff. At T=0, tanh(E/2T) is interpreted as one.
    """
    if L < 1 or U <= 0 or T < 0:
        raise ValueError("Require L>=1, U>0, and T>=0")
    ngrid = samples or L
    kx, ky = momentum_grid(ngrid)
    xi = square_lattice_dispersion(kx, ky, t, t_prime, mu).ravel()
    def rhs(delta: float) -> float:
        E = np.sqrt(xi*xi+delta*delta)
        factor = np.ones_like(E) if T == 0 else np.tanh(E/(2*T))
        return U/2*np.mean(factor/E)
    if rhs(1e-12) <= 1:
        return 0.0
    hi = max(U, 1.0)
    while rhs(hi) > 1:
        hi *= 2
    return float(brentq(lambda d: rhs(d)-1, 1e-12, hi, xtol=1e-13))

