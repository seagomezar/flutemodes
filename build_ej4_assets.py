#!/usr/bin/env python3
"""
Builds all E.J. 4 assets for Web, iOS, and Android:
1. Standalone .abc files in abc_ej4/, FluteModesAndroid/app/src/main/assets/abc_ej4/, and docs/downloads/abc/
2. Copies taffanel_ej4_transcripcion.pdf to workspace root and docs/downloads/pdf/
3. Updates score_template.html in both iOS and Android with EJ4_ALL_MEASURES and renderEj4Leduc(artId, secIdx)
4. Generates Swift and Kotlin snippets for ExerciseGenerator (MIDI notes + ABC lines per section)
"""

import json
import os
import re
import shutil
import generate_ej4_validation as ej4

WORKSPACE_DIR = "/Users/sebas/Desktop/partituras"
ARTIFACT_DIR = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"

ART_META = [
    (0, "00_Taffanel_EJ4_Original_AL16588.abc", "Original (Como está escrito — A. L. 16.588)"),
    (1, "01_Taffanel_EJ4_Articulacion_01_8_Ligadas.abc", "Articulación 1 — 8 ligadas: (CDEFGABc)"),
    (2, "02_Taffanel_EJ4_Articulacion_02_4_y_4_Ligadas.abc", "Articulación 2 — 4 y 4 ligadas: (CDEF)(GABc)"),
    (3, "03_Taffanel_EJ4_Articulacion_03_1_Picada_3_Ligadas.abc", "Articulación 3 — 1 picada y 3 ligadas: .C(DEF) .G(ABc)"),
    (4, "04_Taffanel_EJ4_Articulacion_04_2_Ligadas_2_Picadas.abc", "Articulación 4 — 2 ligadas y 2 picadas: (CD).E.F (GA).B.c"),
    (5, "05_Taffanel_EJ4_Articulacion_05_2_Picadas_2_Ligadas.abc", "Articulación 5 — 2 picadas y 2 ligadas: .C.D(EF) .G.A(Bc)"),
    (6, "06_Taffanel_EJ4_Articulacion_06_1_Picada_2_Ligadas_1_Picada.abc", "Articulación 6 — Sincopadas de 4: .C(DE).F .G(AB).c"),
    (7, "07_Taffanel_EJ4_Articulacion_07_De_2_en_2_Ligadas.abc", "Articulación 7 — De 2 en 2 ligadas: (CD)(EF)(GA)(Bc)"),
    (8, "08_Taffanel_EJ4_Articulacion_08_Sincopadas_de_8.abc", "Articulación 8 — Sincopadas de 8: .C(DE)(FG)(AB).c"),
]

SEMITONE_MAP = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

def abc_token_to_midi(token, key_sig_map, active_bar_acc):
    """
    Converts an ABC note token like '^g', '=f', 'C2z2', 'c'' to a MIDI integer,
    respecting key signature and active bar accidentals (per diatonic pitch + octave).
    """
    m = re.match(r'^(\^\^|\^|__|_|=)?([A-Ga-g])([,\']*).*$', token)
    if not m:
        raise ValueError(f"Cannot parse ABC token: {token}")
    acc_str, letter_raw, oct_mod = m.group(1), m.group(2), m.group(3)
    letter_up = letter_raw.upper()
    octave = 4 if letter_raw.isupper() else 5
    for ch in oct_mod:
        if ch == "'":
            octave += 1
        elif ch == ",":
            octave -= 1

    pitch_key = (letter_up, octave)
    base_acc = key_sig_map.get(letter_up, 0)
    if acc_str is not None:
        if acc_str == "^^": acc_val = 2
        elif acc_str == "^": acc_val = 1
        elif acc_str == "=": acc_val = 0
        elif acc_str == "_": acc_val = -1
        elif acc_str == "__": acc_val = -2
        active_bar_acc[pitch_key] = acc_val
    else:
        acc_val = active_bar_acc.get(pitch_key, base_acc)

    midi = (octave + 1) * 12 + SEMITONE_MAP[letter_up] + acc_val
    return midi

