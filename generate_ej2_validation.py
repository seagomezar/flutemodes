import os
import re
import json
import shutil

ARTIFACT_DIR = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"
SCORE_TEMPLATE_PATH = "/Users/sebas/Desktop/partituras/FluteModes/FluteModes/Resources/score_template.html"

with open(SCORE_TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template_html = f.read()

script_matches = re.findall(r"<script>([\s\S]*?)</script>", template_html)
abcjs_inline_code = script_matches[0]

ARTICULATIONS_HEADER_ABC = """X:0
T:E. J. 2 — Tabla de 10 Articulaciones Oficiales
C:Paul Taffanel & Philippe Gaubert (A. L. 16.588)
M:C
L:1/16
K:C
V:1 clef=treble stem=up
%%score 1
(DEF"^1"GAGFE) | (DEF"^2"G)(AGFE) | .D(EF"^3"G) .A(GFE) | (DEF)."^4"G (AGF).E | (DE).F."^5"G (AG).F.E | .D.E"^6"(FG) .A.G(FE) | .D(EF)."^7"G .A(GF).E | (DE)"^8"(FG)(AG)(FE) | .D(EF)"^9"(GA)(GF).E | .D.E.F."^10"G.A.G.F.E |]"""

EJ2_MEASURES = [
    (1,  "Re menor (i)",          ["DEFGAGFE", "DEFGAGFE", "DEFGAGFE", "DEFGAGFE"], "|:", "|", False),
    (2,  "vii° -> Mib menor",     ["D_E=F_G_AGFE", "DEFGAGFE", "DEFGAGFE", "DEFGAFED"], "", "|", False),
    (3,  "Mib menor (i)",         ["_EF_G_A_BAGF", "EFGABAGF", "EFGABAGF", "EFGABAGF"], "", "|", False),
    (4,  "vii° -> Mi menor",      ["^D=E^F=G=AGFE", "DEFGAGFE", "DEFGAGFE", "DEFGAFED"], "", "|", False),
    (5,  "Mi menor (i)",          ["E^FGABAGF", "EFGABAGF", "EFGABAGF", "EFGABAGF"], "", "|", False),
    (6,  "vii° -> Fa menor",      ["E=F=G_A_BAGF", "EFGABAGF", "EFGABAGF", "EFGABGFE"], "", "|", False),
    (7,  "Fa menor (i)",          ["FG_A_BcBAG", "FGABcBAG", "FGABcBAG", "FGABcBAG"], "", "|", False),
    (8,  "vii° -> Fa# menor",     ["^E^F^G=A=BAGF", "EFGABAGF", "EFGABAGF", "EFGABGFE"], "", "|", False),
    (9,  "Fa# menor (i)",         ["^F^GAB^cBAG", "FGABcBAG", "FGABcBAG", "FGABcBAG"], "", "|", False),
    (10, "vii° -> Sol menor",     ["^F=G=A_B=cBAG", "FGABcBAG", "FGABcBAG", "FGABcAGF"], "", "|", False),
    (11, "Sol menor (i)",         ["GA_BcdcBA", "GABcdcBA", "GABcdcBA", "GABcdcBA"], "", "|", False),
    (12, "vii° -> Sol# menor",    ["^^F^G^AB^cBAG", "FGABcBAG", "FGABcBAG", "FGABcAGF"], "", "|", False),
    (13, "Sol# menor (i)",        ["^G^AB^c^dcBA", "GABcdcBA", "GABcdcBA", "GABcdcBA"], "", "|", False),
    (14, "vii° -> La menor",      ["^G=A=B=c=dcBA", "GABcdcBA", "GABcdcBA", "GABcdBAG"], "", "|", False),
    (15, "La menor (i)",          ["ABcdedcB", "ABcdedcB", "ABcdedcB", "ABcdedcB"], "", "|", False),
    (16, "vii° -> Sib menor",     ["A_B=c_d_edcB", "ABcdedcB", "ABcdedcB", "ABcdecBA"], "", "|", False),
    (17, "Sib menor (i)",         ["_Bc_d_efedc", "Bcdefedc", "Bcdefedc", "Bcdefedc"], "", "|", False),
    (18, "vii° -> Si menor",      ["^A=B^c=d=edcB", "ABcdedcB", "ABcdedcB", "ABcdecBA"], "", "|", False),
    (19, "Si menor (i)",          ["B^cde^fedc", "Bcdefedc", "Bcdefedc", "Bcdefedc"], "", "|", False),
    (20, "vii° -> Do menor",      ["B=c=d_e=fedc", "Bcdefedc", "Bcdefedc", "BcdefdcB"], "", "|", False),
    (21, "Do menor (i)",          ["cd_efgfed", "cdefgfed", "cdefgfed", "cdefgfed"], "", "|", False),
    (22, "vii° -> Do# menor",     ["^B^c^d=e^fedc", "Bcdefedc", "Bcdefedc", "BcdefdcB"], "", "|", False),
    (23, "Do# menor (i)",         ["^c^de^f^gfed", "cdefgfed", "cdefgfed", "cdefgfed"], "", "|", False),
    (24, "vii° -> Re menor",      ["^c=d=e=f=gfed", "cdefgfed", "cdefgfed", "cdefgedc"], "", ":|", False),
    (25, "Re menor (i) [8va]",    ["defgagfe", "defgagfe", "defgagfe", "defgagfe"], "", "|", True),
    (26, "vii° -> Mib m [8va]",   ["d_e=f_g_agfe", "defgagfe", "defgagfe", "defgafed"], "", "|", True),
    (27, "Mib menor (i) [8va]",   ["_ef_g_a_bagf", "efgabagf", "efgabagf", "efgabagf"], "", "|", True),
    (28, "vii° -> Mi m [8va]",    ["^d=e^f=g=agfe", "defgagfe", "defgagfe", "defgafed"], "", "|", True),
    (29, "Mi menor (i) [8va]",    ["e^fgabagf", "efgabagf", "efgabagf", "efgabagf"], "", "|", True),
    (30, "vii° -> Fa + Fin [8va]",["e=f=g_a_bagf", "efgabagf", "efgabagf", "efgabgfe"], "", "| f4 z4 z8 |]", True),
]

ARTICULATION_META = [
    (0,  "Original_AL16588",                    "Original (Sin articulación fija — A. L. 16.588)"),
    (1,  "Articulacion_01_8_Ligadas",           "1. A 8 ligadas (Toda ligada)"),
    (2,  "Articulacion_02_4_y_4_Ligadas",       "2. A 4 y 4 ligadas"),
    (3,  "Articulacion_03_1_Picada_3_Ligadas",  "3. 1 picada y 3 ligadas"),
    (4,  "Articulacion_04_3_Ligadas_1_Picada",  "4. 3 ligadas y 1 picada"),
    (5,  "Articulacion_05_2_Ligadas_2_Picadas", "5. 2 ligadas y 2 picadas"),
    (6,  "Articulacion_06_2_Picadas_2_Ligadas", "6. 2 picadas y 2 ligadas"),
    (7,  "Articulacion_07_1_Picada_2_Ligadas_1_Picada", "7. 1 picada, 2 ligadas y 1 picada"),
    (8,  "Articulacion_08_De_2_en_2_Ligadas",   "8. De 2 en 2 ligadas"),
    (9,  "Articulacion_09_De_2_en_2_Sincopadas","9. De 2 en 2 sincopadas (a contratiempo)"),
    (10, "Articulacion_10_Todo_Picado",         "10. Todo picado (Staccato)"),
]

NOTE_REGEX = re.compile(r'[\^_=]*[A-Ga-g]')

def split_8_notes(beat_str):
    notes = NOTE_REGEX.findall(beat_str)
    assert len(notes) == 8, f"Expected 8 notes in {beat_str}, got {len(notes)}: {notes}"
    return notes

def apply_ej2_articulation(beat_str, art_id):
    n = split_8_notes(beat_str)
    if art_id == 0:
        return "".join(n)
    elif art_id == 1:
        return f"({n[0]}{n[1]}{n[2]}{n[3]}{n[4]}{n[5]}{n[6]}{n[7]})"
    elif art_id == 2:
        return f"({n[0]}{n[1]}{n[2]}{n[3]})({n[4]}{n[5]}{n[6]}{n[7]})"
    elif art_id == 3:
        return f".{n[0]}({n[1]}{n[2]}{n[3]}).{n[4]}({n[5]}{n[6]}{n[7]})"
    elif art_id == 4:
        return f"({n[0]}{n[1]}{n[2]}).{n[3]}({n[4]}{n[5]}{n[6]}).{n[7]}"
    elif art_id == 5:
        return f"({n[0]}{n[1]}).{n[2]}.{n[3]}({n[4]}{n[5]}).{n[6]}.{n[7]}"
    elif art_id == 6:
        return f".{n[0]}.{n[1]}({n[2]}{n[3]}).{n[4]}.{n[5]}({n[6]}{n[7]})"
    elif art_id == 7:
        return f".{n[0]}({n[1]}{n[2]}).{n[3]}.{n[4]}({n[5]}{n[6]}).{n[7]}"
    elif art_id == 8:
        return f"({n[0]}{n[1]})({n[2]}{n[3]})({n[4]}{n[5]})({n[6]}{n[7]})"
    elif art_id == 9:
        return f".{n[0]}({n[1]}{n[2]})({n[3]}{n[4]})({n[5]}{n[6]}).{n[7]}"
    elif art_id == 10:
        return f".{n[0]}.{n[1]}.{n[2]}.{n[3]}.{n[4]}.{n[5]}.{n[6]}.{n[7]}"
    else:
        return "".join(n)

def build_abc_for_articulation(art_id, title_desc, tune_index=1, tempo_bpm=80):
    lines = [
        f"X:{tune_index}",
        f"T:E. J. 2 — {title_desc}",
        "C:Paul Taffanel & Philippe Gaubert (A. L. 16.588)",
        f"% EJ2_LEDUC_ART:{art_id}",
        "%%barsperstaff 1",
        "M:4/2",
        "L:1/16",
        f"Q:1/4={tempo_bpm}",
        "K:C",
        "V:1 clef=treble stem=up",
        "%%score 1",
    ]
    current_stem = "up"
    for m_num, label, beats, prefix, suffix, is_8va in EJ2_MEASURES:
        target_stem = "up" if m_num <= 10 else "down"
        if target_stem != current_stem:
            lines.append(f"[V:1 stem={target_stem}]")
            current_stem = target_stem
        art_beats = [apply_ej2_articulation(b, art_id) for b in beats]
        beats_str = " ".join(art_beats)
        annot = '"^8va"' if m_num == 25 else ""
        if prefix:
            line = f"{prefix} {annot}{beats_str} {suffix} % Compás {m_num}: {label}"
        else:
            line = f"{annot}{beats_str} {suffix} % Compás {m_num}: {label}"
        lines.append(line)
    return "\n".join(lines) + "\n"

def generate_html():
    measures_json = json.dumps([
        {
            "num": m[0],
            "label": m[1],
            "beats": m[2],
            "prefix": m[3],
            "suffix": m[4],
            "is8va": m[5]
        }
        for m in EJ2_MEASURES
    ], ensure_ascii=False)

    abc_by_art = {}
    for art_id, slug, desc in ARTICULATION_META:
        abc_txt = build_abc_for_articulation(art_id, desc, tune_index=1)
        if art_id == 0:
            abc_by_art[art_id] = ARTICULATIONS_HEADER_ABC + "\n\n" + abc_txt
        else:
            abc_by_art[art_id] = abc_txt

    abc_by_art_json = json.dumps(abc_by_art, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Validación Urtext — Taffanel & Gaubert E. J. 2 (A. L. 16.588)</title>
<style>
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}
  body {{
    margin: 0;
    padding: 0;
    background: #1e2028;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #111;
  }}

  /* Sticky Interactive Validation Player Bar */
  .validation-Dock {{
    position: sticky;
    top: 0;
    z-index: 1000;
    background: rgba(20, 22, 30, 0.96);
    backdrop-filter: blur(12px);
    color: #f8fafc;
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
    padding: 12px 20px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.35);
  }}
  .dock-inner {{
    max-width: 1120px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .dock-top {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }}
  .dock-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .dock-badge {{
    background: #f59e0b;
    color: #111827;
    font-weight: 800;
    font-size: 12px;
    padding: 4px 9px;
    border-radius: 6px;
    letter-spacing: 0.4px;
  }}
  .dock-title {{
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
  }}
  .dock-subtitle {{
    font-size: 12px;
    color: #94a3b8;
  }}
  .dock-controls {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
  }}
  .btn-play {{
    background: #10b981;
    color: #052e16;
    border: none;
    border-radius: 999px;
    padding: 9px 20px;
    font-size: 14px;
    font-weight: 800;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.15s ease;
  }}
  .btn-play:hover {{
    background: #34d399;
    transform: translateY(-1px);
  }}
  .btn-play.playing {{
    background: #ef4444;
    color: #ffffff;
  }}
  .btn-secondary {{
    background: #334155;
    color: #f1f5f9;
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 7px 12px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
  }}
  .btn-secondary:hover {{
    background: #475569;
  }}
  .ctrl-group {{
    display: flex;
    align-items: center;
    gap: 6px;
    background: #0f172a;
    border: 1px solid #334155;
    padding: 5px 10px;
    border-radius: 8px;
    font-size: 12px;
    color: #cbd5e1;
  }}
  .ctrl-group select, .ctrl-group input {{
    background: #1e293b;
    color: #f8fafc;
    border: 1px solid #475569;
    border-radius: 5px;
    padding: 3px 6px;
    font-size: 12px;
    font-weight: 600;
  }}
  .art-bar {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    align-items: center;
  }}
  .art-chip {{
    background: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
    border-radius: 999px;
    padding: 5px 11px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.12s ease;
  }}
  .art-chip:hover {{
    background: #334155;
    color: #ffffff;
  }}
  .art-chip.active {{
    background: #3b82f6;
    color: #ffffff;
    border-color: #60a5fa;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.45);
  }}
  .status-pill {{
    font-size: 12px;
    font-weight: 600;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 4px 10px;
    border-radius: 999px;
  }}

  /* Collapsible ABC code panel */
  #abc-panel {{
    display: none;
    max-width: 1120px;
    margin: 12px auto 0;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 12px;
  }}
  #abc-panel pre {{
    margin: 0;
    max-height: 240px;
    overflow: auto;
    font-family: "SF Mono", Menlo, Consolas, monospace;
    font-size: 11.5px;
    color: #e2e8f0;
    line-height: 1.45;
    white-space: pre;
  }}

  /* Leduc Urtext Pages */
  .pages-wrapper {{
    padding: 20px 12px 48px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
  }}
  .leduc-page {{
    width: 210mm;
    min-height: 297mm;
    background: #fdfaf2;
    color: #000000;
    padding: 8mm 10mm 7mm 10mm;
    position: relative;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45);
    border-radius: 3px;
    font-family: "Times New Roman", Georgia, serif;
  }}
  .page-num-left {{
    position: absolute;
    top: 6mm;
    left: 10mm;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 0.5px;
  }}
  .page-num-right {{
    position: absolute;
    top: 6mm;
    right: 10mm;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 0.5px;
  }}
  .ej-header {{
    margin-top: 4mm;
    margin-left: 8mm;
    margin-bottom: 1.5mm;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding-right: 4mm;
  }}
  .ej-title {{
    font-size: 23px;
    font-weight: bold;
    letter-spacing: 1px;
  }}
  .ej-active-art-tag {{
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: #1d4ed8;
    background: #dbeafe;
    border: 1px solid #93c5fd;
    padding: 3px 10px;
    border-radius: 999px;
  }}
  .ej-instruction {{
    margin-left: 8mm;
    margin-bottom: 1.5mm;
    font-size: 13.8px;
    letter-spacing: 0.35px;
  }}
  .staff-row {{
    width: 100%;
    margin: 0;
    padding: 0 4px;
    line-height: 1;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.12s ease;
    position: relative;
  }}
  .staff-row:hover {{
    background: rgba(59, 130, 246, 0.06);
  }}
  .staff-row.playing-measure {{
    background: rgba(245, 158, 11, 0.18) !important;
    outline: 1.5px solid #f59e0b;
  }}
  .measure-badge {{
    position: absolute;
    left: -6px;
    top: 4px;
    font-family: -apple-system, sans-serif;
    font-size: 9.5px;
    font-weight: 700;
    color: #64748b;
    background: rgba(255,255,255,0.85);
    padding: 1px 4px;
    border-radius: 4px;
    pointer-events: none;
  }}
  .staff-row svg {{
    width: 100% !important;
    height: auto !important;
    display: block;
    overflow: visible;
  }}
  .art-staff-row {{
    margin-bottom: 2mm;
  }}
  .m1-container {{
    padding-left: 11mm;
  }}
  .octava-wrap {{
    position: relative;
  }}
  .octava-line {{
    position: absolute;
    top: 1px;
    left: 34px;
    right: 6px;
    display: flex;
    align-items: flex-start;
    pointer-events: none;
    z-index: 5;
  }}
  .octava-last .octava-line {{
    right: 132px;
  }}
  .octava-num {{
    font-family: "Times New Roman", serif;
    font-style: italic;
    font-weight: bold;
    font-size: 13.5px;
    line-height: 1;
    margin-right: 2px;
  }}
  .octava-dots {{
    flex: 1;
    border-top: 1.3px dashed #000;
    height: 1px;
    margin-top: 4px;
  }}
  .octava-hook {{
    width: 1.3px;
    height: 7px;
    background: #000;
    margin-top: 4px;
    display: inline-block;
  }}
  .plate-footer {{
    position: absolute;
    bottom: 5mm;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 10.5px;
    letter-spacing: 0.8px;
  }}

  svg path {{ fill: currentColor; }}
  svg path[stroke]:not([fill]),
  svg path[fill="none"] {{ fill: none !important; }}

  @page {{
    size: A4 portrait;
    margin: 0;
  }}
  @media print {{
    body {{ background: #fdfaf2; }}
    .validation-Dock {{ display: none !important; }}
    .pages-wrapper {{ padding: 0; gap: 0; }}
    .leduc-page {{
      width: 210mm;
      height: 297mm;
      min-height: 297mm;
      max-height: 297mm;
      overflow: hidden;
      box-shadow: none;
      page-break-after: always;
      break-after: page;
    }}
    .leduc-page:last-child {{
      page-break-after: auto;
      break-after: auto;
    }}
  }}
</style>
<script>
{abcjs_inline_code}
</script>
</head>
<body>

<div class="validation-Dock">
  <div class="dock-inner">
    <div class="dock-top">
      <div class="dock-brand">
        <span class="dock-badge">URTEXT A. L. 16.588</span>
        <div>
          <div class="dock-title">Taffanel &amp; Gaubert — E. J. 2 (Pentacordios Menores y 7ª Disminuida)</div>
          <div class="dock-subtitle">Haz clic en cualquier compás para reproducir desde ahí · Plicas ↑ (Comp. 1–10) · Plicas ↓ (Comp. 11–31)</div>
        </div>
      </div>

      <div class="dock-controls">
        <button id="play-btn" class="btn-play" onclick="togglePlayback()">
          <span id="play-icon">▶</span>
          <span id="play-label">Reproducir</span>
        </button>

        <div class="ctrl-group">
          <label for="start-measure">Desde:</label>
          <select id="start-measure" onchange="onStartMeasureChange()"></select>
        </div>

        <div class="ctrl-group">
          <label for="tempo-input">Tempo (♩):</label>
          <input id="tempo-input" type="number" min="40" max="160" value="84" style="width:58px" onchange="onTempoChange()">
          <span>BPM</span>
        </div>

        <div class="ctrl-group">
          <label for="inst-select">Timbre:</label>
          <select id="inst-select">
            <option value="flute">Flauta Traversa</option>
            <option value="piano" selected>Piano de Cola</option>
          </select>
        </div>

        <button class="btn-secondary" onclick="toggleAbcPanel()">📄 Ver / Copiar ABC</button>
        <span id="playback-status" class="status-pill">Listo · 31 compases</span>
      </div>
    </div>

    <div class="art-bar" id="art-buttons"></div>

    <div id="abc-panel">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span style="font-size:12px; font-weight:700; color:#93c5fd;">Código ABC de la articulación seleccionada:</span>
        <button class="btn-secondary" onclick="copyAbcCode()"><span id="copy-label">📋 Copiar ABC</span></button>
      </div>
      <pre id="abc-code-box"></pre>
    </div>
  </div>
</div>

<div class="pages-wrapper">
  <!-- PAGE 1 (Measures 1..14) -->
  <div class="leduc-page" id="page-1">
    <div class="page-num-left">06</div>
    <div class="ej-header">
      <div class="ej-title">E. J. 2</div>
      <div class="ej-active-art-tag" id="active-art-badge">Original A. L. 16.588</div>
    </div>
    <div class="ej-instruction">A travailler successivement avec chacune des dix articulations suivantes:</div>
    <div id="art-staff" class="staff-row art-staff-row" title="Tabla de 10 Articulaciones Oficiales"></div>
    <div id="page1-staves"></div>
    <div class="plate-footer">A. L. 16.588</div>
  </div>

  <!-- PAGE 2 (Measures 15..31) -->
  <div class="leduc-page" id="page-2">
    <div class="page-num-right">10</div>
    <div id="page2-staves" style="margin-top: 4mm;"></div>
    <div class="plate-footer">A. L. 16.588</div>
  </div>
</div>

<script>
const EJ2_ART_HEADER_ABC = [
  "X:0",
  "M:C",
  "L:1/16",
  "K:C",
  "V:1 clef=treble stem=up",
  "%%score 1",
  "(DEF\\"^1\\"GAGFE) | (DEF\\"^2\\"G)(AGFE) | .D(EF\\"^3\\"G) .A(GFE) | (DEF).\\"^4\\"G (AGF).E | (DE).F.\\"^5\\"G (AG).F.E | .D.E\\"^6\\"(FG) .A.G(FE) | .D(EF).\\"^7\\"G .A(GF).E | (DE)\\"^8\\"(FG)(AG)(FE) | .D(EF)\\"^9\\"(GA)(GF).E | .D.E.F.\\"^10\\"G.A.G.F.E |]"
].join("\\n");

const EJ2_MEASURES = {measures_json};
const ABC_BY_ART = {abc_by_art_json};

const ART_INFO = [
  {{ id: 0,  short: "0. Original",      full: "Original A. L. 16.588" }},
  {{ id: 1,  short: "1. (8) ligadas",   full: "Art. 1 · A 8 ligadas" }},
  {{ id: 2,  short: "2. (4)+(4)",       full: "Art. 2 · A 4 y 4 ligadas" }},
  {{ id: 3,  short: "3. ·(3) ·(3)",     full: "Art. 3 · 1 picada y 3 ligadas" }},
  {{ id: 4,  short: "4. (3)· (3)·",     full: "Art. 4 · 3 ligadas y 1 picada" }},
  {{ id: 5,  short: "5. (2)·· (2)··",   full: "Art. 5 · 2 ligadas y 2 picadas" }},
  {{ id: 6,  short: "6. ··(2) ··(2)",   full: "Art. 6 · 2 picadas y 2 ligadas" }},
  {{ id: 7,  short: "7. ·(2)· ·(2)·",   full: "Art. 7 · 1 pic., 2 lig., 1 pic." }},
  {{ id: 8,  short: "8. (2)(2)(2)(2)",  full: "Art. 8 · De 2 en 2 ligadas" }},
  {{ id: 9,  short: "9. ·(2)(2)(2)·",   full: "Art. 9 · De 2 en 2 sincopadas" }},
  {{ id: 10, short: "10. Todo picado",  full: "Art. 10 · Todo picado (Staccato)" }}
];

let currentArtId = 0;
let isPlaying = false;
let audioCtx = null;
let scheduledTimers = [];
let activeOscillators = [];

function split8Notes(beatStr) {{
  return beatStr.match(/[\\^_=]*[A-Ga-g]/g) || [];
}}

function applyArt(beatStr, artId) {{
  const n = split8Notes(beatStr);
  if (n.length !== 8 || artId === 0) return beatStr;
  switch (artId) {{
    case 1: return `(${{n[0]}}${{n[1]}}${{n[2]}}${{n[3]}}${{n[4]}}${{n[5]}}${{n[6]}}${{n[7]}})`;
    case 2: return `(${{n[0]}}${{n[1]}}${{n[2]}}${{n[3]}})(${{n[4]}}${{n[5]}}${{n[6]}}${{n[7]}})`;
    case 3: return `.${{n[0]}}(${{n[1]}}${{n[2]}}${{n[3]}}).${{n[4]}}(${{n[5]}}${{n[6]}}${{n[7]}})`;
    case 4: return `(${{n[0]}}${{n[1]}}${{n[2]}}).${{n[3]}}(${{n[4]}}${{n[5]}}${{n[6]}}).${{n[7]}}`;
    case 5: return `(${{n[0]}}${{n[1]}}).${{n[2]}}.${{n[3]}}(${{n[4]}}${{n[5]}}).${{n[6]}}.${{n[7]}}`;
    case 6: return `.${{n[0]}}.${{n[1]}}(${{n[2]}}${{n[3]}}).${{n[4]}}.${{n[5]}}(${{n[6]}}${{n[7]}})`;
    case 7: return `.${{n[0]}}(${{n[1]}}${{n[2]}}).${{n[3]}}.${{n[4]}}(${{n[5]}}${{n[6]}}).${{n[7]}}`;
    case 8: return `(${{n[0]}}${{n[1]}})(${{n[2]}}${{n[3]}})(${{n[4]}}${{n[5]}})(${{n[6]}}${{n[7]}})`;
    case 9: return `.${{n[0]}}(${{n[1]}}${{n[2]}})(${{n[3]}}${{n[4]}})(${{n[5]}}${{n[6]}}).${{n[7]}}`;
    case 10: return `.${{n[0]}}.${{n[1]}}.${{n[2]}}.${{n[3]}}.${{n[4]}}.${{n[5]}}.${{n[6]}}.${{n[7]}}`;
    default: return beatStr;
  }}
}}

function initControls() {{
  const artBar = document.getElementById("art-buttons");
  artBar.innerHTML = ART_INFO.map(a =>
    `<button class="art-chip ${{a.id === currentArtId ? 'active' : ''}}" id="art-btn-${{a.id}}" onclick="selectArticulation(${{a.id}})">${{a.short}}</button>`
  ).join("");

  const sel = document.getElementById("start-measure");
  sel.innerHTML = EJ2_MEASURES.map(m =>
    `<option value="${{m.num}}">Compás ${{m.num}} (${{m.label}})</option>`
  ).join("");

  const p1 = document.getElementById("page1-staves");
  const p2 = document.getElementById("page2-staves");
  p1.innerHTML = "";
  p2.innerHTML = "";

  EJ2_MEASURES.forEach(m => {{
    const isP1 = m.num <= 14;
    const parent = isP1 ? p1 : p2;
    const row = document.createElement("div");
    let cls = "staff-row";
    if (m.num === 1) cls += " m1-container";
    if (m.is8va) cls += " octava-wrap " + (m.num === 30 ? "octava-last" : "octava-full");
    row.className = cls;
    row.id = `row-m${{m.num}}`;
    row.title = `Compás ${{m.num}}: ${{m.label}} (Clic para reproducir desde aquí)`;
    row.onclick = () => {{
      document.getElementById("start-measure").value = String(m.num);
      startPlaybackFrom(m.num);
    }};

    let inner = `<span class="measure-badge">${{m.num}}</span>`;
    if (m.is8va) {{
      const hook = (m.num === 30) ? '<span class="octava-hook"></span>' : '';
      inner += `<div class="octava-line"><span class="octava-num">8</span><span class="octava-dots"></span>${{hook}}</div>`;
    }}
    inner += `<div id="staff-m${{m.num}}"></div>`;
    row.innerHTML = inner;
    parent.appendChild(row);
  }});
}}

function renderAllStaves() {{
  const info = ART_INFO.find(a => a.id === currentArtId) || ART_INFO[0];
  document.getElementById("active-art-badge").textContent = info.full;
  document.getElementById("abc-code-box").textContent = ABC_BY_ART[currentArtId] || "";

  ABCJS.renderAbc("art-staff", EJ2_ART_HEADER_ABC, {{
    staffwidth: 1030,
    paddingtop: 2,
    paddingbottom: 2,
    paddingleft: 0,
    paddingright: 0,
    responsive: "resize"
  }});

  EJ2_MEASURES.forEach(m => {{
    const stemDir = (m.num <= 10) ? "up" : "down";
    const meterStr = (m.num === 1) ? "M:4/2" : "M:none";
    const staffW = (m.num === 1) ? 965 : 1030;
    const articulated = m.beats.map(b => applyArt(b, currentArtId)).join(" ");
    const body = m.prefix ? `${{m.prefix}} ${{articulated}} ${{m.suffix}}` : `${{articulated}} ${{m.suffix}}`;
    const abc = [
      `X:${{m.num}}`,
      meterStr,
      "L:1/16",
      "K:C",
      `V:1 clef=treble stem=${{stemDir}}`,
      "%%score 1",
      body
    ].join("\\n");

    ABCJS.renderAbc(`staff-m${{m.num}}`, abc, {{
      staffwidth: staffW,
      paddingtop: 1,
      paddingbottom: 1,
      paddingleft: 0,
      paddingright: 0,
      responsive: "resize"
    }});
  }});
}}

function selectArticulation(artId) {{
  currentArtId = artId;
  document.querySelectorAll(".art-chip").forEach(btn => btn.classList.remove("active"));
  const activeBtn = document.getElementById(`art-btn-${{artId}}`);
  if (activeBtn) activeBtn.classList.add("active");
  renderAllStaves();
  if (isPlaying) {{
    const startM = parseInt(document.getElementById("start-measure").value, 10) || 1;
    startPlaybackFrom(startM);
  }}
}}

function toggleAbcPanel() {{
  const panel = document.getElementById("abc-panel");
  panel.style.display = (panel.style.display === "block") ? "none" : "block";
}}

function copyAbcCode() {{
  const code = ABC_BY_ART[currentArtId] || "";
  navigator.clipboard.writeText(code);
  const lbl = document.getElementById("copy-label");
  lbl.textContent = "✅ ¡Copiado!";
  setTimeout(() => {{ lbl.textContent = "📋 Copiar ABC"; }}, 1800);
}}

// --- Web Audio API Synthesizer for E.J. 2 ---
function midiToFreq(midi) {{
  return 440 * Math.pow(2, (midi - 69) / 12);
}}

function isStaccatoNote(idx8, artId) {{
  const i = idx8 % 8;
  switch (artId) {{
    case 0:
    case 1:
    case 2:
    case 8: return false;
    case 3: return (i === 0 || i === 4);
    case 4: return (i === 3 || i === 7);
    case 5: return (i === 2 || i === 3 || i === 6 || i === 7);
    case 6: return (i === 0 || i === 1 || i === 4 || i === 5);
    case 7: return (i === 0 || i === 3 || i === 4 || i === 7);
    case 9: return (i === 0 || i === 7);
    case 10: return true;
    default: return false;
  }}
}}

function buildMeasureMidiNotes(measureNum) {{
  // 15 chromatic pairs (Measures 1..30): pairIndex k = 0..14
  const k = Math.floor((measureNum - 1) / 2);
  const isOdd = (measureNum % 2 === 1);
  // Base MIDI: D4 = 62 + k. (In M.25..30, written D5..E5 + 8va)
  const base = 62 + k;
  if (isOdd) {{
    // Minor pentachord i: 0, 2, 3, 5, 7
    const p = [base, base + 2, base + 3, base + 5, base + 7];
    const grp = [p[0], p[1], p[2], p[3], p[4], p[3], p[2], p[1]];
    return [...grp, ...grp, ...grp, ...grp];
  }} else {{
    // Diminished 7th vii° -> (base + 1) minor: 0, 1, 3, 4, 6
    const p = [base, base + 1, base + 3, base + 4, base + 6];
    const grp = [p[0], p[1], p[2], p[3], p[4], p[3], p[2], p[1]];
    const turn = [p[0], p[1], p[2], p[3], p[4], p[2], p[1], p[0]];
    return [...grp, ...grp, ...grp, ...turn];
  }}
}}

function playSynthNote(freq, startTime, duration, staccato, inst) {{
  if (!audioCtx) return;
  const gate = staccato ? 0.42 : 0.94;
  const soundDur = Math.max(0.02, duration * gate);

  const masterGain = audioCtx.createGain();
  masterGain.connect(audioCtx.destination);

  const attack = 0.006;
  const release = Math.min(0.025, soundDur * 0.3);
  masterGain.gain.setValueAtTime(0.0001, startTime);
  masterGain.gain.linearRampToValueAtTime(0.22, startTime + attack);
  masterGain.gain.exponentialRampToValueAtTime(0.12, startTime + Math.max(attack + 0.01, soundDur - release));
  masterGain.gain.linearRampToValueAtTime(0.0001, startTime + soundDur);

  const harmonics = (inst === "flute")
    ? [[1, 1.0], [2, 0.28], [3, 0.09]]
    : [[1, 1.0], [2, 0.50], [3, 0.25], [4, 0.12]];

  harmonics.forEach(([mult, amp]) => {{
    const osc = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(freq * mult, startTime);
    g.gain.setValueAtTime(amp, startTime);
    osc.connect(g);
    g.connect(masterGain);
    osc.start(startTime);
    osc.stop(startTime + soundDur + 0.01);
    activeOscillators.push(osc);
  }});
}}

function stopPlayback() {{
  isPlaying = false;
  scheduledTimers.forEach(t => clearTimeout(t));
  scheduledTimers = [];
  activeOscillators.forEach(o => {{
    try {{ o.stop(); }} catch (e) {{}}
  }});
  activeOscillators = [];
  document.querySelectorAll(".staff-row").forEach(r => r.classList.remove("playing-measure"));
  const btn = document.getElementById("play-btn");
  btn.classList.remove("playing");
  document.getElementById("play-icon").textContent = "▶";
  document.getElementById("play-label").textContent = "Reproducir";
  document.getElementById("playback-status").textContent = "Detenido · Listo";
}}

function togglePlayback() {{
  if (isPlaying) {{
    stopPlayback();
  }} else {{
    const startM = parseInt(document.getElementById("start-measure").value, 10) || 1;
    startPlaybackFrom(startM);
  }}
}}

function startPlaybackFrom(startMeasureNum) {{
  stopPlayback();
  if (!audioCtx) {{
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }}
  if (audioCtx.state === "suspended") {{
    audioCtx.resume();
  }}

  isPlaying = true;
  const btn = document.getElementById("play-btn");
  btn.classList.add("playing");
  document.getElementById("play-icon").textContent = "⏹";
  document.getElementById("play-label").textContent = "Detener";

  const bpm = Math.max(40, Math.min(160, parseInt(document.getElementById("tempo-input").value, 10) || 84));
  const inst = document.getElementById("inst-select").value || "piano";
  const sixteenthDur = (60.0 / bpm) / 4.0;
  let cursorTime = audioCtx.currentTime + 0.08;
  const baseWallMs = performance.now() + 80;

  for (let mNum = startMeasureNum; mNum <= 30; mNum++) {{
    const mObj = EJ2_MEASURES[mNum - 1];
    const midiList = buildMeasureMidiNotes(mNum);
    const measureStartOffsetMs = (cursorTime - audioCtx.currentTime) * 1000;

    const timerId = setTimeout(() => {{
      if (!isPlaying) return;
      document.querySelectorAll(".staff-row").forEach(r => r.classList.remove("playing-measure"));
      const rowEl = document.getElementById(`row-m${{mNum}}`);
      if (rowEl) {{
        rowEl.classList.add("playing-measure");
        rowEl.scrollIntoView({{ behavior: "smooth", block: "center" }});
      }}
      document.getElementById("start-measure").value = String(mNum);
      document.getElementById("playback-status").textContent = `🔊 Compás ${{mNum}} / 31 · ${{mObj.label}}`;
    }}, Math.max(0, measureStartOffsetMs));
    scheduledTimers.push(timerId);

    midiList.forEach((midi, idx) => {{
      const stacc = isStaccatoNote(idx, currentArtId);
      playSynthNote(midiToFreq(midi), cursorTime, sixteenthDur, stacc, inst);
      cursorTime += sixteenthDur;
    }});
  }}

  // Measure 31 final F5 (MIDI 77)
  const finalOffsetMs = (cursorTime - audioCtx.currentTime) * 1000;
  scheduledTimers.push(setTimeout(() => {{
    if (!isPlaying) return;
    document.getElementById("playback-status").textContent = "🔊 Compás 31 / 31 · Fa final (Cierre)";
  }}, Math.max(0, finalOffsetMs)));
  playSynthNote(midiToFreq(77), cursorTime, sixteenthDur * 4.0, false, inst);
  cursorTime += sixteenthDur * 4.0;

  const endOffsetMs = (cursorTime - audioCtx.currentTime) * 1000 + 150;
  scheduledTimers.push(setTimeout(() => {{
    if (isPlaying) stopPlayback();
  }}, Math.max(0, endOffsetMs)));
}}

function onStartMeasureChange() {{
  if (isPlaying) {{
    const startM = parseInt(document.getElementById("start-measure").value, 10) || 1;
    startPlaybackFrom(startM);
  }}
}}

function onTempoChange() {{
  if (isPlaying) {{
    const startM = parseInt(document.getElementById("start-measure").value, 10) || 1;
    startPlaybackFrom(startM);
  }}
}}

window.addEventListener("DOMContentLoaded", () => {{
  initControls();
  renderAllStaves();
}});
</script>
</body>
</html>
"""
    html_out_1 = os.path.join(ARTIFACT_DIR, "taffanel_ej2_validacion.html")
    html_out_2 = "/Users/sebas/Desktop/partituras/taffanel_ej2_validacion.html"
    with open(html_out_1, "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy(html_out_1, html_out_2)
    print("Wrote HTML to:", html_out_1)

if __name__ == "__main__":
    # First generate ABC
    collection_blocks = [ARTICULATIONS_HEADER_ABC + "\n"]
    for art_id, slug, desc in ARTICULATION_META:
        abc_content = build_abc_for_articulation(art_id, desc, tune_index=art_id + 1)
        collection_blocks.append(abc_content)
    master_abc = "\n".join(collection_blocks)
    abc_out_1 = os.path.join(ARTIFACT_DIR, "taffanel_ej2_completo.abc")
    abc_out_2 = "/Users/sebas/Desktop/partituras/taffanel_ej2_completo.abc"
    with open(abc_out_1, "w", encoding="utf-8") as f:
        f.write(master_abc)
    shutil.copy(abc_out_1, abc_out_2)
    generate_html()
