const phaseSizePayload=window.HARTREE_PHASE_SIZE;
const phaseSizeMeta=phaseSizePayload.metadata;
const phaseSizeSummary=phaseSizePayload.summary;
const phaseEffects=phaseSizePayload.phase_effects;

function phaseChart(series,label) {
  const entries=series.flatMap(s=>s.rows.filter(r=>r.mean_twist_curvature!=null)
    .map(r=>({L:Number(r.L),value:Number(r.mean_twist_curvature),
      sem:Number(r.sem_twist_curvature||0),samples:Number(r.samples),name:s.name,color:s.color})));
  if(!entries.length)return '<p class="empty-chart">No completed points for this comparison.</p>';
  const W=640,H=250,p={l:62,r:18,t:20,b:44};
  let xlo=Math.min(...entries.map(r=>r.L)),xhi=Math.max(...entries.map(r=>r.L));
  if(xlo===xhi){xlo-=.5;xhi+=.5}
  let ylo=Math.min(...entries.map(r=>r.value-r.sem)),yhi=Math.max(...entries.map(r=>r.value+r.sem));
  if(yhi-ylo<1e-12){ylo-=.05;yhi+=.05}else{const pad=(yhi-ylo)*.16;ylo-=pad;yhi+=pad}
  const x=v=>p.l+(v-xlo)/(xhi-xlo)*(W-p.l-p.r);
  const y=v=>p.t+(yhi-v)/(yhi-ylo)*(H-p.t-p.b);
  const grid=Array.from({length:5},(_,i)=>{const v=ylo+(yhi-ylo)*i/4;return `<line x1="${p.l}" y1="${y(v)}" x2="${W-p.r}" y2="${y(v)}" stroke="#264447"/><text x="${p.l-8}" y="${y(v)+4}" text-anchor="end" fill="#91a9a4" font-size="10">${v.toFixed(3)}</text>`}).join('');
  const zero=ylo<0&&yhi>0?`<line x1="${p.l}" y1="${y(0)}" x2="${W-p.r}" y2="${y(0)}" stroke="#e6bb73" stroke-dasharray="4 4"/>`:'';
  const marks=series.map(s=>{
    const rows=entries.filter(r=>r.name===s.name).sort((a,b)=>a.L-b.L);
    const path=rows.map((r,i)=>`${i?'L':'M'}${x(r.L)},${y(r.value)}`).join(' ');
    return `<path d="${path}" fill="none" stroke="${s.color}" stroke-width="2.4"/>`+rows.map(r=>`<g><title>L=${r.L}; ${label}=${r.value.toFixed(5)} ± ${r.sem.toFixed(5)} SEM; n=${r.samples}; ${r.name}</title><line x1="${x(r.L)}" y1="${y(r.value+r.sem)}" x2="${x(r.L)}" y2="${y(r.value-r.sem)}" stroke="${s.color}" stroke-width="2"/><circle cx="${x(r.L)}" cy="${y(r.value)}" r="4.5" fill="${s.color}" stroke="#091719" stroke-width="2"/></g>`).join('');
  }).join('');
  const xt=[...new Set(entries.map(r=>r.L))].sort((a,b)=>a-b).map(v=>`<text x="${x(v)}" y="${H-17}" text-anchor="middle" fill="#91a9a4" font-size="10">${v}</text>`).join('');
  const legend=series.map((s,i)=>`<g transform="translate(${p.l+i*112},10)"><line x1="0" y1="0" x2="15" y2="0" stroke="${s.color}" stroke-width="2.5"/><text x="20" y="4" fill="#91a9a4" font-size="10">${s.name}</text></g>`).join('');
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${label} against lattice size">${legend}${grid}${zero}${marks}${xt}<text x="${W/2}" y="${H-2}" text-anchor="middle" fill="#91a9a4" font-size="10">LINEAR LATTICE SIZE L</text></svg>`;
}

