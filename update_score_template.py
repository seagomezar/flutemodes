#!/usr/bin/env python3
"""
Actualiza score_template.html en iOS (FluteModes) y Android (FluteModesAndroid)
con los renderizadores Urtext completos de E. J. 5, E. J. 10 y E. J. 11,
y exporta los arreglos MIDI por sección para Swift y Kotlin.
"""

import os
import json
import shutil

from generate_ej5_validation import scales_js_data as ej5_scales, EJ5_ARTICULATIONS_META as ej5_arts
from generate_ej10_validation import ALL_MEASURES as ej10_measures, sections_js_data as ej10_sections, EJ10_ARTICULATIONS_META as ej10_arts
from generate_ej11_validation import ALL_MEASURES as ej11_measures, sections_js_data as ej11_sections, EJ11_ARTICULATIONS_META as ej11_arts

ROOT_DIR = "/Users/sebas/Desktop/partituras"
DOCS_PDF_DIR = os.path.join(ROOT_DIR, "docs", "downloads", "pdf")
os.makedirs(DOCS_PDF_DIR, exist_ok=True)

for pdf_name in ["taffanel_ej5_transcripcion.pdf", "taffanel_ej10_transcripcion.pdf", "taffanel_ej11_transcripcion.pdf"]:
    src = os.path.join(ROOT_DIR, pdf_name)
    dst = os.path.join(DOCS_PDF_DIR, pdf_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"✅ Copiado {pdf_name} -> docs/downloads/pdf/")

IOS_TEMPLATE = os.path.join(ROOT_DIR, "FluteModes/FluteModes/Resources/score_template.html")
ANDROID_TEMPLATE = os.path.join(ROOT_DIR, "FluteModesAndroid/app/src/main/assets/score_template.html")

with open(IOS_TEMPLATE, "r", encoding="utf-8") as f:
    html = f.read()

# Si ya tenía un bloque previo de EJ5/10/11, lo reemplazamos limpiamente
if "// === BEGIN EJ5_10_11 LEDUC ===" in html:
    s_idx = html.index("// === BEGIN EJ5_10_11 LEDUC ===")
    e_idx = html.index("// === END EJ5_10_11 LEDUC ===") + len("// === END EJ5_10_11 LEDUC ===")
    html = html[:s_idx] + html[e_idx:]

ej5_scales_json = json.dumps(ej5_scales, ensure_ascii=False)
ej5_arts_json = json.dumps(ej5_arts, ensure_ascii=False)

# Para EJ10 y EJ11 guardamos solo los campos necesarios para el renderizador compacto y rápido
ej10_compact_measures = [
    {
        "m": m["measureNum"],
        "s": m["sectionIdx"],
        "sh": m["sectionShort"],
        "n": m["notes12"],
        "end": m["isSectionEnd"]
    }
    for m in ej10_measures
]
ej11_compact_measures = [
    {
        "m": m["measureNum"],
        "s": m["sectionIdx"],
        "sh": m["sectionShort"],
        "n": m["notes18"],
        "end": m["isSectionEnd"]
    }
    for m in ej11_measures
]

ej10_measures_json = json.dumps(ej10_compact_measures, ensure_ascii=False)
ej10_sections_json = json.dumps(ej10_sections, ensure_ascii=False)
ej10_arts_json = json.dumps(ej10_arts, ensure_ascii=False)

ej11_measures_json = json.dumps(ej11_compact_measures, ensure_ascii=False)
ej11_sections_json = json.dumps(ej11_sections, ensure_ascii=False)
ej11_arts_json = json.dumps(ej11_arts, ensure_ascii=False)

