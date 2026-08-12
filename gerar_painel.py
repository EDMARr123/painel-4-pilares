r"""
Gera painel.html a partir de dados.json — página única, autocontida
(CSS/JS inline), pronta pra publicar como Artifact.
"""

import json
import os

PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DADOS = os.path.join(PASTA_BASE, "dados.json")
CAMINHO_SAIDA = os.path.join(PASTA_BASE, "painel.html")

TEMPLATE = r"""<title>Painel 4 Pilares — Equipe GYN</title>
<style>
:root {
  --bg: #EEF1F4;
  --surface: #FFFFFF;
  --surface-2: #F5F7FA;
  --border: #E1E6EB;
  --ink: #10151C;
  --ink-soft: #5B6472;
  --ink-faint: #6B7684;
  --accent: #0E7C86;
  --accent-soft: #E4F4F3;
  --accent-ink: #063A3F;
  --accent-deep: #0B5158;
  --accent-deep-2: #128A93;
  --good: #1D9A5D;
  --good-soft: #E4F5EC;
  --warn: #B4740A;
  --warn-soft: #FBF0DC;
  --bad: #D33B3B;
  --bad-soft: #FBE7E7;
  --track: #E4E7EC;
  --shadow: 0 1px 2px rgba(16, 21, 28, 0.04), 0 8px 24px -12px rgba(16, 21, 28, 0.18);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0B1116;
    --surface: #131B22;
    --surface-2: #1A232B;
    --border: #253039;
    --ink: #EAF0F4;
    --ink-soft: #93A1AC;
    --ink-faint: #64707B;
    --accent: #4FD1C8;
    --accent-soft: #12302E;
    --accent-ink: #B6F1EB;
    --accent-deep: #0A3F44;
    --accent-deep-2: #1B6E74;
    --good: #3FC17F;
    --good-soft: #123625;
    --warn: #E0A63C;
    --warn-soft: #3A2C10;
    --bad: #F0645E;
    --bad-soft: #3A1616;
    --track: #253039;
    --shadow: 0 1px 2px rgba(0, 0, 0, 0.3), 0 12px 32px -16px rgba(0, 0, 0, 0.6);
  }
}
:root[data-theme="dark"] {
  --bg: #0B1116;
  --surface: #131B22;
  --surface-2: #1A232B;
  --border: #253039;
  --ink: #EAF0F4;
  --ink-soft: #93A1AC;
  --ink-faint: #64707B;
  --accent: #4FD1C8;
  --accent-soft: #12302E;
  --accent-ink: #B6F1EB;
  --accent-deep: #0A3F44;
  --accent-deep-2: #1B6E74;
  --good: #3FC17F;
  --good-soft: #123625;
  --warn: #E0A63C;
  --warn-soft: #3A2C10;
  --bad: #F0645E;
  --bad-soft: #3A1616;
  --track: #253039;
  --shadow: 0 1px 2px rgba(0, 0, 0, 0.3), 0 12px 32px -16px rgba(0, 0, 0, 0.6);
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.wrap {
  max-width: 1400px;
  margin: 0 auto;
  padding: 28px 20px 64px;
}

/* ---------- Header / summary ---------- */

header.top {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 22px;
}

.title-block h1 {
  margin: 0 0 4px;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.01em;
  text-wrap: balance;
}

.title-block p {
  margin: 0;
  color: var(--ink-soft);
  font-size: 14px;
}

.summary-strip {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.stat-pill {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px 16px;
  min-width: 108px;
  box-shadow: var(--shadow);
}

.stat-pill .n {
  font-size: 20px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
}

.stat-pill .l {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ink-faint);
  margin-top: 2px;
}

/* ---------- Filter tabs ---------- */

.tabs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 22px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 14px;
}

.tab {
  appearance: none;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--ink-soft);
  font: inherit;
  font-size: 13px;
  font-weight: 600;
  padding: 7px 14px;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}

.tab:hover { border-color: var(--accent); color: var(--accent); }

.tab.active {
  background: var(--accent-deep);
  border-color: var(--accent-deep);
  color: #fff;
}

.tab .count {
  opacity: 0.7;
  font-weight: 500;
  margin-left: 4px;
}

/* ---------- Resumo do time (mesmo card do vendedor, com totais somados) ---------- */

.resumo-time {
  max-width: 420px;
  margin-bottom: 22px;
}

.resumo-time .card {
  border-width: 2px;
  border-color: var(--accent);
}

/* ---------- Card grid ---------- */

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 18px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: var(--shadow);
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.card-head {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  flex: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 15px;
  color: #fff;
  letter-spacing: -0.02em;
}

.card-head .who { flex: 1; min-width: 0; }

.card-head h2 {
  margin: 0;
  font-size: 15.5px;
  font-weight: 800;
  letter-spacing: -0.005em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-head .meta {
  margin: 1px 0 0;
  font-size: 12px;
  color: var(--ink-faint);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.head-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: none;
}

.badge-pilares {
  font-size: 11.5px;
  font-weight: 800;
  padding: 4px 9px;
  border-radius: 999px;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.icon-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--ink-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex: none;
}
.icon-btn:hover { border-color: var(--accent); color: var(--accent); }
.icon-btn svg { width: 14px; height: 14px; }

/* ---------- Pilar rows ---------- */

.pilar {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 2px 8px;
  align-items: baseline;
}

.pilar .label {
  font-size: 11.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--ink-soft);
}

.pilar .pct {
  font-size: 15px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.pilar .track {
  grid-column: 1 / -1;
  height: 6px;
  border-radius: 999px;
  background: var(--track);
  overflow: hidden;
}

.pilar .fill { height: 100%; border-radius: 999px; }

.pilar .sub {
  grid-column: 1 / -1;
  font-size: 11px;
  color: var(--ink-faint);
  font-variant-numeric: tabular-nums;
}

.pilares-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* ---------- Tendência ---------- */

.box-tendencia {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 14px;
}

.box-tendencia .top-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 6px;
}

.box-tendencia .label {
  font-size: 11.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--ink-soft);
}

.box-tendencia .pct {
  font-size: 14px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.box-tendencia .valor {
  font-size: 19px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  margin-bottom: 6px;
}

.box-tendencia .foot-row {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--ink-faint);
  font-variant-numeric: tabular-nums;
}

/* ---------- Industrializado / Thermo ---------- */

.mini-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.mini-card {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 9px 8px;
  border-top: 3px solid var(--cor-categoria);
  min-width: 0;
}

.mini-card .label {
  font-size: 9.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--ink-soft);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mini-card .pct-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 6px;
  margin-bottom: 6px;
}

.mini-card .pct {
  font-size: 20px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.mini-card .sub-label {
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--ink-faint);
}

.mini-card .sub {
  font-size: 10.5px;
  color: var(--ink-faint);
  font-variant-numeric: tabular-nums;
  line-height: 1.5;
}

/* ---------- Focus / a11y ---------- */

button:focus-visible, .tab:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.empty-state {
  text-align: center;
  color: var(--ink-faint);
  padding: 60px 0;
  font-size: 14px;
}

footer.foot {
  margin-top: 40px;
  text-align: center;
  font-size: 11.5px;
  color: var(--ink-faint);
}
</style>

<div class="wrap">
  <header class="top">
    <div class="title-block">
      <h1>Painel 4 Pilares</h1>
      <p>Positivação · Margem · Mix · Financeiro — atualizado em __DATA_EXTRACAO__</p>
    </div>
    <div class="summary-strip" id="summary"></div>
  </header>

  <nav class="tabs" id="tabs"></nav>

  <section class="resumo-time" id="resumoTime"></section>

  <main class="grid" id="grid"></main>
  <div class="empty-state" id="empty" style="display:none;">Nenhum RCA encontrado pra esse filtro.</div>

  <footer class="foot">Dados extraídos de CONTAR 4 PILARES · gerado automaticamente</footer>
</div>

<script>
const DADOS = __DADOS_JSON__;

function corPct(pct) {
  if (pct >= 1) return "good";
  if (pct >= 0.7) return "warn";
  return "bad";
}

function corBadge(atingidos) {
  if (atingidos >= 3) return "good";
  if (atingidos >= 1) return "warn";
  return "bad";
}

// Cortes definidos pelo Edmar (binário, sem faixa intermediária amarela).
function corParticipacaoIndustrializado(pct) {
  return pct >= 0.25 ? "good" : "bad";
}
function corMargemIndustrializado(pct) {
  return pct >= 0.18 ? "good" : "bad";
}
function corParticipacaoThermo(pct) {
  return pct >= 0.03 ? "good" : "bad";
}
function corMargemThermo(pct) {
  return pct >= 0.15 ? "good" : "bad";
}

// Recompra não tem meta pareada na planilha — faixa própria (taxa de
// clientes que voltam a comprar), ajuste os cortes se quiser outro critério.
function corRecompra(pct) {
  if (pct >= 0.4) return "bad";
  if (pct >= 0.2) return "warn";
  return "good";
}

function fmtMoeda(v) {
  return "R$ " + Number(v).toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fmtPct(v) {
  return (v * 100).toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + "%";
}

function iniciais(nome) {
  return nome.split(/\s+/).filter(Boolean).slice(0, 2).map(p => p[0]).join("").toUpperCase();
}

// cor de avatar determinística a partir do nome (paleta fixa, sem depender de foto real)
const PALETA_AVATAR = ["#0E7C86", "#7A5CC7", "#C0672B", "#3D6FB4", "#1D9A5D", "#B4740A", "#B4406B"];
function corAvatar(nome) {
  let h = 0;
  for (const c of nome) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return PALETA_AVATAR[h % PALETA_AVATAR.length];
}

function linhaPilar(label, p) {
  const cor = corPct(p.pct);
  const largura = Math.min(p.pct * 100, 100);
  return `
    <div class="pilar">
      <span class="label">${label}</span>
      <span class="pct" style="color:var(--${cor})">${fmtPct(p.pct)}</span>
      <div class="track"><div class="fill" style="width:${largura}%;background:var(--${cor})"></div></div>
      <span class="sub">Meta ${p.meta.toLocaleString("pt-BR", {maximumFractionDigits: 2})} · Realizado ${p.real.toLocaleString("pt-BR", {maximumFractionDigits: 2})}</span>
    </div>`;
}

function card(rca) {
  const corB = corBadge(rca.pilares_atingidos);
  const av = corAvatar(rca.nome);
  const textoWhats = encodeURIComponent(
    `*${rca.nome}* (RCA ${rca.codigo} · ${rca.rota})\n` +
    `Pilares: ${rca.pilares_atingidos}/4\n` +
    `Financeiro: ${fmtPct(rca.pilares.financeiro.pct)}\n` +
    `Margem: ${fmtPct(rca.pilares.margem.pct)}\n` +
    `Mix: ${fmtPct(rca.pilares.mix.pct)}\n` +
    `Positivação: ${fmtPct(rca.pilares.positivacao.pct)}\n` +
    `Tendência de fechamento: ${fmtPct(rca.tendencia.pct)}\n` +
    `Industrializados: margem ${fmtPct(rca.industrializado.margem_pct)} (real. ${fmtMoeda(rca.industrializado.real)})\n` +
    `Thermoprocessados: margem ${fmtPct(rca.thermo.margem_pct)} (real. ${fmtMoeda(rca.thermo.real)})\n` +
    `Recompra: ${fmtPct(rca.recompra_pct)}`
  );

  return `
  <article class="card" id="card-${rca.codigo}" data-supervisor="${rca.supervisor}">
    <div class="card-head">
      <div class="avatar" style="background:${av}">${iniciais(rca.nome)}</div>
      <div class="who">
        <h2>${rca.nome}</h2>
        <p class="meta">RCA ${rca.codigo} · ${rca.rota || rca.supervisor}</p>
      </div>
      <div class="head-actions">
        <span class="badge-pilares" style="background:var(--${corB}-soft);color:var(--${corB})">${rca.pilares_atingidos}/4 pilares</span>
        <button class="icon-btn" title="Imprimir" onclick="window.print()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        </button>
        <a class="icon-btn" title="Enviar no WhatsApp" href="https://wa.me/?text=${textoWhats}" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2c-5.52 0-10 4.48-10 10 0 1.77.46 3.45 1.27 4.9L2 22l5.25-1.38a9.96 9.96 0 0 0 4.79 1.22h.01c5.52 0 10-4.48 10-10s-4.48-10-10-10Zm0 18.15h-.01a8.2 8.2 0 0 1-4.17-1.14l-.3-.18-3.11.82.83-3.04-.2-.31a8.19 8.19 0 0 1-1.26-4.35c0-4.52 3.68-8.2 8.22-8.2 2.2 0 4.26.86 5.81 2.41a8.15 8.15 0 0 1 2.4 5.8c0 4.52-3.68 8.2-8.21 8.2Zm4.5-6.15c-.25-.12-1.46-.72-1.68-.8-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.96-.14.16-.29.18-.53.06-.25-.12-1.04-.38-1.98-1.22-.73-.65-1.23-1.46-1.37-1.7-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.16-.24.24-.4.08-.16.04-.31-.02-.43-.06-.12-.56-1.35-.77-1.85-.2-.48-.41-.42-.56-.42-.14 0-.31-.02-.47-.02-.16 0-.43.06-.66.31-.22.24-.86.85-.86 2.08 0 1.22.89 2.4 1.01 2.57.12.16 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.46-.6 1.66-1.17.21-.58.21-1.08.14-1.18-.06-.1-.22-.16-.47-.28Z"></path></svg>
        </a>
      </div>
    </div>

    <div class="pilares-list">
      ${linhaPilar("Financeiro", rca.pilares.financeiro)}
      ${linhaPilar("Margem", rca.pilares.margem)}
      ${linhaPilar("Mix", rca.pilares.mix)}
      ${linhaPilar("Positivação", rca.pilares.positivacao)}
    </div>

    <div class="box-tendencia">
      <div class="top-row">
        <span class="label">Tendência de fechamento</span>
        <span class="pct" style="color:var(--${corPct(rca.tendencia.pct)})">${fmtPct(rca.tendencia.pct)}</span>
      </div>
      <div class="valor">${fmtMoeda(rca.tendencia.projetado)}</div>
      <div class="foot-row">
        <span>Meta ${fmtMoeda(rca.tendencia.meta)}</span>
        <span>Projetado</span>
      </div>
      <div class="foot-row" style="margin-top:4px;padding-top:6px;border-top:1px dashed var(--border)">
        <span>Meta do dia</span>
        <span>${fmtMoeda(rca.tendencia.meta_dia)}</span>
      </div>
      <div class="foot-row" style="margin-top:6px;padding-top:6px;border-top:1px dashed var(--border);align-items:center">
        <span>Recompra</span>
        <span class="pct" style="font-size:13px;color:var(--${corRecompra(rca.recompra_pct)})">${fmtPct(rca.recompra_pct)}</span>
      </div>
    </div>

    <div class="mini-cards">
      <div class="mini-card" style="--cor-categoria:#7A5CC7">
        <div class="label">Industrializados</div>
        <div class="pct-row">
          <span class="sub-label">Participação</span>
          <span class="pct" style="color:var(--${corParticipacaoIndustrializado(rca.industrializado.participacao_pct)})">${fmtPct(rca.industrializado.participacao_pct)}</span>
        </div>
        <div class="pct-row">
          <span class="sub-label">Margem</span>
          <span class="pct" style="color:var(--${corMargemIndustrializado(rca.industrializado.margem_pct)})">${fmtPct(rca.industrializado.margem_pct)}</span>
        </div>
        <div class="sub">Meta ${fmtMoeda(rca.industrializado.meta)}<br>Realizado ${fmtMoeda(rca.industrializado.real)}</div>
      </div>
      <div class="mini-card" style="--cor-categoria:#C0672B">
        <div class="label">Thermoprocessados</div>
        <div class="pct-row">
          <span class="sub-label">Participação</span>
          <span class="pct" style="color:var(--${corParticipacaoThermo(rca.thermo.participacao_pct)})">${fmtPct(rca.thermo.participacao_pct)}</span>
        </div>
        <div class="pct-row">
          <span class="sub-label">Margem</span>
          <span class="pct" style="color:var(--${corMargemThermo(rca.thermo.margem_pct)})">${fmtPct(rca.thermo.margem_pct)}</span>
        </div>
        <div class="sub">Meta ${fmtMoeda(rca.thermo.meta)}<br>Realizado ${fmtMoeda(rca.thermo.real)}</div>
      </div>
    </div>
  </article>`;
}

function montarResumo(dados) {
  const total = dados.length;
  const media = dados.reduce((s, r) => s + r.pilares_atingidos, 0) / (total || 1);
  const acima3 = dados.filter(r => r.pilares_atingidos >= 3).length;
  const supervisores = new Set(dados.map(r => r.supervisor)).size;
  document.getElementById("summary").innerHTML = `
    <div class="stat-pill"><div class="n">${total}</div><div class="l">RCAs</div></div>
    <div class="stat-pill"><div class="n">${supervisores}</div><div class="l">Supervisores</div></div>
    <div class="stat-pill"><div class="n">${media.toFixed(1)}</div><div class="l">Média pilares</div></div>
    <div class="stat-pill"><div class="n">${acima3}</div><div class="l">Com 3-4 pilares</div></div>
  `;
}

function media(valores) {
  return valores.length ? valores.reduce((s, v) => s + v, 0) / valores.length : 0;
}

// Monta um "RCA" sintético com os totais do time — mesmo formato de dado
// que um RCA de verdade, pra poder reaproveitar exatamente o mesmo card().
function agregarTime(dados, nomeSupervisor) {
  const somarMeta = campo => dados.reduce((s, r) => s + r.pilares[campo].meta, 0);
  const somarReal = campo => dados.reduce((s, r) => s + r.pilares[campo].real, 0);
  const pilar = campo => {
    const meta = somarMeta(campo);
    const real = somarReal(campo);
    return { meta, real, pct: meta ? real / meta : 0 };
  };

  const metaFin = somarMeta("financeiro");
  const projetado = dados.reduce((s, r) => s + r.tendencia.projetado, 0);
  const metaDia = dados.reduce((s, r) => s + r.tendencia.meta_dia, 0);

  return {
    codigo: "EQUIPE",
    nome: nomeSupervisor,
    rota: `${dados.length} RCA${dados.length > 1 ? "s" : ""}`,
    supervisor: nomeSupervisor,
    pilares: {
      positivacao: pilar("positivacao"),
      margem: pilar("margem"),
      mix: pilar("mix"),
      financeiro: pilar("financeiro"),
    },
    pilares_atingidos: Math.round(media(dados.map(r => r.pilares_atingidos))),
    tendencia: {
      pct: metaFin ? projetado / metaFin : 0,
      projetado,
      meta: metaFin,
      meta_dia: metaDia,
    },
    industrializado: {
      meta: dados.reduce((s, r) => s + r.industrializado.meta, 0),
      real: dados.reduce((s, r) => s + r.industrializado.real, 0),
      participacao_pct: media(dados.map(r => r.industrializado.participacao_pct)),
      margem_pct: media(dados.map(r => r.industrializado.margem_pct)),
    },
    thermo: {
      meta: dados.reduce((s, r) => s + r.thermo.meta, 0),
      real: dados.reduce((s, r) => s + r.thermo.real, 0),
      participacao_pct: media(dados.map(r => r.thermo.participacao_pct)),
      margem_pct: media(dados.map(r => r.thermo.margem_pct)),
    },
    recompra_pct: media(dados.map(r => r.recompra_pct)),
  };
}

function montarResumoTime(dados, nomeSupervisor) {
  const el = document.getElementById("resumoTime");
  if (!dados.length) { el.innerHTML = ""; return; }
  el.innerHTML = card(agregarTime(dados, nomeSupervisor));
}

function montarTabs(dados) {
  const supervisores = [...new Set(dados.map(r => r.supervisor))].sort();
  const contagem = s => dados.filter(r => r.supervisor === s).length;
  const tabsEl = document.getElementById("tabs");
  tabsEl.innerHTML =
    `<button class="tab active" data-sup="__todos__">Todos <span class="count">${dados.length}</span></button>` +
    supervisores.map(s => `<button class="tab" data-sup="${s}">${s} <span class="count">${contagem(s)}</span></button>`).join("");

  tabsEl.addEventListener("click", (e) => {
    const btn = e.target.closest(".tab");
    if (!btn) return;
    tabsEl.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    btn.classList.add("active");
    filtrar(btn.dataset.sup);
  });
}

function filtrar(sup) {
  const cards = document.querySelectorAll(".card");
  let visiveis = 0;
  cards.forEach(c => {
    const mostra = sup === "__todos__" || c.dataset.supervisor === sup;
    c.style.display = mostra ? "" : "none";
    if (mostra) visiveis++;
  });
  document.getElementById("empty").style.display = visiveis === 0 ? "block" : "none";

  const filtrados = sup === "__todos__" ? DADOS : DADOS.filter(r => r.supervisor === sup);
  montarResumoTime(filtrados, sup === "__todos__" ? "EQUIPE TODA" : sup);
}

function montar() {
  montarResumo(DADOS);
  const supervisorUnico = new Set(DADOS.map(r => r.supervisor)).size === 1 ? DADOS[0].supervisor : "EQUIPE TODA";
  montarResumoTime(DADOS, supervisorUnico);
  montarTabs(DADOS);
  document.getElementById("grid").innerHTML = DADOS
    .slice()
    .sort((a, b) => b.pilares_atingidos - a.pilares_atingidos || a.nome.localeCompare(b.nome))
    .map(card)
    .join("");
}

montar();
</script>
"""


