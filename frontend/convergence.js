const convergence = window.HARTREE_CONVERGENCE;
const convergenceMeta = convergence.metadata;
const convergenceStats = convergence.statistics;
const sampleCounts = convergence.sample_counts;
const twistComparisons = convergence.twist_comparisons;

function convergenceChart(rows, xKey, yKey, semKey, xLabel, yLabel) {
  const valid = rows.filter(r => r[xKey] != null && r[yKey] != null
    && Number.isFinite(Number(r[xKey])) && Number.isFinite(Number(r[yKey])))
    .sort((a,b)=>Number(a[xKey])-Number(b[xKey]));
  if (!valid.length) return '<p class="empty-chart">No completed points for this comparison.</p>';
  const W=640,H=250,p={l:62,r:18,t:18,b:44};
  const xv=valid.map(r=>Number(r[xKey]));
  const ext=valid.flatMap(r=>{
    const value=Number(r[yKey]),err=Number(r[semKey]||0);
    return [value-err,value+err];
  });
  let xlo=Math.min(...xv),xhi=Math.max(...xv);
  if(xhi===xlo){xlo-=.5;xhi+=.5}
  let ylo=Math.min(...ext),yhi=Math.max(...ext);
  if(yhi-ylo<1e-12){ylo-=.05;yhi+=.05}else{const pad=(yhi-ylo)*.15;ylo-=pad;yhi+=pad}
  const x=v=>p.l+(v-xlo)/(xhi-xlo)*(W-p.l-p.r);
  const y=v=>p.t+(yhi-v)/(yhi-ylo)*(H-p.t-p.b);
  const grid=Array.from({length:5},(_,i)=>{
    const val=ylo+(yhi-ylo)*i/4;
    return `<line x1="${p.l}" y1="${y(val)}" x2="${W-p.r}" y2="${y(val)}" stroke="#264447"/><text x="${p.l-8}" y="${y(val)+4}" text-anchor="end" fill="#91a9a4" font-size="10">${val.toFixed(3)}</text>`;
  }).join("");
  const path=valid.map((r,i)=>`${i?'L':'M'}${x(Number(r[xKey]))},${y(Number(r[yKey]))}`).join(' ');
  const marks=valid.map(r=>{
    const xv0=x(Number(r[xKey])),yv0=y(Number(r[yKey])),err=Number(r[semKey]||0);
    return `<g><title>${xLabel}=${Number(r[xKey]).toPrecision(3)}; ${yLabel}=${Number(r[yKey]).toFixed(5)} ± ${err.toFixed(5)} SEM; n=${r.samples??'—'}</title><line x1="${xv0}" y1="${y(Number(r[yKey])+err)}" x2="${xv0}" y2="${y(Number(r[yKey])-err)}" stroke="#74d5b3" stroke-width="2"/><line x1="${xv0-5}" y1="${y(Number(r[yKey])+err)}" x2="${xv0+5}" y2="${y(Number(r[yKey])+err)}" stroke="#74d5b3"/><line x1="${xv0-5}" y1="${y(Number(r[yKey])-err)}" x2="${xv0+5}" y2="${y(Number(r[yKey])-err)}" stroke="#74d5b3"/><circle cx="${xv0}" cy="${yv0}" r="4.5" fill="#74d5b3" stroke="#091719" stroke-width="2"/></g>`;
  }).join('');
  const xticks=[...new Set(xv)].sort((a,b)=>a-b).map(v=>
    `<text x="${x(v)}" y="${H-17}" text-anchor="middle" fill="#91a9a4" font-size="10">${Number(v).toPrecision(3)}</text>`).join('');
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${yLabel} versus ${xLabel}">${grid}<path d="${path}" fill="none" stroke="#74d5b3" stroke-width="2.5"/>${marks}${xticks}<text x="${W/2}" y="${H-2}" text-anchor="middle" fill="#91a9a4" font-size="10">${xLabel.toUpperCase()}</text></svg>`;
}

function renderConvergence() {
  const L=Number(document.getElementById('convergence-size').value);
  const dataRoot=`../results/data/${convergenceMeta.run_id}/`;
  document.getElementById('convergence-realizations-link').href=`${dataRoot}convergence_realizations.csv`;
  document.getElementById('convergence-statistics-link').href=`${dataRoot}convergence_statistics.csv`;
  document.getElementById('convergence-samples-link').href=`${dataRoot}convergence_sample_counts.csv`;
  document.getElementById('convergence-metadata-link').href=`${dataRoot}run_metadata.json`;
  const maxSamples=Number(convergenceMeta.parameters.max_disorder_realizations);
  const minStep=Math.min(...convergenceMeta.parameters.twist_steps);
  const sizeRows=convergenceStats.filter(r=>Number(r.twist_step)===minStep
    && Number(r.samples)===maxSamples);
  document.getElementById('size-pairing-chart').innerHTML=convergenceChart(
    sizeRows,'L','mean_pairing','sem_pairing','lattice size L','mean pairing / t');
  document.getElementById('size-stiffness-chart').innerHTML=convergenceChart(
    sizeRows,'L','mean_twist_curvature','sem_twist_curvature','lattice size L','twist curvature / t');
  const samples=sampleCounts.filter(r=>Number(r.L)===L&&Number(r.twist_step)===minStep);
  document.getElementById('sample-count-chart').innerHTML=convergenceChart(
    samples,'samples','mean_twist_curvature','sem_twist_curvature','cumulative disorder samples','mean twist curvature / t');
  const matched=twistComparisons.filter(r=>Number(r.L)===L);
  document.getElementById('twist-step-chart').innerHTML=convergenceChart(
    matched,'twist_step','mean_twist_curvature','sem_twist_curvature','twist step delta','mean twist curvature / t');
  const completed=convergenceMeta.successful_calculations;
  const planned=convergenceMeta.planned_calculations;
  const matchedN=matched.length?Math.min(...matched.map(r=>Number(r.samples))):0;
  document.getElementById('sample-chart-note').textContent=
    `L=${L}; cumulative prefixes at delta=${minStep}; estimates are correlated`;
  document.getElementById('convergence-status').textContent=
    `Run ${convergenceMeta.run_id}: ${completed}/${planned} calculations complete; ${convergenceMeta.failed_calculations} failed. `+
    `Twist-step comparison uses ${matchedN} realizations matched across all tested steps. Largest recorded mean-density residual: ${Number(convergenceMeta.max_density_residual??NaN).toExponential(2)}.`;
  const cell=(value,format)=>value==null?'—':format(Number(value));
  document.getElementById('convergence-rows').innerHTML=convergenceStats.map(r=>
    `<tr><td>${r.L}</td><td>${Number(r.twist_step).toFixed(3)}</td><td>${r.samples}</td><td>${cell(r.mean_pairing,v=>v.toFixed(5))}</td><td>${cell(r.sem_pairing,v=>v.toFixed(5))}</td><td>${cell(r.mean_twist_curvature,v=>v.toFixed(5))}</td><td>${cell(r.sem_twist_curvature,v=>v.toFixed(5))}</td><td>${cell(r.max_density_residual,v=>v.toExponential(2))}</td></tr>`).join('');
}

const convergenceSizes=[...new Set(convergenceStats.map(r=>Number(r.L)))].sort((a,b)=>a-b);
document.getElementById('convergence-size').innerHTML=convergenceSizes.map(L=>
  `<option value="${L}">L = ${L}</option>`).join('');
document.getElementById('convergence-size').addEventListener('change',renderConvergence);
renderConvergence();
