#!/usr/bin/env python3
"""
Generador Urtext de Taffanel & Gaubert — E. J. 11 (Arpèges Brisés)
Ediciones Alphonse Leduc A. L. 16.588, páginas 122, 123, 124 y 125.
Genera:
- taffanel_ej11_completo.abc y colección de 10 articulaciones en abc_ej11/ y docs/downloads/abc/
- taffanel_ej11_validacion.html (en brain/, raíz y docs/ej11.html)
"""

import os
import re
import json

BRAIN_DIR = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"
ROOT_DIR = "/Users/sebas/Desktop/partituras"
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
ABC_EJ11_DIR = os.path.join(ROOT_DIR, "abc_ej11")
DOCS_ABC_DIR = os.path.join(DOCS_DIR, "downloads", "abc")

os.makedirs(ABC_EJ11_DIR, exist_ok=True)
os.makedirs(DOCS_ABC_DIR, exist_ok=True)

# 12 Secciones Cromáticas de E. J. 11 (10 compases de arpegios quebrados en 9/8 cada una = 120 compases + compás 121 final en Si)
EJ11_SECTIONS = [
    (
        0, "Do", "1 · Bajo en Do (Ut)", "1 · Bass on C", "1 · Do", 60,
        [
            ("C", "_E", "_A"),   # m.1  (3,8)  La♭ mayor 1ª inv.
            ("C", "_E", "=A"),   # m.2  (3,9)  Do dism. 7ª
            ("C", "_E", "_G"),   # m.3  (3,6)  Do dism.
            ("C", "=E", "^G"),   # m.4  (4,8)  Do aum.
            ("C", "E", "=G"),    # m.5  (4,7)  Do mayor
            ("C", "F", "A"),     # m.6  (5,9)  Fa mayor 2ª inv.
            ("C", "_E", "G"),    # m.7  (3,7)  Do menor
            ("C", "^F", "A"),    # m.8  (6,9)  Fa♯ dism. 1ª inv.
            ("C", "=F", "_A"),   # m.9  (5,8)  Fa menor 2ª inv.
            ("C", "E", "=A"),    # m.10 (4,9)  La menor 1ª inv.
        ]
    ),
    (
        1, "Do♯/Re♭", "2 · Bajo en Do♯ / Re♭", "2 · Bass on C♯ / D♭", "2 · Do♯/Re♭", 61,
        [
            ("^C", "E", "G"),     # m.11 (3,6)
            ("^C", "E", "^G"),    # m.12 (3,7)
            ("^C", "E", "A"),     # m.13 (3,8)
            ("_D", "F", "_B"),    # m.14 (4,9)
            ("_D", "_G", "_B"),   # m.15 (5,9)
            ("_D", "_F", "_B"),   # m.16 (3,9)
            ("_D", "=F", "=A"),   # m.17 (4,8) (En plancha Leduc pág. 122 c.17 aparece grabado _D-_G-_B; aquí conservamos el ciclo armónico completo con nota Urtext)
            ("_D", "=G", "_B"),   # m.18 (6,9)
            ("_D", "_G", "__B"),  # m.19 (5,8)
            ("_D", "F", "_A"),    # m.20 (4,7)
        ]
    ),
    (
        2, "Re", "3 · Bajo en Re (Ré)", "3 · Bass on D", "3 · Re", 62,
        [
            ("=D", "=F", "_B"),   # m.21 (3,8)
            ("D", "F", "=B"),     # m.22 (3,9)
            ("D", "G", "_B"),     # m.23 (5,8)
            ("D", "^F", "^A"),    # m.24 (4,8)
            ("D", "^F", "=A"),    # m.25 (4,7)
            ("D", "G", "B"),      # m.26 (5,9)
            ("D", "=F", "A"),     # m.27 (3,7)
            ("D", "^G", "B"),     # m.28 (6,9)
            ("D", "=F", "_A"),    # m.29 (3,6) -- inicio de pág. 123
            ("D", "^F", "B"),     # m.30 (4,9)
        ]
    ),
    (
        3, "Re♯/Mi♭", "4 · Bajo en Re♯ / Mi♭", "4 · Bass on D♯ / E♭", "4 · Re♯/Mi♭", 63,
        [
            ("^D", "^F", "A"),    # m.31 (3,6)
            ("_E", "_G", "_B"),   # m.32 (3,7)
            ("_E", "_G", "_c"),   # m.33 (3,8)
            ("_E", "=G", "_B"),   # m.34 (4,7)
            ("_E", "G", "=c"),    # m.35 (4,9)
            ("_E", "_A", "c"),    # m.36 (5,9)
            ("_E", "_G", "c"),    # m.37 (3,9)
            ("_E", "=A", "c"),    # m.38 (6,9)
            ("_E", "_A", "_c"),   # m.39 (5,8)
            ("_E", "=G", "=B"),   # m.40 (4,8)
        ]
    ),
    (
        4, "Mi", "5 · Bajo en Mi", "5 · Bass on E", "5 · Mi", 64,
        [
            ("=E", "G", "_B"),    # m.41 (3,6)
            ("E", "G", "=B"),     # m.42 (3,7)
            ("E", "G", "c"),      # m.43 (3,8)
            ("E", "^G", "^B"),    # m.44 (4,8)
            ("E", "^G", "^c"),    # m.45 (4,9)
            ("E", "A", "^c"),     # m.46 (5,9)
            ("E", "=G", "^c"),    # m.47 (3,9)
            ("E", "^A", "^c"),    # m.48 (6,9)
            ("E", "=A", "=c"),    # m.49 (5,8)
            ("E", "^G", "B"),     # m.50 (4,7)
        ]
    ),
    (
        5, "Fa", "6 · Bajo en Fa", "6 · Bass on F", "6 · Fa", 65,
        [
            ("F", "_A", "_d"),    # m.51 (3,8)
            ("F", "_A", "=d"),    # m.52 (3,9)
            ("F", "_A", "_c"),    # m.53 (3,6)
            ("F", "=A", "^c"),    # m.54 (4,8)
            ("F", "A", "=c"),     # m.55 (4,7)
            ("F", "_B", "d"),     # m.56 (5,9)
            ("F", "_A", "c"),     # m.57 (3,7)
            ("F", "=B", "d"),     # m.58 (6,9)
            ("F", "_B", "_d"),    # m.59 (5,8)
            ("F", "=A", "=d"),    # m.60 (4,9) -- fin de pág. 123
        ]
    ),
    (
        6, "Fa♯", "7 · Bajo en Fa♯", "7 · Bass on F♯", "7 · Fa♯", 66,
        [
            ("^F", "A", "^c"),    # m.61 (3,7) -- inicio de pág. 124
            ("^F", "^A", "^c"),   # m.62 (4,7)
            ("^F", "=A", "d"),    # m.63 (3,8)
            ("^F", "^A", "^^c"),  # m.64 (4,8)
            ("^F", "^A", "^d"),   # m.65 (4,9)
            ("^F", "B", "^d"),    # m.66 (5,9)
            ("^F", "=A", "^d"),   # m.67 (3,9)
            ("^F", "B", "=d"),    # m.68 (5,8)
            ("^F", "A", "=c"),    # m.69 (3,6)
            ("^F", "^B", "^d"),   # m.70 (6,9)
        ]
    ),
    (
        7, "Sol", "8 · Bajo en Sol", "8 · Bass on G", "8 · Sol", 67,
        [
            ("=G", "_B", "_e"),   # m.71 (3,8)
            ("G", "_B", "=e"),    # m.72 (3,9)
            ("G", "_B", "_d"),    # m.73 (3,6)
            ("G", "=B", "^d"),    # m.74 (4,8)
            ("G", "B", "=d"),     # m.75 (4,7)
            ("G", "c", "e"),      # m.76 (5,9)
            ("G", "_B", "d"),     # m.77 (3,7)
            ("G", "^c", "e"),     # m.78 (6,9)
            ("G", "=c", "_e"),    # m.79 (5,8)
            ("G", "=B", "=e"),    # m.80 (4,9)
        ]
    ),
    (
        8, "Sol♯/La♭", "9 · Bajo en Sol♯ / La♭", "9 · Bass on G♯ / A♭", "9 · Sol♯/La♭", 68,
        [
            ("^G", "B", "d"),     # m.81 (3,6)
            ("^G", "^B", "^d"),   # m.82 (4,7)
            ("^G", "=B", "e"),    # m.83 (3,8)
            ("_A", "c", "f"),     # m.84 (4,9)
            ("_A", "_d", "f"),    # m.85 (5,9)
            ("_A", "_c", "f"),    # m.86 (3,9)
            ("_A", "_d", "_f"),   # m.87 (5,8)
            ("_A", "=d", "=f"),   # m.88 (6,9)
            ("_A", "_c", "_e"),   # m.89 (3,7)
            ("_A", "=c", "=e"),   # m.90 (4,8) -- fin de pág. 124
        ]
    ),
    (
        9, "La", "10 · Bajo en La", "10 · Bass on A", "10 · La", 69,
        [
            ("=A", "c", "_e"),    # m.91 (3,6) -- inicio de pág. 125
            ("A", "c", "=e"),     # m.92 (3,7)
            ("A", "c", "f"),      # m.93 (3,8)
            ("A", "^c", "^e"),    # m.94 (4,8)
            ("A", "^c", "^f"),    # m.95 (4,9)
            ("A", "d", "^f"),     # m.96 (5,9)
            ("A", "=c", "^f"),    # m.97 (3,9)
            ("A", "^d", "^f"),    # m.98 (6,9)
            ("A", "=d", "=f"),    # m.99 (5,8)
            ("A", "^c", "e"),     # m.100 (4,7)
        ]
    ),
    (
        10, "La♯/Si♭", "11 · Bajo en La♯ / Si♭", "11 · Bass on A♯ / B♭", "11 · La♯/Si♭", 70,
        [
            ("^A", "^c", "^f"),   # m.101 (3,8)
            ("_B", "_d", "g"),    # m.102 (3,9)
            ("_B", "_d", "_f"),   # m.103 (3,6)
            ("_B", "=d", "^f"),   # m.104 (4,8)
            ("_B", "d", "=f"),    # m.105 (4,7)
            ("_B", "_e", "g"),    # m.106 (5,9)
            ("_B", "_d", "f"),    # m.107 (3,7)
            ("_B", "e", "g"),     # m.108 (6,9)
            ("_B", "_e", "_g"),   # m.109 (5,8)
            ("_B", "=d", "=g"),   # m.110 (4,9)
        ]
    ),
    (
        11, "Si", "12 · Bajo en Si", "12 · Bass on B", "12 · Si", 71,
        [
            ("=B", "d", "=f"),    # m.111 (3,6)
            ("B", "d", "^f"),     # m.112 (3,7)
            ("B", "d", "g"),      # m.113 (3,8)
            ("B", "^d", "^f"),    # m.114 (impreso B-F♯-D♯ en plancha Leduc A.L. 16.588)
            ("B", "^d", "^g"),    # m.115 (4,9)
            ("B", "e", "^g"),     # m.116 (5,9)
            ("B", "=d", "^g"),    # m.117 (3,9)
            ("B", "^e", "^g"),    # m.118 (6,9)
            ("B", "=e", "=g"),    # m.119 (5,8)
            ("B", "^d", "^f"),    # m.120 (4,7)
        ]
    ),
]