def gerar_html(dados, titulo="Painel 4 Pilares — Equipe GYN"):
    import datetime
    data_extracao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    html = TEMPLATE.replace("__DADOS_JSON__", json.dumps(dados, ensure_ascii=False))
    html = html.replace("__DATA_EXTRACAO__", data_extracao)
    html = html.replace("<title>Painel 4 Pilares — Equipe GYN</title>", f"<title>{titulo}</title>")
    return html


# ---------------------------------------------------------------------------
# Painel do GERENTE — dashboard de verdade (KPIs + gráficos), diferente do
# resto do site (que reaproveita o card do vendedor). Gráficos em SVG
# calculados no Python (dados fixos por geração, sem precisar de JS), com a
# paleta validada da skill de dataviz: cores categóricas de série (7
# supervisores) e cores de status (good/warning/critical) — ambas já
# validadas pro contraste e daltonismo, não escolhidas no olho.
# ---------------------------------------------------------------------------

import math

# CSS base do site (cores/tokens/tipografia/estrutura .wrap, header etc.) —
# reaproveitado pra manter a mesma identidade visual do resto do painel.
_CSS_COMPARTILHADO = TEMPLATE.split("<style>")[1].split("</style>")[0]


def _fmt_moeda_py(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _fmt_num_py(v, casas=2):
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _fmt_pct_py(v):
    return _fmt_num_py(v * 100, 1) + "%"


def _classe_status(pct):
    if pct >= 1:
        return "dv-good"
    if pct >= 0.7:
        return "dv-warn"
    return "dv-bad"


def _svg_barras(itens, largura=560, sublabel=False):
    """itens: [(label, pct_0a1_pra_largura, texto_valor, classe_css)], ou com
    sublabel=True: [(label, linhas_subtitulo, pct, texto_valor, classe_css)]
    — nome à esquerda, 1+ linhas de subtítulo (ex: R$ realizado, Positivação
    real/meta) em cima da própria barra, trilho + preenchido. Sem sublabel,
    valor fica à direita da barra; com sublabel, valor fica dentro da barra
    preenchida, em branco (some pra fora, em tinta escura, se a barra
    estiver curta demais pra caber o texto). `linhas_subtitulo` é uma lista
    de strings (uma por linha) ou None."""
    rotulo_w = 132
    valor_w = 96
    trilho_x = rotulo_w
    trilho_w = largura - rotulo_w - (0 if sublabel else valor_w)
    linhas = []
    y = 0
    for item in itens:
        if sublabel:
            label, linhas_subtitulo, pct, valor_txt, classe = item
            if isinstance(linhas_subtitulo, str):
                linhas_subtitulo = [linhas_subtitulo] if linhas_subtitulo else None
        else:
            label, pct, valor_txt, classe = item
            linhas_subtitulo = None
        n_subtitulo = len(linhas_subtitulo) if linhas_subtitulo else 0
        altura_linha_subtitulo = 17  # espaço de sobra pra 13.5px de fonte não colidir entre linhas
        largura_fill = max(3, min(max(pct, 0), 1) * trilho_w)
        offset_barra = n_subtitulo * altura_linha_subtitulo + 8 if n_subtitulo else 10
        y_barra = y + offset_barra
        y_rotulo = y_barra + 11
        linhas.append(f'''
    <text x="0" y="{y_rotulo}" font-size="12.5" font-weight="700" class="dv-ink-soft">{label}</text>''')
        for i, linha_txt in enumerate(linhas_subtitulo or []):
            linhas.append(f'''
    <text x="{trilho_x}" y="{y + 13 + i * altura_linha_subtitulo}" font-size="13.5" font-weight="800" class="dv-ink">{linha_txt}</text>''')
        linhas.append(f'''
    <rect x="{trilho_x}" y="{y_barra}" width="{trilho_w}" height="13" rx="6.5" class="dv-track"/>
    <rect x="{trilho_x}" y="{y_barra}" width="{largura_fill:.1f}" height="13" rx="6.5" class="{classe}"/>''')
        if sublabel:
            if largura_fill >= 50:
                linhas.append(f'''
    <text x="{trilho_x + largura_fill - 8:.1f}" y="{y_rotulo}" font-size="12.5" font-weight="800" text-anchor="end" fill="#fff">{valor_txt}</text>''')
            else:
                linhas.append(f'''
    <text x="{trilho_x + largura_fill + 6:.1f}" y="{y_rotulo}" font-size="12.5" font-weight="800" text-anchor="start" class="dv-ink">{valor_txt}</text>''')
        else:
            linhas.append(f'''
    <text x="{largura - 2}" y="{y_rotulo}" font-size="12.5" font-weight="800" text-anchor="end" class="dv-ink">{valor_txt}</text>''')
        y += offset_barra + 13 + 11  # altura desta linha (até o fim da barra) + respiro
    return (f'<svg viewBox="0 0 {largura} {y}" width="100%" height="{y}" role="img" '
            f'aria-label="Gráfico de barras">{"".join(linhas)}</svg>')


def _svg_donut(itens, tamanho=176, espessura=28):
    """itens: [(label, valor, classe_css)]. Retorna (svg, legenda_html)."""
    total = sum(v for _, v, _ in itens) or 1
    r = (tamanho - espessura) / 2
    cx = cy = tamanho / 2
    circ = 2 * math.pi * r
    acumulado = 0
    arcos = []
    for _, valor, classe in itens:
        frac = valor / total
        dash = frac * circ
        dash_visivel = max(0.0, dash - 3)
        offset = -(acumulado / total) * circ
        acumulado += valor
        arcos.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" class="{classe}" '
            f'stroke-width="{espessura}" stroke-dasharray="{dash_visivel:.2f} {circ - dash_visivel:.2f}" '
            f'stroke-dashoffset="{offset:.2f}" transform="rotate(-90 {cx} {cy})"/>'
        )
    svg = (f'<svg viewBox="0 0 {tamanho} {tamanho}" width="{tamanho}" height="{tamanho}" role="img" '
           f'aria-label="Gráfico de rosca">{"".join(arcos)}</svg>')

    legenda = '<div class="dv-legenda">'
    for label, valor, classe in itens:
        pct_fatia = valor / total
        legenda += (f'<div class="dv-legenda-item"><span class="dv-dote {classe}"></span>'
                    f'<span class="dv-legenda-label">{label}</span>'
                    f'<span class="dv-legenda-valor">{_fmt_pct_py(pct_fatia)}</span></div>')
    legenda += "</div>"
    return svg, legenda


