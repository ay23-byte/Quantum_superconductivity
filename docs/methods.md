# Numerical methods and run configuration

`src/lattice.py` constructs the one-spin kinetic matrix and momentum
dispersion. `src/hamiltonian.py` builds the Hermitian Nambu matrix, electron DOS,
and site-resolved LDOS. `src/solver.py` diagonalizes densely with
`numpy.linalg.eigh` and uses damped fixed-point updates; convergence is the
maximum absolute gap update before mixing. Results record convergence status,
iteration count, and residual history. `src/gap_equation.py` is an independent
k-space uniform solver. Disorder uses NumPy `default_rng` and explicit integer
seeds.

The default quick run is `python scripts/run_quick_research.py`: L=6,
W/t={0,0.6,1.2}, t'/t={0,0.2}, and three disorder realizations per pair.
The completed extended run was generated with:

```powershell
python scripts/run_quick_research.py --run-id research_20261023 --realizations 20 --size-check-realizations 10
```

It used 20 realizations for each of the six L=6 scan points (120 solves), plus
10 samples at each of L=4,6,8 for a disorder finite-size check. The L=6 samples
were reused between the scan and the size check, for 140 unique solver runs.
Common parameters were t=1, mu=-0.5, U=2.2, T=0.08, tolerance 2e-6, mixing
0.55, and seed base 94721. Each disorder realization uses the same seed at
both hopping values. The size check uses W=1.2 and t'=0. Full details and
software versions are in
`results/data/research_20261023/run_metadata.json`.

The pairing amplitude is the spatial mean of the local self-consistent gap;
the reported spatial standard deviation measures its variation within one
disorder sample. SEM is calculated across disorder realizations, never across
sites. DOS uses Gaussian broadening sigma=0.06t. The run saves realization
tables, summary tables, crosschecks, selected raw arrays, and figures in
`results/data/research_20261023/` and
`results/figures/research_20261023/`.

This remains an exploratory finite-size calculation, not a controlled
thermodynamic-limit study. The disorder size check shows visible size
dependence and only ten samples at each size. Dense diagonalization scales as
O(N^2) memory and O(N^3) operations; larger lattices become costly quickly.

## Fixed-density Hartree extension

`src/solver.py` also provides a balanced Hartree+pairing solver. Its effective
one-spin matrix is `K0 - mu*I - diag(U*n_i/2)`, and it updates local density,
complex pairing, and chemical potential together. The research extension run
uses fixed mean density n=0.87 rather than fixed chemical potential. The
`src/observables.py` finite-difference response applies a total boundary twist
and recomputes the self-consistent solution and chemical potential at three
twists. It compares a finite set of phase initial states and reports the
canonical free-energy curvature. This curvature is a finite-size mean-field
response estimate; twist-step and phase-start checks are required before
interpreting it as a stable helicity modulus.

Run the completed L=4,6 pilot with:

```powershell
python scripts/run_fixed_density_research.py --run-id research_hartree_20261023 --sizes 4 6 --realizations 10 --phase-seeds 1 --twist-step 0.05
```

The current pilot uses ten disorder realizations and one phase initialization
per twist for practical runtime. It is not enough for thermodynamic claims;
the configuration, failure log, data, and figures are recorded in the
matching `results/` run directories.
