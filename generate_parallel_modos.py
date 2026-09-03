import subprocess
import os
import shutil
import fitz

# Definición de las 12 alturas cromáticas
# Con sus notas diatónicas base (15 notas: 2 octavas de registro)
# y las armaduras Mayor y Menor según la propuesta del maestro.

TONICS = [
    {
        "id": "01_si",
        "name": "Si (B3 - Pata de Si)",
        "display": "Si (B3)",
        "title_note": "Si (B3 - Pata de Si)",
        "base_notes": ["B,", "C", "D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'"],
        "major_key": "B",
        "minor_key": "Bm",
        "major_desc": "5 sostenidos (Fa♯, Do♯, Sol♯, Re♯, La♯)",
        "minor_desc": "2 sostenidos (Fa♯, Do♯)",
        "prep_note": "B,",
        # Accidentales sobre grados (0..6):
        # En Si Mayor (F, C, G, D, A sostenidos):
        # Lidio: grado 3 (E) -> ^E
        # Mixolidio: grado 6 (A) -> =A
        "lyd_acc": {3: "^"},
        "mix_acc": {6: "="},
        # En Si Menor (F, C sostenidos):
        # Dórico: grado 5 (G) -> ^G
        # Frigio: grado 1 (C) -> =C
        # Lócrio: grado 1 (C) -> =C, grado 4 (F) -> =F
        "dor_acc": {5: "^"},
        "phr_acc": {1: "="},
        "loc_acc": {1: "=", 4: "="},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Mi♯",
            "mix": "Séptima menor accidental: La♮",
            "dor": "Sexta mayor accidental: Sol♯",
            "phr": "Segunda menor accidental: Do♮",
            "loc": "Segunda menor: Do♮ y Quinta disminuida: Fa♮"
        }
    },
    {
        "id": "02_do",
        "name": "Do",
        "display": "Do",
        "title_note": "Do",
        "base_notes": ["C", "D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'"],
        "major_key": "C",
        "minor_key": "Cm",
        "major_desc": "Sin alteraciones",
        "minor_desc": "3 bemoles (Si♭, Mi♭, La♭)",
        "prep_note": "C",
        "lyd_acc": {3: "^"},
        "mix_acc": {6: "_"},
        "dor_acc": {5: "="},
        "phr_acc": {1: "_"},
        "loc_acc": {1: "_", 4: "_"},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Fa♯",
            "mix": "Séptima menor accidental: Si♭",
            "dor": "Sexta mayor accidental: La♮",
            "phr": "Segunda menor accidental: Re♭",
            "loc": "Segunda menor: Re♭ y Quinta disminuida: Sol♭"
        }
    },
    {
        "id": "03_do_sostenido",
        "name": "Do sostenido (Do♯)",
        "display": "Do♯",
        "title_note": "Do sostenido (Do♯)",
        "base_notes": ["C", "D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'"],
        "major_key": "C#",
        "minor_key": "C#m",
        "major_desc": "7 sostenidos",
        "minor_desc": "4 sostenidos (Fa♯, Do♯, Sol♯, Re♯)",
        "prep_note": "C",
        "lyd_acc": {3: "^^"},
        "mix_acc": {6: "="},
        "dor_acc": {5: "^"},
        "phr_acc": {1: "="},
        "loc_acc": {1: "=", 4: "="},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Fa𝄪 (doble sostenido)",
            "mix": "Séptima menor accidental: Si♮",
            "dor": "Sexta mayor accidental: La♯",
            "phr": "Segunda menor accidental: Re♮",
            "loc": "Segunda menor: Re♮ y Quinta disminuida: Sol♮"
        }
    },
    {
        "id": "04_re",
        "name": "Re",
        "display": "Re",
        "title_note": "Re",
        "base_notes": ["D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'"],
        "major_key": "D",
        "minor_key": "Dm",
        "major_desc": "2 sostenidos (Fa♯, Do♯)",
        "minor_desc": "1 bemol (Si♭)",
        "prep_note": "D",
        "lyd_acc": {3: "^"},
        "mix_acc": {6: "="},
        "dor_acc": {5: "="},
        "phr_acc": {1: "_"},
        "loc_acc": {1: "_", 4: "_"},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Sol♯",
            "mix": "Séptima menor accidental: Do♮",
            "dor": "Sexta mayor accidental: Si♮",
            "phr": "Segunda menor accidental: Mi♭",
            "loc": "Segunda menor: Mi♭ y Quinta disminuida: La♭"
        }
    },
    {
        "id": "05_mi_bemol",
        "name": "Mi bemol (Mi♭)",
        "display": "Mi♭",
        "title_note": "Mi bemol (Mi♭)",
        "base_notes": ["E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'"],
        "major_key": "Eb",
        "minor_key": "Ebm",
        "major_desc": "3 bemoles (Si♭, Mi♭, La♭)",
        "minor_desc": "6 bemoles",
        "prep_note": "E",
        "lyd_acc": {3: "="},
        "mix_acc": {6: "_"},
        "dor_acc": {5: "="},
        "phr_acc": {1: "_"},
        "loc_acc": {1: "_", 4: "_"},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: La♮",
            "mix": "Séptima menor accidental: Re♭",
            "dor": "Sexta mayor accidental: Do♮",
            "phr": "Segunda menor accidental: Fa♭",
            "loc": "Segunda menor: Fa♭ y Quinta disminuida: Si𝄫"
        }
    },
    {
        "id": "06_mi",
        "name": "Mi",
        "display": "Mi",
        "title_note": "Mi",
        "base_notes": ["E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'"],
        "major_key": "E",
        "minor_key": "Em",
        "major_desc": "4 sostenidos (Fa♯, Do♯, Sol♯, Re♯)",
        "minor_desc": "1 sostenido (Fa♯)",
        "prep_note": "E",
        "lyd_acc": {3: "^"},
        "mix_acc": {6: "="},
        "dor_acc": {5: "^"},
        "phr_acc": {1: "="},
        "loc_acc": {1: "=", 4: "_"},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: La♯",
            "mix": "Séptima menor accidental: Re♮",
            "dor": "Sexta mayor accidental: Do♯",
            "phr": "Segunda menor accidental: Fa♮",
            "loc": "Segunda menor: Fa♮ y Quinta disminuida: Si♭"
        }
    },
    {
        "id": "07_fa",
        "name": "Fa",
        "display": "Fa",
        "title_note": "Fa",
        "base_notes": ["F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'"],
        "major_key": "F",
        "minor_key": "Fm",
        "major_desc": "1 bemol (Si♭)",
        "minor_desc": "4 bemoles (Si♭, Mi♭, La♭, Re♭)",
        "prep_note": "F",
        "lyd_acc": {3: "="},
        "mix_acc": {6: "_"},
        "dor_acc": {5: "="},
        "phr_acc": {1: "_"},
        "loc_acc": {1: "_", 4: "_"},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Si♮",
            "mix": "Séptima menor accidental: Mi♭",
            "dor": "Sexta mayor accidental: Re♮",
            "phr": "Segunda menor accidental: Sol♭",
            "loc": "Segunda menor: Sol♭ y Quinta disminuida: Do♭"
        }
    },
    {
        "id": "08_fa_sostenido",
        "name": "Fa sostenido (Fa♯)",
        "display": "Fa♯",
        "title_note": "Fa sostenido (Fa♯)",
        "base_notes": ["F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'"],
        "major_key": "F#",
        "minor_key": "F#m",
        "major_desc": "6 sostenidos",
        "minor_desc": "3 sostenidos (Fa♯, Do♯, Sol♯)",
        "prep_note": "F",
        "lyd_acc": {3: "^"},
        "mix_acc": {6: "="},
        "dor_acc": {5: "^"},
        "phr_acc": {1: "="},
        "loc_acc": {1: "=", 4: "="},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Si♯",
            "mix": "Séptima menor accidental: Mi♮",
            "dor": "Sexta mayor accidental: Re♯",
            "phr": "Segunda menor accidental: Sol♮",
            "loc": "Segunda menor: Sol♮ y Quinta disminuida: Do♮"
        }
    },
    {
        "id": "09_sol",
        "name": "Sol",
        "display": "Sol",
        "title_note": "Sol",
        "base_notes": ["G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'"],
        "major_key": "G",
        "minor_key": "Gm",
        "major_desc": "1 sostenido (Fa♯)",
        "minor_desc": "2 bemoles (Si♭, Mi♭)",
        "prep_note": "G",
        "lyd_acc": {3: "^"},
        "mix_acc": {6: "="},
        "dor_acc": {5: "="},
        "phr_acc": {1: "_"},
        "loc_acc": {1: "_", 4: "_"},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Do♯",
            "mix": "Séptima menor accidental: Fa♮",
            "dor": "Sexta mayor accidental: Mi♮",
            "phr": "Segunda menor accidental: La♭",
            "loc": "Segunda menor: La♭ y Quinta disminuida: Re♭"
        }
    },
    {
        "id": "10_la_bemol",
        "name": "La bemol (La♭)",
        "display": "La♭",
        "title_note": "La bemol (La♭)",
        "base_notes": ["A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'"],
        "major_key": "Ab",
        "minor_key": "Abm",
        "major_desc": "4 bemoles (Si♭, Mi♭, La♭, Re♭)",
        "minor_desc": "7 bemoles",
        "prep_note": "A",
        "lyd_acc": {3: "="},
        "mix_acc": {6: "_"},
        "dor_acc": {5: "="},
        "phr_acc": {1: "_"},
        "loc_acc": {1: "_", 4: "_"},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Re♮",
            "mix": "Séptima menor accidental: Sol♭",
            "dor": "Sexta mayor accidental: Fa♮",
            "phr": "Segunda menor accidental: Si𝄫",
            "loc": "Segunda menor: Si𝄫 y Quinta disminuida: Mi𝄫"
        }
    },
    {
        "id": "11_la",
        "name": "La",
        "display": "La",
        "title_note": "La",
        "base_notes": ["A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'"],
        "major_key": "A",
        "minor_key": "Am",
        "major_desc": "3 sostenidos (Fa♯, Do♯, Sol♯)",
        "minor_desc": "Sin alteraciones",
        "prep_note": "A",
        "lyd_acc": {3: "^"},
        "mix_acc": {6: "="},
        "dor_acc": {5: "^"},
        "phr_acc": {1: "_"},
        "loc_acc": {1: "_", 4: "_"},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Re♯",
            "mix": "Séptima menor accidental: Sol♮",
            "dor": "Sexta mayor accidental: Fa♯",
            "phr": "Segunda menor accidental: Si♭",
            "loc": "Segunda menor: Si♭ y Quinta disminuida: Mi♭"
        }
    },
    {
        "id": "12_si_bemol",
        "name": "Si bemol (Si♭)",
        "display": "Si♭",
        "title_note": "Si bemol (Si♭)",
        "base_notes": ["B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        "major_key": "Bb",
        "minor_key": "Bbm",
        "major_desc": "2 bemoles (Si♭, Mi♭)",
        "minor_desc": "5 bemoles (Si♭, Mi♭, La♭, Re♭, Sol♭)",
        "prep_note": "B",
        "lyd_acc": {3: "="},
        "mix_acc": {6: "_"},
        "dor_acc": {5: "="},
        "phr_acc": {1: "_"},
        "loc_acc": {1: "_", 4: "_"},
        "notes_desc": {
            "lyd": "Cuarta aumentada accidental: Mi♮",
            "mix": "Séptima menor accidental: La♭",
            "dor": "Sexta mayor accidental: Sol♮",
            "phr": "Segunda menor accidental: Do♭",
            "loc": "Segunda menor: Do♭ y Quinta disminuida: Fa♭"
        }
    }
]

