# Model and conventions

## Hamiltonian

We use one orbital per site on a square lattice and write

\[
H= -\sum_{ij\sigma}t_{ij}c^\dagger_{i\sigma}c_{j\sigma}
-\mu\sum_{i\sigma}n_{i\sigma}
-U\sum_i n_{i\uparrow}n_{i\downarrow}
+\sum_{i\sigma}V_i n_{i\sigma},\qquad U>0.
\]

Nearest-neighbor matrix elements are \(t\), diagonal next-nearest-neighbor
elements are \(t'\), and \(K_{ij}= -t_{ij}+(V_i-\mu)\delta_{ij}\).
The clean dispersion is
\(\xi_{\bf k}=-2t(\cos k_x+\cos k_y)-4t'\cos k_x\cos k_y-\mu\).
We set \(k_B=1\); energies and temperature are reported in units of \(t\).
The code fixes chemical potential; it does not solve a number equation for
fixed filling.

## Pairing-only mean field

For \(F_i=\langle c_{i\downarrow}c_{i\uparrow}\rangle\), define
\(\Delta_i=U F_i\). Decoupling only in the pairing channel gives the local
terms \(-\Delta_i c^\dagger_{i\uparrow}c^\dagger_{i\downarrow}
-\Delta_i^*c_{i\downarrow}c_{i\uparrow}+|\Delta_i|^2/U\).
This is a self-consistent order parameter, not an imposed phenomenological
gap. The density (Hartree) channel is intentionally omitted. At fixed \(\mu\),
including it would shift the effective local chemical potential and require
solving density and pairing fields together; results here therefore represent
pairing-only BdG mean field, not the full unrestricted Hartree-Fock-Bogoliubov
decoupling.

Use the Nambu spinor \(\Psi=(c_{1\uparrow},\ldots,c_{N\uparrow},
c^\dagger_{1\downarrow},\ldots,c^\dagger_{N\downarrow})^T\). Up to the usual
constant, its matrix is

\[
\mathcal H_{BdG}=\begin{pmatrix}K&-D\\-D^*&-K^T\end{pmatrix},
\quad D_{ij}=\Delta_i\delta_{ij}.
\]

The transpose is essential for nonuniform real-space potentials. For normalized
positive-energy eigenvectors \((u_n,v_n)^T\), the anomalous average is
\(F_i=-\sum_{E_n>0}u_{in}v^*_{in}\tanh(E_n/2T)\), so the update is
\(\Delta_i=-U\sum_{E_n>0}u_{in}v^*_{in}\tanh(E_n/2T)\). The sum is over one
positive-energy state from each particle-hole pair; adding an additional spin
factor would double count. At \(T=0\), the hyperbolic tangent is one.

For a spatially uniform clean state, \(E_{\bf k}=\sqrt{\xi_{\bf k}^2+|\Delta|^2}\)
and
\[
1=\frac{U}{2N_k}\sum_{\bf k}\frac{\tanh(E_{\bf k}/2T)}{E_{\bf k}}.
\]
The reference solver evaluates this same finite-bandwidth periodic momentum
sum. It has no Debye cutoff and is not the continuum constant-DOS BCS formula.

## Observables and interpretation

The reported local pairing amplitude is \(|\Delta_i|\). It is distinct from the
minimum positive quasiparticle eigenenergy (a spectral gap), and neither is a
thermodynamic transition temperature. In two dimensions, phase fluctuations
and Berezinskii-Kosterlitz-Thouless physics can separate pair formation from
phase coherence; static BdG mean field does not calculate that transition.
Disorder is scalar and time-reversal invariant. The uniform distribution is
\([-W/2,W/2]\), with variance \(W^2/12\). Gaussian input uses standard
deviation \(W\), so the two strengths are not directly equivalent.

Periodic directed translations are accumulated. This preserves the Fourier
dispersion, including bond multiplicities when periodic neighbors coincide for
L=1 or 2. The density function reports total up-plus-down density from the
pairing-only BdG eigenvectors. The electron DOS uses \(|u_{in}|^2\) at positive
energy and \(|v_{in}|^2\) at negative energy. The site-resolved LDOS is saved
for the disordered example. Gaussian broadening has standard deviation
\(\eta\), and the DOS is spin-resolved per site.
