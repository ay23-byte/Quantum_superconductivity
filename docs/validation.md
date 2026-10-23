# Validation record

The numerical tests cover real-space Fourier spectra against the analytic
lattice dispersion for L=1,2,3,4; Hermiticity and BdG particle-hole pairing;
seeded disorder reproducibility; and an independent finite-grid uniform BCS
equation against clean real-space self-consistency.

Validation and execution were completed in the `quantum_sc` Python 3.11.17
environment with NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2, and pandas
3.1.0. The numerical test suite passed after the Hartree/twist additions:
8 passed. All four notebooks also
executed from fresh kernels with a noninteractive Matplotlib backend.

The clean reference comparison at L=4, U/t=2.2, T/t=0.08, mu/t=-0.5 gave
Delta/t=0.34616927167295836 from the momentum-space equation and
0.34616927167295847 from BdG (absolute difference 1.1e-16). Six additional
clean-limit crosschecks at U/t={1.5,2.2,3.0} and T/t={0.05,0.12} agreed within
3.9e-16. All clean checks converged. The clean L=4,6,8 gaps were 0.34617,
0.35871, and 0.37605, respectively. This drift is substantial; a clean L=40
value elsewhere in the project is a finite-grid reference, not an
extrapolation to the thermodynamic limit.

The extended disorder scan completed 140 unique solver runs, all converged.
That count includes 120 L=6 scan samples and 20 unique L=4 and L=8 size-check
samples; the 10 L=6 size-check samples are reused from the main scan. Each
size-check group had 10/10 converged samples. Detailed values and configuration
are stored in `results/data/research_20261023/run_metadata.json`.

All four notebooks were verified using fresh kernels. On this Windows setup,
the harness used a workspace-local Jupyter runtime/IPython directory and
worked around a kernel manager ACL restriction; this did not alter project
notebooks. A local ZMQ event-loop warning appeared during kernel shutdown, but
all cells completed.

These checks verify implementation invariants and clean-limit agreement, not
model adequacy. Pairing-only mean field omits the Hartree channel, finite
lattices do not establish thermodynamic behavior, and the calculation omits
phase fluctuations. It therefore does not measure a BKT transition or an
experimental critical temperature.

The research extension adds checks that twisted hopping matrices remain
Hermitian, zero twist reproduces the periodic matrix, a fixed-density
Hartree solution reaches its target filling, and the clean L=2 finite-twist
curvature is positive. Its L=4,6 pilot run completed 120/120 configurations;
all mean densities were within 1e-4 of target. The resulting twist curvature
is still a finite-size mean-field estimate. Phase starts, twist step, and
lattice-size scaling have not been fully converged.
