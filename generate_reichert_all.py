#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates 100% Urtext transcriptions, interactive Web players, ABC collections,
MIDI pitch arrays, and shared score_template.html data for:
  M. A. Reichert — 7 Exercices Journaliers pour la Flûte, Op. 5
  (B. Schott's Söhne, Mainz, Plate 20623)
  - R1: Nº 1 (pp. 2–3, 6/8, De 80 à 100 dotted quarter, 24 keys + D.S. al Fine)
  - R2: Nº 2 (pp. 4–5, 2/4, de 120 à 152 quarter, 24 keys + D.S. al Fine)
  - R4: Nº 4 (pp. 8–9, C / 4/4, de 116 à 144 quarter, 24 keys + D.S. al Fine)
  - R5: Nº 5 (pp. 10–13, 2/4 triplets, de 144 à 184 eighth, 24 keys + D.S. al Fine)
"""

import json
import os

# ---------------------------------------------------------------------------
# Diatonic & Chromatic Pitch Helper (exact spelling per key signature)
# ---------------------------------------------------------------------------
# Diatonic letter index: 0=C, 1=D, 2=E, 3=F, 4=G, 5=A, 6=B
NAT_SEMI = [0, 2, 4, 5, 7, 9, 11]
LETTERS_UPPER = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
LETTERS_LOWER = ['c', 'd', 'e', 'f', 'g', 'a', 'b']

# Key definitions for the 24 tonalities in Reichert Op. 5 (Schott 20623 order):
# (sec_id, short_es, full_es, full_en, abc_key, tonic_letter_idx, tonic_acc, is_minor, key_sig_map)
# key_sig_map maps letter_idx (0..6) -> default accidental (-1, 0, +1)
def make_key_sig(flats=0, sharps=0):
    sig = {i: 0 for i in range(7)}
    flat_order = [6, 2, 5, 1, 4, 0, 3]   # B E A D G C F
    sharp_order = [3, 0, 4, 1, 5, 2, 6]  # F C G D A E B
    for i in range(flats):
        sig[flat_order[i]] = -1
    for i in range(sharps):
        sig[sharp_order[i]] = 1
    return sig

KEYS_24 = [
    (0,  "1. Do M",    "1. Do Mayor (C Major)",           "1. C Major",          "C",   0,  0, False, make_key_sig()),
    (1,  "2. La m",    "2. La menor (Relatif Mineur)",    "2. A minor",          "Am",  5,  0, True,  make_key_sig()),
    (2,  "3. Fa M",    "3. Fa Mayor (F Major)",           "3. F Major",          "F",   3,  0, False, make_key_sig(flats=1)),
    (3,  "4. Re m",    "4. Re menor (Mineur)",            "4. D minor",          "Dm",  1,  0, True,  make_key_sig(flats=1)),
    (4,  "5. Si♭ M",   "5. Si♭ Mayor (B♭ Major)",         "5. B♭ Major",         "Bb",  6, -1, False, make_key_sig(flats=2)),
    (5,  "6. Sol m",   "6. Sol menor (Mineur)",           "6. G minor",          "Gm",  4,  0, True,  make_key_sig(flats=2)),
    (6,  "7. Mi♭ M",   "7. Mi♭ Mayor (E♭ Major)",         "7. E♭ Major",         "Eb",  2, -1, False, make_key_sig(flats=3)),
    (7,  "8. Do m",    "8. Do menor (Mineur)",            "8. C minor",          "Cm",  0,  0, True,  make_key_sig(flats=3)),
    (8,  "9. La♭ M",   "9. La♭ Mayor (A♭ Major)",         "9. A♭ Major",         "Ab",  5, -1, False, make_key_sig(flats=4)),
    (9,  "10. Fa m",   "10. Fa menor (Mineur)",           "10. F minor",         "Fm",  3,  0, True,  make_key_sig(flats=4)),
    (10, "11. Re♭ M",  "11. Re♭ Mayor (D♭ Major)",        "11. D♭ Major",        "Db",  1, -1, False, make_key_sig(flats=5)),
    (11, "12. Si♭ m",  "12. Si♭ menor (Mineur)",          "12. B♭ minor",        "Bbm", 6, -1, True,  make_key_sig(flats=5)),
    (12, "13. Sol♭ M", "13. Sol♭ Mayor (G♭ Major)",       "13. G♭ Major",        "Gb",  4, -1, False, make_key_sig(flats=6)),
    (13, "14. Mi♭ m",  "14. Mi♭ menor (Mineur)",          "14. E♭ minor",        "Ebm", 2, -1, True,  make_key_sig(flats=6)),
    (14, "15. Si M",   "15. Si Mayor (B Major)",          "15. B Major",         "B",   6,  0, False, make_key_sig(sharps=5)),
    (15, "16. Sol♯ m", "16. Sol♯ menor (Mineur)",         "16. G♯ minor",        "G#m", 4,  1, True,  make_key_sig(sharps=5)),
    (16, "17. Mi M",   "17. Mi Mayor (E Major)",          "17. E Major",         "E",   2,  0, False, make_key_sig(sharps=4)),
    (17, "18. Do♯ m",  "18. Do♯ menor (Mineur)",          "18. C♯ minor",        "C#m", 0,  1, True,  make_key_sig(sharps=4)),
    (18, "19. La M",   "19. La Mayor (A Major)",          "19. A Major",         "A",   5,  0, False, make_key_sig(sharps=3)),
    (19, "20. Fa♯ m",  "20. Fa♯ menor (Mineur)",          "20. F♯ minor",        "F#m", 3,  1, True,  make_key_sig(sharps=3)),
    (20, "21. Re M",   "21. Re Mayor (D Major)",          "21. D Major",         "D",   1,  0, False, make_key_sig(sharps=2)),
    (21, "22. Si m",   "22. Si menor (Mineur)",           "22. B minor",         "Bm",  6,  0, True,  make_key_sig(sharps=2)),
    (22, "23. Sol M",  "23. Sol Mayor (G Major)",         "23. G Major",         "G",   4,  0, False, make_key_sig(sharps=1)),
    (23, "24. Mi m",   "24. Mi menor (Mineur)",           "24. E minor",         "Em",  2,  0, True,  make_key_sig(sharps=1)),
    (24, "25. D.S.",   "25. Do Mayor (D.S. al Fine)",     "25. C Major (Fine)",  "C",   0,  0, False, make_key_sig()),
]


def scale_degree_pitch(key_tuple, base_oct, deg_offset, chrom_alter=0):
    """
    Returns (diatonic_abs, letter_idx, octave, accidental, midi_pitch)
    where base_oct is the octave of the tonic (e.g. 4 for C4..B4),
    deg_offset is 0-indexed diatonic steps from tonic (e.g. 0=tonic, 1=2nd, -3=5th below),
    and chrom_alter is semitone adjustment relative to the natural key signature of key_tuple.
    """
    _, _, _, _, _, t_let, t_acc, _, ksig = key_tuple
    base_diat = base_oct * 7 + t_let
    target_diat = base_diat + deg_offset
    octv = target_diat // 7
    let_idx = target_diat % 7
    default_acc = ksig[let_idx]
    acc = default_acc + chrom_alter
    midi = (octv + 1) * 12 + NAT_SEMI[let_idx] + acc
    return (target_diat, let_idx, octv, acc, midi)


def abc_pitch_str(let_idx, octv, acc, measure_acc_state, force_cautionary=False):
    """
    Formats a single ABC note (without duration) given letter_idx (0..6), octave (3..6),
    desired accidental (-2..+2), and mutable measure_acc_state dict mapping (octv, let_idx) -> current_acc.
    """
    key = (octv, let_idx)
    cur_acc = measure_acc_state[key]
    prefix = ""
    if acc != cur_acc or force_cautionary:
        if acc == -2:
            prefix = "__"
        elif acc == -1:
            prefix = "_"
        elif acc == 0:
            prefix = "="
        elif acc == 1:
            prefix = "^"
        elif acc == 2:
            prefix = "^^"
        measure_acc_state[key] = acc

    if octv <= 4:
        base = LETTERS_UPPER[let_idx]
        suffix = "," * (4 - octv)
        return f"{prefix}{base}{suffix}"
    else:
        base = LETTERS_LOWER[let_idx]
        suffix = "'" * (octv - 5)
        return f"{prefix}{base}{suffix}"


def render_measure_notes(key_tuple, note_specs):
    """
    note_specs: list of tuples (base_oct, deg_offset, chrom_alter, force_cautionary)
    Returns (list_of_abc_pitch_strings, list_of_midi_ints)
    """
    ksig = key_tuple[8]
    measure_state = {}
    for octv in range(2, 8):
        for l_idx in range(7):
            measure_state[(octv, l_idx)] = ksig[l_idx]

    abc_notes = []
    midi_notes = []
    for (b_oct, deg_off, c_alt, caut) in note_specs:
        _, l_idx, octv, acc, midi = scale_degree_pitch(key_tuple, b_oct, deg_off, c_alt)
        s = abc_pitch_str(l_idx, octv, acc, measure_state, force_cautionary=caut)
        abc_notes.append(s)
        midi_notes.append(midi)
    return abc_notes, midi_notes


# ---------------------------------------------------------------------------
# 1. REICHERT OP. 5, Nº 1 (R1) — 6/8, 4 measures per key
# ---------------------------------------------------------------------------
def generate_r1_section_measures(sec_id):
    kt = KEYS_24[sec_id]
    is_min = kt[7]
    b_oct = 4  # Low tonic in M.4 is always in octave 4 (C4..B4); M.1 starts on octave 5 (deg_offset +7)
    # Melodic minor ascending raises degrees 6 (+1) and 7 (+1)
    c6_asc = 1 if is_min else 0
    c7_asc = 1 if is_min else 0

    # Measure 1 (12 sixteenths):
    # Beat 1: 1(mid) - 5(low) - 6(low) - 7(low) - 1(mid) - 2(mid)
    # Beat 2: 3(mid) - 1(mid) - 2(mid) - 3(mid) - 4(mid) - 5(mid)
    m1_specs = [
        (b_oct, 7, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 5, c6_asc, False),
        (b_oct, 6, c7_asc, False),
        (b_oct, 7, 0, False),
        (b_oct, 8, 0, False),
        (b_oct, 9, 0, False),
        (b_oct, 7, 0, False),
        (b_oct, 8, 0, False),
        (b_oct, 9, 0, False),
        (b_oct, 10, 0, False),
        (b_oct, 11, 0, False),
    ]

    # Measure 2 (12 sixteenths):
    # Beat 1: 5(mid) - 3(mid) - 4(mid) - 5(mid) - 6(mid) - 7(mid)
    # Beat 2: 1(high) - 7_nat(mid) - 6_nat(mid) - 5(mid) - 4(mid) - 3(mid)
    m2_specs = [
        (b_oct, 11, 0, False),
        (b_oct, 9, 0, False),
        (b_oct, 10, 0, False),
        (b_oct, 11, 0, False),
        (b_oct, 12, c6_asc, False),
        (b_oct, 13, c7_asc, False),
        (b_oct, 14, 0, False),
        (b_oct, 13, 0, is_min),
        (b_oct, 12, 0, is_min),
        (b_oct, 11, 0, False),
        (b_oct, 10, 0, False),
        (b_oct, 9, 0, False),
    ]

    # Measure 3 (12 sixteenths, natural minor descending):
    # Beat 1: 6(mid) - 5(mid) - 4(mid) - 3(mid) - 2(mid) - 1(mid)
    # Beat 2: 7(low) - 6(low) - 5(low) - 4(low) - 3(low) - 2(low)
    m3_specs = [
        (b_oct, 12, 0, False),
        (b_oct, 11, 0, False),
        (b_oct, 10, 0, False),
        (b_oct, 9, 0, False),
        (b_oct, 8, 0, False),
        (b_oct, 7, 0, False),
        (b_oct, 6, 0, False),
        (b_oct, 5, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 3, 0, False),
        (b_oct, 2, 0, False),
        (b_oct, 1, 0, False),
    ]

    # Measure 4 (6 sixteenths + 1 eighth note + 2 eighth rests):
    # 1(low) - 3(low) - 5(low) - 1(mid) - 3(mid) - 5(mid) | 1(high)2 z2 z2
    m4_specs = [
        (b_oct, 0, 0, False),
        (b_oct, 2, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 7, 0, False),
        (b_oct, 9, 0, False),
        (b_oct, 11, 0, False),
        (b_oct, 14, 0, False),
    ]

    m1_abc, m1_midi = render_measure_notes(kt, m1_specs)
    m2_abc, m2_midi = render_measure_notes(kt, m2_specs)
    m3_abc, m3_midi = render_measure_notes(kt, m3_specs)
    m4_abc, m4_midi = render_measure_notes(kt, m4_specs)

    return [m1_abc, m2_abc, m3_abc, m4_abc], (m1_midi + m2_midi + m3_midi + m4_midi)


def format_12_notes_ej5_art(n, art_id):
    """Formats a 12-note measure (in two 6-note groups) with EJ5Articulation (0..10)."""
    if art_id in (0, 1):
        return f"({n[0]}{n[1]}{n[2]}{n[3]}{n[4]}{n[5]} {n[6]}{n[7]}{n[8]}{n[9]}{n[10]}{n[11]})"
    elif art_id == 2:
        return f"({n[0]}{n[1]}{n[2]}{n[3]}{n[4]}{n[5]}) ({n[6]}{n[7]}{n[8]}{n[9]}{n[10]}{n[11]})"
    elif art_id == 3:
        return f"({n[0]}{n[1]}{n[2]}{n[3]}).{n[4]}.{n[5]} ({n[6]}{n[7]}{n[8]}{n[9]}).{n[10]}.{n[11]}"
    elif art_id == 4:
        return f".{n[0]}.{n[1]}({n[2]}{n[3]}{n[4]}{n[5]}) .{n[6]}.{n[7]}({n[8]}{n[9]}{n[10]}{n[11]})"
    elif art_id == 5:
        return f"({n[0]}{n[1]}).{n[2]}.{n[3]}.{n[4]}.{n[5]} ({n[6]}{n[7]}).{n[8]}.{n[9]}.{n[10]}.{n[11]}"
    elif art_id == 6:
        return f"({n[0]}{n[1]}{n[2]})({n[3]}{n[4]}{n[5]}) ({n[6]}{n[7]}{n[8]})({n[9]}{n[10]}{n[11]})"
    elif art_id == 7:
        return f"({n[0]}{n[1]}{n[2]}).{n[3]}.{n[4]}.{n[5]} ({n[6]}{n[7]}{n[8]}).{n[9]}.{n[10]}.{n[11]}"
    elif art_id == 8:
        return f"({n[0]}{n[1]})({n[2]}{n[3]})({n[4]}{n[5]}) ({n[6]}{n[7]})({n[8]}{n[9]})({n[10]}{n[11]})"
    elif art_id == 9:
        return f".{n[0]}({n[1]}{n[2]})({n[3]}{n[4]}).{n[5]} .{n[6]}({n[7]}{n[8]})({n[9]}{n[10]}).{n[11]}"
    elif art_id == 10:
        return f".{n[0]}.{n[1]}.{n[2]}.{n[3]}.{n[4]}.{n[5]} .{n[6]}.{n[7]}.{n[8]}.{n[9]}.{n[10]}.{n[11]}"
    return f"{''.join(n[:6])} {''.join(n[6:])}"


def format_r1_m4(n, art_id, sec_id):
    """Formats Measure 4 of R1 (6 sixteenths + 1 eighth note + rests)."""
    end_bar = "|]" if sec_id in (0, 23, 24) else "||"
    fine_str = "!fine!" if sec_id in (0, 24) else ("!D.S.!" if sec_id == 23 else "")
    if art_id in (0, 1):
        grp = f"{n[0]}{n[1]}{n[2]}{n[3]}{n[4]}{n[5]} !wedge!{n[6]}2)"
    elif art_id == 2:
        grp = f"({n[0]}{n[1]}{n[2]}{n[3]}{n[4]}{n[5]}) !wedge!{n[6]}2"
    elif art_id == 3:
        grp = f"({n[0]}{n[1]}{n[2]}{n[3]}).{n[4]}.{n[5]} !wedge!{n[6]}2"
    elif art_id == 4:
        grp = f".{n[0]}.{n[1]}({n[2]}{n[3]}{n[4]}{n[5]}) !wedge!{n[6]}2"
    elif art_id == 5:
        grp = f"({n[0]}{n[1]}).{n[2]}.{n[3]}.{n[4]}.{n[5]} !wedge!{n[6]}2"
    elif art_id == 6:
        grp = f"({n[0]}{n[1]}{n[2]})({n[3]}{n[4]}{n[5]}) !wedge!{n[6]}2"
    elif art_id == 7:
        grp = f"({n[0]}{n[1]}{n[2]}).{n[3]}.{n[4]}.{n[5]} !wedge!{n[6]}2"
    elif art_id == 8:
        grp = f"({n[0]}{n[1]})({n[2]}{n[3]})({n[4]}{n[5]}) !wedge!{n[6]}2"
    elif art_id == 9:
        grp = f".{n[0]}({n[1]}{n[2]})({n[3]}{n[4]}).{n[5]} !wedge!{n[6]}2"
    else:
        grp = f".{n[0]}.{n[1]}.{n[2]}.{n[3]}.{n[4]}.{n[5]} !wedge!{n[6]}2"
    return f"{grp} {fine_str}z2 z2 {end_bar}"


def build_r1_section_abc(sec_id, art_id):
    kt = KEYS_24[sec_id]
    measures, _ = generate_r1_section_measures(sec_id)
    segno = "!segno!" if sec_id == 0 else ""
    if art_id in (0, 1):
        m1 = f"{segno}({measures[0][0]}{measures[0][1]}{measures[0][2]}{measures[0][3]}{measures[0][4]}{measures[0][5]} {measures[0][6]}{measures[0][7]}{measures[0][8]}{measures[0][9]}{measures[0][10]}{measures[0][11]}"
        m2 = f"{''.join(measures[1][:6])} {''.join(measures[1][6:])}"
        m3 = f"{''.join(measures[2][:6])} {''.join(measures[2][6:])}"
        m4 = format_r1_m4(measures[3], art_id, sec_id)
    else:
        m1 = segno + format_12_notes_ej5_art(measures[0], art_id)
        m2 = format_12_notes_ej5_art(measures[1], art_id)
        m3 = format_12_notes_ej5_art(measures[2], art_id)
        m4 = format_r1_m4(measures[3], art_id, sec_id)
    return f"[K:{kt[4]}] {m1} | {m2} | {m3} | {m4}"


# ---------------------------------------------------------------------------
# 2. REICHERT OP. 5, Nº 2 (R2) — 2/4, 8 measures per key (with pickup)
# ---------------------------------------------------------------------------
R2_8VA_SECTIONS = {0, 3, 7, 10, 17, 24}  # C, Dm, Cm, Db, C#m, C(Fine)

def generate_r2_section_measures(sec_id):
    """
    Returns (measures_abc, midi_notes) for section sec_id (0..24) of R2.
    When practicing a single section or in the complete score:
    - Each section starts with its own 4-sixteenth tonic triad pickup: 1(low)-3(low)-5(low)-1(mid)
      followed by Measures 1..7 (8 sixteenths each) and Measure 8: 1(mid)2 !wedge! z2.
    - Note: For sections in R2_8VA_SECTIONS (C, Dm, Cm, Db, C#m), written notes are in b_oct=4
      with 8va bracket, so sounding MIDI pitches are +12 semitones (+1 octave)!
    """
    kt = KEYS_24[sec_id]
    is_min = kt[7]
    b_oct = 4
    c7_lead = 1 if is_min else 0
    is_8va = sec_id in R2_8VA_SECTIONS
    midi_shift = 12 if is_8va else 0

    # Pickup (4 sixteenths): 1(low) - 3(low) - 5(low) - 1(mid)
    pickup_specs = [
        (b_oct, 0, 0, False),
        (b_oct, 2, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 7, 0, False),
    ]
    # M.1 (V7 1st inv -> 2nd inv): 7(low)-5(low)-4(low)-2(low) | 4(low)-5(low)-7(low)-2(mid)
    m1_specs = [
        (b_oct, 6, c7_lead, False),
        (b_oct, 4, 0, False),
        (b_oct, 3, 0, False),
        (b_oct, 1, 0, False),
        (b_oct, 3, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 6, c7_lead, False),
        (b_oct, 8, 0, False),
    ]
    # M.2 (I root -> 1st inv): 1(mid)-5(low)-3(low)-1(low) | 3(low)-5(low)-1(mid)-3(mid)
    m2_specs = [
        (b_oct, 7, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 2, 0, False),
        (b_oct, 0, 0, False),
        (b_oct, 2, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 7, 0, False),
        (b_oct, 9, 0, False),
    ]
    # M.3 (V7 2nd inv -> 3rd inv): 2(mid)-7(low)-5(low)-4(low) | 5(low)-7(low)-2(mid)-4(mid)
    m3_specs = [
        (b_oct, 8, 0, False),
        (b_oct, 6, c7_lead, False),
        (b_oct, 4, 0, False),
        (b_oct, 3, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 6, c7_lead, False),
        (b_oct, 8, 0, False),
        (b_oct, 10, 0, False),
    ]
    # M.4 (I 1st inv -> 2nd inv): 3(mid)-1(mid)-5(low)-3(low) | 5(low)-1(mid)-3(mid)-5(mid)
    m4_specs = [
        (b_oct, 9, 0, False),
        (b_oct, 7, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 2, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 7, 0, False),
        (b_oct, 9, 0, False),
        (b_oct, 11, 0, False),
    ]
    # M.5 (V7 3rd inv -> vii°7/V7b9): 4(mid)-2(mid)-7(low)-5(low) | 7(low)-2(mid)-4(mid)-6(mid)
    m5_specs = [
        (b_oct, 10, 0, False),
        (b_oct, 8, 0, False),
        (b_oct, 6, c7_lead, False),
        (b_oct, 4, 0, False),
        (b_oct, 6, c7_lead, False),
        (b_oct, 8, 0, False),
        (b_oct, 10, 0, False),
        (b_oct, 12, 0, False),
    ]
    # M.6 (I 2nd inv -> 1st inv): 5(mid)-3(mid)-1(mid)-5(low) | 3(low)-5(low)-1(mid)-3(mid)
    m6_specs = [
        (b_oct, 11, 0, False),
        (b_oct, 9, 0, False),
        (b_oct, 7, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 2, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 7, 0, False),
        (b_oct, 9, 0, False),
    ]
    # M.7 (V7 descent & turnaround): 2(mid)-7(low)-5(low)-4(low) | 2(low)-4(low)-5(low)-7(low)
    m7_specs = [
        (b_oct, 8, 0, False),
        (b_oct, 6, c7_lead, False),
        (b_oct, 4, 0, False),
        (b_oct, 3, 0, False),
        (b_oct, 1, 0, False),
        (b_oct, 3, 0, False),
        (b_oct, 4, 0, False),
        (b_oct, 6, c7_lead, False),
    ]
    # M.8: 1(mid) eighth note
    m8_specs = [
        (b_oct, 7, 0, False),
    ]

    all_specs = [pickup_specs, m1_specs, m2_specs, m3_specs, m4_specs, m5_specs, m6_specs, m7_specs, m8_specs]
    abc_bars = []
    midi_all = []
    for sp in all_specs:
        a_notes, m_notes = render_measure_notes(kt, sp)
        abc_bars.append(a_notes)
        midi_all.extend([m + midi_shift for m in m_notes])

    return abc_bars, midi_all


def format_8_notes_ej4_art(n, art_id):
    """Formats an 8-note measure (two 4-note groups) with EJ4Articulation (0..8)."""
    if art_id in (0, 1):
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
    return f"{''.join(n[:4])} {''.join(n[4:])}"


def format_4_notes_ej4_art(n, art_id):
    """Formats a 4-note pickup group with EJ4Articulation (0..8)."""
    if art_id in (0, 1, 2):
        return f"({n[0]}{n[1]}{n[2]}{n[3]})"
    elif art_id == 3:
        return f".{n[0]}({n[1]}{n[2]}{n[3]})"
    elif art_id == 4:
        return f"({n[0]}{n[1]}).{n[2]}.{n[3]}"
    elif art_id == 5:
        return f".{n[0]}.{n[1]}({n[2]}{n[3]})"
    elif art_id == 6:
        return f".{n[0]}({n[1]}{n[2]}).{n[3]}"
    elif art_id == 7:
        return f"({n[0]}{n[1]})({n[2]}{n[3]})"
    elif art_id == 8:
        return f".{n[0]}({n[1]}{n[2]}).{n[3]}"
    return "".join(n)


def build_r2_section_abc(sec_id, art_id):
    kt = KEYS_24[sec_id]
    bars, _ = generate_r2_section_measures(sec_id)
    # bars[0] is pickup (4 notes), bars[1..7] are M.1..M.7 (8 notes each), bars[8] is M.8 (1 note)
    segno = "!segno!" if sec_id == 0 else ""
    ottava_annotation = "\"^8va...\"" if sec_id in R2_8VA_SECTIONS else ""
    end_bar = "|]" if sec_id in (0, 23, 24) else "||"
    fine_str = "!fine!" if sec_id in (0, 24) else ("!D.S.!" if sec_id == 23 else "")

    pk = bars[0]
    if art_id in (0, 1):
        pk_str = f"{segno}{ottava_annotation}({pk[0]}{pk[1]}{pk[2]}{pk[3]}"
        mid_strs = [f"{''.join(b[:4])} {''.join(b[4:])}" for b in bars[1:8]]
        m8_str = f"!wedge!{bars[8][0]}2) {fine_str}z2 {end_bar}"
    else:
        pk_str = f"{segno}{ottava_annotation}" + format_4_notes_ej4_art(pk, art_id)
        mid_strs = [format_8_notes_ej4_art(b, art_id) for b in bars[1:8]]
        m8_str = f"!wedge!{bars[8][0]}2 {fine_str}z2 {end_bar}"

    line1 = f"[K:{kt[4]}] {pk_str} | " + " | ".join(mid_strs[:4]) + " |"
    line2 = " | ".join(mid_strs[4:]) + f" | {m8_str}"
    return line1 + "\n" + line2


# ---------------------------------------------------------------------------
# 3. REICHERT OP. 5, Nº 4 (R4) — C (4/4), 4 measures per key
# ---------------------------------------------------------------------------
# Note: In R4, sections 7 (Cm) and 10 (Db) are written starting in octave 5 (C5, Db5),
# and section 17 (C#m) is written in octave 4 with 8va (so sounding in octave 5)!
R4_OCT5_WRITTEN = {7, 10}
R4_8VA_SECTIONS = {17}

def generate_r4_section_measures(sec_id):
    kt = KEYS_24[sec_id]
    is_min = kt[7]
    b_oct = 5 if sec_id in R4_OCT5_WRITTEN else 4
    midi_shift = 12 if sec_id in R4_8VA_SECTIONS else 0

    # Chromatic lower neighbors:
    # - Below 5th degree (deg_offset 4): degree 4 (deg_offset 3) raised by +1 semitone (both Major and Minor!)
    # - Below 8th degree (deg_offset 7): degree 7 (deg_offset 6) raised by +1 in Minor, +0 in Major
    # - Below 10th degree (deg_offset 9): degree 9 (deg_offset 8) raised by +1 in Major, +0 in Minor!
    # - Below 12th degree (deg_offset 11): degree 11 (deg_offset 10) raised by +1 semitone (both Major and Minor!)
    c_below_8 = 1 if is_min else 0
    c_below_10 = 0 if is_min else 1

    # Measure 1 (16 sixteenths):
    # G1: 1 - 3 - 5 - 6
    # G2: 5 - #4 - 5 - 3
    # G3: 3 - 5 - 8 - 9
    # G4: 8 - #7 - 8 - 5
    m1_specs = [
        (b_oct, 0, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False), (b_oct, 5, 0, False),
        (b_oct, 4, 0, False), (b_oct, 3, 1, False), (b_oct, 4, 0, False), (b_oct, 2, 0, False),
        (b_oct, 2, 0, False), (b_oct, 4, 0, False), (b_oct, 7, 0, False), (b_oct, 8, 0, False),
        (b_oct, 7, 0, False), (b_oct, 6, c_below_8, False), (b_oct, 7, 0, False), (b_oct, 4, 0, False),
    ]

    # Measure 2 (16 sixteenths):
    # G1: 5 - 8 - 10 - 11
    # G2: 10 - (#9 in Maj / 9 in Min) - 10 - 8
    # G3: 8 - 10 - 12 - 13
    # G4: 12 - #11 - 12 - 10
    m2_specs = [
        (b_oct, 4, 0, False), (b_oct, 7, 0, False), (b_oct, 9, 0, False), (b_oct, 10, 0, False),
        (b_oct, 9, 0, False), (b_oct, 8, c_below_10, False), (b_oct, 9, 0, False), (b_oct, 7, 0, False),
        (b_oct, 7, 0, False), (b_oct, 9, 0, False), (b_oct, 11, 0, False), (b_oct, 12, 0, False),
        (b_oct, 11, 0, False), (b_oct, 10, 1, False), (b_oct, 11, 0, False), (b_oct, 9, 0, False),
    ]

    # Measure 3 (16 sixteenths):
    # G1: 5 - 8 - 10 - 11
    # G2: 10 - (#9 in Maj / 9 in Min) - 10 - 8
    # G3: 3 - 5 - 8 - =9 (cancels #9 from G2 in Major keys!)
    # G4: 8 - #7 - 8 - 5
    m3_specs = [
        (b_oct, 4, 0, False), (b_oct, 7, 0, False), (b_oct, 9, 0, False), (b_oct, 10, 0, False),
        (b_oct, 9, 0, False), (b_oct, 8, c_below_10, False), (b_oct, 9, 0, False), (b_oct, 7, 0, False),
        (b_oct, 2, 0, False), (b_oct, 4, 0, False), (b_oct, 7, 0, False), (b_oct, 8, 0, not is_min),
        (b_oct, 7, 0, False), (b_oct, 6, c_below_8, False), (b_oct, 7, 0, False), (b_oct, 4, 0, False),
    ]

    # Measure 4 (12 sixteenths + 1 eighth note + 1 eighth rest):
    # G1: 1 - 3 - 5 - 8
    # G2: 10 - 12 - 8 - 10
    # G3: 5 - 8 - 3 - 5
    # Beat 4: 1 (eighth note) + rest
    m4_specs = [
        (b_oct, 0, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False), (b_oct, 7, 0, False),
        (b_oct, 9, 0, False), (b_oct, 11, 0, False), (b_oct, 7, 0, False), (b_oct, 9, 0, False),
        (b_oct, 4, 0, False), (b_oct, 7, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
        (b_oct, 0, 0, False),
    ]

    abc_bars = []
    midi_all = []
    for sp in [m1_specs, m2_specs, m3_specs, m4_specs]:
        a_notes, m_notes = render_measure_notes(kt, sp)
        abc_bars.append(a_notes)
        midi_all.extend([m + midi_shift for m in m_notes])

    return abc_bars, midi_all


def format_16_notes_ej4_art(n, art_id):
    return format_8_notes_ej4_art(n[:8], art_id) + " " + format_8_notes_ej4_art(n[8:16], art_id)


def build_r4_section_abc(sec_id, art_id):
    kt = KEYS_24[sec_id]
    bars, _ = generate_r4_section_measures(sec_id)
    segno = "!segno!" if sec_id == 0 else ""
    ottava_annotation = "\"^8va...\"" if sec_id in R4_8VA_SECTIONS else ""
    end_bar = "|]" if sec_id in (0, 23, 24) else "||"
    fine_str = "!fine!" if sec_id in (0, 24) else ("!D.S.!" if sec_id == 23 else "")

    m4 = bars[3]
    if art_id in (0, 1):
        b1 = f"{segno}{ottava_annotation}({''.join(bars[0][:4])} {''.join(bars[0][4:8])} {''.join(bars[0][8:12])} {''.join(bars[0][12:16])}"
        b2 = f"{''.join(bars[1][:4])} {''.join(bars[1][4:8])} {''.join(bars[1][8:12])} {''.join(bars[1][12:16])}"
        b3 = f"{''.join(bars[2][:4])} {''.join(bars[2][4:8])} {''.join(bars[2][8:12])} {''.join(bars[2][12:16])}"
        b4 = f"{''.join(m4[:4])} {''.join(m4[4:8])} {''.join(m4[8:12])} !wedge!{m4[12]}2) {fine_str}z2 {end_bar}"
    else:
        b1 = f"{segno}{ottava_annotation}" + format_16_notes_ej4_art(bars[0], art_id)
        b2 = format_16_notes_ej4_art(bars[1], art_id)
        b3 = format_16_notes_ej4_art(bars[2], art_id)
        b4 = format_8_notes_ej4_art(m4[:8], art_id) + " " + format_4_notes_ej4_art(m4[8:12], art_id) + f" !wedge!{m4[12]}2 {fine_str}z2 {end_bar}"

    return f"[K:{kt[4]}] {b1} | {b2} |\n{b3} | {b4}"


# ---------------------------------------------------------------------------
# 4. REICHERT OP. 5, Nº 5 (R5) — 2/4 triplets, 8 measures per key
# ---------------------------------------------------------------------------
# Keys with tonic letter G(4), A(5), B(6) start on b_oct = 4;
# keys with tonic letter C(0), D(1), E(2), F(3) start on b_oct = 5!
def generate_r5_section_measures(sec_id):
    kt = KEYS_24[sec_id]
    t_let = kt[5]
    is_min = kt[7]
    # Gb Major (sec_id == 12) is written in b_oct = 5 so that 4_low (Cb5) stays >= C4
    b_oct = 4 if (t_let in (4, 5, 6) and sec_id != 12) else 5
    c7_lead = 1 if is_min else 0

    # M.1 (I / i): (1 3 5) (8 3 5) (1 3 5) (5_low 3 5)
    m1_specs = [
        (b_oct, 0, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
        (b_oct, 7, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
        (b_oct, 0, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
        (b_oct, -3, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
    ]
    # M.2 (V6/5): (2 4 5) (#7 4 5) (2 4 5) (5_low 4 5)
    m2_specs = [
        (b_oct, 1, 0, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
        (b_oct, 6, c7_lead, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
        (b_oct, 1, 0, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
        (b_oct, -3, 0, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
    ]
    # M.3 (V2): (#7_low 4 5) (9 4 5) (#7_low 4 5) (5_low 4 5)
    m3_specs = [
        (b_oct, -1, c7_lead, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
        (b_oct, 8, 0, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
        (b_oct, -1, c7_lead, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
        (b_oct, -3, 0, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
    ]
    # M.4 (I / i): identical to M.1
    m4_specs = list(m1_specs)

    if not is_min:
        # MAJOR KEYS M.5..M.7:
        # M.5: (1 3 5) (10 3 5) (7_low 3 #5) (9 3 #5)
        m5_specs = [
            (b_oct, 0, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
            (b_oct, 9, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
            (b_oct, -1, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 1, False),
            (b_oct, 8, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 1, False),
        ]
        # M.6: (6_low 3 6) (8 3 6) (4_low 2 b6) (9 2 b6)
        m6_specs = [
            (b_oct, -2, 0, False), (b_oct, 2, 0, False), (b_oct, 5, 0, False),
            (b_oct, 7, 0, False), (b_oct, 2, 0, False), (b_oct, 5, 0, False),
            (b_oct, -4, 0, False), (b_oct, 1, 0, False), (b_oct, 5, -1, False),
            (b_oct, 8, 0, False), (b_oct, 1, 0, False), (b_oct, 5, -1, False),
        ]
        # M.7: (5_low 3 5) (8 3 5) (5_low 4 5) (7 4 5)
        m7_specs = [
            (b_oct, -3, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
            (b_oct, 7, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
            (b_oct, -3, 0, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
            (b_oct, 6, 0, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
        ]
    else:
        # MINOR KEYS M.5..M.7:
        # M.5: (1 3 5) (10 3 5) (b7_low #3 5) (b9 #3 5)
        m5_specs = [
            (b_oct, 0, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
            (b_oct, 9, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
            (b_oct, -1, 0, False), (b_oct, 2, 1, False), (b_oct, 4, 0, False),
            (b_oct, 8, -1, False), (b_oct, 2, 1, False), (b_oct, 4, 0, False),
        ]
        # M.6: (6_low 4 6) (8 4 6) (4_low 4 6) (=9 4 6)
        m6_specs = [
            (b_oct, -2, 0, False), (b_oct, 3, 0, False), (b_oct, 5, 0, False),
            (b_oct, 7, 0, False), (b_oct, 3, 0, False), (b_oct, 5, 0, False),
            (b_oct, -4, 0, False), (b_oct, 3, 0, False), (b_oct, 5, 0, False),
            (b_oct, 8, 0, True), (b_oct, 3, 0, False), (b_oct, 5, 0, False),
        ]
        # M.7: (5_low 3 5) (8 3 5) (5_low 4 5) (#7 4 5)
        m7_specs = [
            (b_oct, -3, 0, False), (b_oct, 2, 0, True), (b_oct, 4, 0, False),
            (b_oct, 7, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
            (b_oct, -3, 0, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
            (b_oct, 6, 1, False), (b_oct, 3, 0, False), (b_oct, 4, 0, False),
        ]

    # M.8: (1 3 5) (8 3 5) | 1 (eighth note) + rest
    m8_specs = [
        (b_oct, 0, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
        (b_oct, 7, 0, False), (b_oct, 2, 0, False), (b_oct, 4, 0, False),
        (b_oct, 0, 0, False),
    ]

    abc_bars = []
    midi_all = []
    for sp in [m1_specs, m2_specs, m3_specs, m4_specs, m5_specs, m6_specs, m7_specs, m8_specs]:
        a_notes, m_notes = render_measure_notes(kt, sp)
        abc_bars.append(a_notes)
        midi_all.extend(m_notes)

    return abc_bars, midi_all


def format_12_triplets_ej5_art(n, art_id, show_triplet_num=False):
    """Formats 4 triplets of 3 sixteenth notes (12 notes) in 2/4 with EJ5Articulation (0..10)."""
    p = "(3" if show_triplet_num else ""
    if art_id == 0:
        return f"{p}{n[0]}{n[1]}{n[2]} {p}{n[3]}{n[4]}{n[5]} {p}{n[6]}{n[7]}{n[8]} {p}{n[9]}{n[10]}{n[11]}"
    elif art_id == 1:
        return f"{p}({n[0]}{n[1]}{n[2]} {p}{n[3]}{n[4]}{n[5]} {p}{n[6]}{n[7]}{n[8]} {p}{n[9]}{n[10]}{n[11]})"
    elif art_id == 2:
        return f"{p}({n[0]}{n[1]}{n[2]} {p}{n[3]}{n[4]}{n[5]}) {p}({n[6]}{n[7]}{n[8]} {p}{n[9]}{n[10]}{n[11]})"
    elif art_id == 3:
        return f"{p}({n[0]}{n[1]}{n[2]} {p}{n[3]}).{n[4]}.{n[5]} {p}({n[6]}{n[7]}{n[8]} {p}{n[9]}).{n[10]}.{n[11]}"
    elif art_id == 4:
        return f"{p}.{n[0]}.{n[1]}({n[2]} {p}{n[3]}{n[4]}{n[5]}) {p}.{n[6]}.{n[7]}({n[8]} {p}{n[9]}{n[10]}{n[11]})"
    elif art_id == 5:
        return f"{p}({n[0]}{n[1]}).{n[2]} {p}.{n[3]}.{n[4]}.{n[5]} {p}({n[6]}{n[7]}).{n[8]} {p}.{n[9]}.{n[10]}.{n[11]}"
    elif art_id == 6:
        return f"{p}({n[0]}{n[1]}{n[2]}) {p}({n[3]}{n[4]}{n[5]}) {p}({n[6]}{n[7]}{n[8]}) {p}({n[9]}{n[10]}{n[11]})"
    elif art_id == 7:
        return f"{p}({n[0]}{n[1]}{n[2]}) {p}.{n[3]}.{n[4]}.{n[5]} {p}({n[6]}{n[7]}{n[8]}) {p}.{n[9]}.{n[10]}.{n[11]}"
    elif art_id == 8:
        return f"{p}({n[0]}{n[1]})({n[2]} {p}{n[3]})({n[4]}{n[5]}) {p}({n[6]}{n[7]})({n[8]} {p}{n[9]})({n[10]}{n[11]})"
    elif art_id == 9:
        return f"{p}.{n[0]}({n[1]}{n[2]}) {p}({n[3]}{n[4]}).{n[5]} {p}.{n[6]}({n[7]}{n[8]}) {p}({n[9]}{n[10]}).{n[11]}"
    elif art_id == 10:
        return f"{p}.{n[0]}.{n[1]}.{n[2]} {p}.{n[3]}.{n[4]}.{n[5]} {p}.{n[6]}.{n[7]}.{n[8]} {p}.{n[9]}.{n[10]}.{n[11]}"
    return f"{p}{n[0]}{n[1]}{n[2]} {p}{n[3]}{n[4]}{n[5]} {p}{n[6]}{n[7]}{n[8]} {p}{n[9]}{n[10]}{n[11]}"


def build_r5_section_abc(sec_id, art_id):
    kt = KEYS_24[sec_id]
    bars, _ = generate_r5_section_measures(sec_id)
    segno = "!segno!" if sec_id == 0 else ""
    end_bar = "|]" if sec_id in (0, 23, 24) else "||"
    fine_str = "!fine!" if sec_id in (0, 24) else ("!D.S.!" if sec_id == 23 else "")

    m8 = bars[7]
    if art_id == 0:
        b_strs = [format_12_triplets_ej5_art(b, 0, show_triplet_num=(sec_id == 0 and idx < 4)) for idx, b in enumerate(bars[:7])]
        b_strs[0] = f"{segno}(" + b_strs[0]
        m8_str = f"{m8[0]}{m8[1]}{m8[2]} {m8[3]}{m8[4]}{m8[5]} !wedge!{m8[6]}2) {fine_str}z2 {end_bar}"
    else:
        b_strs = [format_12_triplets_ej5_art(b, art_id, show_triplet_num=False) for b in bars[:7]]
        b_strs[0] = segno + b_strs[0]
        if art_id in (1, 2):
            m8_str = f"({m8[0]}{m8[1]}{m8[2]} {m8[3]}{m8[4]}{m8[5]}) !wedge!{m8[6]}2 {fine_str}z2 {end_bar}"
        elif art_id == 6:
            m8_str = f"({m8[0]}{m8[1]}{m8[2]}) ({m8[3]}{m8[4]}{m8[5]}) !wedge!{m8[6]}2 {fine_str}z2 {end_bar}"
        elif art_id == 7:
            m8_str = f"({m8[0]}{m8[1]}{m8[2]}) .{m8[3]}.{m8[4]}.{m8[5]} !wedge!{m8[6]}2 {fine_str}z2 {end_bar}"
        elif art_id == 10:
            m8_str = f".{m8[0]}.{m8[1]}.{m8[2]} .{m8[3]}.{m8[4]}.{m8[5]} !wedge!{m8[6]}2 {fine_str}z2 {end_bar}"
        else:
            m8_str = f"({m8[0]}{m8[1]}{m8[2]} {m8[3]}{m8[4]}{m8[5]}) !wedge!{m8[6]}2 {fine_str}z2 {end_bar}"

    line1 = f"[K:{kt[4]}] " + " | ".join(b_strs[:4]) + " |"
    line2 = " | ".join(b_strs[4:]) + f" | {m8_str}"
    return line1 + "\n" + line2


if __name__ == "__main__":
    for name, fn in [
        ("R1", generate_r1_section_measures),
        ("R2", generate_r2_section_measures),
        ("R4", generate_r4_section_measures),
        ("R5", generate_r5_section_measures),
    ]:
        all_midis = [fn(s)[1] for s in range(25)]
        min_m = min(min(m) for m in all_midis)
        max_m = max(max(m) for m in all_midis)
        print(f"{name}: 25 sections, notes/sec={len(all_midis[0])}, MIDI range={min_m}..{max_m}")
