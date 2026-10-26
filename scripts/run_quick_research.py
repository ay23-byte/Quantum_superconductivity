"""Generate the checked-in-size quick research run (CPU only, deterministic)."""
from __future__ import annotations
import json, platform, sys, argparse
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import scipy, matplotlib
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.lattice import square_lattice_hamiltonian, square_lattice_dispersion
from src.gap_equation import uniform_gap
from src.disorder import onsite_disorder
from src.solver import solve_bdg, density_from_result
from src.hamiltonian import bdg_hamiltonian, electron_ldos
from src.validation import clean_limit_comparison
from scripts.build_dashboard_data import main as build_dashboard_data

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--run-id",default="quick_20261023")
parser.add_argument("--realizations",type=int,default=3)
parser.add_argument("--size-check-realizations",type=int,default=10)
args=parser.parse_args()
if args.realizations<2 or args.size_check_realizations<2:
    raise SystemExit("Use at least two disorder realizations for statistical summaries")
RUN=args.run_id
DATA=ROOT/"results"/"data"/RUN; FIG=ROOT/"results"/"figures"/RUN
DATA.mkdir(parents=True,exist_ok=True); FIG.mkdir(parents=True,exist_ok=True)
L=6; t=1.; mu=-.5; U=2.2; T=.08; seed=94721; nreal=args.realizations
Wvals=[0.,.6,1.2]; tpvals=[0.,.2]
def savefig(name):
    plt.tight_layout(); plt.savefig(FIG/(name+".png"),dpi=180); plt.savefig(FIG/(name+".pdf")); plt.close()

# Independent clean uniform results and hopping/disorder scan. Use matched seeds
# for each W across t' values to make controlled comparisons.
records=[]; maps={}; sample=0
for tp in tpvals:
  for W in Wvals:
    for r in range(nreal):
      this_seed=seed+round(W*100)+r
      v=onsite_disorder(L*L,W,"uniform",this_seed)
      K=square_lattice_hamiltonian(L,t,tp,mu,v)
      out=solve_bdg(K,U,T,initial_gap=.25,tolerance=2e-6,max_iterations=350,mixing=.55)
      g=np.abs(out.gap)
      records.append(dict(L=L,t=t,t_prime=tp,mu=mu,U=U,T=T,W_uniform= W,realization=r,seed=this_seed,
          mean_pairing=g.mean(),spatial_std_pairing=g.std(),minimum_pairing=g.min(),maximum_pairing=g.max(),
          iterations=out.iterations,final_residual=out.residual_history[-1],converged=out.converged,
          mean_density=float(density_from_result(K,out,T).mean())))
      if tp==0 and W==1.2 and r==0: maps["disorder"]=v; maps["gap"]=out.gap.copy(); maps["energies"]=out.all_energies.copy(); maps["history"]=out.residual_history; maps["seed"]=this_seed
      sample+=1
raw=pd.DataFrame(records); raw.to_csv(DATA/"hopping_disorder_realizations.csv",index=False)
summary=raw.groupby(["t_prime","W_uniform"]).agg(mean_pairing=("mean_pairing","mean"),
    sample_sd_pairing=("mean_pairing","std"), mean_spatial_std=("spatial_std_pairing","mean"),
    sample_sd_spatial_std=("spatial_std_pairing","std"),converged_samples=("converged","sum"),samples=("realization","count")).reset_index()
summary["sem_pairing"]=summary.sample_sd_pairing/np.sqrt(summary.samples)
summary["sem_spatial_std"]=summary.sample_sd_spatial_std/np.sqrt(summary.samples)
summary.to_csv(DATA/"hopping_disorder_statistics.csv",index=False)

# Figure 1: normal state dispersion and Fermi contour on a continuous grid.
k=np.linspace(-np.pi,np.pi,121); kx,ky=np.meshgrid(k,k,indexing="ij")
xi=square_lattice_dispersion(kx,ky,t,.0,mu)
plt.figure(figsize=(6,4.8)); plt.contourf(kx,ky,xi,40,cmap="coolwarm"); plt.colorbar(label=r"$\xi_{\mathbf{k}}/t$"); plt.xlabel(r"$k_x$"); plt.ylabel(r"$k_y$"); plt.title("Square-lattice normal-state dispersion"); savefig("dispersion")