MODES_PARALLEL = [
    # Familia Mayor (Armadura Mayor fija)
    {
        "num": 1, "family": "Mayor",
        "name": "Jónico (Mayor)", "char": "Brillante y luminoso",
        "formula": "1 - 2 - 3 - 4 - 5 - 6 - 7",
        "is_major_family": True, "acc_key": None,
        "note_label": "Escala mayor base"
    },
    {
        "num": 2, "family": "Mayor",
        "name": "Lidio", "char": "Etéreo y soñador",
        "formula": "1 - 2 - 3 - ♯4 - 5 - 6 - 7",
        "is_major_family": True, "acc_key": "lyd",
        "note_label": "Cuarta aumentada (♯4)"
    },
    {
        "num": 3, "family": "Mayor",
        "name": "Mixolidio", "char": "Festivo y folclórico",
        "formula": "1 - 2 - 3 - 4 - 5 - 6 - ♭7",
        "is_major_family": True, "acc_key": "mix",
        "note_label": "Séptima menor (♭7)"
    },
    # Familia Menor (Armadura Menor fija)
    {
        "num": 4, "family": "Menor",
        "name": "Dórico", "char": "Melancólico y noble",
        "formula": "1 - 2 - ♭3 - 4 - 5 - 6 - ♭7",
        "is_major_family": False, "acc_key": "dor",
        "note_label": "Sexta mayor (6)"
    },
    {
        "num": 5, "family": "Menor",
        "name": "Eólico (Menor Natural)", "char": "Triste e introspectivo",
        "formula": "1 - 2 - ♭3 - 4 - 5 - ♭6 - ♭7",
        "is_major_family": False, "acc_key": None,
        "note_label": "Escala menor natural base"
    },
    {
        "num": 6, "family": "Menor",
        "name": "Frigio", "char": "Oscuro y exótico",
        "formula": "1 - ♭2 - ♭3 - 4 - 5 - ♭6 - ♭7",
        "is_major_family": False, "acc_key": "phr",
        "note_label": "Segunda menor (♭2)"
    },
    {
        "num": 7, "family": "Menor",
        "name": "Lócrio", "char": "Inestable y tenso",
        "formula": "1 - ♭2 - ♭3 - 4 - ♭5 - ♭6 - ♭7",
        "is_major_family": False, "acc_key": "loc",
        "note_label": "Segunda menor (♭2) y Quinta disminuida (♭5)"
    }
]

