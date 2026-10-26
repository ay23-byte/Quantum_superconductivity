const runs = window.QUANTUM_RUNS || [];
const runSelect = document.getElementById("run-select");
const hoppingSelect = document.getElementById("hopping-select");
const minSelect = document.getElementById("disorder-min");
const maxSelect = document.getElementById("disorder-max");

const figures = [
  ["dispersion","Square-lattice band","NORMAL-STATE DISPERSION"],
  ["gap_vs_temperature","Pairing vs temperature","UNIFORM BCS REFERENCE"],
  ["gap_vs_interaction","Pairing vs attraction","UNIFORM BCS REFERENCE"],
  ["bdg_spectrum","Signed quasiparticle spectrum","CLEAN BDG"],
  ["dos_clean_disordered","Electron density of states","CLEAN / DISORDERED"],
  ["disorder_map","Onsite potential map","ONE REALIZATION"],
  ["gap_map","Self-consistent pairing map","ONE REALIZATION"],
  ["mean_gap_vs_disorder_tp0","Pairing vs disorder","t′/t = 0.0 · ± SEM"],
  ["mean_gap_vs_disorder_tp0.2","Pairing vs disorder","t′/t = 0.2 · ± SEM"],
  ["inhomogeneity_vs_disorder_tp0","Pairing inhomogeneity","t′/t = 0.0"],
  ["inhomogeneity_vs_disorder_tp0.2","Pairing inhomogeneity","t′/t = 0.2"],
  ["hopping_disorder_heatmap","Hopping × disorder scan","MEAN PAIRING AMPLITUDE"],
  ["convergence_residual","Self-consistency residual","ONE DISORDER REALIZATION"],
  ["finite_size_comparison","Clean finite-size comparison","CLEAN L = 4, 6, 8"],
  ["finite_size_disorder_comparison","Disordered finite-size comparison","W/t = 1.2 · L = 4, 6, 8"]
];

function fmt(value) { return Number(value).toFixed(5); }
function currentRun() { return runs.find(run => run.id === runSelect.value) || runs[0]; }

function fillSelect(select, values, label) {
  select.innerHTML = values.map(value => `<option value="${value}">${label(value)}</option>`).join("");
}

function updateRunControls(run, preserveHopping = false) {
  const hoppingBefore = hoppingSelect.value;
  const hoppings = [...new Set(run.scan.map(row => row.t_prime))].sort((a, b) => a - b);
  const disorders = [...new Set(run.scan.map(row => row.W_uniform))].sort((a, b) => a - b);
  fillSelect(hoppingSelect, hoppings, value => `t′ / t = ${Number(value).toFixed(1)}`);
  if (preserveHopping && hoppings.includes(Number(hoppingBefore))) hoppingSelect.value = hoppingBefore;
  fillSelect(minSelect, disorders, value => Number(value).toFixed(1));
  fillSelect(maxSelect, disorders, value => Number(value).toFixed(1));
  minSelect.value = disorders[0];
  maxSelect.value = disorders.at(-1);
}

