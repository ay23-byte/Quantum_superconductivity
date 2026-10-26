# Quantum lattice superconductivity (exploratory BdG project)

This project contains a small, reproducible implementation of the pairing-only
mean-field attractive Hubbard model on a periodic square lattice. The clean
finite-grid solver is independently checked against a momentum-space gap
equation. Disorder results are exploratory finite-size calculations, not a
novelty claim or an experimental transition temperature.

## Setup

Recommended environment (Python 3.11):

```powershell
conda create -n quantum_sc python=3.11 -y
conda activate quantum_sc
python -m pip install -r requirements.txt
```

Validation and the extended run were completed in the `quantum_sc` Python
3.11.17 environment. See [docs/validation.md](docs/validation.md) for the
recorded checks and results.

## Quick start

From the repository root:

```powershell
python -m pytest -q
python scripts\run_quick_research.py
jupyter notebook
```

The default quick scan is CPU-only and uses L=6 with three realizations per
point. The completed extended scan uses 20 realizations per L=6
disorder/hopping point and a 10-realization disorder finite-size check at
L=4,6,8. To reproduce it:

```powershell
python scripts\run_quick_research.py --run-id research_20261023 --realizations 20 --size-check-realizations 10
```

The research extension adds local Hartree feedback, adjusts chemical
potential to hold mean density fixed, and estimates the response to a boundary
phase twist. Its completed pilot used 10 realizations per point at L=4,6:

```powershell
python scripts\run_fixed_density_research.py --run-id research_hartree_20261023 --sizes 4 6 --realizations 10 --phase-seeds 1 --twist-step 0.05
```

The robustness extension repeats the six-point disorder/hopping grid with 20
realizations per point and two deterministic phase starts per twist:

```powershell
python scripts\run_fixed_density_research.py --run-id research_hartree_robust_20261023 --sizes 4 6 --realizations 20 --phase-seeds 2 --twist-step 0.05
python scripts\analyze_phase_start_sensitivity.py
```

It writes the expanded CSV summaries, realization data, metadata, and figures
to `results/data/research_hartree_robust_20261023/` and
`results/figures/research_hartree_robust_20261023/`. The dashboard reads this
run's generated summary. `phase_start_sensitivity_paired.csv` compares its
first ten disorder samples with the matched one-start pilot.

The twist curvature is a finite-size mean-field response, not a transition
temperature. Read [docs/research_extension.md](docs/research_extension.md)
before interpreting it.

An additional convergence workflow checks lattice size, cumulative disorder
sample count, and finite-difference twist step at W/t=1.2 and t'/t=0. The
default run uses L=4,6,8, twelve disorder samples, and three twist steps:

```powershell
python scripts\run_convergence_study.py
```

It writes raw results, convergence summaries, metadata, and dashboard data to
`results/data/convergence_hartree_20261023/` and
`frontend/convergence_data.js`. The research dashboard displays these checks
alongside the original Hartree scan. This is a selected-point robustness check,
not a full phase diagram or thermodynamic extrapolation.

The extended size check carries those same 12 disorder samples and all three
twist steps through L=10. It resumes the completed L=4,6,8 rows and computes
only the 36 new L=10 cases:

```powershell
python scripts\run_convergence_study.py --run-id convergence_hartree_extended_20261023 --sizes 4 6 8 10 --resume-from convergence_hartree_20261023
```

Its complete dataset is saved in
`results/data/convergence_hartree_extended_20261023/` and replaces the
dashboard's convergence data with the combined four-size result. This remains
a finite-size exploratory model calculation, not a material-specific prediction.

To increase this selected-point convergence scan to 20 samples per size while
reusing its 12-sample L=4,6,8,10 data, run:

```powershell
python scripts\run_convergence_study.py --run-id convergence_hartree_20sample_20261023 --sizes 4 6 8 10 --realizations 20 --resume-from convergence_hartree_extended_20261023
```

The follow-up validation compares one and four phase starts on four matched
disorder samples at L=4,6,8 and adds an L=10 size point:

```powershell
python scripts\run_phase_size_validation.py
```

Its realization data and summaries are saved in
`results/data/phase_size_validation_20261023/` and shown on the same research
dashboard.

The multi-point convergence follow-up checks two additional settings across
L=4,6,8,10 using matched disorder seeds, two twist steps, and four samples
per point:

```powershell
python scripts\run_multi_point_convergence.py
```

