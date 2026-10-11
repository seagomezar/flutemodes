import os
import re
import shutil

ARTIFACT_DIR = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"
ABC_EJ1_DIR = "/Users/sebas/Desktop/partituras/abc_ej1"
SCORES_ABC_DIR = "/Users/sebas/Desktop/partituras/scores/abc"

os.makedirs(ABC_EJ1_DIR, exist_ok=True)
os.makedirs(SCORES_ABC_DIR, exist_ok=True)

# 10 Articulaciones oficiales de Taffanel & Gaubert E.J. 1 (A. L. 16.588)
ARTICULATIONS_HEADER_ABC = """X:0
T:E. J. 1 — Tabla de 10 Articulaciones Oficiales
C:Paul Taffanel & Philippe Gaubert (A. L. 16.588)
M:none
L:1/16
K:C
V:1 clef=treble stem=up
%%score 1
(DEF"^1"GAGFE) | (DEF"^2"G)(AGFE) | .D(EF"^3"G) .A(GFE) | (DEF)."^4"G (AGF).E | (DE).F."^5"G (AG).F.E | .D.E"^6"(FG) .A.G(FE) | .D(EF)."^7"G .A(GF).E | (DE)"^8"(FG)(AG)(FE) | .D(EF)"^9"(GA)(GF).E | .D.E.F."^10"G.A.G.F.E |]"""

