"""Compare phase-start counts and extend the selected disorder size check."""
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


def average(values: list[float]) -> tuple[float | None, float]:
    x = np.asarray(values, dtype=float)
    if not len(x):
        return None, 0.0
    sem = float(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 1 else 0.0
    return float(x.mean()), sem


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--run-id", default="phase_size_validation_20261023")
parser.add_argument("--samples", type=int, default=4)
parser.add_argument("--phase-seeds", type=int, default=4)
parser.add_argument("--extended-size", type=int, default=10)
parser.add_argument("--max-iterations", type=int, default=3000)
args = parser.parse_args()
if args.samples < 2 or args.phase_seeds < 2 or args.extended_size < 9:
    raise SystemExit("Require samples>=2, phase-seeds>=2, and extended-size>=9")

comparison_sizes = [4, 6, 8]
all_sizes = comparison_sizes + [args.extended_size]
seed_counts = [1, args.phase_seeds]
step = 0.05
run_id = args.run_id
data_dir = ROOT / "results" / "data" / run_id
data_dir.mkdir(parents=True, exist_ok=True)
raw_path = data_dir / "phase_size_realizations.csv"
metadata_path = data_dir / "run_metadata.json"
seed_base = 826103
parameters = dict(
    L_values=all_sizes, comparison_sizes=comparison_sizes,
    extended_size_phase_seeds=1, realizations=args.samples,
    phase_seed_counts=seed_counts, twist_step=step,
    t=1.0, U=2.2, T=0.08, target_density=0.87,
    t_prime=0.0, W_uniform=1.2,
    disorder_distribution="uniform[-W/2,W/2]",
    seed_formula="seed_base + 1000*L + realization_index",
    seed_base=seed_base, pairing_tolerance=2e-5,
    density_tolerance=1e-4, mixing=0.1,
    Hartree_convention="K_eff = K0 - mu*I - diag(U*n_i/2)")
if metadata_path.exists():
    old = json.loads(metadata_path.read_text(encoding="utf-8"))
    if old.get("parameters") != parameters:
        raise SystemExit(f"Run {run_id} already has different parameters; choose another --run-id")

raw: list[dict] = []
if raw_path.exists():
    with raw_path.open(newline="", encoding="utf-8") as handle:
        raw = list(csv.DictReader(handle))
done = {(int(r["L"]), int(r["realization"]), int(r["phase_seeds"])) for r in raw}
plan = [(L, realization, count)
        for L in comparison_sizes for realization in range(args.samples)
        for count in seed_counts]
plan += [(args.extended_size, realization, 1)
         for realization in range(args.samples)]
completed = len(done)
failures: list[dict] = []

for L, realization, phase_seeds in plan:
    key = (L, realization, phase_seeds)
    if key in done:
        continue
    seed = seed_base + 1000*L + realization
    potential = onsite_disorder(L*L, 1.2, "uniform", seed)
    try:
        result = phase_stiffness_fixed_density_hartree(
            L, 2.2, 0.08, 0.87, t=1.0, t_prime=0.0,
            potential=potential, delta=step, phase_seeds=phase_seeds,
            tolerance=2e-5, density_tolerance=1e-4,
            mixing=0.1, max_iterations=args.max_iterations)
        center = result["twists"]["0.0"]
        raw.append(dict(
            L=L, sites=L*L, realization=realization, seed=seed,
            W_uniform=1.2, t_prime=0.0, twist_step=step,
            phase_seeds=phase_seeds,
            selected_seed_negative=result["twists"][str(-step)]["phase_seed"],
            selected_seed_center=center["phase_seed"],
            selected_seed_positive=result["twists"][str(step)]["phase_seed"],
            mean_pairing=center["mean_gap"],
            twist_curvature=result["twist_curvature"],
            mean_density=center["mean_density"],
            density_residual=center["density_residual"],
            paired_state=result["paired_state"], converged=True))
        done.add(key)
    except (RuntimeError, ValueError, np.linalg.LinAlgError) as exc:
        failures.append(dict(L=L, realization=realization, seed=seed,
                             phase_seeds=phase_seeds, error=str(exc)))
    completed += 1
    write_csv(raw_path, raw)
    print(f"L={L} sample={realization+1}/{args.samples} "
          f"phase-seeds={phase_seeds} progress={completed}/{len(plan)} "
          f"success={len(raw)}", flush=True)

summary: list[dict] = []
for L in all_sizes:
    counts = [1] if L == args.extended_size else seed_counts
    for phase_seeds in counts:
        group = [r for r in raw if int(r["L"]) == L
                 and int(r["phase_seeds"]) == phase_seeds]
        gap, gap_sem = average([float(r["mean_pairing"]) for r in group])
        stiffness, stiffness_sem = average([float(r["twist_curvature"]) for r in group])
        summary.append(dict(
            L=L, phase_seeds=phase_seeds, twist_step=step,
            mean_pairing=gap, sem_pairing=gap_sem,
            mean_twist_curvature=stiffness,
            sem_twist_curvature=stiffness_sem,
            max_density_residual=max((float(r["density_residual"]) for r in group),
                                     default=None),
            samples=len(group)))

phase_effects: list[dict] = []
for L in comparison_sizes:
    one = {int(r["realization"]): float(r["twist_curvature"])
           for r in raw if int(r["L"]) == L and int(r["phase_seeds"]) == 1}
    many = {int(r["realization"]): float(r["twist_curvature"])
            for r in raw if int(r["L"]) == L
            and int(r["phase_seeds"]) == args.phase_seeds}
    shared = sorted(set(one) & set(many))
    mean, sem = average([many[i]-one[i] for i in shared])
    phase_effects.append(dict(
        L=L, phase_seed_counts=seed_counts,
        mean_curvature_change=mean, sem_curvature_change=sem,
        samples=len(shared)))

write_csv(data_dir / "phase_size_summary.csv", summary)
write_csv(data_dir / "phase_start_sensitivity.csv", phase_effects)
(data_dir / "failed_calculations.json").write_text(
    json.dumps(failures, indent=2), encoding="utf-8")
metadata = dict(
    run_id=run_id, python=sys.version, platform=platform.platform(),
    numpy=np.__version__, scipy=scipy.__version__, parameters=parameters,
    planned_calculations=len(plan), successful_calculations=len(raw),
    failed_calculations=len(failures),
    complete=len(raw) == len(plan) and not failures,
    max_density_residual=max((float(r["density_residual"]) for r in raw),
                             default=None),
    caveats=[
        "Phase-start comparison is limited to four seeded disorder realizations and the selected point W/t=1.2, t'/t=0.",
        "The L=10 extension uses the one-start baseline and four realizations; it is an additional finite-size check, not an extrapolation.",
        "A finite set of starts does not prove the global mean-field free-energy minimum.",
        "Twist curvature is a finite-size mean-field response, not a BKT temperature or experimental transition temperature."])
metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
payload = dict(summary=summary, phase_effects=phase_effects, metadata=metadata)
(ROOT / "frontend" / "phase_size_data.js").write_text(
    "window.HARTREE_PHASE_SIZE = " + json.dumps(payload, indent=2) + ";\n",
    encoding="utf-8")
print(json.dumps(metadata, indent=2))
print("Data:", data_dir)
print("Dashboard data: frontend/phase_size_data.js")