_CORES_CATEGORICAS = [f"dv-cat-{i}" for i in range(1, 8)]

_CSS_DASHBOARD_GERENTE = """
:root {
  --dv-good: #0ca30c; --dv-warn: #fab219; --dv-bad: #d03b3b;
  --dv-track: #E4E7EC;
  --dv-cat-1: #2a78d6; --dv-cat-2: #eb6834; --dv-cat-3: #1baf7a; --dv-cat-4: #eda100;
  --dv-cat-5: #e87ba4; --dv-cat-6: #008300; --dv-cat-7: #4a3aa7;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --dv-track: #253039;
    --dv-cat-1: #3987e5; --dv-cat-2: #d95926; --dv-cat-3: #199e70; --dv-cat-4: #c98500;
    --dv-cat-5: #d55181; --dv-cat-6: #008300; --dv-cat-7: #9085e9;
  }
}
:root[data-theme="dark"] {
  --dv-track: #253039;
  --dv-cat-1: #3987e5; --dv-cat-2: #d95926; --dv-cat-3: #199e70; --dv-cat-4: #c98500;
  --dv-cat-5: #d55181; --dv-cat-6: #008300; --dv-cat-7: #9085e9;
}
.dv-good { fill: var(--dv-good); } .dv-warn { fill: var(--dv-warn); } .dv-bad { fill: var(--dv-bad); }
.dv-track { fill: var(--dv-track); }
.dv-ink { fill: var(--ink); } .dv-ink-soft { fill: var(--ink-soft); }
.dv-cat-1 { fill: var(--dv-cat-1); } .dv-cat-2 { fill: var(--dv-cat-2); } .dv-cat-3 { fill: var(--dv-cat-3); }
.dv-cat-4 { fill: var(--dv-cat-4); } .dv-cat-5 { fill: var(--dv-cat-5); } .dv-cat-6 { fill: var(--dv-cat-6); }
.dv-cat-7 { fill: var(--dv-cat-7); }

.dv-donut-wrap circle { fill: none; }
.dv-donut-wrap .dv-good { stroke: var(--dv-good); }
.dv-donut-wrap .dv-warn { stroke: var(--dv-warn); }
.dv-donut-wrap .dv-bad { stroke: var(--dv-bad); }
.dv-donut-wrap .dv-cat-1 { stroke: var(--dv-cat-1); } .dv-donut-wrap .dv-cat-2 { stroke: var(--dv-cat-2); }
.dv-donut-wrap .dv-cat-3 { stroke: var(--dv-cat-3); } .dv-donut-wrap .dv-cat-4 { stroke: var(--dv-cat-4); }
.dv-donut-wrap .dv-cat-5 { stroke: var(--dv-cat-5); } .dv-donut-wrap .dv-cat-6 { stroke: var(--dv-cat-6); }
.dv-donut-wrap .dv-cat-7 { stroke: var(--dv-cat-7); }

.dv-kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 22px; }
.dv-kpi { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 16px 18px; border-top: 4px solid; }
.dv-kpi.dv-good { border-top-color: var(--dv-good); }
.dv-kpi.dv-warn { border-top-color: var(--dv-warn); }
.dv-kpi.dv-bad { border-top-color: var(--dv-bad); }
.dv-kpi .l { font-size: 11.5px; font-weight: 800; text-transform: uppercase; letter-spacing: .04em; color: var(--ink-soft); margin-bottom: 6px; }
.dv-kpi .v { font-size: 24px; font-weight: 800; letter-spacing: -0.01em; margin-bottom: 2px; }
.dv-kpi .m { font-size: 14px; font-weight: 700; color: var(--ink-faint); margin-bottom: 10px; }
.dv-kpi .badge { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 800; padding: 3px 9px; border-radius: 999px; }
.dv-kpi .badge.dv-good { background: var(--good-soft); color: var(--good); }
.dv-kpi .badge.dv-warn { background: var(--warn-soft); color: var(--warn); }
.dv-kpi .badge.dv-bad { background: var(--bad-soft); color: var(--bad); }

.dv-row { display: grid; grid-template-columns: 1.3fr 1fr; gap: 18px; margin-bottom: 18px; }
.dv-row.dv-row-inv { grid-template-columns: 1fr 1.3fr; }
@media (max-width: 760px) { .dv-row, .dv-row.dv-row-inv { grid-template-columns: 1fr; } }
.dv-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 18px 20px; }
.dv-panel h3 { margin: 0 0 16px; font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: .04em; color: var(--ink-soft); }
.dv-donut-wrap { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; justify-content: center; }
.dv-legenda { display: flex; flex-direction: column; gap: 8px; }
.dv-legenda-item { display: flex; align-items: center; gap: 8px; font-size: 12.5px; }
.dv-dote { width: 10px; height: 10px; border-radius: 3px; flex: none; }
.dv-dote.dv-good { background: var(--dv-good); } .dv-dote.dv-warn { background: var(--dv-warn); } .dv-dote.dv-bad { background: var(--dv-bad); }
.dv-dote.dv-cat-1 { background: var(--dv-cat-1); } .dv-dote.dv-cat-2 { background: var(--dv-cat-2); }
.dv-dote.dv-cat-3 { background: var(--dv-cat-3); } .dv-dote.dv-cat-4 { background: var(--dv-cat-4); }
.dv-dote.dv-cat-5 { background: var(--dv-cat-5); } .dv-dote.dv-cat-6 { background: var(--dv-cat-6); }
.dv-dote.dv-cat-7 { background: var(--dv-cat-7); }
.dv-legenda-label { color: var(--ink-soft); font-weight: 600; flex: 1; white-space: nowrap; }
.dv-legenda-valor { font-weight: 800; font-variant-numeric: tabular-nums; }

.dv-tabela { width: 100%; border-collapse: collapse; margin-top: 18px; font-size: 11.5px; }
.dv-tabela th, .dv-tabela td { padding: 5px 6px; text-align: right; font-variant-numeric: tabular-nums; }
.dv-tabela thead th { font-size: 10.5px; text-transform: uppercase; letter-spacing: .03em; color: var(--ink-faint); font-weight: 800; border-bottom: 1px solid var(--border); }
.dv-tabela thead tr:first-child th { text-align: center; }
.dv-tabela .dv-tab-sub th { padding-top: 2px; }
.dv-tabela .dv-tab-sup { text-align: left; font-weight: 700; color: var(--ink-soft); }
.dv-tabela tbody tr:nth-child(even) { background: var(--surface-2); }
.dv-tabela td.dv-good { color: var(--good); font-weight: 800; }
.dv-tabela td.dv-bad { color: var(--bad); font-weight: 800; }
"""

