"""Run one reproducible, instrument-smoothed virtual STM/STS experiment."""
from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.ndimage import gaussian_filter1d
from scipy.integrate import trapezoid
from scipy.signal import fftconvolve

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.disorder import onsite_disorder
from src.hamiltonian import electron_ldos
from src.lattice import square_lattice_hamiltonian
from src.solver import solve_hartree_bdg_fixed_density


def thermal_kernel(energy: np.ndarray, temperature: float) -> np.ndarray:
    """Normalized -df/dE kernel for finite-temperature tunneling conductance."""
    z = np.clip(energy / (2 * temperature), -350, 350)
    kernel = 1.0 / (4 * temperature * np.cosh(z) ** 2)
    area = trapezoid(kernel, energy)
    if not np.isfinite(area) or area <= 0:
        raise ValueError("Could not normalize the thermal broadening kernel")
    return kernel / area


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="virtual_sts_20261026")
    parser.add_argument("--size", type=int, default=6, help="Linear lattice size (default: 6)")
    parser.add_argument("--U", type=float, default=2.2, help="Attraction magnitude in units of t")
    parser.add_argument("--temperature", type=float, default=0.08, help="k_B T / t")
    parser.add_argument("--density", type=float, default=0.87, help="Target total density per site")
    parser.add_argument("--disorder", type=float, default=0.6, help="Uniform disorder width W/t")
    parser.add_argument("--t-prime", type=float, default=0.0, help="Next-neighbor hopping t'/t")
    parser.add_argument("--seed", type=int, default=20261026)
    parser.add_argument("--eta", type=float, default=0.06, help="Gaussian spectral sigma in units of t")
    parser.add_argument("--lockin", type=float, default=0.025, help="Gaussian lock-in sigma in units of t")
    parser.add_argument("--energy-limit", type=float, default=3.5, help="Plot bias range in units of t")
    parser.add_argument("--points", type=int, default=501, help="Number of energy/bias points")
    args = parser.parse_args()
    if (args.size < 3 or args.U <= 0 or args.temperature <= 0 or not 0 < args.density < 2
            or args.disorder < 0 or args.eta <= 0 or args.lockin < 0
            or args.energy_limit <= 0 or args.points < 101):
        raise SystemExit("Invalid parameters; require size>=3, positive U/T/eta/energy-limit, "
                         "0<density<2, disorder>=0, lockin>=0, and points>=101")

    run_id = args.run_id
    data_dir = ROOT / "results" / "data" / run_id
    figure_dir = ROOT / "results" / "figures" / run_id
    data_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    L = args.size
    nsite = L * L
    potential = onsite_disorder(nsite, args.disorder, "uniform", args.seed)
    K0 = square_lattice_hamiltonian(L, 1.0, args.t_prime, 0.0, potential)
    solution = solve_hartree_bdg_fixed_density(
        K0, args.U, args.temperature, args.density,
        initial_gap=0.25, tolerance=2e-5, density_tolerance=1e-4,
        max_iterations=2500, mixing=0.12,
    )
    if not solution.converged:
        raise RuntimeError(
            f"Self-consistency did not converge after {solution.iterations} iterations; "
            f"density residual={solution.density_residual:.3g}. No measurement was generated."
        )

    K_eff = K0 - solution.mu * np.eye(nsite) - np.diag(args.U * solution.density / 2)
    energy = np.linspace(-args.energy_limit, args.energy_limit, args.points)
    spacing = float(energy[1] - energy[0])
    ldos = electron_ldos(K_eff, solution.gap, energy, args.eta)

    # Synthetic dI/dV(V) = integral A(E) [-df(E-V)/dE] dE, followed by
    # Gaussian lock-in smoothing. This is the ideal local tunneling limit;
    # matrix elements and feedback are intentionally not modeled.
    temp_kernel = thermal_kernel(energy, args.temperature)
    ideal_conductance = fftconvolve(ldos, temp_kernel[None, :], mode="same", axes=1) * spacing
    lockin_sigma_points = args.lockin / spacing
    conductance = (gaussian_filter1d(ideal_conductance, lockin_sigma_points, axis=1, mode="nearest")
                   if lockin_sigma_points > 0 else ideal_conductance)

    coords_x = np.repeat(np.arange(L), L)
    coords_y = np.tile(np.arange(L), L)
    site_frame = pd.DataFrame({
        "site": np.arange(nsite), "x": coords_x, "y": coords_y,
        "onsite_potential_over_t": potential,
        "local_density": solution.density,
        "gap_real_over_t": np.real(solution.gap),
        "gap_imag_over_t": np.imag(solution.gap),
        "gap_amplitude_over_t": np.abs(solution.gap),
    })
    site_frame.to_csv(data_dir / "virtual_sample_sites.csv", index=False)

    sts_rows = []
    for site in range(nsite):
        sts_rows.append(pd.DataFrame({
            "site": site, "x": int(coords_x[site]), "y": int(coords_y[site]),
            "bias_over_t": energy,
            "ldos_per_site_per_spin_over_1_over_t": ldos[site],
            "synthetic_didv_arb_per_t": conductance[site],
        }))
    pd.concat(sts_rows, ignore_index=True).to_csv(data_dir / "virtual_sts_spectra.csv", index=False)

    # Measure at zero bias and at the dominant positive-bias coherence peak.
    mean_spectrum = conductance.mean(axis=0)
    positive = np.flatnonzero(energy > max(args.temperature, 0.05))
    peak_index = positive[np.argmax(mean_spectrum[positive])]
    zero_index = int(np.argmin(np.abs(energy)))
    peak_bias = float(energy[peak_index])
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), constrained_layout=True)
    maps = [
        (potential.reshape(L, L), "Disorder landscape", r"$V_i/t$", "coolwarm"),
        (np.abs(solution.gap).reshape(L, L), "Self-consistent gap map", r"$|\Delta_i|/t$", "viridis"),
        (conductance[:, zero_index].reshape(L, L), "Synthetic dI/dV at zero bias", "arb. units", "magma"),
    ]
    for ax, (values, title, label, cmap) in zip(axes, maps):
        im = ax.imshow(values, origin="lower", cmap=cmap)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("y site")
        ax.set_ylabel("x site")
        fig.colorbar(im, ax=ax, shrink=0.78, label=label)
    fig.savefig(figure_dir / "virtual_stm_maps.png", dpi=180)
    fig.savefig(figure_dir / "virtual_stm_maps.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.4), constrained_layout=True)
    ax.plot(energy, mean_spectrum, color="#168b73", lw=2.2, label="site-averaged dI/dV")
    for site, label in ((0, "site 0"), (nsite // 2, f"site {nsite // 2}"), (nsite - 1, f"site {nsite - 1}")):
        ax.plot(energy, conductance[site], lw=1, alpha=0.72, label=label)
    ax.axvline(0, color="#555", lw=0.8)
    ax.axvline(peak_bias, color="#b24c41", lw=0.9, ls="--", label=f"positive peak {peak_bias:.3f} t")
    ax.set(xlabel="Bias energy / t", ylabel="Synthetic dI/dV (arb. units)",
           title="Virtual tunneling spectra")
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(figure_dir / "virtual_stm_spectra.png", dpi=180)
    fig.savefig(figure_dir / "virtual_stm_spectra.pdf")
    plt.close(fig)

    mean_ldos = ldos.mean(axis=0)
    pd.DataFrame({
        "energy_or_bias_over_t": energy,
        "mean_ldos_per_site_per_spin_over_1_over_t": mean_ldos,
        "mean_synthetic_didv_arb_per_t": mean_spectrum,
    }).to_csv(data_dir / "virtual_sts_average_spectrum.csv", index=False)

    metadata = {
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__, "scipy": scipy.__version__, "pandas": pd.__version__,
        "protocol": [
            "Generate a periodic square-lattice sample with seeded uniform onsite disorder.",
            "Solve Hartree and pairing fields self-consistently at fixed mean density.",
            "Calculate site-resolved electron LDOS with Gaussian spectral broadening eta.",
            "Convolve LDOS with the finite-temperature -df/dE kernel to form ideal local dI/dV.",
            "Apply Gaussian lock-in broadening and save virtual spatial maps and spectra.",
        ],
        "parameters": {
            "L": L, "sites": nsite, "t_over_t": 1.0, "t_prime_over_t": args.t_prime,
            "U_over_t": args.U, "temperature_kBT_over_t": args.temperature,
            "target_total_density_per_site": args.density,
            "uniform_disorder_width_W_over_t": args.disorder,
            "disorder_distribution": "uniform[-W/2,W/2]", "seed": args.seed,
            "spectral_gaussian_sigma_eta_over_t": args.eta,
            "lockin_gaussian_sigma_over_t": args.lockin,
            "energy_grid_over_t": [-args.energy_limit, args.energy_limit, args.points],
            "solver_tolerance": 2e-5, "density_tolerance": 1e-4,
            "solver_iterations": solution.iterations,
        },
        "solver": {"converged": solution.converged, "chemical_potential_over_t": solution.mu,
                   "mean_density": float(solution.density.mean()),
                   "density_residual": solution.density_residual,
                   "mean_gap_amplitude_over_t": float(np.mean(np.abs(solution.gap))),
                   "positive_conductance_peak_bias_over_t": peak_bias,
                   "zero_bias_mean_didv_arb_per_t": float(mean_spectrum[zero_index])},
        "measurement_model": "Local tunneling approximation; thermally convolved electron LDOS plus Gaussian lock-in broadening.",
        "limitations": [
            "Generic attractive-Hubbard BdG model; parameters are not mapped to a named material.",
            "Synthetic dI/dV uses a local, energy-independent tunneling matrix element.",
            "No tip height feedback, setpoint normalization, spatial tip convolution, or measurement noise is included.",
            "One small periodic disorder realization is a demonstration, not a disorder average or experimental prediction.",
        ],
    }
    (data_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    print(f"Data: {data_dir}")
    print(f"Figures: {figure_dir}")


if __name__ == "__main__":
    main()
