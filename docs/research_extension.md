# Fixed-density Hartree and phase-response extension

## Research question

At a fixed mean filling of n=0.87, how do onsite disorder and next-neighbor
hopping affect the self-consistent pairing field and the finite-size response
to a boundary phase twist? This isolates hopping and disorder changes from
changes in average density that occur when chemical potential is held fixed.

## Model additions

The one-spin matrix includes the self-consistent Hartree field

`K_eff = K0 - mu I - diag(U n_i / 2)`,

where U>0 is the magnitude of the onsite attraction and n_i is the total
local density. The solver updates the local density, complex pairing field,
and chemical potential together. The chemical-potential update enforces the
target mean density; each returned run records the remaining density residual.

To estimate a phase response, the code places a Peierls phase on every
directed hopping link corresponding to total x-boundary twist theta. It
self-consistently re-solves the Hartree and complex pairing fields for
theta=-delta, 0, +delta, adjusts mu at every twist to hold density fixed, and
calculates the canonical mean-field free energy F=Omega+mu*N. The reported
twist curvature is

`[F(+delta) + F(-delta) - 2 F(0)] / delta^2`.

For a square two-dimensional torus this has the units and normalization of a
helicity-modulus estimate. The implementation tries a configurable set of
initial phase configurations and selects the lowest converged mean-field free
energy among those starts. A finite set of starts does not prove a global
minimum. Negative or unusually large curvature must be treated as a stability
or finite-size warning until it survives twist-step, phase-search, and size
checks. The quantity is not a BKT transition temperature.

## Completed pilot calculation

Run ID: `research_hartree_20261023`. Parameters: t=1, U=2.2, T=0.08,
n=0.87, W/t={0,0.6,1.2}, t'/t={0,0.2}, L={4,6}, and ten disorder
realizations per point. The generated run used one phase initialization per
twist for throughput; phase-start sensitivity is therefore still required.
All 120 calculations converged, and the maximum mean-density residual was
1.25e-6 (the requested tolerance was 1e-4).

At L=6 and t'/t=0, mean pairing amplitude (mean ± SEM over ten disorder
samples) was 0.49424 ± 0.00000, 0.43849 ± 0.00887, and 0.37052 ± 0.01292 at
W/t=0, 0.6, and 1.2. At t'/t=0.2 it was 0.48475 ± 0.00000, 0.43823 ±
0.00819, and 0.36673 ± 0.01104. Within this parameter set, the mean pairing
decreased as disorder increased at fixed density.

At L=6, the mean twist curvature at t'/t=0 decreased from 0.73477 in the
clean case to 0.53196 ± 0.03235 at W/t=0.6 and 0.34213 ± 0.03015 at W/t=1.2.
At t'/t=0.2 it was 0.78024, 0.56820 ± 0.03612, and 0.31908 ± 0.03065,
respectively. This is a finite-size mean-field response. Ten samples per
point and two small lattice sizes are not enough for a thermodynamic or
transition claim. At L=4, t'/t=0.2, W/t=1.2, the sample-averaged curvature
was slightly negative and its uncertainty included zero; this reinforces the
need to check phase starts and twist-step convergence before interpreting
the response.

## Expanded parameter grid and phase-start check

Run ID: `research_hartree_robust_20261023`. The full grid uses L=4,6,
t'/t={0,0.2}, W/t={0,0.6,1.2}, twenty disorder realizations per point,
and two deterministic phase starts per twist, for 240 converged calculations
and zero failures. The maximum density residual was 1.20e-5, below the
1e-4 tolerance. At L=6, the disorder trends were:

| t'/t | W/t | Mean pairing / t | Mean twist curvature / t |
|---:|---:|---:|---:|
| 0.0 | 0.0 | 0.49424 +/- 0.00000 | 0.73477 +/- 0.00000 |
| 0.0 | 0.6 | 0.43116 +/- 0.00721 | 0.51064 +/- 0.02542 |
| 0.0 | 1.2 | 0.37803 +/- 0.00681 | 0.37273 +/- 0.01708 |
| 0.2 | 0.0 | 0.48476 +/- 0.00000 | 0.78024 +/- 0.00000 |
| 0.2 | 0.6 | 0.43199 +/- 0.00661 | 0.54365 +/- 0.02895 |
| 0.2 | 1.2 | 0.37581 +/- 0.00611 | 0.35960 +/- 0.01886 |

