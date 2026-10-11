#!/usr/bin/env python3
"""
Generador Urtext completo de E. J. 4 — Taffanel & Gaubert (A. L. 16.588, págs. 111–114)
194 compases (24 secciones de 8 compases: 12 Mayores + 12 Menores Relativas + 2 compases finales en Do Mayor)
+ 8 Articulaciones oficiales + Visor HTML interactivo con reproductor Web Audio.
"""

import json
import os
import shutil

ARTIFACT_DIR = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"
WORKSPACE_DIR = "/Users/sebas/Desktop/partituras"

LETTERS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

KEY_SIGS = {
    'C':  {},
    'F':  {'B': -1},
    'Bb': {'B': -1, 'E': -1},
    'Eb': {'B': -1, 'E': -1, 'A': -1},
    'Ab': {'B': -1, 'E': -1, 'A': -1, 'D': -1},
    'Db': {'B': -1, 'E': -1, 'A': -1, 'D': -1, 'G': -1},
    'Gb': {'B': -1, 'E': -1, 'A': -1, 'D': -1, 'G': -1, 'C': -1},
    'B':  {'F': 1, 'C': 1, 'G': 1, 'D': 1, 'A': 1},
    'E':  {'F': 1, 'C': 1, 'G': 1, 'D': 1},
    'A':  {'F': 1, 'C': 1, 'G': 1},
    'D':  {'F': 1, 'C': 1},
    'G':  {'F': 1},
}

# 24 sections in exact Urtext order (A. L. 16.588, pages 111–114)
SECTIONS = [
    ("1_C",    "1. Do Mayor (C Major)",           "",               "C",  "maj", 0),
    ("2_Am",   "2. La menor (Relatif Mineur)",    "RELATIF MINEUR", "C",  "min", 5),
    ("3_F",    "3. Fa Mayor (F Major)",           "",               "F",  "maj", 3),
    ("4_Dm",   "4. Re menor (Mineur)",            "MINEUR",         "F",  "min", 1),
    ("5_Bb",   "5. Si♭ Mayor (B♭ Major)",         "",               "Bb", "maj", 6),
    ("6_Gm",   "6. Sol menor (Mineur)",           "MINEUR",         "Bb", "min", 4),
    ("7_Eb",   "7. Mi♭ Mayor (E♭ Major)",         "",               "Eb", "maj", 2),
    ("8_Cm",   "8. Do menor (Mineur)",            "MINEUR",         "Eb", "min", 0),
    ("9_Ab",   "9. La♭ Mayor (A♭ Major)",         "",               "Ab", "maj", 5),
    ("10_Fm",  "10. Fa menor (Mineur)",           "MINEUR",         "Ab", "min", 3),
    ("11_Db",  "11. Re♭ Mayor (D♭ Major)",        "",               "Db", "maj", 1),
    ("12_Bbm", "12. Si♭ menor (Mineur)",          "MINEUR",         "Db", "min", 6),
    ("13_Gb",  "13. Sol♭ Mayor (G♭ Major)",       "",               "Gb", "maj", 4),
    ("14_Ebm", "14. Mi♭ menor (Mineur)",          "MINEUR",         "Gb", "min", 2),
    ("15_B",   "15. Si Mayor (B Major)",          "",               "B",  "maj", 6),
    ("16_Gsm", "16. Sol♯ menor (Mineur)",         "MINEUR",         "B",  "min", 4),
    ("17_E",   "17. Mi Mayor (E Major)",          "",               "E",  "maj", 2),
    ("18_Csm", "18. Do♯ menor (Mineur)",          "MINEUR",         "E",  "min", 0),
    ("19_A",   "19. La Mayor (A Major)",          "",               "A",  "maj", 5),
    ("20_Fsm", "20. Fa♯ menor (Mineur)",          "MINEUR",         "A",  "min", 3),
    ("21_D",   "21. Re Mayor (D Major)",          "",               "D",  "maj", 1),
    ("22_Bm",  "22. Si menor (Mineur)",           "MINEUR",         "D",  "min", 6),
    ("23_G",   "23. Sol Mayor (G Major)",         "",               "G",  "maj", 4),
    ("24_Em",  "24. Mi menor (Mineur)",           "MINEUR",         "G",  "min", 2),
]

def acc_to_abc(acc_val):
    if acc_val == -2: return "__"
    if acc_val == -1: return "_"
    if acc_val == 0:  return "="
    if acc_val == 1:  return "^"
    if acc_val == 2:  return "^^"
    raise ValueError(f"Invalid accidental {acc_val}")

