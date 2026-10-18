#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los portales interactivos de validación:
  1. docs/modos_variaciones.html (y validacion_modos_taffanel_reichert.html en raíz):
     Visor y reproductor interactivo de las 840 variaciones modales (12 Tónicas × 7 Modos × 10 Esquemas:
     Taffanel E.J. 1, 2, 4, 5, 10, 11 y Reichert R. 1, 2, 4, 5) con síntesis Web Audio y vista comparativa.
  2. docs/propuestas_ux_wizard_modos.html (y propuestas_ux_wizard_modos.html en raíz):
     Investigación de usabilidad (Stitch Project 14323574806802443450) con las 4 Opciones de UX/UI para:
       - Nuevo Dashboard Inicial
       - Asistente de Práctica (Practice Wizard con <dialog closedby="any">)
       - Nueva Pantalla de Modos con selector de los 10 esquemas de Taffanel y Reichert.
"""

import os
import shutil

MODOS_VARIACIONES_HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FluteModes · Validación de 840 Variaciones Modales (Taffanel &amp; Gaubert + Reichert Op. 5)</title>
  <script src="abcjs-basic-min.js"></script>
  <script src="modes_variations_data.js"></script>
  <style>
    :root {
      --bg: #fdfbf7;
      --surface: #f7f3e9;
      --surface-elev: #efe9d9;
      --ink: #1c1a17;
      --ink-muted: #5c5346;
      --gold: #8c6d1f;
      --gold-bright: #d4af37;
      --indigo: #1e3a8a;
      --emerald: #0d9488;
      --border: #ddd6c6;
      --radius: 12px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Plus Jakarta Sans", "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.5;
    }
    header.top-nav {
      background: #181410;
      color: #fdfbf7;
      padding: 14px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      border-bottom: 2px solid var(--gold-bright);
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-badge {
      background: var(--gold-bright);
      color: #181410;
      font-weight: 800;
      font-size: 0.78rem;
      padding: 4px 10px;
      border-radius: 999px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }
    .brand h1 {
      font-family: Georgia, "EB Garamond", serif;
      font-size: 1.25rem;
      margin: 0;
      font-weight: 600;
    }
    .nav-links {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }
    .nav-links a {
      color: #fdfbf7;
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      padding: 7px 14px;
      border-radius: 999px;
      border: 1px solid rgba(212, 175, 55, 0.45);
      background: rgba(255, 255, 255, 0.06);
      transition: all 0.15s ease;
    }
    .nav-links a:hover, .nav-links a.active {
      background: var(--gold-bright);
      color: #181410;
      border-color: var(--gold-bright);
    }

    .container {
      max-width: 1380px;
      margin: 0 auto;
      padding: 20px 24px 60px;
    }

    .hero-banner {
      background: linear-gradient(135deg, #f7f3e9 0%, #efe7d3 100%);
      border: 1px solid var(--border);
      border-left: 5px solid var(--gold);
      border-radius: var(--radius);
      padding: 18px 22px;
      margin-bottom: 20px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }
    .hero-banner h2 {
      font-family: Georgia, serif;
      margin: 0 0 6px 0;
      font-size: 1.4rem;
      color: var(--ink);
    }
    .hero-banner p {
      margin: 0;
      font-size: 0.92rem;
      color: var(--ink-muted);
      max-width: 820px;
    }
    .stats-row {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }
    .stat-pill {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 8px 14px;
      text-align: center;
      min-width: 110px;
    }
    .stat-pill strong {
      display: block;
      font-size: 1.15rem;
      color: var(--gold);
    }
    .stat-pill span {
      font-size: 0.74rem;
      color: var(--ink-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .control-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
      margin-bottom: 18px;
    }
    .control-panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 14px 18px;
    }
    .panel-label {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--ink-muted);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .scheme-groups {
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 14px;
    }
    @media (max-width: 960px) {
      .scheme-groups { grid-template-columns: 1fr; }
    }
    .scheme-group-box {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
    }
    .scheme-group-title {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--gold);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .pill-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    button.chip {
      appearance: none;
      border: 1px solid #cfc6b4;
      background: #fdfbf7;
      color: var(--ink);
      padding: 7px 12px;
      border-radius: 999px;
      font-size: 0.83rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.14s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    button.chip:hover {
      border-color: var(--gold);
      background: #f5eedc;
    }
    button.chip.active {
      background: var(--gold);
      color: #fff;
      border-color: var(--gold);
      box-shadow: 0 2px 6px rgba(140, 109, 31, 0.28);
    }
    button.chip.reichert.active {
      background: var(--indigo);
      border-color: var(--indigo);
      box-shadow: 0 2px 6px rgba(30, 58, 138, 0.28);
    }
    button.chip small {
      opacity: 0.82;
      font-size: 0.72rem;
      font-weight: 500;
    }

    .selectors-two-col {
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 14px;
    }
    @media (max-width: 960px) {
      .selectors-two-col { grid-template-columns: 1fr; }
    }

    .toolbar-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 12px 18px;
      margin-bottom: 18px;
    }
    .toolbar-group {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }
    .toolbar-group label {
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--ink-muted);
    }
    select.std-select {
      padding: 7px 12px;
      border-radius: 8px;
      border: 1px solid #c9bfa9;
      background: var(--bg);
      color: var(--ink);
      font-size: 0.85rem;
      font-weight: 600;
    }
    .btn-play {
      background: var(--gold);
      color: #fff;
      border: none;
      padding: 9px 18px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 0.88rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
    }
    .btn-play:hover { background: #715614; }
    .btn-stop {
      background: #9a4228;
      color: #fff;
      border: none;
      padding: 9px 15px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 0.85rem;
      cursor: pointer;
    }
    .btn-secondary {
      background: var(--surface);
      color: var(--ink);
      border: 1px solid var(--border);
      padding: 8px 14px;
      border-radius: 999px;
      font-weight: 600;
      font-size: 0.82rem;
      cursor: pointer;
      text-decoration: none;
    }
    .btn-secondary:hover { background: var(--surface-elev); }

    .score-card {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px 24px;
      box-shadow: 0 4px 16px rgba(28, 26, 23, 0.05);
      margin-bottom: 24px;
    }
    .score-meta-bar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 14px;
    }
    .score-meta-bar h3 {
      font-family: Georgia, serif;
      font-size: 1.35rem;
      margin: 0 0 4px 0;
    }
    .score-meta-bar .pedagogy-note {
      font-size: 0.88rem;
      color: var(--ink-muted);
      margin: 0;
    }
    .badge-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .meta-badge {
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.76rem;
      font-weight: 600;
      color: var(--ink);
    }
    .meta-badge.highlight {
      background: #fef3c7;
      border-color: #f59e0b;
      color: #78350f;
    }

    #score-paper {
      width: 100%;
      overflow-x: auto;
      min-height: 220px;
    }
    .abcjs-highlight {
      fill: #d97706 !important;
      stroke: #d97706 !important;
    }

    .abc-source-details {
      margin-top: 14px;
      border-top: 1px dashed var(--border);
      padding-top: 10px;
    }
    .abc-source-details summary {
      cursor: pointer;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--gold);
    }
    pre#abc-raw-box {
      background: #1c1a17;
      color: #f7f3e9;
      padding: 12px;
      border-radius: 8px;
      font-size: 0.78rem;
      overflow-x: auto;
      margin-top: 8px;
    }

    .all-schemes-section {
      margin-top: 28px;
    }
    .all-schemes-header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .all-schemes-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(410px, 1fr));
      gap: 16px;
    }
    .mini-scheme-card {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
      transition: transform 0.14s ease, box-shadow 0.14s ease;
    }
    .mini-scheme-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(28, 26, 23, 0.08);
    }
    .mini-scheme-card.active-card {
      border: 2px solid var(--gold);
      background: #fffdf8;
    }
    .mini-scheme-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }
    .mini-scheme-head h4 {
      margin: 0;
      font-size: 0.96rem;
      color: var(--ink);
    }
    .mini-scheme-sub {
      font-size: 0.78rem;
      color: var(--ink-muted);
      margin-bottom: 10px;
    }
    .download-strip {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 20px;
      margin-top: 28px;
    }
    .download-strip h3 {
      margin: 0 0 10px 0;
      font-family: Georgia, serif;
      font-size: 1.1rem;
    }
    .download-links {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
  </style>
</head>
<body>
  <header class="top-nav">
    <div class="brand">
      <span class="brand-badge">FluteModes v2.0</span>
      <h1>Validación de las 840 Variaciones Modales (Taffanel &amp; Gaubert + Reichert Op. 5)</h1>
    </div>
    <nav class="nav-links">
      <a href="propuestas_ux_wizard_modos.html">🎨 Ver 4 Opciones UX (Dashboard, Wizard y Modos)</a>
      <a href="modos_variaciones.html" class="active">🎼 Validar 840 Ejercicios de Modos</a>
      <a href="index.html">🏛️ Portal Principal</a>
    </nav>
  </header>

  <main class="container">
    <section class="hero-banner">
      <div>
        <h2>Laboratorio Completo de Modos Paralelos: 12 Tónicas × 7 Modos × 10 Esquemas Técnicos</h2>
        <p>
          Antes sólo existía el esquema <strong>E.J. 4</strong> para los 84 modos paralelos. Ahora puedes tocar, visualizar y escuchar
          cualquiera de los <strong>84 modos paralelos</strong> bajo todos los esquemas de <strong>Taffanel &amp; Gaubert (E.J. 1, 2, 4, 5, 10 y 11)</strong>
          y <strong>M. A. Reichert Op. 5 (R. 1, 2, 4 y 5)</strong> con sus articulaciones oficiales y tesitura verificada (Si3–Do7).
        </p>
      </div>
      <div class="stats-row">
        <div class="stat-pill"><strong>840</strong><span>Partituras Modales</span></div>
        <div class="stat-pill"><strong>10</strong><span>Esquemas T&amp;G + Reichert</span></div>
        <div class="stat-pill"><strong>12 × 7</strong><span>Tónicas × Modos Paralelos</span></div>
        <div class="stat-pill"><strong>7,896</strong><span>Variantes Articuladas</span></div>
      </div>
    </section>

    <section class="control-grid">
      <div class="control-panel">
        <div class="panel-label">
          <span>1. Selecciona el Esquema Técnico (Taffanel &amp; Gaubert o Reichert Op. 5)</span>
          <span id="active-scheme-source">Alphonse Leduc A. L. 16.588</span>
        </div>
        <div class="scheme-groups">
          <div class="scheme-group-box">
            <div class="scheme-group-title">
              <span>🇫🇷 P. Taffanel &amp; Ph. Gaubert — 17 Grands Exercices Journaliers</span>
              <span>6 Esquemas</span>
            </div>
            <div class="pill-row" id="taffanel-scheme-pills"></div>
          </div>
          <div class="scheme-group-box">
            <div class="scheme-group-title" style="color: var(--indigo);">
              <span>🇧🇪 M. A. Reichert — 7 Exercices Journaliers, Op. 5</span>
              <span>4 Esquemas</span>
            </div>
            <div class="pill-row" id="reichert-scheme-pills"></div>
          </div>
        </div>
      </div>

      <div class="selectors-two-col">
        <div class="control-panel">
          <div class="panel-label">
            <span>2. Selecciona la Tónica Cromática (12 Tónicas: Si3 a Si♭4)</span>
            <span id="active-tonic-label">Do</span>
          </div>
          <div class="pill-row" id="tonic-pills"></div>
        </div>

        <div class="control-panel">
          <div class="panel-label">
            <span>3. Selecciona el Modo Paralelo (Orden Pedagógico por Familia Mayor / Menor)</span>
            <span id="active-family-label">Familia Mayor</span>
          </div>
          <div class="pill-row" id="mode-pills"></div>
        </div>
      </div>
    </section>

    <section class="toolbar-row">
      <div class="toolbar-group">
        <button class="btn-play" id="btn-play-score" type="button">▶ Escuchar Ejercicio Modal</button>
        <button class="btn-stop" id="btn-stop-score" type="button" style="display:none;">⏹ Detener</button>
        <span id="playback-status" style="font-size:0.82rem; font-weight:600; color:var(--gold);">Listo para reproducir</span>
      </div>

      <div class="toolbar-group">
        <label for="art-select">Articulación Oficial:</label>
        <select id="art-select" class="std-select"></select>

        <label for="bpm-input">Tempo (BPM):</label>
        <input id="bpm-input" type="range" min="48" max="144" value="84" style="width:110px;" />
        <span id="bpm-val" style="font-size:0.84rem; font-weight:700; min-width:58px;">84 BPM</span>
      </div>
    </section>

    <section class="score-card">
      <div class="score-meta-bar">
        <div>
          <h3 id="score-title">Do Jónico (Mayor) — E.J. 4</h3>
          <p class="pedagogy-note" id="score-pedagogy"></p>
        </div>
        <div class="badge-row" id="score-badges"></div>
      </div>

      <div id="score-paper"></div>

      <details class="abc-source-details">
        <summary>Ver código fuente ABC exacto de esta variación modal</summary>
        <pre id="abc-raw-box"></pre>
      </details>
    </section>

    <section class="all-schemes-section">
      <div class="all-schemes-header">
        <div>
          <h3 style="margin:0; font-family:Georgia,serif;">Vista Comparativa: Los 10 Esquemas para <span id="compare-mode-label">Do Jónico (Mayor)</span></h3>
          <p style="margin:2px 0 0 0; font-size:0.86rem; color:var(--ink-muted);">
            Haz clic en cualquier tarjeta para cargarla en el reproductor principal o escucharla directamente.
          </p>
        </div>
      </div>
      <div class="all-schemes-grid" id="comparison-grid"></div>
    </section>

    <section class="download-strip">
      <h3>📥 Descarga Directa de las 10 Colecciones Maestras ABC (84 Modos por Esquema = 840 Ejercicios)</h3>
      <div class="download-links">
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_EJ1.abc" download>📄 84 Modos · E.J. 1 (ABC)</a>
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_EJ2.abc" download>📄 84 Modos · E.J. 2 (ABC)</a>
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_EJ4.abc" download>📄 84 Modos · E.J. 4 (ABC)</a>
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_EJ5.abc" download>📄 84 Modos · E.J. 5 (ABC)</a>
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_EJ10.abc" download>📄 84 Modos · E.J. 10 (ABC)</a>
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_EJ11.abc" download>📄 84 Modos · E.J. 11 (ABC)</a>
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_R1.abc" download>📄 84 Modos · Reichert 1 (ABC)</a>
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_R2.abc" download>📄 84 Modos · Reichert 2 (ABC)</a>
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_R4.abc" download>📄 84 Modos · Reichert 4 (ABC)</a>
        <a class="btn-secondary" href="downloads/abc/00_Coleccion_84_Modos_R5.abc" download>📄 84 Modos · Reichert 5 (ABC)</a>
      </div>
    </section>
  </main>

  <script>
    (function() {
      const DATA = window.MODES_VARIATIONS_DATA;
      if (!DATA) return;

      let state = {
        schemeId: "ej1",
        tonicId: "02_do",
        modeNum: 1,
        artId: "a",
        bpm: 84,
      };

      // Parse URL params if provided (e.g. ?scheme=ej10&tonic=04_re&mode=4)
      const params = new URLSearchParams(window.location.search);
      if (params.get("scheme") && DATA.schemes.some(s => s.id === params.get("scheme"))) {
        state.schemeId = params.get("scheme");
      }
      if (params.get("tonic") && DATA.tonics.some(t => t.id === params.get("tonic"))) {
        state.tonicId = params.get("tonic");
      }
      if (params.get("mode") && DATA.modes.some(m => String(m.num) === params.get("mode"))) {
        state.modeNum = parseInt(params.get("mode"), 10);
      }

      let audioCtx = null;
      let activeTimers = [];
      let isPlaying = false;

      function stopPlayback() {
        activeTimers.forEach(id => clearTimeout(id));
        activeTimers = [];
        isPlaying = false;
        document.getElementById("btn-play-score").style.display = "inline-flex";
        document.getElementById("btn-stop-score").style.display = "none";
        document.getElementById("playback-status").textContent = "Listo para reproducir";
        document.querySelectorAll("#score-paper .abcjs-note").forEach(el => el.classList.remove("abcjs-highlight"));
      }

      function playFluteNote(freq, startTime, durationSec, isStaccato) {
        if (!audioCtx) return;
        const osc1 = audioCtx.createOscillator();
        const osc2 = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc1.type = "sine";
        osc2.type = "triangle";
        osc1.frequency.setValueAtTime(freq, startTime);
        osc2.frequency.setValueAtTime(freq * 2, startTime);

        const g2 = audioCtx.createGain();
        g2.gain.setValueAtTime(0.12, startTime);

        const effDur = isStaccato ? Math.max(0.05, durationSec * 0.55) : Math.max(0.07, durationSec * 0.92);
        gain.gain.setValueAtTime(0.001, startTime);
        gain.gain.linearRampToValueAtTime(0.24, startTime + Math.min(0.025, effDur * 0.25));
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + effDur);

        osc1.connect(gain);
        osc2.connect(g2);
        g2.connect(gain);
        gain.connect(audioCtx.destination);

        osc1.start(startTime);
        osc2.start(startTime);
        osc1.stop(startTime + effDur + 0.02);
        osc2.stop(startTime + effDur + 0.02);
      }

      function getCurrentScheme() {
        return DATA.schemes.find(s => s.id === state.schemeId) || DATA.schemes[0];
      }

      function getCurrentExercise() {
        const key = `${state.schemeId}__${state.tonicId}__${state.modeNum}`;
        return DATA.exercises[key];
      }

      function renderSchemePills() {
        const tContainer = document.getElementById("taffanel-scheme-pills");
        const rContainer = document.getElementById("reichert-scheme-pills");
        tContainer.innerHTML = "";
        rContainer.innerHTML = "";

        DATA.schemes.forEach(s => {
          const btn = document.createElement("button");
          const isReichert = s.id.startsWith("r");
          btn.className = "chip" + (isReichert ? " reichert" : "") + (s.id === state.schemeId ? " active" : "");
          btn.innerHTML = `<span>${s.code}</span> <small>${s.meter} · ${s.totalNotes}n</small>`;
          btn.onclick = () => {
            stopPlayback();
            state.schemeId = s.id;
            const arts = DATA.articulationCatalog[s.articulationGroup] || [];
            if (!arts.some(a => a.id === state.artId)) {
              state.artId = "a";
            }
            updateUI();
          };
          if (isReichert) rContainer.appendChild(btn);
          else tContainer.appendChild(btn);
        });
      }

      function renderTonicPills() {
        const container = document.getElementById("tonic-pills");
        container.innerHTML = "";
        DATA.tonics.forEach(t => {
          const btn = document.createElement("button");
          btn.className = "chip" + (t.id === state.tonicId ? " active" : "");
          btn.textContent = t.display;
          btn.onclick = () => {
            stopPlayback();
            state.tonicId = t.id;
            updateUI();
          };
          container.appendChild(btn);
        });
      }

      function renderModePills() {
        const container = document.getElementById("mode-pills");
        container.innerHTML = "";
        DATA.modes.forEach(m => {
          const btn = document.createElement("button");
          btn.className = "chip" + (m.num === state.modeNum ? " active" : "");
          btn.innerHTML = `<span>${m.num}. ${m.name}</span> <small>(${m.family})</small>`;
          btn.onclick = () => {
            stopPlayback();
            state.modeNum = m.num;
            updateUI();
          };
          container.appendChild(btn);
        });
      }

      function renderArticulationSelect() {
        const scheme = getCurrentScheme();
        const arts = DATA.articulationCatalog[scheme.articulationGroup] || [];
        const sel = document.getElementById("art-select");
        sel.innerHTML = "";
        arts.forEach(a => {
          const opt = document.createElement("option");
          opt.value = a.id;
          opt.textContent = `${a.name} — ${a.desc}`;
          if (a.id === state.artId) opt.selected = true;
          sel.appendChild(opt);
        });
      }

      function renderMainScore() {
        const scheme = getCurrentScheme();
        const ex = getCurrentExercise();
        if (!ex) return;

        document.getElementById("active-scheme-source").textContent = `${scheme.tradition} · ${scheme.sourceRef}`;
        document.getElementById("active-tonic-label").textContent = ex.tonicName;
        document.getElementById("active-family-label").textContent = `Familia ${ex.family} (Armadura: K:${ex.keySig})`;

        document.getElementById("score-title").textContent =
          `${ex.tonicDisplay} ${ex.modeName} — Esquema ${scheme.code} (${scheme.title})`;
        document.getElementById("score-pedagogy").textContent = scheme.pedagogy;

        const badgesEl = document.getElementById("score-badges");
        badgesEl.innerHTML = `
          <span class="meta-badge highlight">${ex.badge}</span>
          <span class="meta-badge">Fórmula: ${ex.formula}</span>
          <span class="meta-badge">Armadura: K:${ex.keySig}</span>
          <span class="meta-badge">Compás: ${scheme.meter}</span>
          <span class="meta-badge">${ex.totalNotes} notas (MIDI ${ex.minMidi}–${ex.maxMidi})</span>
        `;

        const abcStr = (ex.abcByArticulation && ex.abcByArticulation[state.artId]) || ex.abc;
        document.getElementById("abc-raw-box").textContent = abcStr;

        if (window.ABCJS) {
          ABCJS.renderAbc("score-paper", abcStr, {
            responsive: "resize",
            staffwidth: 1080,
            scale: 0.95,
            add_classes: true,
          });
        }
      }

      function renderComparisonGrid() {
        const grid = document.getElementById("comparison-grid");
        grid.innerHTML = "";
        const currentEx = getCurrentExercise();
        if (currentEx) {
          document.getElementById("compare-mode-label").textContent =
            `${currentEx.tonicDisplay} ${currentEx.modeName}`;
        }

        DATA.schemes.forEach((s, idx) => {
          const ex = DATA.exercises[`${s.id}__${state.tonicId}__${state.modeNum}`];
          if (!ex) return;
          const card = document.createElement("div");
          card.className = "mini-scheme-card" + (s.id === state.schemeId ? " active-card" : "");
          const paperId = `mini-paper-${idx}`;
          card.innerHTML = `
            <div class="mini-scheme-head">
              <h4>${s.code} · ${s.shortName}</h4>
              <span class="meta-badge">${s.meter} · ${s.totalNotes} notas</span>
            </div>
            <div class="mini-scheme-sub">${s.title}</div>
            <div id="${paperId}" style="overflow-x:auto;"></div>
            <div style="margin-top:8px; display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:0.75rem; color:var(--ink-muted);">${ex.badge}</span>
              <button type="button" class="btn-secondary" data-scheme="${s.id}">Seleccionar y Escuchar →</button>
            </div>
          `;
          card.querySelector("button").onclick = () => {
            stopPlayback();
            state.schemeId = s.id;
            updateUI();
            window.scrollTo({ top: 0, behavior: "smooth" });
          };
          grid.appendChild(card);

          if (window.ABCJS) {
            ABCJS.renderAbc(paperId, ex.abc, {
              responsive: "resize",
              staffwidth: 520,
              scale: 0.68,
            });
          }
        });
      }

      function startPlayback() {
        stopPlayback();
        const ex = getCurrentExercise();
        const scheme = getCurrentScheme();
        if (!ex) return;

        if (!audioCtx) {
          const AudioContextClass = window.AudioContext || window.webkitAudioContext;
          audioCtx = new AudioContextClass();
        }
        if (audioCtx.state === "suspended") {
          audioCtx.resume();
        }

        isPlaying = true;
        document.getElementById("btn-play-score").style.display = "none";
        document.getElementById("btn-stop-score").style.display = "inline-flex";

        const bpm = state.bpm;
        let noteDur = (60 / bpm) / 4; // default 1/16
        if (scheme.id === "ej4") {
          noteDur = (60 / bpm) / 2;
        } else if (scheme.id === "r5") {
          noteDur = (60 / bpm) / 6; // sixteenth triplets
        } else if (scheme.meter === "6/8" || scheme.meter === "9/8") {
          noteDur = (60 / bpm) / 3;
        }

        const abcStr = (ex.abcByArticulation && ex.abcByArticulation[state.artId]) || ex.abc;
        const bodyText = abcStr
          .split("\n")
          .filter(line => !/^[XTCMQLK]:|^%/.test(line.trim()))
          .join(" ");
        const noteStaccatos = Array.from(
          bodyText.matchAll(/(\.?)(?:\^\^|__|[\^_=])?[A-Ga-g][',]*/g),
          m => m[1] === "."
        );
        const freqs = ex.frequencies;
        const noteEls = Array.from(document.querySelectorAll("#score-paper .abcjs-note"));
        const baseTime = audioCtx.currentTime + 0.08;

        freqs.forEach((f, idx) => {
          const isLast = idx === freqs.length - 1;
          const dur = isLast ? noteDur * 2.5 : noteDur;
          const tStart = baseTime + idx * noteDur;
          const noteIsStaccato = !isLast && Boolean(noteStaccatos[idx]);
          playFluteNote(f, tStart, dur, noteIsStaccato);

          const delayMs = Math.max(0, (tStart - audioCtx.currentTime) * 1000);
          const tid = setTimeout(() => {
            if (!isPlaying) return;
            document.getElementById("playback-status").textContent =
              `Reproduciendo nota ${idx + 1}/${freqs.length} (${f.toFixed(1)} Hz)`;
            noteEls.forEach(el => el.classList.remove("abcjs-highlight"));
            if (noteEls[idx]) noteEls[idx].classList.add("abcjs-highlight");
          }, delayMs);
          activeTimers.push(tid);
        });

        const totalMs = (freqs.length * noteDur + 0.4) * 1000;
        activeTimers.push(setTimeout(() => stopPlayback(), totalMs));
      }

      function updateUI() {
        renderSchemePills();
        renderTonicPills();
        renderModePills();
        renderArticulationSelect();
        renderMainScore();
        renderComparisonGrid();
      }

      document.getElementById("art-select").addEventListener("change", (e) => {
        stopPlayback();
        state.artId = e.target.value;
        renderMainScore();
      });

      document.getElementById("bpm-input").addEventListener("input", (e) => {
        state.bpm = parseInt(e.target.value, 10) || 84;
        document.getElementById("bpm-val").textContent = `${state.bpm} BPM`;
      });

      document.getElementById("btn-play-score").addEventListener("click", startPlayback);
      document.getElementById("btn-stop-score").addEventListener("click", stopPlayback);

      updateUI();
    })();
  </script>
</body>
</html>
"""

