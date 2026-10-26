"""Bundle compatible saved scan runs for the static dashboard."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "results" / "data"
FIGURE_ROOT = ROOT / "results" / "figures"
OUTPUT = ROOT / "frontend" / "dashboard_runs.js"
RESEARCH_OUTPUT = ROOT / "frontend" / "research_runs.js"


def main() -> None:
    runs = []
    for data_dir in sorted(DATA_ROOT.iterdir()):
        if not data_dir.is_dir():
            continue
        metadata_path = data_dir / "run_metadata.json"
        summary_path = data_dir / "hopping_disorder_statistics.csv"
        figure_dir = FIGURE_ROOT / data_dir.name
        if not (metadata_path.is_file() and summary_path.is_file()):
            continue

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        with summary_path.open(newline="", encoding="utf-8-sig") as source:
            scan = list(csv.DictReader(source))
        if not scan:
            continue

        for row in scan:
            for key in ("t_prime", "W_uniform", "mean_pairing", "mean_spatial_std",
                        "sem_pairing", "converged_samples", "samples"):
                row[key] = float(row[key])
            row["converged_samples"] = int(row["converged_samples"])
            row["samples"] = int(row["samples"])

        runs.append({
            "id": data_dir.name,
            "scan": scan,
            "metadata": metadata,
            "figures": sorted(path.stem for path in figure_dir.glob("*.png")),
        })

    if not runs:
        raise RuntimeError("No saved scan runs with metadata and summary CSVs were found")
    OUTPUT.write_text(
        "window.QUANTUM_RUNS = " + json.dumps(runs, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )

    research_runs = []
    for data_dir in sorted(DATA_ROOT.glob("research_hartree*")):
        metadata_path = data_dir / "run_metadata.json"
        summary_path = data_dir / "hartree_fixed_density_statistics.csv"
        if not (metadata_path.is_file() and summary_path.is_file()):
            continue
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        with summary_path.open(newline="", encoding="utf-8-sig") as source:
            scan = list(csv.DictReader(source))
        if not scan:
            continue
        for row in scan:
            for key in ("L", "t_prime", "W_uniform", "mean_pairing", "sem_pairing",
                        "mean_twist_curvature", "sem_twist_curvature", "mean_density",
                        "max_density_residual", "samples"):
                row[key] = float(row[key])
            row["L"] = int(row["L"])
            row["samples"] = int(row["samples"])
        research_runs.append({"id": data_dir.name, "scan": scan, "metadata": metadata})
    if not research_runs:
        raise RuntimeError("No Hartree research runs with metadata and summary CSVs were found")
    RESEARCH_OUTPUT.write_text(
        "window.HARTREE_RUNS = " + json.dumps(research_runs, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"Bundled {len(runs)} scan runs and {len(research_runs)} Hartree research runs")


if __name__ == "__main__":
    main()