js_injection = f"""// === BEGIN EJ5_10_11 LEDUC ===
    const EJ5_SCALES_DATA = {ej5_scales_json};
    const EJ5_ARTS_DATA = {ej5_arts_json};
    const EJ10_MEASURES_DATA = {ej10_measures_json};
    const EJ10_SECTIONS_DATA = {ej10_sections_json};
    const EJ10_ARTS_DATA = {ej10_arts_json};
    const EJ11_MEASURES_DATA = {ej11_measures_json};
    const EJ11_SECTIONS_DATA = {ej11_sections_json};
    const EJ11_ARTS_DATA = {ej11_arts_json};

    const EJ5_10_ART_ROW1_ABC = [
      "X:101",
      "M:6/8",
      "L:1/16",
      "K:C",
      "V:1 clef=treble stem=down",
      '"^1" (cccccc cccccc) || "^2" (cccccc) (cccccc) || "^3" (cccc).c.c (cccc).c.c || "^4" .c.c(cccc) .c.c(cccc) || "^5" (cc).c.c.c.c (cc).c.c.c.c ||'
    ].join("\\n");

    const EJ5_10_ART_ROW2_ABC = [
      "X:102",
      "M:2/4",
      "L:1/16",
      "K:C",
      "V:1 clef=treble stem=down",
      '"^6" (ccc) (ccc) (ccc) (ccc) || "^7" (ccc) .c.c.c (ccc) .c.c.c || [M:6/8] "^8" (cc)(cc)(cc) (cc)(cc)(cc) || "^9" .c(cc)(cc)(c c)(cc)(cc).c || "^10" .c.c.c.c.c.c .c.c.c.c.c.c ||'
    ].join("\\n");

    const EJ11_ART_ROW1_ABC = [
      "X:101",
      "M:9/8",
      "L:1/16",
      "K:C",
      "V:1 clef=treble stem=down",
      '"^1" (cccccc cccccc cccccc) || "^2" (cccccc) (cccccc) (cccccc) || "^3" (cccc).c.c (cccc).c.c (cccc).c.c || "^4" .c.c(cccc) .c.c(cccc) .c.c(cccc) || "^5" (cc).c.c.c.c (cc).c.c.c.c (cc).c.c.c.c ||'
    ].join("\\n");

    const EJ11_ART_ROW2_ABC = [
      "X:102",
      "M:3/4",
      "L:1/16",
      "K:C",
      "V:1 clef=treble stem=down",
      '"^6" (ccc)(ccc) (ccc)(ccc) (ccc)(ccc) || "^7" (ccc).c.c.c (ccc).c.c.c (ccc).c.c.c || [M:9/8] "^8" (cc)(cc)(cc) (cc)(cc)(cc) (cc)(cc)(cc) || "^9" .c(cc)(cc)(c c)(cc)(cc)(c c)(cc)(cc).c || "^10" .c.c.c.c.c.c .c.c.c.c.c.c .c.c.c.c.c.c ||'
    ].join("\\n");

    function formatEj5_10Measure12(n, artId) {{
      switch (artId) {{
        case 0:  return n.slice(0,6).join("") + " " + n.slice(6,12).join("");
        case 1:  return "(" + n.slice(0,6).join("") + " " + n.slice(6,12).join("") + ")";
        case 2:  return "(" + n.slice(0,6).join("") + ") (" + n.slice(6,12).join("") + ")";
        case 3:  return `(${{n[0]}}${{n[1]}}${{n[2]}}${{n[3]}}).${{n[4]}}.${{n[5]}} (${{n[6]}}${{n[7]}}${{n[8]}}${{n[9]}}).${{n[10]}}.${{n[11]}}`;
        case 4:  return `.${{n[0]}}.${{n[1]}}(${{n[2]}}${{n[3]}}${{n[4]}}${{n[5]}}) .${{n[6]}}.${{n[7]}}(${{n[8]}}${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 5:  return `(${{n[0]}}${{n[1]}}).${{n[2]}}.${{n[3]}}.${{n[4]}}.${{n[5]}} (${{n[6]}}${{n[7]}}).${{n[8]}}.${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        case 6:  return `(${{n[0]}}${{n[1]}}${{n[2]}}) (${{n[3]}}${{n[4]}}${{n[5]}}) (${{n[6]}}${{n[7]}}${{n[8]}}) (${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 7:  return `(${{n[0]}}${{n[1]}}${{n[2]}}) .${{n[3]}}.${{n[4]}}.${{n[5]}} (${{n[6]}}${{n[7]}}${{n[8]}}) .${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        case 8:  return `(${{n[0]}}${{n[1]}})(${{n[2]}}${{n[3]}})(${{n[4]}}${{n[5]}}) (${{n[6]}}${{n[7]}})(${{n[8]}}${{n[9]}})(${{n[10]}}${{n[11]}})`;
        case 9:  return `.${{n[0]}}(${{n[1]}}${{n[2]}})(${{n[3]}}${{n[4]}})(${{n[5]}} ${{n[6]}})(${{n[7]}}${{n[8]}})(${{n[9]}}${{n[10]}}).${{n[11]}}`;
        case 10: return n.slice(0,6).map(x => "." + x).join("") + " " + n.slice(6,12).map(x => "." + x).join("");
        default: return n.slice(0,6).join("") + " " + n.slice(6,12).join("");
      }}
    }}

    function formatEj11Measure18(n, artId) {{
      switch (artId) {{
        case 0:  return n.slice(0,6).join("") + " " + n.slice(6,12).join("") + " " + n.slice(12,18).join("");
        case 1:  return "(" + n.slice(0,6).join("") + " " + n.slice(6,12).join("") + " " + n.slice(12,18).join("") + ")";
        case 2:  return "(" + n.slice(0,6).join("") + ") (" + n.slice(6,12).join("") + ") (" + n.slice(12,18).join("") + ")";
        case 3:  return `(${{n[0]}}${{n[1]}}${{n[2]}}${{n[3]}}).${{n[4]}}.${{n[5]}} (${{n[6]}}${{n[7]}}${{n[8]}}${{n[9]}}).${{n[10]}}.${{n[11]}} (${{n[12]}}${{n[13]}}${{n[14]}}${{n[15]}}).${{n[16]}}.${{n[17]}}`;
        case 4:  return `.${{n[0]}}.${{n[1]}}(${{n[2]}}${{n[3]}}${{n[4]}}${{n[5]}}) .${{n[6]}}.${{n[7]}}(${{n[8]}}${{n[9]}}${{n[10]}}${{n[11]}}) .${{n[12]}}.${{n[13]}}(${{n[14]}}${{n[15]}}${{n[16]}}${{n[17]}})`;
        case 5:  return `(${{n[0]}}${{n[1]}}).${{n[2]}}.${{n[3]}}.${{n[4]}}.${{n[5]}} (${{n[6]}}${{n[7]}}).${{n[8]}}.${{n[9]}}.${{n[10]}}.${{n[11]}} (${{n[12]}}${{n[13]}}).${{n[14]}}.${{n[15]}}.${{n[16]}}.${{n[17]}}`;
        case 6:  return `(${{n[0]}}${{n[1]}}${{n[2]}})(${{n[3]}}${{n[4]}}${{n[5]}}) (${{n[6]}}${{n[7]}}${{n[8]}})(${{n[9]}}${{n[10]}}${{n[11]}}) (${{n[12]}}${{n[13]}}${{n[14]}})(${{n[15]}}${{n[16]}}${{n[17]}})`;
        case 7:  return `(${{n[0]}}${{n[1]}}${{n[2]}}).${{n[3]}}.${{n[4]}}.${{n[5]}} (${{n[6]}}${{n[7]}}${{n[8]}}).${{n[9]}}.${{n[10]}}.${{n[11]}} (${{n[12]}}${{n[13]}}${{n[14]}}).${{n[15]}}.${{n[16]}}.${{n[17]}}`;
        case 8:  return `(${{n[0]}}${{n[1]}})(${{n[2]}}${{n[3]}})(${{n[4]}}${{n[5]}}) (${{n[6]}}${{n[7]}})(${{n[8]}}${{n[9]}})(${{n[10]}}${{n[11]}}) (${{n[12]}}${{n[13]}})(${{n[14]}}${{n[15]}})(${{n[16]}}${{n[17]}})`;
        case 9:  return `.${{n[0]}}(${{n[1]}}${{n[2]}})(${{n[3]}}${{n[4]}})(${{n[5]}} ${{n[6]}})(${{n[7]}}${{n[8]}})(${{n[9]}}${{n[10]}})(${{n[11]}} ${{n[12]}})(${{n[13]}}${{n[14]}})(${{n[15]}}${{n[16]}}).${{n[17]}}`;
        case 10: return n.slice(0,6).map(x => "." + x).join("") + " " + n.slice(6,12).map(x => "." + x).join("") + " " + n.slice(12,18).map(x => "." + x).join("");
        default: return n.slice(0,6).join("") + " " + n.slice(6,12).join("") + " " + n.slice(12,18).join("");
      }}
    }}

    function buildEj5SingleScaleAbc(scaleIdx, artId, includeTimeSig) {{
      const sc = EJ5_SCALES_DATA[scaleIdx] || EJ5_SCALES_DATA[0];
      const art = EJ5_ARTS_DATA[artId] || EJ5_ARTS_DATA[0];
      const meterStr = includeTimeSig ? art.meter : "none";
      const b1 = formatEj5_10Measure12(sc.m1, artId);
      const b2 = formatEj5_10Measure12(sc.m2, artId);
      const b3 = formatEj5_10Measure12(sc.m3, artId);
      const b4 = formatEj5_10Measure12(sc.m4, artId);
      const b5 = `${{sc.m5}}4 z4 |`;
      return [
        `X:${{scaleIdx + 1}}`,
        "%%stretchlast 1",
        `M:${{meterStr}}`,
        "L:1/16",
        `K:${{sc.keySig}}`,
        "V:1 clef=treble stem=down",
        `"${{sc.letter}}" ${{b1}} | ${{b2}} | ${{b3}} | ${{b4}} | ${{b5}}]`
      ].join("\\n");
    }}

    function renderEj5Leduc(artId, secIdx) {{
      const paper = document.getElementById("paper");
      const art = EJ5_ARTS_DATA[artId] || EJ5_ARTS_DATA[0];
      const sc = EJ5_SCALES_DATA[secIdx] || EJ5_SCALES_DATA[0];

      let html = `
        <div class="ej1-leduc-wrapper">
          <div class="ej1-top-header">
            <div class="ej1-title">E. J. 5 — <em>GAMMES CHROMATIQUES (${{sc.titleEs}})</em></div>
            <div class="ej1-active-badge">${{art.name}} (${{art.meter}})</div>
          </div>
          <div class="ej1-subtitle">A travailler successivement avec chacune des articulations suivantes:</div>
          <div id="ej5-art-row-1" class="ej1-art-row" style="border-bottom:none; margin-bottom:0;"></div>
          <div id="ej5-art-row-2" class="ej1-art-row"></div>
      `;
      for (let i = 0; i < EJ5_SCALES_DATA.length; i++) {{
        const highlight = (i === secIdx) ? "background:#eff6ff; border-left:3px solid #2563eb; padding-left:4px; border-radius:4px;" : "";
        html += `<div id="ej5-scale-row-${{i}}" class="ej1-staff-row" style="${{highlight}}"></div>`;
      }}
      html += `<div class="ej1-plate-footer">A. L. 16.588</div></div>`;
      paper.innerHTML = html;

      ABCJS.renderAbc("ej5-art-row-1", EJ5_10_ART_ROW1_ABC, {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      ABCJS.renderAbc("ej5-art-row-2", EJ5_10_ART_ROW2_ABC, {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});

      for (let i = 0; i < EJ5_SCALES_DATA.length; i++) {{
        ABCJS.renderAbc(`ej5-scale-row-${{i}}`, buildEj5SingleScaleAbc(i, artId, i === 0), {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      }}
      const activeRow = document.getElementById(`ej5-scale-row-${{secIdx}}`);
      window.activeSectionNotes = activeRow ? Array.from(activeRow.querySelectorAll(".abcjs-note")) : [];
      if (secIdx > 0 && activeRow) {{
        setTimeout(() => activeRow.scrollIntoView({{ behavior: "smooth", block: "center" }}), 60);
      }}
    }}

    function buildEj10SystemAbc(sysIdx, artId) {{
      const art = EJ10_ARTS_DATA[artId] || EJ10_ARTS_DATA[0];
      const meterStr = sysIdx === 0 ? art.meter : "none";
      const startM = sysIdx * 4;
      const slice = EJ10_MEASURES_DATA.slice(startM, startM + 4);
      const bars = slice.map(mObj => {{
        const bTxt = formatEj5_10Measure12(mObj.n, artId);
        const barline = mObj.end ? "||" : "|";
        return `${{bTxt}} ${{barline}}`;
      }});
      if (sysIdx === 29) bars.push("B4 z4 |]");
      return [
        `X:${{sysIdx + 1}}`,
        "%%stretchlast 1",
        `M:${{meterStr}}`,
        "L:1/16",
        "K:C",
        "V:1 clef=treble",
        bars.join(" ")
      ].join("\\n");
    }}

    function renderEj10Leduc(artId, secIdx) {{
      const paper = document.getElementById("paper");
      const art = EJ10_ARTS_DATA[artId] || EJ10_ARTS_DATA[0];
      const sec = EJ10_SECTIONS_DATA[secIdx] || EJ10_SECTIONS_DATA[0];

      let html = `
        <div class="ej1-leduc-wrapper">
          <div class="ej1-top-header">
            <div class="ej1-title">E. J. 10 — <em>ARPÈGES (${{sec.titleEs}})</em></div>
            <div class="ej1-active-badge">${{art.name}} (${{art.meter}})</div>
          </div>
          <div class="ej1-subtitle">A travailler successivement avec chacune des articulations suivantes:</div>
          <div id="ej10-art-row-1" class="ej1-art-row" style="border-bottom:none; margin-bottom:0;"></div>
          <div id="ej10-art-row-2" class="ej1-art-row"></div>
          <div style="font-size:11px; font-weight:bold; color:#334155; margin:4px 4px 2px 4px;">Pág. 120 (Sistemas 1–14 · c. 1–56)</div>
      `;
      const startM = secIdx * 10 + 1;
      const endM = (secIdx === 11) ? 121 : secIdx * 10 + 10;
      for (let s = 0; s < 30; s++) {{
        if (s === 14) {{
          html += `<div style="font-size:11px; font-weight:bold; color:#334155; margin:10px 4px 2px 4px; border-top:1px dashed #cbd5e1; padding-top:6px;">Pág. 121 (Sistemas 15–30 · c. 57–121)</div>`;
        }}
        const sysStart = s * 4 + 1;
        const sysEnd = (s === 29) ? 121 : s * 4 + 4;
        const hl = (sysStart <= endM && sysEnd >= startM) ? "background:#eff6ff; border-left:3px solid #2563eb; padding-left:4px; border-radius:4px;" : "";
        html += `<div id="ej10-sys-${{s}}" class="ej1-staff-row" style="${{hl}}"></div>`;
      }}
      html += `<div class="ej1-plate-footer">A. L. 16.588</div></div>`;
      paper.innerHTML = html;

      ABCJS.renderAbc("ej10-art-row-1", EJ5_10_ART_ROW1_ABC, {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      ABCJS.renderAbc("ej10-art-row-2", EJ5_10_ART_ROW2_ABC, {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});

      const allSysNotes = [];
      for (let s = 0; s < 30; s++) {{
        const divId = `ej10-sys-${{s}}`;
        ABCJS.renderAbc(divId, buildEj10SystemAbc(s, artId), {{ staffwidth: s === 29 ? 1020 : 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
        const sysEl = document.getElementById(divId);
        if (sysEl) {{
          const sNotes = sysEl.querySelectorAll(".abcjs-note");
          for (let k = 0; k < sNotes.length; k++) allSysNotes.push(sNotes[k]);
        }}
      }}
      const startNote = secIdx * 120;
      const endNote = (secIdx === 11) ? startNote + 121 : startNote + 120;
      window.activeSectionNotes = allSysNotes.slice(startNote, endNote);
      if (secIdx > 0 && window.activeSectionNotes.length > 0) {{
        setTimeout(() => window.activeSectionNotes[0].scrollIntoView({{ behavior: "smooth", block: "center" }}), 60);
      }}
    }}

    function buildEj11SystemAbc(sysIdx, artId) {{
      const art = EJ11_ARTS_DATA[artId] || EJ11_ARTS_DATA[0];
      const meterStr = sysIdx === 0 ? art.meter : "none";
      const startM = sysIdx * 2;
      const slice = EJ11_MEASURES_DATA.slice(startM, startM + 2);
      const bars = slice.map(mObj => {{
        const bTxt = formatEj11Measure18(mObj.n, artId);
        const barline = mObj.end ? "||" : "|";
        return `${{bTxt}} ${{barline}}`;
      }});
      if (sysIdx === 59) bars.push("B4 z4 z10 |]");
      return [
        `X:${{sysIdx + 1}}`,
        "%%stretchlast 1",
        `M:${{meterStr}}`,
        "L:1/16",
        "K:C",
        "V:1 clef=treble",
        bars.join(" ")
      ].join("\\n");
    }}

    function renderEj11Leduc(artId, secIdx) {{
      const paper = document.getElementById("paper");
      const art = EJ11_ARTS_DATA[artId] || EJ11_ARTS_DATA[0];
      const sec = EJ11_SECTIONS_DATA[secIdx] || EJ11_SECTIONS_DATA[0];

      let html = `
        <div class="ej1-leduc-wrapper">
          <div class="ej1-top-header">
            <div class="ej1-title">E. J. 11 — <em>ARPÈGES BRISÉS (${{sec.titleEs}})</em></div>
            <div class="ej1-active-badge">${{art.name}} (${{art.meter}})</div>
          </div>
          <div class="ej1-subtitle">A travailler successivement avec chacune des articulations suivantes:</div>
          <div id="ej11-art-row-1" class="ej1-art-row" style="border-bottom:none; margin-bottom:0;"></div>
          <div id="ej11-art-row-2" class="ej1-art-row"></div>
          <div style="font-size:11px; font-weight:bold; color:#334155; margin:4px 4px 2px 4px;">Pág. 122 (Sistemas 1–14 · c. 1–28)</div>
      `;
      const startM = secIdx * 10 + 1;
      const endM = (secIdx === 11) ? 121 : secIdx * 10 + 10;
      for (let s = 0; s < 60; s++) {{
        if (s === 14) {{
          html += `<div style="font-size:11px; font-weight:bold; color:#334155; margin:10px 4px 2px 4px; border-top:1px dashed #cbd5e1; padding-top:6px;">Pág. 123 (Sistemas 15–30 · c. 29–60)</div>`;
        }} else if (s === 30) {{
          html += `<div style="font-size:11px; font-weight:bold; color:#334155; margin:10px 4px 2px 4px; border-top:1px dashed #cbd5e1; padding-top:6px;">Pág. 124 (Sistemas 31–45 · c. 61–90)</div>`;
        }} else if (s === 45) {{
          html += `<div style="font-size:11px; font-weight:bold; color:#334155; margin:10px 4px 2px 4px; border-top:1px dashed #cbd5e1; padding-top:6px;">Pág. 125 (Sistemas 46–60 · c. 91–121)</div>`;
        }}
        const sysStart = s * 2 + 1;
        const sysEnd = (s === 59) ? 121 : s * 2 + 2;
        const hl = (sysStart <= endM && sysEnd >= startM) ? "background:#eff6ff; border-left:3px solid #2563eb; padding-left:4px; border-radius:4px;" : "";
        html += `<div id="ej11-sys-${{s}}" class="ej1-staff-row" style="${{hl}}"></div>`;
      }}
      html += `<div class="ej1-plate-footer">A. L. 16.588</div></div>`;
      paper.innerHTML = html;

      ABCJS.renderAbc("ej11-art-row-1", EJ11_ART_ROW1_ABC, {{ staffwidth: 980, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      ABCJS.renderAbc("ej11-art-row-2", EJ11_ART_ROW2_ABC, {{ staffwidth: 980, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});

      const allSysNotes = [];
      for (let s = 0; s < 60; s++) {{
        const divId = `ej11-sys-${{s}}`;
        ABCJS.renderAbc(divId, buildEj11SystemAbc(s, artId), {{ staffwidth: s === 59 ? 1020 : 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
        const sysEl = document.getElementById(divId);
        if (sysEl) {{
          const sNotes = sysEl.querySelectorAll(".abcjs-note");
          for (let k = 0; k < sNotes.length; k++) allSysNotes.push(sNotes[k]);
        }}
      }}
      const startNote = secIdx * 180;
      const endNote = (secIdx === 11) ? startNote + 181 : startNote + 180;
      window.activeSectionNotes = allSysNotes.slice(startNote, endNote);
      if (secIdx > 0 && window.activeSectionNotes.length > 0) {{
        setTimeout(() => window.activeSectionNotes[0].scrollIntoView({{ behavior: "smooth", block: "center" }}), 60);
      }}
    }}
// === END EJ5_10_11 LEDUC ===
"""