Across the six matched parameter points, the new run's first ten disorder
realizations reuse the seeds from the earlier one-start pilot. Comparing those
paired samples, the mean twist-curvature change from adding the second start
was at most 4.8e-8, while the second start was selected for 95 of 240 runs.
This checks the effect of these two starts on this grid; it does not prove a
global minimum. The L=4, t'/t=0.2, W/t=1.2 curvature is
-0.04290 +/- 0.09026, so it is statistically consistent with zero at this
sample size. Raw data and figures are in
`results/data/research_hartree_robust_20261023/` and
`results/figures/research_hartree_robust_20261023/`.

## Selected-point convergence study

The convergence workflow examines W/t=1.2, t'/t=0, n=0.87 at L=4,6,8. It
uses twelve deterministically seeded disorder realizations per size and
repeats each realization at twist steps delta={0.1,0.05,0.025}. Size
comparisons use the same sample count and smallest twist step. Twist
comparisons use the intersection of successful realization IDs across the
three steps. Sample-count curves use cumulative prefixes, so neighboring
points on that curve are correlated. All 108/108 calculations converged;
the largest recorded mean-density residual was 1.41e-6 (tolerance 1e-4).

At delta=0.025, the measured mean pairing and twist curvature (mean +/- SEM)
were:

| L | Mean pairing / t | Mean twist curvature / t |
|---:|---:|---:|
| 4 | 0.33122 +/- 0.03142 | 0.15064 +/- 0.06307 |
| 6 | 0.37653 +/- 0.01043 | 0.36665 +/- 0.02938 |
| 8 | 0.36584 +/- 0.00463 | 0.43116 +/- 0.01285 |

The twist-step change from delta=0.1 to 0.025 fell from 0.00217 at L=4 to
0.00055 at L=6 and 0.00030 at L=8. The response still changes substantially
with lattice size, so this is evidence of finite-difference stability over
these steps, not size convergence or a thermodynamic result. Generated CSV
summaries, metadata, and frontend data live in
`results/data/convergence_hartree_20261023/` and
`frontend/convergence_data.js`.

### Extended four-size convergence scan: 12 samples

Run ID: `convergence_hartree_extended_20261023`. The original 108 L=4,6,8
rows were reused, and the 36 missing L=10 cases were calculated, giving a
matched 12-disorder-sample scan at each of L=4,6,8,10 and each of
delta={0.1,0.05,0.025}. All 144/144 calculations converged; the maximum
mean-density residual remained 1.41e-6 (tolerance 1e-4).

At delta=0.025, the four-size results are:

| L | Mean pairing / t | Mean twist curvature / t |
|---:|---:|---:|
| 4 | 0.33122 +/- 0.03142 | 0.15064 +/- 0.06307 |
| 6 | 0.37653 +/- 0.01043 | 0.36665 +/- 0.02938 |
| 8 | 0.36584 +/- 0.00463 | 0.43116 +/- 0.01285 |
| 10 | 0.34747 +/- 0.00588 | 0.42242 +/- 0.01526 |

The L=8 and L=10 curvature estimates overlap within their SEMs, but four
sizes do not establish a thermodynamic limit. The change in mean curvature
between delta=0.1 and 0.025 decreases from 0.00217 (L=4) to 0.00019 (L=10),
supporting finite-difference stability over the tested steps. These results
are for one representative disordered parameter point and one phase start;
the separate four-start comparison still covers only four disorder samples
at L=4,6,8. Raw rows, summaries, metadata, and regenerated dashboard data are
in `results/data/convergence_hartree_extended_20261023/` and
`frontend/convergence_data.js`.

### Increased disorder statistics: 20 samples

Run ID: `convergence_hartree_20sample_20261023`. It reuses the complete
12-sample four-size scan and adds eight samples per size at each of the three
twist steps, producing 240/240 successful calculations with zero failures.
The maximum mean-density residual remains 1.41e-6 (tolerance 1e-4).

At delta=0.025, the 20-sample results are:

| L | Mean pairing / t | Mean twist curvature / t |
|---:|---:|---:|
| 4 | 0.34129 +/- 0.02312 | 0.16508 +/- 0.04528 |
| 6 | 0.36984 +/- 0.00711 | 0.34384 +/- 0.01972 |
| 8 | 0.36106 +/- 0.00454 | 0.41536 +/- 0.01228 |
| 10 | 0.35068 +/- 0.00436 | 0.43286 +/- 0.01162 |

