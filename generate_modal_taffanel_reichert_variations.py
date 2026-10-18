#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Maestro de las 840 Variaciones Modales (84 Modos Paralelos × 10 Esquemas Técnicos)
============================================================================================
Extiende los 84 Modos Paralelos (12 Tónicas Cromáticas × 7 Modos Griegos en Orden por Familia)
a TODOS los esquemas técnicos de Taffanel & Gaubert (A. L. 16.588) y M. A. Reichert (Op. 5):

  - Taffanel & Gaubert:
      1. E.J. 1  — Pentacordios Modales por Grados Conjuntos (M:4/2, L:1/16, 257 notas, 10 articulaciones)
      2. E.J. 2  — Pentacordios Modales con Giro Cadencial (M:4/2, L:1/16, 257 notas, 10 articulaciones)
      3. E.J. 4  — Escalas Diatónicas Modales por Terceras (M:4/2, L:1/8, 127 notas, 8 articulaciones)
      4. E.J. 5  — Escalas Modales Continuas en 6/8 (M:6/8, L:1/16, 49 notas, 10 articulaciones)
      5. E.J. 10 — Arpegios Modales Diatónicos en 6/8 (M:6/8, L:1/16, 97 notas, 10 articulaciones)
      6. E.J. 11 — Arpegios Quebrados (Arpèges Brisés) Modales en 9/8 (M:9/8, L:1/16, 145 notas, 10 articulaciones)

  - Mathieu-André Reichert (7 Exercices Journaliers, Op. 5):
      7. R. 1    — Ejercicio Diario Nº 1 Modal en 6/8 (M:6/8, L:1/16, 43 notas, 10 articulaciones)
      8. R. 2    — Ejercicio Diario Nº 2 Modal en 2/4 (M:2/4, L:1/16, 61 notas, 8 articulaciones)
      9. R. 4    — Ejercicio Diario Nº 4 Modal en 4/4 (M:C, L:1/16, 61 notas, 8 articulaciones)
     10. R. 5    — Ejercicio Diario Nº 5 Modal en 2/4 Tresillos (M:2/4, L:1/16, 91 notas, 10 articulaciones)
