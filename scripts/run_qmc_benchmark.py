"""Compare fixed-density Hartree-BdG twist response with a published QMC trend."""
from __future__ import annotations

import csv
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.disorder import onsite_disorder
from src.observables import phase_stiffness_fixed_density_hartree

RUN_ID = "qmc_benchmark_scalettar_20261026"
DATA = ROOT / "results" / "data" / RUN_ID
DATA.mkdir(parents=True, exist_ok=True)
L, U, T, density, tp = 8, 4.0, 0.1, 0.875, 0.0
W_VALUES, REALIZATIONS, TWIST_STEP, PHASE_SEEDS = [1.0, 4.0], 8, 0.05, 1
SEED_BASE = 71026
RAW = DATA / "benchmark_realizations.csv"
SUMMARY = DATA / "benchmark_summary.csv"
RAW_FIELDS = ["L", "realization", "seed", "W_uniform", "t_prime", "U", "T",
    "target_density", "mean_pairing", "mean_density", "twist_curvature",
    "paired_state", "converged", "density_residual", "twist_step",
    "phase_seeds", "error"]
existing = {}
if RAW.exists():
    with RAW.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            row["converged"] = row["converged"].lower() == "true"
            existing[(float(row["W_uniform"]), int(row["realization"]))] = row

for W in W_VALUES:
    for realization in range(REALIZATIONS):
        key = (W, realization)
        if key in existing:
            continue
        seed = SEED_BASE + int(W * 100) + realization
        potential = onsite_disorder(L*L, W, "uniform", seed)
        try:
            result = phase_stiffness_fixed_density_hartree(
                L, U, T, density, t=1.0, t_prime=tp, potential=potential,
                delta=TWIST_STEP, phase_seeds=PHASE_SEEDS,
                tolerance=2e-5, density_tolerance=1e-4,
                mixing=0.1, max_iterations=3000)
            center = result["twists"]["0.0"]
            existing[key] = dict(
                L=L, realization=realization, seed=seed, W_uniform=W,
                t_prime=tp, U=U, T=T, target_density=density,
                mean_pairing=center["mean_gap"],
                mean_density=center["mean_density"],
                twist_curvature=result["twist_curvature"],
                paired_state=result["paired_state"], converged=True,
                density_residual=center["density_residual"],
                twist_step=TWIST_STEP, phase_seeds=PHASE_SEEDS)
        except (RuntimeError, ValueError, np.linalg.LinAlgError) as exc:
            existing[key] = dict(L=L, realization=realization, seed=seed,
                W_uniform=W, t_prime=tp, U=U, T=T, target_density=density,
                paired_state=False, converged=False, error=str(exc))
        ordered = [existing[k] for k in sorted(existing)]
        with RAW.open("w", newline="", encoding="utf-8") as destination:
            writer = csv.DictWriter(destination, fieldnames=RAW_FIELDS)
            writer.writeheader()
            writer.writerows(ordered)
        print(f"W={W:g} sample={realization+1}/{REALIZATIONS} completed "
              f"({len(existing)}/{len(W_VALUES)*REALIZATIONS})", flush=True)

rows = [existing[key] for key in sorted(existing)]
stats = []
for W in W_VALUES:
    group = [row for row in rows if float(row["W_uniform"]) == W and row.get("converged") is True]
    summary = {"W_uniform": W, "samples": len(group),
               "converged_samples": len(group)}
    for input_key, output_key in (("mean_pairing", "mean_pairing"),
                                  ("twist_curvature", "mean_twist_curvature")):
        values = np.asarray([float(row[input_key]) for row in group])
        summary[output_key] = float(values.mean()) if len(values) else None
        summary["sem_" + output_key.removeprefix("mean_")] = (
            float(values.std(ddof=1)/np.sqrt(len(values))) if len(values) > 1 else 0.0)
    summary["max_density_residual"] = max(
        (float(row["density_residual"]) for row in group), default=None)
    stats.append(summary)
with SUMMARY.open("w", newline="", encoding="utf-8") as destination:
    writer = csv.DictWriter(destination, fieldnames=list(stats[0]))
    writer.writeheader()
    writer.writerows(stats)

metadata = dict(run_id=RUN_ID, python=sys.version, platform=platform.platform(),
    numpy=np.__version__, scipy=np.__version__,
    parameters=dict(L=L, U=U, T=T, target_density=density, t=1.0,
        t_prime=tp, W_uniform_values=W_VALUES, realizations=REALIZATIONS,
        twist_step=TWIST_STEP, phase_seeds=PHASE_SEEDS, seed_base=SEED_BASE),
    successful_calculations=sum(row.get("converged") is True for row in rows),
    failed_calculations=sum(row.get("converged") is False for row in rows),
    max_density_residual=max((float(row["density_residual"]) for row in rows
                              if row.get("converged") is True), default=None),
    qmc_reference=dict(title="Quantum Monte Carlo Study of the Disordered Attractive Hubbard Model",
        authors="R. T. Scalettar, N. Trivedi, and C. Huscroft",
        arxiv="https://arxiv.org/abs/cond-mat/9807008",
        qmc_parameters="L=8, U/t=4, T/t=0.1, density approximately 0.875, t'=0; uniform site disorder",
        reported_trend="QMC stiffness falls strongly with disorder and is zero at W/t=4; the paper estimates a critical disorder near 3–4t."),
    comparison_limits=[
        "This run compares the disorder trend, not pointwise numerical values.",
        "The project estimates fixed-density mean-field free-energy curvature; QMC obtains stiffness from current-current correlations.",
        "QMC targets density after disorder averaging; this run enforces target density separately for each realization.",
        "Eight samples and one phase initialization are a small benchmark check, not a statistical reproduction of QMC."])
(DATA / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
print(json.dumps(metadata, indent=2))
print("Data:", DATA)
