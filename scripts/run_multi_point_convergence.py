"""Run matched fixed-density Hartree size checks at several (W, t') points."""
from __future__ import annotations

import argparse
import csv
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.disorder import onsite_disorder
from src.observables import phase_stiffness_fixed_density_hartree


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--run-id", default="convergence_hartree_multipoint_20261026")
parser.add_argument("--points", type=float, nargs="+", default=[0.6, 0.0, 1.2, 0.2],
                    help="W, t' pairs; provide an even number of values")
parser.add_argument("--sizes", type=int, nargs="+", default=[4, 6, 8, 10])
parser.add_argument("--realizations", type=int, default=8)
parser.add_argument("--twist-steps", type=float, nargs="+", default=[0.05, 0.025])
parser.add_argument("--phase-seeds", type=int, default=1)
parser.add_argument("--max-iterations", type=int, default=3000)
args = parser.parse_args()
if (len(args.points) < 2 or len(args.points) % 2 or args.realizations < 2
        or args.phase_seeds < 1 or args.max_iterations < 1
        or len(set(args.sizes)) != len(args.sizes) or any(size < 2 for size in args.sizes)
        or any(step <= 0 for step in args.twist_steps)
        or len(set(args.twist_steps)) != len(args.twist_steps)):
    raise SystemExit("Require W,t' pairs, unique L>=2, realizations>=2, phase-seeds>=1, and unique positive twist steps")

points = sorted(set(zip(args.points[::2], args.points[1::2])))
sizes = sorted(args.sizes)
steps = sorted(args.twist_steps, reverse=True)
run_id = args.run_id
data_dir = ROOT / "results" / "data" / run_id
data_dir.mkdir(parents=True, exist_ok=True)
raw_path = data_dir / "multipoint_realizations.csv"
meta_path = data_dir / "run_metadata.json"
seed_base = 10261026
parameters = dict(
    points=[{"W_uniform": w, "t_prime": tp} for w, tp in points],
    L_values=sizes, realizations=args.realizations, twist_steps=steps,
    phase_seeds=args.phase_seeds, t=1.0, U=2.2, T=0.08,
    target_density=0.87, seed_formula="seed_base + 1000*L + realization_index",
    seed_base=seed_base, pairing_tolerance=2e-5, density_tolerance=1e-4,
    mixing=0.1, max_iterations=args.max_iterations,
    Hartree_convention="K_eff = K0 - mu*I - diag(U*n_i/2)")
if meta_path.exists():
    previous = json.loads(meta_path.read_text(encoding="utf-8"))
    if previous.get("parameters") != parameters:
        raise SystemExit(f"Run {run_id} has different parameters; choose a new --run-id")

raw = read_csv(raw_path)
raw = [row for row in raw if int(row["L"]) in sizes
       and int(row["realization"]) < args.realizations]
done = {(int(row["L"]), int(row["realization"]), float(row["W_uniform"]),
         float(row["t_prime"]), float(row["twist_step"])) for row in raw}
planned = len(sizes) * args.realizations * len(points) * len(steps)
failures = []
completed = len(done)
for L in sizes:
    for realization in range(args.realizations):
        seed = seed_base + 1000 * L + realization
        for W, tp in points:
            potential = onsite_disorder(L*L, W, "uniform", seed)
            for step in steps:
                key = (L, realization, W, tp, float(step))
                if key in done:
                    continue
                try:
                    result = phase_stiffness_fixed_density_hartree(
                        L, 2.2, 0.08, 0.87, t=1.0, t_prime=tp,
                        potential=potential, delta=step, phase_seeds=args.phase_seeds,
                        tolerance=2e-5, density_tolerance=1e-4, mixing=0.1,
                        max_iterations=args.max_iterations)
                    center = result["twists"]["0.0"]
                    raw.append(dict(L=L, sites=L*L, realization=realization,
                        seed=seed, W_uniform=W, t_prime=tp, twist_step=step,
                        mean_pairing=center["mean_gap"],
                        twist_curvature=result["twist_curvature"],
                        mean_density=center["mean_density"],
                        density_residual=center["density_residual"],
                        paired_state=result["paired_state"],
                        phase_seeds=args.phase_seeds, converged=True))
                    done.add(key)
                except (RuntimeError, ValueError, np.linalg.LinAlgError) as exc:
                    failures.append(dict(L=L, realization=realization, seed=seed,
                        W_uniform=W, t_prime=tp, twist_step=step, error=str(exc)))
                completed += 1
                write_csv(raw_path, raw)
                print(f"L={L} W={W:g} t'={tp:g} sample={realization+1}/{args.realizations} "
                      f"delta={step:g} progress={completed}/{planned} success={len(raw)}", flush=True)