# Definición de los 30 compases + compás 31 de cierre (exactamente como en A. L. 16.588)
# Cada tupla: (measure_number, tonal_label, [beat1, beat2, beat3, beat4], bar_prefix, bar_suffix, is_8va)
EJ1_MEASURES = [
    (1,  "Re Mayor (I)",        ["DE^FGAGFE", "DEFGAGFE", "DEFGAGFE", "DEFGAGFE"], "|:", "|", False),
    (2,  "vii° -> Mib Mayor",   ["D_E=FG_AGFE", "DEFGAGFE", "DEFGAGFE", "DEFGAFED"], "",   "|", False),
    (3,  "Mib Mayor (I)",       ["_EFG_A_BAGF", "EFGABAGF", "EFGABAGF", "EFGABAGF"], "",   "|", False),
    (4,  "vii° -> Mi Mayor",    ["^D=E^F^G=AGFE", "DEFGAGFE", "DEFGAGFE", "DEFGAFED"], "", "|", False),
    (5,  "Mi Mayor (I)",        ["E^F^GABAGF", "EFGABAGF", "EFGABAGF", "EFGABAGF"], "",   "|", False),
    (6,  "vii° -> Fa Mayor",    ["E=F=GA_BAGF", "EFGABAGF", "EFGABAGF", "EFGABGFE"], "",   "|", False),
    (7,  "Fa Mayor (I)",        ["FGA_BcBAG", "FGABcBAG", "FGABcBAG", "FGABcBAG"], "",     "|", False),
    (8,  "vii° -> Fa# Mayor",   ["^E^F^G^A=BAGF", "EFGABAGF", "EFGABAGF", "EFGABGFE"], "", "|", False),
    (9,  "Fa# Mayor (I)",       ["^F^G^AB^cBAG", "FGABcBAG", "FGABcBAG", "FGABcBAG"], "",  "|", False),
    (10, "vii° -> Sol Mayor",   ["^F=G=AB=cBAG", "FGABcBAG", "FGABcBAG", "FGABcAGF"], "",  "|", False),
    (11, "Sol Mayor (I)",       ["GABcdcBA", "GABcdcBA", "GABcdcBA", "GABcdcBA"], "",      "|", False),
    (12, "vii° -> Lab Mayor",   ["G_A_Bc_dcBA", "GABcdcBA", "GABcdcBA", "GABcdBAG"], "",   "|", False),
    (13, "Lab Mayor (I)",       ["_A_Bc_d_edcB", "ABcdedcB", "ABcdedcB", "ABcdedcB"], "",  "|", False),
    (14, "vii° -> La Mayor",    ["^G=A=B^c=dcBA", "GABcdcBA", "GABcdcBA", "GABcdBAG"], "", "|", False),
    (15, "La Mayor (I)",        ["AB^cdedcB", "ABcdedcB", "ABcdedcB", "ABcdedcB"], "",     "|", False),
    (16, "vii° -> Sib Mayor",   ["A_B=cd_edcB", "ABcdedcB", "ABcdedcB", "ABcdecBA"], "",   "|", False),
    (17, "Sib Mayor (I)",       ["_Bcd_efedc", "Bcdefedc", "Bcdefedc", "Bcdefedc"], "",    "|", False),
    (18, "vii° -> Si Mayor",    ["^A=B^c^dedcB", "ABcdedcB", "ABcdedcB", "ABcdecBA"], "",  "|", False),
    (19, "Si Mayor (I)",        ["B^c^de^fedc", "Bcdefedc", "Bcdefedc", "Bcdefedc"], "",   "|", False),
    (20, "vii° -> Do Mayor",    ["B=c=de=fedc", "Bcdefedc", "Bcdefedc", "BcdefdcB"], "",   "|", False),
    (21, "Do Mayor (I)",        ["cdefgfed", "cdefgfed", "cdefgfed", "cdefgfed"], "",      "|", False),
    (22, "vii° -> Reb Mayor",   ["c_d_ef_gfed", "cdefgfed", "cdefgfed", "cdefgedc"], "",   "|", False),
    (23, "Reb Mayor (I)",       ["_d_ef_g_agfe", "defgagfe", "defgagfe", "defgagfe"], "",  "|", False),
    (24, "vii° -> Re Mayor",    ["^c=d=e^f=gfed", "cdefgfed", "cdefgfed", "cdefgedc"], "", ":|", False),
    (25, "Re Mayor (I) [8va]",  ["de^fgagfe", "defgagfe", "defgagfe", "defgagfe"], "",     "|", True),
    (26, "vii° -> Mib [8va]",   ["d_e=fg_agfe", "defgagfe", "defgagfe", "defgafed"], "",   "|", True),
    (27, "Mib Mayor (I) [8va]", ["_efg_a_bagf", "efgabagf", "efgabagf", "efgabagf"], "",   "|", True),
    (28, "vii° -> Mi [8va]",    ["^d=e^f^g=agfe", "defgagfe", "defgagfe", "defgafed"], "", "|", True),
    (29, "Mi Mayor (I) [8va]",  ["e^f^gabagf", "efgabagf", "efgabagf", "efgabagf"], "",   "|", True),
    (30, "vii° -> Fa + Fin [8va]", ["e=f=ga_bagf", "efgabagf", "efgabagf", "efgabgfe"], "", "| f4 z4 z8 |]", True),
]

ARTICULATION_META = [
    (0,  "Original_AL16588",                 "Original (Sin articulación fija — A. L. 16.588)"),
    (1,  "Articulacion_01_8_Ligadas",        "1. A 8 ligadas (Toda ligada)"),
    (2,  "Articulacion_02_4_y_4_Ligadas",    "2. A 4 y 4 ligadas"),
    (3,  "Articulacion_03_1_Picada_3_Ligadas", "3. 1 picada y 3 ligadas"),
    (4,  "Articulacion_04_3_Ligadas_1_Picada", "4. 3 ligadas y 1 picada"),
    (5,  "Articulacion_05_2_Ligadas_2_Picadas", "5. 2 ligadas y 2 picadas"),
    (6,  "Articulacion_06_2_Picadas_2_Ligadas", "6. 2 picadas y 2 ligadas"),
    (7,  "Articulacion_07_1_Picada_2_Ligadas_1_Picada", "7. 1 picada, 2 ligadas y 1 picada"),
    (8,  "Articulacion_08_De_2_en_2_Ligadas", "8. De 2 en 2 ligadas"),
    (9,  "Articulacion_09_De_2_en_2_Sincopadas", "9. De 2 en 2 sincopadas (a contratiempo)"),
    (10, "Articulacion_10_Todo_Picado",      "10. Todo picado (Staccato)"),
]

