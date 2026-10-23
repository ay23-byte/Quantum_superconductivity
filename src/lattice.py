"""Square-lattice tight-binding operators with periodic boundary conditions."""
from __future__ import annotations

import numpy as np


def square_lattice_hamiltonian(
    L: int, t: float = 1.0, t_prime: float = 0.0, mu: float = 0.0,
    potential: np.ndarray | None = None, twist_x: float = 0.0,
    twist_y: float = 0.0,
) -> np.ndarray:
    """Return the one-spin K for an LxL periodic square lattice.

    The dispersion is -2t(cos kx+cos ky)-4t'cos(kx)cos(ky)-mu.
    Periodic directed bonds are accumulated as a sum of translations, so bonds
    that coincide at L=1 or L=2 retain their correct multiplicity. ``twist_x``
    and ``twist_y`` are total boundary phase twists in radians; each bond gets
    the Peierls phase exp(i*(dx*twist_x+dy*twist_y)/L).
    """
    if not isinstance(L, (int, np.integer)) or L < 1:
        raise ValueError("L must be a positive integer")
    n = L * L
    v = np.zeros(n) if potential is None else np.asarray(potential, dtype=float)
    if v.shape != (n,) or not np.all(np.isfinite(v)):
        raise ValueError(f"potential must be a finite vector of shape ({n},)")
    K = np.diag((v - mu).astype(complex))
    bonds = ((1, 0, t), (-1, 0, t), (0, 1, t), (0, -1, t),
             (1, 1, t_prime), (1, -1, t_prime),
             (-1, 1, t_prime), (-1, -1, t_prime))
    for x in range(L):
        for y in range(L):
            i = x * L + y
            for dx, dy, amp in bonds:
                if amp:
                    j = ((x + dx) % L) * L + (y + dy) % L
                    phase = np.exp(1j*(dx*twist_x + dy*twist_y)/L)
                    K[i, j] -= amp*phase
    return K


def square_lattice_dispersion(kx: np.ndarray, ky: np.ndarray, t: float = 1.0,
                              t_prime: float = 0.0, mu: float = 0.0) -> np.ndarray:
    """Tight-binding energy xi(k), in the same convention as the real-space K."""
    return -2*t*(np.cos(kx)+np.cos(ky))-4*t_prime*np.cos(kx)*np.cos(ky)-mu


def momentum_grid(L: int) -> tuple[np.ndarray, np.ndarray]:
    """Allowed periodic momenta in [-pi, pi), returned as kx and ky grids."""
    k = 2*np.pi*np.fft.fftfreq(L)
    return np.meshgrid(k, k, indexing="ij")