def build_abc_files(all_measures):
    abc_dir = os.path.join(WORKSPACE_DIR, "abc_ej4")
    android_abc_dir = os.path.join(WORKSPACE_DIR, "FluteModesAndroid/app/src/main/assets/abc_ej4")
    docs_abc_dir = os.path.join(WORKSPACE_DIR, "docs/downloads/abc")
    os.makedirs(abc_dir, exist_ok=True)
    os.makedirs(android_abc_dir, exist_ok=True)
    os.makedirs(docs_abc_dir, exist_ok=True)

    collection_parts = []
    for art_id, fname, desc in ART_META:
        raw_abc = ej4.build_full_single_abc(all_measures, art_id)
        # Customize X: and T: for standalone file
        lines = raw_abc.splitlines()
        out_lines = []
        for line in lines:
            if line.startswith("X:1"):
                out_lines.append(f"X:{art_id if art_id > 0 else 1}")
            elif line.startswith("T:"):
                out_lines.append(f"T:E. J. 4 — {desc}")
            else:
                out_lines.append(line)
        content = "\n".join(out_lines) + "\n"
        for target_dir in (abc_dir, android_abc_dir, docs_abc_dir):
            with open(os.path.join(target_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)
        if art_id > 0:
            collection_parts.append(content.replace("%!abctab2ps\n", ""))

    coll_name = "09_Coleccion_Completa_Taffanel_EJ4_8_Articulaciones.abc"
    coll_content = "%!abctab2ps\n% Colección Completa E. J. 4 (8 Articulaciones Oficiales — A. L. 16.588)\n\n" + "\n\n".join(collection_parts)
    for target_dir in (abc_dir, android_abc_dir, docs_abc_dir):
        with open(os.path.join(target_dir, coll_name), "w", encoding="utf-8") as f:
            f.write(coll_content)
    print(f"Generated 10 .abc files in {abc_dir}, {android_abc_dir}, and {docs_abc_dir}")

def copy_pdf_files():
    src_pdf = os.path.join(ARTIFACT_DIR, "taffanel_ej4_transcripcion.pdf")
    if os.path.exists(src_pdf):
        dst1 = os.path.join(WORKSPACE_DIR, "taffanel_ej4_transcripcion.pdf")
        dst2 = os.path.join(WORKSPACE_DIR, "docs/downloads/pdf/taffanel_ej4_transcripcion.pdf")
        os.makedirs(os.path.dirname(dst2), exist_ok=True)
        shutil.copyfile(src_pdf, dst1)
        shutil.copyfile(src_pdf, dst2)
        print(f"Copied PDF to {dst1} and {dst2}")

def build_compact_measures_for_js(all_measures):
    # Map section_id to 0..24 index
    sec_ids = []
    for m in all_measures:
        if m["section_id"] not in sec_ids:
            sec_ids.append(m["section_id"])
    sec_map = {sid: idx for idx, sid in enumerate(sec_ids)}

    compact = []
    for m in all_measures:
        compact.append({
            "num": m["measure_num"],
            "sec": sec_map[m["section_id"]],
            "secName": m["section_name"],
            "label": m["label_fr"],
            "key": m["key_sig"],
            "keyChg": m["key_change"],
            "dblBar": m["double_bar_before"],
            "notes": m["notes"],
            "final": m["is_final"]
        })
    return compact

def update_score_template(template_path, compact_measures, art_strip_abc):
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Remove any previous EJ4 block if re-running
    html = re.sub(r'// === BEGIN EJ4 LEDUC ===.*?// === END EJ4 LEDUC ===\n?', '', html, flags=re.DOTALL)

    ej4_js_block = f"""// === BEGIN EJ4 LEDUC ===
    const EJ4_ARTICULATIONS_ABC = {json.dumps(art_strip_abc, ensure_ascii=False)};
    const EJ4_ALL_MEASURES = {json.dumps(compact_measures, ensure_ascii=False)};
    const EJ4_ART_NAMES = {{
      0: "Original A. L. 16.588",
      1: "Art. 1 · 8 ligadas",
      2: "Art. 2 · 4 y 4 ligadas",
      3: "Art. 3 · 1 picada, 3 ligadas",
      4: "Art. 4 · 2 ligadas, 2 picadas",
      5: "Art. 5 · 2 picadas, 2 ligadas",
      6: "Art. 6 · 1 pic., 2 lig., 1 pic.",
      7: "Art. 7 · De 2 en 2 ligadas",
      8: "Art. 8 · Sincopadas de 8"
    }};

    function applyEj4Art8(n, artId) {{
      if (!n || n.length < 8) return (n || []).join("");
      switch (artId) {{
        case 0: return n.slice(0,4).join("") + " " + n.slice(4,8).join("");
        case 1: return `(${{n[0]}}${{n[1]}}${{n[2]}}${{n[3]}} ${{n[4]}}${{n[5]}}${{n[6]}}${{n[7]}})`;
        case 2: return `(${{n[0]}}${{n[1]}}${{n[2]}}${{n[3]}}) (${{n[4]}}${{n[5]}}${{n[6]}}${{n[7]}})`;
        case 3: return `.${{n[0]}}(${{n[1]}}${{n[2]}}${{n[3]}}) .${{n[4]}}(${{n[5]}}${{n[6]}}${{n[7]}})`;
        case 4: return `(${{n[0]}}${{n[1]}}).${{n[2]}}.${{n[3]}} (${{n[4]}}${{n[5]}}).${{n[6]}}.${{n[7]}}`;
        case 5: return `.${{n[0]}}.${{n[1]}}(${{n[2]}}${{n[3]}}) .${{n[4]}}.${{n[5]}}(${{n[6]}}${{n[7]}})`;
        case 6: return `.${{n[0]}}(${{n[1]}}${{n[2]}}).${{n[3]}} .${{n[4]}}(${{n[5]}}${{n[6]}}).${{n[7]}}`;
        case 7: return `(${{n[0]}}${{n[1]}})(${{n[2]}}${{n[3]}}) (${{n[4]}}${{n[5]}})(${{n[6]}}${{n[7]}})`;
        case 8: return `.${{n[0]}}(${{n[1]}}${{n[2]}})(${{n[3]}}${{n[4]}})(${{n[5]}}${{n[6]}}).${{n[7]}}`;
        default: return n.slice(0,4).join("") + " " + n.slice(4,8).join("");
      }}
    }}

    function formatEj4Measure(m, artId) {{
      const prefix = m.label ? `"^${{m.label}}"` : "";
      const notes = m.notes;
      if (m.final) {{
        const h1 = applyEj4Art8(notes.slice(0,8), artId);
        let h2 = "";
        const n4 = notes.slice(8,12);
        const cEnd = notes[12];
        if (artId === 0) h2 = n4.join("") + " " + cEnd;
        else if (artId === 1 || artId === 2) h2 = `(${{n4.join("")}} ${{cEnd}})`;
        else if (artId === 3) h2 = `.${{n4[0]}}(${{n4[1]}}${{n4[2]}}${{n4[3]}}) .${{cEnd}}`;
        else if (artId === 4) h2 = `(${{n4[0]}}${{n4[1]}}).${{n4[2]}}.${{n4[3]}} .${{cEnd}}`;
        else if (artId === 5) h2 = `.${{n4[0]}}.${{n4[1]}}(${{n4[2]}}${{n4[3]}}) .${{cEnd}}`;
        else if (artId === 6) h2 = `.${{n4[0]}}(${{n4[1]}}${{n4[2]}}).${{n4[3]}} .${{cEnd}}`;
        else if (artId === 7) h2 = `(${{n4[0]}}${{n4[1]}})(${{n4[2]}}${{n4[3]}}) .${{cEnd}}`;
        else if (artId === 8) h2 = `.${{n4[0]}}(${{n4[1]}}${{n4[2]}})(${{n4[3]}} ${{cEnd}})`;
        return prefix + h1 + " " + h2;
      }} else {{
        const h1 = applyEj4Art8(notes.slice(0,8), artId);
        const h2 = applyEj4Art8(notes.slice(8,16), artId);
        return prefix + h1 + " " + h2;
      }}
    }}

    function buildEj4SectionAbc(secIdx, artId) {{
      const secMeasures = EJ4_ALL_MEASURES.filter(m => m.sec === secIdx);
      if (!secMeasures.length) return "";
      const initKey = secMeasures[0].key;
      const lines = [
        "X:1",
        "M:4/2",
        "L:1/8",
        `K:${{initKey}}`
      ];
      for (let i = 0; i < secMeasures.length; i += 2) {{
        const row = secMeasures.slice(i, i + 2);
        const parts = row.map((m, idx) => {{
          const body = formatEj4Measure(m, artId);
          const isLastInSec = (i + idx === secMeasures.length - 1);
          const bar = m.final ? "|]" : (isLastInSec ? "||" : "|");
          return `${{body}} ${{bar}}`;
        }});
        lines.push(parts.join(" "));
      }}
      return lines.join("\\n");
    }}

    function buildEj4PageAbc(pageNum, artId) {{
      let slice = [];
      let initKey = "C";
      if (pageNum === 1) {{ slice = EJ4_ALL_MEASURES.slice(0, 45); initKey = "C"; }}
      else if (pageNum === 2) {{ slice = EJ4_ALL_MEASURES.slice(45, 96); initKey = "Bb"; }}
      else if (pageNum === 3) {{ slice = EJ4_ALL_MEASURES.slice(96, 146); initKey = "Gb"; }}
      else {{ slice = EJ4_ALL_MEASURES.slice(146, 194); initKey = "A"; }}

      const lines = [
        `X:${{pageNum}}`,
        "M:4/2",
        "L:1/8",
        `K:${{initKey}}`
      ];
      let idx = 0;
      while (idx < slice.length) {{
        const count = (pageNum === 3 && idx === 15) ? 2 : 3;
        const row = slice.slice(idx, idx + count);
        idx += count;
        if (row[0].keyChg && row[0].num !== 1 && row[0].num !== 97) {{
          lines.push(`K:${{row[0].key}}`);
        }}
        const parts = row.map((m, posInRow) => {{
          let barPrefix = "";
          if (posInRow > 0 && m.dblBar) {{
            barPrefix = m.keyChg ? `|| [K:${{m.key}}] ` : "|| ";
          }}
          const body = formatEj4Measure(m, artId);
          if (m.final) return `${{barPrefix}}${{body}} |]`;
          const nextIdx = m.num;
          if (nextIdx < EJ4_ALL_MEASURES.length && EJ4_ALL_MEASURES[nextIdx].dblBar) {{
            return posInRow === row.length - 1 ? `${{barPrefix}}${{body}} ||` : `${{barPrefix}}${{body}} `;
          }}
          return `${{barPrefix}}${{body}} |`;
        }});
        lines.push(parts.join(" "));
      }}
      return lines.join("\\n");
    }}

    function renderEj4Leduc(artId, secIdx) {{
      const paper = document.getElementById("paper");
      const badgeLabel = EJ4_ART_NAMES[artId] || EJ4_ART_NAMES[0];
      const secMeasures = EJ4_ALL_MEASURES.filter(m => m.sec === secIdx);
      const secTitle = secMeasures.length ? secMeasures[0].secName : "1. Do Mayor";
      const startM = secMeasures.length ? secMeasures[0].num : 1;
      const endM = secMeasures.length ? secMeasures[secMeasures.length - 1].num : 8;

      let html = `
        <div class="ej1-leduc-wrapper">
          <div class="ej1-top-header">
            <div class="ej1-title">E. J. 4</div>
            <div class="ej1-active-badge">${{badgeLabel}}</div>
          </div>
          <div class="ej1-subtitle">A travailler successivement avec chacune des articulations suivantes:</div>
          <div id="ej4-art-score" class="ej1-art-row"></div>

          <div style="margin: 8px 0 12px 0; padding: 8px 8px 4px 8px; border: 1.5px solid #3b82f6; border-radius: 10px; background: #f8fafc;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px; margin-bottom:4px;">
              <span style="font-family:-apple-system,sans-serif; font-size:12px; font-weight:700; color:#1e3a8a;">
                🎯 Tonalidad Activa: ${{secTitle}}
              </span>
              <span style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:600; color:#475569; background:#e2e8f0; padding:2px 8px; border-radius:999px;">
                Compases ${{startM}}–${{endM}} de 194
              </span>
            </div>
            <div id="ej4-focus-score" class="ej1-staff-row"></div>
          </div>

          <div style="font-family:-apple-system,sans-serif; font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.6px; margin: 12px 4px 6px 4px; border-top: 1px solid #cbd5e1; padding-top: 8px;">
            Partitura Urtext Completa · Alphonse Leduc A. L. 16.588 (Págs. 111–114)
          </div>
          <div style="font-size:11px; font-weight:bold; color:#334155; margin:4px 4px 2px 4px;">Pág. 111 (c. 1–45)</div>
          <div id="ej4-p1-score" class="ej1-staff-row" style="border-bottom:1px dashed #cbd5e1; padding-bottom:8px; margin-bottom:8px;"></div>
          <div style="font-size:11px; font-weight:bold; color:#334155; margin:4px 4px 2px 4px;">Pág. 112 (c. 46–96)</div>
          <div id="ej4-p2-score" class="ej1-staff-row" style="border-bottom:1px dashed #cbd5e1; padding-bottom:8px; margin-bottom:8px;"></div>
          <div style="font-size:11px; font-weight:bold; color:#334155; margin:4px 4px 2px 4px;">Pág. 113 (c. 97–146)</div>
          <div id="ej4-p3-score" class="ej1-staff-row" style="border-bottom:1px dashed #cbd5e1; padding-bottom:8px; margin-bottom:8px;"></div>
          <div style="font-size:11px; font-weight:bold; color:#334155; margin:4px 4px 2px 4px;">Pág. 114 (c. 147–194)</div>
          <div id="ej4-p4-score" class="ej1-staff-row"></div>
          <div class="ej1-plate-footer">A. L. 16.588</div>
        </div>
      `;
      paper.innerHTML = html;

      ABCJS.renderAbc("ej4-art-score", EJ4_ARTICULATIONS_ABC, {{
        staffwidth: 920,
        paddingtop: 2,
        paddingbottom: 2,
        paddingleft: 0,
        paddingright: 0,
        responsive: "resize"
      }});

      ABCJS.renderAbc("ej4-focus-score", buildEj4SectionAbc(secIdx, artId), {{
        staffwidth: 720,
        paddingtop: 4,
        paddingbottom: 4,
        paddingleft: 2,
        paddingright: 2,
        responsive: "resize"
      }});

      for (let p = 1; p <= 4; p++) {{
        ABCJS.renderAbc(`ej4-p${{p}}-score`, buildEj4PageAbc(p, artId), {{
          staffwidth: 980,
          paddingtop: 2,
          paddingbottom: 2,
          paddingleft: 0,
          paddingright: 0,
          responsive: "resize"
        }});
      }}
    }}
// === END EJ4 LEDUC ===
"""

    # Insert before function renderScore(abcString)
    target = "    function renderScore(abcString) {"
    replacement = ej4_js_block + "\n    function renderScore(abcString) {\n      const ej4Match = abcString && abcString.match(/%\\s*EJ4_LEDUC_ART:(\\d+):SEC:(\\d+)/);\n      if (ej4Match) {\n        const artId = parseInt(ej4Match[1], 10) || 0;\n        const secIdx = parseInt(ej4Match[2], 10) || 0;\n        renderEj4Leduc(artId, secIdx);\n        return;\n      }"
    # If ej4Match was already added, clean it up first
    html = re.sub(r'\s*const ej4Match = abcString && abcString\.match\(/%\\s\*EJ4_LEDUC_ART:\(\\d\+\):SEC:\(\\d\+\)/\);\s*if \(ej4Match\) \{\s*const artId = parseInt\(ej4Match\[1\], 10\) \|\| 0;\s*const secIdx = parseInt\(ej4Match\[2\], 10\) \|\| 0;\s*renderEj4Leduc\(artId, secIdx\);\s*return;\s*\}', '', html)
    assert target in html, f"Could not find {target} in {template_path}"
    html = html.replace(target, replacement, 1)

    with open(template_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated {template_path}")

def generate_swift_and_kotlin_midi(all_measures):
    # Group measures by section_id (25 sections)
    sec_ids = []
    for m in all_measures:
        if m["section_id"] not in sec_ids:
            sec_ids.append(m["section_id"])

    section_midi_lists = []
    section_names = []
    for sid in sec_ids:
        sec_m = [m for m in all_measures if m["section_id"] == sid]
        section_names.append(sec_m[0]["section_name"])
        ks_map = ej4.KEY_SIGS[sec_m[0]["key_sig"]]
        midi_notes = []
        for m in sec_m:
            active_bar_acc = {}
            for tok in m["notes"]:
                midi_notes.append(abc_token_to_midi(tok, ks_map, active_bar_acc))
        section_midi_lists.append(midi_notes)

    swift_lines = ["    public static let ej4SectionMidiNotes: [[Int]] = ["]
    kotlin_lines = ["    val ej4SectionMidiNotes: List<IntArray> = listOf("]
    for idx, mlist in enumerate(section_midi_lists):
        comma = "," if idx < len(section_midi_lists) - 1 else ""
        arr_str = ", ".join(str(x) for x in mlist)
        swift_lines.append(f"        [{arr_str}]{comma} // {section_names[idx]}")
        kotlin_lines.append(f"        intArrayOf({arr_str}){comma} // {section_names[idx]}")
    swift_lines.append("    ]")
    kotlin_lines.append("    )")

    with open(os.path.join(WORKSPACE_DIR, "ej4_generated_snippets.txt"), "w", encoding="utf-8") as f:
        f.write("// SWIFT:\n" + "\n".join(swift_lines) + "\n\n// KOTLIN:\n" + "\n".join(kotlin_lines) + "\n")
    print("Wrote ej4_generated_snippets.txt")

if __name__ == "__main__":
    all_m = ej4.build_all_measures()
    build_abc_files(all_m)
    copy_pdf_files()
    compact_m = build_compact_measures_for_js(all_m)
    art_strip = ej4.build_articulation_strip_abc()
    update_score_template(
        os.path.join(WORKSPACE_DIR, "FluteModes/FluteModes/Resources/score_template.html"),
        compact_m,
        art_strip
    )
    update_score_template(
        os.path.join(WORKSPACE_DIR, "FluteModesAndroid/app/src/main/assets/score_template.html"),
        compact_m,
        art_strip
    )
    generate_swift_and_kotlin_midi(all_m)