The L=8 and L=10 curvature SEM intervals overlap. The change between delta=0.1
and 0.025 decreases from 0.00218 at L=4 to 0.00018 at L=10. This supports
finite-difference stability for the tested steps; it does not establish size
convergence. This remains one disordered point and one phase start. Data,
summaries, metadata, and frontend payload are in
`results/data/convergence_hartree_20sample_20261023/` and
`frontend/convergence_data.js`.

## Phase-start sensitivity and L=10 extension

A second validation run compares one and four deterministic phase starts on
the same four disorder realizations at L=4,6,8 and adds L=10 using the same
four-sample one-start protocol. It uses the same disorder seed formula and
delta=0.05 as the first convergence run, so the one-start L=4,6,8 results
match its first four samples. The paired phase-start differences and larger
size result are reported by the dashboard and stored in
`results/data/phase_size_validation_20261023/`. All 28/28 calculations
converged, with maximum mean-density residual 4.9e-7.

Across the four matched disorder realizations, adding three more phase starts
changed the mean curvature by less than 1e-7 at each tested size:

| L | Four-start minus one-start curvature / t (mean +/- SEM) |
|---:|---:|
| 4 | +1.6e-8 +/- 1.2e-8 |
| 6 | -7.0e-8 +/- 7.4e-9 |
| 8 | -9.8e-8 +/- 5.6e-8 |

At L=10, the four-sample one-start result was mean pairing 0.34972 +/- 0.01474
and twist curvature 0.42749 +/- 0.03379. L=8 and L=10 are consistent within
these errors, but four L=10 samples cannot establish size convergence. The
four-start check found no meaningful curvature shift for these initial states
and samples; it does not guarantee a global phase-field minimum.

## Reproduction

```powershell
conda activate quantum_sc
python -m pytest -q
python scripts\run_fixed_density_research.py --run-id research_hartree_20261023 --sizes 4 6 --realizations 10 --phase-seeds 1 --twist-step 0.05
python scripts\run_fixed_density_research.py --run-id research_hartree_robust_20261023 --sizes 4 6 --realizations 20 --phase-seeds 2 --twist-step 0.05
python scripts\analyze_phase_start_sensitivity.py
python scripts\run_convergence_study.py --realizations 12
python scripts\run_convergence_study.py --run-id convergence_hartree_extended_20261023 --sizes 4 6 8 10 --resume-from convergence_hartree_20261023
python scripts\run_convergence_study.py --run-id convergence_hartree_20sample_20261023 --sizes 4 6 8 10 --realizations 20 --resume-from convergence_hartree_extended_20261023
python scripts\run_phase_size_validation.py
```

The solver, realization data, summary data, failure records, figures, and run
metadata are in `src/solver.py`, `src/observables.py`,
`results/data/research_hartree_20261023/`, and
`results/figures/research_hartree_20261023/`. View the extension dashboard at
`http://localhost:8765/frontend/research.html` after serving the repository
root.

## Limits and next validation

This is a model-level numerical study, not a calculation for a specific
material. The selected-point convergence run now uses twenty samples at
L=4,6,8,10, but only one disordered parameter point and one phase start. The
expanded parameter grid uses twenty samples and two starts at L=4,6. The
four-start phase comparison still has four samples at L=4,6,8; the paired
one-start/two-start grid comparison covers ten shared samples per point.
Together these checks improve numerical robustness but do not establish a
thermodynamic quantity or a global mean-field minimum. Further work should
study larger sizes, additional parameter points at larger sizes, more
independent disorder realizations, and broader phase searches. A
material-specific calculation additionally requires a target material, a
mapping from its measured or computed band structure and interaction/disorder
parameters to this model, and validation against material-specific
observables. No experimental transition temperature is predicted by the
present model.
Compare the stiffness convention and parameter-matched observables against
published many-body calculations. Prior work already studies disorder-driven
superconductor-insulator behavior and stiffness in the attractive Hubbard
model ([Scalettar, Trivedi, and Huscroft, 1999](https://doi.org/10.1103/PhysRevB.59.4364));
BdG work also shows that phase relaxation changes the stiffness in strongly
disordered systems ([Seibold et al., 2012](https://doi.org/10.1103/PhysRevLett.108.207004)).
The present scan does not claim a novel phase transition.
