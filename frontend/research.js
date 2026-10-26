const runs = window.HARTREE_RUNS || [];
const runSelect = document.getElementById("research-run-select");
let scan = [];
let meta = {};

function fmt(x, digits=4){return Number(x).toFixed(digits)}
function svgChart(rows, valueKey, semKey, label){
  const W=740,H=270,p={l:62,r:20,t:18,b:42};
  const xs=rows.map(r=>Number(r.W_uniform));
  const extremes=rows.flatMap(r=>[Number(r[valueKey])-Number(r[semKey]||0),Number(r[valueKey])+Number(r[semKey]||0)]);
  let lo=Math.min(...extremes),hi=Math.max(...extremes); if(hi-lo<1e-9){lo-=.05;hi+=.05}else{const pad=(hi-lo)*.14;lo-=pad;hi+=pad}
  const x=v=>p.l+(v/1.2)*(W-p.l-p.r),y=v=>p.t+(hi-v)/(hi-lo)*(H-p.t-p.b);
  const ticks=Array.from({length:5},(_,i)=>lo+(hi-lo)*i/4);
  const grid=ticks.map(v=>`<line x1="${p.l}" y1="${y(v)}" x2="${W-p.r}" y2="${y(v)}" stroke="#264447"/><text x="${p.l-8}" y="${y(v)+4}" text-anchor="end" fill="#91a9a4" font-size="10">${v.toFixed(2)}</text>`).join("");
  const zero=lo<0&&hi>0?`<line x1="${p.l}" y1="${y(0)}" x2="${W-p.r}" y2="${y(0)}" stroke="#e6bb73" stroke-dasharray="4 4"/>`:"";
  const points=rows.map(r=>`${x(Number(r.W_uniform))},${y(Number(r[valueKey]))}`).join(" ");
  const marks=rows.map(r=>{const xv=x(Number(r.W_uniform)),yv=y(Number(r[valueKey])),err=Number(r[semKey]||0);return `<g><title>W/t=${fmt(r.W_uniform,1)}; ${label}=${fmt(r[valueKey])} ± ${fmt(err)} SEM; n=${r.samples}</title><line x1="${xv}" y1="${y(Number(r[valueKey])+err)}" x2="${xv}" y2="${y(Number(r[valueKey])-err)}" stroke="#74d5b3" stroke-width="2"/><circle cx="${xv}" cy="${yv}" r="5" fill="#74d5b3" stroke="#091719" stroke-width="2"/></g>`}).join("");
  const xt=[0,.3,.6,.9,1.2].map(v=>`<text x="${x(v)}" y="${H-13}" text-anchor="middle" fill="#91a9a4" font-size="10">${v.toFixed(1)}</text>`).join("");
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${label} against disorder"><text x="${W/2}" y="${H-1}" text-anchor="middle" fill="#91a9a4" font-size="10">DISORDER WIDTH W/t</text>${grid}${zero}<polyline points="${points}" fill="none" stroke="#74d5b3" stroke-width="2.5"/>${marks}${xt}</svg>`;
}
function fill(){
  const L=Number(document.getElementById("size-select").value),tp=Number(document.getElementById("tp-select").value);
  const rows=scan.filter(r=>Number(r.L)===L&&Number(r.t_prime)===tp).sort((a,b)=>a.W_uniform-b.W_uniform);
  document.getElementById("pair-chart").innerHTML=svgChart(rows,"mean_pairing","sem_pairing","pairing");
  document.getElementById("stiffness-chart").innerHTML=svgChart(rows,"mean_twist_curvature","sem_twist_curvature","twist curvature");
  document.getElementById("table").innerHTML=rows.map(r=>`<tr><td>${fmt(r.W_uniform,1)}</td><td>${fmt(r.mean_pairing)}</td><td>${fmt(r.sem_pairing)}</td><td>${fmt(r.mean_twist_curvature)}</td><td>${fmt(r.sem_twist_curvature)}</td><td>${fmt(r.mean_density)}</td><td>${r.samples}</td></tr>`).join("");
}
function loadRun(run, preferredSize) {
  scan = run.scan;
  meta = run.metadata;
  const sizes = [...new Set(scan.map(row => Number(row.L)))].sort((a,b) => a-b);
  const hoppings = [...new Set(scan.map(row => Number(row.t_prime)))].sort((a,b) => a-b);
  const sizeSelect = document.getElementById("size-select");
  const tpSelect = document.getElementById("tp-select");
  sizeSelect.innerHTML = sizes.map(size => `<option value="${size}">L = ${size}</option>`).join("");
  tpSelect.innerHTML = hoppings.map(value => `<option value="${value}">t'/t = ${value.toFixed(1)}</option>`).join("");
  sizeSelect.value = sizes.includes(Number(preferredSize)) ? preferredSize : sizes[0];
  document.getElementById("solves").textContent = meta.successful_calculations;
  document.getElementById("failures").textContent = meta.failed_calculations;
  document.getElementById("density").textContent = fmt(meta.parameters.target_density,3);
  document.getElementById("density-error").textContent = fmt(Math.max(...scan.map(row => Number(row.max_density_residual))),2);
  document.getElementById("run-id").textContent = `${meta.run_id} · ${meta.parameters.realizations} samples/point · ${meta.parameters.phase_seeds} phase starts · δ=${meta.parameters.twist_step}`;
  document.getElementById("footer-run").textContent = meta.run_id;
  fill();
}

if (runs.length) {
  runSelect.innerHTML = runs.map(run => `<option value="${run.id}">${run.id} · ${run.metadata.parameters.realizations} samples/point</option>`).join("");
  const preferred = runs.find(run => run.id === "research_hartree_robust_20261023") || runs.at(-1);
  runSelect.value = preferred.id;
  loadRun(preferred, 4);
  runSelect.addEventListener("change", () => loadRun(runs.find(run => run.id === runSelect.value), Number(document.getElementById("size-select").value)));
  document.getElementById("size-select").addEventListener("change",fill);
  document.getElementById("tp-select").addEventListener("change",fill);
} else {
  document.getElementById("pair-chart").textContent = "No Hartree research runs are bundled.";
}