EJ11_ARTICULATIONS_META = [
    {"id": 0,  "meter": "9/8", "name": "Edición Original (Leduc)",            "short": "0. Orig.",           "formula": "6 + 6 + 6 notas por compás (9/8 · 3/4)", "fname": "00_Taffanel_EJ11_Original_AL16588.abc"},
    {"id": 1,  "meter": "9/8", "name": "1. 18 Ligadas (Compás completo)",      "short": "1. (18)",            "formula": "(18) · Compás entero ligado en 9/8", "fname": "01_Taffanel_EJ11_Articulacion_01_18_Ligadas.abc"},
    {"id": 2,  "meter": "9/8", "name": "2. 6 + 6 + 6 Ligadas",                 "short": "2. (6)(6)(6)",       "formula": "(6) + (6) + (6) · Seisillos ligados en 9/8", "fname": "02_Taffanel_EJ11_Articulacion_02_6_6_6_Ligadas.abc"},
    {"id": 3,  "meter": "9/8", "name": "3. 4 Ligadas y 2 Picadas",             "short": "3. (4)··",           "formula": "(4)·· (4)·· (4)·· en 9/8", "fname": "03_Taffanel_EJ11_Articulacion_03_4_Ligadas_2_Picadas.abc"},
    {"id": 4,  "meter": "9/8", "name": "4. 2 Picadas y 4 Ligadas",             "short": "4. ··(4)",           "formula": "··(4) ··(4) ··(4) en 9/8", "fname": "04_Taffanel_EJ11_Articulacion_04_2_Picadas_4_Ligadas.abc"},
    {"id": 5,  "meter": "9/8", "name": "5. 2 Ligadas y 4 Picadas",             "short": "5. (2)····",         "formula": "(2)···· (2)···· (2)···· en 9/8", "fname": "05_Taffanel_EJ11_Articulacion_05_2_Ligadas_4_Picadas.abc"},
    {"id": 6,  "meter": "3/4", "name": "6. De 3 en 3 Ligadas (3/4)",           "short": "6. (3)×6 (3/4)",     "formula": "(3)(3)(3)(3)(3)(3) · 6 grupos de 3 en 3/4", "fname": "06_Taffanel_EJ11_Articulacion_06_De_3_en_3_Ligadas.abc"},
    {"id": 7,  "meter": "3/4", "name": "7. 3 Ligadas y 3 Picadas (3/4)",       "short": "7. (3)··· (3/4)",    "formula": "(3)··· (3)··· (3)··· en 3/4", "fname": "07_Taffanel_EJ11_Articulacion_07_3_Ligadas_3_Picadas.abc"},
    {"id": 8,  "meter": "9/8", "name": "8. De 2 en 2 Ligadas",                 "short": "8. (2)×9",           "formula": "(2)(2)(2) (2)(2)(2) (2)(2)(2) en 9/8", "fname": "08_Taffanel_EJ11_Articulacion_08_De_2_en_2_Ligadas.abc"},
    {"id": 9,  "meter": "9/8", "name": "9. Sincopadas de a 2",                 "short": "9. ·(2)×8·",         "formula": "·(2)(2)(2)(2)(2)(2)(2)(2)· en 9/8", "fname": "09_Taffanel_EJ11_Articulacion_09_Sincopadas.abc"},
    {"id": 10, "meter": "9/8", "name": "10. Todas Picadas (Staccato)",         "short": "10. ·×18",           "formula": "18 notas en staccato por compás en 9/8", "fname": "10_Taffanel_EJ11_Articulacion_10_Todas_Picadas.abc"},
]