function drawChart(rows) {
  const box = document.getElementById("pairing-chart");
  if (!rows.length) {
    box.innerHTML = '<p class="empty-chart">No results match these filters.</p>';
    return;
  }
  const W = 760, H = 290, p = { l: 58, r: 22, t: 16, b: 42 };
  const vals = rows.flatMap(d => [d.mean - d.sem, d.mean + d.sem]);
  let lo = Math.min(...vals), hi = Math.max(...vals);
  if (hi - lo < 1e-9) { lo -= .02; hi += .02; }
  else { const pad = (hi - lo) * .16; lo -= pad; hi += pad; }
  const minW = Number(minSelect.value), maxW = Number(maxSelect.value);
  let xLo = minW, xHi = maxW;
  if (xHi - xLo < 1e-9) { xLo -= .1; xHi += .1; }
  const x = value => p.l + (value - xLo) / (xHi - xLo) * (W - p.l - p.r);
  const y = value => p.t + (hi - value) / (hi - lo) * (H - p.t - p.b);
  const yGrid = Array.from({ length: 6 }, (_, i) => lo + (hi - lo) * i / 5);
  const grid = yGrid.map(value => `<line x1="${p.l}" y1="${y(value)}" x2="${W-p.r}" y2="${y(value)}" stroke="#edf1ed"/><text x="${p.l-10}" y="${y(value)+3}" text-anchor="end" fill="#8a9793" font-size="10" font-family="DM Mono,monospace">${value.toFixed(2)}</text>`).join("");
  const xTicks = Array.from({ length: 5 }, (_, i) => xLo + (xHi - xLo) * i / 4).map(value => `<line x1="${x(value)}" y1="${H-p.b}" x2="${x(value)}" y2="${H-p.b+4}" stroke="#9daaa5"/><text x="${x(value)}" y="${H-p.b+18}" text-anchor="middle" fill="#8a9793" font-size="10" font-family="DM Mono,monospace">${value.toFixed(1)}</text>`).join("");
  const path = rows.map((d, i) => `${i ? "L" : "M"}${x(d.W)},${y(d.mean)}`).join(" ");
  const marks = rows.map(d => `<g class="chart-mark" tabindex="0"><title>W/t ${d.W.toFixed(1)}: mean ${fmt(d.mean)} ± ${fmt(d.sem)} SEM; spatial SD ${fmt(d.inhomogeneity)}</title><line x1="${x(d.W)}" y1="${y(d.mean-d.sem)}" x2="${x(d.W)}" y2="${y(d.mean+d.sem)}" stroke="#85aaa0" stroke-width="2"/><line x1="${x(d.W)-5}" y1="${y(d.mean-d.sem)}" x2="${x(d.W)+5}" y2="${y(d.mean-d.sem)}" stroke="#85aaa0"/><line x1="${x(d.W)-5}" y1="${y(d.mean+d.sem)}" x2="${x(d.W)+5}" y2="${y(d.mean+d.sem)}" stroke="#85aaa0"/><circle cx="${x(d.W)}" cy="${y(d.mean)}" r="5" fill="#0b7469" stroke="white" stroke-width="2"/></g>`).join("");
  const area = rows.length > 1 ? `<path d="${path} L${x(rows.at(-1).W)},${H-p.b} L${x(rows[0].W)},${H-p.b} Z" fill="url(#area)"/>` : "";
  box.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Mean pairing amplitude with standard error bars"><defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#72bca1" stop-opacity=".19"/><stop offset="1" stop-color="#72bca1" stop-opacity="0"/></linearGradient></defs>${grid}${area}<path d="${path}" fill="none" stroke="#0b7469" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>${marks}${xTicks}<text x="${(p.l+W-p.r)/2}" y="${H-5}" text-anchor="middle" fill="#6f817c" font-size="10" font-family="DM Mono,monospace">UNIFORM DISORDER WIDTH W / t</text><text transform="translate(15 ${(H-p.b+p.t)/2}) rotate(-90)" text-anchor="middle" fill="#6f817c" font-size="10" font-family="DM Mono,monospace">MEAN |Δᵢ| / t</text></svg>`;
}

function render() {
  const run = currentRun();
  const metadata = run.metadata;
  const parameters = metadata.parameters;
  const tp = Number(hoppingSelect.value);
  const minW = Number(minSelect.value), maxW = Number(maxSelect.value);
  const rows = run.scan.filter(row => row.t_prime === tp && row.W_uniform >= minW && row.W_uniform <= maxW)
    .sort((a, b) => a.W_uniform - b.W_uniform)
    .map(row => ({ W: row.W_uniform, mean: row.mean_pairing, sem: row.sem_pairing,
      inhomogeneity: row.mean_spatial_std, converged: row.converged_samples, samples: row.samples }));
  drawChart(rows);
  if (rows.length) {
    const n = rows[0].samples;
    document.getElementById("chart-samples").textContent = n;
    document.getElementById("sample-badge").textContent = `${n} REALIZATIONS / POINT`;
    document.getElementById("result-rows").innerHTML = rows.map(row => `<tr><td>${row.W.toFixed(1)}</td><td>${fmt(row.mean)}</td><td>${row.sem === 0 ? "—" : fmt(row.sem)}</td><td>${fmt(row.inhomogeneity)}</td><td><span class="converged">${row.converged} / ${row.samples} ✓</span></td></tr>`).join("");
    const first = rows[0], last = rows.at(-1);
    document.getElementById("max-gap").textContent = fmt(last.mean);
    document.getElementById("max-gap-label").textContent = `mean |Δᵢ| / t at W/t = ${last.W.toFixed(1)}`;
    const delta = first.mean ? ((last.mean - first.mean) / first.mean) * 100 : 0;
    document.getElementById("max-delta").textContent = `${delta >= 0 ? "+" : ""}${delta.toFixed(1)}%`;
    document.getElementById("inhomogeneity").textContent = fmt(last.inhomogeneity);
    document.getElementById("inhomogeneity-label").textContent = `spatial SD of |Δᵢ| / t at W/t = ${last.W.toFixed(1)}`;
    const maxInhom = Math.max(...rows.map(row => row.inhomogeneity), 1e-12);
    document.getElementById("inhom-bars").innerHTML = rows.map(row => `<i title="W/t=${row.W.toFixed(1)} · spatial SD ${fmt(row.inhomogeneity)}" style="height:${Math.max(5, row.inhomogeneity / maxInhom * 100)}%"></i>`).join("");
  } else {
    document.getElementById("result-rows").innerHTML = '<tr><td colspan="5">No results match these filters.</td></tr>';
  }

  const allHoppings = [...new Set(run.scan.map(row => row.t_prime))];
  document.getElementById("scan-scope").textContent = `${rows.length} disorder points · ${allHoppings.length} hopping values · ${rows[0]?.samples ?? "—"} samples`;
  document.getElementById("lattice-size").textContent = `${parameters.L} × ${parameters.L}`;
  document.getElementById("interaction-strength").textContent = `U/t = ${Number(parameters.U).toFixed(1)}`;
  document.getElementById("temperature").textContent = `T/t = ${Number(parameters.T).toFixed(2)}`;
  const converged = metadata.all_unique_runs_converged;
  document.getElementById("run-converged").textContent = converged ? `${metadata.unique_solver_runs} / ${metadata.unique_solver_runs}` : "Check metadata";
  document.getElementById("gallery-count").textContent = `${run.figures.length} FIGURES · PNG + PDF`;
  document.getElementById("run-name").textContent = run.id;
  document.getElementById("run-metadata-link").href = `../results/data/${run.id}/run_metadata.json`;
  buildGallery(run);
}

function buildGallery(run) {
  const available = new Set(run.figures);
  const root = document.getElementById("figure-gallery");
  root.innerHTML = figures.filter(([name]) => available.has(name)).map(([name, title, tag]) => `<article class="figure-item"><a class="figure-link" href="../results/figures/${run.id}/${name}.png" target="_blank" rel="noreferrer"><div class="figure-thumb"><img loading="lazy" src="../results/figures/${run.id}/${name}.png" alt="${title} scientific figure"></div></a><div class="figure-caption"><strong>${title}</strong><div><span>${tag}</span><a href="../results/figures/${run.id}/${name}.pdf" target="_blank" rel="noreferrer">PDF ↗</a></div></div></article>`).join("");
}

if (!runs.length) {
  document.getElementById("pairing-chart").textContent = "No bundled scan data is available.";
} else {
  const preferred = runs.find(run => run.id === "user_simulation_20261023") || runs[0];
  runSelect.innerHTML = runs.map(run => `<option value="${run.id}">${run.id} · ${run.metadata.parameters.realizations_per_pair} samples/point</option>`).join("");
  runSelect.value = preferred.id;
  updateRunControls(preferred);
  runSelect.addEventListener("change", () => { updateRunControls(currentRun()); render(); });
  hoppingSelect.addEventListener("change", render);
  minSelect.addEventListener("change", () => {
    if (Number(minSelect.value) > Number(maxSelect.value)) maxSelect.value = minSelect.value;
    render();
  });
  maxSelect.addEventListener("change", () => {
    if (Number(maxSelect.value) < Number(minSelect.value)) minSelect.value = maxSelect.value;
    render();
  });
  render();
}
