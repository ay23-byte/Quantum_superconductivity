# Literature review and novelty assessment

## Verified references

1. J. Bardeen, L. N. Cooper, and J. R. Schrieffer, “Theory of
   Superconductivity,” *Phys. Rev.* **108**, 1175 (1957),
   [doi:10.1103/PhysRev.108.1175](https://doi.org/10.1103/PhysRev.108.1175).
   Foundational weak-coupling BCS theory.
2. P. G. de Gennes, *Superconductivity of Metals and Alloys*, Addison-Wesley
   (1989 reprint). Standard BdG and superconductivity reference.
3. A. Ghosal, M. Randeria, and N. Trivedi, “Inhomogeneous pairing in highly
   disordered s-wave superconductors,” *Phys. Rev. B* **65**, 014501 (2001),
   [doi:10.1103/PhysRevB.65.014501](https://doi.org/10.1103/PhysRevB.65.014501).
   Their two-dimensional random-potential BdG study reports spatially
   inhomogeneous pairing at strong disorder and discusses spectral and
   phase-related consequences.
4. C. Huscroft and R. T. Scalettar, “Effect of disorder on charge-density
   wave and superconducting order in the half-filled attractive Hubbard
   model,” *Phys. Rev. B* **55**, 1185 (1997),
   [doi:10.1103/PhysRevB.55.1185](https://doi.org/10.1103/PhysRevB.55.1185).
   Quantum Monte Carlo study of site-energy disorder and competing CDW and
   superconducting correlations at half filling.
5. K. Aryanpour et al., “Effect of inhomogeneity on s-wave superconductivity
   in the attractive Hubbard model,” *Phys. Rev. B* **73**, 104518 (2006),
   [doi:10.1103/PhysRevB.73.104518](https://doi.org/10.1103/PhysRevB.73.104518).
   BdG study of inhomogeneous interaction strength in the square-lattice
   attractive Hubbard model.
6. R. A. Fontenele et al., “Second-Neighbor Hopping Effects in the
   Two-Dimensional Attractive Hubbard Model,” *Condensed Matter* **8**(1), 11
   (2023), [doi:10.3390/condmat8010011](https://doi.org/10.3390/condmat8010011).
   Fixed-density determinant quantum Monte Carlo study of pairing and
   next-nearest-neighbor hopping.
7. R. A. Fontenele, N. C. Costa, T. Paiva, and R. R. dos Santos, “Effects of
   next-nearest neighbor hopping on the pairing and critical temperatures of
   the attractive Hubbard model on a square lattice,” *Phys. Rev. B* **113**,
   104519 (2026), [doi:10.1103/tgs1-r698](https://doi.org/10.1103/tgs1-r698).
   Determinant quantum Monte Carlo study of pairing response, superfluid
   density, spin susceptibility, and transition-temperature effects of t'.
8. R. R. dos Santos, “Second-neighbor hopping in the attractive Hubbard
   model,” *Phys. Rev. B* **46**, 5496 (1992),
   [doi:10.1103/PhysRevB.46.5496](https://doi.org/10.1103/PhysRevB.46.5496).
   Earlier Monte Carlo study of next-neighbor hopping in the attractive model.

Bibliographic metadata for the newer t' results were checked against the
publisher records. The summaries above are scoped; consult each full article
before using detailed claims in a thesis.

## Novelty gate

Disorder-induced spatial modulation of s-wave pairing in two-dimensional
BdG/Hubbard models is established prior work. Effects of next-nearest-neighbor
hopping on attractive-Hubbard pairing and transition behavior are also
established, including recent determinant quantum Monte Carlo studies.
Consequently, neither theme is novel by itself, and adding a t' scan does not
establish novelty. The current repository is an implementation-validation
and exploratory calculation, not a publication-ready discovery.

The literature check did not establish whether the precise combination of
scalar onsite disorder and t' in this project's fixed-chemical-potential,
pairing-only BdG setup has already been studied. No novelty claim should be
made without a systematic search and comparison of methods and observables.
Potential follow-up questions include matched-variance disorder comparisons
at fixed density, correlated disorder, filling dependence near the van Hove
region, finite-size scaling, and superfluid stiffness or phase fluctuations
benchmarked against quantum Monte Carlo. The current results do not answer
those questions.
