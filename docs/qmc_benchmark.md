# Parameter-matched QMC trend check

## Reference

Scalettar, Trivedi, and Huscroft studied the disordered attractive Hubbard
model using determinant quantum Monte Carlo (DQMC). Their square-lattice
calculation uses a uniform random site potential and reports a strong reduction
of superfluid stiffness with increasing disorder. For their U/t=4, density
near 0.875, and T/t=0.1 case, stiffness is finite at weak disorder and vanishes
at W/t=4; their finite-size analysis places the critical disorder around
3–4t. See the [arXiv paper](https://arxiv.org/abs/cond-mat/9807008), especially
the stiffness discussion and Figs. 7–10.

## Project calculation

The comparison run uses L=8, U/t=4, T/t=0.1, target density 0.875, t'/t=0,
uniform disorder at W/t=1 and 4, eight seeded disorder realizations per point,
one phase start, and twist step delta=0.05. Results are stored in
`results/data/qmc_benchmark_scalettar_20261026/`.

The project reports the second derivative of the relaxed fixed-density
mean-field free energy with respect to boundary twist. The QMC paper instead
extracts stiffness from the transverse current-current response and relates its
normalization to rho_s = D_s/pi. The values are therefore not treated as
numerically interchangeable. The benchmark checks whether the computed
disorder trend is consistent with QMC, not whether mean field reproduces the
QMC values.

The eight-sample project result was:

| W/t | Mean pairing / t | Mean twist curvature / t |
|---:|---:|---:|
| 1 | 1.126 +/- 0.021 | 0.418 +/- 0.020 |
| 4 | 0.371 +/- 0.044 | 0.021 +/- 0.008 |

All 16 calculations converged and the largest density residual was
1.68e-7. Both project observables drop strongly between W/t=1 and 4, matching
the direction of the QMC trend. The L=8 mean-field twist curvature remains
small but positive at W/t=4, while the paper reports zero QMC stiffness there.
This difference is a useful warning about finite-size and method dependence;
it does not support claiming a reproduced critical point.

There are two more differences: this project fixes the target density for each
disorder realization, while the QMC paper tunes density after disorder
averaging; and eight samples with one phase start are only a small numerical
check. A mismatch in magnitude or behavior is evidence to investigate, not a
failed reproduction of identical methods. No critical disorder or transition
temperature is inferred from this run.