# Insertar antes de function renderScore(abcString)
target_render_score = """    function renderScore(abcString) {
      const ej4Match = abcString && abcString.match(/%\\s*EJ4_LEDUC_ART:(\\d+):SEC:(\\d+)/);"""

replacement_render_score = js_injection + """
    function renderScore(abcString) {
      window.activeSectionNotes = null;
      const ej5Match = abcString && abcString.match(/%\\s*EJ5_LEDUC_ART:(\\d+):SEC:(\\d+)/);
      if (ej5Match) {
        const artId = parseInt(ej5Match[1], 10) || 0;
        const secIdx = parseInt(ej5Match[2], 10) || 0;
        renderEj5Leduc(artId, secIdx);
        normalizeAllSvgs();
        return;
      }
      const ej10Match = abcString && abcString.match(/%\\s*EJ10_LEDUC_ART:(\\d+):SEC:(\\d+)/);
      if (ej10Match) {
        const artId = parseInt(ej10Match[1], 10) || 0;
        const secIdx = parseInt(ej10Match[2], 10) || 0;
        renderEj10Leduc(artId, secIdx);
        normalizeAllSvgs();
        return;
      }
      const ej11Match = abcString && abcString.match(/%\\s*EJ11_LEDUC_ART:(\\d+):SEC:(\\d+)/);
      if (ej11Match) {
        const artId = parseInt(ej11Match[1], 10) || 0;
        const secIdx = parseInt(ej11Match[2], 10) || 0;
        renderEj11Leduc(artId, secIdx);
        normalizeAllSvgs();
        return;
      }
      const ej4Match = abcString && abcString.match(/%\\s*EJ4_LEDUC_ART:(\\d+):SEC:(\\d+)/);"""