PROPUESTAS_UX_HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FluteModes v2.0 · Investigación de Usabilidad (Stitch) — 4 Opciones de Dashboard, Wizard y Modos</title>
  <script src="abcjs-basic-min.js"></script>
  <script src="modes_variations_data.js"></script>
  <style>
    :root {
      --bg: #fdfbf7;
      --surface: #f7f3e9;
      --ink: #1c1a17;
      --ink-muted: #5c5346;
      --gold: #8c6d1f;
      --gold-bright: #d4af37;
      --border: #ddd6c6;
      --radius: 14px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Plus Jakarta Sans", "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.55;
    }
    header.top-nav {
      background: #181410;
      color: #fdfbf7;
      padding: 14px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      border-bottom: 2px solid var(--gold-bright);
      position: sticky;
      top: 0;
      z-index: 60;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-badge {
      background: var(--gold-bright);
      color: #181410;
      font-weight: 800;
      font-size: 0.78rem;
      padding: 4px 10px;
      border-radius: 999px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }
    .brand h1 {
      font-family: Georgia, serif;
      font-size: 1.22rem;
      margin: 0;
      font-weight: 600;
    }
    .nav-links {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }
    .nav-links a, .nav-links button {
      color: #fdfbf7;
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      padding: 7px 14px;
      border-radius: 999px;
      border: 1px solid rgba(212, 175, 55, 0.45);
      background: rgba(255, 255, 255, 0.06);
      cursor: pointer;
    }
    .nav-links a:hover, .nav-links a.active, .nav-links button.cta-wiz {
      background: var(--gold-bright);
      color: #181410;
      border-color: var(--gold-bright);
    }

    .container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 24px 24px 70px;
    }

    /* Usability Research Findings Section */
    .research-box {
      background: #fff;
      border: 1px solid var(--border);
      border-left: 5px solid var(--gold);
      border-radius: var(--radius);
      padding: 20px 24px;
      margin-bottom: 24px;
      box-shadow: 0 4px 14px rgba(28, 26, 23, 0.04);
    }
    .research-box h2 {
      font-family: Georgia, serif;
      margin: 0 0 8px 0;
      font-size: 1.45rem;
    }
    .findings-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }
    .finding-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
    }
    .finding-card h4 {
      margin: 0 0 6px 0;
      font-size: 0.95rem;
      color: var(--gold);
    }
    .finding-card p {
      margin: 0;
      font-size: 0.86rem;
      color: var(--ink-muted);
    }

    /* 4 Options Comparison Cards */
    .options-overview-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 18px;
      margin-bottom: 28px;
    }
    .opt-card {
      background: #fff;
      border: 2px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: all 0.16s ease;
      cursor: pointer;
    }
    .opt-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 24px rgba(28, 26, 23, 0.09);
    }
    .opt-card.selected {
      border-color: var(--gold);
      box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.35);
    }
    .opt-thumb-wrap {
      position: relative;
      height: 210px;
      background: #181410;
      overflow: hidden;
      border-bottom: 1px solid var(--border);
    }
    .opt-thumb-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
      transition: transform 0.3s ease;
    }
    .opt-card:hover .opt-thumb-wrap img {
      transform: scale(1.03);
    }
    .opt-tag {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(24, 20, 16, 0.86);
      color: var(--gold-bright);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 0.74rem;
      font-weight: 700;
      border: 1px solid rgba(212, 175, 55, 0.5);
    }
    .opt-body {
      padding: 16px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .opt-body h3 {
      font-family: Georgia, serif;
      font-size: 1.12rem;
      margin: 0 0 6px 0;
    }
    .opt-body p {
      font-size: 0.84rem;
      color: var(--ink-muted);
      margin: 0 0 10px 0;
    }
    .opt-specs {
      list-style: none;
      padding: 0;
      margin: 0 0 12px 0;
      font-size: 0.8rem;
    }
    .opt-specs li {
      margin-bottom: 4px;
    }
    .opt-btn {
      width: 100%;
      padding: 9px 12px;
      border-radius: 8px;
      border: 1px solid var(--gold);
      background: var(--surface);
      color: var(--ink);
      font-weight: 700;
      font-size: 0.83rem;
      cursor: pointer;
    }
    .opt-card.selected .opt-btn {
      background: var(--gold);
      color: #fff;
    }

    /* Interactive Prototype Simulator */
    .simulator-shell {
      border-radius: 18px;
      padding: 24px;
      border: 2px solid var(--border);
      transition: all 0.25s ease;
      margin-bottom: 32px;
    }
    /* Theme classes for the 4 Options */
    .simulator-shell.theme-opt1 {
      background: #fdfbf7;
      color: #1c1a17;
      border-color: #d4af37;
      --sim-card: #f7f3e9;
      --sim-accent: #8c6d1f;
      --sim-accent-fg: #ffffff;
      --sim-border: #ddd6c6;
      --sim-muted: #5c5346;
    }
    .simulator-shell.theme-opt2 {
      background: #0f141c;
      color: #dee2ee;
      border-color: #e5c158;
      --sim-card: #1b2028;
      --sim-accent: #e5c158;
      --sim-accent-fg: #181410;
      --sim-border: #30353e;
      --sim-muted: #a6adbb;
    }
    .simulator-shell.theme-opt3 {
      background: #f6f5f0;
      color: #1b1c19;
      border-color: #1e3a8a;
      --sim-card: #ffffff;
      --sim-accent: #1e3a8a;
      --sim-accent-fg: #ffffff;
      --sim-border: #c5c5d3;
      --sim-muted: #444651;
    }
    .simulator-shell.theme-opt4 {
      background: #f8fafc;
      color: #191c1e;
      border-color: #0d9488;
      --sim-card: #ffffff;
      --sim-accent: #0d9488;
      --sim-accent-fg: #ffffff;
      --sim-border: #cbd5e1;
      --sim-muted: #475569;
    }

    .sim-header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--sim-border);
      margin-bottom: 20px;
    }
    .sim-layout {
      display: grid;
      grid-template-columns: 1fr 1.35fr;
      gap: 20px;
    }
    @media (max-width: 1024px) {
      .sim-layout { grid-template-columns: 1fr; }
    }
    .sim-panel {
      background: var(--sim-card);
      border: 1px solid var(--sim-border);
      border-radius: 14px;
      padding: 18px;
    }
    .sim-panel h3 {
      margin: 0 0 10px 0;
      font-family: Georgia, serif;
      font-size: 1.15rem;
    }
    .sim-cta-btn {
      background: var(--sim-accent);
      color: var(--sim-accent-fg);
      border: none;
      padding: 10px 18px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 0.86rem;
      cursor: pointer;
    }
    .sim-routine-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px;
      margin-top: 12px;
    }
    .sim-mini-card {
      padding: 12px;
      border-radius: 10px;
      border: 1px solid var(--sim-border);
      background: rgba(128, 128, 128, 0.06);
      cursor: pointer;
    }
    .sim-mini-card:hover {
      border-color: var(--sim-accent);
    }
    .sim-chip-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 10px;
    }
    .sim-chip {
      padding: 6px 11px;
      border-radius: 999px;
      border: 1px solid var(--sim-border);
      background: transparent;
      color: inherit;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
    }
    .sim-chip.active {
      background: var(--sim-accent);
      color: var(--sim-accent-fg);
      border-color: var(--sim-accent);
    }
    #sim-score-paper {
      background: #ffffff;
      color: #1c1a17;
      border-radius: 10px;
      padding: 10px;
      min-height: 190px;
      overflow-x: auto;
    }

    /* Native Dialog for the 3-Step Practice Wizard (modern-web-guidance: closedby="any") */
    dialog#practice-wizard-dialog {
      max-width: 680px;
      width: 92vw;
      border: 2px solid var(--gold);
      border-radius: 18px;
      padding: 0;
      background: var(--bg);
      color: var(--ink);
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
    }
    dialog#practice-wizard-dialog::backdrop {
      background: rgba(15, 20, 28, 0.65);
      backdrop-filter: blur(3px);
    }
    .wiz-head {
      background: #181410;
      color: #fdfbf7;
      padding: 16px 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--gold-bright);
    }
    .wiz-head h3 {
      margin: 0;
      font-family: Georgia, serif;
      font-size: 1.2rem;
    }
    .wiz-body {
      padding: 20px 24px;
    }
    .wiz-step {
      margin-bottom: 16px;
    }
    .wiz-step-label {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--gold);
      margin-bottom: 8px;
    }
    .wiz-options {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 8px;
    }
    .wiz-opt-btn {
      padding: 10px 12px;
      border-radius: 10px;
      border: 1.5px solid var(--border);
      background: #fff;
      color: var(--ink);
      text-align: left;
      cursor: pointer;
      font-size: 0.83rem;
      font-weight: 600;
    }
    .wiz-opt-btn.active {
      border-color: var(--gold);
      background: #fef3c7;
      color: #78350f;
    }
    .wiz-result-box {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 4px solid var(--gold);
      border-radius: 10px;
      padding: 14px 16px;
      margin-top: 14px;
    }
    .wiz-foot {
      padding: 14px 24px;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: var(--surface);
    }
  </style>