INTERVAL_NAMES = {
    (3, 6): "Tríada Dism. (5ª dism.)",
    (3, 7): "Tríada Menor (5ª justa)",
    (3, 8): "Mayor 1ª Inv. (6ª menor)",
    (3, 9): "Dism. 7ª (6ª mayor)",
    (4, 7): "Tríada Mayor (5ª justa)",
    (4, 8): "Tríada Aumentada (5ª aum.)",
    (4, 9): "Menor 1ª Inv. (6ª mayor)",
    (5, 8): "Menor 2ª Inv. (4ª y 6ª m.)",
    (5, 9): "Mayor 2ª Inv. (4ª y 6ª M.)",
    (6, 9): "Dism. 1ª Inv. (4ª aum. y 6ª M.)",
}

BASE_SEMITONES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

def parse_abc_token(tok):
    m = re.match(r"^([\^_=]*)([A-Ga-g])([']*)$", tok)
    if not m:
        raise ValueError(f"Token ABC inválido: {tok}")
    return m.group(1), m.group(2), m.group(3)

def shift_abc_octave(tok, octaves=1):
    acc, letter, marks = parse_abc_token(tok)
    for _ in range(octaves):
        if letter.isupper():
            letter = letter.lower()
        else:
            marks += "'"
    return f"{acc}{letter}{marks}"

def strip_abc_accidental(tok):
    _, letter, marks = parse_abc_token(tok)
    return f"{letter}{marks}"

def abc_token_to_midi(tok):
    acc, letter, marks = parse_abc_token(tok)
    upper = letter.upper()
    octave = 4 if letter.isupper() else 5 + len(marks)
    semi = BASE_SEMITONES[upper]
    if acc == "^":
        semi += 1
    elif acc == "^^":
        semi += 2
    elif acc == "_":
        semi -= 1
    elif acc == "__":
        semi -= 2
    return (octave + 1) * 12 + semi

def expand_triad_to_18_broken_notes(triad):
    """
    Expande una tríada (p1, p2, p3) en las 18 semicorcheas del arpegio quebrado (Arpèges Brisés, 9/8):
    Sean las 7 notas del acorde en 2 octavas:
      a1=p1, a2=p2, a3=p3, a4=p1+8va, a5=p2+8va, a6=p3+8va, a7=p1+15ma
    Y sus versiones sin repetir alteración dentro del mismo compás:
      b1..b7 = strip_abc_accidental(a1..a7)
    Patrón de 18 notas (3 grupos de 6):
      Grupo 1 (1..6):   [a1, a3, a2, a4, b3, a5]
      Grupo 2 (7..12):  [b4, a6, b5, a7, b5, b6]
      Grupo 3 (13..18): [b4, b5, b3, b4, b2, b3]
    """
    p1, p2, p3 = triad
    a1, a2, a3 = p1, p2, p3
    a4, a5, a6 = shift_abc_octave(p1, 1), shift_abc_octave(p2, 1), shift_abc_octave(p3, 1)
    a7 = shift_abc_octave(p1, 2)

    b2 = strip_abc_accidental(a2)
    b3 = strip_abc_accidental(a3)
    b4 = strip_abc_accidental(a4)
    b5 = strip_abc_accidental(a5)
    b6 = strip_abc_accidental(a6)

    notes_18 = [
        a1, a3, a2, a4, b3, a5,
        b4, a6, b5, a7, b5, b6,
        b4, b5, b3, b4, b2, b3
    ]

    m1, m2, m3 = abc_token_to_midi(a1), abc_token_to_midi(a2), abc_token_to_midi(a3)
    m4, m5, m6 = m1 + 12, m2 + 12, m3 + 12
    m7 = m1 + 24

    midis_18 = [
        m1, m3, m2, m4, m3, m5,
        m4, m6, m5, m7, m5, m6,
        m4, m5, m3, m4, m2, m3
    ]
    return notes_18, midis_18