def apply_accidentals_to_notes(notes_16, acc_dict):
    """
    notes_16 is a list of 16 note strings across 2 octaves.
    acc_dict maps degree index (0..6) to accidental string ('^', '=', '_', '^^')
    """
    if not acc_dict:
        return list(notes_16)
    res = []
    for idx, note in enumerate(notes_16):
        degree = idx % 7
        if degree in acc_dict:
            acc = acc_dict[degree]
            res.append(f"{acc}{note}")
        else:
            res.append(note)
    return res

def generate_mode_measures(notes_16):
    s = notes_16
    # 8 measures contour
    c1 = f"({s[0]}{s[1]}{s[2]}{s[3]} {s[4]}{s[5]}{s[6]}{s[7]}) ({s[8]}{s[7]}{s[6]}{s[5]} {s[4]}{s[3]}{s[2]}{s[1]})"
    c2 = f"({s[2]}{s[3]}{s[4]}{s[5]} {s[6]}{s[7]}{s[8]}{s[9]}) ({s[10]}{s[9]}{s[8]}{s[7]} {s[6]}{s[5]}{s[4]}{s[3]})"
    c3 = f"({s[4]}{s[5]}{s[6]}{s[7]} {s[8]}{s[9]}{s[10]}{s[11]}) ({s[12]}{s[11]}{s[10]}{s[9]} {s[8]}{s[7]}{s[6]}{s[5]})"
    c4 = f"({s[6]}{s[7]}{s[8]}{s[9]} {s[10]}{s[11]}{s[12]}{s[13]}) ({s[14]}{s[13]}{s[12]}{s[11]} {s[10]}{s[9]}{s[8]}{s[7]})"
    c5 = f"({s[6]}{s[7]}{s[8]}{s[9]} {s[10]}{s[11]}{s[12]}{s[13]}) ({s[12]}{s[11]}{s[10]}{s[9]} {s[8]}{s[7]}{s[6]}{s[5]})"
    c6 = f"({s[4]}{s[5]}{s[6]}{s[7]} {s[8]}{s[9]}{s[10]}{s[11]}) ({s[10]}{s[9]}{s[8]}{s[7]} {s[6]}{s[5]}{s[4]}{s[3]})"
    c7 = f"({s[2]}{s[3]}{s[4]}{s[5]} {s[6]}{s[7]}{s[8]}{s[9]}) ({s[8]}{s[7]}{s[6]}{s[5]} {s[4]}{s[3]}{s[2]}{s[1]})"
    c8 = f"({s[0]}{s[1]}{s[2]}{s[3]} {s[4]}{s[5]}{s[6]}{s[7]}) ({s[6]}{s[5]}{s[4]}{s[3]} {s[2]}{s[1]}{s[0]}2)"
    return c1, c2, c3, c4, c5, c6, c7, c8

