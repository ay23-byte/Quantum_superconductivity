"""Run a fixed-density Hartree+BdG disorder and phase-response pilot scan."""
from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.disorder import onsite_disorder
from src.lattice import square_lattice_hamiltonian
from src.observables import phase_stiffness_fixed_density_hartree

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--run-id", default="hartree_fixed_density_20261023")
parser.add_argument("--sizes", type=int, nargs="+", default=[4, 6])
parser.add_argument("--realizations", type=int, default=2)
parser.add_argument("--phase-seeds", type=int, default=4)
parser.add_argument("--twist-step", type=float, default=0.05)
args = parser.parse_args()
if args.realizations < 2 or args.phase_seeds < 1 or any(L < 2 for L in args.sizes):
    raise SystemExit("Require at least two realizations, phase-seeds>=1, and L>=2")

run_id = args.run_id
data_dir = ROOT / "results" / "data" / run_id
figure_dir = ROOT / "results" / "figures" / run_id
data_dir.mkdir(parents=True, exist_ok=True)
figure_dir.mkdir(parents=True, exist_ok=True)

t, U, T, density_target = 1.0, 2.2, 0.08, 0.87
W_values, tprime_values = [0.0, 0.6, 1.2], [0.0, 0.2]
seed_base = 56321
rows: list[dict] = []
failures: list[dict] = []

for L in args.sizes:
    for tprime in tprime_values:
        for W in W_values:
            for realization in range(args.realizations):
                seed = seed_base + int(round(100*W)) + realization
                potential = onsite_disorder(L*L, W, "uniform", seed)
                try:
                    result = phase_stiffness_fixed_density_hartree(
                        L, U, T, density_target, t=t, t_prime=tprime,
                        potential=potential, delta=args.twist_step,
                        phase_seeds=args.phase_seeds, tolerance=2e-5,
                        density_tolerance=1e-4, mixing=0.1,
                        max_iterations=3000)
                    center = result["twists"]["0.0"]
                    rows.append(dict(
                        L=L, sites=L*L, hopping_t=t, t_prime=tprime, W_uniform=W,
                        target_density=density_target, U=U, temperature_T=T,
                        realization=realization, seed=seed,
                        chemical_potential=center["mu"],
                        mean_density=center["mean_density"],
                        density_residual=center["density_residual"],
                        mean_pairing=center["mean_gap"],
                        paired_state=result["paired_state"],
                        twist_curvature=result["twist_curvature"],
                        rho_s_candidate=result["rho_s"],
                        twist_step=result["delta"],
                        selected_phase_seed=center["phase_seed"],
                        phase_seeds=args.phase_seeds,
                        converged=True))
                except (RuntimeError, ValueError, np.linalg.LinAlgError) as exc:
                    failures.append(dict(L=L, t_prime=tprime, W_uniform=W,
                        realization=realization, seed=seed, error=str(exc)))
                print(f"L={L} t'={tprime:g} W={W:g} sample={realization+1}/"
                      f"{args.realizations} complete={len(rows)} failed={len(failures)}",
                      flush=True)

raw = pd.DataFrame(rows)
raw.to_csv(data_dir / "hartree_fixed_density_realizations.csv", index=False)
if rows:
    summary = raw.groupby(["L", "t_prime", "W_uniform"]).agg(
        mean_pairing=("mean_pairing", "mean"),
        sample_sd_pairing=("mean_pairing", "std"),
        mean_twist_curvature=("twist_curvature", "mean"),
        sample_sd_twist_curvature=("twist_curvature", "std"),
        mean_density=("mean_density", "mean"),
        max_density_residual=("density_residual", "max"),
        paired_samples=("paired_state", "sum"), converged_samples=("converged", "sum"),
        samples=("realization", "count")).reset_index()
    summary["sem_pairing"] = summary.sample_sd_pairing.fillna(0)/np.sqrt(summary.samples)
    summary["sem_twist_curvature"] = summary.sample_sd_twist_curvature.fillna(0)/np.sqrt(summary.samples)
else:
    summary = pd.DataFrame()
summary.to_csv(data_dir / "hartree_fixed_density_statistics.csv", index=False)
(data_dir / "failed_calculations.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")

for L in args.sizes:
    subsize = summary[summary.L == L] if len(summary) else summary
    for tprime in tprime_values:
        sub = subsize[subsize.t_prime == tprime] if len(subsize) else subsize
        if sub.empty:
            continue
        plt.figure(figsize=(6, 4))
        plt.errorbar(sub.W_uniform, sub.mean_pairing, yerr=sub.sem_pairing,
                     fmt="o-", capsize=3)
        plt.xlabel("Uniform disorder width W/t")
        plt.ylabel("Mean local pairing amplitude / t")
        plt.title(fr"Fixed density n={density_target:g}, Hartree BdG, L={L}, t'/t={tprime:g}")
        plt.tight_layout()
        plt.savefig(figure_dir / f"pairing_L{L}_tp{tprime:g}.png", dpi=180)
        plt.savefig(figure_dir / f"pairing_L{L}_tp{tprime:g}.pdf")
        plt.close()

        plt.figure(figsize=(6, 4))
        plt.errorbar(sub.W_uniform, sub.mean_twist_curvature,
                     yerr=sub.sem_twist_curvature, fmt="s-", capsize=3)
        plt.axhline(0, color="black", lw=0.7)
        plt.xlabel("Uniform disorder width W/t")
        plt.ylabel(r"Finite-twist curvature $d^2F/d\theta^2$ / t")
        plt.title(fr"Relaxed twist response, L={L}, t'/t={tprime:g}")
        plt.tight_layout()
        plt.savefig(figure_dir / f"twist_curvature_L{L}_tp{tprime:g}.png", dpi=180)
        plt.savefig(figure_dir / f"twist_curvature_L{L}_tp{tprime:g}.pdf")
        plt.close()

metadata = dict(
    run_id=run_id, python=sys.version, platform=platform.platform(),
    numpy=np.__version__, scipy=scipy.__version__, pandas=pd.__version__,
    parameters=dict(L_values=args.sizes, realizations=args.realizations,
        phase_seeds=args.phase_seeds, twist_step=args.twist_step,
        t=t, U=U, T=T, target_density=density_target,
        W_uniform_values=W_values, tprime_values=tprime_values,
        disorder_distribution="uniform[-W/2,W/2]", seed_base=seed_base,
        pairing_tolerance=2e-5, density_tolerance=1e-4,
        Hartree_convention="K_eff = K0 - mu*I - diag(U*n_i/2)"),
    successful_calculations=len(rows), failed_calculations=len(failures),
    all_successful_densities_within_tolerance=bool(
        rows and max(r["density_residual"] for r in rows) <= 1e-4),
    caveats=[
        "Small pilot sample counts; do not interpret as converged disorder averages.",
        "Finite-difference twist curvature is a mean-field response, not a BKT temperature.",
        "Phase search compares a finite set of deterministic initial states, not a proof of the global free-energy minimum.",
        "Check twist-step and lattice-size convergence before interpreting negative or large curvature.",
    ])
(data_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
(ROOT / "frontend" / "research_data.js").write_text(
    "window.HARTREE_RESEARCH = " + json.dumps({
        "scan": summary.to_dict(orient="records") if len(summary) else [],
        "metadata": metadata}, indent=2) + ";\n", encoding="utf-8")
print(json.dumps(metadata, indent=2))
print("Data:", data_dir)
print("Figures:", figure_dir)