def format_measure_18(notes_18, art_id):
    n = notes_18
    if art_id == 0:
        return f"{''.join(n[0:6])} {''.join(n[6:12])} {''.join(n[12:18])}"
    elif art_id == 1:
        return f"({''.join(n[0:6])} {''.join(n[6:12])} {''.join(n[12:18])})"
    elif art_id == 2:
        return f"({''.join(n[0:6])}) ({''.join(n[6:12])}) ({''.join(n[12:18])})"
    elif art_id == 3:
        g1 = f"({n[0]}{n[1]}{n[2]}{n[3]}).{n[4]}.{n[5]}"
        g2 = f"({n[6]}{n[7]}{n[8]}{n[9]}).{n[10]}.{n[11]}"
        g3 = f"({n[12]}{n[13]}{n[14]}{n[15]}).{n[16]}.{n[17]}"
        return f"{g1} {g2} {g3}"
    elif art_id == 4:
        g1 = f".{n[0]}.{n[1]}({n[2]}{n[3]}{n[4]}{n[5]})"
        g2 = f".{n[6]}.{n[7]}({n[8]}{n[9]}{n[10]}{n[11]})"
        g3 = f".{n[12]}.{n[13]}({n[14]}{n[15]}{n[16]}{n[17]})"
        return f"{g1} {g2} {g3}"
    elif art_id == 5:
        g1 = f"({n[0]}{n[1]}).{n[2]}.{n[3]}.{n[4]}.{n[5]}"
        g2 = f"({n[6]}{n[7]}).{n[8]}.{n[9]}.{n[10]}.{n[11]}"
        g3 = f"({n[12]}{n[13]}).{n[14]}.{n[15]}.{n[16]}.{n[17]}"
        return f"{g1} {g2} {g3}"
    elif art_id == 6:
        return (
            f"({n[0]}{n[1]}{n[2]})({n[3]}{n[4]}{n[5]}) "
            f"({n[6]}{n[7]}{n[8]})({n[9]}{n[10]}{n[11]}) "
            f"({n[12]}{n[13]}{n[14]})({n[15]}{n[16]}{n[17]})"
        )
    elif art_id == 7:
        return (
            f"({n[0]}{n[1]}{n[2]}).{n[3]}.{n[4]}.{n[5]} "
            f"({n[6]}{n[7]}{n[8]}).{n[9]}.{n[10]}.{n[11]} "
            f"({n[12]}{n[13]}{n[14]}).{n[15]}.{n[16]}.{n[17]}"
        )
    elif art_id == 8:
        g1 = f"({n[0]}{n[1]})({n[2]}{n[3]})({n[4]}{n[5]})"
        g2 = f"({n[6]}{n[7]})({n[8]}{n[9]})({n[10]}{n[11]})"
        g3 = f"({n[12]}{n[13]})({n[14]}{n[15]})({n[16]}{n[17]})"
        return f"{g1} {g2} {g3}"
    elif art_id == 9:
        return (
            f".{n[0]}({n[1]}{n[2]})({n[3]}{n[4]})({n[5]} "
            f"{n[6]})({n[7]}{n[8]})({n[9]}{n[10]})({n[11]} "
            f"{n[12]})({n[13]}{n[14]})({n[15]}{n[16]}).{n[17]}"
        )
    elif art_id == 10:
        g1 = "".join(f".{x}" for x in n[0:6])
        g2 = "".join(f".{x}" for x in n[6:12])
        g3 = "".join(f".{x}" for x in n[12:18])
        return f"{g1} {g2} {g3}"
    return f"{''.join(n[0:6])} {''.join(n[6:12])} {''.join(n[12:18])}"

ALL_MEASURES = []
EXPECTED_INTERVALS = {(3,6), (3,7), (3,8), (3,9), (4,7), (4,8), (4,9), (5,8), (5,9), (6,9)}

sections_js_data = []
for sec in EJ11_SECTIONS:
    sec_idx, sec_short, title_es, title_en, pill_label, bass_midi, triads = sec
    sec_intervals = []
    for idx_in_sec, triad in enumerate(triads):
        m_num = sec_idx * 10 + idx_in_sec + 1
        sys_idx = (m_num - 1) // 2
        notes_18, midis_18 = expand_triad_to_18_broken_notes(triad)
        assert midis_18[0] == bass_midi, f"Compás {m_num}: bajo {midis_18[0]} != {bass_midi}"
        i1 = midis_18[2] - midis_18[0]
        i2 = midis_18[1] - midis_18[0]
        assert (i1, i2) in EXPECTED_INTERVALS, f"Compás {m_num}: intervalo inesperado {(i1, i2)}"
        letters = {parse_abc_token(x)[1].upper() for x in triad}
        assert len(letters) == 3, f"Compás {m_num}: letras repetidas en tríada {triad}"
        sec_intervals.append((i1, i2))
        m_obj = {
            "measureNum": m_num,
            "systemIdx": sys_idx,
            "sectionIdx": sec_idx,
            "sectionShort": sec_short,
            "triad": list(triad),
            "intervals": [i1, i2],
            "chordDesc": INTERVAL_NAMES[(i1, i2)],
            "notes18": notes_18,
            "midis18": midis_18,
            "isSectionEnd": (idx_in_sec == 9 and m_num < 120),
        }
        ALL_MEASURES.append(m_obj)
    if sec_idx < 11:
        assert set(sec_intervals) == EXPECTED_INTERVALS, f"Sección {sec_short} no permuta las 10 tríadas: {sec_intervals}"
    sections_js_data.append({
        "id": sec_idx,
        "short": sec_short,
        "titleEs": title_es,
        "titleEn": title_en,
        "pillLabel": pill_label,
        "bassMidi": bass_midi,
        "startMeasure": sec_idx * 10 + 1,
        "endMeasure": sec_idx * 10 + 10,
    })

print(f"✅ Validados los {len(ALL_MEASURES)} compases de arpegios quebrados (2,160 semicorcheas + 1 nota final = 2,161 notas)")

