"""Create a paired one-start versus two-start sensitivity summary."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--one-start-run", default="research_hartree_20261023")
parser.add_argument("--two-start-run", default="research_hartree_robust_20261023")
args = parser.parse_args()

one_path = ROOT / "results" / "data" / args.one_start_run / "hartree_fixed_density_realizations.csv"
two_path = ROOT / "results" / "data" / args.two_start_run / "hartree_fixed_density_realizations.csv"
if not one_path.exists() or not two_path.exists():
    raise SystemExit("Both input runs must contain hartree_fixed_density_realizations.csv")

one = pd.read_csv(one_path)
two = pd.read_csv(two_path)
keys = ["L", "t_prime", "W_uniform", "realization", "seed"]
paired = one.merge(two, on=keys, suffixes=("_one_start", "_two_start"), validate="one_to_one")
if paired.empty:
    raise SystemExit("The runs have no matched disorder realizations")

paired["pairing_change"] = paired["mean_pairing_two_start"] - paired["mean_pairing_one_start"]
paired["curvature_change"] = paired["twist_curvature_two_start"] - paired["twist_curvature_one_start"]
group_keys = ["L", "t_prime", "W_uniform"]
rows = []
for (L, t_prime, W), group in paired.groupby(group_keys, sort=True):
    n = len(group)
    rows.append(dict(
        L=int(L), t_prime=float(t_prime), W_uniform=float(W),
        paired_samples=n,
        mean_pairing_change=float(group.pairing_change.mean()),
        sem_pairing_change=float(group.pairing_change.std(ddof=1)/np.sqrt(n)) if n > 1 else 0.0,
        mean_curvature_change=float(group.curvature_change.mean()),
        sem_curvature_change=float(group.curvature_change.std(ddof=1)/np.sqrt(n)) if n > 1 else 0.0,
        two_start_selected_second=int((group.selected_phase_seed_two_start == 1).sum()),
    ))

out = ROOT / "results" / "data" / args.two_start_run / "phase_start_sensitivity_paired.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"Matched {len(paired)} disorder realizations across {len(rows)} parameter groups")
print(f"Wrote {out}")
