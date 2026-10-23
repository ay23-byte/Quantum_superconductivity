"""Run size, disorder-sample, and twist-step convergence checks for Hartree BdG."""
from __future__ import annotations

import argparse
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


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--run-id", default="convergence_hartree_20261023")
parser.add_argument("--resume-from", default=None,
                    help="reuse compatible completed rows from a run with no more sizes or disorder samples")
parser.add_argument("--sizes", type=int, nargs="+", default=[4, 6, 8])
parser.add_argument("--realizations", type=int, default=12,
                    help="maximum nested disorder sample count per lattice size")
parser.add_argument("--twist-steps", type=float, nargs="+",
                    default=[0.1, 0.05, 0.025])
parser.add_argument("--phase-seeds", type=int, default=1)
parser.add_argument("--max-iterations", type=int, default=3000)
args = parser.parse_args()
if (args.realizations < 2 or args.phase_seeds < 1 or args.max_iterations < 1
        or len(set(args.sizes)) != len(args.sizes)
        or any(L < 2 for L in args.sizes)
        or any(step <= 0 for step in args.twist_steps)
        or len(set(args.twist_steps)) != len(args.twist_steps)):
    raise SystemExit("Require unique L>=2, realizations>=2, phase-seeds>=1, "
                     "max-iterations>=1, and unique positive twist steps")

sizes = sorted(args.sizes)
steps = sorted(args.twist_steps, reverse=True)
run_id = args.run_id
data_dir = ROOT / "results" / "data" / run_id
data_dir.mkdir(parents=True, exist_ok=True)
raw_path = data_dir / "convergence_realizations.csv"
metadata_path = data_dir / "run_metadata.json"
seed_base = 826103
parameters = dict(
    L_values=sizes, max_disorder_realizations=args.realizations,
    twist_steps=steps, phase_seeds=args.phase_seeds,
    t=1.0, U=2.2, T=0.08, target_density=0.87,
    t_prime=0.0, W_uniform=1.2,
    disorder_distribution="uniform[-W/2,W/2]",
    seed_formula="seed_base + 1000*L + realization_index",
    seed_base=seed_base, pairing_tolerance=2e-5,
    density_tolerance=1e-4, mixing=0.1,
    Hartree_convention="K_eff = K0 - mu*I - diag(U*n_i/2)")

if metadata_path.exists():
    previous = json.loads(metadata_path.read_text(encoding="utf-8"))
    if previous.get("parameters") != parameters:
        raise SystemExit(f"Run {run_id} already has different parameters; choose a new --run-id")

raw: list[dict] = []
if args.resume_from:
    source_dir = ROOT / "results" / "data" / args.resume_from
    source_meta_path = source_dir / "run_metadata.json"
    source_raw_path = source_dir / "convergence_realizations.csv"
    if not source_meta_path.exists() or not source_raw_path.exists():
        raise SystemExit(f"Cannot resume: run {args.resume_from} is missing metadata or realization data")
    source_meta = json.loads(source_meta_path.read_text(encoding="utf-8"))
    source_params = source_meta.get("parameters", {})
    compatible = all(source_params.get(k) == v for k, v in parameters.items()
                     if k not in {"L_values", "max_disorder_realizations"})
    source_sizes = set(source_params.get("L_values", []))
    source_realizations = source_params.get("max_disorder_realizations", 0)
    target_realizations = parameters["max_disorder_realizations"]
    if not compatible or not source_sizes.issubset(set(sizes)):
        raise SystemExit("Resume source parameters are incompatible with this run")
    if not isinstance(source_realizations, int) or source_realizations > target_realizations:
        raise SystemExit("Resume source has more disorder samples than the target run")
    if not source_meta.get("complete", False):
        raise SystemExit("Resume source run is incomplete; resume that run first")
    with source_raw_path.open(newline="", encoding="utf-8") as handle:
        raw.extend(csv.DictReader(handle))
if raw_path.exists():
    with raw_path.open(newline="", encoding="utf-8") as handle:
        existing = list(csv.DictReader(handle))
    existing_keys = {(int(r["L"]), int(r["realization"]), float(r["twist_step"]))
                     for r in raw}
    raw.extend(r for r in existing
               if (int(r["L"]), int(r["realization"]), float(r["twist_step"]))
               not in existing_keys)
if raw:
    write_csv(raw_path, raw)
done = {(int(row["L"]), int(row["realization"]), float(row["twist_step"]))
        for row in raw}
failures: list[dict] = []
total = len(sizes) * args.realizations * len(steps)
completed = len(done)