# Figure 2 and 3: k-grid BCS at L=12, finite bandwidth.
Ts=np.linspace(.01,.35,36); gapsT=np.array([uniform_gap(12,U,z,mu=mu) for z in Ts])
pd.DataFrame({"T_over_t":Ts,"gap_over_t":gapsT}).to_csv(DATA/"clean_gap_vs_temperature.csv",index=False)
plt.figure(figsize=(6,4)); plt.plot(Ts,gapsT,"o-",ms=3); plt.xlabel("T/t"); plt.ylabel(r"Uniform pairing amplitude $\Delta/t$"); plt.title("Finite-grid uniform BCS gap vs temperature"); savefig("gap_vs_temperature")
Us=np.linspace(0.5,4.0,36); gapsU=np.array([uniform_gap(12,float(u),T,mu=mu) for u in Us])
pd.DataFrame({"U_over_t":Us,"gap_over_t":gapsU}).to_csv(DATA/"clean_gap_vs_interaction.csv",index=False)
plt.figure(figsize=(6,4)); plt.plot(Us,gapsU); plt.xlabel("U/t"); plt.ylabel(r"Uniform pairing amplitude $\Delta/t$"); plt.title("Uniform BCS gap vs attraction"); savefig("gap_vs_interaction")

# Figure 4: positive/negative BdG spectrum. Clean self-consistency at same grid.
K0=square_lattice_hamiltonian(L,t,0.,mu); d0=uniform_gap(L,U,T,mu=mu)
clean=solve_bdg(K0,U,T,initial_gap=d0,tolerance=1e-9,max_iterations=10)
plt.figure(figsize=(6,4)); plt.plot(np.arange(len(clean.all_energies)),clean.all_energies,".",ms=3); plt.axhline(0,color="k",lw=.7); plt.xlabel("Sorted BdG state index"); plt.ylabel("Energy/t"); plt.title("Clean BdG spectrum (both signs)"); savefig("bdg_spectrum")

# Figure 5: normalized positive-energy DOS with stated Gaussian broadening.
grid=np.linspace(-4,4,601); eta=.06
Kdis=square_lattice_hamiltonian(L,t,0.,mu,maps["disorder"])
scdis=solve_bdg(Kdis,U,T,initial_gap=.25,tolerance=2e-6,max_iterations=350,mixing=.55)
ldos0=electron_ldos(K0,clean.gap,grid,eta); ldos1=electron_ldos(Kdis,scdis.gap,grid,eta)
dos0=ldos0.mean(axis=0); dos1=ldos1.mean(axis=0)
plt.figure(figsize=(6,4)); plt.plot(grid,dos0,label="clean"); plt.plot(grid,dos1,label="uniform disorder W/t=1.2"); plt.xlabel("E/t"); plt.ylabel("Electron DOS per site per spin / t"); plt.title(f"Electron DOS, Gaussian sigma={eta:g}t"); plt.legend(); savefig("dos_clean_disordered")
pd.DataFrame(ldos1.T,index=grid,columns=[f"site_{i}" for i in range(L*L)]).rename_axis("energy_over_t").to_csv(DATA/"disordered_local_dos.csv")

# Disorder and pairing spatial maps.
for name,data,title,label in [("disorder_map",maps["disorder"],"Onsite disorder, W/t=1.2",r"$V_i/t$"),("gap_map",np.abs(maps["gap"]),"Self-consistent local pairing amplitude",r"$|\Delta_i|/t$")]:
    plt.figure(figsize=(5,4.4)); plt.imshow(data.reshape(L,L),origin="lower",cmap="viridis"); plt.colorbar(label=label); plt.xlabel("x site"); plt.ylabel("y site"); plt.title(title); savefig(name)

# Scan figures with realization-level uncertainty, never treating sites as samples.
for tp in tpvals:
    sub=summary[summary.t_prime==tp]
    plt.figure(figsize=(6,4)); plt.errorbar(sub.W_uniform,sub.mean_pairing,yerr=sub.sem_pairing,fmt="o-",capsize=3); plt.xlabel("Uniform disorder width W/t (support [-W/2,W/2])"); plt.ylabel(r"Mean $|\Delta_i|/t$"); plt.title(fr"Pairing vs disorder, $t'/t={tp:g}$, n={nreal} realizations"); savefig(f"mean_gap_vs_disorder_tp{tp:g}")
    plt.figure(figsize=(6,4)); plt.errorbar(sub.W_uniform,sub.mean_spatial_std,yerr=sub.sem_spatial_std,fmt="s-",capsize=3); plt.xlabel("W/t"); plt.ylabel(r"Mean spatial SD of $|\Delta_i|/t$"); plt.title(fr"Pairing inhomogeneity, $t'/t={tp:g}$"); savefig(f"inhomogeneity_vs_disorder_tp{tp:g}")
