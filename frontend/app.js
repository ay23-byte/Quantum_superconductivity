const scan = window.QUANTUM_RESULTS.scan;
const metadata = window.QUANTUM_RESULTS.metadata;
const parameters = metadata.parameters;

const figures = [
  ["dispersion","Square-lattice band","NORMAL-STATE DISPERSION"],
  ["gap_vs_temperature","Pairing vs temperature","UNIFORM BCS REFERENCE"],
  ["gap_vs_interaction","Pairing vs attraction","UNIFORM BCS REFERENCE"],
  ["bdg_spectrum","Signed quasiparticle spectrum","CLEAN BDG"],
  ["dos_clean_disordered","Electron density of states","CLEAN / DISORDERED"],
  ["disorder_map","Onsite potential map","W/t = 1.2 · ONE REALIZATION"],
  ["gap_map","Self-consistent pairing map","W/t = 1.2 · ONE REALIZATION"],
  ["mean_gap_vs_disorder_tp0","Pairing vs disorder","t′/t = 0.0 · ± SEM"],
  ["mean_gap_vs_disorder_tp0.2","Pairing vs disorder","t′/t = 0.2 · ± SEM"],
  ["inhomogeneity_vs_disorder_tp0","Pairing inhomogeneity","t′/t = 0.0"],
  ["inhomogeneity_vs_disorder_tp0.2","Pairing inhomogeneity","t′/t = 0.2"],
  ["hopping_disorder_heatmap","Hopping × disorder scan","MEAN PAIRING AMPLITUDE"],
  ["convergence_residual","Self-consistency residual","ONE DISORDER REALIZATION"],
  ["finite_size_comparison","Clean finite-size comparison","CLEAN L = 4, 6, 8"],
  ["finite_size_disorder_comparison","Disordered finite-size comparison","W/t = 1.2 · L = 4, 6, 8"]
];
const figRoot=`../results/figures/${window.QUANTUM_RESULTS.metadata.run_id}/`;