def generate_prep_variants_abc(p_note, key_sig):
    p = p_note
    # Preparatory notes: 8 eighth notes starting on p_note
    return f"""X:0
M:4/2
L:1/8
Q:1/2=90
K:{key_sig}
V:1 clef=treble
%%score 1
%%barsperstaff 8
%%stem down
"1"({p}DEF GABc) | "2"({p}DEF) (GABc) | "3"({p}D).E.F (GA).B.c | "4".{p}(DE).F .G(AB).c | "5".{p}.D(EF) .G.A(Bc) | "6".{p}(DEF) .G(ABc) | "7"({p}DE).F (GAB).c | "8".{p}.D.E.F .G.A.B.c |]"""

def generate_full_tonic_abc(tonic):
    abc_parts = []
    t_id = tonic["id"]
    t_name = tonic["name"]

    for m in MODES_PARALLEL:
        m_num = m["num"]
        m_name = m["name"]
        m_char = m["char"]
        m_formula = m["formula"]
        is_maj = m["is_major_family"]
        key_sig = tonic["major_key"] if is_maj else tonic["minor_key"]
        acc_dict = {}
        if m["acc_key"]:
            acc_dict = tonic.get(f"{m['acc_key']}_acc", {})
        
        notes_with_acc = apply_accidentals_to_notes(tonic["base_notes"], acc_dict)
        c1, c2, c3, c4, c5, c6, c7, c8 = generate_mode_measures(notes_with_acc)

        header = f"""X:{m_num}
T:Modo {m_num}: {t_name} {m_name}
% Familia {m["family"]} | Carácter: {m_char} | Fórmula: {m_formula}
%%barsperstaff 2
M:4/2
L:1/8
Q:1/2=90
K:{key_sig}
V:1 clef=treble
%%score 1
{c1} | {c2} |
{c3} | {c4} |
{c5} | {c6} |
{c7} | {c8} |]"""
        abc_parts.append(header)

    return "\n\n".join(abc_parts)