The QMC trend benchmark uses the same L, interaction, temperature, filling,
and disorder distribution as a published disordered attractive-Hubbard study;
it compares disorder trends while keeping the different stiffness estimators
explicit:

```powershell
python scripts\run_qmc_benchmark.py
```

See [docs/qmc_benchmark.md](docs/qmc_benchmark.md) for the comparison limits.

The virtual STM/STS experiment follows a seeded disordered sample through
self-consistent preparation, site-resolved LDOS, finite-temperature tunneling
convolution, and Gaussian lock-in broadening:

```powershell
python scripts\run_virtual_sts.py
```

It writes site maps, full site-resolved spectra, a site-averaged spectrum,
figures, and a step-by-step run record under
`results/data/virtual_sts_20261026/` and
`results/figures/virtual_sts_20261026/`. Adjust the sample with options such as
`--size 8 --disorder 1.0 --seed 23`. The measurement model is a generic local
tunneling approximation; it does not include tip feedback, matrix elements,
spatial tip resolution, noise, or a material-specific calibration.
Read the [virtual STM/STS protocol](docs/virtual_sts.md) for the measurement
equation and interpretation limits.

Dense diagonalization becomes expensive rapidly as L grows. See
[docs/methods.md](docs/methods.md) before expanding the scan.

## Visual frontend

To view the dashboard with the completed extended scan, serve the repository
root and open `http://localhost:8000/frontend/`:

```powershell
python -m http.server 8000
```

The dependency-free HTML/CSS/JavaScript dashboard lets you switch between the
saved quick, extended, and user simulation scans, compare hopping values, and
filter the disorder range. It reads bundled summaries and links to each run's
PNG/PDF figures. Running `run_quick_research.py` refreshes that bundle; the
static deployment builder also rebuilds it. The server runs in the foreground;
press Ctrl+C to stop it.

The Hartree extension view is at `http://localhost:8000/frontend/research.html`.

## Project layout

- `src/`: lattice, disorder, gap-equation, BdG, solver, and validation modules.
- `notebooks/`: four independent teaching/research notebooks importing `src`.
- `scripts/run_quick_research.py`: deterministic CSV, metadata, and figure run.
- `scripts/run_fixed_density_research.py`: fixed-density Hartree and twist-response pilot.
- `scripts/run_convergence_study.py`: size, sample-count, and twist-step convergence scan.
- `scripts/run_multi_point_convergence.py`: matched size checks at extra disorder/hopping points.
- `scripts/run_qmc_benchmark.py`: parameter-matched trend check against published DQMC.
- `scripts/run_virtual_sts.py`: reproducible synthetic STM/STS sample and measurement workflow.
- `scripts/run_phase_size_validation.py`: matched phase-start sensitivity and L=10 extension.
- `scripts/analyze_phase_start_sensitivity.py`: paired one-start/two-start summary for shared disorder seeds.
- `results/data/research_20261023/`: extended realization data, summaries,
  metadata, and clean-limit crosschecks.
- `results/figures/research_20261023/`: extended PNG and PDF figures.
- `results/data/research_hartree_20261023/`: fixed-density Hartree realization and summary data.
- `results/data/research_hartree_robust_20261023/`: 20-sample, two-start
  realization data and summaries across the six-point L=4,6 parameter grid.
- `results/figures/research_hartree_20261023/`: pairing and twist-response figures.
- `results/data/convergence_hartree_20261023/`: convergence realizations, summaries, and metadata.
- `results/data/convergence_hartree_extended_20261023/`: resumed L=4,6,8,10 twelve-sample scan at three twist steps.
- `results/data/convergence_hartree_20sample_20261023/`: 20-sample L=4,6,8,10 convergence scan at three twist steps.
- `results/data/convergence_hartree_multipoint_20261026/`: matched multi-point L=4,6,8,10 follow-up.
- `results/data/qmc_benchmark_scalettar_20261026/`: run data for the published QMC trend check.
- `docs/`: derivation, methods, validation, literature assessment, report draft.

The earlier quick-run files were preserved. The original scan fixes chemical
potential and omits the Hartree channel; the separate extension holds density
fixed and includes Hartree feedback. Both remain limited by small lattices.
The twist response is not a phase-coherence/BKT transition temperature, and
publication novelty is not established.
Read [docs/theory.md](docs/theory.md), [docs/validation.md](docs/validation.md),
and [docs/literature_review.md](docs/literature_review.md) for the full scope.