heat=summary.pivot(index="t_prime",columns="W_uniform",values="mean_pairing")
plt.figure(figsize=(6,3.5)); plt.imshow(heat.values,aspect="auto",origin="lower",cmap="magma",extent=[min(Wvals)-.3,max(Wvals)+.3,min(tpvals)-.1,max(tpvals)+.1]); plt.xticks(Wvals); plt.yticks(tpvals); plt.xlabel("W/t"); plt.ylabel("t'/t"); plt.colorbar(label=r"Mean $|\Delta_i|/t$"); plt.title("Exploratory hopping-disorder scan"); savefig("hopping_disorder_heatmap")
plt.figure(figsize=(6,4)); plt.semilogy(np.maximum(maps["history"],1e-16)); plt.xlabel("Iteration"); plt.ylabel("Maximum gap residual/t"); plt.title("BdG fixed-point residual (one realization)"); savefig("convergence_residual")

# Finite-size check: clean pairing amplitude at L=4,6,8 using same mu,U,T.
fs=[]
for size in [4,6,8]:
    ref=uniform_gap(size,U,T,mu=mu)
    res=solve_bdg(square_lattice_hamiltonian(size,t,0.,mu),U,T,initial_gap=ref,tolerance=1e-8,max_iterations=20)
    fs.append(dict(L=size,N_sites=size*size,reference_gap=ref,bdg_mean_gap=float(res.gap.mean()),spatial_std=float(res.gap.std()),converged=res.converged))
pd.DataFrame(fs).to_csv(DATA/"finite_size_check.csv",index=False)
plt.figure(figsize=(6,4)); plt.plot([r["L"] for r in fs],[r["bdg_mean_gap"] for r in fs],"o-",label="finite periodic k grids"); plt.axhline(uniform_gap(40,U,T,mu=mu),ls="--",label="L=40 k-grid reference"); plt.xlabel("Linear size L"); plt.ylabel(r"Mean pairing amplitude $\Delta/t$"); plt.title("Clean finite-size comparison"); plt.legend(); savefig("finite_size_comparison")

# Repeat the independent clean-limit check at multiple U and T values.
crosschecks=[]
for interaction in (1.5,2.2,3.0):
    for temperature in (.05,.12):
        ref=uniform_gap(4,interaction,temperature,t,0.0,mu)
        check=solve_bdg(square_lattice_hamiltonian(4,t,0.0,mu),interaction,temperature,
            initial_gap=ref,tolerance=1e-8,max_iterations=20)
        crosschecks.append(dict(L=4,U_over_t=interaction,T_over_t=temperature,
            reference_gap=ref,bdg_mean_gap=float(check.gap.mean()),
            absolute_difference=abs(float(check.gap.mean())-ref),converged=check.converged))
crosscheck_df=pd.DataFrame(crosschecks)
crosscheck_df.to_csv(DATA/"clean_limit_crosschecks.csv",index=False)

# Disorder finite-size check at W/t=1.2, t'/t=0. Reuse the first nf L=6
# samples from the main scan and add independently seeded L=4 and L=8 samples.
nf=min(args.size_check_realizations,nreal)
finite_dis=[]
middle=raw[(raw.t_prime==0.0)&(raw.W_uniform==1.2)].sort_values("realization").head(nf)
for _,row in middle.iterrows():
    finite_dis.append(dict(L=6,realization=int(row.realization),seed=int(row.seed),
        mean_pairing=row.mean_pairing,spatial_std_pairing=row.spatial_std_pairing,
        converged=bool(row.converged)))
for size in (4,8):
    for r in range(nf):
        this_seed=seed+120+r
        v=onsite_disorder(size*size,1.2,"uniform",this_seed)
        K=square_lattice_hamiltonian(size,t,0.0,mu,v)
        out=solve_bdg(K,U,T,initial_gap=.25,tolerance=2e-6,max_iterations=350,mixing=.55)
        a=np.abs(out.gap)
        finite_dis.append(dict(L=size,realization=r,seed=this_seed,mean_pairing=a.mean(),
            spatial_std_pairing=a.std(),converged=out.converged))