for L in sizes:
    for realization in range(args.realizations):
        seed = seed_base + 1000*L + realization
        potential = onsite_disorder(L*L, 1.2, "uniform", seed)
        for step in steps:
            key = (L, realization, float(step))
            if key in done:
                continue
            try:
                result = phase_stiffness_fixed_density_hartree(
                    L, 2.2, 0.08, 0.87, t=1.0, t_prime=0.0,
                    potential=potential, delta=step,
                    phase_seeds=args.phase_seeds, tolerance=2e-5,
                    density_tolerance=1e-4, mixing=0.1,
                    max_iterations=args.max_iterations)
                center = result["twists"]["0.0"]
                raw.append(dict(
                    L=L, sites=L*L, realization=realization, seed=seed,
                    W_uniform=1.2, t_prime=0.0, twist_step=step,
                    mean_pairing=center["mean_gap"],
                    twist_curvature=result["twist_curvature"],
                    mean_density=center["mean_density"],
                    density_residual=center["density_residual"],
                    paired_state=result["paired_state"],
                    phase_seeds=args.phase_seeds,
                    max_iterations=args.max_iterations, converged=True))
                done.add(key)
            except (RuntimeError, ValueError, np.linalg.LinAlgError) as exc:
                failures.append(dict(L=L, realization=realization, seed=seed,
                                     twist_step=step, error=str(exc)))
            completed += 1
            write_csv(raw_path, raw)
            print(f"L={L} sample={realization+1}/{args.realizations} "
                  f"delta={step:g} progress={completed}/{total} "
                  f"success={len(raw)}", flush=True)

stats: list[dict] = []
for L in sizes:
    for step in steps:
        group = [r for r in raw if int(r["L"]) == L
                 and float(r["twist_step"]) == step]
        for key in ("mean_pairing", "twist_curvature"):
            vals = np.asarray([float(r[key]) for r in group])
            mean = float(vals.mean()) if len(vals) else float("nan")
            sem = (float(vals.std(ddof=1)/np.sqrt(len(vals)))
                   if len(vals) > 1 else 0.0)
            if key == "mean_pairing":
                pairing_mean, pairing_sem = mean, sem
            else:
                stiffness_mean, stiffness_sem = mean, sem
        stats.append(dict(
            L=L, twist_step=step, W_uniform=1.2, t_prime=0.0,
            mean_pairing=pairing_mean, sem_pairing=pairing_sem,
            mean_twist_curvature=stiffness_mean,
            sem_twist_curvature=stiffness_sem,
            max_density_residual=max((float(r["density_residual"]) for r in group),
                                     default=float("nan")),
            samples=len(group)))

sample_counts: list[dict] = []
for L in sizes:
    for step in steps:
        group = sorted((r for r in raw if int(r["L"]) == L
                        and float(r["twist_step"]) == step),
                       key=lambda r: int(r["realization"]))
        for count in range(2, len(group)+1):
            values = np.asarray([float(r["twist_curvature"]) for r in group[:count]])
            sample_counts.append(dict(
                L=L, twist_step=step, samples=count,
                mean_twist_curvature=float(values.mean()),
                sem_twist_curvature=(float(values.std(ddof=1)/np.sqrt(count))
                                     if count > 1 else 0.0)))

twist_comparisons: list[dict] = []
for L in sizes:
    per_step = {
        step: {int(r["realization"]): float(r["twist_curvature"])
               for r in raw if int(r["L"]) == L
               and float(r["twist_step"]) == step}
        for step in steps}
    matched = (set.intersection(*(set(values) for values in per_step.values()))
               if per_step else set())
    for step in steps:
        values = np.asarray([per_step[step][idx] for idx in sorted(matched)])
        twist_comparisons.append(dict(
            L=L, twist_step=step,
            mean_twist_curvature=float(values.mean()) if len(values) else None,
            sem_twist_curvature=(float(values.std(ddof=1)/np.sqrt(len(values)))
                                 if len(values) > 1 else 0.0),
            samples=len(values)))

write_csv(data_dir / "convergence_statistics.csv", stats)
write_csv(data_dir / "convergence_sample_counts.csv", sample_counts)
(data_dir / "failed_calculations.json").write_text(
    json.dumps(failures, indent=2), encoding="utf-8")
metadata = dict(
    run_id=run_id, python=sys.version, platform=platform.platform(),
    numpy=np.__version__, scipy=scipy.__version__, parameters=parameters,
    planned_calculations=total, successful_calculations=len(raw),
    failed_calculations=len(failures),
    complete=len(raw) == total and not failures,
    max_density_residual=max((float(r["density_residual"]) for r in raw),
                             default=None),
    interpretation=dict(
        size_comparison="Compare the same maximum disorder sample count at the smallest twist step.",
        sample_comparison="Cumulative prefixes use deterministic seeded realizations; prefix estimates are correlated.",
        twist_comparison="Compare twist-step values on the same disorder realizations; this tests finite-difference sensitivity."),
    caveats=[
        "This convergence scan covers one representative disordered point (W/t=1.2, t'/t=0).",
        "Disorder counts are pilot-scale and do not establish asymptotic self-averaging.",
        "The phase search uses a finite number of deterministic starts and does not prove the global free-energy minimum.",
        "Twist curvature is a finite-size mean-field response, not a BKT temperature or experimental transition temperature."])
metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

payload = dict(
    statistics=stats, sample_counts=sample_counts,
    twist_comparisons=twist_comparisons, metadata=metadata)
(ROOT / "frontend" / "convergence_data.js").write_text(
    "window.HARTREE_CONVERGENCE = " + json.dumps(payload, indent=2) + ";\n",
    encoding="utf-8")
print(json.dumps(metadata, indent=2))
print("Data:", data_dir)
print("Dashboard data: frontend/convergence_data.js")
