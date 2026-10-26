# Virtual STM/STS protocol

This workflow models one small simulated sample as a sequence of sample
preparation and scanning tunneling spectroscopy steps. It provides an
experiment-inspired observable for the generic attractive-Hubbard BdG model;
it is not calibrated to a specific material.

## Measurement sequence

1. **Prepare the sample.** A periodic `L × L` square lattice is assigned a
   seeded uniform onsite potential, with `V_i` drawn from `[-W/2, W/2]`.
2. **Set the state.** The Hartree density and superconducting pairing fields
   are solved self-consistently at a chosen temperature and target mean
   density. A run that does not converge stops without generating spectra.
3. **Scan local spectra.** For each site, the code calculates the electron
   local density of states (LDOS), with Gaussian spectral standard deviation
   `eta`.
4. **Model the conductance measurement.** In the local tunneling approximation,
   the finite-temperature signal is

   `dI/dV_i(V) ∝ ∫ A_i(E) [-∂f(E−V)/∂E] dE`,

   where `A_i(E)` is the site LDOS and `f` is the Fermi function. The result is
   then smoothed by a Gaussian lock-in resolution.
5. **Make maps and line spectra.** The script saves disorder and gap maps, a
   zero-bias conductance map, site-resolved spectra, a site-average spectrum,
   and run metadata. The dashed marker on the spectrum figure shows the
   strongest positive-bias peak of the site-averaged signal.

## Reproduce the example

From the project root:

```powershell
python scripts\run_virtual_sts.py
```

The checked-in example uses `L=6`, `U/t=2.2`, `kBT/t=0.08`, target density
`0.87`, uniform `W/t=0.6`, seed `20261026`, LDOS broadening `eta/t=0.06`, and
lock-in Gaussian sigma `0.025t`. Change these values with command-line options;
for example:

```powershell
python scripts\run_virtual_sts.py --size 8 --disorder 1.0 --seed 23
```

The default results are written to `results/data/virtual_sts_20261026/` and
`results/figures/virtual_sts_20261026/`. Rebuild the static frontend with
`python scripts/build_static_site.py`. The results are shown on
`frontend/research.html`.

## Interpretation limits

The conductance is an idealized local tunneling signal with an
energy-independent tunneling matrix element. The model does not simulate tip
height feedback or setpoint normalization, spatial tip convolution, lock-in
harmonics, noise, a real material's band structure, or a disorder average. The
default is one 36-site sample. Its maps illustrate how this model connects a
disorder realization to local spectra; they should not be interpreted as an
experimental prediction.