print("Setup completed successfully.")

def generate_tonic_html(tonic):
    t_name = tonic["title_note"]
    p_note = tonic["prep_note"]
    maj_key = tonic["major_key"]
    min_key = tonic["minor_key"]
    maj_desc = tonic["major_desc"]
    min_desc = tonic["minor_desc"]

    # Preparatory ABC
    prep_abc = f"""X:0
M:4/2
L:1/8
Q:1/2=90
K:{maj_key}
V:1 clef=treble
%%score 1
%%barsperstaff 8
%%stem down
"1"({p_note}DEF GABc) | "2"({p_note}DEF) (GABc) | "3"({p_note}D).E.F (GA).B.c | "4".{p_note}(DE).F .G(AB).c | "5".{p_note}.D(EF) .G.A(Bc) | "6".{p_note}(DEF) .G(ABc) | "7"({p_note}DE).F (GAB).c | "8".{p_note}.D.E.F .G.A.B.c |]"""

    # Generate 7 modes ABC strings
    modes_abcs = {}
    for m in MODES_PARALLEL:
        m_num = m["num"]
        is_maj = m["is_major_family"]
        key_sig = maj_key if is_maj else min_key
        acc_dict = {}
        if m["acc_key"]:
            acc_dict = tonic.get(f"{m['acc_key']}_acc", {})
        
        notes_with_acc = apply_accidentals_to_notes(tonic["base_notes"], acc_dict)
        c1, c2, c3, c4, c5, c6, c7, c8 = generate_mode_measures(notes_with_acc)

        if m_num == 5:
            # Split mode 5 into two halves
            modes_abcs["5_part1"] = f"""X:51
%%barsperstaff 2
M:4/2
L:1/8
Q:1/2=90
K:{key_sig}
V:1 clef=treble
%%score 1
{c1} | {c2} |
{c3} | {c4} |"""

            modes_abcs["5_part2"] = f"""X:52
%%barsperstaff 2
M:4/2
L:1/8
Q:1/2=90
K:{key_sig}
V:1 clef=treble
%%score 1
{c5} | {c6} |
{c7} | {c8} |]"""
        else:
            modes_abcs[str(m_num)] = f"""X:{m_num}
%%barsperstaff 2
M:4/2
L:1/8
Q:1/2=90
K:{key_sig}
V:1 clef=treble
%%score 1
{c1} | {c2} |
{c3} | {c4} |
{c5} | {c6} |
{c7} | {c8} |]"""

    notes_desc = tonic["notes_desc"]

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<title>Estudio Didáctico de Modos Paralelos: {t_name}</title>
<script src="./abcjs-basic-min.js"></script>
<style>
  @page {{
    size: A4 portrait;
    margin: 8mm 10mm 8mm 10mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: "Palatino", "Georgia", "Times New Roman", serif;
    color: #000000;
    margin: 0;
    padding: 0;
    background: #ffffff;
    -webkit-print-color-adjust: exact;
  }}
  .sheet-page {{
    width: 190mm;
    height: 280mm;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 2px;
    box-sizing: border-box;
  }}
  .sheet-page:last-child {{
    page-break-after: avoid;
  }}
  
  /* Encabezados */
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 1.5px solid #000000;
    padding-bottom: 2px;
    margin-bottom: 3px;
  }}
  .title-area h1 {{
    font-size: 16pt;
    font-weight: bold;
    margin: 0 0 1px 0;
    letter-spacing: -0.2px;
  }}
  .title-area p {{
    font-size: 7.5pt;
    font-style: italic;
    color: #333333;
    margin: 0;
  }}
  .author-area {{
    text-align: right;
  }}
  .author-area .orig {{
    font-size: 8pt;
    font-weight: bold;
    margin: 0;
  }}
  .author-area .arr {{
    font-size: 7.5pt;
    font-weight: 600;
    color: #000000;
    margin: 1px 0 0 0;
  }}
  .running-header {{
    display: flex;
    justify-content: space-between;
    font-size: 7.5pt;
    font-style: italic;
    color: #444444;
    border-bottom: 0.8px solid #aaaaaa;
    padding-bottom: 2px;
    margin-bottom: 3px;
  }}

  /* Bloques de modo */
  .mode-block {{
    margin-bottom: 1px;
  }}
  .mode-banner {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f1f2f4;
    padding: 2.5px 7px;
    border-radius: 3.5px;
    margin-bottom: 1px;
  }}
  .mode-title {{
    font-size: 8.8pt;
    font-weight: bold;
    color: #000000;
  }}
  .mode-char {{
    font-size: 7.5pt;
    font-style: italic;
    color: #444444;
    margin-left: 6px;
    font-weight: normal;
  }}
  .badges-group {{
    display: flex;
    gap: 4.5px;
  }}
  .badge {{
    background: #e2e4e8;
    color: #111111;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 6.8pt;
    font-weight: 500;
    padding: 1.5px 5.5px;
    border-radius: 3px;
    border: 0.5px solid #d0d2d7;
  }}
  .badge-acc {{
    background: #e8e6df;
    color: #222222;
    border: 0.5px solid #d4d0c5;
    font-weight: 600;
  }}

  /* Variantes de articulación preparatoria */
  .prep-container {{
    background: #f8f9fa;
    border: 0.8px solid #e0e2e5;
    border-radius: 4px;
    padding: 3px 6px 1px 6px;
    margin-bottom: 3px;
  }}
  .prep-header {{
    display: flex;
    justify-content: space-between;
    font-size: 7pt;
    font-weight: bold;
    color: #222222;
    margin-bottom: 0px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }}
  .prep-subtitle {{
    font-size: 6.8pt;
    font-style: italic;
    color: #555555;
    font-weight: normal;
  }}
  .score-box {{
    width: 100%;
  }}
