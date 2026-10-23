# Pairing in a disordered square-lattice attractive Hubbard model

## Abstract

We implemented a self-consistent finite-temperature, pairing-only BdG solver
for the square-lattice attractive Hubbard model with scalar onsite disorder
and next-nearest-neighbor hopping. The clean finite-grid solution agrees with
an independent momentum-space gap equation to numerical precision across
seven parameter checks. An exploratory run completed 140 unique solver
calculations: a 20-realization L=6 scan over three disorder strengths and two
hopping values, plus a ten-realization disorder size check at L=4,6,8. Every
calculation converged. Disorder increased spatial variation in the pairing
field in the L=6 scan, while the mean pairing response depended on t'. The
size check shows visible finite-size and sample uncertainty. These results
validate an implementation and describe an exploratory scan; they do not
establish thermodynamic behavior, a transition temperature, or a novel
mechanism.

## Introduction and prior work

Spatially inhomogeneous pairing under disorder has been studied using
real-space BdG methods, including Ghosal, Randeria, and Trivedi (2001).
Next-nearest-neighbor hopping effects in the attractive Hubbard model were
also studied using quantum Monte Carlo, including Fontenele et al. (2023,
fixed-density DQMC) and Fontenele et al. (2026, determinant QMC response
functions and critical temperatures). The broad themes of disorder-driven
pairing inhomogeneity and t'-dependent pairing are established. This project
does not claim novelty for their combination; no exhaustive search was made
to determine whether this precise disorder-plus-t' parameter scan has prior
precedent.

## Research question and model

The exploratory question is how nonmagnetic onsite disorder and t'/t alter
the local pairing amplitude and positive quasiparticle spectrum in a finite
two-dimensional square-lattice attractive Hubbard model at fixed chemical
potential. The Hamiltonian, sign conventions, pairing-only decoupling, Nambu
matrix, and gap equation are given in [theory.md](theory.md). The chemical
potential is fixed at mu/t=-0.5 and Hartree feedback is omitted. Disorder is
uniform on [-W/2,W/2], with W/t={0,0.6,1.2}; t'/t={0,0.2}.

## Methods and validation

The main scan uses L=6, t=1, U=2.2, T=0.08, 20 realizations per W,t' pair,
tolerance 2e-6, and mixing 0.55. A disorder size check uses W=1.2, t'=0,
10 realizations per size at L=4,6,8, reusing the L=6 samples from the main
scan. In total 140 unique solver runs completed and converged. Six additional
clean-limit checks at L=4 varied U/t={1.5,2.2,3.0} and T/t={0.05,0.12}.
Momentum-space and real-space gaps agreed within 3.9e-16 across these checks.
Software versions and full run configuration are recorded in
`results/data/research_20261023/run_metadata.json`.

## Results

At L=6, the mean spatial pairing amplitude (mean ± SEM across 20 disorder
realizations) was:

| t'/t | W/t=0 | W/t=0.6 | W/t=1.2 |
|---:|---:|---:|---:|
| 0.0 | 0.35870 ± 0.00000 | 0.36960 ± 0.00405 | 0.37796 ± 0.00490 |
| 0.2 | 0.32003 ± 0.00000 | 0.31991 ± 0.00127 | 0.31855 ± 0.00263 |

The within-sample spatial standard deviation increased with disorder. For
t'/t=0 it was 0.00000, 0.02538, and 0.04752 at W/t=0, 0.6, and 1.2. For
t'/t=0.2 it was approximately 0.00000, 0.02724, and 0.05448. These are
descriptive finite-L results: at t'=0 the mean rises modestly with W, while
at t'=0.2 it is nearly flat and trends slightly down. They do not support a
universal disorder trend.

At W/t=1.2 and t'/t=0, the ten-sample size check gave mean pairing amplitudes
of 0.36898 ± 0.02218, 0.38687 ± 0.00679, and 0.37868 ± 0.00445 for L=4,6,8.
The central values are not monotonic in L, and the uncertainty remains
material. This is not a finite-size extrapolation. Realization-level values,
summary tables, saved arrays, and figures are in
`results/data/research_20261023/` and `results/figures/research_20261023/`.

## Discussion and limitations

The run demonstrates working lattice construction, particle-hole symmetry,
seeded disorder generation, clean-limit agreement, and convergent
self-consistency for the recorded parameter sets. The scan is exploratory:
20 disorder realizations and L=6 are insufficient for robust finite-size
inference, while the size check has only ten samples per size. Pairing
amplitude is neither the quasiparticle spectral gap nor an experimental
transition temperature. In two dimensions phase fluctuations and BKT physics
are absent; the calculation also omits Hartree feedback and fixes chemical
potential rather than density. Novelty is not established.

## Reproducibility and next work

Install dependencies from `requirements.txt`. Run
`python -m pytest tests\\test_numerics.py -q -p no:cacheprovider` and execute
the four notebooks to reproduce implementation checks. The extended run is
`python scripts\\run_quick_research.py --run-id research_20261023 --realizations 20 --size-check-realizations 10`.
Before making stronger physical claims, increase sample counts and lattice
sizes, solve at fixed density, quantify alternative disorder distributions
at matched variance, and compare with a many-body method or established
benchmark.
