#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates all ABC files, interactive Web players, validation HTMLs, print HTMLs,
and shared score_template.html updates for M. A. Reichert Op. 5:
  - R1 (Nº 1, pp. 2–3)
  - R2 (Nº 2, pp. 4–5)
  - R4 (Nº 4, pp. 8–9)
  - R5 (Nº 5, pp. 10–13)
"""

import json
import os
import shutil

from generate_reichert_all import (
    KEYS_24,
    R2_8VA_SECTIONS,
    R4_8VA_SECTIONS,
    R4_OCT5_WRITTEN,
    generate_r1_section_measures,
    generate_r2_section_measures,
    generate_r4_section_measures,
    generate_r5_section_measures,
    build_r1_section_abc,
    build_r2_section_abc,
    build_r4_section_abc,
    build_r5_section_abc,
)

WORKSPACE = "/Users/sebas/Desktop/partituras"
ARTIFACT_DIR = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"
SCRATCH_DIR = os.path.join(ARTIFACT_DIR, "scratch")
ABC_DL_DIR = os.path.join(WORKSPACE, "docs", "downloads", "abc")
PDF_DL_DIR = os.path.join(WORKSPACE, "docs", "downloads", "pdf")

os.makedirs(SCRATCH_DIR, exist_ok=True)
os.makedirs(ABC_DL_DIR, exist_ok=True)
os.makedirs(PDF_DL_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Articulation Metadata
# ---------------------------------------------------------------------------
ARTS_12 = [
    {"id": 0,  "meter": "6/8", "name": "Edición Original (Schott 20623)", "short": "0. Orig.",           "formula": "Legato fraseado completo (Urtext Schott)", "slug": "00_Original_Op5"},
    {"id": 1,  "meter": "6/8", "name": "1. 12 Ligadas (Compás completo)", "short": "1. (12)",            "formula": "(12) · Compás entero ligado",              "slug": "01_Articulacion_01_12_Ligadas"},
    {"id": 2,  "meter": "6/8", "name": "2. 6 y 6 Ligadas",                "short": "2. (6)(6)",          "formula": "(6) + (6) · Seisillos ligados",            "slug": "02_Articulacion_02_6_y_6_Ligadas"},
    {"id": 3,  "meter": "6/8", "name": "3. 4 Ligadas y 2 Picadas",        "short": "3. (4)··",           "formula": "(4)·· (4)··",                              "slug": "03_Articulacion_03_4_Ligadas_2_Picadas"},
    {"id": 4,  "meter": "6/8", "name": "4. 2 Picadas y 4 Ligadas",        "short": "4. ··(4)",           "formula": "··(4) ··(4)",                              "slug": "04_Articulacion_04_2_Picadas_4_Ligadas"},
    {"id": 5,  "meter": "6/8", "name": "5. 2 Ligadas y 4 Picadas",        "short": "5. (2)····",         "formula": "(2)···· (2)····",                          "slug": "05_Articulacion_05_2_Ligadas_4_Picadas"},
    {"id": 6,  "meter": "2/4", "name": "6. De 3 en 3 Ligadas",            "short": "6. (3)(3)(3)(3)",    "formula": "(3)(3)(3)(3) · 4 grupos de 3",             "slug": "06_Articulacion_06_De_3_en_3_Ligadas"},
    {"id": 7,  "meter": "2/4", "name": "7. 3 Ligadas y 3 Picadas",        "short": "7. (3)···(3)···",    "formula": "(3)··· (3)···",                            "slug": "07_Articulacion_07_3_Ligadas_3_Picadas"},
    {"id": 8,  "meter": "6/8", "name": "8. De 2 en 2 Ligadas",            "short": "8. (2)(2)(2)",       "formula": "(2)(2)(2) (2)(2)(2)",                      "slug": "08_Articulacion_08_De_2_en_2_Ligadas"},
    {"id": 9,  "meter": "6/8", "name": "9. Sincopadas de a 2",            "short": "9. ·(2)(2)·",        "formula": "·(2)(2)· ·(2)(2)· desplazadas",            "slug": "09_Articulacion_09_Sincopadas"},
    {"id": 10, "meter": "6/8", "name": "10. Todas Picadas (Staccato)",    "short": "10. ·×12",           "formula": "12 notas en staccato por compás",          "slug": "10_Articulacion_10_Todas_Picadas"},
]

ARTS_8 = [
    {"id": 0, "meter": "2/4", "name": "Edición Original (Schott 20623)",  "short": "0. Orig.",           "formula": "Legato fraseado completo (Urtext Schott)", "slug": "00_Original_Op5"},
    {"id": 1, "meter": "2/4", "name": "1. 8 Ligadas",                     "short": "1. (8)",             "formula": "(8) · 8 semicorcheas ligadas",             "slug": "01_Articulacion_01_8_Ligadas"},
    {"id": 2, "meter": "2/4", "name": "2. De 4 en 4 Ligadas",             "short": "2. (4)(4)",          "formula": "(4)(4) · 4 y 4 ligadas",                   "slug": "02_Articulacion_02_4_y_4_Ligadas"},
    {"id": 3, "meter": "2/4", "name": "3. 1 Picada y 3 Ligadas",          "short": "3. ·(3) ·(3)",       "formula": "·(3) ·(3)",                                "slug": "03_Articulacion_03_1_Picada_3_Ligadas"},
    {"id": 4, "meter": "2/4", "name": "4. 2 Ligadas y 2 Picadas",         "short": "4. (2)·· (2)··",     "formula": "(2)·· (2)··",                              "slug": "04_Articulacion_04_2_Ligadas_2_Picadas"},
    {"id": 5, "meter": "2/4", "name": "5. 2 Picadas y 2 Ligadas",         "short": "5. ··(2) ··(2)",     "formula": "··(2) ··(2)",                              "slug": "05_Articulacion_05_2_Picadas_2_Ligadas"},
    {"id": 6, "meter": "2/4", "name": "6. 1 Picada, 2 Ligadas, 1 Picada", "short": "6. ·(2)· ·(2)·",     "formula": "·(2)· ·(2)·",                              "slug": "06_Articulacion_06_1_Picada_2_Ligadas_1_Picada"},
    {"id": 7, "meter": "2/4", "name": "7. De 2 en 2 Ligadas",             "short": "7. (2)(2)(2)(2)",    "formula": "(2)(2) (2)(2)",                            "slug": "07_Articulacion_07_De_2_en_2_Ligadas"},
    {"id": 8, "meter": "2/4", "name": "8. Sincopadas (De 2 en 2)",        "short": "8. ·(2)(2)(2)·",     "formula": "·(2)(2)(2)· desplazadas",                  "slug": "08_Articulacion_08_Sincopadas"},
]

SECTIONS_META = [
    {
        "id": k[0],
        "short": k[1],
        "titleEs": k[2],
        "titleEn": k[3],
        "keySig": k[4],
        "isMinor": k[7],
    }
    for k in KEYS_24
]


# ---------------------------------------------------------------------------
# Build JSON datasets for R1, R2, R4, R5
# ---------------------------------------------------------------------------
def build_r1_data():
    sections = []
    for sec_id in range(25):
        kt = KEYS_24[sec_id]
        bars, midis = generate_r1_section_measures(sec_id)
        sections.append({
            "id": sec_id,
            "short": kt[1],
            "titleEs": kt[2],
            "titleEn": kt[3],
            "keySig": kt[4],
            "isMinor": kt[7],
            "startMeasure": sec_id * 4 + 1,
            "endMeasure": sec_id * 4 + 4,
            "bars": bars,
            "midis": midis,
        })
    return sections


def build_r2_data():
    sections = []
    for sec_id in range(25):
        kt = KEYS_24[sec_id]
        bars, midis = generate_r2_section_measures(sec_id)
        sections.append({
            "id": sec_id,
            "short": kt[1],
            "titleEs": kt[2],
            "titleEn": kt[3],
            "keySig": kt[4],
            "isMinor": kt[7],
            "is8va": sec_id in R2_8VA_SECTIONS,
            "startMeasure": sec_id * 8 + 1,
            "endMeasure": sec_id * 8 + 8,
            "bars": bars,  # bars[0]=pickup(4), bars[1..7]=M1..M7(8), bars[8]=M8(1)
            "midis": midis,
        })
    return sections


def build_r4_data():
    sections = []
    for sec_id in range(25):
        kt = KEYS_24[sec_id]
        bars, midis = generate_r4_section_measures(sec_id)
        sections.append({
            "id": sec_id,
            "short": kt[1],
            "titleEs": kt[2],
            "titleEn": kt[3],
            "keySig": kt[4],
            "isMinor": kt[7],
            "is8va": sec_id in R4_8VA_SECTIONS,
            "startMeasure": sec_id * 4 + 1,
            "endMeasure": sec_id * 4 + 4,
            "bars": bars,  # bars[0..2]=16 notes each, bars[3]=12 sixteenths + 1 eighth
            "midis": midis,
        })
    return sections


def build_r5_data():
    sections = []
    for sec_id in range(25):
        kt = KEYS_24[sec_id]
        bars, midis = generate_r5_section_measures(sec_id)
        sections.append({
            "id": sec_id,
            "short": kt[1],
            "titleEs": kt[2],
            "titleEn": kt[3],
            "keySig": kt[4],
            "isMinor": kt[7],
            "startMeasure": sec_id * 8 + 1,
            "endMeasure": sec_id * 8 + 8,
            "bars": bars,  # bars[0..6]=12 triplet notes each, bars[7]=6 triplet notes + 1 eighth
            "midis": midis,
        })
    return sections


# ---------------------------------------------------------------------------
# Generate Complete & Per-Articulation ABC Files
# ---------------------------------------------------------------------------
def write_abc_collections():
    specs = [
        ("R1", "Nº 1 — Gammes et Arpèges en 6/8 (pp. 2–3)", "6/8", "1/4.=92", ARTS_12, build_r1_section_abc, "reichert_r1_completo.abc"),
        ("R2", "Nº 2 — Arpèges de Septième de Dominante et Tonique en 2/4 (pp. 4–5)", "2/4", "1/4=136", ARTS_8, build_r2_section_abc, "reichert_r2_completo.abc"),
        ("R4", "Nº 4 — Exercice d'Agilité en 4/4 (pp. 8–9)", "C", "1/4=128", ARTS_8, build_r4_section_abc, "reichert_r4_completo.abc"),
        ("R5", "Nº 5 — Arpèges en Tresillos 2/4 (pp. 10–13)", "2/4", "1/8=160", ARTS_12, build_r5_section_abc, "reichert_r5_completo.abc"),
    ]

    for code, title_desc, default_meter, default_q, arts_list, sec_builder, root_abc_name in specs:
        all_tunes = []
        for art in arts_list:
            art_id = art["id"]
            meter = art["meter"] if code in ("R1",) else default_meter
            header = [
                f"X:{art_id + 1}",
                f"T:Reichert Op. 5, {title_desc} — {art['name']}",
                "C:Mathieu-André Reichert (1830–1880) · Ed. B. Schott's Söhne, Plate 20623",
                f"M:{meter}",
                "L:1/16",
                f"Q:{default_q}",
                "K:C",
                "V:1 clef=treble",
            ]
            body = []
            for sec_id in range(25):
                kt = KEYS_24[sec_id]
                body.append(f"% --- {kt[2]} ---")
                body.append(sec_builder(sec_id, art_id))
            abc_text = "\n".join(header + body) + "\n"
            fname = f"{art['slug'].replace('_Articulacion', f'_Reichert_{code}_Articulacion').replace('_Original_Op5', f'_Reichert_{code}_Original_Op5')}.abc"
            with open(os.path.join(ABC_DL_DIR, fname), "w", encoding="utf-8") as f:
                f.write(abc_text)
            all_tunes.append(abc_text)

        collection_text = "\n\n".join(all_tunes)
        with open(os.path.join(ABC_DL_DIR, f"Reichert_{code}_Coleccion_Completa.abc"), "w", encoding="utf-8") as f:
            f.write(collection_text)
        with open(os.path.join(ABC_DL_DIR, root_abc_name), "w", encoding="utf-8") as f:
            f.write(collection_text)

        # Write root_abc_name (original Urtext + all articulations) to workspace & artifacts
        for dst in [os.path.join(WORKSPACE, root_abc_name), os.path.join(ARTIFACT_DIR, root_abc_name)]:
            with open(dst, "w", encoding="utf-8") as f:
                f.write(collection_text)


# ---------------------------------------------------------------------------
# Interactive Web Player & Print HTML Generator
# ---------------------------------------------------------------------------
def generate_web_player_html(code, sections_data):
    if code == "R1":
        page_title = "M. A. Reichert — Op. 5, Nº 1 (7 Exercices Journaliers · Urtext Schott 20623, págs. 2–3)"
        brand_main = "M. A. Reichert — 7 Exercices Journaliers, Op. 5 · Nº 1 (R. 1)"
        brand_sub = "Edición Urtext B. Schott's Söhne (Mainz, Plate 20623, págs. 2–3) · 24 Tonalidades Mayores y Menores en 6/8 + D.S. al Fine"
        pdf_file = "reichert_r1_transcripcion.pdf"
        tempo_min, tempo_max, tempo_def = 60, 120, 92
        tempo_unit = "♩."
        arts = [
            {**a, "fname": f"{a['slug'].replace('_Articulacion', '_Reichert_R1_Articulacion').replace('_Original_Op5', '_Reichert_R1_Original_Op5')}.abc"}
            for a in ARTS_12
        ]
        pages_meta = [
            {"num": 2, "title": "7 EXERCICES JOURNALIERS POUR LA FLÛTE · Op. 5 — Nº 1", "subtitle": "De 80 à 100 = ♩. · Tonalidades 1–12 (Do Mayor a Si♭ menor · Compases 1–48)", "secStart": 0, "secEnd": 11},
            {"num": 3, "title": "REICHERT Op. 5 — Nº 1 (Continuación)", "subtitle": "Tonalidades 13–24 (Sol♭ Mayor a Mi menor + D.S. al Fine · Compases 49–100)", "secStart": 12, "secEnd": 24},
        ]
    elif code == "R2":
        page_title = "M. A. Reichert — Op. 5, Nº 2 (7 Exercices Journaliers · Urtext Schott 20623, págs. 4–5)"
        brand_main = "M. A. Reichert — 7 Exercices Journaliers, Op. 5 · Nº 2 (R. 2)"
        brand_sub = "Edición Urtext B. Schott's Söhne (Mainz, Plate 20623, págs. 4–5) · Arpegios Modulantes en 24 Tonalidades (2/4) + D.S. al Fine"
        pdf_file = "reichert_r2_transcripcion.pdf"
        tempo_min, tempo_max, tempo_def = 80, 168, 132
        tempo_unit = "♩"
        arts = [
            {**a, "fname": f"{a['slug'].replace('_Articulacion', '_Reichert_R2_Articulacion').replace('_Original_Op5', '_Reichert_R2_Original_Op5')}.abc"}
            for a in ARTS_8
        ]
        pages_meta = [
            {"num": 4, "title": "7 EXERCICES JOURNALIERS POUR LA FLÛTE · Op. 5 — Nº 2", "subtitle": "de 120 à 152 = ♩ · Tonalidades 1–12 (Do Mayor a Si♭ menor · Compases 1–96)", "secStart": 0, "secEnd": 11},
            {"num": 5, "title": "REICHERT Op. 5 — Nº 2 (Continuación)", "subtitle": "Tonalidades 13–24 (Sol♭ Mayor a Mi menor + D.S. al Fine · Compases 97–200)", "secStart": 12, "secEnd": 24},
        ]
    elif code == "R4":
        page_title = "M. A. Reichert — Op. 5, Nº 4 (7 Exercices Journaliers · Urtext Schott 20623, págs. 8–9)"
        brand_main = "M. A. Reichert — 7 Exercices Journaliers, Op. 5 · Nº 4 (R. 4)"
        brand_sub = "Edición Urtext B. Schott's Söhne (Mainz, Plate 20623, págs. 8–9) · Bordaduras Cromáticas y Arpegios en 24 Tonalidades (4/4) + D.S. al Fine"
        pdf_file = "reichert_r4_transcripcion.pdf"
        tempo_min, tempo_max, tempo_def = 80, 160, 124
        tempo_unit = "♩"
        arts = [
            {**a, "fname": f"{a['slug'].replace('_Articulacion', '_Reichert_R4_Articulacion').replace('_Original_Op5', '_Reichert_R4_Original_Op5')}.abc"}
            for a in ARTS_8
        ]
        pages_meta = [
            {"num": 8, "title": "7 EXERCICES JOURNALIERS POUR LA FLÛTE · Op. 5 — Nº 4", "subtitle": "de 116 à 144 = ♩ · Tonalidades 1–12 (Do Mayor a Si♭ menor · Compases 1–48)", "secStart": 0, "secEnd": 11},
            {"num": 9, "title": "REICHERT Op. 5 — Nº 4 (Continuación)", "subtitle": "Tonalidades 13–24 (Sol♭ Mayor a Mi menor + D.S. al Fine · Compases 49–100)", "secStart": 12, "secEnd": 24},
        ]
    else:  # R5
        page_title = "M. A. Reichert — Op. 5, Nº 5 (7 Exercices Journaliers · Urtext Schott 20623, págs. 10–13)"
        brand_main = "M. A. Reichert — 7 Exercices Journaliers, Op. 5 · Nº 5 (R. 5)"
        brand_sub = "Edición Urtext B. Schott's Söhne (Mainz, Plate 20623, págs. 10–13) · Tresillos de Arpegios en 24 Tonalidades (2/4) + D.S. al Fine"
        pdf_file = "reichert_r5_transcripcion.pdf"
        tempo_min, tempo_max, tempo_def = 100, 192, 152
        tempo_unit = "♪"
        arts = [
            {**a, "fname": f"{a['slug'].replace('_Articulacion', '_Reichert_R5_Articulacion').replace('_Original_Op5', '_Reichert_R5_Original_Op5')}.abc"}
            for a in ARTS_12
        ]
        pages_meta = [
            {"num": 10, "title": "7 EXERCICES JOURNALIERS POUR LA FLÛTE · Op. 5 — Nº 5", "subtitle": "de 144 à 184 = ♪ · Tonalidades 1–6 (Do Mayor a Sol menor · Compases 1–48)", "secStart": 0, "secEnd": 5},
            {"num": 11, "title": "REICHERT Op. 5 — Nº 5 (Pág. 11)", "subtitle": "Tonalidades 7–12 (Mi♭ Mayor a Si♭ menor · Compases 49–96)", "secStart": 6, "secEnd": 11},
            {"num": 12, "title": "REICHERT Op. 5 — Nº 5 (Pág. 12)", "subtitle": "Tonalidades 13–18 (Sol♭ Mayor a Do♯ menor · Compases 97–144)", "secStart": 12, "secEnd": 17},
            {"num": 13, "title": "REICHERT Op. 5 — Nº 5 (Pág. 13)", "subtitle": "Tonalidades 19–24 (La Mayor a Mi menor + D.S. al Fine · Compases 145–200)", "secStart": 18, "secEnd": 24},
        ]

    pages_html = []
    for idx, pm in enumerate(pages_meta):
        art_strip_html = ""
        if idx == 0:
            art_strip_html = """
      <div class="ej-instruction">A travailler successivement avec chacune des articulations suivantes :</div>
      <div class="art-strip-box">
        <div id="art-strip-1"></div>
        <div id="art-strip-2"></div>
      </div>"""
        pages_html.append(f"""
    <section class="leduc-page" id="page-{pm['num']}">
      <div class="page-header">
        <span class="ej-main-title">{pm['title']}</span>
        <span class="ej-page-num">Pág. {pm['num']}</span>
      </div>
      <div class="ej-instruction">{pm['subtitle']}</div>{art_strip_html}
      <div class="systems-list" id="systems-page-{pm['num']}"></div>
      <div class="page-footer">
        <span>M. A. Reichert — 7 Exercices Journaliers pour la Flûte, Op. 5</span>
        <span>B. Schott's Söhne · Plate 20623</span>
        <span>Página {pm['num']}</span>
      </div>
    </section>""")

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <script src="https://cdn.jsdelivr.net/npm/abcjs@6.4.4/dist/abcjs-basic-min.js"></script>
  <style>
    :root {{
      --bg-dark: #0f172a;
      --card-dark: #1e293b;
      --border-dark: rgba(255,255,255,0.12);
      --paper: #fdfaf3;
      --paper-border: #d6cfc2;
      --ink: #111827;
      --accent: #2563eb;
      --gold: #f59e0b;
      --emerald: #10b981;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Georgia', 'Times New Roman', serif;
      background: var(--bg-dark);
      color: #f8fafc;
      min-height: 100vh;
      padding-bottom: 48px;
    }}
    .top-toolbar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: rgba(15, 23, 42, 0.96);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-dark);
      padding: 12px 20px;
      box-shadow: 0 8px 28px rgba(0,0,0,0.45);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .toolbar-row {{
      max-width: 1360px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .brand-title {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 16px;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.2px;
    }}
    .brand-sub {{
      font-size: 12px;
      color: #94a3b8;
      font-weight: 500;
      margin-top: 2px;
    }}
    .controls-wrap {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }}
    .play-btn {{
      background: linear-gradient(135deg, #10b981, #059669);
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 8px 15px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 3px 12px rgba(16, 185, 129, 0.35);
      transition: all 0.15s ease;
    }}
    .play-btn:hover {{ transform: translateY(-1px); }}
    .play-btn.playing {{
      background: linear-gradient(135deg, #ef4444, #dc2626);
      box-shadow: 0 3px 12px rgba(239, 68, 68, 0.4);
    }}
    .tempo-box {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(255,255,255,0.06);
      border: 1px solid var(--border-dark);
      padding: 5px 10px;
      border-radius: 8px;
      font-size: 12px;
      color: #cbd5e1;
    }}
    .tempo-box input[type="range"] {{
      width: 80px;
      accent-color: var(--gold);
      cursor: pointer;
    }}
    .tool-btn {{
      background: rgba(255,255,255,0.08);
      color: #e2e8f0;
      border: 1px solid var(--border-dark);
      border-radius: 8px;
      padding: 7px 12px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: background 0.15s;
    }}
    .tool-btn:hover {{ background: rgba(255,255,255,0.15); color: #fff; }}
    .selector-strip {{
      max-width: 1360px;
      margin: 8px auto 0 auto;
      padding-top: 8px;
      border-top: 1px solid rgba(255,255,255,0.08);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .strip-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 5px;
    }}
    .strip-label {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: #94a3b8;
      margin-right: 4px;
      min-width: 125px;
    }}
    .pill-btn {{
      background: rgba(255,255,255,0.06);
      color: #cbd5e1;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 6px;
      padding: 4px 8px;
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.12s;
    }}
    .pill-btn:hover {{
      background: rgba(255,255,255,0.14);
      color: #fff;
    }}
    .pill-btn.active {{
      background: var(--gold);
      color: #0f172a;
      border-color: var(--gold);
      font-weight: 800;
    }}
    .pill-btn.active-sec {{
      background: #3b82f6;
      color: #fff;
      border-color: #60a5fa;
      font-weight: 700;
    }}
    .pages-wrapper {{
      max-width: 1360px;
      margin: 22px auto;
      padding: 0 16px;
      display: flex;
      flex-direction: column;
      gap: 28px;
    }}
    .leduc-page {{
      background: var(--paper);
      color: var(--ink);
      border: 1px solid var(--paper-border);
      border-radius: 6px;
      box-shadow: 0 16px 44px rgba(0,0,0,0.45);
      padding: 22px 26px 16px 26px;
      position: relative;
    }}
    .page-header {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      border-bottom: 1.5px solid #1f2937;
      padding-bottom: 5px;
      margin-bottom: 5px;
    }}
    .ej-main-title {{
      font-size: 19px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #111827;
    }}
    .ej-page-num {{
      font-size: 16px;
      font-weight: 700;
      color: #111827;
    }}
    .ej-instruction {{
      text-align: center;
      font-style: italic;
      font-size: 13px;
      color: #1f2937;
      margin-bottom: 5px;
    }}
    .art-strip-box {{
      background: rgba(255,255,255,0.58);
      border: 1px solid #d6cfc2;
      border-radius: 4px;
      padding: 3px 6px 1px 6px;
      margin-bottom: 8px;
    }}
    .art-strip-box svg {{
      width: 100% !important;
      height: auto !important;
      display: block;
    }}
    .focus-card {{
      display: none;
      background: #fffbeb;
      border: 2px solid #f59e0b;
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 14px;
      box-shadow: 0 6px 18px rgba(245, 158, 11, 0.16);
    }}
    .focus-card.visible {{ display: block; }}
    .focus-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 6px;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .focus-title {{
      font-size: 14px;
      font-weight: 800;
      color: #92400e;
    }}
    .focus-badge {{
      font-size: 11.5px;
      font-weight: 700;
      background: #fef3c7;
      color: #78350f;
      border: 1px solid #f59e0b;
      padding: 2px 9px;
      border-radius: 999px;
    }}
    .systems-list {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .system-row {{
      display: flex;
      align-items: center;
      border-radius: 4px;
      padding: 0 2px;
      margin: -4px 0;
      cursor: pointer;
      transition: background 0.12s;
    }}
    .system-row:hover {{
      background: rgba(59, 130, 246, 0.08);
    }}
    .system-row.active-system {{
      background: rgba(245, 158, 11, 0.18);
      border-left: 3px solid #d97706;
      padding-left: 4px;
    }}
    .sys-label {{
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 10px;
      font-weight: 800;
      color: #475569;
      min-width: 62px;
      text-align: right;
      padding-right: 6px;
      user-select: none;
      line-height: 1.15;
    }}
    .sys-label .sec-tag {{
      display: block;
      font-size: 9px;
      color: #2563eb;
      font-weight: 700;
    }}
    .system-staff {{
      flex: 1;
      min-width: 0;
    }}
    .system-staff svg {{
      width: 100% !important;
      height: auto !important;
      display: block;
    }}
    .page-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 8px;
      padding-top: 5px;
      border-top: 1px solid #d6cfc2;
      font-size: 11px;
      color: #4b5563;
      font-weight: 600;
    }}
    .abc-drawer {{
      max-width: 1360px;
      margin: 18px auto 0 auto;
      padding: 0 16px;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    details.abc-details {{
      background: var(--card-dark);
      border: 1px solid var(--border-dark);
      border-radius: 10px;
      padding: 12px 16px;
    }}
    details.abc-details summary {{
      cursor: pointer;
      font-weight: 700;
      font-size: 13px;
      color: #93c5fd;
    }}
    .abc-textarea {{
      width: 100%;
      height: 220px;
      margin-top: 10px;
      background: #090d16;
      color: #a7f3d0;
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 6px;
      padding: 10px;
      font-family: 'SFMono-Regular', Consolas, monospace;
      font-size: 11.5px;
      line-height: 1.45;
    }}
    @page {{
      size: A4 portrait;
      margin: 3mm;
    }}
    @media print {{
      body {{ background: #fff; color: #000; padding: 0; }}
      .top-toolbar, .abc-drawer, .focus-card {{ display: none !important; }}
      .pages-wrapper {{ margin: 0; padding: 0; max-width: 100%; gap: 0; }}
      .leduc-page {{
        box-shadow: none;
        border: none;
        padding: 1mm 2mm;
        zoom: 0.56;
        page-break-after: always;
        break-after: page;
      }}
      .leduc-page:last-child {{
        page-break-after: auto;
        break-after: auto;
      }}
      .system-row {{ margin: -6px 0; }}
    }}
  </style>
</head>
<body>

  <header class="top-toolbar">
    <div class="toolbar-row">
      <div>
        <div class="brand-title">
          <span>🪈 {brand_main}</span>
        </div>
        <div class="brand-sub">
          {brand_sub}
        </div>
      </div>

      <div class="controls-wrap">
        <button id="play-btn" class="play-btn" onclick="togglePlay()">
          <span id="play-icon">▶</span>
          <span id="play-label">Escuchar Piano</span>
        </button>

        <div class="tempo-box">
          <span>{tempo_unit} =</span>
          <input type="range" id="tempo-slider" min="{tempo_min}" max="{tempo_max}" value="{tempo_def}" oninput="updateTempo(this.value)">
          <strong id="tempo-label">{tempo_def} BPM</strong>
        </div>

        <span id="measure-badge" class="tool-btn" style="cursor:default;">
          Tonalidades: 1–24 + D.S.
        </span>

        <button class="tool-btn" onclick="copyCurrentAbc()">
          📋 <span id="copy-label">Copiar ABC</span>
        </button>

        <a id="download-abc-link" class="tool-btn" href="downloads/abc/{arts[0]['fname']}" download>
          ⬇ ABC Activo
        </a>

        <a class="tool-btn" href="downloads/pdf/{pdf_file}" target="_blank">
          📄 PDF Alta Resolución
        </a>

        <a class="tool-btn" href="index.html">
          ← Portal
        </a>
      </div>
    </div>

    <div class="selector-strip">
      <div class="strip-row" id="art-buttons-row">
        <span class="strip-label">Articulación:</span>
      </div>
      <div class="strip-row" id="sec-buttons-row">
        <span class="strip-label">Tonalidad (24 + D.S.):</span>
      </div>
    </div>
  </header>

  <main class="pages-wrapper">
    <div id="focus-card" class="focus-card">
      <div class="focus-header">
        <div class="focus-title" id="focus-title">🎯 Tonalidad Activa: 1. Do Mayor</div>
        <div class="focus-badge" id="focus-badge">Compases 1–4</div>
      </div>
      <div id="focus-staff"></div>
    </div>
    {"".join(pages_html)}
  </main>

  <section class="abc-drawer">
    <details class="abc-details">
      <summary>🔍 Ver / Copiar Código Fuente ABC Completo de la Articulación Activa</summary>
      <textarea id="abc-source-box" class="abc-textarea" readonly></textarea>
    </details>
  </section>

  <script>
    const EX_CODE = {json.dumps(code)};
    const EX_ARTS = {json.dumps(arts, ensure_ascii=False)};
    const EX_SECTIONS = {json.dumps(sections_data, ensure_ascii=False)};
    const PAGES_META = {json.dumps(pages_meta, ensure_ascii=False)};

    const ART_STRIP_12_ROW1 = [
      "X:901", "M:6/8", "L:1/16", "K:C", "V:1 clef=treble stem=down",
      '"^1" (cccccc cccccc) || "^2" (cccccc) (cccccc) || "^3" (cccc).c.c (cccc).c.c || "^4" .c.c(cccc) .c.c(cccc) || "^5" (cc).c.c.c.c (cc).c.c.c.c ||'
    ].join("\\n");
    const ART_STRIP_12_ROW2 = [
      "X:902", "M:2/4", "L:1/16", "K:C", "V:1 clef=treble stem=down",
      '"^6" (ccc) (ccc) (ccc) (ccc) || "^7" (ccc) .c.c.c (ccc) .c.c.c || [M:6/8] "^8" (cc)(cc)(cc) (cc)(cc)(cc) || "^9" .c(cc)(cc).c .c(cc)(cc).c || "^10" .c.c.c.c.c.c .c.c.c.c.c.c ||'
    ].join("\\n");
    const ART_STRIP_8_ROW1 = [
      "X:903", "M:2/4", "L:1/16", "K:C", "V:1 clef=treble",
      '"^1" (CDEFGABc) || "^2" (CDEF)(GABc) || "^3" .C(DEF) .G(ABc) || "^4" (CD).E.F (GA).B.c || "^5" .C.D(EF) .G.A(Bc) || "^6" .C(DE).F .G(AB).c || "^7" (CD)(EF)(GA)(Bc) || "^8" .C(DE)(FG)(AB).c ||'
    ].join("\\n");

    let currentArtId = 0;
    let currentSecIdx = -1;
    let currentTempo = {tempo_def};
    let isPlaying = false;
    let audioCtx = null;
    let playTimeouts = [];

    function format12Notes(n, artId) {{
      switch (artId) {{
        case 0:
        case 1:  return `(${{n.slice(0,6).join("")}} ${{n.slice(6,12).join("")}})`;
        case 2:  return `(${{n.slice(0,6).join("")}}) (${{n.slice(6,12).join("")}})`;
        case 3:  return `(${{n[0]}}${{n[1]}}${{n[2]}}${{n[3]}}).${{n[4]}}.${{n[5]}} (${{n[6]}}${{n[7]}}${{n[8]}}${{n[9]}}).${{n[10]}}.${{n[11]}}`;
        case 4:  return `.${{n[0]}}.${{n[1]}}(${{n[2]}}${{n[3]}}${{n[4]}}${{n[5]}}) .${{n[6]}}.${{n[7]}}(${{n[8]}}${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 5:  return `(${{n[0]}}${{n[1]}}).${{n[2]}}.${{n[3]}}.${{n[4]}}.${{n[5]}} (${{n[6]}}${{n[7]}}).${{n[8]}}.${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        case 6:  return `(${{n[0]}}${{n[1]}}${{n[2]}})(${{n[3]}}${{n[4]}}${{n[5]}}) (${{n[6]}}${{n[7]}}${{n[8]}})(${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 7:  return `(${{n[0]}}${{n[1]}}${{n[2]}}).${{n[3]}}.${{n[4]}}.${{n[5]}} (${{n[6]}}${{n[7]}}${{n[8]}}).${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        case 8:  return `(${{n[0]}}${{n[1]}})(${{n[2]}}${{n[3]}})(${{n[4]}}${{n[5]}}) (${{n[6]}}${{n[7]}})(${{n[8]}}${{n[9]}})(${{n[10]}}${{n[11]}})`;
        case 9:  return `.${{n[0]}}(${{n[1]}}${{n[2]}})(${{n[3]}}${{n[4]}}).${{n[5]}} .${{n[6]}}(${{n[7]}}${{n[8]}})(${{n[9]}}${{n[10]}}).${{n[11]}}`;
        case 10: return n.slice(0,6).map(x => "." + x).join("") + " " + n.slice(6,12).map(x => "." + x).join("");
        default: return n.slice(0,6).join("") + " " + n.slice(6,12).join("");
      }}
    }}

    function format12Triplets(n, artId, showNum) {{
      const p = showNum ? "(3" : "";
      switch (artId) {{
        case 0:  return `${{p}}${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}} ${{p}}${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}}`;
        case 1:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}} ${{p}}${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 2:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}}) ${{p}}(${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 3:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}).${{n[4]}}.${{n[5]}} ${{p}}(${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}).${{n[10]}}.${{n[11]}}`;
        case 4:  return `${{p}}.${{n[0]}}.${{n[1]}}(${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}}) ${{p}}.${{n[6]}}.${{n[7]}}(${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 5:  return `${{p}}(${{n[0]}}${{n[1]}}).${{n[2]}} ${{p}}.${{n[3]}}.${{n[4]}}.${{n[5]}} ${{p}}(${{n[6]}}${{n[7]}}).${{n[8]}} ${{p}}.${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        case 6:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}}) ${{p}}(${{n[3]}}${{n[4]}}${{n[5]}}) ${{p}}(${{n[6]}}${{n[7]}}${{n[8]}}) ${{p}}(${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 7:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}}) ${{p}}.${{n[3]}}.${{n[4]}}.${{n[5]}} ${{p}}(${{n[6]}}${{n[7]}}${{n[8]}}) ${{p}}.${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        case 8:  return `${{p}}(${{n[0]}}${{n[1]}})(${{n[2]}} ${{p}}${{n[3]}})(${{n[4]}}${{n[5]}}) ${{p}}(${{n[6]}}${{n[7]}})(${{n[8]}} ${{p}}${{n[9]}})(${{n[10]}}${{n[11]}})`;
        case 9:  return `${{p}}.${{n[0]}}(${{n[1]}}${{n[2]}}) ${{p}}(${{n[3]}}${{n[4]}}).${{n[5]}} ${{p}}.${{n[6]}}(${{n[7]}}${{n[8]}}) ${{p}}(${{n[9]}}${{n[10]}}).${{n[11]}}`;
        case 10: return `${{p}}.${{n[0]}}.${{n[1]}}.${{n[2]}} ${{p}}.${{n[3]}}.${{n[4]}}.${{n[5]}} ${{p}}.${{n[6]}}.${{n[7]}}.${{n[8]}} ${{p}}.${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        default: return `${{p}}${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}} ${{p}}${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}}`;
      }}
    }}

    function format8Notes(n, artId) {{
      switch (artId) {{
        case 0:
        case 1: return `(${{n.slice(0,4).join("")}} ${{n.slice(4,8).join("")}})`;
        case 2: return `(${{n.slice(0,4).join("")}}) (${{n.slice(4,8).join("")}})`;
        case 3: return `.${{n[0]}}(${{n[1]}}${{n[2]}}${{n[3]}}) .${{n[4]}}(${{n[5]}}${{n[6]}}${{n[7]}})`;
        case 4: return `(${{n[0]}}${{n[1]}}).${{n[2]}}.${{n[3]}} (${{n[4]}}${{n[5]}}).${{n[6]}}.${{n[7]}}`;
        case 5: return `.${{n[0]}}.${{n[1]}}(${{n[2]}}${{n[3]}}) .${{n[4]}}.${{n[5]}}(${{n[6]}}${{n[7]}})`;
        case 6: return `.${{n[0]}}(${{n[1]}}${{n[2]}}).${{n[3]}} .${{n[4]}}(${{n[5]}}${{n[6]}}).${{n[7]}}`;
        case 7: return `(${{n[0]}}${{n[1]}})(${{n[2]}}${{n[3]}}) (${{n[4]}}${{n[5]}})(${{n[6]}}${{n[7]}})`;
        case 8: return `.${{n[0]}}(${{n[1]}}${{n[2]}})(${{n[3]}}${{n[4]}})(${{n[5]}}${{n[6]}}).${{n[7]}}`;
        default: return n.slice(0,4).join("") + " " + n.slice(4,8).join("");
      }}
    }}

    function format4Notes(n, artId) {{
      switch (artId) {{
        case 0:
        case 1:
        case 2: return `(${{n.join("")}})`;
        case 3: return `.${{n[0]}}(${{n[1]}}${{n[2]}}${{n[3]}})`;
        case 4: return `(${{n[0]}}${{n[1]}}).${{n[2]}}.${{n[3]}}`;
        case 5: return `.${{n[0]}}.${{n[1]}}(${{n[2]}}${{n[3]}})`;
        case 6:
        case 8: return `.${{n[0]}}(${{n[1]}}${{n[2]}}).${{n[3]}}`;
        case 7: return `(${{n[0]}}${{n[1]}})(${{n[2]}}${{n[3]}})`;
        default: return n.join("");
      }}
    }}

    function buildSectionAbcBody(secIdx, artId, forSystemPart = -1) {{
      const sec = EX_SECTIONS[secIdx];
      const b = sec.bars;
      const segno = secIdx === 0 ? "!segno!" : "";
      const endBar = (secIdx === 0 || secIdx === 23 || secIdx === 24) ? "|]" : "||";
      const fineStr = (secIdx === 0 || secIdx === 24) ? "!fine!" : (secIdx === 23 ? "!D.S.!" : "");

      if (EX_CODE === "R1") {{
        const n4 = b[3];
        let m1, m2, m3, m4;
        if (artId === 0 || artId === 1) {{
          m1 = `${{segno}}(${{b[0].slice(0,6).join("")}} ${{b[0].slice(6,12).join("")}}`;
          m2 = `${{b[1].slice(0,6).join("")}} ${{b[1].slice(6,12).join("")}}`;
          m3 = `${{b[2].slice(0,6).join("")}} ${{b[2].slice(6,12).join("")}}`;
          m4 = `${{n4.slice(0,6).join("")}} !wedge!${{n4[6]}}2) ${{fineStr}}z2 z2 ${{endBar}}`;
        }} else {{
          m1 = segno + format12Notes(b[0], artId);
          m2 = format12Notes(b[1], artId);
          m3 = format12Notes(b[2], artId);
          const g6 = format12Notes(n4.slice(0,6).concat(n4.slice(0,6)), artId).split(" ")[0];
          m4 = `${{g6}} !wedge!${{n4[6]}}2 ${{fineStr}}z2 z2 ${{endBar}}`;
        }}
        return `${{m1}} | ${{m2}} | ${{m3}} | ${{m4}}`;
      }} else if (EX_CODE === "R2") {{
        const ott = sec.is8va ? '"^8va..."' : "";
        const pk = b[0];
        let pkStr, midStrs, m8Str;
        if (artId === 0 || artId === 1) {{
          pkStr = `${{segno}}${{ott}}(${{pk.join("")}}`;
          midStrs = b.slice(1,8).map(m => `${{m.slice(0,4).join("")}} ${{m.slice(4,8).join("")}}`);
          m8Str = `!wedge!${{b[8][0]}}2) ${{fineStr}}z2 ${{endBar}}`;
        }} else {{
          pkStr = `${{segno}}${{ott}}` + format4Notes(pk, artId);
          midStrs = b.slice(1,8).map(m => format8Notes(m, artId));
          m8Str = `!wedge!${{b[8][0]}}2 ${{fineStr}}z2 ${{endBar}}`;
        }}
        if (forSystemPart === 2) {{
          return `${{pkStr}} | ${{midStrs.slice(0,4).join(" | ")}} |\\n${{midStrs.slice(4,7).join(" | ")}} | ${{m8Str}}`;
        }}
        return `${{pkStr}} | ${{midStrs.join(" | ")}} | ${{m8Str}}`;
      }} else if (EX_CODE === "R4") {{
        const ott = sec.is8va ? '"^8va..."' : "";
        const m4 = b[3];
        let b1, b2, b3, b4;
        if (artId === 0 || artId === 1) {{
          b1 = `${{segno}}${{ott}}(${{b[0].slice(0,4).join("")}} ${{b[0].slice(4,8).join("")}} ${{b[0].slice(8,12).join("")}} ${{b[0].slice(12,16).join("")}}`;
          b2 = `${{b[1].slice(0,4).join("")}} ${{b[1].slice(4,8).join("")}} ${{b[1].slice(8,12).join("")}} ${{b[1].slice(12,16).join("")}}`;
          b3 = `${{b[2].slice(0,4).join("")}} ${{b[2].slice(4,8).join("")}} ${{b[2].slice(8,12).join("")}} ${{b[2].slice(12,16).join("")}}`;
          b4 = `${{m4.slice(0,4).join("")}} ${{m4.slice(4,8).join("")}} ${{m4.slice(8,12).join("")}} !wedge!${{m4[12]}}2) ${{fineStr}}z2 ${{endBar}}`;
        }} else {{
          b1 = `${{segno}}${{ott}}` + format8Notes(b[0].slice(0,8), artId) + " " + format8Notes(b[0].slice(8,16), artId);
          b2 = format8Notes(b[1].slice(0,8), artId) + " " + format8Notes(b[1].slice(8,16), artId);
          b3 = format8Notes(b[2].slice(0,8), artId) + " " + format8Notes(b[2].slice(8,16), artId);
          b4 = format8Notes(m4.slice(0,8), artId) + " " + format4Notes(m4.slice(8,12), artId) + ` !wedge!${{m4[12]}}2 ${{fineStr}}z2 ${{endBar}}`;
        }}
        if (forSystemPart === 2) {{
          return `${{b1}} | ${{b2}} |\\n${{b3}} | ${{b4}}`;
        }}
        return `${{b1}} | ${{b2}} | ${{b3}} | ${{b4}}`;
      }} else {{
        // R5 (8 bars per section: part 0 = bars 0..3, part 1 = bars 4..7)
        const m8 = b[7];
        let bStrs, m8Str;
        if (artId === 0) {{
          bStrs = b.slice(0,7).map((bar, idx) => format12Triplets(bar, 0, secIdx === 0 && idx < 4));
          bStrs[0] = `${{segno}}(` + bStrs[0];
          m8Str = `${{m8[0]}}${{m8[1]}}${{m8[2]}} ${{m8[3]}}${{m8[4]}}${{m8[5]}} !wedge!${{m8[6]}}2) ${{fineStr}}z2 ${{endBar}}`;
        }} else {{
          bStrs = b.slice(0,7).map(bar => format12Triplets(bar, artId, false));
          bStrs[0] = segno + bStrs[0];
          if (artId === 6) {{
            m8Str = `(${{m8[0]}}${{m8[1]}}${{m8[2]}}) (${{m8[3]}}${{m8[4]}}${{m8[5]}}) !wedge!${{m8[6]}}2 ${{fineStr}}z2 ${{endBar}}`;
          }} else if (artId === 7) {{
            m8Str = `(${{m8[0]}}${{m8[1]}}${{m8[2]}}) .${{m8[3]}}.${{m8[4]}}.${{m8[5]}} !wedge!${{m8[6]}}2 ${{fineStr}}z2 ${{endBar}}`;
          }} else if (artId === 10) {{
            m8Str = `.${{m8[0]}}.${{m8[1]}}.${{m8[2]}} .${{m8[3]}}.${{m8[4]}}.${{m8[5]}} !wedge!${{m8[6]}}2 ${{fineStr}}z2 ${{endBar}}`;
          }} else {{
            m8Str = `(${{m8[0]}}${{m8[1]}}${{m8[2]}} ${{m8[3]}}${{m8[4]}}${{m8[5]}}) !wedge!${{m8[6]}}2 ${{fineStr}}z2 ${{endBar}}`;
          }}
        }}
        if (forSystemPart === 0) {{
          return bStrs.slice(0,4).join(" | ") + " |";
        }} else if (forSystemPart === 1) {{
          return bStrs.slice(4,7).join(" | ") + ` | ${{m8Str}}`;
        }}
        return bStrs.slice(0,4).join(" | ") + " |\\n" + bStrs.slice(4,7).join(" | ") + ` | ${{m8Str}}`;
      }}
    }}

    function getActiveMeter(artId, includeMeter) {{
      if (!includeMeter) return "none";
      if (EX_CODE === "R1") return EX_ARTS[artId].meter;
      if (EX_CODE === "R4") return "C";
      return "2/4";
    }}

    function initLayout() {{
      const artRow = document.getElementById("art-buttons-row");
      EX_ARTS.forEach(art => {{
        const btn = document.createElement("button");
        btn.className = "pill-btn" + (art.id === currentArtId ? " active" : "");
        btn.id = `art-btn-${{art.id}}`;
        btn.textContent = art.short;
        btn.title = `${{art.name}} — ${{art.formula}}`;
        btn.onclick = () => selectArticulation(art.id);
        artRow.appendChild(btn);
      }});

      const secRow = document.getElementById("sec-buttons-row");
      const allBtn = document.createElement("button");
      allBtn.className = "pill-btn active-sec";
      allBtn.id = "sec-btn-all";
      allBtn.textContent = "Todas (24 + D.S.)";
      allBtn.onclick = () => selectSection(-1);
      secRow.appendChild(allBtn);

      EX_SECTIONS.forEach(sec => {{
        const btn = document.createElement("button");
        btn.className = "pill-btn";
        btn.id = `sec-btn-${{sec.id}}`;
        btn.textContent = sec.short;
        btn.title = sec.titleEs;
        btn.onclick = () => selectSection(sec.id);
        secRow.appendChild(btn);
      }});

      PAGES_META.forEach(pm => {{
        const container = document.getElementById(`systems-page-${{pm.num}}`);
        container.innerHTML = "";
        for (let s = pm.secStart; s <= pm.secEnd; s++) {{
          const sec = EX_SECTIONS[s];
          if (EX_CODE === "R5") {{
            for (let half = 0; half < 2; half++) {{
              const sysId = s * 2 + half;
              const mStart = sec.startMeasure + half * 4;
              const mEnd = mStart + 3;
              const row = document.createElement("div");
              row.className = "system-row";
              row.id = `sys-row-${{sysId}}`;
              row.onclick = () => selectSection(s);
              row.innerHTML = `
                <div class="sys-label">
                  c.${{mStart}}–${{mEnd}}
                  <span class="sec-tag">${{half === 0 ? sec.short : "↳ cont."}}</span>
                </div>
                <div class="system-staff" id="sys-staff-${{sysId}}"></div>
              `;
              container.appendChild(row);
            }}
          }} else {{
            const row = document.createElement("div");
            row.className = "system-row";
            row.id = `sys-row-${{s}}`;
            row.onclick = () => selectSection(s);
            row.innerHTML = `
              <div class="sys-label">
                c.${{sec.startMeasure}}–${{sec.endMeasure}}
                <span class="sec-tag">${{sec.short}}</span>
              </div>
              <div class="system-staff" id="sys-staff-${{s}}"></div>
            `;
            container.appendChild(row);
          }}
        }}
      }});
    }}

    function renderStaffLine(elemId, abc, virtualWidth, padY = 0) {{
      const el = document.getElementById(elemId);
      if (!el) return;
      ABCJS.renderAbc(elemId, abc, {{
        staffwidth: virtualWidth,
        paddingtop: padY,
        paddingbottom: padY,
        paddingleft: 2,
        paddingright: 4
      }});
      const svg = el.querySelector("svg");
      if (svg) {{
        const w = parseFloat(svg.getAttribute("width")) || (virtualWidth + 10);
        const h = parseFloat(svg.getAttribute("height")) || 85;
        svg.setAttribute("viewBox", `0 0 ${{w}} ${{h}}`);
        svg.style.width = "100%";
        svg.style.height = "auto";
        svg.style.display = "block";
      }}
    }}

    function buildFullAbcText(artId) {{
      const art = EX_ARTS[artId];
      const lines = [
        `X:${{artId + 1}}`,
        `T:Reichert Op. 5, ${{EX_CODE}} (${{art.name}})`,
        "C:Mathieu-André Reichert (Ed. B. Schott's Söhne, Plate 20623)",
        `M:${{getActiveMeter(artId, true)}}`,
        "L:1/16",
        `K:C`,
        "V:1 clef=treble"
      ];
      for (let s = 0; s < 25; s++) {{
        const sec = EX_SECTIONS[s];
        lines.push(`% --- ${{sec.titleEs}} ---`);
        lines.push(`[K:${{sec.keySig}}] ` + buildSectionAbcBody(s, artId, -1));
      }}
      return lines.join("\\n");
    }}

    function renderAll() {{
      if (EX_CODE === "R1" || EX_CODE === "R5") {{
        renderStaffLine("art-strip-1", ART_STRIP_12_ROW1, 2050, 1);
        renderStaffLine("art-strip-2", ART_STRIP_12_ROW2, 2050, 1);
      }} else {{
        renderStaffLine("art-strip-1", ART_STRIP_8_ROW1, 2050, 1);
      }}

      if (EX_CODE === "R5") {{
        for (let s = 0; s < 25; s++) {{
          const sec = EX_SECTIONS[s];
          for (let half = 0; half < 2; half++) {{
            const sysId = s * 2 + half;
            const meterStr = (half === 0) ? getActiveMeter(currentArtId, true) : "none";
            const abc = [
              `X:${{sysId + 1}}`,
              "%%stretchlast 1",
              `M:${{meterStr}}`,
              "L:1/16",
              `K:${{sec.keySig}}`,
              "V:1 clef=treble",
              buildSectionAbcBody(s, currentArtId, half)
            ].join("\\n");
            renderStaffLine(`sys-staff-${{sysId}}`, abc, 1950, 0);
          }}
        }}
      }} else {{
        const vWidth = (EX_CODE === "R2") ? 2280 : (EX_CODE === "R4" ? 2080 : 1880);
        for (let s = 0; s < 25; s++) {{
          const sec = EX_SECTIONS[s];
          const meterStr = getActiveMeter(currentArtId, s === 0);
          const abc = [
            `X:${{s + 1}}`,
            "%%stretchlast 1",
            `M:${{meterStr}}`,
            "L:1/16",
            `K:${{sec.keySig}}`,
            "V:1 clef=treble",
            buildSectionAbcBody(s, currentArtId, -1)
          ].join("\\n");
          renderStaffLine(`sys-staff-${{s}}`, abc, vWidth, 0);
        }}
      }}

      const focusCard = document.getElementById("focus-card");
      if (currentSecIdx >= 0) {{
        const sec = EX_SECTIONS[currentSecIdx];
        const art = EX_ARTS[currentArtId];
        focusCard.classList.add("visible");
        document.getElementById("focus-title").textContent = `🎯 Tonalidad Activa: ${{sec.titleEs}} — ${{art.name}}`;
        const minM = Math.min(...sec.midis);
        const maxM = Math.max(...sec.midis);
        document.getElementById("focus-badge").textContent = `Compases ${{sec.startMeasure}}–${{sec.endMeasure}} · ${{sec.midis.length}} notas (MIDI ${{minM}}–${{maxM}})`;
        const focusAbc = [
          "X:500",
          "%%stretchlast 1",
          `M:${{getActiveMeter(currentArtId, true)}}`,
          "L:1/16",
          `K:${{sec.keySig}}`,
          "V:1 clef=treble",
          buildSectionAbcBody(currentSecIdx, currentArtId, (EX_CODE === "R2" || EX_CODE === "R4") ? 2 : -1)
        ].join("\\n");
        renderStaffLine("focus-staff", focusAbc, 1650, 2);
      }} else {{
        focusCard.classList.remove("visible");
      }}

      document.getElementById("abc-source-box").value = buildFullAbcText(currentArtId);
      const dlLink = document.getElementById("download-abc-link");
      if (dlLink) dlLink.href = "downloads/abc/" + EX_ARTS[currentArtId].fname;
    }}

    function selectArticulation(artId) {{
      currentArtId = artId;
      EX_ARTS.forEach(a => {{
        const el = document.getElementById(`art-btn-${{a.id}}`);
        if (el) el.classList.toggle("active", a.id === artId);
      }});
      if (isPlaying) {{
        stopPlayback();
        startPlayback();
      }}
      renderAll();
    }}

    function highlightActiveSection(secIdx) {{
      if (EX_CODE === "R5") {{
        for (let sysId = 0; sysId < 50; sysId++) {{
          const r = document.getElementById(`sys-row-${{sysId}}`);
          if (r) r.classList.toggle("active-system", Math.floor(sysId / 2) === secIdx);
        }}
      }} else {{
        for (let s = 0; s < 25; s++) {{
          const r = document.getElementById(`sys-row-${{s}}`);
          if (r) r.classList.toggle("active-system", s === secIdx);
        }}
      }}
    }}

    function selectSection(secIdx) {{
      currentSecIdx = secIdx;
      const allBtn = document.getElementById("sec-btn-all");
      if (allBtn) allBtn.classList.toggle("active-sec", secIdx === -1);
      EX_SECTIONS.forEach(sec => {{
        const btn = document.getElementById(`sec-btn-${{sec.id}}`);
        if (btn) btn.classList.toggle("active-sec", sec.id === secIdx);
      }});
      highlightActiveSection(secIdx);
      const badge = document.getElementById("measure-badge");
      if (secIdx >= 0) {{
        const sec = EX_SECTIONS[secIdx];
        badge.textContent = `Tonalidad: ${{sec.short}} (c. ${{sec.startMeasure}}–${{sec.endMeasure}})`;
      }} else {{
        badge.textContent = `Tonalidades: 1–24 + D.S.`;
      }}
      if (isPlaying) {{
        stopPlayback();
        startPlayback();
      }}
      renderAll();
    }}

    function updateTempo(val) {{
      currentTempo = parseInt(val, 10) || {tempo_def};
      document.getElementById("tempo-label").textContent = `${{currentTempo}} BPM`;
    }}

    function midiToFreq(midi) {{
      return 440 * Math.pow(2, (midi - 69) / 12);
    }}

    function playPianoNote(midi, startTime, durationSec, isStaccato) {{
      if (!audioCtx) return;
      const freq = midiToFreq(midi);
      const effDur = isStaccato ? Math.min(durationSec * 0.42, 0.09) : durationSec * 0.94;
      const osc1 = audioCtx.createOscillator();
      const osc2 = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc1.type = "triangle";
      osc2.type = "sine";
      osc1.frequency.setValueAtTime(freq, startTime);
      osc2.frequency.setValueAtTime(freq * 2, startTime);
      const g2 = audioCtx.createGain();
      g2.gain.setValueAtTime(0.18, startTime);
      gain.gain.setValueAtTime(0.0001, startTime);
      gain.gain.linearRampToValueAtTime(0.28, startTime + 0.008);
      gain.gain.exponentialRampToValueAtTime(0.0008, startTime + effDur);
      osc1.connect(gain);
      osc2.connect(g2);
      g2.connect(gain);
      gain.connect(audioCtx.destination);
      osc1.start(startTime);
      osc2.start(startTime);
      osc1.stop(startTime + effDur + 0.02);
      osc2.stop(startTime + effDur + 0.02);
    }}

    function isNoteStaccato(artId, pos, totalNotes) {{
      if (pos === totalNotes - 1) return true; // Final eighth note has wedge!
      if (EX_CODE === "R1" || EX_CODE === "R5") {{
        const pos6 = pos % 6;
        switch (artId) {{
          case 3:  return pos6 === 4 || pos6 === 5;
          case 4:  return pos6 === 0 || pos6 === 1;
          case 5:  return pos6 >= 2;
          case 7:  return pos6 >= 3;
          case 9:  return pos6 === 0 || pos6 === 5;
          case 10: return true;
          default: return false;
        }}
      }} else {{
        const pos4 = pos % 4;
        switch (artId) {{
          case 3:  return pos4 === 0;
          case 4:  return pos4 === 2 || pos4 === 3;
          case 5:  return pos4 === 0 || pos4 === 1;
          case 6:  return pos4 === 0 || pos4 === 3;
          case 8:  return (pos % 8 === 0) || (pos % 8 === 7);
          default: return false;
        }}
      }}
    }}

    function getSixteenthDurationSec() {{
      if (EX_CODE === "R1") return (60 / currentTempo) / 6;   // dotted quarter = currentTempo
      if (EX_CODE === "R5") return (60 / currentTempo) / 3;   // eighth note = currentTempo (3 triplet sixteenths per eighth)
      return (60 / currentTempo) / 4;                         // quarter note = currentTempo
    }}

    function startPlayback() {{
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === "suspended") audioCtx.resume();
      isPlaying = true;
      const btn = document.getElementById("play-btn");
      btn.classList.add("playing");
      document.getElementById("play-icon").textContent = "⏹";
      document.getElementById("play-label").textContent = "Detener";

      const noteDur = getSixteenthDurationSec();
      const secsToPlay = currentSecIdx >= 0 ? [EX_SECTIONS[currentSecIdx]] : EX_SECTIONS;
      let cursor = audioCtx.currentTime + 0.06;

      secsToPlay.forEach(sec => {{
        const N = sec.midis.length;
        for (let i = 0; i < N; i++) {{
          const isLast = (i === N - 1);
          const dur = isLast ? noteDur * 2 : noteDur;
          const stacc = isNoteStaccato(currentArtId, i, N);
          playPianoNote(sec.midis[i], cursor, dur, stacc);

          if (i === 0) {{
            const delayMs = Math.max(0, (cursor - audioCtx.currentTime) * 1000);
            const tid = setTimeout(() => {{
              if (!isPlaying) return;
              document.getElementById("measure-badge").textContent = `${{sec.short}} (c. ${{sec.startMeasure}}–${{sec.endMeasure}})`;
              highlightActiveSection(sec.id);
            }}, delayMs);
            playTimeouts.push(tid);
          }}
          cursor += isLast ? noteDur * 4 : noteDur;
        }}
      }});

      const totalMs = Math.max(0, (cursor - audioCtx.currentTime) * 1000);
      playTimeouts.push(setTimeout(() => stopPlayback(), totalMs));
    }}

    function stopPlayback() {{
      isPlaying = false;
      playTimeouts.forEach(t => clearTimeout(t));
      playTimeouts = [];
      if (audioCtx) {{
        try {{ audioCtx.close(); }} catch (e) {{}}
        audioCtx = null;
      }}
      const btn = document.getElementById("play-btn");
      if (btn) btn.classList.remove("playing");
      document.getElementById("play-icon").textContent = "▶";
      document.getElementById("play-label").textContent = "Escuchar Piano";
    }}

    function togglePlay() {{
      if (isPlaying) stopPlayback();
      else startPlayback();
    }}

    function copyCurrentAbc() {{
      const txt = document.getElementById("abc-source-box").value;
      navigator.clipboard.writeText(txt).then(() => {{
        const lbl = document.getElementById("copy-label");
        lbl.textContent = "¡Copiado!";
        setTimeout(() => {{ lbl.textContent = "Copiar ABC"; }}, 1800);
      }});
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      initLayout();
      renderAll();
    }});
  </script>
</body>
</html>
"""
    return html


