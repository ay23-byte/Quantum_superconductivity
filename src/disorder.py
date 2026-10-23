"""Reproducible scalar onsite disorder generators."""
from __future__ import annotations
import numpy as np

def onsite_disorder(n_sites: int, strength: float, distribution: str = "uniform",
                    seed: int | None = None) -> np.ndarray:
    """Generate onsite energies in units consistent with hopping.

    Uniform strength W means support [-W/2,W/2] and variance W^2/12.
    Gaussian strength W means standard deviation W (clearly distinct convention).
    """
    if n_sites < 1 or strength < 0:
        raise ValueError("n_sites must be positive and strength nonnegative")
    rng = np.random.default_rng(seed)
    if distribution == "uniform":
        return rng.uniform(-strength/2, strength/2, n_sites)
    if distribution == "gaussian":
        return rng.normal(0, strength, n_sites)
    if distribution == "none":
        return np.zeros(n_sites)
    raise ValueError("distribution must be 'uniform', 'gaussian', or 'none'")