NOTE_REGEX = re.compile(r'[\^_=]?[A-Ga-g]')

def split_8_notes(beat_str):
    notes = NOTE_REGEX.findall(beat_str)
    assert len(notes) == 8, f"Expected 8 notes in {beat_str}, got {len(notes)}: {notes}"
    return notes

def apply_ej1_articulation(beat_str, art_id):
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
        f"T:E. J. 1 — {title_desc}",
        "C:Paul Taffanel & Philippe Gaubert (A. L. 16.588)",
        f"% EJ1_LEDUC_ART:{art_id}",
        "%%barsperstaff 1",
        "M:4/2",
        "L:1/16",
        f"Q:1/4={tempo_bpm}",
        "K:C",
        "V:1 clef=treble stem=up",
        "%%score 1",
    ]
    current_stem = "up"
    for m_num, label, beats, prefix, suffix, is_8va in EJ1_MEASURES:
        target_stem = "up" if m_num <= 10 else "down"
        if target_stem != current_stem:
            lines.append(f"[V:1 stem={target_stem}]")
            current_stem = target_stem
        art_beats = [apply_ej1_articulation(b, art_id) for b in beats]
        beats_str = " ".join(art_beats)
        reprise_annot = '"^Reprise à l\'octave"' if m_num == 1 else ('"^8va"' if m_num == 25 else "")
        if prefix:
            line = f"{prefix} {reprise_annot}{beats_str} {suffix} % Compás {m_num}: {label}"
        else:
            line = f"{reprise_annot}{beats_str} {suffix} % Compás {m_num}: {label}"
        lines.append(line)
    return "\n".join(lines) + "\n"

def main():
    collection_blocks = [ARTICULATIONS_HEADER_ABC + "\n"]
    created_files = []

    for art_id, slug, desc in ARTICULATION_META:
        filename = f"{art_id:02d}_Taffanel_EJ1_{slug}.abc"
        abc_content = build_abc_for_articulation(art_id, desc, tune_index=art_id + 1)
        if art_id == 0:
            full_file_content = ARTICULATIONS_HEADER_ABC + "\n\n" + abc_content
        else:
            full_file_content = abc_content

        out_path_1 = os.path.join(ABC_EJ1_DIR, filename)
        out_path_2 = os.path.join(SCORES_ABC_DIR, filename)
        with open(out_path_1, "w", encoding="utf-8") as f:
            f.write(full_file_content)
        shutil.copy(out_path_1, out_path_2)
        created_files.append(out_path_1)
        collection_blocks.append(abc_content)

    master_filename = "11_Coleccion_Completa_Taffanel_EJ1_10_Articulaciones.abc"
    master_content = "\n".join(collection_blocks)
    master_path_1 = os.path.join(ABC_EJ1_DIR, master_filename)
    master_path_2 = os.path.join(SCORES_ABC_DIR, master_filename)
    master_artifact = os.path.join(ARTIFACT_DIR, "taffanel_ej1_completo.abc")
    with open(master_path_1, "w", encoding="utf-8") as f:
        f.write(master_content)
    shutil.copy(master_path_1, master_path_2)
    shutil.copy(master_path_1, master_artifact)
    shutil.copy(master_path_1, "/Users/sebas/Desktop/partituras/taffanel_ej1_completo.abc")
    created_files.append(master_path_1)

    print(f"Created {len(created_files)} ABC files in {ABC_EJ1_DIR} and {SCORES_ABC_DIR}:")
    for p in created_files:
        print(" -", p)

if __name__ == "__main__":
    main()