statistics = []
for W, tp in points:
    for L in sizes:
        for step in steps:
            group = [row for row in raw if int(row["L"]) == L
                     and float(row["W_uniform"]) == W and float(row["t_prime"]) == tp
                     and float(row["twist_step"]) == step]
            summary = dict(L=L, W_uniform=W, t_prime=tp, twist_step=step,
                           samples=len(group))
            for key, output in (("mean_pairing", "mean_pairing"),
                                ("twist_curvature", "mean_twist_curvature")):
                values = np.asarray([float(row[key]) for row in group])
                summary[output] = float(values.mean()) if len(values) else None
                summary["sem_" + output.removeprefix("mean_")] = (
                    float(values.std(ddof=1)/np.sqrt(len(values))) if len(values) > 1 else 0.0)
            summary["max_density_residual"] = max(
                (float(row["density_residual"]) for row in group), default=None)
            statistics.append(summary)

write_csv(data_dir / "multipoint_statistics.csv", statistics)
(data_dir / "failed_calculations.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")
figure_dir = ROOT / "results" / "figures" / run_id
figure_dir.mkdir(parents=True, exist_ok=True)
plot_steps = [float(row["twist_step"]) for row in statistics]
plot_step = min(plot_steps)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
for W, tp in points:
    label = f"W/t={W:g}, t'/t={tp:g}"
    group = [row for row in statistics if float(row["W_uniform"]) == W
             and float(row["t_prime"]) == tp
             and float(row["twist_step"]) == plot_step]
    axes[0].errorbar([row["L"] for row in group],
        [row["mean_twist_curvature"] for row in group],
        yerr=[row["sem_twist_curvature"] for row in group], marker="o", capsize=3, label=label)
    axes[1].errorbar([row["L"] for row in group],
        [row["mean_pairing"] for row in group],
        yerr=[row["sem_pairing"] for row in group], marker="o", capsize=3, label=label)
axes[0].set(xlabel="Linear size L", ylabel="Twist curvature / t",
            title=f"Fixed-density response (delta={plot_step:g})")
axes[1].set(xlabel="Linear size L", ylabel="Mean pairing / t",
            title=f"Pairing amplitude (delta={plot_step:g})")
for axis in axes:
    axis.grid(alpha=.25)
    axis.legend(frameon=False, fontsize=8)
fig.suptitle(f"Matched multi-point size checks; {args.realizations} disorder samples per point")
fig.tight_layout()
fig.savefig(figure_dir / "multipoint_size_trends.png", dpi=180)
fig.savefig(figure_dir / "multipoint_size_trends.pdf")
plt.close(fig)
metadata = dict(run_id=run_id, python=sys.version, platform=platform.platform(),
    numpy=np.__version__, scipy=scipy.__version__, parameters=parameters,
    planned_calculations=planned, successful_calculations=len(raw),
    failed_calculations=len(failures), complete=len(raw) == planned and not failures,
    max_density_residual=max((float(row["density_residual"]) for row in raw), default=None),
    caveats=["Two additional disorder/hopping points are not a full phase diagram.",
             f"{args.realizations} disorder realizations are a pilot-scale matched size check.",
             "One phase start does not establish a global free-energy minimum.",
             "Twist curvature is a finite-size mean-field response, not a BKT temperature."])
meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
print(json.dumps(metadata, indent=2))
print("Data:", data_dir)