TEMPLATE_GERENTE = None  # gerado dinamicamente em gerar_html_gerente()


def gerar_html_gerente(dados, totais):
    import datetime
    data_extracao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def soma(pilar, campo):
        return sum(r["pilares"][pilar][campo] for r in dados)

    supervisores = sorted({r["supervisor"] for r in dados})

    # ---- KPIs (somatória geral) ----
    # Financeiro/Positivação: soma direta das linhas por RCA (bate com o
    # total da planilha). Margem/Mix: vêm prontos do bloco de totais da
    # planilha (T84/U84, T87/U87) — não são soma/média das linhas por RCA.
    fmt_pct_2casas = lambda v: _fmt_num_py(v * 100, 2) + "%"
    meta_financeiro = soma("financeiro", "meta")
    tendencia_projetado = sum(r["tendencia"]["projetado"] for r in dados)
    tendencia_pct = tendencia_projetado / meta_financeiro if meta_financeiro else 0
    kpis_fonte = [
        ("Financeiro", *[soma("financeiro", c) for c in ("meta", "real")], _fmt_moeda_py),
        ("Positivação", *[soma("positivacao", c) for c in ("meta", "real")], lambda v: _fmt_num_py(v, 0)),
        ("Margem", totais["margem"]["meta"], totais["margem"]["real"], fmt_pct_2casas),
        ("Mix", totais["mix"]["meta"], totais["mix"]["real"], fmt_pct_2casas),
    ]
    kpis_html = ""
    for label, meta, real, fmt in kpis_fonte:
        pct = real / meta if meta else 0
        classe = _classe_status(pct)
        extra = ""
        if label == "Financeiro":
            classe_tendencia = _classe_status(tendencia_pct)
            extra = f'''
      <div class="m">Tendência {_fmt_moeda_py(tendencia_projetado)}</div>
      <span class="badge {classe_tendencia}" style="margin-left:6px;">Tend. {_fmt_pct_py(tendencia_pct)}</span>'''
        badge_pct = "" if label == "Financeiro" else f'<span class="badge {classe}">{_fmt_pct_py(pct)}</span>'
        kpis_html += f'''
    <div class="dv-kpi {classe}">
      <div class="l">{label}</div>
      <div class="v">{fmt(real)}</div>
      <div class="m">Meta {fmt(meta)}</div>
      {badge_pct}{extra}
    </div>'''

    # Industrializados/Thermoprocessados: mesmos cortes de cor já usados no
    # resto do site (participação/margem, critério binário definido pelo
    # Edmar) — meta/real são somáveis, participação/margem são médias.
    # Ficam numa segunda fileira própria, separados dos 4 pilares principais.
    kpis_html_industrializados = ""
    for label, chave, limite_participacao, limite_margem in [
        ("Industrializados", "industrializado", 0.25, 0.18),
        ("Thermoprocessados", "thermo", 0.03, 0.15),
    ]:
        meta = sum(r[chave]["meta"] for r in dados)
        real = sum(r[chave]["real"] for r in dados)
        participacoes = [r[chave]["participacao_pct"] for r in dados]
        margens = [r[chave]["margem_pct"] for r in dados]
        media_participacao = sum(participacoes) / len(participacoes) if participacoes else 0
        media_margem = sum(margens) / len(margens) if margens else 0
        classe_participacao = "dv-good" if media_participacao >= limite_participacao else "dv-bad"
        classe_margem = "dv-good" if media_margem >= limite_margem else "dv-bad"
        kpis_html_industrializados += f'''
    <div class="dv-kpi {classe_margem}">
      <div class="l">{label}</div>
      <div class="v">{_fmt_moeda_py(real)}</div>
      <div class="m">Meta {_fmt_moeda_py(meta)}</div>
      <span class="badge {classe_participacao}">Particip. {_fmt_pct_py(media_participacao)}</span>
      <span class="badge {classe_margem}" style="margin-left:6px;">Margem {_fmt_pct_py(media_margem)}</span>
    </div>'''

    # ---- Gráfico 1: tendência de fechamento por supervisor (barras) ----
    linhas_tendencia = []
    for sup in supervisores:
        do_sup = [r for r in dados if r["supervisor"] == sup]
        meta_sup = sum(r["pilares"]["financeiro"]["meta"] for r in do_sup)
        real_sup = sum(r["pilares"]["financeiro"]["real"] for r in do_sup)
        meta_posit_sup = sum(r["pilares"]["positivacao"]["meta"] for r in do_sup)
        real_posit_sup = sum(r["pilares"]["positivacao"]["real"] for r in do_sup)
        projetado_sup = sum(r["tendencia"]["projetado"] for r in do_sup)
        pct = projetado_sup / meta_sup if meta_sup else 0
        subtitulo = [
            _fmt_moeda_py(real_sup),
            f"Positivação {_fmt_num_py(real_posit_sup, 0)}/{_fmt_num_py(meta_posit_sup, 0)}",
        ]
        linhas_tendencia.append((sup, subtitulo, pct, _fmt_pct_py(pct), _classe_status(pct)))
    linhas_tendencia.sort(key=lambda x: x[2], reverse=True)
    svg_tendencia = _svg_barras(linhas_tendencia, sublabel=True)

    # ---- Gráfico 2: participação no faturamento realizado por supervisor (rosca) ----
    fatias_faturamento = []
    for i, sup in enumerate(supervisores):
        do_sup = [r for r in dados if r["supervisor"] == sup]
        real_sup = sum(r["pilares"]["financeiro"]["real"] for r in do_sup)
        fatias_faturamento.append((sup, real_sup, _CORES_CATEGORICAS[i % len(_CORES_CATEGORICAS)]))
    fatias_faturamento.sort(key=lambda x: x[1], reverse=True)
    svg_faturamento, legenda_faturamento = _svg_donut(fatias_faturamento)

    # Tabela Industrializado/Thermo por supervisor (mesmos critérios de cor
    # dos KPIs de cima: margem industrializado >=18% bom, margem thermo >=15%
    # bom) — mostrada embaixo do donut de participação no faturamento.
    linhas_ind_thermo = ""
    for sup in supervisores:
        do_sup = [r for r in dados if r["supervisor"] == sup]
        meta_ind = sum(r["industrializado"]["meta"] for r in do_sup)
        real_ind = sum(r["industrializado"]["real"] for r in do_sup)
        margens_ind = [r["industrializado"]["margem_pct"] for r in do_sup]
        media_margem_ind = sum(margens_ind) / len(margens_ind) if margens_ind else 0
        meta_thermo = sum(r["thermo"]["meta"] for r in do_sup)
        real_thermo = sum(r["thermo"]["real"] for r in do_sup)
        margens_thermo = [r["thermo"]["margem_pct"] for r in do_sup]
        media_margem_thermo = sum(margens_thermo) / len(margens_thermo) if margens_thermo else 0
        classe_ind = "dv-good" if media_margem_ind >= 0.18 else "dv-bad"
        classe_thermo = "dv-good" if media_margem_thermo >= 0.15 else "dv-bad"
        linhas_ind_thermo += f'''
      <tr>
        <td class="dv-tab-sup">{sup}</td>
        <td>{_fmt_moeda_py(meta_ind)}</td>
        <td>{_fmt_moeda_py(real_ind)}</td>
        <td class="{classe_ind}">{_fmt_pct_py(media_margem_ind)}</td>
        <td>{_fmt_moeda_py(meta_thermo)}</td>
        <td>{_fmt_moeda_py(real_thermo)}</td>
        <td class="{classe_thermo}">{_fmt_pct_py(media_margem_thermo)}</td>
      </tr>'''
    tabela_ind_thermo = f'''
    <table class="dv-tabela">
      <thead>
        <tr>
          <th>Supervisor</th>
          <th colspan="3">Industrializado</th>
          <th colspan="3">Thermo</th>
        </tr>
        <tr class="dv-tab-sub">
          <th></th>
          <th>Meta</th>
          <th>Realizado</th>
          <th>Margem</th>
          <th>Meta</th>
          <th>Realizado</th>
          <th>Margem</th>
        </tr>
      </thead>
      <tbody>{linhas_ind_thermo}
      </tbody>
    </table>'''

    # ---- Gráfico 3: RCAs com 3-4 pilares por supervisor (barras) ----
    linhas_pilares = []
    maior_qtd = max(
        (sum(1 for r in dados if r["supervisor"] == sup and r["pilares_atingidos"] >= 3) for sup in supervisores),
        default=0,
    ) or 1
    for sup in supervisores:
        qtd = sum(1 for r in dados if r["supervisor"] == sup and r["pilares_atingidos"] >= 3)
        total_sup = sum(1 for r in dados if r["supervisor"] == sup)
        linhas_pilares.append((sup, qtd / maior_qtd, f"{qtd}/{total_sup}", "dv-cat-1"))
    linhas_pilares.sort(key=lambda x: x[1], reverse=True)
    svg_pilares = _svg_barras(linhas_pilares)

    # ---- Gráfico 4: RCAs por faixa de pilares atingidos (rosca, status) ----
    baixo = sum(1 for r in dados if r["pilares_atingidos"] <= 1)
    medio = sum(1 for r in dados if r["pilares_atingidos"] == 2)
    alto = sum(1 for r in dados if r["pilares_atingidos"] >= 3)
    fatias_faixa = [
        ("0-1 pilares", baixo, "dv-bad"),
        ("2 pilares", medio, "dv-warn"),
        ("3-4 pilares", alto, "dv-good"),
    ]
    svg_faixa, legenda_faixa = _svg_donut(fatias_faixa)

    total_rcas = len(dados)

    corpo = f"""<title>Painel do Gerente — Equipe GYN</title>
<style>
{_CSS_COMPARTILHADO}
{_CSS_DASHBOARD_GERENTE}
</style>

<div class="wrap">
  <header class="top">
    <div class="title-block">
      <h1>Painel do Gerente</h1>
      <p>{total_rcas} RCAs · {len(supervisores)} supervisores — atualizado em {data_extracao}</p>
    </div>
  </header>

  <section class="dv-kpis">{kpis_html}
  </section>

  <section class="dv-kpis">{kpis_html_industrializados}
  </section>

  <section class="dv-row dv-row-inv">
    <div class="dv-panel">
      <h3>Participação no faturamento realizado</h3>
      <div class="dv-donut-wrap">{svg_faturamento}{legenda_faturamento}</div>
      {tabela_ind_thermo}
    </div>
    <div class="dv-panel">
      <h3>Tendência de fechamento por supervisor</h3>
      {svg_tendencia}
    </div>
  </section>

  <section class="dv-row">
    <div class="dv-panel">
      <h3>RCAs com 3-4 pilares por supervisor</h3>
      {svg_pilares}
    </div>
    <div class="dv-panel">
      <h3>RCAs por faixa de pilares atingidos</h3>
      <div class="dv-donut-wrap">{svg_faixa}{legenda_faixa}</div>
    </div>
  </section>

  <footer class="foot">Dados extraídos de CONTAR 4 PILARES · gerado automaticamente</footer>
</div>
"""
    return corpo