function fmt(x){return Number(x).toFixed(5)}
function drawChart(rows){
  const box=document.getElementById("pairing-chart"), W=760,H=290,p={l:58,r:22,t:16,b:42};
  const vals=rows.flatMap(d=>[d.mean-d.sem,d.mean+d.sem]);
  const lo=Math.floor((Math.min(...vals)-.01)*100)/100, hi=Math.ceil((Math.max(...vals)+.01)*100)/100;
  const x=v=>p.l+(v/1.2)*(W-p.l-p.r), y=v=>p.t+(hi-v)/(hi-lo)*(H-p.t-p.b);
  const ticks=5, yGrid=Array.from({length:ticks+1},(_,i)=>lo+(hi-lo)*i/ticks);
  const grid=yGrid.map(v=>`<line x1="${p.l}" y1="${y(v)}" x2="${W-p.r}" y2="${y(v)}" stroke="#edf1ed"/><text x="${p.l-10}" y="${y(v)+3}" text-anchor="end" fill="#8a9793" font-size="10" font-family="DM Mono,monospace">${v.toFixed(2)}</text>`).join("");
  const xTicks=[0,.3,.6,.9,1.2].map(v=>`<line x1="${x(v)}" y1="${H-p.b}" x2="${x(v)}" y2="${H-p.b+4}" stroke="#9daaa5"/><text x="${x(v)}" y="${H-p.b+18}" text-anchor="middle" fill="#8a9793" font-size="10" font-family="DM Mono,monospace">${v.toFixed(1)}</text>`).join("");
  const path=rows.map((d,i)=>`${i?"L":"M"}${x(d.W)},${y(d.mean)}`).join(" ");
  const marks=rows.map(d=>`<g class="chart-mark" tabindex="0"><title>W/t ${d.W.toFixed(1)}: mean ${fmt(d.mean)} ± ${fmt(d.sem)} SEM; spatial SD ${fmt(d.inhomogeneity)}</title><line x1="${x(d.W)}" y1="${y(d.mean-d.sem)}" x2="${x(d.W)}" y2="${y(d.mean+d.sem)}" stroke="#85aaa0" stroke-width="2"/><line x1="${x(d.W)-5}" y1="${y(d.mean-d.sem)}" x2="${x(d.W)+5}" y2="${y(d.mean-d.sem)}" stroke="#85aaa0"/><line x1="${x(d.W)-5}" y1="${y(d.mean+d.sem)}" x2="${x(d.W)+5}" y2="${y(d.mean+d.sem)}" stroke="#85aaa0"/><circle cx="${x(d.W)}" cy="${y(d.mean)}" r="5" fill="#0b7469" stroke="white" stroke-width="2"/></g>`).join("");
  box.innerHTML=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Mean pairing amplitude with standard error bars"><defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#72bca1" stop-opacity=".19"/><stop offset="1" stop-color="#72bca1" stop-opacity="0"/></linearGradient></defs>${grid}<path d="${path} L${x(rows.at(-1).W)},${H-p.b} L${x(rows[0].W)},${H-p.b} Z" fill="url(#area)"/><path d="${path}" fill="none" stroke="#0b7469" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>${marks}${xTicks}<text x="${(p.l+W-p.r)/2}" y="${H-5}" text-anchor="middle" fill="#6f817c" font-size="10" font-family="DM Mono,monospace">UNIFORM DISORDER WIDTH W / t</text><text transform="translate(15 ${(H-p.b+p.t)/2}) rotate(-90)" text-anchor="middle" fill="#6f817c" font-size="10" font-family="DM Mono,monospace">MEAN |Δᵢ| / t</text></svg>`;
}
function render(){
  const tp=Number(document.getElementById("hopping-select").value), rows=scan.filter(d=>d.t_prime===tp).map(d=>({W:d.W_uniform,mean:d.mean_pairing,sem:d.sem_pairing,inhomogeneity:d.mean_spatial_std,converged:d.converged_samples,samples:d.samples}));
  drawChart(rows);
  const n=scan.find(d=>d.t_prime===tp).samples;
  document.getElementById("chart-samples").textContent=n;
  document.getElementById("sample-badge").textContent=`${n} REALIZATIONS / POINT`;
  document.getElementById("scan-scope").textContent=`${rows.length} × ${new Set(scan.map(d=>d.t_prime)).size} × ${n}`;
  document.getElementById("lattice-size").textContent=`${parameters.L} \u00D7 ${parameters.L}`;
  document.getElementById("interaction-strength").textContent=`U/t = ${Number(parameters.U).toFixed(1)}`;
  document.getElementById("temperature").textContent=`T/t = ${Number(parameters.T).toFixed(2)}`;
  document.getElementById("run-converged").textContent=metadata.all_unique_runs_converged?`${metadata.unique_solver_runs} / ${metadata.unique_solver_runs}`:"Check metadata";
  document.getElementById("gallery-count").textContent=`${figures.length} FIGURES · PNG + PDF`;
  document.getElementById("result-rows").innerHTML=rows.map(d=>`<tr><td>${d.W.toFixed(1)}</td><td>${fmt(d.mean)}</td><td>${d.sem===0?"—":fmt(d.sem)}</td><td>${fmt(d.inhomogeneity)}</td><td><span class="converged">${d.converged} / ${d.samples} ✓</span></td></tr>`).join("");
  const clean=rows[0].mean,last=rows.at(-1);
  document.getElementById("max-gap").textContent=fmt(last.mean);
  const delta=((last.mean-clean)/clean)*100;
  document.getElementById("max-delta").textContent=`${delta>=0?"+":""}${delta.toFixed(1)}%`;
  document.getElementById("inhomogeneity").textContent=fmt(last.inhomogeneity);
  const maxInhom=Math.max(...rows.map(d=>d.inhomogeneity),1e-12);
  document.getElementById("inhom-bars").innerHTML=rows.map(d=>`<i title="W/t=${d.W.toFixed(1)} · spatial SD ${fmt(d.inhomogeneity)}" style="height:${Math.max(5,d.inhomogeneity/maxInhom*100)}%"></i>`).join("");
}
function buildGallery(){
  const root=document.getElementById("figure-gallery");
  root.innerHTML=figures.map(([name,title,tag])=>`<article class="figure-item"><a class="figure-link" href="${figRoot}${name}.png" target="_blank" rel="noreferrer"><div class="figure-thumb"><img loading="lazy" src="${figRoot}${name}.png" alt="${title} scientific figure"></div></a><div class="figure-caption"><strong>${title}</strong><div><span>${tag}</span><a href="${figRoot}${name}.pdf" target="_blank" rel="noreferrer">PDF ↗</a></div></div></article>`).join("");
}
document.getElementById("hopping-select").addEventListener("change",render);
buildGallery();render();