function phaseEffectChart(rows) {
  const valid=rows.filter(r=>r.mean_curvature_change!=null);
  if(!valid.length)return '<p class="empty-chart">No paired phase-start results available.</p>';
  const W=640,H=250,p={l:62,r:18,t:20,b:44};
  const Ls=valid.map(r=>Number(r.L));let xlo=Math.min(...Ls),xhi=Math.max(...Ls);
  if(xlo===xhi){xlo-=.5;xhi+=.5}
  let lo=Math.min(0,...valid.map(r=>Number(r.mean_curvature_change)-Number(r.sem_curvature_change||0)));
  let hi=Math.max(0,...valid.map(r=>Number(r.mean_curvature_change)+Number(r.sem_curvature_change||0)));
  if(hi-lo<1e-12){lo-=.05;hi+=.05}else{const pad=(hi-lo)*.18;lo-=pad;hi+=pad}
  const x=v=>p.l+(v-xlo)/(xhi-xlo)*(W-p.l-p.r),y=v=>p.t+(hi-v)/(hi-lo)*(H-p.t-p.b);
  const grid=Array.from({length:5},(_,i)=>{const v=lo+(hi-lo)*i/4;return `<line x1="${p.l}" y1="${y(v)}" x2="${W-p.r}" y2="${y(v)}" stroke="#264447"/><text x="${p.l-8}" y="${y(v)+4}" text-anchor="end" fill="#91a9a4" font-size="10">${v.toFixed(3)}</text>`}).join('');
  const sortedRows=valid.slice().sort((a,b)=>a.L-b.L),path=sortedRows.map((r,i)=>`${i?'L':'M'}${x(Number(r.L))},${y(Number(r.mean_curvature_change))}`).join(' ');
  const marks=sortedRows.map(r=>{const xv=x(Number(r.L)),v=Number(r.mean_curvature_change),e=Number(r.sem_curvature_change||0);return `<g><title>L=${r.L}; four-start minus one-start curvature=${v.toFixed(5)} ± ${e.toFixed(5)} SEM; paired n=${r.samples}</title><line x1="${xv}" y1="${y(v+e)}" x2="${xv}" y2="${y(v-e)}" stroke="#d59b5a" stroke-width="2"/><circle cx="${xv}" cy="${y(v)}" r="4.5" fill="#d59b5a" stroke="#091719" stroke-width="2"/></g>`}).join('');
  const xt=[...new Set(Ls)].sort((a,b)=>a-b).map(v=>`<text x="${x(v)}" y="${H-17}" text-anchor="middle" fill="#91a9a4" font-size="10">${v}</text>`).join('');
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Paired change in curvature due to adding phase starts"><line x1="${p.l}" y1="${y(0)}" x2="${W-p.r}" y2="${y(0)}" stroke="#e6bb73" stroke-dasharray="4 4"/>${grid}<path d="${path}" fill="none" stroke="#d59b5a" stroke-width="2.4"/>${marks}${xt}<text x="${W/2}" y="${H-2}" text-anchor="middle" fill="#91a9a4" font-size="10">LINEAR LATTICE SIZE L</text></svg>`;
}

const highSeedCount=Math.max(...phaseSizeMeta.parameters.phase_seed_counts);
document.getElementById('phase-size-chart').innerHTML=phaseChart([
  {name:'1 start',color:'#74d5b3',rows:phaseSizeSummary.filter(r=>Number(r.phase_seeds)===1)},
  {name:`${highSeedCount} starts`,color:'#d59b5a',rows:phaseSizeSummary.filter(r=>Number(r.phase_seeds)===highSeedCount)}
],'mean twist curvature / t');
document.getElementById('phase-effect-chart').innerHTML=phaseEffectChart(phaseEffects);
document.getElementById('phase-size-status').textContent=
  `Run ${phaseSizeMeta.run_id}: ${phaseSizeMeta.successful_calculations}/${phaseSizeMeta.planned_calculations} calculations complete; ${phaseSizeMeta.failed_calculations} failed. `+
  `Largest mean-density residual: ${Number(phaseSizeMeta.max_density_residual).toExponential(2)}.`;
const root=`../results/data/${phaseSizeMeta.run_id}/`;
document.getElementById('phase-size-raw-link').href=`${root}phase_size_realizations.csv`;
document.getElementById('phase-size-summary-link').href=`${root}phase_size_summary.csv`;
document.getElementById('phase-size-effect-link').href=`${root}phase_start_sensitivity.csv`;
document.getElementById('phase-size-metadata-link').href=`${root}run_metadata.json`;
const cell=(value,format)=>value==null?'—':format(Number(value));
document.getElementById('phase-size-rows').innerHTML=phaseSizeSummary.map(r=>
  `<tr><td>${r.L}</td><td>${r.phase_seeds}</td><td>${r.samples}</td><td>${cell(r.mean_pairing,v=>v.toFixed(5))}</td><td>${cell(r.sem_pairing,v=>v.toFixed(5))}</td><td>${cell(r.mean_twist_curvature,v=>v.toFixed(5))}</td><td>${cell(r.sem_twist_curvature,v=>v.toFixed(5))}</td><td>${cell(r.max_density_residual,v=>v.toExponential(2))}</td></tr>`).join('');