</head>
<body>
  <header class="top-nav">
    <div class="brand">
      <span class="brand-badge">Stitch Research · Project 14323574806802443450</span>
      <h1>Investigación de Usabilidad: 4 Opciones de Dashboard, Wizard y Modos (Taffanel + Reichert)</h1>
    </div>
    <nav class="nav-links">
      <button type="button" class="cta-wiz" id="open-wizard-top">✨ Probar Wizard de Práctica (3 Pasos)</button>
      <a href="modos_variaciones.html">🎼 Validar las 840 Partituras de Modos</a>
      <a href="index.html">🏛️ Portal Principal</a>
    </nav>
  </header>

  <main class="container">
    <!-- Hallazgos de la investigación de usabilidad -->
    <section class="research-box">
      <h2>1. Diagnóstico de Usabilidad de la Pantalla Inicial Actual y Solución Propuesta</h2>
      <p style="margin:0; font-size:0.92rem; color:var(--ink-muted);">
        Al analizar la pantalla inicial actual de <code>FluteModes</code> (`HomeView.swift`) junto con el feedback de usuarios reales,
        identificamos tres cuellos de botella cognitivos y funcionales que resuelven las 4 opciones diseñadas en <strong>Stitch</strong>:
      </p>
      <div class="findings-grid">
        <div class="finding-card">
          <h4>⚠️ Problema 1: Sobrecarga de Elección (Ley de Hick)</h4>
          <p>
            La pantalla actual muestra 12 botones de ejercicios al mismo nivel jerárquico (84 Modos, E.J. 1, 2, 4, 5, 10, 11, R. 1, 2, 4, 5)
            más selectores de tónica y modo. El estudiante abre la app y no sabe por dónde empezar ni cómo armar su sesión diaria.
          </p>
        </div>
        <div class="finding-card">
          <h4>✨ Solución: Practice Wizard Guiado (3 Pasos)</h4>
          <p>
            Un asistente interactivo que pregunta <strong>1) Tiempo disponible (15/30/45 min)</strong>,
            <strong>2) Meta técnica del día (Sonido/Escalas, Arpegios, Modos o Velocidad)</strong> y
            <strong>3) Tónica del Día</strong>, generando una rutina de 3 bloques lista para tocar con un solo toque.
          </p>
        </div>
        <div class="finding-card">
          <h4>🎼 Solución: Pantalla de Modos 84 × 10 Esquemas</h4>
          <p>
            En lugar de limitar los 84 Modos Paralelos al esquema <strong>E.J. 4</strong>, la nueva pantalla de Modos integra un
            selector de esquema técnico para tocar cualquier modo bajo <strong>Taffanel (E.J. 1, 2, 4, 5, 10, 11)</strong> y
            <strong>Reichert (R. 1, 2, 4, 5)</strong> = <strong>840 ejercicios modales</strong>.
          </p>
        </div>
      </div>
    </section>

    <!-- Las 4 Opciones generadas en Stitch -->
    <h2 style="font-family:Georgia,serif; margin:0 0 12px 0;">2. Comparativa de las 4 Opciones de Diseño (Haz clic en cualquiera para probarla en vivo abajo)</h2>
    <section class="options-overview-grid" id="options-cards-container">
      <!-- Option 1 -->
      <article class="opt-card selected" data-opt="opt1">
        <div class="opt-thumb-wrap">
          <span class="opt-tag">Opción 1 (Recomendada) · Urtext Parchment</span>
          <img src="stitch_options/option1_conservatory_coach.png" alt="Opción 1 Conservatory Guided Coach" />
        </div>
        <div class="opt-body">
          <div>
            <h3>Opción 1: Conservatory Guided Coach</h3>
            <p>Estética Urtext en pergamino cálido (<code>#FDFBF7</code>) y oro antiguo (<code>#D4AF37</code>). Mantiene la identidad clásica de Henle/Leduc pero simplifica el inicio.</p>
            <ul class="opt-specs">
              <li>✅ <strong>Dashboard:</strong> Tarjeta Hero <em>«¿Qué practicar hoy?»</em> + botón de 1 toque para continuar la última sesión y 3 tarjetas de foco.</li>
              <li>✅ <strong>Wizard:</strong> Modal limpio de 3 pasos con generador de rutina de 3 bloques (Calentamiento + Modos + Arpegios).</li>
              <li>✅ <strong>Pantalla de Modos:</strong> Selector de 12 tónicas + 7 modos + barra doble de chips para Taffanel (1, 2, 4, 5, 10, 11) y Reichert (1, 2, 4, 5).</li>
            </ul>
          </div>
          <button type="button" class="opt-btn">Probar Opción 1 en el Simulador ↓</button>
        </div>
      </article>

      <!-- Option 2 -->
      <article class="opt-card" data-opt="opt2">
        <div class="opt-thumb-wrap">
          <span class="opt-tag">Opción 2 · OLED Concert Hall (Dark)</span>
          <img src="stitch_options/option2_dark_stage_studio.png" alt="Opción 2 Dark Stage Focus Studio" />
        </div>
        <div class="opt-body">
          <div>
            <h3>Opción 2: Dark Stage Focus Studio</h3>
            <p>Estética nocturna de atril de concierto en obsidiana (<code>#0F141C</code>) y oro champán (<code>#E5C158</code>) para eliminar fatiga visual en estudio prolongado.</p>
            <ul class="opt-specs">
              <li>✅ <strong>Dashboard:</strong> 3 tarjetas de rutina directa por tiempo (<em>15m Express, 30m Conservatorio, 45m Maestría</em>).</li>
              <li>✅ <strong>Wizard:</strong> Asistente diagnóstico integrado en bandeja desplegable (Inline Drawer) sin cambiar de pantalla.</li>
              <li>✅ <strong>Pantalla de Modos:</strong> Conmutador segmentado <code>[Taffanel 1·2·4·5·10·11]</code> vs <code>[Reichert 1·2·4·5]</code> con partitura de alto contraste.</li>
            </ul>
          </div>
          <button type="button" class="opt-btn">Probar Opción 2 en el Simulador ↓</button>
        </div>
      </article>

      <!-- Option 3 -->
      <article class="opt-card" data-opt="opt3">
        <div class="opt-thumb-wrap">
          <span class="opt-tag">Opción 3 · Split-Workbench &amp; Matriz 2D</span>
          <img src="stitch_options/option3_editorial_workbench.png" alt="Opción 3 Editorial Split-Workbench" />
        </div>
        <div class="opt-body">
          <div>
            <h3>Opción 3: Editorial Split-Workbench</h3>
            <p>Banco de trabajo de doble panel en crema editorial (<code>#F6F5F0</code>) e índigo real (<code>#1E3A8A</code>), ideal para iPad/Tablet horizontal y Desktop.</p>
            <ul class="opt-specs">
              <li>✅ <strong>Dashboard:</strong> Barra lateral con Rueda Cromática de 12 Tónicas y diagnóstico rápido de técnica diaria.</li>
              <li>✅ <strong>Wizard:</strong> Diagnóstico técnico (<em>¿Qué sientes hoy en tu embocadura y mecanismo?</em>) con prescripción algorítmica.</li>
              <li>✅ <strong>Pantalla de Modos:</strong> Matriz bidimensional interactiva <strong>7 Modos × 10 Esquemas</strong> siempre visible junto al pentagrama.</li>
            </ul>
          </div>
          <button type="button" class="opt-btn">Probar Opción 3 en el Simulador ↓</button>
        </div>
      </article>

      <!-- Option 4 -->
      <article class="opt-card" data-opt="opt4">
        <div class="opt-thumb-wrap">
          <span class="opt-tag">Opción 4 · Mastery Rings &amp; 4 Pestañas</span>
          <img src="stitch_options/option4_nordic_mastery_rings.png" alt="Opción 4 Progressive Mastery Rings" />
        </div>
        <div class="opt-body">
          <div>
            <h3>Opción 4: Mastery Rings &amp; 4-Tab Nav</h3>
            <p>Arquitectura moderna nórdica en alabastro (<code>#F8FAFC</code>), esmeralda (<code>#0D9488</code>) y ámbar (<code>#D97706</code>) con barra inferior de 4 pestañas.</p>
            <ul class="opt-specs">
              <li>✅ <strong>Dashboard:</strong> 3 Anillos de Dominio Diario (<em>Escalas, Arpegios, Modos</em>) y separación en 4 pestañas (<code>Hoy | Wizard | Modos | Método</code>).</li>
              <li>✅ <strong>Wizard:</strong> Flujo conversacional tipo tarjetas con seguimiento de racha y cobertura de las 12 tónicas.</li>
              <li>✅ <strong>Pantalla de Modos:</strong> Tarjetas agrupadas por compás (<code>4/2</code>, <code>6/8</code>, <code>9/8</code>, <code>2/4</code>, <code>4/4</code>) con insignias de conteo de notas.</li>
            </ul>
          </div>
          <button type="button" class="opt-btn">Probar Opción 4 en el Simulador ↓</button>
        </div>
      </article>
    </section>

    <!-- Simulador Interactivo en Vivo de la Opción Seleccionada -->
    <section class="simulator-shell theme-opt1" id="live-simulator">
      <div class="sim-header">
        <div>
          <span style="font-size:0.76rem; font-weight:800; text-transform:uppercase; letter-spacing:0.08em;" id="sim-badge">
            Simulador Interactivo en Vivo · Opción 1 Seleccionada
          </span>
          <h2 style="margin:4px 0 0 0; font-family:Georgia,serif;" id="sim-title">
            Opción 1: Conservatory Guided Coach (Urtext Parchment &amp; Gold)
          </h2>
        </div>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
          <button type="button" class="sim-cta-btn" id="sim-open-wizard">✨ Abrir Practice Wizard (3 Pasos)</button>
          <a href="modos_variaciones.html" class="sim-cta-btn" style="text-decoration:none; opacity:0.9;">🎼 Ir al Visor de 840 Modos →</a>
        </div>
      </div>

      <div class="sim-layout">
        <!-- Columna Izquierda: Dashboard + Rutina Sugerida -->
        <div class="sim-panel">
          <h3 id="sim-dash-heading">Dashboard Inicial Simplificado: ¿Qué practicar hoy?</h3>
          <p style="font-size:0.86rem; color:var(--sim-muted); margin:0 0 12px 0;" id="sim-dash-sub">
            En lugar de 12 botones compitiendo por atención, el Dashboard ofrece continuidad inmediata o una rutina guiada según tu tiempo:
          </p>

          <div class="sim-routine-cards">
            <div class="sim-mini-card" data-preset="express">
              <strong>⏱️ 15 min · Express</strong>
              <div style="font-size:0.78rem; color:var(--sim-muted); margin-top:4px;">
                Pentacordios E.J. 1 + Modo del día en R. 1 (6/8)
              </div>
            </div>
            <div class="sim-mini-card" data-preset="conservatorio">
              <strong>🏛️ 30 min · Conservatorio</strong>
              <div style="font-size:0.78rem; color:var(--sim-muted); margin-top:4px;">
                Escala Modal E.J. 4 + Arpegio Modal E.J. 10 + Reichert Nº 2
              </div>
            </div>
            <div class="sim-mini-card" data-preset="maestria">
              <strong>👑 45 min · Maestría</strong>
              <div style="font-size:0.78rem; color:var(--sim-muted); margin-top:4px;">
                Ciclo Completo: E.J. 2, E.J. 5, E.J. 11 y Reichert Nº 5 (Tresillos)
              </div>
            </div>
          </div>

          <div style="margin-top:16px; padding-top:14px; border-top:1px solid var(--sim-border);">
            <div style="font-size:0.8rem; font-weight:700; margin-bottom:8px;">
              📋 Rutina Activa Generada por el Wizard (<span id="active-routine-label">30 min · Conservatorio en Re Dórico</span>):
            </div>
            <div id="sim-routine-steps" style="display:grid; gap:8px;"></div>
          </div>
        </div>

        <!-- Columna Derecha: Nueva Pantalla de Modos con los 10 Esquemas -->
        <div class="sim-panel">
          <h3>Nueva Pantalla de Modos: 84 Modos × 10 Esquemas (Taffanel + Reichert)</h3>
          <div style="font-size:0.78rem; color:var(--sim-muted); margin-bottom:6px;">Tónica Cromática:</div>
          <div class="sim-chip-bar" id="sim-tonic-bar"></div>

          <div style="font-size:0.78rem; color:var(--sim-muted); margin-bottom:6px;">Modo Paralelo (7 Modos):</div>
          <div class="sim-chip-bar" id="sim-mode-bar"></div>

          <div style="font-size:0.78rem; color:var(--sim-muted); margin-bottom:6px;">
            Esquema Técnico — <strong>Taffanel (1, 2, 4, 5, 10, 11)</strong> y <strong>Reichert (1, 2, 4, 5)</strong>:
          </div>
          <div class="sim-chip-bar" id="sim-scheme-bar"></div>

          <div style="display:flex; justify-content:space-between; align-items:center; margin:10px 0;">
            <strong id="sim-score-label" style="font-size:0.92rem;">Re Dórico — E.J. 10 (Arpegios 6/8)</strong>
            <button type="button" class="sim-cta-btn" id="sim-play-btn" style="padding:6px 14px; font-size:0.8rem;">▶ Escuchar</button>
          </div>

          <div id="sim-score-paper"></div>
        </div>
      </div>
    </section>
  </main>

  <!-- Diálogo Nativo del Practice Wizard con closedby="any" (modern-web-guidance: platform-controls-dismiss-dialog) -->
  <dialog id="practice-wizard-dialog" closedby="any">
    <div class="wiz-head">
      <h3>✨ Asistente de Práctica Guiada (Practice Wizard · 3 Pasos)</h3>
      <button type="button" id="wiz-close-btn" style="background:transparent; border:1px solid #d4af37; color:#fdfbf7; border-radius:999px; padding:4px 12px; cursor:pointer;">✕ Cerrar</button>
    </div>
    <div class="wiz-body">
      <div class="wiz-step">
        <div class="wiz-step-label">Paso 1 · ¿Cuánto tiempo tienes para practicar hoy?</div>
        <div class="wiz-options" id="wiz-time-opts">
          <button type="button" class="wiz-opt-btn" data-time="15">⏱️ 15 min<br/><small>Mantenimiento Express</small></button>
          <button type="button" class="wiz-opt-btn active" data-time="30">🏛️ 30 min<br/><small>Sesión Conservatorio</small></button>
          <button type="button" class="wiz-opt-btn" data-time="45">👑 45 min<br/><small>Dominio Integral</small></button>
        </div>
      </div>

      <div class="wiz-step">
        <div class="wiz-step-label">Paso 2 · ¿Qué aspecto técnico quieres priorizar?</div>
        <div class="wiz-options" id="wiz-focus-opts">
          <button type="button" class="wiz-opt-btn" data-focus="escalas">🎵 Igualdad Digital<br/><small>E.J. 1, E.J. 2, E.J. 4, E.J. 5</small></button>
          <button type="button" class="wiz-opt-btn active" data-focus="arpegios">🎶 Flexibilidad y Arpegios<br/><small>E.J. 10, E.J. 11, R. 2, R. 4</small></button>
          <button type="button" class="wiz-opt-btn" data-focus="reichert">⚡ Agilidad y Saltos<br/><small>Reichert R. 1, R. 2, R. 4, R. 5</small></button>
        </div>
      </div>

      <div class="wiz-step">
        <div class="wiz-step-label">Paso 3 · Tónica y Modo Principal de la Sesión</div>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
          <select id="wiz-tonic-select" style="padding:8px 12px; border-radius:8px; border:1px solid var(--border); font-weight:600;"></select>
          <select id="wiz-mode-select" style="padding:8px 12px; border-radius:8px; border:1px solid var(--border); font-weight:600;"></select>
        </div>
      </div>

      <div class="wiz-result-box" id="wiz-preview-box"></div>
    </div>
    <div class="wiz-foot">
      <span style="font-size:0.78rem; color:var(--ink-muted);">Puedes cerrar este diálogo con ESC o clic fuera (<code>closedby="any"</code>)</span>
      <button type="button" class="sim-cta-btn" id="wiz-apply-btn" style="background:var(--gold); color:#fff;">Aplicar Rutina y Empezar a Tocar →</button>
    </div>
  </dialog>

  <script>
    (function() {
      const DATA = window.MODES_VARIATIONS_DATA;
      if (!DATA) return;

      const OPT_META = {
        opt1: {
          theme: "theme-opt1",
          badge: "Simulador Interactivo en Vivo · Opción 1 Seleccionada (Recomendada)",
          title: "Opción 1: Conservatory Guided Coach (Urtext Parchment & Gold)",
          dashHeading: "Dashboard Inicial: Hero Coach «¿Qué practicar hoy?» + Continuar Sesión",
        },
        opt2: {
          theme: "theme-opt2",
          badge: "Simulador Interactivo en Vivo · Opción 2 Seleccionada (Dark Stage)",
          title: "Opción 2: Dark Stage Focus Studio (OLED Concert Hall #0F141C)",
          dashHeading: "Dashboard Nocturno de Atril: 3 Rutinas por Tiempo + Wizard Inline",
        },
        opt3: {
          theme: "theme-opt3",
          badge: "Simulador Interactivo en Vivo · Opción 3 Seleccionada (Split-Workbench)",
          title: "Opción 3: Editorial Split-Workbench & Matriz Modal 7×10",
          dashHeading: "Panel Izquierdo de Trabajo: Rueda Cromática + Diagnóstico Técnico",
        },
        opt4: {
          theme: "theme-opt4",
          badge: "Simulador Interactivo en Vivo · Opción 4 Seleccionada (4-Tab & Rings)",
          title: "Opción 4: Progressive Mastery Rings & Arquitectura de 4 Pestañas",
          dashHeading: "Pestaña «Hoy»: 3 Anillos de Dominio Diario + Asistente Conversacional",
        }
      };

      let simState = {
        opt: "opt1",
        tonicId: "04_re",
        modeNum: 4, // Dórico
        schemeId: "ej10",
        wizTime: "30",
        wizFocus: "arpegios",
        routineBlocks: [
          { schemeId: "ej1", label: "Bloque 1 (Calentamiento · 8 min): Pentacordios Modales E.J. 1" },
          { schemeId: "ej10", label: "Bloque 2 (Núcleo · 12 min): Arpegios Modales Diatónicos E.J. 10 en 6/8" },
          { schemeId: "r2", label: "Bloque 3 (Agilidad · 10 min): Reichert Op. 5 Nº 2 en 2/4" },
        ]
      };

      let audioCtx = null;
      let simTimers = [];

      function stopSimAudio() {
        simTimers.forEach(t => clearTimeout(t));
        simTimers = [];
        document.getElementById("sim-play-btn").textContent = "▶ Escuchar";
      }

      function playSimScore() {
        if (simTimers.length > 0) {
          stopSimAudio();
          return;
        }
        const ex = DATA.exercises[`${simState.schemeId}__${simState.tonicId}__${simState.modeNum}`];
        if (!ex) return;
        if (!audioCtx) {
          const AC = window.AudioContext || window.webkitAudioContext;
          audioCtx = new AC();
        }
        if (audioCtx.state === "suspended") audioCtx.resume();

        document.getElementById("sim-play-btn").textContent = "⏹ Detener";
        const noteDur = 0.16;
        const t0 = audioCtx.currentTime + 0.05;
        ex.frequencies.slice(0, 48).forEach((f, i) => {
          const osc = audioCtx.createOscillator();
          const g = audioCtx.createGain();
          osc.type = "sine";
          osc.frequency.setValueAtTime(f, t0 + i * noteDur);
          g.gain.setValueAtTime(0.001, t0 + i * noteDur);
          g.gain.linearRampToValueAtTime(0.2, t0 + i * noteDur + 0.02);
          g.gain.exponentialRampToValueAtTime(0.001, t0 + (i + 0.9) * noteDur);
          osc.connect(g);
          g.connect(audioCtx.destination);
          osc.start(t0 + i * noteDur);
          osc.stop(t0 + (i + 0.95) * noteDur);
        });
        simTimers.push(setTimeout(() => stopSimAudio(), Math.min(48, ex.frequencies.length) * noteDur * 1000 + 200));
      }

      function buildRoutineBlocks(time, focus) {
        if (focus === "escalas") {
          return [
            { schemeId: "ej1", label: `Bloque 1 (${time === "15" ? "5" : "10"} min): Pentacordios por Grados E.J. 1` },
            { schemeId: "ej4", label: `Bloque 2 (${time === "15" ? "5" : "10"} min): Escalas Modales por Terceras E.J. 4` },
            { schemeId: "ej5", label: `Bloque 3 (${time === "15" ? "5" : "10"} min): Escala Continua en 6/8 E.J. 5` },
          ];
        } else if (focus === "reichert") {
          return [
            { schemeId: "r1", label: `Bloque 1 (${time === "15" ? "5" : "10"} min): Reichert Op. 5 Nº 1 en 6/8` },
            { schemeId: "r4", label: `Bloque 2 (${time === "15" ? "5" : "10"} min): Reichert Op. 5 Nº 4 (Bordaduras Modales)` },
            { schemeId: "r5", label: `Bloque 3 (${time === "15" ? "5" : "10"} min): Reichert Op. 5 Nº 5 (Tresillos con Pedal)` },
          ];
        }
        return [
          { schemeId: "ej2", label: `Bloque 1 (${time === "15" ? "5" : "10"} min): Pentacordios con Giro E.J. 2` },
          { schemeId: "ej10", label: `Bloque 2 (${time === "15" ? "5" : "10"} min): Arpegios Modales en 6/8 E.J. 10` },
          { schemeId: "ej11", label: `Bloque 3 (${time === "15" ? "5" : "10"} min): Arpegios Quebrados en 9/8 E.J. 11` },
        ];
      }

      function renderSimulator() {
        const meta = OPT_META[simState.opt];
        const shell = document.getElementById("live-simulator");
        shell.className = `simulator-shell ${meta.theme}`;
        document.getElementById("sim-badge").textContent = meta.badge;
        document.getElementById("sim-title").textContent = meta.title;
        document.getElementById("sim-dash-heading").textContent = meta.dashHeading;

        // Render routine blocks
        const stepsContainer = document.getElementById("sim-routine-steps");
        stepsContainer.innerHTML = "";
        simState.routineBlocks.forEach(b => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "sim-mini-card";
          btn.style.textAlign = "left";
          btn.style.color = "inherit";
          btn.style.borderColor = (b.schemeId === simState.schemeId) ? "var(--sim-accent)" : "var(--sim-border)";
          btn.innerHTML = `<strong>${b.label}</strong> <span style="float:right; font-size:0.78rem;">Cargar →</span>`;
          btn.onclick = () => {
            stopSimAudio();
            simState.schemeId = b.schemeId;
            renderSimulator();
          };
          stepsContainer.appendChild(btn);
        });

        // Render tonic chips
        const tBar = document.getElementById("sim-tonic-bar");
        tBar.innerHTML = "";
        DATA.tonics.forEach(t => {
          const b = document.createElement("button");
          b.type = "button";
          b.className = "sim-chip" + (t.id === simState.tonicId ? " active" : "");
          b.textContent = t.display;
          b.onclick = () => { stopSimAudio(); simState.tonicId = t.id; renderSimulator(); };
          tBar.appendChild(b);
        });

        // Render mode chips
        const mBar = document.getElementById("sim-mode-bar");
        mBar.innerHTML = "";
        DATA.modes.forEach(m => {
          const b = document.createElement("button");
          b.type = "button";
          b.className = "sim-chip" + (m.num === simState.modeNum ? " active" : "");
          b.textContent = `${m.num}. ${m.name}`;
          b.onclick = () => { stopSimAudio(); simState.modeNum = m.num; renderSimulator(); };
          mBar.appendChild(b);
        });

        // Render scheme chips (all 10: Taffanel 1,2,4,5,10,11 + Reichert 1,2,4,5)
        const sBar = document.getElementById("sim-scheme-bar");
        sBar.innerHTML = "";
        DATA.schemes.forEach(s => {
          const b = document.createElement("button");
          b.type = "button";
          b.className = "sim-chip" + (s.id === simState.schemeId ? " active" : "");
          b.textContent = `${s.code} (${s.meter})`;
          b.onclick = () => { stopSimAudio(); simState.schemeId = s.id; renderSimulator(); };
          sBar.appendChild(b);
        });

        const ex = DATA.exercises[`${simState.schemeId}__${simState.tonicId}__${simState.modeNum}`];
        const scheme = DATA.schemes.find(s => s.id === simState.schemeId);
        if (ex && scheme) {
          document.getElementById("sim-score-label").textContent =
            `${ex.tonicDisplay} ${ex.modeName} — ${scheme.title} (${ex.totalNotes} notas)`;
          document.getElementById("active-routine-label").textContent =
            `${simState.wizTime} min · ${ex.tonicDisplay} ${ex.modeName}`;
          if (window.ABCJS) {
            ABCJS.renderAbc("sim-score-paper", ex.abc, {
              responsive: "resize",
              staffwidth: 680,
              scale: 0.82,
            });
          }
        }
      }

      // Option card selection
      document.querySelectorAll(".opt-card").forEach(card => {
        card.addEventListener("click", () => {
          document.querySelectorAll(".opt-card").forEach(c => c.classList.remove("selected"));
          card.classList.add("selected");
          simState.opt = card.getAttribute("data-opt");
          renderSimulator();
          document.getElementById("live-simulator").scrollIntoView({ behavior: "smooth", block: "nearest" });
        });
      });

      // Preset routine cards in simulator
      document.querySelectorAll("[data-preset]").forEach(card => {
        card.addEventListener("click", () => {
          const p = card.getAttribute("data-preset");
          if (p === "express") {
            simState.wizTime = "15";
            simState.wizFocus = "escalas";
          } else if (p === "conservatorio") {
            simState.wizTime = "30";
            simState.wizFocus = "arpegios";
          } else {
            simState.wizTime = "45";
            simState.wizFocus = "reichert";
          }
          simState.routineBlocks = buildRoutineBlocks(simState.wizTime, simState.wizFocus);
          simState.schemeId = simState.routineBlocks[0].schemeId;
          renderSimulator();
        });
      });

      document.getElementById("sim-play-btn").addEventListener("click", playSimScore);

      // Setup Practice Wizard Dialog
      const dialog = document.getElementById("practice-wizard-dialog");
      const wizTonicSel = document.getElementById("wiz-tonic-select");
      const wizModeSel = document.getElementById("wiz-mode-select");

      DATA.tonics.forEach(t => {
        const o = document.createElement("option");
        o.value = t.id;
        o.textContent = `Tónica: ${t.name}`;
        if (t.id === simState.tonicId) o.selected = true;
        wizTonicSel.appendChild(o);
      });
      DATA.modes.forEach(m => {
        const o = document.createElement("option");
        o.value = m.num;
        o.textContent = `Modo ${m.num}: ${m.name} (${m.family})`;
        if (m.num === simState.modeNum) o.selected = true;
        wizModeSel.appendChild(o);
      });

      function updateWizardPreview() {
        const blocks = buildRoutineBlocks(simState.wizTime, simState.wizFocus);
        const tObj = DATA.tonics.find(t => t.id === wizTonicSel.value) || DATA.tonics[0];
        const mObj = DATA.modes.find(m => String(m.num) === String(wizModeSel.value)) || DATA.modes[0];
        document.getElementById("wiz-preview-box").innerHTML = `
          <strong>🎯 Plan Generado (${simState.wizTime} min) en ${tObj.display} ${mObj.name}:</strong>
          <ul style="margin:6px 0 0 18px; padding:0; font-size:0.84rem;">
            ${blocks.map(b => `<li>${b.label}</li>`).join("")}
          </ul>
        `;
      }

      document.querySelectorAll("#wiz-time-opts .wiz-opt-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          document.querySelectorAll("#wiz-time-opts .wiz-opt-btn").forEach(b => b.classList.remove("active"));
          btn.classList.add("active");
          simState.wizTime = btn.getAttribute("data-time");
          updateWizardPreview();
        });
      });

      document.querySelectorAll("#wiz-focus-opts .wiz-opt-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          document.querySelectorAll("#wiz-focus-opts .wiz-opt-btn").forEach(b => b.classList.remove("active"));
          btn.classList.add("active");
          simState.wizFocus = btn.getAttribute("data-focus");
          updateWizardPreview();
        });
      });

      wizTonicSel.addEventListener("change", updateWizardPreview);
      wizModeSel.addEventListener("change", updateWizardPreview);

      function openWizard() {
        updateWizardPreview();
        if (typeof dialog.showModal === "function") dialog.showModal();
        else dialog.setAttribute("open", "open");
      }

      document.getElementById("open-wizard-top").addEventListener("click", openWizard);
      document.getElementById("sim-open-wizard").addEventListener("click", openWizard);
      document.getElementById("wiz-close-btn").addEventListener("click", () => dialog.close());
      document.getElementById("wiz-apply-btn").addEventListener("click", () => {
        simState.tonicId = wizTonicSel.value;
        simState.modeNum = parseInt(wizModeSel.value, 10);
        simState.routineBlocks = buildRoutineBlocks(simState.wizTime, simState.wizFocus);
        simState.schemeId = simState.routineBlocks[0].schemeId;
        dialog.close();
        renderSimulator();
      });

      renderSimulator();
    })();
  </script>