def diatonic_to_abc_pitch(diatonic_idx):
    letter = LETTERS[diatonic_idx % 7]
    octave = 4 + (diatonic_idx // 7)
    if octave == 3:
        return letter + ","
    elif octave == 4:
        return letter
    elif octave == 5:
        return letter.lower()
    elif octave >= 6:
        return letter.lower() + ("'" * (octave - 5))
    raise ValueError(f"Unsupported octave {octave}")

def build_measure_notes(key_sig, tonic_idx, deg_offsets, alterations):
    ks = KEY_SIGS[key_sig]
    notes = []
    active_acc = {}
    for pos, deg in enumerate(deg_offsets):
        d_idx = tonic_idx + deg
        letter = LETTERS[d_idx % 7]
        base_acc = ks.get(letter, 0)
        pitch_str = diatonic_to_abc_pitch(d_idx)

        if pos in alterations:
            kind = alterations[pos]
            if isinstance(kind, tuple) and kind[0] == "ABS":
                d_over, acc_val = kind[1], kind[2]
                p_over = diatonic_to_abc_pitch(d_over)
                notes.append(acc_to_abc(acc_val) + p_over)
                active_acc[d_over] = acc_val
                continue
            target_acc = base_acc + kind
            acc_prefix = acc_to_abc(target_acc)
            active_acc[d_idx] = target_acc
            notes.append(acc_prefix + pitch_str)
        else:
            cur_acc = active_acc.get(d_idx, base_acc)
            if cur_acc != base_acc:
                acc_prefix = acc_to_abc(base_acc)
                active_acc[d_idx] = base_acc
                notes.append(acc_prefix + pitch_str)
            else:
                notes.append(pitch_str)
    return notes

def generate_section_measures(sec_idx, sec):
    sec_id, name_es, label_fr, key_sig, mode, t_idx = sec

    m1_deg = [0,1,2,3, 4,5,6,7, 8,7,6,5, 4,3,2,1]
    m2_deg = [2,3,4,5, 6,7,8,9, 10,9,8,7, 6,5,4,3]
    m3_deg = [4,5,6,7, 8,9,10,11, 12,11,10,9, 8,7,6,5]
    m4_deg = [6,7,8,9, 10,11,12,13, 14,13,12,11, 10,9,8,7]
    m5_deg = [6,7,8,9, 10,11,12,13, 12,11,10,9, 8,7,6,5]
    m6_deg = [4,5,6,7, 8,9,10,11, 10,9,8,7, 6,5,4,3]
    m7_deg = [2,3,4,5, 6,7,8,9, 8,7,6,5, 4,3,2,1]

    measures = []

    if mode == "maj":
        for degs in [m1_deg, m2_deg, m3_deg, m4_deg, m5_deg, m6_deg, m7_deg]:
            measures.append(build_measure_notes(key_sig, t_idx, degs, {}))

        if t_idx in (0, 1):
            m8_deg = [0,1,2,3, 4,5,6,7, 6,5,4,3, 2,8,7,6]
        else:
            m8_deg = [0,1,2,3, 4,5,6,7, 6,5,4,3, 2,1,0,-1]
        m8_alt = {10: +1}
        if key_sig in ('C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'D', 'G'):
            m8_alt[11] = 0
        measures.append(build_measure_notes(key_sig, t_idx, m8_deg, m8_alt))

    else:
        measures.append(build_measure_notes(key_sig, t_idx, m1_deg, {5: +1, 6: +1, 10: +1, 11: 0}))
        measures.append(build_measure_notes(key_sig, t_idx, m2_deg, {3: +1, 4: +1, 12: 0, 13: 0}))
        measures.append(build_measure_notes(key_sig, t_idx, m3_deg, {1: +1, 2: +1, 8: 0, 14: +1, 15: +1}))
        measures.append(build_measure_notes(key_sig, t_idx, m4_deg, {0: +1, 6: +1, 7: +1, 9: 0, 10: 0}))
        measures.append(build_measure_notes(key_sig, t_idx, m5_deg, {0: +1, 6: 0, 7: 0, 14: 0}))
        measures.append(build_measure_notes(key_sig, t_idx, m6_deg, {1: +1, 2: +1, 12: 0, 13: 0}))
        measures.append(build_measure_notes(key_sig, t_idx, m7_deg, {3: +1, 4: +1, 10: +1, 11: 0}))

        if sec_id == "14_Ebm":
            m8_deg = [0,1,2,3, 4,5,6,7, 6,5,4,3, 2,8,7,6]
            m8_alt = {
                5: +1, 6: +1, 8: 0, 9: 0,
                13: ("ABS", 9, 0),   # =e5
                14: ("ABS", 8, +1),  # ^d5
                15: ("ABS", 7, +1),  # ^c5
            }
            measures.append(build_measure_notes(key_sig, t_idx, m8_deg, m8_alt))
        elif sec_id in ("4_Dm", "8_Cm", "18_Csm"):
            m8_deg = [0,1,2,3, 4,5,6,7, 6,5,4,3, 2,8,7,6]
            m8_alt = {5: +1, 6: +1, 8: 0, 9: 0, 13: -1}
            measures.append(build_measure_notes(key_sig, t_idx, m8_deg, m8_alt))
        else:
            m8_deg = [0,1,2,3, 4,5,6,7, 6,5,4,3, 2,1,0,-1]
            m8_alt = {5: +1, 6: +1, 8: 0, 9: 0, 13: -1}
            measures.append(build_measure_notes(key_sig, t_idx, m8_deg, m8_alt))

    return measures

def build_all_measures():
    all_measures = []
    m_num = 1
    for s_idx, sec in enumerate(SECTIONS):
        sec_id, name_es, label_fr, key_sig, mode, t_idx = sec
        sec_measures = generate_section_measures(s_idx, sec)
        for local_idx, m_notes in enumerate(sec_measures):
            all_measures.append({
                "measure_num": m_num,
                "section_id": sec_id,
                "section_name": name_es,
                "label_fr": label_fr if local_idx == 0 else "",
                "key_sig": key_sig,
                "key_change": (local_idx == 0 and mode == "maj" and s_idx > 0),
                "double_bar_before": (local_idx == 0 and s_idx > 0),
                "notes": m_notes,
                "is_coda": False,
                "is_final": False,
            })
            m_num += 1

    # Measures 193 & 194: Coda in Do Mayor (C Major)
    m193_notes = [diatonic_to_abc_pitch(i) for i in [0,1,2,3, 4,5,6,7, 8,9,10,11, 12,13,14,13]]
    all_measures.append({
        "measure_num": 193,
        "section_id": "25_C_Coda",
        "section_name": "25. Do Mayor (Coda Final)",
        "label_fr": "",
        "key_sig": "C",
        "key_change": True,
        "double_bar_before": True,
        "notes": m193_notes,
        "is_coda": True,
        "is_final": False,
    })
    m194_notes = [diatonic_to_abc_pitch(i) for i in [12,11,10,9, 8,7,6,5, 4,3,2,1]] + ["C2z2"]
    all_measures.append({
        "measure_num": 194,
        "section_id": "25_C_Coda",
        "section_name": "25. Do Mayor (Coda Final)",
        "label_fr": "",
        "key_sig": "C",
        "key_change": False,
        "double_bar_before": False,
        "notes": m194_notes,
        "is_coda": True,
        "is_final": True,
    })
    return all_measures

def apply_articulation_to_8(notes_8, art_id):
    n = list(notes_8)
    if art_id == 0:
        return "".join(n[0:4]) + " " + "".join(n[4:8])
    elif art_id == 1:
        return f"({n[0]}{n[1]}{n[2]}{n[3]} {n[4]}{n[5]}{n[6]}{n[7]})"
    elif art_id == 2:
        return f"({n[0]}{n[1]}{n[2]}{n[3]}) ({n[4]}{n[5]}{n[6]}{n[7]})"
    elif art_id == 3:
        return f".{n[0]}({n[1]}{n[2]}{n[3]}) .{n[4]}({n[5]}{n[6]}{n[7]})"
    elif art_id == 4:
        return f"({n[0]}{n[1]}).{n[2]}.{n[3]} ({n[4]}{n[5]}).{n[6]}.{n[7]}"
    elif art_id == 5:
        return f".{n[0]}.{n[1]}({n[2]}{n[3]}) .{n[4]}.{n[5]}({n[6]}{n[7]})"
    elif art_id == 6:
        return f".{n[0]}({n[1]}{n[2]}).{n[3]} .{n[4]}({n[5]}{n[6]}).{n[7]}"
    elif art_id == 7:
        return f"({n[0]}{n[1]})({n[2]}{n[3]}) ({n[4]}{n[5]})({n[6]}{n[7]})"
    elif art_id == 8:
        return f".{n[0]}({n[1]}{n[2]})({n[3]}{n[4]})({n[5]}{n[6]}).{n[7]}"
    return "".join(n[0:4]) + " " + "".join(n[4:8])

def format_measure_abc(m, art_id=0):
    prefix = ""
    if m.get("label_fr"):
        prefix += f'"^{m["label_fr"]}"'
    notes = m["notes"]
    if m.get("is_final"):
        half1 = apply_articulation_to_8(notes[0:8], art_id)
        if art_id == 0:
            half2 = "".join(notes[8:12]) + " " + notes[12]
        else:
            n4 = notes[8:12]
            c_end = notes[12]
            if art_id in (1, 2):
                half2 = f"({n4[0]}{n4[1]}{n4[2]}{n4[3]} {c_end})"
            elif art_id == 3:
                half2 = f".{n4[0]}({n4[1]}{n4[2]}{n4[3]}) .{c_end}"
            elif art_id == 4:
                half2 = f"({n4[0]}{n4[1]}).{n4[2]}.{n4[3]} .{c_end}"
            elif art_id == 5:
                half2 = f".{n4[0]}.{n4[1]}({n4[2]}{n4[3]}) .{c_end}"
            elif art_id == 6:
                half2 = f".{n4[0]}({n4[1]}{n4[2]}).{n4[3]} .{c_end}"
            elif art_id == 7:
                half2 = f"({n4[0]}{n4[1]})({n4[2]}{n4[3]}) .{c_end}"
            elif art_id == 8:
                half2 = f".{n4[0]}({n4[1]}{n4[2]})({n4[3]} {c_end})"
        return prefix + f"{half1} {half2}"
    else:
        half1 = apply_articulation_to_8(notes[0:8], art_id)
        half2 = apply_articulation_to_8(notes[8:16], art_id)
        return prefix + f"{half1} {half2}"

def build_page_abc(all_measures, page_num, art_id=0):
    if page_num == 1:
        slice_m = all_measures[0:45]
        init_key = "C"
    elif page_num == 2:
        slice_m = all_measures[45:96]
        init_key = "Bb"
    elif page_num == 3:
        slice_m = all_measures[96:146]
        init_key = "Gb"
    elif page_num == 4:
        slice_m = all_measures[146:194]
        init_key = "A"

    lines = [
        f"X:{page_num}",
        "M:4/2",
        "L:1/8",
        f"K:{init_key}",
    ]

    idx = 0
    while idx < len(slice_m):
        if page_num == 3 and idx == 15:
            row_measures = slice_m[idx:idx+2]
            idx += 2
        else:
            row_measures = slice_m[idx:idx+3]
            idx += 3

        # If the first measure of this row has a key change (and wasn't already switched), emit K: line
        if row_measures[0]["key_change"] and row_measures[0]["measure_num"] not in (1, 97):
            lines.append(f"K:{row_measures[0]['key_sig']}")

        row_str_parts = []
        for pos_in_row, m in enumerate(row_measures):
            bar_prefix = ""
            if pos_in_row > 0 and m["double_bar_before"]:
                if m["key_change"]:
                    bar_prefix = f"|| [K:{m['key_sig']}] "
                else:
                    bar_prefix = "|| "
            m_body = format_measure_abc(m, art_id)
            if m.get("is_final"):
                row_str_parts.append(f"{bar_prefix}{m_body} |]")
            else:
                next_global_idx = m["measure_num"]
                if next_global_idx < len(all_measures) and all_measures[next_global_idx]["double_bar_before"]:
                    if pos_in_row == len(row_measures) - 1:
                        row_str_parts.append(f"{bar_prefix}{m_body} ||")
                    else:
                        row_str_parts.append(f"{bar_prefix}{m_body} ")
                else:
                    row_str_parts.append(f"{bar_prefix}{m_body} |")

        lines.append(" ".join(row_str_parts))

    return "\n".join(lines)

def build_articulation_strip_abc():
    return """X:99
M:2/4
L:1/16
K:C
"^1" (CDEFGABc) || "^2" (CDEF)(GABc) || "^3" .C(DEF) .G(ABc) || "^4" (CD).E.F (GA).B.c || "^5" .C.D(EF) .G.A(Bc) || "^6" .C(DE).F .G(AB).c || "^7" (CD)(EF)(GA)(Bc) || "^8" .C(DE)(FG)(AB).c ||"""

def build_full_single_abc(all_measures, art_id=0):
    header = [
        "%!abctab2ps",
        "X:1",
        "T:E. J. 4 — Grands Exercices Journaliers de Mécanisme (Urtext)",
        "C:Paul Taffanel & Philippe Gaubert (Alphonse Leduc A. L. 16.588, págs. 111–114)",
        "M:4/2",
        "L:1/8",
        "Q:1/4=116",
        "K:C",
    ]
    body = []
    for p in (1, 2, 3, 4):
        p_abc = build_page_abc(all_measures, p, art_id)
        for line in p_abc.splitlines():
            if line.startswith(("X:", "M:", "L:", "%%")):
                continue
            if line == "K:C" and not body:
                continue
            body.append(line)
    return "\n".join(header + body)

def generate_html(all_measures):
    # Precompute the 4 page ABC strings AND the full continuous playback ABC string for each of the 9 articulation modes (0..8)
    pages_by_art = {}
    full_abc_by_art = {}
    for art_id in range(9):
        pages_by_art[art_id] = [
            build_page_abc(all_measures, 1, art_id),
            build_page_abc(all_measures, 2, art_id),
            build_page_abc(all_measures, 3, art_id),
            build_page_abc(all_measures, 4, art_id),
        ]
        full_abc_by_art[art_id] = build_full_single_abc(all_measures, art_id)

    art_strip_abc = build_articulation_strip_abc()

    # Build section jump list: (section_id, section_name, start_measure_1_indexed, page_num)
    section_jumps = []
    seen_sec = set()
    for m in all_measures:
        sid = m["section_id"]
        if sid not in seen_sec:
            seen_sec.add(sid)
            mnum = m["measure_num"]
            if mnum <= 45: pnum = 1
            elif mnum <= 96: pnum = 2
            elif mnum <= 146: pnum = 3
            else: pnum = 4
            section_jumps.append({
                "id": sid,
                "name": m["section_name"],
                "startMeasure": mnum,
                "page": pnum,
            })

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Taffanel & Gaubert — E. J. 4 (A. L. 16.588) — Validación Urtext & Reproductor</title>
<script src="https://cdn.jsdelivr.net/npm/abcjs@6.2.2/dist/abcjs-basic-min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap');

  :root {{
    --paper-bg: #fdfaf3;
    --ink: #181614;
    --accent: #b45309;
    --accent-light: rgba(245, 158, 11, 0.22);
    --bar-bg: rgba(20, 18, 16, 0.94);
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: #23201d;
    color: var(--ink);
    font-family: 'EB Garamond', Georgia, serif;
    padding-top: 74px;
    padding-bottom: 60px;
  }}

  /* Top sticky interactive player dock */
  .player-dock {{
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 1000;
    background: var(--bar-bg);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255,255,255,0.12);
    padding: 10px 18px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #f5f2eb;
    box-shadow: 0 6px 24px rgba(0,0,0,0.45);
  }}

  .dock-left, .dock-center, .dock-right {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }}

  .brand-badge {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.03em;
    color: #fbbf24;
    margin-right: 6px;
    text-decoration: none;
  }}

  .btn {{
    background: #302c27;
    color: #f3efe6;
    border: 1px solid rgba(255,255,255,0.16);
    padding: 6px 12px;
    border-radius: 7px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    transition: all 0.15s ease;
  }}
  .btn:hover {{ background: #3f3a34; border-color: rgba(255,255,255,0.28); }}
  .btn-primary {{
    background: linear-gradient(135deg, #d97706, #b45309);
    border-color: #f59e0b;
    color: #fff;
  }}
  .btn-primary:hover {{ background: linear-gradient(135deg, #f59e0b, #d97706); }}
  .btn-primary.playing {{
    background: linear-gradient(135deg, #059669, #047857);
    border-color: #34d399;
  }}

  select.dock-select {{
    background: #27231f;
    color: #f5f2eb;
    border: 1px solid rgba(255,255,255,0.18);
    padding: 6px 10px;
    border-radius: 7px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    max-width: 220px;
  }}

  .tempo-box {{
    display: flex;
    align-items: center;
    gap: 6px;
    background: #27231f;
    padding: 4px 10px;
    border-radius: 7px;
    border: 1px solid rgba(255,255,255,0.12);
    font-size: 12px;
  }}
  .tempo-box input[type=range] {{
    width: 75px;
    accent-color: #f59e0b;
    cursor: pointer;
  }}

  .status-pill {{
    background: rgba(251, 191, 36, 0.12);
    border: 1px solid rgba(251, 191, 36, 0.35);
    color: #fde68a;
    font-size: 11.5px;
    font-weight: 600;
    padding: 5px 10px;
    border-radius: 999px;
    white-space: nowrap;
  }}

  /* Score Pages */
  .pages-wrapper {{
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 14px;
    display: flex;
    flex-direction: column;
    gap: 28px;
  }}

  .leduc-page {{
    background: var(--paper-bg);
    color: var(--ink);
    border-radius: 3px;
    box-shadow: 0 12px 42px rgba(0,0,0,0.55), inset 0 0 0 1px rgba(0,0,0,0.08);
    padding: 34px 38px 28px 38px;
    position: relative;
  }}

  .page-header-row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 4px;
  }}
  .page-num {{
    font-size: 19px;
    font-weight: 600;
    letter-spacing: 0.03em;
    color: #222;
  }}
  .ej-title {{
    font-size: 29px;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-left: 24px;
  }}
  .ej-subtitle {{
    font-size: 15.5px;
    font-style: italic;
    margin-left: 24px;
    margin-bottom: 6px;
    color: #2c2825;
  }}

  .art-strip-box {{
    margin-bottom: 6px;
    padding: 2px 0;
    border-bottom: 1px solid rgba(0,0,0,0.08);
  }}

  .score-canvas svg {{
    width: 100% !important;
    height: auto !important;
    display: block;
  }}

  /* Interactive measure hover & active highlight */
  .measure-hit-rect {{
    fill: transparent;
    cursor: pointer;
    transition: fill 0.12s ease;
  }}
  .measure-hit-rect:hover {{
    fill: rgba(217, 119, 6, 0.10);
  }}
  .measure-hit-rect.active-measure {{
    fill: rgba(245, 158, 11, 0.26) !important;
    stroke: #d97706;
    stroke-width: 1.5px;
    rx: 4px;
  }}

  .plate-footer {{
    text-align: center;
    font-size: 12px;
    letter-spacing: 0.14em;
    color: #3a3530;
    margin-top: 10px;
    font-weight: 600;
  }}

  /* Modal for ABC source */
  .modal-backdrop {{
    display: none;
    position: fixed;
    inset: 0;
    z-index: 2000;
    background: rgba(0,0,0,0.75);
    align-items: center;
    justify-content: center;
    padding: 24px;
  }}
  .modal-backdrop.open {{ display: flex; }}
  .modal-card {{
    background: #1e1b18;
    color: #f5f2eb;
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 12px;
    max-width: 880px;
    width: 100%;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    font-family: 'Inter', sans-serif;
    overflow: hidden;
  }}
  .modal-header {{
    padding: 14px 18px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .modal-body {{
    padding: 16px;
    overflow-y: auto;
  }}
  .modal-body textarea {{
    width: 100%;
    height: 55vh;
    background: #12100e;
    color: #fde68a;
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 12px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 12px;
    line-height: 1.45;
  }}

  @page {{ size: A4 portrait; margin: 0; }}
  @media print {{
    body {{ background: #fff !important; padding: 0 !important; margin: 0 !important; }}
    .player-dock, .modal-backdrop, .measure-hit-rect {{ display: none !important; }}
    .pages-wrapper {{ max-width: none !important; padding: 0 !important; gap: 0 !important; margin: 0 !important; }}
    .leduc-page {{
      width: 210mm !important;
      height: 297mm !important;
      min-height: 297mm !important;
      max-height: 297mm !important;
      box-sizing: border-box !important;
      box-shadow: none !important;
      padding: 6mm 8mm 5mm 8mm !important;
      margin: 0 !important;
      overflow: hidden !important;
      page-break-after: always;
      break-after: page;
      page-break-inside: avoid;
      break-inside: avoid;
      background: #fff !important;
    }}
    .leduc-page:last-child {{
      page-break-after: auto;
      break-after: auto;
    }}
    .page-header-row {{ margin-bottom: 1px !important; }}
    .page-num {{ font-size: 15px !important; }}
    .ej-title {{ font-size: 21px !important; margin-bottom: 0 !important; }}
    .ej-subtitle {{ font-size: 12px !important; margin-bottom: 2px !important; }}
    .art-strip-box, .score-canvas {{
      padding: 0 !important;
      height: auto !important;
      position: static !important;
      margin-bottom: 2px !important;
    }}
    .art-strip-box svg {{
      position: static !important;
      width: 100% !important;
      max-height: 17mm !important;
      height: auto !important;
    }}
    #page-1 #canvas-p1 svg {{
      position: static !important;
      width: auto !important;
      max-width: 100% !important;
      height: 246mm !important;
      max-height: 246mm !important;
      margin: 0 auto !important;
    }}
    #page-2 #canvas-p2 svg,
    #page-3 #canvas-p3 svg,
    #page-4 #canvas-p4 svg {{
      position: static !important;
      width: auto !important;
      max-width: 100% !important;
      height: 268mm !important;
      max-height: 268mm !important;
      margin: 0 auto !important;
    }}
    .plate-footer {{ margin-top: 2px !important; font-size: 10px !important; }}
  }}
</style>
</head>
<body>

<div class="player-dock">
  <div class="dock-left">
    <a href="index.html" class="brand-badge" title="Volver al Portal">🪈 E. J. 4 · A. L. 16.588</a>
    <button id="btnPlay" class="btn btn-primary" onclick="togglePlay()">▶ Reproducir</button>
    <button id="btnStop" class="btn" onclick="stopPlayback()">⏹ Detener</button>
    <span id="statusPill" class="status-pill">Compás 1 / 194 · Do Mayor</span>
  </div>

  <div class="dock-center">
    <label style="font-size:11px;color:#cbd5e1;">Tonalidad:</label>
    <select id="selectSection" class="dock-select" onchange="onSectionSelect(this.value)">
    </select>

    <label style="font-size:11px;color:#cbd5e1;">Articulación:</label>
    <select id="selectArt" class="dock-select" onchange="onArticulationChange(parseInt(this.value,10))">
      <option value="0">0. Original (Como está escrito)</option>
      <option value="1">1. Ligado de 8 — (CDEFGABc)</option>
      <option value="2">2. Ligado 4 + 4 — (CDEF)(GABc)</option>
      <option value="3">3. 1 picado + 3 ligados — .C(DEF) .G(ABc)</option>
      <option value="4">4. 2 ligados + 2 picados — (CD).E.F (GA).B.c</option>
      <option value="5">5. 2 picados + 2 ligados — .C.D(EF) .G.A(Bc)</option>
      <option value="6">6. Sincopado de 4 — .C(DE).F .G(AB).c</option>
      <option value="7">7. Ligado de 2 en 2 — (CD)(EF)(GA)(Bc)</option>
      <option value="8">8. Sincopado de 8 — .C(DE)(FG)(AB).c</option>
    </select>

    <label style="font-size:11px;color:#cbd5e1;">Sonido:</label>
    <select id="selectInst" class="dock-select" style="max-width:140px;" onchange="onInstrumentChange(parseInt(this.value,10))">
      <option value="0">🎹 Piano (Steinway)</option>
      <option value="73">🪈 Flauta (Sustain)</option>
    </select>

    <div class="tempo-box">
      <span>♩=</span>
      <input id="tempoSlider" type="range" min="48" max="176" value="116" oninput="onTempoInput(this.value)">
      <strong id="tempoVal">116</strong>
    </div>
  </div>

  <div class="dock-right">
    <button class="btn" onclick="openAbcModal()">📄 Código ABC</button>
    <button class="btn" onclick="window.print()">🖨️ Imprimir / PDF</button>
  </div>
</div>

<div class="pages-wrapper">
  <!-- PAGE 111 -->
  <section class="leduc-page" id="page-1">
    <div class="page-header-row">
      <div>
        <div class="ej-title">E. J. 4</div>
        <div class="ej-subtitle">A travailler successivement avec chacune des articulations suivantes:</div>
      </div>
      <div class="page-num">111</div>
    </div>
    <div id="art-strip-canvas" class="art-strip-box score-canvas"></div>
    <div id="canvas-p1" class="score-canvas"></div>
    <div class="plate-footer">A. L. 16.588</div>
  </section>

  <!-- PAGE 112 -->
  <section class="leduc-page" id="page-2">
    <div class="page-header-row">
      <div class="page-num">112</div>
      <div style="font-size:13px;font-style:italic;color:#555;">E. J. 4 (suite)</div>
    </div>
    <div id="canvas-p2" class="score-canvas"></div>
    <div class="plate-footer">A. L. 16.588</div>
  </section>

  <!-- PAGE 113 -->
  <section class="leduc-page" id="page-3">
    <div class="page-header-row">
      <div style="font-size:13px;font-style:italic;color:#555;">E. J. 4 (suite)</div>
      <div class="page-num">113</div>
    </div>
    <div id="canvas-p3" class="score-canvas"></div>
    <div class="plate-footer">A. L. 16.588</div>
  </section>

  <!-- PAGE 114 -->
  <section class="leduc-page" id="page-4">
    <div class="page-header-row">
      <div class="page-num">114</div>
      <div style="font-size:13px;font-style:italic;color:#555;">E. J. 4 (fin)</div>
    </div>
    <div id="canvas-p4" class="score-canvas"></div>
    <div class="plate-footer">A. L. 16.588</div>
  </section>
</div>

<!-- Hidden container for continuous audio synth -->
<div id="hidden-synth-paper" style="display:none;"></div>

<!-- Modal ABC -->
<div id="abcModal" class="modal-backdrop" onclick="if(event.target===this)closeAbcModal()">
  <div class="modal-card">
    <div class="modal-header">
      <strong>Código ABC Urtext Completo — E. J. 4 (194 compases)</strong>
      <div style="display:flex;gap:8px;">
        <button class="btn btn-primary" onclick="copyAbcCode()">📋 Copiar ABC</button>
        <button class="btn" onclick="closeAbcModal()">✕ Cerrar</button>
      </div>
    </div>
    <div class="modal-body">
      <textarea id="abcTextarea" readonly></textarea>
    </div>
  </div>
</div>

<script>
const PAGES_BY_ART = {json.dumps(pages_by_art, ensure_ascii=False)};
const FULL_ABC_BY_ART = {json.dumps(full_abc_by_art, ensure_ascii=False)};
const ART_STRIP_ABC = {json.dumps(art_strip_abc, ensure_ascii=False)};
const SECTION_JUMPS = {json.dumps(section_jumps, ensure_ascii=False)};
const MEASURE_META = {json.dumps([
    {"m": m["measure_num"], "secId": m["section_id"], "secName": m["section_name"]}
    for m in all_measures
], ensure_ascii=False)};

const PAGE_MEASURE_RANGES = [
  {{ page: 1, start: 1,   end: 45  }},
  {{ page: 2, start: 46,  end: 96  }},
  {{ page: 3, start: 97,  end: 146 }},
  {{ page: 4, start: 147, end: 194 }}
];

let currentArt = 0;
let currentProgram = 0;
let currentBpm = 116;
let currentMeasure = 1;
let isPlaying = false;
let midiBuffer = null;
let audioCtx = null;
let playbackTimer = null;
let playbackStartTime = 0;
let playbackStartOffsetSec = 0;
let measureHitRects = {{}}; // measure_num (1..194) -> SVGRectElement

function initSectionSelector() {{
  const sel = document.getElementById('selectSection');
  sel.innerHTML = '';
  SECTION_JUMPS.forEach(s => {{
    const opt = document.createElement('option');
    opt.value = s.startMeasure;
    opt.textContent = `${{s.name}} (c. ${{s.startMeasure}})`;
    sel.appendChild(opt);
  }});
}}

function normalizeAbcSvg(targetId) {{
  const c = document.getElementById(targetId);
  if (!c) return;
  c.style.paddingBottom = '';
  c.style.position = '';
  c.style.height = '';
  c.querySelectorAll('div').forEach(d => {{
    d.style.paddingBottom = '';
    d.style.position = '';
    d.style.height = '';
  }});
  const s = c.querySelector('svg');
  if (s) {{
    s.style.position = 'static';
    s.style.top = '';
    s.style.left = '';
  }}
}}

function renderAllPages() {{
  // Render top articulation strip
  ABCJS.renderAbc("art-strip-canvas", ART_STRIP_ABC, {{
    responsive: "resize",
    staffwidth: 1000,
    paddingtop: 2,
    paddingbottom: 4,
    paddingleft: 8,
    paddingright: 8,
    scale: 0.86,
    add_classes: true
  }});
  normalizeAbcSvg("art-strip-canvas");

  measureHitRects = {{}};
  const pages = PAGES_BY_ART[currentArt];
  for (let p = 1; p <= 4; p++) {{
    const targetId = `canvas-p${{p}}`;
    ABCJS.renderAbc(targetId, pages[p - 1], {{
      responsive: "resize",
      staffwidth: 1020,
      paddingtop: 4,
      paddingbottom: 4,
      paddingleft: 8,
      paddingright: 8,
      scale: 0.90,
      add_classes: true
    }});
    normalizeAbcSvg(targetId);
    buildMeasureHitBoxesForPage(p, document.getElementById(targetId));
  }}

  document.getElementById('abcTextarea').value = FULL_ABC_BY_ART[currentArt];
  highlightMeasure(currentMeasure, false);
}}

function buildMeasureHitBoxesForPage(pageNum, container) {{
  const svg = container.querySelector('svg');
  if (!svg) return;

  // Nudge section labels ("RELATIF MINEUR", "MINEUR", "MAJEUR") slightly closer to their own staff
  svg.querySelectorAll('text.abcjs-annotation').forEach(t => {{
    const curY = parseFloat(t.getAttribute('y') || '0');
    if (!isNaN(curY)) {{
      t.setAttribute('y', (curY + 11).toFixed(1));
    }}
  }});

  // Group noteheads/rests by system line (m0, m1, m2...) using abcjs classes or barlines
  // Better yet: find all staff systems via .abcjs-staff or barlines, and split each line into its known measures!
  const range = PAGE_MEASURE_RANGES[pageNum - 1];
  // Expected measures per line on this page:
  const lineMeasureCounts = [];
  let rem = range.end - range.start + 1;
  let lineIdx = 0;
  while (rem > 0) {{
    const cnt = (pageNum === 3 && lineIdx === 5) ? 2 : Math.min(3, rem);
    lineMeasureCounts.push(cnt);
    rem -= cnt;
    lineIdx++;
  }}

  // Find vertical staff bands by clustering .abcjs-bar or .abcjs-note elements by Y
  const notesAndBars = Array.from(svg.querySelectorAll('.abcjs-note, .abcjs-rest, .abcjs-bar'));
  if (!notesAndBars.length) return;

  // Find the 5-line staves via path elements with class .abcjs-staff
  const staffEls = Array.from(svg.querySelectorAll('.abcjs-staff'));
  const lineBoxes = [];
  if (staffEls.length === lineMeasureCounts.length) {{
    staffEls.forEach(el => {{
      const b = el.getBBox();
      lineBoxes.push({{ y: b.y - 16, height: b.height + 32, xMin: b.x, xMax: b.x + b.width }});
    }});
  }} else {{
    // Fallback: divide SVG height evenly into lineMeasureCounts.length rows
    const vb = svg.viewBox.baseVal;
    const rowH = vb.height / lineMeasureCounts.length;
    for (let i = 0; i < lineMeasureCounts.length; i++) {{
      lineBoxes.push({{ y: i * rowH + 6, height: rowH - 12, xMin: 20, xMax: vb.width - 20 }});
    }}
  }}

  let mCursor = range.start;
  lineBoxes.forEach((lb, rIdx) => {{
    const cols = lineMeasureCounts[rIdx];
    const startX = lb.xMin + 55; // skip clef + key sig
    const usableW = Math.max(100, lb.xMax - startX);
    const colW = usableW / cols;
    for (let c = 0; c < cols; c++) {{
      const mNum = mCursor++;
      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", (startX + c * colW).toFixed(1));
      rect.setAttribute("y", lb.y.toFixed(1));
      rect.setAttribute("width", colW.toFixed(1));
      rect.setAttribute("height", lb.height.toFixed(1));
      rect.setAttribute("class", "measure-hit-rect");
      rect.setAttribute("data-measure", mNum);
      rect.innerHTML = `<title>Compás ${{mNum}} — Click para reproducir desde aquí</title>`;
      rect.addEventListener("click", (ev) => {{
        ev.stopPropagation();
        jumpAndPlayMeasure(mNum);
      }});
      svg.appendChild(rect);
      measureHitRects[mNum] = rect;
    }}
  }});
}}

function highlightMeasure(mNum, scrollIntoView = true) {{
  currentMeasure = Math.max(1, Math.min(194, mNum));
  Object.values(measureHitRects).forEach(r => r.classList.remove('active-measure'));
  const targetRect = measureHitRects[currentMeasure];
  if (targetRect) {{
    targetRect.classList.add('active-measure');
    if (scrollIntoView) {{
      const bbox = targetRect.getBoundingClientRect();
      if (bbox.top < 110 || bbox.bottom > window.innerHeight - 60) {{
        targetRect.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}
    }}
  }}
  const meta = MEASURE_META[currentMeasure - 1];
  if (meta) {{
    document.getElementById('statusPill').textContent = `Compás ${{currentMeasure}} / 194 · ${{meta.secName}}`;
    // Sync section dropdown
    const secObj = SECTION_JUMPS.slice().reverse().find(s => currentMeasure >= s.startMeasure);
    if (secObj) {{
      document.getElementById('selectSection').value = secObj.startMeasure;
    }}
  }}
}}

function getMeasureDurationSec() {{
  // M:4/2, L:1/8 => 16 eighth-notes per measure = 8 quarter-notes per measure!
  // At Q:1/4 = currentBpm, 1 quarter-note = 60 / currentBpm seconds.
  // So 1 measure (8 quarter-notes) = 8 * (60 / currentBpm) seconds.
  return (8.0 * 60.0) / currentBpm;
}}

async function startPlaybackFrom(measureNum) {{
  stopPlayback(false);
  currentMeasure = measureNum;
  highlightMeasure(currentMeasure, true);

  const btn = document.getElementById('btnPlay');
  btn.textContent = "⏳ Cargando...";

  try {{
    if (!audioCtx) {{
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContextClass();
    }}
    if (audioCtx.state === 'suspended') {{
      await audioCtx.resume();
    }}

    const visualObjs = ABCJS.renderAbc("hidden-synth-paper", FULL_ABC_BY_ART[currentArt], {{
      program: currentProgram
    }});

    midiBuffer = new ABCJS.synth.CreateSynth();
    const msPerMeasure = getMeasureDurationSec() * 1000;

    await midiBuffer.init({{
      visualObj: visualObjs[0],
      audioContext: audioCtx,
      millisecondsPerMeasure: msPerMeasure,
      options: {{
        program: currentProgram,
        soundFontUrl: "https://paulrosen.github.io/midi-js-soundfonts/FluidR3_GM/"
      }}
    }});

    await midiBuffer.prime();

    const totalMeasures = 194;
    const seekRatio = (currentMeasure - 1) / totalMeasures;
    midiBuffer.seek(seekRatio);
    midiBuffer.start();

    isPlaying = true;
    btn.textContent = "⏸ Pausar";
    btn.classList.add('playing');

    const measureSec = getMeasureDurationSec();
    playbackStartOffsetSec = (currentMeasure - 1) * measureSec;
    playbackStartTime = audioCtx.currentTime;

    playbackTimer = setInterval(() => {{
      if (!isPlaying) return;
      const elapsed = audioCtx.currentTime - playbackStartTime + playbackStartOffsetSec;
      const mNow = Math.floor(elapsed / getMeasureDurationSec()) + 1;
      if (mNow > 194) {{
        stopPlayback(true);
        return;
      }}
      if (mNow !== currentMeasure) {{
        highlightMeasure(mNow, true);
      }}
    }}, 80);

  }} catch (err) {{
    console.error("Audio playback error:", err);
    btn.textContent = "▶ Reproducir";
    btn.classList.remove('playing');
  }}
}}

function togglePlay() {{
  if (isPlaying) {{
    stopPlayback(false);
  }} else {{
    startPlaybackFrom(currentMeasure);
  }}
}}

function stopPlayback(resetToStart = false) {{
  if (playbackTimer) {{
    clearInterval(playbackTimer);
    playbackTimer = null;
  }}
  if (midiBuffer) {{
    try {{ midiBuffer.stop(); }} catch (e) {{}}
    midiBuffer = null;
  }}
  isPlaying = false;
  const btn = document.getElementById('btnPlay');
  btn.textContent = "▶ Reproducir";
  btn.classList.remove('playing');
  if (resetToStart) {{
    highlightMeasure(1, false);
  }}
}}

function jumpAndPlayMeasure(mNum) {{
  highlightMeasure(mNum, true);
  startPlaybackFrom(mNum);
}}

function onSectionSelect(startMeasureStr) {{
  const mNum = parseInt(startMeasureStr, 10) || 1;
  highlightMeasure(mNum, true);
  if (isPlaying) {{
    startPlaybackFrom(mNum);
  }}
}}

function onArticulationChange(artId) {{
  const wasPlaying = isPlaying;
  const savedMeasure = currentMeasure;
  if (wasPlaying) stopPlayback(false);
  currentArt = artId;
  renderAllPages();
  highlightMeasure(savedMeasure, false);
  if (wasPlaying) {{
    startPlaybackFrom(savedMeasure);
  }}
}}

function onInstrumentChange(prog) {{
  currentProgram = prog;
  if (isPlaying) {{
    startPlaybackFrom(currentMeasure);
  }}
}}

function onTempoInput(val) {{
  currentBpm = parseInt(val, 10) || 116;
  document.getElementById('tempoVal').textContent = currentBpm;
  if (isPlaying) {{
    startPlaybackFrom(currentMeasure);
  }}
}}

function openAbcModal() {{
  document.getElementById('abcModal').classList.add('open');
}}
function closeAbcModal() {{
  document.getElementById('abcModal').classList.remove('open');
}}
function copyAbcCode() {{
  const ta = document.getElementById('abcTextarea');
  ta.select();
  navigator.clipboard.writeText(ta.value);
}}

window.addEventListener('DOMContentLoaded', () => {{
  initSectionSelector();
  renderAllPages();
}});
</script>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    all_m = build_all_measures()
    full_abc = build_full_single_abc(all_m, 0)
    html_out = generate_html(all_m)

    # Save ABC to artifact and workspace
    abc_art_path = os.path.join(ARTIFACT_DIR, "taffanel_ej4_completo.abc")
    abc_ws_path = os.path.join(WORKSPACE_DIR, "taffanel_ej4_completo.abc")
    with open(abc_art_path, "w", encoding="utf-8") as f:
        f.write(full_abc)
    with open(abc_ws_path, "w", encoding="utf-8") as f:
        f.write(full_abc)

    # Save HTML to artifact, workspace, and docs/ej4.html
    html_art_path = os.path.join(ARTIFACT_DIR, "taffanel_ej4_validacion.html")
    html_ws_path = os.path.join(WORKSPACE_DIR, "taffanel_ej4_validacion.html")
    html_docs_path = os.path.join(WORKSPACE_DIR, "docs", "ej4.html")
    with open(html_art_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    with open(html_ws_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    if os.path.isdir(os.path.join(WORKSPACE_DIR, "docs")):
        with open(html_docs_path, "w", encoding="utf-8") as f:
            f.write(html_out)

    print("Successfully generated:")
    print(" -", abc_art_path)
    print(" -", html_art_path)
    print(" -", html_ws_path)
    print(" -", html_docs_path)