CAMINHO_TOTAIS = os.path.join(PASTA_BASE, "totais_gerais.json")


def main():
    with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
        dados = json.load(f)
    with open(CAMINHO_TOTAIS, "r", encoding="utf-8") as f:
        totais = json.load(f)

    html = gerar_html(dados)
    with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Painel gerado em: {CAMINHO_SAIDA}")

    # Um painel filtrado por supervisor, além do geral — cada supervisor
    # tem seu próprio arquivo/link, só com o time dele.
    supervisores = sorted({r["supervisor"] for r in dados})
    pasta_supervisores = os.path.join(PASTA_BASE, "supervisores")
    os.makedirs(pasta_supervisores, exist_ok=True)
    for sup in supervisores:
        dados_sup = [r for r in dados if r["supervisor"] == sup]
        html_sup = gerar_html(dados_sup, titulo=f"Painel 4 Pilares — {sup}")
        caminho_sup = os.path.join(pasta_supervisores, f"painel_{sup}.html")
        with open(caminho_sup, "w", encoding="utf-8") as f:
            f.write(html_sup)
        print(f"  -> Painel de {sup} gerado em: {caminho_sup}")

    html_gerente = gerar_html_gerente(dados, totais)
    caminho_gerente = os.path.join(PASTA_BASE, "painel_gerente.html")
    with open(caminho_gerente, "w", encoding="utf-8") as f:
        f.write(html_gerente)
    print(f"  -> Painel do gerente gerado em: {caminho_gerente}")


if __name__ == "__main__":
    main()