def write_web_and_validation_htmls(r1_data, r2_data, r4_data, r5_data):
    for code, data in [("R1", r1_data), ("R2", r2_data), ("R4", r4_data), ("R5", r5_data)]:
        html = generate_web_player_html(code, data)
        lower_code = code.lower()
        web_path = os.path.join(WORKSPACE, "docs", f"{lower_code}.html")
        val_name = f"reichert_{lower_code}_validacion.html"
        val_root = os.path.join(WORKSPACE, val_name)
        val_art = os.path.join(ARTIFACT_DIR, val_name)
        for p in [web_path, val_root, val_art]:
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)


# ---------------------------------------------------------------------------
# Update Shared score_template.html (iOS & Android)
# ---------------------------------------------------------------------------
def update_score_template(r1_data, r2_data, r4_data, r5_data):
    ios_template = os.path.join(WORKSPACE, "FluteModes", "FluteModes", "Resources", "score_template.html")
    android_template = os.path.join(WORKSPACE, "FluteModesAndroid", "app", "src", "main", "assets", "score_template.html")

    with open(ios_template, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove previous Reichert block if present
    start_marker = "// === BEGIN REICHERT OP5 SCHOTT ==="
    end_marker = "// === END REICHERT OP5 SCHOTT ==="
    if start_marker in content and end_marker in content:
        s_idx = content.index(start_marker)
        e_idx = content.index(end_marker) + len(end_marker)
        content = content[:s_idx].rstrip() + "\n" + content[e_idx:].lstrip()

    reichert_js = f"""// === BEGIN REICHERT OP5 SCHOTT ===
    const R1_SECTIONS_DATA = {json.dumps(r1_data, ensure_ascii=False)};
    const R2_SECTIONS_DATA = {json.dumps(r2_data, ensure_ascii=False)};
    const R4_SECTIONS_DATA = {json.dumps(r4_data, ensure_ascii=False)};
    const R5_SECTIONS_DATA = {json.dumps(r5_data, ensure_ascii=False)};
    const REICHERT_ARTS_8 = {json.dumps(ARTS_8, ensure_ascii=False)};
    const REICHERT_ARTS_12 = {json.dumps(ARTS_12, ensure_ascii=False)};

    function formatReichert8(n, artId) {{
      switch (artId) {{
        case 0:
        case 1: return `(${{n.slice(0,4).join("")}} ${{n.slice(4,8).join("")}})`;
        case 2: return `(${{n.slice(0,4).join("")}}) (${{n.slice(4,8).join("")}})`;
        case 3: return `.${{n[0]}}(${{n[1]}}${{n[2]}}${{n[3]}}) .${{n[4]}}(${{n[5]}}${{n[6]}}${{n[7]}})`;
        case 4: return `(${{n[0]}}${{n[1]}}).${{n[2]}}.${{n[3]}} (${{n[4]}}${{n[5]}}).${{n[6]}}.${{n[7]}}`;
        case 5: return `.${{n[0]}}.${{n[1]}}(${{n[2]}}${{n[3]}}) .${{n[4]}}.${{n[5]}}(${{n[6]}}${{n[7]}})`;
        case 6: return `.${{n[0]}}(${{n[1]}}${{n[2]}}).${{n[3]}} .${{n[4]}}(${{n[5]}}${{n[6]}}).${{n[7]}}`;
        case 7: return `(${{n[0]}}${{n[1]}})(${{n[2]}}${{n[3]}}) (${{n[4]}}${{n[5]}})(${{n[6]}}${{n[7]}})`;
        case 8: return `.${{n[0]}}(${{n[1]}}${{n[2]}})(${{n[3]}}${{n[4]}})(${{n[5]}}${{n[6]}}).${{n[7]}}`;
        default: return n.slice(0,4).join("") + " " + n.slice(4,8).join("");
      }}
    }}

    function formatReichert4(n, artId) {{
      switch (artId) {{
        case 0:
        case 1:
        case 2: return `(${{n.join("")}})`;
        case 3: return `.${{n[0]}}(${{n[1]}}${{n[2]}}${{n[3]}})`;
        case 4: return `(${{n[0]}}${{n[1]}}).${{n[2]}}.${{n[3]}}`;
        case 5: return `.${{n[0]}}.${{n[1]}}(${{n[2]}}${{n[3]}})`;
        case 6:
        case 8: return `.${{n[0]}}(${{n[1]}}${{n[2]}}).${{n[3]}}`;
        case 7: return `(${{n[0]}}${{n[1]}})(${{n[2]}}${{n[3]}})`;
        default: return n.join("");
      }}
    }}

    function formatReichert12Triplets(n, artId, showNum) {{
      const p = showNum ? "(3" : "";
      switch (artId) {{
        case 0:  return `${{p}}${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}} ${{p}}${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}}`;
        case 1:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}} ${{p}}${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 2:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}}) ${{p}}(${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 3:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}).${{n[4]}}.${{n[5]}} ${{p}}(${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}).${{n[10]}}.${{n[11]}}`;
        case 4:  return `${{p}}.${{n[0]}}.${{n[1]}}(${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}}) ${{p}}.${{n[6]}}.${{n[7]}}(${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 5:  return `${{p}}(${{n[0]}}${{n[1]}}).${{n[2]}} ${{p}}.${{n[3]}}.${{n[4]}}.${{n[5]}} ${{p}}(${{n[6]}}${{n[7]}}).${{n[8]}} ${{p}}.${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        case 6:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}}) ${{p}}(${{n[3]}}${{n[4]}}${{n[5]}}) ${{p}}(${{n[6]}}${{n[7]}}${{n[8]}}) ${{p}}(${{n[9]}}${{n[10]}}${{n[11]}})`;
        case 7:  return `${{p}}(${{n[0]}}${{n[1]}}${{n[2]}}) ${{p}}.${{n[3]}}.${{n[4]}}.${{n[5]}} ${{p}}(${{n[6]}}${{n[7]}}${{n[8]}}) ${{p}}.${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        case 8:  return `${{p}}(${{n[0]}}${{n[1]}})(${{n[2]}} ${{p}}${{n[3]}})(${{n[4]}}${{n[5]}}) ${{p}}(${{n[6]}}${{n[7]}})(${{n[8]}} ${{p}}${{n[9]}})(${{n[10]}}${{n[11]}})`;
        case 9:  return `${{p}}.${{n[0]}}(${{n[1]}}${{n[2]}}) ${{p}}(${{n[3]}}${{n[4]}}).${{n[5]}} ${{p}}.${{n[6]}}(${{n[7]}}${{n[8]}}) ${{p}}(${{n[9]}}${{n[10]}}).${{n[11]}}`;
        case 10: return `${{p}}.${{n[0]}}.${{n[1]}}.${{n[2]}} ${{p}}.${{n[3]}}.${{n[4]}}.${{n[5]}} ${{p}}.${{n[6]}}.${{n[7]}}.${{n[8]}} ${{p}}.${{n[9]}}.${{n[10]}}.${{n[11]}}`;
        default: return `${{p}}${{n[0]}}${{n[1]}}${{n[2]}} ${{p}}${{n[3]}}${{n[4]}}${{n[5]}} ${{p}}${{n[6]}}${{n[7]}}${{n[8]}} ${{p}}${{n[9]}}${{n[10]}}${{n[11]}}`;
      }}
    }}

    function buildR1SecAbc(secIdx, artId, includeMeter) {{
      const sec = R1_SECTIONS_DATA[secIdx] || R1_SECTIONS_DATA[0];
      const art = REICHERT_ARTS_12[artId] || REICHERT_ARTS_12[0];
      const b = sec.bars;
      const n4 = b[3];
      const segno = secIdx === 0 ? "!segno!" : "";
      const endBar = (secIdx === 0 || secIdx === 23 || secIdx === 24) ? "|]" : "||";
      const fineStr = (secIdx === 0 || secIdx === 24) ? "!fine!" : (secIdx === 23 ? "!D.S.!" : "");
      let m1, m2, m3, m4;
      if (artId === 0 || artId === 1) {{
        m1 = `${{segno}}(${{b[0].slice(0,6).join("")}} ${{b[0].slice(6,12).join("")}}`;
        m2 = `${{b[1].slice(0,6).join("")}} ${{b[1].slice(6,12).join("")}}`;
        m3 = `${{b[2].slice(0,6).join("")}} ${{b[2].slice(6,12).join("")}}`;
        m4 = `${{n4.slice(0,6).join("")}} !wedge!${{n4[6]}}2) ${{fineStr}}z2 z2 ${{endBar}}`;
      }} else {{
        m1 = segno + formatEj5_10Measure12(b[0], artId);
        m2 = formatEj5_10Measure12(b[1], artId);
        m3 = formatEj5_10Measure12(b[2], artId);
        const g6 = formatEj5_10Measure12(n4.slice(0,6).concat(n4.slice(0,6)), artId).split(" ")[0];
        m4 = `${{g6}} !wedge!${{n4[6]}}2 ${{fineStr}}z2 z2 ${{endBar}}`;
      }}
      return [
        `X:${{secIdx + 1}}`,
        "%%stretchlast 1",
        `M:${{includeMeter ? art.meter : "none"}}`,
        "L:1/16",
        `K:${{sec.keySig}}`,
        "V:1 clef=treble",
        `"${{sec.short}}" ${{m1}} | ${{m2}} | ${{m3}} | ${{m4}}`
      ].join("\\n");
    }}

    function renderR1Schott(artId, secIdx) {{
      const paper = document.getElementById("paper");
      const art = REICHERT_ARTS_12[artId] || REICHERT_ARTS_12[0];
      const sec = R1_SECTIONS_DATA[secIdx] || R1_SECTIONS_DATA[0];
      let html = `
        <div class="ej1-leduc-wrapper">
          <div class="ej1-top-header">
            <div class="ej1-title">REICHERT Op. 5, Nº 1 — <em>EXERCICE JOURNALIER (6/8)</em></div>
            <div class="ej1-active-badge">${{art.name}} (${{art.meter}})</div>
          </div>
          <div class="ej1-subtitle">Edición Urtext B. Schott's Söhne (Plate 20623, págs. 2–3) · 24 Tonalidades Mayores y Menores:</div>
          <div id="r1-art-row-1" class="ej1-art-row" style="border-bottom:none; margin-bottom:0;"></div>
          <div id="r1-art-row-2" class="ej1-art-row"></div>
          <div style="margin: 8px 0 12px 0; padding: 8px 8px 4px 8px; border: 1.5px solid #2563eb; border-radius: 10px; background: #f8fafc;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px; margin-bottom:4px;">
              <span style="font-family:-apple-system,sans-serif; font-size:12px; font-weight:700; color:#1e3a8a;">🎯 Tonalidad Activa: ${{sec.titleEs}}</span>
              <span style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:600; color:#475569; background:#e2e8f0; padding:2px 8px; border-radius:999px;">Compases ${{sec.startMeasure}}–${{sec.endMeasure}} de 100</span>
            </div>
            <div id="r1-focus-score" class="ej1-staff-row"></div>
          </div>
          <div style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.6px; margin: 12px 4px 6px 4px; border-top: 1px solid #cbd5e1; padding-top: 8px;">Partitura Urtext Completa · B. Schott's Söhne Plate 20623 (Págs. 2–3)</div>
      `;
      for (let i = 0; i < 25; i++) {{
        const hl = (i === secIdx) ? "background:#eff6ff; border-left:3px solid #2563eb; padding-left:4px; border-radius:4px;" : "";
        html += `<div id="r1-sec-row-${{i}}" class="ej1-staff-row" style="${{hl}}"></div>`;
      }}
      html += `<div class="ej1-plate-footer">B. Schott's Söhne · 20623</div></div>`;
      paper.innerHTML = html;

      ABCJS.renderAbc("r1-art-row-1", EJ5_10_ART_ROW1_ABC, {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      ABCJS.renderAbc("r1-art-row-2", EJ5_10_ART_ROW2_ABC, {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      ABCJS.renderAbc("r1-focus-score", buildR1SecAbc(secIdx, artId, true), {{ staffwidth: 920, paddingtop: 3, paddingbottom: 3, paddingleft: 2, paddingright: 2, responsive: "resize", add_classes: true }});
      for (let i = 0; i < 25; i++) {{
        ABCJS.renderAbc(`r1-sec-row-${{i}}`, buildR1SecAbc(i, artId, i === 0), {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      }}
    }}

    function buildR2SecAbc(secIdx, artId, twoLines) {{
      const sec = R2_SECTIONS_DATA[secIdx] || R2_SECTIONS_DATA[0];
      const b = sec.bars;
      const segno = secIdx === 0 ? "!segno!" : "";
      const ott = sec.is8va ? '"^8va..."' : "";
      const endBar = (secIdx === 0 || secIdx === 23 || secIdx === 24) ? "|]" : "||";
      const fineStr = (secIdx === 0 || secIdx === 24) ? "!fine!" : (secIdx === 23 ? "!D.S.!" : "");
      const pk = b[0];
      let pkStr, midStrs, m8Str;
      if (artId === 0 || artId === 1) {{
        pkStr = `${{segno}}${{ott}}(${{pk.join("")}}`;
        midStrs = b.slice(1,8).map(m => `${{m.slice(0,4).join("")}} ${{m.slice(4,8).join("")}}`);
        m8Str = `!wedge!${{b[8][0]}}2) ${{fineStr}}z2 ${{endBar}}`;
      }} else {{
        pkStr = `${{segno}}${{ott}}` + formatReichert4(pk, artId);
        midStrs = b.slice(1,8).map(m => formatReichert8(m, artId));
        m8Str = `!wedge!${{b[8][0]}}2 ${{fineStr}}z2 ${{endBar}}`;
      }}
      const body = twoLines
        ? `"${{sec.short}}" ${{pkStr}} | ${{midStrs.slice(0,4).join(" | ")}} |\\n${{midStrs.slice(4,7).join(" | ")}} | ${{m8Str}}`
        : `"${{sec.short}}" ${{pkStr}} | ${{midStrs.join(" | ")}} | ${{m8Str}}`;
      return [
        `X:${{secIdx + 1}}`,
        "%%stretchlast 1",
        `M:${{(secIdx === 0 || twoLines) ? "2/4" : "none"}}`,
        "L:1/16",
        `K:${{sec.keySig}}`,
        "V:1 clef=treble",
        body
      ].join("\\n");
    }}

    function renderR2Schott(artId, secIdx) {{
      const paper = document.getElementById("paper");
      const art = REICHERT_ARTS_8[artId] || REICHERT_ARTS_8[0];
      const sec = R2_SECTIONS_DATA[secIdx] || R2_SECTIONS_DATA[0];
      let html = `
        <div class="ej1-leduc-wrapper">
          <div class="ej1-top-header">
            <div class="ej1-title">REICHERT Op. 5, Nº 2 — <em>ARPÈGES MODULANTS (2/4)</em></div>
            <div class="ej1-active-badge">${{art.name}} (2/4)</div>
          </div>
          <div class="ej1-subtitle">Edición Urtext B. Schott's Söhne (Plate 20623, págs. 4–5) · 24 Tonalidades Mayores y Menores:</div>
          <div id="r2-art-score" class="ej1-art-row"></div>
          <div style="margin: 8px 0 12px 0; padding: 8px 8px 4px 8px; border: 1.5px solid #2563eb; border-radius: 10px; background: #f8fafc;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px; margin-bottom:4px;">
              <span style="font-family:-apple-system,sans-serif; font-size:12px; font-weight:700; color:#1e3a8a;">🎯 Tonalidad Activa: ${{sec.titleEs}}${{sec.is8va ? " (8va)" : ""}}</span>
              <span style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:600; color:#475569; background:#e2e8f0; padding:2px 8px; border-radius:999px;">Compases ${{sec.startMeasure}}–${{sec.endMeasure}} de 200</span>
            </div>
            <div id="r2-focus-score" class="ej1-staff-row"></div>
          </div>
          <div style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.6px; margin: 12px 4px 6px 4px; border-top: 1px solid #cbd5e1; padding-top: 8px;">Partitura Urtext Completa · B. Schott's Söhne Plate 20623 (Págs. 4–5)</div>
      `;
      for (let i = 0; i < 25; i++) {{
        const hl = (i === secIdx) ? "background:#eff6ff; border-left:3px solid #2563eb; padding-left:4px; border-radius:4px;" : "";
        html += `<div id="r2-sec-row-${{i}}" class="ej1-staff-row" style="${{hl}}"></div>`;
      }}
      html += `<div class="ej1-plate-footer">B. Schott's Söhne · 20623</div></div>`;
      paper.innerHTML = html;

      ABCJS.renderAbc("r2-art-score", EJ4_ARTICULATIONS_ABC, {{ staffwidth: 920, paddingtop: 2, paddingbottom: 2, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      ABCJS.renderAbc("r2-focus-score", buildR2SecAbc(secIdx, artId, true), {{ staffwidth: 900, paddingtop: 3, paddingbottom: 3, paddingleft: 2, paddingright: 2, responsive: "resize", add_classes: true }});
      for (let i = 0; i < 25; i++) {{
        ABCJS.renderAbc(`r2-sec-row-${{i}}`, buildR2SecAbc(i, artId, false), {{ staffwidth: 1080, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      }}
    }}

    function buildR4SecAbc(secIdx, artId, twoLines) {{
      const sec = R4_SECTIONS_DATA[secIdx] || R4_SECTIONS_DATA[0];
      const b = sec.bars;
      const m4 = b[3];
      const segno = secIdx === 0 ? "!segno!" : "";
      const ott = sec.is8va ? '"^8va..."' : "";
      const endBar = (secIdx === 0 || secIdx === 23 || secIdx === 24) ? "|]" : "||";
      const fineStr = (secIdx === 0 || secIdx === 24) ? "!fine!" : (secIdx === 23 ? "!D.S.!" : "");
      let b1, b2, b3, b4;
      if (artId === 0 || artId === 1) {{
        b1 = `${{segno}}${{ott}}(${{b[0].slice(0,4).join("")}} ${{b[0].slice(4,8).join("")}} ${{b[0].slice(8,12).join("")}} ${{b[0].slice(12,16).join("")}}`;
        b2 = `${{b[1].slice(0,4).join("")}} ${{b[1].slice(4,8).join("")}} ${{b[1].slice(8,12).join("")}} ${{b[1].slice(12,16).join("")}}`;
        b3 = `${{b[2].slice(0,4).join("")}} ${{b[2].slice(4,8).join("")}} ${{b[2].slice(8,12).join("")}} ${{b[2].slice(12,16).join("")}}`;
        b4 = `${{m4.slice(0,4).join("")}} ${{m4.slice(4,8).join("")}} ${{m4.slice(8,12).join("")}} !wedge!${{m4[12]}}2) ${{fineStr}}z2 ${{endBar}}`;
      }} else {{
        b1 = `${{segno}}${{ott}}` + formatReichert8(b[0].slice(0,8), artId) + " " + formatReichert8(b[0].slice(8,16), artId);
        b2 = formatReichert8(b[1].slice(0,8), artId) + " " + formatReichert8(b[1].slice(8,16), artId);
        b3 = formatReichert8(b[2].slice(0,8), artId) + " " + formatReichert8(b[2].slice(8,16), artId);
        b4 = formatReichert8(m4.slice(0,8), artId) + " " + formatReichert4(m4.slice(8,12), artId) + ` !wedge!${{m4[12]}}2 ${{fineStr}}z2 ${{endBar}}`;
      }}
      const body = twoLines
        ? `"${{sec.short}}" ${{b1}} | ${{b2}} |\\n${{b3}} | ${{b4}}`
        : `"${{sec.short}}" ${{b1}} | ${{b2}} | ${{b3}} | ${{b4}}`;
      return [
        `X:${{secIdx + 1}}`,
        "%%stretchlast 1",
        `M:${{(secIdx === 0 || twoLines) ? "C" : "none"}}`,
        "L:1/16",
        `K:${{sec.keySig}}`,
        "V:1 clef=treble",
        body
      ].join("\\n");
    }}

    function renderR4Schott(artId, secIdx) {{
      const paper = document.getElementById("paper");
      const art = REICHERT_ARTS_8[artId] || REICHERT_ARTS_8[0];
      const sec = R4_SECTIONS_DATA[secIdx] || R4_SECTIONS_DATA[0];
      let html = `
        <div class="ej1-leduc-wrapper">
          <div class="ej1-top-header">
            <div class="ej1-title">REICHERT Op. 5, Nº 4 — <em>EXERCICE D'AGILITÉ (4/4)</em></div>
            <div class="ej1-active-badge">${{art.name}} (4/4)</div>
          </div>
          <div class="ej1-subtitle">Edición Urtext B. Schott's Söhne (Plate 20623, págs. 8–9) · 24 Tonalidades Mayores y Menores:</div>
          <div id="r4-art-score" class="ej1-art-row"></div>
          <div style="margin: 8px 0 12px 0; padding: 8px 8px 4px 8px; border: 1.5px solid #2563eb; border-radius: 10px; background: #f8fafc;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px; margin-bottom:4px;">
              <span style="font-family:-apple-system,sans-serif; font-size:12px; font-weight:700; color:#1e3a8a;">🎯 Tonalidad Activa: ${{sec.titleEs}}${{sec.is8va ? " (8va)" : ""}}</span>
              <span style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:600; color:#475569; background:#e2e8f0; padding:2px 8px; border-radius:999px;">Compases ${{sec.startMeasure}}–${{sec.endMeasure}} de 100</span>
            </div>
            <div id="r4-focus-score" class="ej1-staff-row"></div>
          </div>
          <div style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.6px; margin: 12px 4px 6px 4px; border-top: 1px solid #cbd5e1; padding-top: 8px;">Partitura Urtext Completa · B. Schott's Söhne Plate 20623 (Págs. 8–9)</div>
      `;
      for (let i = 0; i < 25; i++) {{
        const hl = (i === secIdx) ? "background:#eff6ff; border-left:3px solid #2563eb; padding-left:4px; border-radius:4px;" : "";
        html += `<div id="r4-sec-row-${{i}}" class="ej1-staff-row" style="${{hl}}"></div>`;
      }}
      html += `<div class="ej1-plate-footer">B. Schott's Söhne · 20623</div></div>`;
      paper.innerHTML = html;

      ABCJS.renderAbc("r4-art-score", EJ4_ARTICULATIONS_ABC, {{ staffwidth: 920, paddingtop: 2, paddingbottom: 2, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      ABCJS.renderAbc("r4-focus-score", buildR4SecAbc(secIdx, artId, true), {{ staffwidth: 900, paddingtop: 3, paddingbottom: 3, paddingleft: 2, paddingright: 2, responsive: "resize", add_classes: true }});
      for (let i = 0; i < 25; i++) {{
        ABCJS.renderAbc(`r4-sec-row-${{i}}`, buildR4SecAbc(i, artId, false), {{ staffwidth: 1040, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      }}
    }}

    function buildR5SecAbc(secIdx, artId) {{
      const sec = R5_SECTIONS_DATA[secIdx] || R5_SECTIONS_DATA[0];
      const b = sec.bars;
      const m8 = b[7];
      const segno = secIdx === 0 ? "!segno!" : "";
      const endBar = (secIdx === 0 || secIdx === 23 || secIdx === 24) ? "|]" : "||";
      const fineStr = (secIdx === 0 || secIdx === 24) ? "!fine!" : (secIdx === 23 ? "!D.S.!" : "");
      let bStrs, m8Str;
      if (artId === 0) {{
        bStrs = b.slice(0,7).map((bar, idx) => formatReichert12Triplets(bar, 0, secIdx === 0 && idx < 4));
        bStrs[0] = `${{segno}}(` + bStrs[0];
        m8Str = `${{m8[0]}}${{m8[1]}}${{m8[2]}} ${{m8[3]}}${{m8[4]}}${{m8[5]}} !wedge!${{m8[6]}}2) ${{fineStr}}z2 ${{endBar}}`;
      }} else {{
        bStrs = b.slice(0,7).map(bar => formatReichert12Triplets(bar, artId, false));
        bStrs[0] = segno + bStrs[0];
        if (artId === 6) {{
          m8Str = `(${{m8[0]}}${{m8[1]}}${{m8[2]}}) (${{m8[3]}}${{m8[4]}}${{m8[5]}}) !wedge!${{m8[6]}}2 ${{fineStr}}z2 ${{endBar}}`;
        }} else if (artId === 7) {{
          m8Str = `(${{m8[0]}}${{m8[1]}}${{m8[2]}}) .${{m8[3]}}.${{m8[4]}}.${{m8[5]}} !wedge!${{m8[6]}}2 ${{fineStr}}z2 ${{endBar}}`;
        }} else if (artId === 10) {{
          m8Str = `.${{m8[0]}}.${{m8[1]}}.${{m8[2]}} .${{m8[3]}}.${{m8[4]}}.${{m8[5]}} !wedge!${{m8[6]}}2 ${{fineStr}}z2 ${{endBar}}`;
        }} else {{
          m8Str = `(${{m8[0]}}${{m8[1]}}${{m8[2]}} ${{m8[3]}}${{m8[4]}}${{m8[5]}}) !wedge!${{m8[6]}}2 ${{fineStr}}z2 ${{endBar}}`;
        }}
      }}
      return [
        `X:${{secIdx + 1}}`,
        "%%stretchlast 1",
        "M:2/4",
        "L:1/16",
        `K:${{sec.keySig}}`,
        "V:1 clef=treble",
        `"${{sec.short}}" ` + bStrs.slice(0,4).join(" | ") + " |",
        bStrs.slice(4,7).join(" | ") + ` | ${{m8Str}}`
      ].join("\\n");
    }}

    function renderR5Schott(artId, secIdx) {{
      const paper = document.getElementById("paper");
      const art = REICHERT_ARTS_12[artId] || REICHERT_ARTS_12[0];
      const sec = R5_SECTIONS_DATA[secIdx] || R5_SECTIONS_DATA[0];
      let html = `
        <div class="ej1-leduc-wrapper">
          <div class="ej1-top-header">
            <div class="ej1-title">REICHERT Op. 5, Nº 5 — <em>ARPÈGES EN TRIOLETS (2/4)</em></div>
            <div class="ej1-active-badge">${{art.name}} (2/4)</div>
          </div>
          <div class="ej1-subtitle">Edición Urtext B. Schott's Söhne (Plate 20623, págs. 10–13) · 24 Tonalidades Mayores y Menores:</div>
          <div id="r5-art-row-1" class="ej1-art-row" style="border-bottom:none; margin-bottom:0;"></div>
          <div id="r5-art-row-2" class="ej1-art-row"></div>
          <div style="margin: 8px 0 12px 0; padding: 8px 8px 4px 8px; border: 1.5px solid #2563eb; border-radius: 10px; background: #f8fafc;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px; margin-bottom:4px;">
              <span style="font-family:-apple-system,sans-serif; font-size:12px; font-weight:700; color:#1e3a8a;">🎯 Tonalidad Activa: ${{sec.titleEs}}</span>
              <span style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:600; color:#475569; background:#e2e8f0; padding:2px 8px; border-radius:999px;">Compases ${{sec.startMeasure}}–${{sec.endMeasure}} de 200</span>
            </div>
            <div id="r5-focus-score" class="ej1-staff-row"></div>
          </div>
          <div style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.6px; margin: 12px 4px 6px 4px; border-top: 1px solid #cbd5e1; padding-top: 8px;">Partitura Urtext Completa · B. Schott's Söhne Plate 20623 (Págs. 10–13)</div>
      `;
      for (let i = 0; i < 25; i++) {{
        const hl = (i === secIdx) ? "background:#eff6ff; border-left:3px solid #2563eb; padding-left:4px; border-radius:4px;" : "";
        html += `<div id="r5-sec-row-${{i}}" class="ej1-staff-row" style="${{hl}}"></div>`;
      }}
      html += `<div class="ej1-plate-footer">B. Schott's Söhne · 20623</div></div>`;
      paper.innerHTML = html;

      ABCJS.renderAbc("r5-art-row-1", EJ5_10_ART_ROW1_ABC, {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      ABCJS.renderAbc("r5-art-row-2", EJ5_10_ART_ROW2_ABC, {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      ABCJS.renderAbc("r5-focus-score", buildR5SecAbc(secIdx, artId), {{ staffwidth: 920, paddingtop: 3, paddingbottom: 3, paddingleft: 2, paddingright: 2, responsive: "resize", add_classes: true }});
      for (let i = 0; i < 25; i++) {{
        ABCJS.renderAbc(`r5-sec-row-${{i}}`, buildR5SecAbc(i, artId), {{ staffwidth: 960, paddingtop: 1, paddingbottom: 1, paddingleft: 0, paddingright: 0, responsive: "resize", add_classes: true }});
      }}
    }}
// === END REICHERT OP5 SCHOTT ===
"""

    target_hook = "function renderScore(abcString) {"
    dispatch_hooks = """function renderScore(abcString) {
      const r1Match = abcString && abcString.match(/%\\s*R1_SCHOTT_ART:(\\d+):SEC:(\\d+)/);
      if (r1Match) {
        renderR1Schott(parseInt(r1Match[1], 10) || 0, parseInt(r1Match[2], 10) || 0);
        return;
      }
      const r2Match = abcString && abcString.match(/%\\s*R2_SCHOTT_ART:(\\d+):SEC:(\\d+)/);
      if (r2Match) {
        renderR2Schott(parseInt(r2Match[1], 10) || 0, parseInt(r2Match[2], 10) || 0);
        return;
      }
      const r4Match = abcString && abcString.match(/%\\s*R4_SCHOTT_ART:(\\d+):SEC:(\\d+)/);
      if (r4Match) {
        renderR4Schott(parseInt(r4Match[1], 10) || 0, parseInt(r4Match[2], 10) || 0);
        return;
      }
      const r5Match = abcString && abcString.match(/%\\s*R5_SCHOTT_ART:(\\d+):SEC:(\\d+)/);
      if (r5Match) {
        renderR5Schott(parseInt(r5Match[1], 10) || 0, parseInt(r5Match[2], 10) || 0);
        return;
      }"""

    # Clean up old r1Match..r5Match if re-running
    if "const r1Match =" not in content:
        content = content.replace(target_hook, reichert_js + "\n" + dispatch_hooks, 1)
    else:
        content = content.replace(target_hook, reichert_js + "\n" + target_hook, 1)

    with open(ios_template, "w", encoding="utf-8") as f:
        f.write(content)
    shutil.copyfile(ios_template, android_template)


if __name__ == "__main__":
    r1 = build_r1_data()
    r2 = build_r2_data()
    r4 = build_r4_data()
    r5 = build_r5_data()
    write_abc_collections()
    write_web_and_validation_htmls(r1, r2, r4, r5)
    update_score_template(r1, r2, r4, r5)
    print("Successfully generated all Reichert Op. 5 ABCs, Web players, Validation HTMLs, and updated score_template.html!")