</style>
</head>
<body>

  <!-- ================= PÁGINA 1 (9 Sistemas) ================= -->
  <div class="sheet-page">
    <div class="header">
      <div class="title-area">
        <h1>Estudio Didáctico de Modos Paralelos: {t_name}</h1>
        <p>Sistema Paralelo del Maestro León Giraldo · Basado en P. Taffanel &amp; Ph. Gaubert (E.J. 4)</p>
      </div>
      <div class="author-area">
        <p class="orig">Pedagogía: Maestro León Giraldo</p>
        <p class="arr">Arreglos y edición: Sebastián Gómez</p>
      </div>
    </div>

    <!-- Articulaciones Preparatorias (1 sistema) -->
    <div class="prep-container">
      <div class="prep-header">
        <span>Variantes de Articulación Preparatorias</span>
        <span class="prep-subtitle">Trabajar sucesivamente con cada una de las siguientes articulaciones:</span>
      </div>
      <div id="prep-score" class="score-box"></div>
    </div>

    <!-- MODO 1: JÓNICO (4 sistemas) -->
    <div class="mode-block">
      <div class="mode-banner">
        <div>
          <span class="mode-title">Modo 1: {t_name} Jónico (Mayor)</span>
          <span class="mode-char">— Brillante y luminoso</span>
        </div>
        <div class="badges-group">
          <span class="badge">Fórmula: 1 - 2 - 3 - 4 - 5 - 6 - 7</span>
          <span class="badge">Armadura fija: {maj_desc}</span>
        </div>
      </div>
      <div id="mode1-score" class="score-box"></div>
    </div>

    <!-- MODO 2: LIDIO (4 sistemas) -->
    <div class="mode-block">
      <div class="mode-banner">
        <div>
          <span class="mode-title">Modo 2: {t_name} Lidio</span>
          <span class="mode-char">— Etéreo y soñador</span>
        </div>
        <div class="badges-group">
          <span class="badge">Fórmula: 1 - 2 - 3 - ♯4 - 5 - 6 - 7</span>
          <span class="badge badge-acc">{notes_desc["lyd"]}</span>
          <span class="badge">Armadura fija: {maj_desc}</span>
        </div>
      </div>
      <div id="mode2-score" class="score-box"></div>
    </div>
  </div>

  <!-- ================= PÁGINA 2 (10 Sistemas) ================= -->
  <div class="sheet-page">
    <div class="running-header">
      <span>Estudio Didáctico de Modos Paralelos: {t_name} · Maestro León Giraldo</span>
      <span>Arreglos: Sebastián Gómez</span>
    </div>

    <!-- MODO 3: MIXOLIDIO (4 sistemas) -->
    <div class="mode-block">
      <div class="mode-banner">
        <div>
          <span class="mode-title">Modo 3: {t_name} Mixolidio</span>
          <span class="mode-char">— Festivo y folclórico</span>
        </div>
        <div class="badges-group">
          <span class="badge">Fórmula: 1 - 2 - 3 - 4 - 5 - 6 - ♭7</span>
          <span class="badge badge-acc">{notes_desc["mix"]}</span>
          <span class="badge">Armadura fija: {maj_desc}</span>
        </div>
      </div>
      <div id="mode3-score" class="score-box"></div>
    </div>

    <!-- MODO 4: DÓRICO (4 sistemas) -->
    <div class="mode-block">
      <div class="mode-banner">
        <div>
          <span class="mode-title">Modo 4: {t_name} Dórico</span>
          <span class="mode-char">— Melancólico y noble</span>
        </div>
        <div class="badges-group">
          <span class="badge">Fórmula: 1 - 2 - ♭3 - 4 - 5 - 6 - ♭7</span>
          <span class="badge badge-acc">{notes_desc["dor"]}</span>
          <span class="badge">Armadura fija: {min_desc}</span>
        </div>
      </div>
      <div id="mode4-score" class="score-box"></div>
    </div>

    <!-- MODO 5: EÓLICO (Parte 1: cc. 1-4) (2 sistemas) -->
    <div class="mode-block">
      <div class="mode-banner">
        <div>
          <span class="mode-title">Modo 5: {t_name} Eólico (Menor Natural)</span>
          <span class="mode-char">— Triste e introspectivo</span>
        </div>
        <div class="badges-group">
          <span class="badge">Fórmula: 1 - 2 - ♭3 - 4 - 5 - ♭6 - ♭7</span>
          <span class="badge">Armadura fija: {min_desc}</span>
        </div>
      </div>
      <div id="mode5-p1-score" class="score-box"></div>
    </div>
  </div>

  <!-- ================= PÁGINA 3 (10 Sistemas) ================= -->
  <div class="sheet-page">
    <div class="running-header">
      <span>Estudio Didáctico de Modos Paralelos: {t_name} · Maestro León Giraldo</span>
      <span>Arreglos: Sebastián Gómez</span>
    </div>

    <!-- MODO 5: EÓLICO (Parte 2: cc. 5-8) (2 sistemas) -->
    <div class="mode-block">
      <div class="mode-banner">
        <div>
          <span class="mode-title">Modo 5: {t_name} Eólico (Continuación: cc. 5 a 8)</span>
        </div>
        <div class="badges-group">
          <span class="badge">Resolución a tónica</span>
        </div>
      </div>
      <div id="mode5-p2-score" class="score-box"></div>
    </div>

    <!-- MODO 6: FRIGIO (4 sistemas) -->
    <div class="mode-block">
      <div class="mode-banner">
        <div>
          <span class="mode-title">Modo 6: {t_name} Frigio</span>
          <span class="mode-char">— Oscuro y exótico</span>
        </div>
        <div class="badges-group">
          <span class="badge">Fórmula: 1 - ♭2 - ♭3 - 4 - 5 - ♭6 - ♭7</span>
          <span class="badge badge-acc">{notes_desc["phr"]}</span>
          <span class="badge">Armadura fija: {min_desc}</span>
        </div>
      </div>
      <div id="mode6-score" class="score-box"></div>
    </div>

    <!-- MODO 7: LÓCRIO (4 sistemas) -->
    <div class="mode-block">
      <div class="mode-banner">
        <div>
          <span class="mode-title">Modo 7: {t_name} Lócrio</span>
          <span class="mode-char">— Inestable y tenso</span>
        </div>
        <div class="badges-group">
          <span class="badge">Fórmula: 1 - ♭2 - ♭3 - 4 - ♭5 - ♭6 - ♭7</span>
          <span class="badge badge-acc">{notes_desc["loc"]}</span>
          <span class="badge">Armadura fija: {min_desc}</span>
        </div>
      </div>
      <div id="mode7-score" class="score-box"></div>
    </div>
  </div>