finite_dis_df=pd.DataFrame(finite_dis)
finite_dis_df.to_csv(DATA/"finite_size_disorder_realizations.csv",index=False)
finite_summary=finite_dis_df.groupby("L").agg(mean_pairing=("mean_pairing","mean"),
    sample_sd_pairing=("mean_pairing","std"),mean_spatial_std=("spatial_std_pairing","mean"),
    sample_sd_spatial_std=("spatial_std_pairing","std"),samples=("realization","count"),
    converged_samples=("converged","sum")).reset_index()
finite_summary["sem_pairing"]=finite_summary.sample_sd_pairing/np.sqrt(finite_summary.samples)
finite_summary["sem_spatial_std"]=finite_summary.sample_sd_spatial_std/np.sqrt(finite_summary.samples)
finite_summary.to_csv(DATA/"finite_size_disorder_statistics.csv",index=False)
plt.figure(figsize=(6,4)); plt.errorbar(finite_summary.L,finite_summary.mean_pairing,
    yerr=finite_summary.sem_pairing,fmt="o-",capsize=4)
plt.xlabel("Linear size L"); plt.ylabel(r"Mean pairing amplitude $|\Delta_i|/t$")
plt.title("Finite-size check: disordered pairing at W/t=1.2"); savefig("finite_size_disorder_comparison")

# Export arrays behind the one-sample diagnostic figures.
pd.DataFrame({"site":np.arange(L*L),"x":np.repeat(np.arange(L),L),"y":np.tile(np.arange(L),L),
    "onsite_potential_over_t":maps["disorder"],"gap_real_over_t":maps["gap"],
    "gap_amplitude_over_t":np.abs(maps["gap"])}).to_csv(DATA/"example_disorder_and_gap_map.csv",index=False)
pd.DataFrame({"iteration":np.arange(1,len(maps["history"])+1),
    "max_update_over_t":maps["history"]}).to_csv(DATA/"example_convergence_history.csv",index=False)
pd.DataFrame({"state_index":np.arange(len(clean.all_energies)),
    "energy_over_t":clean.all_energies}).to_csv(DATA/"clean_bdg_spectrum.csv",index=False)
pd.DataFrame({"energy_over_t":grid,"clean_electron_dos_per_site_per_spin":dos0,
    "disordered_electron_dos_per_site_per_spin":dos1}).to_csv(DATA/"clean_disordered_dos.csv",index=False)

validation=clean_limit_comparison(L=4,U=U,T=T,mu=mu,tolerance=1e-8)
unique_solves=int(len(raw)+2*nf)
meta=dict(run_id=RUN,timestamp_local="2026-10-23",python=sys.version,platform=platform.platform(),numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,pandas=pd.__version__,parameters=dict(L=L,t=t,mu=mu,U=U,T=T,uniform_W_values=Wvals,tprime_values=tpvals,disorder_distribution="uniform[-W/2,W/2]",disorder_seed_formula="seed_base + round(100*W) + realization_index",seed_base=seed,realizations_per_pair=nreal,finite_size_disorder_realizations=nf,tolerance=2e-6,mixing=.55),clean_validation=validation,clean_limit_crosschecks=crosscheck_df.to_dict(orient="records"),finite_size_clean=fs,finite_size_disorder=finite_summary.to_dict(orient="records"),all_scan_samples_converged=bool(raw.converged.all()),all_finite_size_disorder_converged=bool(finite_dis_df.converged.all()),all_clean_crosschecks_converged=bool(crosscheck_df.converged.all()),sample_count=int(len(raw)),unique_solver_runs=unique_solves,all_unique_runs_converged=bool(raw.converged.all() and finite_dis_df.converged.all()),dos_broadening_eta=eta,dos_convention="spin-resolved electron DOS; Gaussian broadening")
(DATA/"run_metadata.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
(ROOT/"frontend"/"data.js").write_text(
    "window.QUANTUM_RESULTS = "+json.dumps({"scan":json.loads(summary.to_json(orient="records")),"metadata":meta},indent=2)+";\n",
    encoding="utf-8")
build_dashboard_data()
print(json.dumps(meta,indent=2)); print("Data:",DATA); print("Figures:",FIG)