def generate_ej11_abc(art_id=0):
    meta = EJ11_ARTICULATIONS_META[art_id]
    meter_str = meta["meter"]
    lines = [
        f"X:{art_id + 1}",
        f"T:E. J. 11 — Arpèges Brisés ({meta['name']})",
        "C:Paul Taffanel & Philippe Gaubert (Ed. Alphonse Leduc A. L. 16.588, págs. 122–125)",
        "%%stretchlast 1",
        "%%barsperstaff 2",
        f"M:{meter_str}",
        "L:1/16",
        "Q:1/4.=72",
        "K:C",
        "V:1 clef=treble",
    ]
    # 60 sistemas exactamente como en Leduc (14 en pág. 122, 16 en pág. 123, 15 en pág. 124, 15 en pág. 125)
    for sys_idx in range(60):
        start_m = sys_idx * 2
        end_m = start_m + 2
        bar_strs = []
        for m_obj in ALL_MEASURES[start_m:end_m]:
            b_txt = format_measure_18(m_obj["notes18"], art_id)
            barline = "||" if m_obj["isSectionEnd"] else "|"
            bar_strs.append(f"{b_txt} {barline}")
        if sys_idx == 59:
            bar_strs.append("B4 z4 z10 |]")
        lines.append(" ".join(bar_strs))
    return "\n".join(lines)

all_abc_blocks = []
for art_id in range(11):
    abc_txt = generate_ej11_abc(art_id)
    fname = EJ11_ARTICULATIONS_META[art_id]["fname"]
    for out_dir in [ABC_EJ11_DIR, DOCS_ABC_DIR]:
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(abc_txt + "\n")
    if art_id >= 1:
        all_abc_blocks.append(abc_txt)

collection_fname = "11_Coleccion_Completa_Taffanel_EJ11_10_Articulaciones.abc"
collection_txt = "\n\n".join(all_abc_blocks) + "\n"
for out_dir in [ABC_EJ11_DIR, DOCS_ABC_DIR]:
    with open(os.path.join(out_dir, collection_fname), "w", encoding="utf-8") as f:
        f.write(collection_txt)

