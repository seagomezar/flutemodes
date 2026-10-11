#!/usr/bin/env python3
"""
Generador Urtext de Taffanel & Gaubert — E. J. 5 (Gammes Chromatiques)
Ediciones Alphonse Leduc A. L. 16.588, página 115.
Genera:
- taffanel_ej5_completo.abc y colección de 10 articulaciones en abc_ej5/ y docs/downloads/abc/
- taffanel_ej5_validacion.html (en brain/, raíz y docs/ej5.html)
"""

import os
import json

BRAIN_DIR = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"
ROOT_DIR = "/Users/sebas/Desktop/partituras"
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
ABC_EJ5_DIR = os.path.join(ROOT_DIR, "abc_ej5")
DOCS_ABC_DIR = os.path.join(DOCS_DIR, "downloads", "abc")

os.makedirs(ABC_EJ5_DIR, exist_ok=True)
os.makedirs(DOCS_ABC_DIR, exist_ok=True)

EJ5_SCALES = [
    (
        0, "A", "A · Do (Ut)", "A · C Chromatic", "A · Do", "C", 60,
        ["C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "_B", "=B"],
        ["c", "^c", "d", "^d", "e", "f", "^f", "g", "^g", "a", "_b", "=b"],
        ["c'", "b", "_b", "a", "_a", "g", "^f", "=f", "e", "_e", "d", "_d"],
        ["c", "B", "_B", "A", "_A", "G", "^F", "=F", "E", "_E", "D", "_D"],
        "C", "up"
    ),
    (
        1, "B", "B · Re♭ (Ré♭)", "B · D♭ Chromatic", "B · Re♭", "Db", 61,
        ["D", "=D", "E", "=E", "F", "G", "=G", "A", "=A", "B", "_c", "=c"],
        ["d", "=d", "e", "=e", "f", "g", "=g", "a", "=a", "b", "_c'", "=c'"],
        ["d'", "c'", "_c'", "b", "__b", "a", "=g", "_g", "f", "_f", "e", "__e"],
        ["d", "c", "_c", "B", "__B", "A", "=G", "_G", "F", "_F", "E", "__E"],
        "D", "up"
    ),
    (
        2, "C", "C · Re (Ré)", "C · D Chromatic", "C · Re", "D", 62,
        ["D", "^D", "E", "^E", "F", "G", "^G", "A", "^A", "B", "=c", "^c"],
        ["d", "^d", "e", "^e", "f", "g", "^g", "a", "^a", "b", "=c'", "^c'"],
        ["d'", "c'", "=c'", "b", "_b", "a", "^g", "=g", "f", "=f", "e", "_e"],
        ["d", "c", "=c", "B", "_B", "A", "^G", "=G", "F", "=F", "E", "_E"],
        "D", "up"
    ),
    (
        3, "D", "D · Mi♭ (Mi♭)", "D · E♭ Chromatic", "D · Mi♭", "Eb", 63,
        ["E", "=E", "F", "^F", "G", "A", "=A", "B", "=B", "c", "_d", "=d"],
        ["e", "=e", "f", "^f", "g", "a", "=a", "b", "=b", "c'", "_d'", "=d'"],
        ["e'", "d'", "_d'", "c'", "_c'", "b", "=a", "_a", "g", "_g", "f", "_f"],
        ["e", "d", "_d", "c", "_c", "B", "=A", "_A", "G", "_G", "F", "_F"],
        "E", "up"
    ),
    (
        4, "E", "E · Mi (Mi)", "E · E Chromatic", "E · Mi", "E", 64,
        ["E", "^E", "F", "^^F", "G", "A", "^A", "B", "^B", "c", "=d", "^d"],
        ["e", "^e", "f", "^^f", "g", "a", "^a", "b", "^b", "c'", "=d'", "^d'"],
        ["e'", "d'", "=d'", "c'", "=c'", "b", "^a", "=a", "g", "=g", "f", "=f"],
        ["e", "d", "=d", "c", "=c", "B", "^A", "=A", "G", "=G", "F", "=F"],
        "E", "up"
    ),
    (
        5, "F", "F · Fa (Fa)", "F · F Chromatic", "F · Fa", "F", 65,
        ["F", "^F", "G", "^G", "A", "B", "=B", "c", "^c", "d", "_e", "=e"],
        ["f", "^f", "g", "^g", "a", "b", "=b", "c'", "^c'", "d'", "_e'", "=e'"],
        ["f'", "e'", "_e'", "d'", "_d'", "c'", "=b", "_b", "a", "_a", "g", "_g"],
        ["f", "e", "_e", "d", "_d", "c", "=B", "_B", "A", "_A", "G", "_G"],
        "F", "up"
    ),
    (
        6, "G", "G · Sol♭ (Sol♭)", "G · G♭ Chromatic", "G · Sol♭", "Gb", 66,
        ["G", "=G", "A", "=A", "B", "c", "=c", "d", "=d", "e", "_f", "=f"],
        ["g", "=g", "a", "=a", "b", "c'", "=c'", "d'", "=d'", "e'", "_f'", "=f'"],
        ["g'", "f'", "_f'", "e'", "__e'", "d'", "=c'", "_c'", "b", "__b", "a", "__a"],
        ["g", "f", "_f", "e", "__e", "d", "=c", "_c", "B", "__B", "A", "__A"],
        "G", "up"
    ),
    (
        7, "H", "H · Sol (Sol)", "H · G Chromatic", "H · Sol", "G", 67,
        ["G", "^G", "A", "^A", "B", "c", "^c", "d", "^d", "e", "=f", "^f"],
        ["g", "^g", "a", "^a", "b", "c'", "^c'", "d'", "^d'", "e'", "=f'", "^f'"],
        ["g'", "f'", "=f'", "e'", "_e'", "d'", "^c'", "=c'", "b", "_b", "a", "_a"],
        ["g", "f", "=f", "e", "_e", "d", "^c", "=c", "B", "_B", "A", "_A"],
        "G", "up"
    ),
    (
        8, "I", "I · La♭ (La♭)", "I · A♭ Chromatic", "I · La♭", "Ab", 68,
        ["A", "=A", "B", "=B", "c", "d", "=d", "e", "=e", "f", "_g", "=g"],
        ["a", "=a", "b", "=b", "c'", "d'", "=d'", "e'", "=e'", "f'", "_g'", "=g'"],
        ["a'", "g'", "_g'", "f'", "_f'", "e'", "=d'", "_d'", "c'", "_c'", "b", "__b"],
        ["a", "g", "_g", "f", "_f", "e", "=d", "_d", "c", "_c", "B", "__B"],
        "A", "up"
    ),
    (
        9, "J", "J · La (La)", "J · A Chromatic", "J · La", "A", 69,
        ["A", "^A", "B", "^B", "c", "d", "^d", "e", "^e", "f", "=g", "^g"],
        ["a", "^a", "b", "^b", "c'", "d'", "^d'", "e'", "^e'", "f'", "=g'", "^g'"],
        ["a'", "g'", "=g'", "f'", "=f'", "e'", "^d'", "=d'", "c'", "=c'", "b", "_b"],
        ["a", "g", "=g", "f", "=f", "e", "^d", "=d", "c", "=c", "B", "_B"],
        "A", "up"
    ),
    (
        10, "K", "K · Si♭ (Si♭)", "K · B♭ Chromatic", "K · Si♭", "Bb", 70,
        ["B", "=B", "c", "^c", "d", "e", "=e", "f", "^f", "g", "_a", "=a"],
        ["b", "=b", "c'", "^c'", "d'", "e'", "=e'", "f'", "^f'", "g'", "_a'", "=a'"],
        ["b'", "a'", "_a'", "g'", "_g'", "f'", "=e'", "_e'", "d'", "_d'", "c'", "_c'"],
        ["b", "a", "_a", "g", "_g", "f", "=e", "_e", "d", "_d", "c", "_c"],
        "B", "up"
    ),
    (
        11, "L", "L · Si (Si)", "L · B Chromatic", "L · Si", "B", 71,
        ["B", "^B", "c", "^^c", "d", "e", "^e", "f", "^^f", "g", "=a", "^a"],
        ["b", "^b", "c'", "^^c'", "d'", "e'", "^e'", "f'", "^^f'", "g'", "=a'", "^a'"],
        ["b'", "a'", "=a'", "g'", "=g'", "f'", "^e'", "=e'", "d'", "=d'", "c'", "=c'"],
        ["b", "a", "=a", "g", "=g", "f", "^e", "=e", "d", "=d", "c", "=c"],
        "B", "down"
    ),
]

EJ5_ARTICULATIONS_META = [
    {"id": 0,  "meter": "6/8", "name": "Edición Original (Leduc)",            "short": "0. Orig.",        "formula": "6 + 6 notas por compás (6/8 · 2/4)", "fname": "00_Taffanel_EJ5_Original_AL16588.abc"},
    {"id": 1,  "meter": "6/8", "name": "1. 12 Ligadas (Compás completo)",      "short": "1. (12)",         "formula": "(12) · Compás entero ligado en 6/8", "fname": "01_Taffanel_EJ5_Articulacion_01_12_Ligadas.abc"},
    {"id": 2,  "meter": "6/8", "name": "2. 6 y 6 Ligadas",                     "short": "2. (6)(6)",       "formula": "(6) + (6) · Seisillos ligados en 6/8", "fname": "02_Taffanel_EJ5_Articulacion_02_6_y_6_Ligadas.abc"},
    {"id": 3,  "meter": "6/8", "name": "3. 4 Ligadas y 2 Picadas",             "short": "3. (4)··",        "formula": "(4)·· (4)·· en 6/8", "fname": "03_Taffanel_EJ5_Articulacion_03_4_Ligadas_2_Picadas.abc"},
    {"id": 4,  "meter": "6/8", "name": "4. 2 Picadas y 4 Ligadas",             "short": "4. ··(4)",        "formula": "··(4) ··(4) en 6/8", "fname": "04_Taffanel_EJ5_Articulacion_04_2_Picadas_4_Ligadas.abc"},
    {"id": 5,  "meter": "6/8", "name": "5. 2 Ligadas y 4 Picadas",             "short": "5. (2)····",      "formula": "(2)···· (2)···· en 6/8", "fname": "05_Taffanel_EJ5_Articulacion_05_2_Ligadas_4_Picadas.abc"},
    {"id": 6,  "meter": "2/4", "name": "6. De 3 en 3 Ligadas (2/4)",           "short": "6. (3)(3)(3)(3)", "formula": "(3)(3)(3)(3) · 4 grupos de 3 en 2/4", "fname": "06_Taffanel_EJ5_Articulacion_06_De_3_en_3_Ligadas.abc"},
    {"id": 7,  "meter": "2/4", "name": "7. 3 Ligadas y 3 Picadas (2/4)",       "short": "7. (3)···(3)···", "formula": "(3)··· (3)··· · 4 grupos de 3 en 2/4", "fname": "07_Taffanel_EJ5_Articulacion_07_3_Ligadas_3_Picadas.abc"},
    {"id": 8,  "meter": "6/8", "name": "8. De 2 en 2 Ligadas",                 "short": "8. (2)(2)(2)",    "formula": "(2)(2)(2) (2)(2)(2) en 6/8", "fname": "08_Taffanel_EJ5_Articulacion_08_De_2_en_2_Ligadas.abc"},
    {"id": 9,  "meter": "6/8", "name": "9. Sincopadas de a 2",                 "short": "9. ·(2)(2)(2)·",  "formula": "·(2)(2)(2)(2)(2)· desplazadas en 6/8", "fname": "09_Taffanel_EJ5_Articulacion_09_Sincopadas.abc"},
    {"id": 10, "meter": "6/8", "name": "10. Todas Picadas (Staccato)",         "short": "10. ············","formula": "12 notas en staccato por compás en 6/8", "fname": "10_Taffanel_EJ5_Articulacion_10_Todas_Picadas.abc"},
]

def format_measure_12(notes_12, art_id):
    n = notes_12
    if art_id == 0:
        return f"{''.join(n[0:6])} {''.join(n[6:12])}"
    elif art_id == 1:
        return f"({''.join(n[0:6])} {''.join(n[6:12])})"
    elif art_id == 2:
        return f"({''.join(n[0:6])}) ({''.join(n[6:12])})"
    elif art_id == 3:
        return f"({n[0]}{n[1]}{n[2]}{n[3]}).{n[4]}.{n[5]} ({n[6]}{n[7]}{n[8]}{n[9]}).{n[10]}.{n[11]}"
    elif art_id == 4:
        return f".{n[0]}.{n[1]}({n[2]}{n[3]}{n[4]}{n[5]}) .{n[6]}.{n[7]}({n[8]}{n[9]}{n[10]}{n[11]})"
    elif art_id == 5:
        return f"({n[0]}{n[1]}).{n[2]}.{n[3]}.{n[4]}.{n[5]} ({n[6]}{n[7]}).{n[8]}.{n[9]}.{n[10]}.{n[11]}"
    elif art_id == 6:
        return f"({n[0]}{n[1]}{n[2]}) ({n[3]}{n[4]}{n[5]}) ({n[6]}{n[7]}{n[8]}) ({n[9]}{n[10]}{n[11]})"
    elif art_id == 7:
        return f"({n[0]}{n[1]}{n[2]}) .{n[3]}.{n[4]}.{n[5]} ({n[6]}{n[7]}{n[8]}) .{n[9]}.{n[10]}.{n[11]}"
    elif art_id == 8:
        return f"({n[0]}{n[1]})({n[2]}{n[3]})({n[4]}{n[5]}) ({n[6]}{n[7]})({n[8]}{n[9]})({n[10]}{n[11]})"
    elif art_id == 9:
        return f".{n[0]}({n[1]}{n[2]})({n[3]}{n[4]})({n[5]} {n[6]})({n[7]}{n[8]})({n[9]}{n[10]}).{n[11]}"
    elif art_id == 10:
        g1 = "".join(f".{x}" for x in n[0:6])
        g2 = "".join(f".{x}" for x in n[6:12])
        return f"{g1} {g2}"
    return f"{''.join(n[0:6])} {''.join(n[6:12])}"

def generate_ej5_abc(art_id=0):
    meta = EJ5_ARTICULATIONS_META[art_id]
    meter_str = meta["meter"]
    lines = [
        f"X:{art_id + 1}",
        f"T:E. J. 5 — Gammes Chromatiques ({meta['name']})",
        "C:Paul Taffanel & Philippe Gaubert (Ed. Alphonse Leduc A. L. 16.588, pág. 115)",
        "%%stretchlast 1",
        "%%barsperstaff 5",
        f"M:{meter_str}",
        "L:1/16",
        "Q:1/4=96",
        "K:C",
        "V:1 clef=treble stem=down",
    ]
    for sc in EJ5_SCALES:
        idx, letter, title_es, title_en, short_es, key_sig, root_midi, m1, m2, m3, m4, m5, m5_stem = sc
        b1 = format_measure_12(m1, art_id)
        b2 = format_measure_12(m2, art_id)
        b3 = format_measure_12(m3, art_id)
        b4 = format_measure_12(m4, art_id)
        b5 = f"{m5}4 z4 |]"
        lines.append(f'[K:{key_sig}] "{letter}" {b1} | {b2} | {b3} | {b4} | {b5}')
    return "\n".join(lines)

# Guardar todos los archivos .abc individuales y la colección completa
all_abc_blocks = []
for art_id in range(11):
    abc_txt = generate_ej5_abc(art_id)
    fname = EJ5_ARTICULATIONS_META[art_id]["fname"]
    for out_dir in [ABC_EJ5_DIR, DOCS_ABC_DIR]:
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(abc_txt + "\n")
    if art_id >= 1:
        all_abc_blocks.append(abc_txt)

collection_fname = "11_Coleccion_Completa_Taffanel_EJ5_10_Articulaciones.abc"
collection_txt = "\n\n".join(all_abc_blocks) + "\n"
for out_dir in [ABC_EJ5_DIR, DOCS_ABC_DIR]:
    with open(os.path.join(out_dir, collection_fname), "w", encoding="utf-8") as f:
        f.write(collection_txt)

for target in [
    os.path.join(BRAIN_DIR, "taffanel_ej5_completo.abc"),
    os.path.join(ROOT_DIR, "taffanel_ej5_completo.abc"),
]:
    with open(target, "w", encoding="utf-8") as f:
        f.write(generate_ej5_abc(0) + "\n")

# Construir JSON de escalas para el visor HTML
scales_js_data = []
for sc in EJ5_SCALES:
    idx, letter, title_es, title_en, short_es, key_sig, root_midi, m1, m2, m3, m4, m5, m5_stem = sc
    midis = (
        [root_midi + i for i in range(12)] +
        [root_midi + 12 + i for i in range(12)] +
        [root_midi + 24 - i for i in range(12)] +
        [root_midi + 12 - i for i in range(12)] +
        [root_midi]
    )
    scales_js_data.append({
        "id": idx,
        "letter": letter,
        "titleEs": title_es,
        "titleEn": title_en,
        "shortEs": short_es,
        "keySig": key_sig,
        "rootMidi": root_midi,
        "m1": m1,
        "m2": m2,
        "m3": m3,
        "m4": m4,
        "m5": m5,
        "m5Stem": m5_stem,
        "midis": midis
    })

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Taffanel & Gaubert — E. J. 5 (Gammes Chromatiques · Urtext A. L. 16.588)</title>
  <script src="https://cdn.jsdelivr.net/npm/abcjs@6.4.4/dist/abcjs-basic-min.js"></script>
  <style>
    :root {{
      --bg-dark: #0f172a;
      --card-dark: #1e293b;
      --border-dark: rgba(255,255,255,0.12);
      --gold: #d4af37;
      --gold-light: #f3e5ab;
      --paper-bg: #fdfaf3;
      --ink: #18181b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      font-family: 'Georgia', 'Times New Roman', serif;
      background: var(--bg-dark);
      color: #f8fafc;
    }}
    .top-toolbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(15, 23, 42, 0.96);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border-dark);
      padding: 12px 20px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .toolbar-row {{
      max-width: 1380px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }}
    .brand-title {{
      font-size: 16px;
      font-weight: 800;
      color: var(--gold);
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .brand-sub {{
      font-size: 12px;
      color: #94a3b8;
      font-weight: 500;
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
      border-radius: 999px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 3px 12px rgba(16, 185, 129, 0.35);
    }}
    .play-btn.playing {{
      background: linear-gradient(135deg, #ef4444, #dc2626);
      box-shadow: 0 3px 12px rgba(239, 68, 68, 0.35);
    }}
    .tool-btn {{
      background: #1e293b;
      color: #e2e8f0;
      border: 1px solid rgba(255,255,255,0.16);
      border-radius: 8px;
      padding: 7px 12px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}
    .tool-btn:hover {{
      border-color: var(--gold);
      color: var(--gold);
    }}
    .tempo-box {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: #1e293b;
      padding: 5px 10px;
      border-radius: 8px;
      border: 1px solid var(--border-dark);
      font-size: 12px;
    }}
    .selector-strip {{
      max-width: 1380px;
      margin: 8px auto 0 auto;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .strip-row {{
      display: flex;
      align-items: center;
      gap: 5px;
      flex-wrap: wrap;
    }}
    .strip-label {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #94a3b8;
      margin-right: 4px;
    }}
    .pill-btn {{
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 6px;
      padding: 4px 9px;
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .pill-btn:hover {{
      border-color: var(--gold);
      color: #fff;
    }}
    .pill-btn.active {{
      background: var(--gold);
      color: #0f172a;
      border-color: var(--gold);
      font-weight: 800;
    }}
    .pill-btn.active-scale {{
      background: #3b82f6;
      color: #fff;
      border-color: #60a5fa;
      font-weight: 800;
    }}

    /* PÁGINA URTEXT (PÁG. 115) */
    .pages-wrapper {{
      max-width: 1320px;
      margin: 22px auto 50px auto;
      padding: 0 16px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .leduc-page {{
      background: var(--paper-bg);
      color: var(--ink);
      border-radius: 6px;
      box-shadow: 0 16px 42px rgba(0, 0, 0, 0.55);
      border: 1px solid #d6cfc2;
      padding: 28px 32px 24px 32px;
      position: relative;
    }}
    .page-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      border-bottom: 1.5px solid #27272a;
      padding-bottom: 6px;
      margin-bottom: 8px;
    }}
    .ej-main-title {{
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 0.6px;
      color: #111827;
    }}
    .ej-page-num {{
      font-size: 18px;
      font-weight: 700;
      color: #111827;
    }}
    .ej-instruction {{
      font-size: 14px;
      font-style: italic;
      color: #27272a;
      margin: 6px 0 8px 0;
    }}
    .art-strip-box {{
      background: rgba(212, 175, 55, 0.06);
      border: 1px solid #d6cfc2;
      border-radius: 4px;
      padding: 4px 8px;
      margin-bottom: 14px;
    }}
    .focus-card {{
      margin: 0 0 16px 0;
      padding: 12px 16px;
      border: 2px solid #2563eb;
      border-radius: 8px;
      background: #f8fafc;
      display: none;
    }}
    .focus-card.visible {{
      display: block;
    }}
    .focus-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      margin-bottom: 4px;
    }}
    .focus-title {{
      font-size: 14px;
      font-weight: 800;
      color: #1e3a8a;
    }}
    .focus-badge {{
      font-size: 12px;
      font-weight: 700;
      color: #475569;
      background: #e2e8f0;
      padding: 2px 10px;
      border-radius: 999px;
    }}
    /* FILAS A - L */
    .scales-list {{
      display: flex;
      flex-direction: column;
      gap: 0px;
    }}
    .scale-row {{
      display: grid;
      grid-template-columns: 28px 1fr;
      align-items: center;
      border-radius: 6px;
      padding: 0 4px;
      margin: -4px 0;
      cursor: pointer;
      transition: background 0.15s;
    }}
    .scale-row:hover {{
      background: rgba(59, 130, 246, 0.06);
    }}
    .scale-row.selected-row {{
      background: rgba(59, 130, 246, 0.11);
      outline: 1.5px solid rgba(37, 99, 235, 0.45);
    }}
    .scale-letter {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 14px;
      font-weight: 800;
      color: #111827;
      text-align: center;
      user-select: none;
      padding-top: 4px;
    }}
    .scale-staff {{
      width: 100%;
      overflow: hidden;
    }}
    .scale-staff svg {{
      width: 100% !important;
      height: auto !important;
      display: block;
    }}
    .nb-footnote {{
      margin-top: 10px;
      padding-top: 6px;
      border-top: 1px solid #d6cfc2;
      font-size: 12.5px;
      line-height: 1.4;
      color: #18181b;
    }}
    .nb-footnote em {{
      font-style: italic;
    }}
    .nb-footnote strong {{
      font-style: normal;
      font-weight: 700;
      letter-spacing: 0.3px;
    }}
    .plate-footer {{
      text-align: center;
      font-size: 11.5px;
      font-weight: 700;
      color: #3f3f46;
      margin-top: 6px;
      letter-spacing: 0.8px;
    }}

    /* PANEL DE CÓDIGO ABC */
    .abc-code-section {{
      max-width: 1320px;
      margin: 0 auto 60px auto;
      padding: 0 16px;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .abc-details {{
      background: #1e293b;
      border: 1px solid var(--border-dark);
      border-radius: 10px;
      padding: 12px 16px;
    }}
    .abc-details summary {{
      cursor: pointer;
      font-weight: 700;
      font-size: 14px;
      color: var(--gold);
    }}
    .abc-textarea {{
      width: 100%;
      min-height: 260px;
      margin-top: 12px;
      background: #0f172a;
      color: #e2e8f0;
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 8px;
      padding: 12px;
      font-family: 'SFMono-Regular', Consolas, monospace;
      font-size: 12px;
      line-height: 1.45;
    }}

    @page {{
      size: A4 portrait;
      margin: 4mm;
    }}
    @media print {{
      body {{ background: #fff; }}
      .top-toolbar, .abc-code-section, .focus-card {{ display: none !important; }}
      .pages-wrapper {{ margin: 0; padding: 0; max-width: 100%; }}
      .leduc-page {{
        box-shadow: none;
        border: none;
        padding: 2mm 4mm;
        zoom: 0.74;
      }}
      .scale-row {{ margin: -5px 0; }}
    }}
  </style>
</head>
<body>

  <!-- BARRA SUPERIOR INTERACTIVA -->
  <div class="top-toolbar">
    <div class="toolbar-row">
      <div>
        <div class="brand-title">
          <span>🎼 Taffanel & Gaubert — E. J. 5 (Gammes Chromatiques · Urtext A. L. 16.588)</span>
        </div>
        <div class="brand-sub" id="status-subtitle">
          Página 115 · 12 Escalas Cromáticas (A–L, 2 octavas c/u, 60 compases) · 10 Articulaciones Oficiales (6/8 y 2/4)
        </div>
      </div>

      <div class="controls-wrap">
        <button id="play-btn" class="play-btn" onclick="togglePlay()">
          <span id="play-icon">▶</span>
          <span id="play-label">Escuchar Piano</span>
        </button>

        <div class="tempo-box">
          <span>♩ =</span>
          <input type="range" id="tempo-slider" min="50" max="144" value="88" oninput="updateTempo(this.value)">
          <strong id="tempo-label">88 BPM</strong>
        </div>

        <span id="measure-badge" class="tool-btn" style="cursor:default;">Escala: A (c. 1/60)</span>

        <button class="tool-btn" onclick="copyCurrentAbc()">
          <span>📋</span>
          <span id="copy-label">Copiar ABC</span>
        </button>
        <a id="download-abc-link" href="downloads/abc/00_Taffanel_EJ5_Original_AL16588.abc" download class="tool-btn">
          <span>📥</span>
          <span>Descargar .ABC</span>
        </a>
        <button class="tool-btn" onclick="window.print()">
          <span>🖨️</span>
          <span>Imprimir / PDF</span>
        </button>
      </div>
    </div>

    <div class="selector-strip">
      <div class="strip-row" id="art-buttons-row">
        <span class="strip-label">Articulación (1–10):</span>
      </div>
      <div class="strip-row" id="scale-buttons-row">
        <span class="strip-label">Escala Cromática (A–L):</span>
      </div>
    </div>
  </div>

  <!-- PÁGINA 115 URTEXT -->
  <div class="pages-wrapper">
    <div class="leduc-page">
      <div class="page-header">
        <div class="ej-main-title">E. J. 5 — <em>GAMMES CHROMATIQUES</em></div>
        <div class="ej-page-num">115</div>
      </div>
      <div class="ej-instruction">
        A travailler successivement avec chacune des articulations suivantes:
      </div>

      <!-- 10 ARTICULACIONES OFICIALES (2 FILAS: 1-5 en 6/8 y 6-10 en 2/4 + 6/8) -->
      <div class="art-strip-box">
        <div id="ej5-art-strip-1"></div>
        <div id="ej5-art-strip-2" style="margin-top:-6px;"></div>
      </div>

      <!-- TARJETA DE ENFOQUE DE ESCALA SELECCIONADA -->
      <div id="focus-card" class="focus-card">
        <div class="focus-header">
          <div class="focus-title" id="focus-title">🎯 Escala Activa: A · Do (Ut)</div>
          <div class="focus-badge" id="focus-badge">5 Compases · 2 Octavas Cromáticas (Do4 → Do6 → Do4)</div>
        </div>
        <div id="ej5-focus-staff"></div>
      </div>

      <!-- 12 ESCALAS CROMÁTICAS (A a L) -->
      <div class="scales-list" id="scales-list-container"></div>

      <!-- NOTA AL PIE URTEXT (GARIBOLDI) -->
      <div class="nb-footnote">
        <em>N. B. — La Méthode contient tout ce qui concerne les Gammes. Toutefois, les élèves qui voudront avoir sous la main un recueil spécial pour ce travail journalier se procureront utilement l'ouvrage de</em>
        <strong>GARIBOLDI : "ÉTUDE COMPLÈTE DES GAMMES POUR FLÛTE"</strong>
      </div>
      <div class="plate-footer">A. L. 16.588</div>
    </div>
  </div>

  <!-- INSPECTOR DE CÓDIGO ABC -->
  <div class="abc-code-section">
    <details class="abc-details" open>
      <summary>📄 Ver Código Fuente ABC Completo (E. J. 5 · Articulación Activa)</summary>
      <textarea id="abc-source-box" class="abc-textarea" readonly></textarea>
    </details>
  </div>

  <script>
    const EJ5_SCALES = {json.dumps(scales_js_data, ensure_ascii=False)};
    const EJ5_ARTS = {json.dumps(EJ5_ARTICULATIONS_META, ensure_ascii=False)};

    let currentArtId = 0;
    let currentScaleIdx = -1; // -1 = Todas (A-L), 0..11 = A..L individual
    let currentTempo = 88;
    let isPlaying = false;
    let audioCtx = null;
    let playTimeouts = [];

    // Construir ABC de las 2 filas de articulaciones de referencia (1-5 y 6-10)
    const ART_STRIP_ROW1_ABC = [
      "X:101",
      "M:6/8",
      "L:1/16",
      "K:C",
      "V:1 clef=treble stem=down",
      '"^1" (cccccc cccccc) || "^2" (cccccc) (cccccc) || "^3" (cccc).c.c (cccc).c.c || "^4" .c.c(cccc) .c.c(cccc) || "^5" (cc).c.c.c.c (cc).c.c.c.c ||'
    ].join("\\n");

    const ART_STRIP_ROW2_ABC = [
      "X:102",
      "M:2/4",
      "L:1/16",
      "K:C",
      "V:1 clef=treble stem=down",
      '"^6" (ccc) (ccc) (ccc) (ccc) || "^7" (ccc) .c.c.c (ccc) .c.c.c || [M:6/8] "^8" (cc)(cc)(cc) (cc)(cc)(cc) || "^9" .c(cc)(cc)(c c)(cc)(cc).c || "^10" .c.c.c.c.c.c .c.c.c.c.c.c ||'
    ].join("\\n");

    function formatMeasure12(n, artId) {{
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

    function buildSingleScaleAbc(scaleIdx, artId, includeTimeSig) {{
      const sc = EJ5_SCALES[scaleIdx];
      const art = EJ5_ARTS[artId];
      const meterStr = includeTimeSig ? art.meter : "none";
      const b1 = formatMeasure12(sc.m1, artId);
      const b2 = formatMeasure12(sc.m2, artId);
      const b3 = formatMeasure12(sc.m3, artId);
      const b4 = formatMeasure12(sc.m4, artId);
      const b5 = `${{sc.m5}}4 z4 |`;
      return [
        `X:${{scaleIdx + 1}}`,
        "%%stretchlast 1",
        `M:${{meterStr}}`,
        "L:1/16",
        `K:${{sc.keySig}}`,
        "V:1 clef=treble stem=down",
        `${{b1}} | ${{b2}} | ${{b3}} | ${{b4}} | ${{b5}}]`
      ].join("\\n");
    }}

    function buildFullAbcText(artId) {{
      const art = EJ5_ARTS[artId];
      const lines = [
        `X:${{artId + 1}}`,
        `T:E. J. 5 — Gammes Chromatiques (${{art.name}})`,
        "C:Paul Taffanel & Philippe Gaubert (Ed. Alphonse Leduc A. L. 16.588, pág. 115)",
        "%%stretchlast 1",
        `M:${{art.meter}}`,
        "L:1/16",
        `Q:1/4=${{currentTempo}}`,
        "K:C",
        "V:1 clef=treble stem=down"
      ];
      EJ5_SCALES.forEach(sc => {{
        const b1 = formatMeasure12(sc.m1, artId);
        const b2 = formatMeasure12(sc.m2, artId);
        const b3 = formatMeasure12(sc.m3, artId);
        const b4 = formatMeasure12(sc.m4, artId);
        const b5 = `${{sc.m5}}4 z4 |]`;
        lines.push(`[K:${{sc.keySig}}] "${{sc.letter}}" ${{b1}} | ${{b2}} | ${{b3}} | ${{b4}} | ${{b5}}`);
      }});
      return lines.join("\\n");
    }}

    function initSelectors() {{
      const artRow = document.getElementById("art-buttons-row");
      EJ5_ARTS.forEach(art => {{
        const btn = document.createElement("button");
        btn.className = "pill-btn" + (art.id === currentArtId ? " active" : "");
        btn.id = `art-btn-${{art.id}}`;
        btn.textContent = art.short;
        btn.title = `${{art.name}} — ${{art.formula}}`;
        btn.onclick = () => selectArticulation(art.id);
        artRow.appendChild(btn);
      }});

      const scaleRow = document.getElementById("scale-buttons-row");
      const allBtn = document.createElement("button");
      allBtn.className = "pill-btn active-scale";
      allBtn.id = "scale-btn-all";
      allBtn.textContent = "Todas (A–L)";
      allBtn.onclick = () => selectScale(-1);
      scaleRow.appendChild(allBtn);

      EJ5_SCALES.forEach(sc => {{
        const btn = document.createElement("button");
        btn.className = "pill-btn";
        btn.id = `scale-btn-${{sc.id}}`;
        btn.textContent = sc.shortEs;
        btn.onclick = () => selectScale(sc.id);
        scaleRow.appendChild(btn);
      }});

      const listContainer = document.getElementById("scales-list-container");
      listContainer.innerHTML = "";
      EJ5_SCALES.forEach(sc => {{
        const row = document.createElement("div");
        row.className = "scale-row";
        row.id = `scale-row-${{sc.id}}`;
        row.onclick = () => selectScale(sc.id);
        row.innerHTML = `
          <div class="scale-letter">${{sc.letter}}</div>
          <div class="scale-staff" id="ej5-staff-${{sc.id}}"></div>
        `;
        listContainer.appendChild(row);
      }});
    }}

    function renderStaffSingleLine(elemId, abc, virtualWidth, padY = 1) {{
      ABCJS.renderAbc(elemId, abc, {{
        staffwidth: virtualWidth,
        paddingtop: padY,
        paddingbottom: padY,
        paddingleft: 2,
        paddingright: 4
      }});
      const el = document.getElementById(elemId);
      const svg = el && el.querySelector("svg");
      if (svg) {{
        const w = parseFloat(svg.getAttribute("width")) || (virtualWidth + 10);
        const h = parseFloat(svg.getAttribute("height")) || 85;
        svg.setAttribute("viewBox", `0 0 ${{w}} ${{h}}`);
        svg.style.width = "100%";
        svg.style.height = "auto";
        svg.style.display = "block";
      }}
    }}

    function renderAll() {{
      renderStaffSingleLine("ej5-art-strip-1", ART_STRIP_ROW1_ABC, 1750, 1);
      renderStaffSingleLine("ej5-art-strip-2", ART_STRIP_ROW2_ABC, 1750, 1);

      EJ5_SCALES.forEach((sc, idx) => {{
        const abc = buildSingleScaleAbc(idx, currentArtId, idx === 0);
        renderStaffSingleLine(`ej5-staff-${{idx}}`, abc, 2180, 0);
      }});

      const focusCard = document.getElementById("focus-card");
      if (currentScaleIdx >= 0) {{
        const sc = EJ5_SCALES[currentScaleIdx];
        const art = EJ5_ARTS[currentArtId];
        focusCard.classList.add("visible");
        document.getElementById("focus-title").textContent = `🎯 Escala Activa: ${{sc.titleEs}} — ${{art.name}}`;
        document.getElementById("focus-badge").textContent = `Armadura: K:${{sc.keySig}} · Compás: ${{art.meter}} · 5 Compases (MIDI ${{sc.rootMidi}} → ${{sc.rootMidi + 24}} → ${{sc.rootMidi}})`;
        renderStaffSingleLine("ej5-focus-staff", buildSingleScaleAbc(currentScaleIdx, currentArtId, true), 1820, 3);
      }} else {{
        focusCard.classList.remove("visible");
      }}

      const fullAbc = buildFullAbcText(currentArtId);
      document.getElementById("abc-source-box").value = fullAbc;
      const dlLink = document.getElementById("download-abc-link");
      if (dlLink) {{
        dlLink.href = "downloads/abc/" + EJ5_ARTS[currentArtId].fname;
      }}
    }}

    function selectArticulation(artId) {{
      currentArtId = artId;
      EJ5_ARTS.forEach(a => {{
        const el = document.getElementById(`art-btn-${{a.id}}`);
        if (el) el.classList.toggle("active", a.id === artId);
      }});
      if (isPlaying) {{
        stopPlayback();
        startPlayback();
      }}
      renderAll();
    }}

    function selectScale(scaleIdx) {{
      currentScaleIdx = scaleIdx;
      const allBtn = document.getElementById("scale-btn-all");
      if (allBtn) allBtn.classList.toggle("active-scale", scaleIdx === -1);
      EJ5_SCALES.forEach(sc => {{
        const btn = document.getElementById(`scale-btn-${{sc.id}}`);
        if (btn) btn.classList.toggle("active-scale", sc.id === scaleIdx);
        const row = document.getElementById(`scale-row-${{sc.id}}`);
        if (row) row.classList.toggle("selected-row", sc.id === scaleIdx);
      }});
      const badge = document.getElementById("measure-badge");
      if (scaleIdx >= 0) {{
        badge.textContent = `Escala: ${{EJ5_SCALES[scaleIdx].shortEs}} (5 c.)`;
      }} else {{
        badge.textContent = `Escalas: Todas A–L (60 c.)`;
      }}
      if (isPlaying) {{
        stopPlayback();
        startPlayback();
      }}
      renderAll();
    }}

    function updateTempo(val) {{
      currentTempo = parseInt(val, 10) || 88;
      document.getElementById("tempo-label").textContent = `${{currentTempo}} BPM`;
      document.getElementById("abc-source-box").value = buildFullAbcText(currentArtId);
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

    function isNoteStaccato(artId, posInMeasure) {{
      const pos6 = posInMeasure % 6;
      const pos3 = posInMeasure % 6;
      switch (artId) {{
        case 3:  return pos6 === 4 || pos6 === 5;
        case 4:  return pos6 === 0 || pos6 === 1;
        case 5:  return pos6 >= 2;
        case 7:  return pos3 >= 3;
        case 9:  return posInMeasure === 0 || posInMeasure === 11;
        case 10: return true;
        default: return false;
      }}
    }}

    function startPlayback() {{
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

      // 6 notes per beat (quarter/dotted-quarter beat at currentTempo)
      const noteDur = (60 / currentTempo) / 6;
      const scalesToPlay = currentScaleIdx >= 0 ? [EJ5_SCALES[currentScaleIdx]] : EJ5_SCALES;
      let cursor = audioCtx.currentTime + 0.06;

      scalesToPlay.forEach((sc) => {{
        // 48 sixteenth notes (4 measures of 12) + 1 final quarter note + rest
        for (let i = 0; i < 48; i++) {{
          const mNum = Math.floor(i / 12) + 1;
          const posInM = i % 12;
          const midi = sc.midis[i];
          const stacc = isNoteStaccato(currentArtId, posInM);
          playPianoNote(midi, cursor, noteDur, stacc);

          if (posInM === 0) {{
            const delayMs = Math.max(0, (cursor - audioCtx.currentTime) * 1000);
            const tid = setTimeout(() => {{
              if (!isPlaying) return;
              document.getElementById("measure-badge").textContent = `Escala ${{sc.letter}} · Compás ${{mNum}}/5`;
              EJ5_SCALES.forEach(s => {{
                const r = document.getElementById(`scale-row-${{s.id}}`);
                if (r) r.classList.toggle("selected-row", s.id === sc.id);
              }});
            }}, delayMs);
            playTimeouts.push(tid);
          }}
          cursor += noteDur;
        }}
        // Measure 5: final tonic + rest
        const finalMidi = sc.midis[48];
        playPianoNote(finalMidi, cursor, noteDur * 6, false);
        const delayMs5 = Math.max(0, (cursor - audioCtx.currentTime) * 1000);
        const tid5 = setTimeout(() => {{
          if (!isPlaying) return;
          document.getElementById("measure-badge").textContent = `Escala ${{sc.letter}} · Compás 5/5 (Tónica)`;
        }}, delayMs5);
        playTimeouts.push(tid5);
        cursor += noteDur * 12;
      }});

      const totalMs = Math.max(0, (cursor - audioCtx.currentTime) * 1000);
      const endTid = setTimeout(() => {{
        stopPlayback();
      }}, totalMs);
      playTimeouts.push(endTid);
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
      initSelectors();
      renderAll();
    }});
  </script>
</body>
</html>
"""

for target in [
    os.path.join(BRAIN_DIR, "taffanel_ej5_validacion.html"),
    os.path.join(ROOT_DIR, "taffanel_ej5_validacion.html"),
    os.path.join(DOCS_DIR, "ej5.html"),
]:
    with open(target, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)

print("✅ Saved taffanel_ej5_validacion.html and docs/ej5.html")
