"""Replace duplicated scratch cells with independent reusable-module notebooks."""
import json
from pathlib import Path
from itertools import count
root=Path(__file__).resolve().parents[1]
_ids=count(1)
def md(s): return {"id":f"cell-{next(_ids):03d}","cell_type":"markdown","metadata":{},"source":s.splitlines(True)}
def code(s): return {"id":f"cell-{next(_ids):03d}","cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":s.splitlines(True)}
setup='''from pathlib import Path
import sys
ROOT = Path.cwd()
if not (ROOT / "src").exists(): ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
from src.lattice import square_lattice_hamiltonian, square_lattice_dispersion, momentum_grid
from src.gap_equation import uniform_gap
from src.solver import solve_bdg
from src.disorder import onsite_disorder
from src.hamiltonian import gaussian_dos
print("Project:", ROOT)
'''
books={
'01_clean_bcs_validation.ipynb':[
md('# Clean BCS validation\n\nThis notebook compares the finite-bandwidth momentum-space gap equation with independent real-space self-consistent BdG calculations. Units use t=1 and k_B=1; chemical potential is fixed.'),code(setup),
code('''L, U, T, mu = 4, 2.2, 0.08, -0.5
reference = uniform_gap(L, U, T, mu=mu)
K = square_lattice_hamiltonian(L, mu=mu)
result = solve_bdg(K, U, T, initial_gap=reference, tolerance=1e-9)
print(f"k-space gap={reference:.12g}; BdG mean={result.gap.mean():.12g}")
print("converged:", result.converged, "max spatial variation:", np.ptp(result.gap))
assert result.converged and np.allclose(result.gap, reference, atol=1e-8)
'''),
md('The reference uses the finite periodic lattice k-grid and the same dispersion, chemical potential, and pairing-only assumptions as BdG. It is not a constant-DOS approximation.'),
code('''temperatures = np.linspace(0.01, 0.4, 35)
gaps = np.array([uniform_gap(12, U, t, mu=mu) for t in temperatures])
plt.plot(temperatures, gaps, "o-", ms=3); plt.xlabel("T/t"); plt.ylabel("Uniform pairing amplitude Δ/t"); plt.grid(alpha=.3); plt.show()
''')],
'02_clean_bdg.ipynb':[
md('# Clean real-space BdG\n\nDispersion, self-consistent gap, complete signed spectrum, broadened positive-mode spectrum, and residual history.'),code(setup),
code('''L, t, t_prime, mu, U, T = 6, 1., 0.1, -0.5, 2.2, 0.08
k = np.linspace(-np.pi, np.pi, 100)
kx, ky = np.meshgrid(k,k,indexing="ij")
xi = square_lattice_dispersion(kx,ky,t,t_prime,mu)
plt.contourf(kx,ky,xi,35,cmap="coolwarm"); plt.colorbar(label="ξ(k)/t"); plt.xlabel("kx"); plt.ylabel("ky"); plt.show()
'''),
code('''K = square_lattice_hamiltonian(L,t,t_prime,mu)
guess = uniform_gap(L,U,T,t,t_prime,mu)
result = solve_bdg(K,U,T,initial_gap=guess,tolerance=1e-8,max_iterations=100)
print("converged:",result.converged,"iterations:",result.iterations,"mean |Δ|:",np.mean(np.abs(result.gap)))
plt.semilogy(np.maximum(result.residual_history,1e-16)); plt.xlabel("Iteration"); plt.ylabel("max update/t"); plt.show()
plt.plot(result.all_energies,".",ms=3); plt.axhline(0,color="k",lw=.7); plt.ylabel("Energy/t"); plt.xlabel("Sorted state"); plt.show()
grid=np.linspace(0,4,400); dos=gaussian_dos(result.energies,grid,.06)
plt.plot(grid,dos); plt.xlabel("Positive mode energy/t"); plt.ylabel("Normalized mode DOS"); plt.show()
''')],
'03_disorder_study.ipynb':[
md('# Disorder study\n\nA reproducible scalar-disorder realization and self-consistent local pairing solution. Uniform width W means V∈[-W/2,W/2] and variance W²/12.'),code(setup),
code('''L, t, tp, mu, U, T, W, seed = 8, 1., 0., -0.5, 2.2, 0.08, 1.0, 4207
V = onsite_disorder(L*L,W,"uniform",seed)
K = square_lattice_hamiltonian(L,t,tp,mu,V)
result = solve_bdg(K,U,T,initial_gap=.3,tolerance=2e-6,max_iterations=400,mixing=.5)
print("seed",seed,"converged",result.converged,"iterations",result.iterations)
print("mean, spatial SD, min, max |Δ|:",np.mean(np.abs(result.gap)),np.std(np.abs(result.gap)),np.min(np.abs(result.gap)),np.max(np.abs(result.gap)))
'''),
code('''fig,ax=plt.subplots(1,2,figsize=(9,4))
im=ax[0].imshow(V.reshape(L,L),origin="lower"); fig.colorbar(im,ax=ax[0],label="Vi/t"); ax[0].set_title("Onsite potential")
im=ax[1].imshow(np.abs(result.gap).reshape(L,L),origin="lower"); fig.colorbar(im,ax=ax[1],label="|Δi|/t"); ax[1].set_title("Pairing amplitude")
plt.tight_layout(); plt.show()
''')],
'04_parameter_scan.ipynb':[
md('# Small parameter scan\n\nIndependent quick scan with matched seeded configurations, realization-level uncertainty, and a heatmap. Increase sizes and sample counts only after checking runtime. This notebook does not read another notebook’s state.'),code(setup),
code('''L, t, mu, U, T = 6, 1., -0.5, 2.2, 0.08
Ws, tps, nreal, seed0 = [0.,.8], [0.,.2], 2, 7341
rows=[]
for tp in tps:
    for W in Ws:
        for r in range(nreal):
            seed=seed0+int(W*100)+r
            V=onsite_disorder(L*L,W,"uniform",seed)
            result=solve_bdg(square_lattice_hamiltonian(L,t,tp,mu,V),U,T,initial_gap=.3,tolerance=5e-6,max_iterations=300,mixing=.55)
            a=np.abs(result.gap)
            rows.append(dict(t_prime=tp,W=W,realization=r,seed=seed,mean_gap=a.mean(),spatial_std=a.std(),converged=result.converged,iterations=result.iterations))
import pandas as pd
raw=pd.DataFrame(rows); display(raw)
summary=raw.groupby(["t_prime","W"]).agg(mean_gap=("mean_gap","mean"),sd=("mean_gap","std"),mean_spatial_std=("spatial_std","mean"),samples=("realization","count")).reset_index()
summary["sem"]=summary.sd/np.sqrt(summary.samples); display(summary)
'''),
code('''for tp in tps:
    q=summary[summary.t_prime==tp]
plt.errorbar(q["W"],q["mean_gap"],yerr=q["sem"],marker="o",capsize=3,label=f"t'/t={tp:g}")
plt.xlabel("Uniform disorder width W/t"); plt.ylabel("Mean |Δi|/t"); plt.legend(); plt.grid(alpha=.3); plt.show()
heat=summary.pivot(index="t_prime",columns="W",values="mean_gap")
plt.imshow(heat.values,aspect="auto",origin="lower"); plt.xticks(range(len(heat.columns)),heat.columns); plt.yticks(range(len(heat.index)),heat.index); plt.xlabel("W/t grid index"); plt.ylabel("t'/t grid index"); plt.colorbar(label="Mean |Δi|/t"); plt.show()
''')]
}
for name,cells in books.items():
    doc={"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.11+"}},"nbformat":4,"nbformat_minor":5}
    (root/"notebooks"/name).write_text(json.dumps(doc,indent=1,ensure_ascii=False)+"\n",encoding="utf-8")
    print("wrote",name)