<script>
  const commonOptions = {{
    staffwidth: 715,
    paddingtop: 0,
    paddingbottom: 0,
    paddingleft: 0,
    paddingright: 0,
    scale: 0.84
  }};

  const prepABC = `{prep_abc}`;
  const m1ABC = `{modes_abcs["1"]}`;
  const m2ABC = `{modes_abcs["2"]}`;
  const m3ABC = `{modes_abcs["3"]}`;
  const m4ABC = `{modes_abcs["4"]}`;
  const m5P1ABC = `{modes_abcs["5_part1"]}`;
  const m5P2ABC = `{modes_abcs["5_part2"]}`;
  const m6ABC = `{modes_abcs["6"]}`;
  const m7ABC = `{modes_abcs["7"]}`;

  ABCJS.renderAbc("prep-score", prepABC, commonOptions);
  ABCJS.renderAbc("mode1-score", m1ABC, commonOptions);
  ABCJS.renderAbc("mode2-score", m2ABC, commonOptions);
  ABCJS.renderAbc("mode3-score", m3ABC, commonOptions);
  ABCJS.renderAbc("mode4-score", m4ABC, commonOptions);
  ABCJS.renderAbc("mode5-p1-score", m5P1ABC, commonOptions);
  ABCJS.renderAbc("mode5-p2-score", m5P2ABC, commonOptions);
  ABCJS.renderAbc("mode6-score", m6ABC, commonOptions);
  ABCJS.renderAbc("mode7-score", m7ABC, commonOptions);