</body>
</html>
"""


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    # Write docs/modos_variaciones.html and docs/propuestas_ux_wizard_modos.html
    modos_var_docs = os.path.join(docs_dir, "modos_variaciones.html")
    with open(modos_var_docs, "w", encoding="utf-8") as f:
        f.write(MODOS_VARIACIONES_HTML)

    ux_docs = os.path.join(docs_dir, "propuestas_ux_wizard_modos.html")
    with open(ux_docs, "w", encoding="utf-8") as f:
        f.write(PROPUESTAS_UX_HTML)

    # Also write root-level convenience copies (with adjusted script/asset paths if opened from root)
    root_modos_html = MODOS_VARIACIONES_HTML.replace(
        'src="modes_variations_data.js"', 'src="docs/modes_variations_data.js"'
    ).replace(
        'href="propuestas_ux_wizard_modos.html"', 'href="docs/propuestas_ux_wizard_modos.html"'
    ).replace(
        'href="modos_variaciones.html"', 'href="docs/modos_variaciones.html"'
    ).replace(
        'href="index.html"', 'href="docs/index.html"'
    ).replace(
        'href="downloads/abc/', 'href="docs/downloads/abc/'
    )
    with open(os.path.join(base_dir, "validacion_modos_taffanel_reichert.html"), "w", encoding="utf-8") as f:
        f.write(root_modos_html)

    root_ux_html = PROPUESTAS_UX_HTML.replace(
        'src="modes_variations_data.js"', 'src="docs/modes_variations_data.js"'
    ).replace(
        'src="stitch_options/', 'src="docs/stitch_options/'
    ).replace(
        'href="modos_variaciones.html"', 'href="docs/modos_variaciones.html"'
    ).replace(
        'href="index.html"', 'href="docs/index.html"'
    )
    with open(os.path.join(base_dir, "propuestas_ux_wizard_modos.html"), "w", encoding="utf-8") as f:
        f.write(root_ux_html)

    print("Páginas interactivas generadas con éxito:")
    print(" -", modos_var_docs)
    print(" -", ux_docs)
    print(" -", os.path.join(base_dir, "validacion_modos_taffanel_reichert.html"))
    print(" -", os.path.join(base_dir, "propuestas_ux_wizard_modos.html"))


if __name__ == "__main__":
    main()
