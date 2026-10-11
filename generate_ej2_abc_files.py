import os
import re
import shutil

ARTIFACT_DIR = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"
ABC_EJ2_DIR = "/Users/sebas/Desktop/partituras/abc_ej2"
SCORES_ABC_DIR = "/Users/sebas/Desktop/partituras/scores/abc"
DOCS_ABC_DIR = "/Users/sebas/Desktop/partituras/docs/downloads/abc"
IOS_ABC_EJ2_DIR = "/Users/sebas/Desktop/partituras/FluteModes/FluteModes/Resources/abc_ej2"
ANDROID_ABC_EJ2_DIR = "/Users/sebas/Desktop/partituras/FluteModesAndroid/app/src/main/assets/abc_ej2"

for d in [ABC_EJ2_DIR, SCORES_ABC_DIR, DOCS_ABC_DIR, IOS_ABC_EJ2_DIR, ANDROID_ABC_EJ2_DIR]:
    os.makedirs(d, exist_ok=True)

# 10 Articulaciones oficiales de Taffanel & Gaubert E.J. 2 (A. L. 16.588) en Re menor
ARTICULATIONS_HEADER_ABC = """X:0
T:E. J. 2 — Tabla de 10 Articulaciones Oficiales (Re menor)
C:Paul Taffanel & Philippe Gaubert (A. L. 16.588)
M:C
L:1/16
K:C
V:1 clef=treble stem=up
%%score 1
(DEF"^1"GAGFE) | (DEF"^2"G)(AGFE) | .D(EF"^3"G) .A(GFE) | (DEF)."^4"G (AGF).E | (DE).F."^5"G (AG).F.E | .D.E"^6"(FG) .A.G(FE) | .D(EF)."^7"G .A(GF).E | (DE)"^8"(FG)(AG)(FE) | .D(EF)"^9"(GA)(GF).E | .D.E.F."^10"G.A.G.F.E |]"""