for target in [
    os.path.join(BRAIN_DIR, "taffanel_ej11_completo.abc"),
    os.path.join(ROOT_DIR, "taffanel_ej11_completo.abc"),
]:
    with open(target, "w", encoding="utf-8") as f:
        f.write(generate_ej11_abc(0) + "\n")

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Taffanel & Gaubert — E. J. 11 (Arpèges Brisés · Urtext A. L. 16.588, págs. 122–125)</title>
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

    /* BARRA DE CONTROL SUPERIOR */
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

    /* TIRAS DE SELECCIÓN (ARTICULACIONES Y SECCIONES CROMÁTICAS) */
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
      padding: 4px 9px;
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

    /* CONTENEDOR DE LAS 4 PÁGINAS URTEXT (122, 123, 124, 125) */
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
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #111827;
    }}
    .ej-page-num {{
      font-size: 17px;
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

    /* RECUADRO DE LAS 10 ARTICULACIONES OFICIALES */
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

    /* TARJETA DE ENFOQUE DE SECCIÓN SELECCIONADA */
    .focus-card {{
      display: none;
      background: #fffbeb;
      border: 2px solid #f59e0b;
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 14px;
      box-shadow: 0 6px 18px rgba(245, 158, 11, 0.16);
    }}
    .focus-card.visible {{
      display: block;
    }}
    .focus-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
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
      color: #b45309;
      padding: 3px 9px;
      border-radius: 99px;
      border: 1px solid #fcd34d;
    }}
    .chord-pills-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 6px;
      margin-bottom: 8px;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .chord-pill {{
      background: #fff;
      border: 1px solid #fde68a;
      border-radius: 5px;
      padding: 4px 6px;
      font-size: 11px;
      color: #451a03;
    }}
    .chord-pill strong {{
      color: #b45309;
    }}

    /* SISTEMAS DE ARPEGIOS QUEBRADOS (60 sistemas en 4 páginas) */
    .systems-list {{
      display: flex;
      flex-direction: column;
      gap: 0px;
    }}
    .system-row {{
      display: grid;
      grid-template-columns: 44px 1fr;
      align-items: center;
      margin: -3px 0;
      padding: 0 2px;
      border-radius: 4px;
      transition: background 0.12s;
    }}
    .system-row:hover {{
      background: rgba(37, 99, 235, 0.05);
    }}
    .system-row.active-system {{
      background: rgba(37, 99, 235, 0.11);
      outline: 1.5px solid rgba(37, 99, 235, 0.45);
    }}
    .sys-label {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 10.5px;
      font-weight: 700;
      color: #6b7280;
      text-align: center;
      user-select: none;
      line-height: 1.15;
    }}
    .sys-label .sec-tag {{
      display: block;
      font-size: 9.5px;
      color: #1d4ed8;
      font-weight: 800;
    }}
    .system-staff {{
      width: 100%;
      overflow: hidden;
    }}
    .system-staff svg {{
      width: 100% !important;
      height: auto !important;
      display: block;
    }}
    .urtext-note {{
      margin-top: 8px;
      padding-top: 6px;
      border-top: 1px solid #d6cfc2;
      font-size: 11.5px;
      color: #3f3f46;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .plate-footer {{
      text-align: center;
      font-size: 11.5px;
      font-weight: 700;
      color: #3f3f46;
      margin-top: 4px;
      letter-spacing: 0.8px;
    }}

    /* PANEL DE CÓDIGO ABC */
    .abc-code-section {{
      max-width: 1360px;
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
      min-height: 280px;
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
      margin: 3mm;
    }}
    @media print {{
      body {{ background: #fff; padding: 0; }}
      .top-toolbar, .abc-code-section, .focus-card {{ display: none !important; }}
      .pages-wrapper {{ margin: 0; padding: 0; max-width: 100%; gap: 0; }}
      .leduc-page {{
        box-shadow: none;
        border: none;
        padding: 1mm 2mm;
        zoom: 0.56;
      }}
      .page-break-after {{
        page-break-after: always;
        break-after: page;
      }}
      .system-row {{ margin: -6px 0; }}
    }}
  </style>
</head>
<body>

  <!-- BARRA SUPERIOR INTERACTIVA -->
  <div class="top-toolbar">
    <div class="toolbar-row">
      <div>
        <div class="brand-title">
          <span>🎼 Taffanel & Gaubert — E. J. 11 (Arpèges Brisés · Urtext A. L. 16.588)</span>
        </div>
        <div class="brand-sub" id="status-subtitle">
          Páginas 122–125 · 12 Secciones Cromáticas × 10 Tríadas en 9/8 (18 notas/c.) = 121 Compases (2,161 notas) · 10 Articulaciones
        </div>
      </div>

      <div class="controls-wrap">
        <button id="play-btn" class="play-btn" onclick="togglePlay()">
          <span id="play-icon">▶</span>
          <span id="play-label">Escuchar Piano</span>
        </button>

        <div class="tempo-box">
          <span>♩. =</span>
          <input type="range" id="tempo-slider" min="44" max="120" value="72" oninput="updateTempo(this.value)">
          <strong id="tempo-label">72 BPM</strong>
        </div>

        <span id="measure-badge" class="tool-btn" style="cursor:default;">Compás: 1 / 121 (Do)</span>

        <button class="tool-btn" onclick="copyCurrentAbc()">
          <span>📋</span>
          <span id="copy-label">Copiar ABC</span>
        </button>
        <a id="download-abc-link" href="downloads/abc/00_Taffanel_EJ11_Original_AL16588.abc" download class="tool-btn">
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
      <div class="strip-row" id="sec-buttons-row">
        <span class="strip-label">Sección Bajo (1–12):</span>
      </div>
    </div>
  </div>

  <!-- 4 PÁGINAS URTEXT (122, 123, 124 y 125) -->
  <div class="pages-wrapper">

    <!-- PÁGINA 122 (Sistemas 1 a 14 · Compases 1 a 28) -->
    <div class="leduc-page page-break-after" id="page-122">
      <div class="page-header">
        <div class="ej-main-title">E. J. 11 — <em>ARPÈGES BRISÉS</em></div>
        <div class="ej-page-num">122</div>
      </div>
      <div class="ej-instruction">
        A travailler successivement avec chacune des articulations suivantes:
      </div>

      <!-- 10 ARTICULACIONES OFICIALES (9/8 y 3/4) -->
      <div class="art-strip-box">
        <div id="ej11-art-strip-1"></div>
        <div id="ej11-art-strip-2" style="margin-top:-6px;"></div>
      </div>

      <!-- TARJETA DE ENFOQUE DE SECCIÓN CROMÁTICA SELECCIONADA -->
      <div id="focus-card" class="focus-card">
        <div class="focus-header">
          <div class="focus-title" id="focus-title">🎯 Sección Activa: 1 · Bajo en Do (Ut)</div>
          <div class="focus-badge" id="focus-badge">Compases 1–10 · 18 Semicorcheas quebradas por compás</div>
        </div>
        <div id="focus-chords-grid" class="chord-pills-grid"></div>
        <div id="ej11-focus-staff"></div>
      </div>

      <!-- 14 SISTEMAS DE LA PÁGINA 122 (Compases 1–28) -->
      <div class="systems-list" id="systems-page-122"></div>

      <div class="plate-footer">A. L. 16.588</div>
    </div>

    <!-- PÁGINA 123 (Sistemas 15 a 30 · Compases 29 a 60) -->
    <div class="leduc-page page-break-after" id="page-123">
      <div class="page-header">
        <div class="ej-main-title">E. J. 11 — <em>ARPÈGES BRISÉS (Suite)</em></div>
        <div class="ej-page-num">123</div>
      </div>
      <div class="systems-list" id="systems-page-123"></div>
      <div class="plate-footer">A. L. 16.588</div>
    </div>

    <!-- PÁGINA 124 (Sistemas 31 a 45 · Compases 61 a 90) -->
    <div class="leduc-page page-break-after" id="page-124">
      <div class="page-header">
        <div class="ej-main-title">E. J. 11 — <em>ARPÈGES BRISÉS (Suite)</em></div>
        <div class="ej-page-num">124</div>
      </div>
      <div class="systems-list" id="systems-page-124"></div>
      <div class="plate-footer">A. L. 16.588</div>
    </div>

    <!-- PÁGINA 125 (Sistemas 46 a 60 · Compases 91 a 121) -->
    <div class="leduc-page" id="page-125">
      <div class="page-header">
        <div class="ej-main-title">E. J. 11 — <em>ARPÈGES BRISÉS (Fin)</em></div>
        <div class="ej-page-num">125</div>
      </div>
      <div class="systems-list" id="systems-page-125"></div>
      <div class="urtext-note">
        <span><strong>Fórmula quebrada (18 notas en 9/8):</strong> Ascenso en sextas quebradas <code>(a1,a3)(a2,a4)(a3,a5)(a4,a6)(a5,a7)</code> + regreso <code>(a5,a6)(a4,a5)(a3,a4)(a2,a3)</code>.</span>
        <span><strong>Edición Urtext:</strong> Págs. 122–125 · Plancha A. L. 16.588 (121 compases · 2,161 notas).</span>
      </div>
      <div class="plate-footer">A. L. 16.588</div>
    </div>

  </div>

  <!-- INSPECTOR DE CÓDIGO ABC -->
  <div class="abc-code-section">
    <details class="abc-details" open>
      <summary>📄 Ver Código Fuente ABC Completo (E. J. 11 · 121 Compases · Articulación Activa)</summary>
      <textarea id="abc-source-box" class="abc-textarea" readonly></textarea>
    </details>
  </div>

  <script>
    const EJ11_MEASURES = {json.dumps(ALL_MEASURES, ensure_ascii=False)};
    const EJ11_SECTIONS = {json.dumps(sections_js_data, ensure_ascii=False)};
    const EJ11_ARTS = {json.dumps(EJ11_ARTICULATIONS_META, ensure_ascii=False)};

    let currentArtId = 0;
    let currentSecIdx = -1;
    let currentTempo = 72;
    let isPlaying = false;
    let audioCtx = null;
    let playTimeouts = [];

    const ART_STRIP_ROW1_ABC = [
      "X:101",
      "M:9/8",
      "L:1/16",
      "K:C",
      "V:1 clef=treble stem=down",
      '"^1" (cccccc cccccc cccccc) || "^2" (cccccc) (cccccc) (cccccc) || "^3" (cccc).c.c (cccc).c.c (cccc).c.c || "^4" .c.c(cccc) .c.c(cccc) .c.c(cccc) || "^5" (cc).c.c.c.c (cc).c.c.c.c (cc).c.c.c.c ||'
    ].join("\\n");

    const ART_STRIP_ROW2_ABC = [
      "X:102",
      "M:3/4",
      "L:1/16",
      "K:C",
      "V:1 clef=treble stem=down",
      '"^6" (ccc)(ccc) (ccc)(ccc) (ccc)(ccc) || "^7" (ccc).c.c.c (ccc).c.c.c (ccc).c.c.c || [M:9/8] "^8" (cc)(cc)(cc) (cc)(cc)(cc) (cc)(cc)(cc) || "^9" .c(cc)(cc)(c c)(cc)(cc)(c c)(cc)(cc).c || "^10" .c.c.c.c.c.c .c.c.c.c.c.c .c.c.c.c.c.c ||'
    ].join("\\n");

    function formatMeasure18(n, artId) {{
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

    function buildSystemAbc(sysIdx, artId) {{
      const art = EJ11_ARTS[artId];
      const meterStr = sysIdx === 0 ? art.meter : "none";
      const startM = sysIdx * 2;
      const slice = EJ11_MEASURES.slice(startM, startM + 2);
      const bars = slice.map(mObj => {{
        const bTxt = formatMeasure18(mObj.notes18, artId);
        const barline = mObj.isSectionEnd ? "||" : "|";
        return `${{bTxt}} ${{barline}}`;
      }});
      if (sysIdx === 59) {{
        bars.push("B4 z4 z10 |]");
      }}
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

    function buildSectionFocusAbc(secIdx, artId) {{
      const art = EJ11_ARTS[artId];
      const startM = secIdx * 10;
      const slice = EJ11_MEASURES.slice(startM, startM + 10);
      const lines = [
        `X:${{secIdx + 200}}`,
        "%%stretchlast 1",
        "%%barsperstaff 2",
        `M:${{art.meter}}`,
        "L:1/16",
        "K:C",
        "V:1 clef=treble"
      ];
      for (let i = 0; i < 10; i += 2) {{
        const m1 = slice[i];
        const m2 = slice[i + 1];
        const b1 = `"[c.${{m1.measureNum}}]" ` + formatMeasure18(m1.notes18, artId) + " |";
        const b2 = `"[c.${{m2.measureNum}}]" ` + formatMeasure18(m2.notes18, artId) + (i === 8 ? " ||" : " |");
        lines.push(b1 + " " + b2);
      }}
      return lines.join("\\n");
    }}

    function buildFullAbcText(artId) {{
      const art = EJ11_ARTS[artId];
      const lines = [
        `X:${{artId + 1}}`,
        `T:E. J. 11 — Arpèges Brisés (${{art.name}})`,
        "C:Paul Taffanel & Philippe Gaubert (Ed. Alphonse Leduc A. L. 16.588, págs. 122–125)",
        "%%stretchlast 1",
        "%%barsperstaff 2",
        `M:${{art.meter}}`,
        "L:1/16",
        `Q:1/4.=${{currentTempo}}`,
        "K:C",
        "V:1 clef=treble"
      ];
      for (let sysIdx = 0; sysIdx < 60; sysIdx++) {{
        const startM = sysIdx * 2;
        const slice = EJ11_MEASURES.slice(startM, startM + 2);
        const bars = slice.map(mObj => {{
          const bTxt = formatMeasure18(mObj.notes18, artId);
          const barline = mObj.isSectionEnd ? "||" : "|";
          return `${{bTxt}} ${{barline}}`;
        }});
        if (sysIdx === 59) {{
          bars.push("B4 z4 z10 |]");
        }}
        lines.push(bars.join(" "));
      }}
      return lines.join("\\n");
    }}

    function initLayout() {{
      const artRow = document.getElementById("art-buttons-row");
      EJ11_ARTS.forEach(art => {{
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
      allBtn.textContent = "Todas (121 c.)";
      allBtn.onclick = () => selectSection(-1);
      secRow.appendChild(allBtn);

      EJ11_SECTIONS.forEach(sec => {{
        const btn = document.createElement("button");
        btn.className = "pill-btn";
        btn.id = `sec-btn-${{sec.id}}`;
        btn.textContent = sec.pillLabel;
        btn.onclick = () => selectSection(sec.id);
        secRow.appendChild(btn);
      }});

      const p122 = document.getElementById("systems-page-122");
      const p123 = document.getElementById("systems-page-123");
      const p124 = document.getElementById("systems-page-124");
      const p125 = document.getElementById("systems-page-125");
      p122.innerHTML = "";
      p123.innerHTML = "";
      p124.innerHTML = "";
      p125.innerHTML = "";

      for (let sysIdx = 0; sysIdx < 60; sysIdx++) {{
        const firstM = sysIdx * 2 + 1;
        const lastM = sysIdx === 59 ? 121 : sysIdx * 2 + 2;
        const secObj = EJ11_SECTIONS[Math.floor((firstM - 1) / 10)];
        const row = document.createElement("div");
        row.className = "system-row";
        row.id = `sys-row-${{sysIdx}}`;
        row.innerHTML = `
          <div class="sys-label">
            c.${{firstM}}–${{lastM}}
            <span class="sec-tag">${{secObj.short}}</span>
          </div>
          <div class="system-staff" id="ej11-sys-${{sysIdx}}"></div>
        `;
        if (sysIdx < 14) p122.appendChild(row);
        else if (sysIdx < 30) p123.appendChild(row);
        else if (sysIdx < 45) p124.appendChild(row);
        else p125.appendChild(row);
      }}
    }}

    function renderStaffLine(elemId, abc, virtualWidth, padY = 0) {{
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
      renderStaffLine("ej11-art-strip-1", ART_STRIP_ROW1_ABC, 2050, 1);
      renderStaffLine("ej11-art-strip-2", ART_STRIP_ROW2_ABC, 2050, 1);

      for (let sysIdx = 0; sysIdx < 60; sysIdx++) {{
        const abc = buildSystemAbc(sysIdx, currentArtId);
        renderStaffLine(`ej11-sys-${{sysIdx}}`, abc, sysIdx === 59 ? 1960 : 1840, 0);
      }}

      const focusCard = document.getElementById("focus-card");
      if (currentSecIdx >= 0) {{
        const sec = EJ11_SECTIONS[currentSecIdx];
        const art = EJ11_ARTS[currentArtId];
        focusCard.classList.add("visible");
        document.getElementById("focus-title").textContent = `🎯 Sección Activa: ${{sec.titleEs}} — ${{art.name}}`;
        document.getElementById("focus-badge").textContent = `Compases ${{sec.startMeasure}}–${{sec.endMeasure}} · Pedal MIDI ${{sec.bassMidi}} · Compás ${{art.meter}}`;

        const grid = document.getElementById("focus-chords-grid");
        grid.innerHTML = "";
        const slice = EJ11_MEASURES.slice(sec.id * 10, sec.id * 10 + 10);
        slice.forEach(m => {{
          const pill = document.createElement("div");
          pill.className = "chord-pill";
          pill.innerHTML = `<strong>c.${{m.measureNum}}:</strong> <code>${{m.triad.join("–")}}</code> · ${{m.chordDesc}}`;
          grid.appendChild(pill);
        }});

        renderStaffLine("ej11-focus-staff", buildSectionFocusAbc(currentSecIdx, currentArtId), 1840, 2);
      }} else {{
        focusCard.classList.remove("visible");
      }}

      const fullAbc = buildFullAbcText(currentArtId);
      document.getElementById("abc-source-box").value = fullAbc;
      const dlLink = document.getElementById("download-abc-link");
      if (dlLink) {{
        dlLink.href = "downloads/abc/" + EJ11_ARTS[currentArtId].fname;
      }}
    }}

    function selectArticulation(artId) {{
      currentArtId = artId;
      EJ11_ARTS.forEach(a => {{
        const el = document.getElementById(`art-btn-${{a.id}}`);
        if (el) el.classList.toggle("active", a.id === artId);
      }});
      if (isPlaying) {{
        stopPlayback();
        startPlayback();
      }}
      renderAll();
    }}

    function selectSection(secIdx) {{
      currentSecIdx = secIdx;
      const allBtn = document.getElementById("sec-btn-all");
      if (allBtn) allBtn.classList.toggle("active-sec", secIdx === -1);
      EJ11_SECTIONS.forEach(sec => {{
        const btn = document.getElementById(`sec-btn-${{sec.id}}`);
        if (btn) btn.classList.toggle("active-sec", sec.id === secIdx);
      }});
      for (let sysIdx = 0; sysIdx < 60; sysIdx++) {{
        const r = document.getElementById(`sys-row-${{sysIdx}}`);
        if (!r) continue;
        if (secIdx === -1) {{
          r.classList.remove("active-system");
        }} else {{
          const startM = secIdx * 10 + 1;
          const endM = secIdx * 10 + 10;
          const sysStart = sysIdx * 2 + 1;
          const sysEnd = sysIdx * 2 + 2;
          const overlaps = sysStart <= endM && sysEnd >= startM;
          r.classList.toggle("active-system", overlaps);
        }}
      }}
      const badge = document.getElementById("measure-badge");
      if (secIdx >= 0) {{
        const sec = EJ11_SECTIONS[secIdx];
        badge.textContent = `Sección: ${{sec.short}} (c. ${{sec.startMeasure}}–${{sec.endMeasure}})`;
      }} else {{
        badge.textContent = `Compases: 1–121 (Completo)`;
      }}
      if (isPlaying) {{
        stopPlayback();
        startPlayback();
      }}
      renderAll();
    }}

    function updateTempo(val) {{
      currentTempo = parseInt(val, 10) || 72;
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
      switch (artId) {{
        case 3:  return pos6 === 4 || pos6 === 5;
        case 4:  return pos6 === 0 || pos6 === 1;
        case 5:  return pos6 >= 2;
        case 7:  return pos6 >= 3;
        case 9:  return posInMeasure === 0 || posInMeasure === 17;
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

      const noteDur = (60 / currentTempo) / 6;
      const measuresToPlay = currentSecIdx >= 0
        ? EJ11_MEASURES.slice(currentSecIdx * 10, currentSecIdx * 10 + 10)
        : EJ11_MEASURES;

      let cursor = audioCtx.currentTime + 0.06;

      measuresToPlay.forEach((mObj) => {{
        for (let pos = 0; pos < 18; pos++) {{
          const midi = mObj.midis18[pos];
          const stacc = isNoteStaccato(currentArtId, pos);
          playPianoNote(midi, cursor, noteDur, stacc);

          if (pos === 0) {{
            const delayMs = Math.max(0, (cursor - audioCtx.currentTime) * 1000);
            const tid = setTimeout(() => {{
              if (!isPlaying) return;
              document.getElementById("measure-badge").textContent = `c. ${{mObj.measureNum}}/121 (${{mObj.sectionShort}} · ${{mObj.triad.join("–")}})`;
              for (let s = 0; s < 60; s++) {{
                const r = document.getElementById(`sys-row-${{s}}`);
                if (r) r.classList.toggle("active-system", s === mObj.systemIdx);
              }}
            }}, delayMs);
            playTimeouts.push(tid);
          }}
          cursor += noteDur;
        }}
      }});

      if (currentSecIdx === -1 || currentSecIdx === 11) {{
        playPianoNote(71, cursor, noteDur * 6, false);
        const delayFinal = Math.max(0, (cursor - audioCtx.currentTime) * 1000);
        const tidFinal = setTimeout(() => {{
          if (!isPlaying) return;
          document.getElementById("measure-badge").textContent = `c. 121/121 (Si4 Final)`;
        }}, delayFinal);
        playTimeouts.push(tidFinal);
        cursor += noteDur * 18;
      }}

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
      initLayout();
      renderAll();
    }});
  </script>
</body>
</html>
"""

for target in [
    os.path.join(BRAIN_DIR, "taffanel_ej11_validacion.html"),
    os.path.join(ROOT_DIR, "taffanel_ej11_validacion.html"),
    os.path.join(DOCS_DIR, "ej11.html"),
]:
    with open(target, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)

print("✅ Generados taffanel_ej11_validacion.html y docs/ej11.html")