"""

import json
import math
import os
from generate_parallel_modos import (
    TONICS,
    MODES_PARALLEL,
    apply_accidentals_to_notes,
)
from tests.test_helpers import count_abc_notes_in_body

MODE_SEMITONES = {
    1: [0, 2, 4, 5, 7, 9, 11],  # Jónico (Mayor)
    2: [0, 2, 4, 6, 7, 9, 11],  # Lidio
    3: [0, 2, 4, 5, 7, 9, 10],  # Mixolidio
    4: [0, 2, 3, 5, 7, 9, 10],  # Dórico
    5: [0, 2, 3, 5, 7, 8, 10],  # Eólico (Menor Natural)
    6: [0, 1, 3, 5, 7, 8, 10],  # Frigio
    7: [0, 1, 3, 5, 6, 8, 10],  # Lócrio
}

MODE_IDS = {
    1: "jonico",
    2: "lidio",
    3: "mixolidio",
    4: "dorico",
    5: "eolico",
    6: "frigio",
    7: "locrio",
}

# 8 articulaciones clásicas para grupos de 8 notas (E.J. 4, R. 2, R. 4 — Leduc / Schott)
ARTICULATIONS_8 = [
    {"id": "a", "name": "a) Ligado de 8 (Pulso completo)", "desc": "(8) — Legato continuo por grupo de 8 notas"},
    {"id": "b", "name": "b) Ligado de 4 + 4", "desc": "(4)(4) — Dos grupos ligados de 4 notas"},
    {"id": "c", "name": "c) 2 Ligadas + 2 Picadas", "desc": "(2) . . (2) . . — Articulación mixta clásica"},
    {"id": "d", "name": "d) 1 Picada + 2 Ligadas + 1 Picada", "desc": ". (2) . . (2) . — Síncopa de articulación"},
    {"id": "e", "name": "e) 2 Picadas + 2 Ligadas", "desc": ". . (2) . . (2) — Alternancia picado-ligado"},
    {"id": "f", "name": "f) 1 Picada + 3 Ligadas", "desc": ". (3) . (3) — Impulso picado y tres ligadas"},
    {"id": "g", "name": "g) 3 Ligadas + 1 Picada", "desc": "(3) . (3) . — Tres ligadas y cierre staccato"},
    {"id": "h", "name": "h) Todo Picado (Staccato / Détaché)", "desc": ". . . . . . . . — Igualdad de ataque simple/doble"},
]

# 10 articulaciones oficiales Leduc A. L. 16.588 para pentacordios en M:4/2 (E.J. 1 y E.J. 2, grupos de 8 semicorcheas)
ARTICULATIONS_EJ1_EJ2 = [
    {"id": "a", "name": "a) 1. A 8 Ligadas (Pulso completo)", "desc": "(8) — Un solo ligado por pulso de blanca"},
    {"id": "b", "name": "b) 2. A 4 y 4 Ligadas", "desc": "(4)(4) — Dos grupos ligados de 4 semicorcheas"},
    {"id": "c", "name": "c) 3. 1 Picada y 3 Ligadas", "desc": ". (3) . (3) — Impulso articulado y tres ligadas"},
    {"id": "d", "name": "d) 4. 3 Ligadas y 1 Picada", "desc": "(3) . (3) . — Tres ligadas y cierre picado"},
    {"id": "e", "name": "e) 5. 2 Ligadas y 2 Picadas", "desc": "(2) . . (2) . . — Alternancia ligado-picado"},
    {"id": "f", "name": "f) 6. 2 Picadas y 2 Ligadas", "desc": ". . (2) . . (2) — Alternancia picado-ligado"},
    {"id": "g", "name": "g) 7. 1 Picada, 2 Ligadas y 1 Picada", "desc": ". (2) . . (2) . — Síncopa simétrica de 4 notas"},
    {"id": "h", "name": "h) 8. De 2 en 2 Ligadas", "desc": "(2)(2)(2)(2) — Cuatro pares ligados por pulso"},
    {"id": "i", "name": "i) 9. De 2 en 2 Sincopadas (a contratiempo)", "desc": ". (2)(2)(2) . — Ligaduras desplazadas a contratiempo"},
    {"id": "j", "name": "j) 10. Todo Picado (Staccato / Détaché)", "desc": ". . . . . . . . — Articulación staccato integral"},
]

# 10 articulaciones oficiales Leduc/Schott para 6/8, 9/8 y Tresillos (E.J. 5, E.J. 10, E.J. 11, R. 1, R. 5 — grupos de 6 semicorcheas)
ARTICULATIONS_6_8 = [
    {"id": "a", "name": "a) 1. Ligado de 6 (Pulso completo)", "desc": "(6) — Seisillo/pulso ligado íntegro"},
    {"id": "b", "name": "b) 2. De 3 en 3 Ligadas", "desc": "(3)(3) — Subdivisión binaria de tresillos"},
    {"id": "c", "name": "c) 3. 4 Ligadas y 2 Picadas", "desc": "(4) . . — Cuatro ligadas y dos picadas"},
    {"id": "d", "name": "d) 4. 2 Picadas y 4 Ligadas", "desc": ". . (4) — Dos picadas y cuatro ligadas"},
    {"id": "e", "name": "e) 5. 2 Ligadas y 4 Picadas", "desc": "(2) . . . . — Dos ligadas y cuatro picadas"},
    {"id": "f", "name": "f) 6. 2 Ligadas y 1 Picada (x2)", "desc": "(2) . (2) . — Articulación mixta ternaria"},
    {"id": "g", "name": "g) 7. 1 Picada y 2 Ligadas (x2)", "desc": ". (2) . (2) — Picado seguido de par ligado"},
    {"id": "h", "name": "h) 8. 3 Ligadas y 3 Picadas", "desc": "(3) . . . — Contraste ligado-staccato por pulso"},
    {"id": "i", "name": "i) 9. De 2 en 2 Ligadas", "desc": "(2)(2)(2) — Hemiola de pares ligados"},
    {"id": "j", "name": "j) 10. Todo Picado (Staccato / Triple golpe)", "desc": ". . . . . . — Détaché de precisión"},
]

SCHEMES = [
    {
        "id": "ej1",
        "code": "E.J. 1",
        "shortName": "Taffanel E.J. 1",
        "title": "E.J. 1 — Pentacordios Modales por Grados",
        "tradition": "Taffanel & Gaubert",
        "sourceRef": "Taffanel & Gaubert (págs. 2–9)",
        "meter": "4/2",
        "unitLen": "1/16",
        "tempo": "1/4=80",
        "barsPerStaff": 1,
        "totalNotes": 257,
        "measures": 8,
        "articulationGroup": "ej1_ej2",
        "pedagogy": "Trabaja la igualdad digital de los 5 primeros sonidos de cada grado del modo (I a I') manteniendo fija la alteración característica modal.",
    },
    {
        "id": "ej2",
        "code": "E.J. 2",
        "shortName": "Taffanel E.J. 2",
        "title": "E.J. 2 — Pentacordios Modales con Giro en 2 Octavas",
        "tradition": "Taffanel & Gaubert",
        "sourceRef": "Taffanel & Gaubert (págs. 10–17)",
        "meter": "4/2",
        "unitLen": "1/16",
        "tempo": "1/4=80",
        "barsPerStaff": 1,
        "totalNotes": 257,
        "measures": 8,
        "articulationGroup": "ej1_ej2",
        "pedagogy": "Recorre las 2 octavas del modo mediante pentacordios enlazados con el giro cadencial característico de Taffanel en el 4º pulso.",
    },
    {
        "id": "ej4",
        "code": "E.J. 4",
        "shortName": "Taffanel E.J. 4",
        "title": "E.J. 4 — Escalas Diatónicas Modales por Terceras",
        "tradition": "Taffanel & Gaubert",
        "sourceRef": "Taffanel & Gaubert (págs. 111–114)",
        "meter": "4/2",
        "unitLen": "1/8",
        "tempo": "1/2=80",
        "barsPerStaff": 2,
        "totalNotes": 127,
        "measures": 8,
        "articulationGroup": "ej4_8",
        "pedagogy": "Esquema canónico de escalas modales de 8 compases subiendo y bajando por terceras diatónicas a través de 2 octavas completas.",
    },
    {
        "id": "ej5",
        "code": "E.J. 5",
        "shortName": "Taffanel E.J. 5",
        "title": "E.J. 5 — Escalas Modales Continuas en 6/8",
        "tradition": "Taffanel & Gaubert",
        "sourceRef": "Taffanel & Gaubert (pág. 115)",
        "meter": "6/8",
        "unitLen": "1/16",
        "tempo": "1/4.=72",
        "barsPerStaff": 2,
        "totalNotes": 49,
        "measures": 4,
        "articulationGroup": "6_8",
        "pedagogy": "Fluidez lineal en compás compuesto (6/8) recorriendo las 2 octavas del modo sin saltos mediante doble arco sobre la dominante modal.",
    },
    {
        "id": "ej10",
        "code": "E.J. 10",
        "shortName": "Taffanel E.J. 10",
        "title": "E.J. 10 — Arpegios Modales Diatónicos en 6/8",
        "tradition": "Taffanel & Gaubert",
        "sourceRef": "Taffanel & Gaubert (págs. 120–121)",
        "meter": "6/8",
        "unitLen": "1/16",
        "tempo": "1/4.=66",
        "barsPerStaff": 2,
        "totalNotes": 97,
        "measures": 8,
        "articulationGroup": "6_8",
        "pedagogy": "Despliega los 7 acordes diatónicos generados por el modo (I, II, III, IV, V, VI, VII, I) en arpegios de 2 octavas.",
    },
    {
        "id": "ej11",
        "code": "E.J. 11",
        "shortName": "Taffanel E.J. 11",
        "title": "E.J. 11 — Arpegios Quebrados Modales en 9/8",
        "tradition": "Taffanel & Gaubert",
        "sourceRef": "Taffanel & Gaubert (págs. 122–125)",
        "meter": "9/8",
        "unitLen": "1/16",
        "tempo": "1/4.=60",
        "barsPerStaff": 2,
        "totalNotes": 145,
        "measures": 8,
        "articulationGroup": "6_8",
        "pedagogy": "Aplica la fórmula de arpèges brisés de Taffanel en 9/8 sobre los 7 grados armónicos del modo para flexibilidad de embocadura.",
    },
    {
        "id": "r1",
        "code": "R. 1",
        "shortName": "Reichert Nº 1",
        "title": "Reichert Op. 5 Nº 1 — Diseño Melódico Modal en 6/8",
        "tradition": "M. A. Reichert Op. 5",
        "sourceRef": "M.-A. Reichert Op. 5 (págs. 2–3)",
        "meter": "6/8",
        "unitLen": "1/16",
        "tempo": "1/4.=88",
        "barsPerStaff": 2,
        "totalNotes": 43,
        "measures": 4,
        "articulationGroup": "6_8",
        "pedagogy": "Adapta el célebre Ejercicio Nº 1 de Reichert a la escala de cada modo, culminando con el arpegio de 2 octavas hasta la tónica aguda.",
    },
    {
        "id": "r2",
        "code": "R. 2",
        "shortName": "Reichert Nº 2",
        "title": "Reichert Op. 5 Nº 2 — Saltos Armónicos Modales en 2/4",
        "tradition": "M. A. Reichert Op. 5",
        "sourceRef": "M.-A. Reichert Op. 5 (págs. 4–5)",
        "meter": "2/4",
        "unitLen": "1/16",
        "tempo": "1/4=116",
        "barsPerStaff": 4,
        "totalNotes": 61,
        "measures": 8,
        "articulationGroup": "ej4_8",
        "pedagogy": "Alterna el arpegio de tónica modal con el acorde de sensible/subtónica modal a través de 2 octavas con anacrusa de 4 semicorcheas.",
    },
    {
        "id": "r4",
        "code": "R. 4",
        "shortName": "Reichert Nº 4",
        "title": "Reichert Op. 5 Nº 4 — Bordaduras y Arpegios Modales en 4/4",
        "tradition": "M. A. Reichert Op. 5",
        "sourceRef": "M.-A. Reichert Op. 5 (págs. 8–9)",
        "meter": "C",
        "unitLen": "1/16",
        "tempo": "1/4=112",
        "barsPerStaff": 2,
        "totalNotes": 61,
        "measures": 4,
        "articulationGroup": "ej4_8",
        "pedagogy": "Combina arpegios en inversiones ascendentes con bordaduras superiores e inferiores propias de los semitonos modales.",
    },
    {
        "id": "r5",
        "code": "R. 5",
        "shortName": "Reichert Nº 5",
        "title": "Reichert Op. 5 Nº 5 — Tresillos con Pedal Modal en 2/4",
        "tradition": "M. A. Reichert Op. 5",
        "sourceRef": "M.-A. Reichert Op. 5 (págs. 10–13)",
        "meter": "2/4",
        "unitLen": "1/16",
        "tempo": "1/4=76",
        "barsPerStaff": 4,
        "totalNotes": 91,
        "measures": 8,
        "articulationGroup": "6_8",
        "pedagogy": "Desarrolla grandes intervalos ligados en tresillos entre el registro grave modal y el registro agudo sobre pedal armónico.",
    },
]


def get_scale_notes_pair(tonic, mode):
    """
    Devuelve (s_base, s_acc):
      - s_base: las 16 notas diatónicas sin prefijo de alteración accidental redundante.
      - s_acc: las 16 notas con la alteración accidental exacta del modo (incluyendo doble bemol '__'
        en Mi♭ Lócrio [__B] y La♭ Frigio/Lócrio [__B, __E], y doble sostenido '^^' en Do♯ Lidio [^^F]).
    """
    s_base = list(tonic["base_notes"])
    acc_dict = {}
    if mode["acc_key"]:
        acc_dict = dict(tonic[f"{mode['acc_key']}_acc"])
        # Corrección ortográfica Urtext para dobles bemoles en armaduras de 6 y 7 bemoles:
        # - En Mi♭ menor (K:Ebm, 6 bemoles), el 5º grado es Si♭; disminuido en Lócrio es Si𝄫 (__B).
        if tonic["id"] == "05_mi_bemol" and mode["acc_key"] == "loc":
            acc_dict[4] = "__"
        # - En La♭ menor (K:Abm, 7 bemoles), el 2º grado es Si♭ y el 5º grado es Mi♭;
        #   rebajados en Frigio/Lócrio son Si𝄫 (__B) y Mi𝄫 (__E).
        elif tonic["id"] == "10_la_bemol" and mode["acc_key"] == "phr":
            acc_dict[1] = "__"
        elif tonic["id"] == "10_la_bemol" and mode["acc_key"] == "loc":
            acc_dict[1] = "__"
            acc_dict[4] = "__"
    s_acc = apply_accidentals_to_notes(s_base, acc_dict)
    return s_base, s_acc


def resolve_measure_groups(groups_of_indices, s_base, s_acc):
    """
    Aplica la regla de grabado musical Urtext dentro de un mismo compás:
    la primera vez que aparece un grado alterado `d` (misma letra y octava) dentro del compás
    se escribe con su alteración (`s_acc[d]`), y las apariciones subsiguientes de ese mismo `d`
    dentro del mismo compás usan `s_base[d]` sin repetir innecesariamente el signo accidental.
    """
    seen_in_measure = set()
    resolved = []
    for idx_list in groups_of_indices:
        grp = []
        for d in idx_list:
            if d not in seen_in_measure:
                grp.append(s_acc[d])
                seen_in_measure.add(d)
            else:
                grp.append(s_base[d])
        resolved.append(grp)
    return resolved


def get_accidental_badge(tonic, mode):
    if mode["acc_key"]:
        return tonic["notes_desc"][mode["acc_key"]]
    return mode["note_label"]


def format_group_8_8ths(notes8, art_id):
    n = notes8
    if art_id == "a":
        return f"({n[0]}{n[1]}{n[2]}{n[3]}{n[4]}{n[5]}{n[6]}{n[7]})"
    elif art_id == "b":
        return f"({n[0]}{n[1]}{n[2]}{n[3]}) ({n[4]}{n[5]}{n[6]}{n[7]})"
    elif art_id == "c":
        return f"({n[0]}{n[1]}).{n[2]}.{n[3]} ({n[4]}{n[5]}).{n[6]}.{n[7]}"
    elif art_id == "d":
        return f".{n[0]}({n[1]}{n[2]}).{n[3]} .{n[4]}({n[5]}{n[6]}).{n[7]}"
    elif art_id == "e":
        return f".{n[0]}.{n[1]}({n[2]}{n[3]}) .{n[4]}.{n[5]}({n[6]}{n[7]})"
    elif art_id == "f":
        return f".{n[0]}({n[1]}{n[2]}{n[3]}) .{n[4]}({n[5]}{n[6]}{n[7]})"
    elif art_id == "g":
        return f"({n[0]}{n[1]}{n[2]}).{n[3]} ({n[4]}{n[5]}{n[6]}).{n[7]}"
    elif art_id == "h":
        return f".{n[0]}.{n[1]}.{n[2]}.{n[3]} .{n[4]}.{n[5]}.{n[6]}.{n[7]}"
    return f"({''.join(n)})"


def format_group_4_16ths(notes4, art_id):
    n = notes4
    if art_id in ("a", "b"):
        return f"({n[0]}{n[1]}{n[2]}{n[3]})"
    elif art_id == "c":
        return f"({n[0]}{n[1]}).{n[2]}.{n[3]}"
    elif art_id == "d":
        return f".{n[0]}({n[1]}{n[2]}).{n[3]}"
    elif art_id == "e":
        return f".{n[0]}.{n[1]}({n[2]}{n[3]})"
    elif art_id == "f":
        return f".{n[0]}({n[1]}{n[2]}{n[3]})"
    elif art_id == "g":
        return f"({n[0]}{n[1]}{n[2]}).{n[3]}"
    elif art_id == "h":
        return f".{n[0]}.{n[1]}.{n[2]}.{n[3]}"
    return f"({''.join(n)})"


def format_group_8_16ths_ej1(notes8, art_id):
    n = notes8
    if art_id == "a":
        return f"({''.join(n)})"
    elif art_id == "b":
        return f"({''.join(n[0:4])})({''.join(n[4:8])})"
    elif art_id == "c":
        return f".{n[0]}({n[1]}{n[2]}{n[3]}).{n[4]}({n[5]}{n[6]}{n[7]})"
    elif art_id == "d":
        return f"({n[0]}{n[1]}{n[2]}).{n[3]}({n[4]}{n[5]}{n[6]}).{n[7]}"
    elif art_id == "e":
        return f"({n[0]}{n[1]}).{n[2]}.{n[3]}({n[4]}{n[5]}).{n[6]}.{n[7]}"
    elif art_id == "f":
        return f".{n[0]}.{n[1]}({n[2]}{n[3]}).{n[4]}.{n[5]}({n[6]}{n[7]})"
    elif art_id == "g":
        return f".{n[0]}({n[1]}{n[2]}).{n[3]}.{n[4]}({n[5]}{n[6]}).{n[7]}"
    elif art_id == "h":
        return f"({n[0]}{n[1]})({n[2]}{n[3]})({n[4]}{n[5]})({n[6]}{n[7]})"
    elif art_id == "i":
        return f".{n[0]}({n[1]}{n[2]})({n[3]}{n[4]})({n[5]}{n[6]}).{n[7]}"
    elif art_id == "j":
        return "".join(f".{x}" for x in n)
    return f"({''.join(n)})"


def format_group_6_16ths(notes6, art_id):
    n = notes6
    if art_id == "a":
        return f"({''.join(n)})"
    elif art_id == "b":
        return f"({n[0]}{n[1]}{n[2]})({n[3]}{n[4]}{n[5]})"
    elif art_id == "c":
        return f"({n[0]}{n[1]}{n[2]}{n[3]}).{n[4]}.{n[5]}"
    elif art_id == "d":
        return f".{n[0]}.{n[1]}({n[2]}{n[3]}{n[4]}{n[5]})"
    elif art_id == "e":
        return f"({n[0]}{n[1]}).{n[2]}.{n[3]}.{n[4]}.{n[5]}"
    elif art_id == "f":
        return f"({n[0]}{n[1]}).{n[2]}({n[3]}{n[4]}).{n[5]}"
    elif art_id == "g":
        return f".{n[0]}({n[1]}{n[2]}).{n[3]}({n[4]}{n[5]})"
    elif art_id == "h":
        return f"({n[0]}{n[1]}{n[2]}).{n[3]}.{n[4]}.{n[5]}"
    elif art_id == "i":
        return f"({n[0]}{n[1]})({n[2]}{n[3]})({n[4]}{n[5]})"
    elif art_id == "j":
        return "".join(f".{x}" for x in n)
    return f"({''.join(n)})"


def format_triplet_pair(notes6, art_id):
    n = notes6
    t1 = f"(3{n[0]}{n[1]}{n[2]}"
    t2 = f"(3{n[3]}{n[4]}{n[5]}"
    if art_id == "a":
        return f"((3{n[0]}{n[1]}{n[2]}(3{n[3]}{n[4]}{n[5]})"
    elif art_id == "b":
        return f"((3{n[0]}{n[1]}{n[2]}) ((3{n[3]}{n[4]}{n[5]})"
    elif art_id == "c":
        return f"((3{n[0]}{n[1]}{n[2]}(3{n[3]}).{n[4]}.{n[5]}"
    elif art_id == "d":
        return f"(3.{n[0]}.{n[1]}({n[2]}(3{n[3]}{n[4]}{n[5]})"
    elif art_id == "e":
        return f"(3({n[0]}{n[1]}).{n[2]} (3.{n[3]}.{n[4]}.{n[5]}"
    elif art_id == "f":
        return f"(3({n[0]}{n[1]}).{n[2]} (3({n[3]}{n[4]}).{n[5]}"
    elif art_id == "g":
        return f"(3.{n[0]}({n[1]}{n[2]}) (3.{n[3]}({n[4]}{n[5]})"
    elif art_id == "h":
        return f"((3{n[0]}{n[1]}{n[2]}) (3.{n[3]}.{n[4]}.{n[5]}"
    elif art_id == "i":
        return f"(3({n[0]}{n[1]})({n[2]}(3{n[3]})({n[4]}{n[5]})"
    elif art_id == "j":
        return f"(3.{n[0]}.{n[1]}.{n[2]} (3.{n[3]}.{n[4]}.{n[5]}"
    return f"{t1} {t2}"


def generate_scheme_degrees_and_abc(tonic, mode, scheme_id, art_id="a"):
    """
    Construye simultáneamente:
      1. La lista exacta de grados de la escala (0..15) para cada nota del ejercicio.
      2. Las líneas del cuerpo musical ABC para (tonic, mode, scheme_id, art_id),
         aplicando deduplicación de alteraciones accidentales dentro de cada compás.
    """
    s_base, s_acc = get_scale_notes_pair(tonic, mode)
    degrees = []

    if scheme_id == "ej1":
        lines = []
        for d in range(8):
            idx_std = [d, d + 1, d + 2, d + 3, d + 4, d + 3, d + 2, d + 1]
            if d < 7:
                beats_idx = [idx_std, idx_std, idx_std, idx_std]
                bar_end = "|"
            else:
                idx_turn = [d, d + 1, d + 2, d + 3, d + 4, d + 2, d + 1, d]
                beats_idx = [idx_std, idx_std, idx_std, idx_turn]
                bar_end = f"| {s_acc[7]}4 z4 z8 |]"
            for b_i in beats_idx:
                degrees.extend(b_i)
            beats = resolve_measure_groups(beats_idx, s_base, s_acc)
            art_str = " ".join(format_group_8_16ths_ej1(b, art_id) for b in beats)
            lines.append(f"{art_str} {bar_end}")
        degrees.append(7)
        return degrees, lines

    elif scheme_id == "ej2":
        degrees_arch = [0, 2, 4, 7, 10, 5, 3]
        lines = []
        for d in degrees_arch:
            idx_std = [d, d + 1, d + 2, d + 3, d + 4, d + 3, d + 2, d + 1]
            idx_turn = [d, d + 1, d + 2, d + 3, d + 4, d + 2, d + 1, d]
            beats_idx = [idx_std, idx_std, idx_std, idx_turn]
            for b_i in beats_idx:
                degrees.extend(b_i)
            beats = resolve_measure_groups(beats_idx, s_base, s_acc)
            art_str = " ".join(format_group_8_16ths_ej1(b, art_id) for b in beats)
            lines.append(f"{art_str} |")
        idx_ii = [1, 2, 3, 4, 5, 4, 3, 2]
        idx_i = [0, 1, 2, 3, 4, 3, 2, 1]
        idx_i_turn = [0, 1, 2, 3, 4, 2, 1, 0]
        c8_beats_idx = [idx_ii, idx_ii, idx_i, idx_i_turn]
        for b_i in c8_beats_idx:
            degrees.extend(b_i)
        degrees.append(0)
        c8_beats = resolve_measure_groups(c8_beats_idx, s_base, s_acc)
        art_c8 = " ".join(format_group_8_16ths_ej1(b, art_id) for b in c8_beats)
        lines.append(f"{art_c8} | {s_acc[0]}4 z4 z8 |]")
        return degrees, lines

    elif scheme_id == "ej4":
        groups_idx = [
            (list(range(0, 8)), [8, 7, 6, 5, 4, 3, 2, 1]),
            (list(range(2, 10)), [10, 9, 8, 7, 6, 5, 4, 3]),
            (list(range(4, 12)), [12, 11, 10, 9, 8, 7, 6, 5]),
            (list(range(6, 14)), [14, 13, 12, 11, 10, 9, 8, 7]),
            (list(range(6, 14)), [12, 11, 10, 9, 8, 7, 6, 5]),
            (list(range(4, 12)), [10, 9, 8, 7, 6, 5, 4, 3]),
            (list(range(2, 10)), [8, 7, 6, 5, 4, 3, 2, 1]),
        ]
        bars = []
        for g_asc, g_desc in groups_idx:
            degrees.extend(g_asc)
            degrees.extend(g_desc)
            n_asc, n_desc = resolve_measure_groups([g_asc, g_desc], s_base, s_acc)
            bars.append(
                f"{format_group_8_8ths(n_asc, art_id)} "
                f"{format_group_8_8ths(n_desc, art_id)}"
            )
        c8_asc_idx = list(range(0, 8))
        c8_desc_idx = [6, 5, 4, 3, 2, 1, 0]
        degrees.extend(c8_asc_idx)
        degrees.extend(c8_desc_idx)
        n8_asc, n8_desc = resolve_measure_groups([c8_asc_idx, c8_desc_idx], s_base, s_acc)
        c8_asc = format_group_8_8ths(n8_asc, art_id)
        if art_id == "h":
            c8_desc = f".{n8_desc[0]}.{n8_desc[1]}.{n8_desc[2]}.{n8_desc[3]} .{n8_desc[4]}.{n8_desc[5]}.{n8_desc[6]}2"
        else:
            c8_desc = f"({n8_desc[0]}{n8_desc[1]}{n8_desc[2]}{n8_desc[3]}{n8_desc[4]}{n8_desc[5]} {n8_desc[6]}2)"
        bars.append(f"{c8_asc} {c8_desc}")
        return degrees, [
            f"{bars[0]} | {bars[1]} |",
            f"{bars[2]} | {bars[3]} |",
            f"{bars[4]} | {bars[5]} |",
            f"{bars[6]} | {bars[7]} |]",
        ]

    elif scheme_id == "ej5":
        measure_pairs = [
            ([0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]),
            ([12, 13, 14, 13, 12, 11], [10, 9, 8, 7, 6, 5]),
            ([4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 13]),
            ([12, 11, 10, 9, 8, 7], [6, 5, 4, 3, 2, 1]),
        ]
        fmt_bars = []
        for g1, g2 in measure_pairs:
            degrees.extend(g1)
            degrees.extend(g2)
            n1, n2 = resolve_measure_groups([g1, g2], s_base, s_acc)
            fmt_bars.append(f"{format_group_6_16ths(n1, art_id)} {format_group_6_16ths(n2, art_id)}")
        degrees.append(0)
        return degrees, [
            f"{fmt_bars[0]} | {fmt_bars[1]} |",
            f"{fmt_bars[2]} | {fmt_bars[3]} | {s_acc[0]}4 z2 z6 |]",
        ]

    elif scheme_id in ("ej10", "ej11"):
        chord_degrees = [
            [0, 2, 4, 7, 9, 11, 14],    # I
            [1, 3, 5, 8, 10, 12, 15],   # II
            [0, 2, 4, 6, 9, 11, 13],    # III
            [0, 3, 5, 7, 10, 12, 14],   # IV
            [1, 4, 6, 8, 11, 13, 15],   # V
            [0, 2, 5, 7, 9, 12, 14],    # VI
            [1, 3, 6, 8, 10, 13, 15],   # VII
            [0, 2, 4, 7, 9, 11, 14],    # I
        ]
        bars = []
        for cd in chord_degrees:
            d1, d2, d3, d4, d5, d6, d7 = cd
            if scheme_id == "ej10":
                g1_idx = [d1, d2, d3, d4, d5, d6]
                g2_idx = [d7, d6, d5, d4, d3, d2]
                degrees.extend(g1_idx)
                degrees.extend(g2_idx)
                n1, n2 = resolve_measure_groups([g1_idx, g2_idx], s_base, s_acc)
                bars.append(
                    f"{format_group_6_16ths(n1, art_id)} "
                    f"{format_group_6_16ths(n2, art_id)}"
                )
            else:
                g1_idx = [d1, d3, d2, d4, d3, d5]
                g2_idx = [d4, d6, d5, d7, d5, d6]
                g3_idx = [d4, d5, d3, d4, d2, d3]
                degrees.extend(g1_idx)
                degrees.extend(g2_idx)
                degrees.extend(g3_idx)
                n1, n2, n3 = resolve_measure_groups([g1_idx, g2_idx, g3_idx], s_base, s_acc)
                bars.append(
                    f"{format_group_6_16ths(n1, art_id)} "
                    f"{format_group_6_16ths(n2, art_id)} "
                    f"{format_group_6_16ths(n3, art_id)}"
                )
        degrees.append(0)
        closing = f"{s_acc[0]}4 z2 z6 |]" if scheme_id == "ej10" else f"{s_acc[0]}6 z3 z9 |]"
        return degrees, [
            f"{bars[0]} | {bars[1]} |",
            f"{bars[2]} | {bars[3]} |",
            f"{bars[4]} | {bars[5]} |",
            f"{bars[6]} | {bars[7]} | {closing}",
        ]

    elif scheme_id == "r1":
        m1_g = ([7, 4, 5, 6, 7, 8], [9, 7, 8, 9, 10, 11])
        m2_g = ([11, 9, 10, 11, 12, 13], [14, 13, 12, 11, 10, 9])
        m3_g = ([12, 11, 10, 9, 8, 7], [6, 5, 4, 3, 2, 1])
        m4_g = ([0, 2, 4, 7, 9, 11], [14])
        for g1, g2 in (m1_g, m2_g, m3_g):
            degrees.extend(g1)
            degrees.extend(g2)
        degrees.extend(m4_g[0])
        degrees.extend(m4_g[1])

        m1_n = resolve_measure_groups(list(m1_g), s_base, s_acc)
        m2_n = resolve_measure_groups(list(m2_g), s_base, s_acc)
        m3_n = resolve_measure_groups(list(m3_g), s_base, s_acc)
        m4_n = resolve_measure_groups(list(m4_g), s_base, s_acc)

        return degrees, [
            f"{format_group_6_16ths(m1_n[0], art_id)} {format_group_6_16ths(m1_n[1], art_id)} | "
            f"{format_group_6_16ths(m2_n[0], art_id)} {format_group_6_16ths(m2_n[1], art_id)} |",
            f"{format_group_6_16ths(m3_n[0], art_id)} {format_group_6_16ths(m3_n[1], art_id)} | "
            f"{format_group_6_16ths(m4_n[0], art_id)} .{m4_n[1][0]}2 z2 z2 |]",
        ]

    elif scheme_id == "r2":
        pickup_idx = [0, 2, 4, 7]
        measures_idx = [
            [6, 4, 3, 1, 3, 4, 6, 8],
            [7, 4, 2, 0, 2, 4, 7, 9],
            [8, 6, 4, 3, 4, 6, 8, 10],
            [9, 7, 4, 2, 4, 7, 9, 11],
            [10, 8, 6, 4, 6, 8, 10, 11],
            [11, 9, 7, 4, 7, 9, 11, 14],
            [8, 6, 4, 3, 1, 3, 4, 6],
        ]
        degrees.extend(pickup_idx)
        for m_idx in measures_idx:
            degrees.extend(m_idx)
        degrees.append(7)
        pk_notes = resolve_measure_groups([pickup_idx], s_base, s_acc)[0]
        pickup = format_group_4_16ths(pk_notes, art_id)
        m_strs = [
            format_group_8_8ths(resolve_measure_groups([m_idx], s_base, s_acc)[0], art_id)
            for m_idx in measures_idx
        ]
        return degrees, [
            f"{pickup} | {m_strs[0]} | {m_strs[1]} | {m_strs[2]} |",
            f"{m_strs[3]} | {m_strs[4]} | {m_strs[5]} | {m_strs[6]} | .{s_acc[7]}2 z2 |]",
        ]

    elif scheme_id == "r4":
        bars_idx = [
            ([0, 2, 4, 5, 4, 3, 4, 2], [2, 4, 7, 8, 7, 6, 7, 4]),
            ([4, 7, 9, 10, 9, 8, 9, 7], [7, 9, 11, 12, 11, 10, 11, 9]),
            ([4, 7, 9, 10, 9, 8, 9, 7], [2, 4, 7, 8, 7, 6, 7, 4]),
        ]
        m4_hb1_idx = [0, 2, 4, 7, 9, 11, 7, 9]
        m4_tail_idx = [4, 7, 2, 4]
        m4_end_idx = [0]

        bar_strs = []
        for hb1, hb2 in bars_idx:
            degrees.extend(hb1)
            degrees.extend(hb2)
            n1, n2 = resolve_measure_groups([hb1, hb2], s_base, s_acc)
            bar_strs.append(f"{format_group_8_8ths(n1, art_id)} {format_group_8_8ths(n2, art_id)}")

        degrees.extend(m4_hb1_idx)
        degrees.extend(m4_tail_idx)
        degrees.extend(m4_end_idx)
        n4_hb1, n4_tail, n4_end = resolve_measure_groups([m4_hb1_idx, m4_tail_idx, m4_end_idx], s_base, s_acc)
        m4_str = (
            f"{format_group_8_8ths(n4_hb1, art_id)} "
            f"{format_group_4_16ths(n4_tail, art_id)} .{n4_end[0]}2 z2 |]"
        )
        return degrees, [
            f"{bar_strs[0]} | {bar_strs[1]} |",
            f"{bar_strs[2]} | {m4_str}",
        ]

    elif scheme_id == "r5":
        triplet_pairs_idx = [
            ([7, 9, 11, 14, 9, 11], [7, 9, 11, 4, 9, 11]),
            ([8, 10, 11, 13, 10, 11], [8, 10, 11, 4, 10, 11]),
            ([6, 10, 11, 15, 10, 11], [6, 10, 11, 4, 10, 11]),
            ([7, 9, 11, 14, 9, 11], [7, 9, 11, 4, 9, 11]),
            ([7, 9, 12, 14, 9, 12], [6, 9, 11, 15, 9, 11]),
            ([5, 9, 12, 14, 9, 12], [3, 8, 11, 15, 8, 11]),
            ([4, 9, 11, 14, 9, 11], [4, 10, 11, 13, 10, 11]),
        ]
        m8_idx = [7, 9, 11, 14, 9, 11]
        m8_end_idx = [7]
        m_strs = []
        for p1, p2 in triplet_pairs_idx:
            degrees.extend(p1)
            degrees.extend(p2)
            n1, n2 = resolve_measure_groups([p1, p2], s_base, s_acc)
            m_strs.append(
                f"{format_triplet_pair(n1, art_id)} "
                f"{format_triplet_pair(n2, art_id)}"
            )
        degrees.extend(m8_idx)
        degrees.extend(m8_end_idx)
        n8_trip, n8_end = resolve_measure_groups([m8_idx, m8_end_idx], s_base, s_acc)
        m8_str = f"{format_triplet_pair(n8_trip, art_id)} .{n8_end[0]}2 z2"
        return degrees, [
            f"{m_strs[0]} | {m_strs[1]} | {m_strs[2]} | {m_strs[3]} |",
            f"{m_strs[4]} | {m_strs[5]} | {m_strs[6]} | {m8_str} |]",
        ]

    raise ValueError(f"Unknown scheme_id: {scheme_id}")


def compute_midis_and_freqs(tonic_idx, mode_num, degrees):
    """Calcula la secuencia exacta de alturas MIDI y frecuencias (A4=440Hz) para los grados dados."""
    root_midi = 59 + tonic_idx  # 01_si = B3 (59) .. 12_si_bemol = Bb4 (70)
    semitones = MODE_SEMITONES[mode_num]
    midis = []
    freqs = []
    for d in degrees:
        m = root_midi + 12 * (d // 7) + semitones[d % 7]
        f = round(440.0 * (2.0 ** ((m - 69.0) / 12.0)), 2)
        midis.append(m)
        freqs.append(f)
    return midis, freqs


def build_single_abc(tonic, mode, scheme, x_num=1, art_id="a"):
    key_sig = tonic["major_key"] if mode["is_major_family"] else tonic["minor_key"]
    acc_badge = get_accidental_badge(tonic, mode)
    degrees, body_lines = generate_scheme_degrees_and_abc(tonic, mode, scheme["id"], art_id)

    short_tonic = tonic["display"].split(" (")[0]
    short_mode_name = mode["name"].split(" (")[0]
    header = [
        f"X:{x_num}",
        f"T:Modo {mode['num']}: {short_tonic} {short_mode_name} ({scheme['code']})",
        f"C:{scheme['tradition']} · Adaptación Modal ({scheme['sourceRef']})",
        f"% Modo {mode['num']}/7 ({mode['family']}) | {acc_badge} | Fórmula: {mode['formula']}",
        f"%%barsperstaff {scheme['barsPerStaff']}",
        f"M:{scheme['meter']}",
        f"L:{scheme['unitLen']}",
        f"Q:{scheme['tempo']}",
        f"K:{key_sig}",
        "V:1 clef=treble",
        "%%score 1",
    ]
    return degrees, "\n".join(header + body_lines)


def get_articulations_for_scheme(scheme):
    grp = scheme["articulationGroup"]
    if grp == "ej1_ej2":
        return ARTICULATIONS_EJ1_EJ2
    elif grp == "6_8":
        return ARTICULATIONS_6_8
    return ARTICULATIONS_8


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    var_dir = os.path.join(base_dir, "abc_modos_variaciones")
    docs_dir = os.path.join(base_dir, "docs")
    docs_abc_dir = os.path.join(docs_dir, "downloads", "abc")
    os.makedirs(var_dir, exist_ok=True)
    os.makedirs(docs_abc_dir, exist_ok=True)

    compact_browser_data = {
        "schemes": SCHEMES,
        "articulationCatalog": {
            "ej1_ej2": ARTICULATIONS_EJ1_EJ2,
            "ej4_8": ARTICULATIONS_8,
            "6_8": ARTICULATIONS_6_8,
        },
        "tonics": [
            {
                "id": t["id"],
                "name": t["name"],
                "display": t["display"],
                "majorKey": t["major_key"],
                "minorKey": t["minor_key"],
                "majorDesc": t["major_desc"],
                "minorDesc": t["minor_desc"],
            }
            for t in TONICS
        ],
        "modes": [
            {
                "id": MODE_IDS[m["num"]],
                "num": m["num"],
                "name": m["name"],
                "family": m["family"],
                "char": m["char"],
                "formula": m["formula"],
                "noteLabel": m["note_label"],
            }
            for m in MODES_PARALLEL
        ],
        "exercises": {},  # key: f"{scheme_id}__{tonic_id}__{mode_num}"
    }

    total_generated = 0

    for scheme in SCHEMES:
        scheme_id = scheme["id"]
        scheme_code_slug = scheme["code"].replace(". ", "").replace(".", "").replace(" ", "")
        scheme_subdir = os.path.join(var_dir, scheme_id)
        os.makedirs(scheme_subdir, exist_ok=True)

        master_lines = [
            "%abc-2.1",
            "%%pagewidth 21.0cm",
            "%%pageheight 29.7cm",
            "%%topmargin 1.2cm",
            "%%botmargin 1.2cm",
            "%%leftmargin 1.3cm",
            "%%rightmargin 1.3cm",
            "%%titlespace 0.2cm",
            "%%musicspace 0.25cm",
            "%%staffsep 1.1cm",
            "%% scale 0.68",
            "% ===========================================================================",
            f"% COLECCIÓN COMPLETA: 84 MODOS PARALELOS — ESQUEMA {scheme['code']} ({scheme['title']})",
            f"% Fuente: {scheme['tradition']} ({scheme['sourceRef']})",
            "% 12 Tónicas Cromáticas (Si a Si bemol) × 7 Modos Paralelos = 84 Ejercicios",
            "% ===========================================================================",
            "",
        ]

        global_x = 1
        for t_idx, tonic in enumerate(TONICS):
            tonic_lines = [
                "%abc-2.1",
                f"% Tónica {tonic['id']}: {tonic['name']} — 7 Modos Paralelos bajo el esquema {scheme['code']}",
                f"% {scheme['title']} ({scheme['sourceRef']})",
                "",
            ]

            for mode in MODES_PARALLEL:
                mode_num = mode["num"]
                mode_id = MODE_IDS[mode_num]
                key_sig = tonic["major_key"] if mode["is_major_family"] else tonic["minor_key"]

                degrees, abc_default = build_single_abc(tonic, mode, scheme, x_num=mode_num, art_id="a")
                _, abc_master_item = build_single_abc(tonic, mode, scheme, x_num=global_x, art_id="a")

                tonic_lines.append(abc_default)
                tonic_lines.append("")
                master_lines.append(abc_master_item)
                master_lines.append("")

                midis, freqs = compute_midis_and_freqs(t_idx, mode_num, degrees)
                parsed_note_count = count_abc_notes_in_body(abc_default)
                assert len(midis) == scheme["totalNotes"] == parsed_note_count, (
                    f"Note count mismatch for {scheme_id} {tonic['name']} {mode['name']}: "
                    f"expected {scheme['totalNotes']}, midis={len(midis)}, abc_notes={parsed_note_count}"
                )
                assert min(midis) >= 59 and max(midis) <= 98, (
                    f"Tessitura out of Boehm range [59,98] for {scheme_id} {tonic['name']} {mode['name']}: "
                    f"[{min(midis)}, {max(midis)}]"
                )

                arts = get_articulations_for_scheme(scheme)
                abc_by_art = {}
                for art in arts:
                    _, art_abc = build_single_abc(tonic, mode, scheme, x_num=mode_num, art_id=art["id"])
                    assert count_abc_notes_in_body(art_abc) == scheme["totalNotes"], (
                        f"Articulation {art['id']} altered note count in {scheme_id} {tonic['id']} {mode_id}"
                    )
                    abc_by_art[art["id"]] = art_abc

                ex_key = f"{scheme_id}__{tonic['id']}__{mode_num}"
                compact_browser_data["exercises"][ex_key] = {
                    "key": ex_key,
                    "schemeId": scheme_id,
                    "schemeCode": scheme["code"],
                    "tonicId": tonic["id"],
                    "tonicName": tonic["name"],
                    "tonicDisplay": tonic["display"],
                    "modeId": mode_id,
                    "modeNum": mode_num,
                    "modeName": mode["name"],
                    "family": mode["family"],
                    "char": mode["char"],
                    "keySig": key_sig,
                    "badge": get_accidental_badge(tonic, mode),
                    "formula": mode["formula"],
                    "meter": scheme["meter"],
                    "unitLen": scheme["unitLen"],
                    "tempo": scheme["tempo"],
                    "totalNotes": len(midis),
                    "minMidi": min(midis),
                    "maxMidi": max(midis),
                    "midiNotes": midis,
                    "frequencies": freqs,
                    "abc": abc_default,
                    "abcByArticulation": abc_by_art,
                }

                global_x += 1
                total_generated += 1

            tonic_filename = f"modos_{tonic['id']}_{scheme_id}.abc"
            with open(os.path.join(scheme_subdir, tonic_filename), "w", encoding="utf-8") as f:
                f.write("\n".join(tonic_lines))

        master_filename = f"00_Coleccion_84_Modos_{scheme_code_slug}.abc"
        master_content = "\n".join(master_lines)
        for target_dir in (base_dir, var_dir, docs_abc_dir):
            with open(os.path.join(target_dir, master_filename), "w", encoding="utf-8") as f:
                f.write(master_content)

    json_path = os.path.join(docs_dir, "modes_variations_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(compact_browser_data, f, ensure_ascii=False, indent=2)

    js_path = os.path.join(docs_dir, "modes_variations_data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("window.MODES_VARIATIONS_DATA = ")
        json.dump(compact_browser_data, f, ensure_ascii=False)
        f.write(";\n")

    print(f"Generadas y verificadas con éxito {total_generated} variaciones modales (84 modos × 10 esquemas).")
    print(f"Datos exportados en: {json_path} y {js_path}")


if __name__ == "__main__":
    main()