# Definición de los 30 compases + compás 31 de cierre de E.J. 2 (A. L. 16.588, págs. 06 y 10)
EJ2_MEASURES = [
    (1,  "Re menor (i)",           ["DEFGAGFE",     "DEFGAGFE", "DEFGAGFE", "DEFGAGFE"], "|:", "|", False),
    (2,  "vii° -> Mib menor",      ["D_E=F_G_AGFE", "DEFGAGFE", "DEFGAGFE", "DEFGAFED"], "",   "|", False),
    (3,  "Mib menor (i)",          ["_EF_G_A_BAGF", "EFGABAGF", "EFGABAGF", "EFGABAGF"], "",   "|", False),
    (4,  "vii° -> Mi menor",       ["^D=E^F=G=AGFE", "DEFGAGFE", "DEFGAGFE", "DEFGAFED"], "",  "|", False),
    (5,  "Mi menor (i)",           ["E^FGABAGF",    "EFGABAGF", "EFGABAGF", "EFGABAGF"], "",   "|", False),
    (6,  "vii° -> Fa menor",       ["E=F=G_A_BAGF", "EFGABAGF", "EFGABAGF", "EFGABGFE"], "",   "|", False),
    (7,  "Fa menor (i)",           ["FG_A_BcBAG",   "FGABcBAG", "FGABcBAG", "FGABcBAG"], "",   "|", False),
    (8,  "vii° -> Fa# menor",      ["^E^F^G=A=BAGF", "EFGABAGF", "EFGABAGF", "EFGABGFE"], "",  "|", False),
    (9,  "Fa# menor (i)",          ["^F^GAB^cBAG",  "FGABcBAG", "FGABcBAG", "FGABcBAG"], "",   "|", False),
    (10, "vii° -> Sol menor",      ["^F=G=A_B=cBAG", "FGABcBAG", "FGABcBAG", "FGABcAGF"], "",  "|", False),
    (11, "Sol menor (i)",          ["GA_BcdcBA",    "GABcdcBA", "GABcdcBA", "GABcdcBA"], "",   "|", False),
    (12, "vii° -> Sol# menor",     ["^^F^G^AB^cBAG", "FGABcBAG", "FGABcBAG", "FGABcAGF"], "",  "|", False),
    (13, "Sol# menor (i)",         ["^G^AB^c^dcBA", "GABcdcBA", "GABcdcBA", "GABcdcBA"], "",   "|", False),
    (14, "vii° -> La menor",       ["^G=A=B=c=dcBA", "GABcdcBA", "GABcdcBA", "GABcdBAG"], "",  "|", False),
    (15, "La menor (i)",           ["ABcdedcB",     "ABcdedcB", "ABcdedcB", "ABcdedcB"], "",   "|", False),
    (16, "vii° -> Sib menor",      ["A_B=c_d_edcB", "ABcdedcB", "ABcdedcB", "ABcdecBA"], "",   "|", False),
    (17, "Sib menor (i)",          ["_Bc_d_efedc",  "Bcdefedc", "Bcdefedc", "Bcdefedc"], "",   "|", False),
    (18, "vii° -> Si menor",       ["^A=B^c=d=edcB", "ABcdedcB", "ABcdedcB", "ABcdecBA"], "",  "|", False),
    (19, "Si menor (i)",           ["B^cde^fedc",   "Bcdefedc", "Bcdefedc", "Bcdefedc"], "",   "|", False),
    (20, "vii° -> Do menor",       ["B=c=d_e=fedc", "Bcdefedc", "Bcdefedc", "BcdefdcB"], "",   "|", False),
    (21, "Do menor (i)",           ["cd_efgfed",    "cdefgfed", "cdefgfed", "cdefgfed"], "",   "|", False),
    (22, "vii° -> Do# menor",      ["^B^c^d=e^fedc", "Bcdefedc", "Bcdefedc", "BcdefdcB"], "",  "|", False),
    (23, "Do# menor (i)",          ["^c^de^f^gfed", "cdefgfed", "cdefgfed", "cdefgfed"], "",   "|", False),
    (24, "vii° -> Re menor",       ["^c=d=e=f=gfed", "cdefgfed", "cdefgfed", "cdefgedc"], "",  ":|", False),
    (25, "Re menor (i) [8va]",     ["defgagfe",     "defgagfe", "defgagfe", "defgagfe"], "",   "|", True),
    (26, "vii° -> Mib m [8va]",    ["d_e=f_g_agfe", "defgagfe", "defgagfe", "defgafed"], "",   "|", True),
    (27, "Mib menor (i) [8va]",    ["_ef_g_a_bagf", "efgabagf", "efgabagf", "efgabagf"], "",   "|", True),
    (28, "vii° -> Mi m [8va]",     ["^d=e^f=g=agfe", "defgagfe", "defgagfe", "defgafed"], "",  "|", True),
    (29, "Mi menor (i) [8va]",     ["e^fgabagf",    "efgabagf", "efgabagf", "efgabagf"], "",   "|", True),
    (30, "vii° -> Fa m + Fin [8va]", ["e=f=g_a_bagf", "efgabagf", "efgabagf", "efgabgfe"], "", "| f4 z4 z8 |]", True),
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

def main():
    collection_blocks = [ARTICULATIONS_HEADER_ABC + "\n"]
    created_files = []

    for art_id, slug, desc in ARTICULATION_META:
        filename = f"{art_id:02d}_Taffanel_EJ2_{slug}.abc"
        abc_content = build_abc_for_articulation(art_id, desc, tune_index=art_id + 1)
        if art_id == 0:
            full_file_content = ARTICULATIONS_HEADER_ABC + "\n\n" + abc_content
        else:
            full_file_content = abc_content

        out_path_1 = os.path.join(ABC_EJ2_DIR, filename)
        with open(out_path_1, "w", encoding="utf-8") as f:
            f.write(full_file_content)

        for target_dir in [SCORES_ABC_DIR, DOCS_ABC_DIR, IOS_ABC_EJ2_DIR, ANDROID_ABC_EJ2_DIR]:
            shutil.copy(out_path_1, os.path.join(target_dir, filename))

        created_files.append(out_path_1)
        collection_blocks.append(abc_content)

    master_filename = "11_Coleccion_Completa_Taffanel_EJ2_10_Articulaciones.abc"
    master_content = "\n".join(collection_blocks)
    master_path_1 = os.path.join(ABC_EJ2_DIR, master_filename)
    with open(master_path_1, "w", encoding="utf-8") as f:
        f.write(master_content)

    for target_dir in [SCORES_ABC_DIR, DOCS_ABC_DIR, IOS_ABC_EJ2_DIR, ANDROID_ABC_EJ2_DIR]:
        shutil.copy(master_path_1, os.path.join(target_dir, master_filename))
    shutil.copy(master_path_1, os.path.join(ARTIFACT_DIR, "taffanel_ej2_completo.abc"))
    shutil.copy(master_path_1, "/Users/sebas/Desktop/partituras/taffanel_ej2_completo.abc")
    created_files.append(master_path_1)

    print(f"Created {len(created_files)} E.J. 2 ABC files across all directories.")

if __name__ == "__main__":
    main()