</script>
</body>
</html>"""
    return html

# Batch execution function
def run_batch():
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    artifact_dir = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"
    compiled_pdfs = []

    for t in TONICS:
        t_id = t["id"]
        abc_str = generate_full_tonic_abc(t)
        abc_file = f"modos_{t_id}.abc"
        with open(abc_file, "w") as f:
            f.write(abc_str)
        print(f"Generated {abc_file}")

        html_str = generate_tonic_html(t)
        html_file = f"modos_{t_id}.html"
        with open(html_file, "w") as f:
            f.write(html_str)
        print(f"Generated {html_file}")

        pdf_file = f"modos_{t_id}.pdf"
        abs_html = os.path.abspath(html_file)
        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_file}",
            f"file://{abs_html}"
        ]
        subprocess.run(cmd, check=True)
        print(f"Compiled {pdf_file}")
        compiled_pdfs.append(pdf_file)

    # Merge into Master PDF
    master_pdf_name = "metodo_completo_modos_flauta.pdf"
    master_doc = fitz.open()
    for p in compiled_pdfs:
        doc = fitz.open(p)
        master_doc.insert_pdf(doc)
    master_doc.save(master_pdf_name)
    print(f"=== Master PDF generated: {master_pdf_name} with {len(master_doc)} pages! ===")

    # Copy deliverables to artifacts
    for p in compiled_pdfs:
        shutil.copy(p, os.path.join(artifact_dir, p))
        abc_name = p.replace(".pdf", ".abc")
        shutil.copy(abc_name, os.path.join(artifact_dir, abc_name))
    shutil.copy(master_pdf_name, os.path.join(artifact_dir, master_pdf_name))
    print("All deliverables copied to artifacts directory.")

if __name__ == "__main__":
    run_batch()