# Si ya tenía ej5Match, primero limpiamos
if "const ej5Match =" in html:
    s2 = html.index("    function renderScore(abcString) {")
    e2 = html.index("      const ej4Match = abcString && abcString.match(/%\\s*EJ4_LEDUC_ART:(\\d+):SEC:(\\d+)/);")
    html = html[:s2] + "    function renderScore(abcString) {\n" + html[e2:]

assert target_render_score in html, "No se encontró target_render_score en score_template.html"
html = html.replace(target_render_score, replacement_render_score, 1)

for out_path in [IOS_TEMPLATE, ANDROID_TEMPLATE]:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Actualizado {out_path} ({len(html)} bytes)")

# También exportar los MIDI arrays de EJ5, EJ10 y EJ11 para Swift y Kotlin
ej5_midi_by_sec = [sc["midis"] for sc in ej5_scales]
ej10_midi_by_sec = []
ej11_midi_by_sec = []
for sec_idx in range(12):
    m10 = []
    for m_obj in ej10_measures[sec_idx * 10 : (sec_idx + 1) * 10]:
        m10.extend(m_obj["midis12"])
    if sec_idx == 11:
        m10.append(71)  # Si4 final (c. 121)
    ej10_midi_by_sec.append(m10)

    m11 = []
    for m_obj in ej11_measures[sec_idx * 10 : (sec_idx + 1) * 10]:
        m11.extend(m_obj["midis18"])
    if sec_idx == 11:
        m11.append(71)  # Si4 final (c. 121)
    ej11_midi_by_sec.append(m11)

with open("/tmp/ej5_10_11_midis.json", "w", encoding="utf-8") as f:
    json.dump({
        "ej5": ej5_midi_by_sec,
        "ej10": ej10_midi_by_sec,
        "ej11": ej11_midi_by_sec,
    }, f)
print("✅ Exportados arreglos MIDI de EJ5, EJ10 y EJ11 en /tmp/ej5_10_11_midis.json")
