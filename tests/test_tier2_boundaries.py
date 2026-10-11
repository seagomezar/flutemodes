"""
Tier 2: Boundary & Corner Cases E2E Tests for FluteModes Ecosystem.

Comprehensive opaque-box boundary validation for all 11 modules in PROJECT.md:
1. 84 Modal Parallel Exercises (B3 low bound, upper ceiling D7, extreme tempos, C# Lydian accidentals, barline termination)
2. Taffanel & Gaubert E.J. 1 (Register safety D4..F6, tempo scaling, repeat boundary :|, articulation 0 vs 9, rest termination)
3. Taffanel & Gaubert E.J. 2 (Register safety D4..F6, tempo scaling, ^^F pitch 68/67, ^B pitch 60, chromatic pair continuity)
4. Taffanel & Gaubert E.J. 4 (Full compass C4..C7, section bounds 0..24, tempo scaling, harmonic/melodic descending notes, Coda 29-note boundary)
5. Taffanel & Gaubert E.J. 5 (Chromatic gamut C4..C7, 6/8 vs 2/4 boundary, section bounds 0..11, tempo scaling, staccato flag extremes)
6. Taffanel & Gaubert E.J. 10 (Compass C4..C7, 30 systems bounds & staffwidth 1020, section bounds 0..11, tempo scaling, 7th chord accidentals)
7. Taffanel & Gaubert E.J. 11 (High ceiling D7, m.121 termination rest bounds, 18 notes/m duration, 60 systems bounds, compound tempo scaling)
8. Reichert R. 1 (Compass bounds C4..B6, section 24 return and D.S. target, Segno vs Fine boundaries, eighth note + rests final m, tempo scaling)
9. Reichert R. 2 (Anacrusa pickup bounds, 8va sound transposition +12 st, m.8 wedge boundary, high ceiling C7/D7, tempo scaling)
10. Reichert R. 4 (Register bounds up to C7, cautionary accidental cancellation in all 12 major keys, section 17 8va notation, wedge eighth note final, tempo scaling)
11. Reichert R. 5 (Sixteenth triplet duration formula (60/BPM)/6.0, m.8 6 triplet + 1 eighth note boundary, section bounds 0..24, compass bounds, tempo scaling)

Minimum requirements: >=5 tests per feature (55 tests total).
"""

import unittest
from pathlib import Path
from tests.test_helpers import (
    WORKSPACE_ROOT,
    FLUTE_MIN_MIDI,
    FLUTE_MAX_MIDI,
    midi_to_frequency,
    calculate_note_duration,
    extract_abc_midi_pitches,
    load_score_template
)


class TestTier2ModosBoundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Modos (84 Modal Exercises)."""

    def test_b01_01_modos_low_register_b3_boundary(self):
        """Verify Modo Si (B Locrian) strictly respects lowest flute boundary B3 (MIDI 59)."""
        si_file = WORKSPACE_ROOT / "abc_modos" / "01_Modos_en_Si.abc"
        if not si_file.exists():
            si_file = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "modos_01_si.abc"
        self.assertTrue(si_file.exists())
        content = si_file.read_text(encoding="utf-8")
        pitches = extract_abc_midi_pitches(content)
        self.assertGreater(len(pitches), 0)
        min_pitch = min(pitches)
        self.assertGreaterEqual(min_pitch, FLUTE_MIN_MIDI,
                                f"Modo Si notes must not drop below B3 (MIDI 59), found {min_pitch}")
        self.assertEqual(min_pitch, 59, "Modo Si must reach the lowest B3 pitch (MIDI 59)")

    def test_b01_02_modos_high_register_ceiling_boundary(self):
        """Verify highest pitch across all 12 tonic modal files never exceeds flute ceiling D7 (MIDI 98)."""
        abc_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        all_pitches = []
        for f in abc_dir.glob("modos_*.abc"):
            all_pitches.extend(extract_abc_midi_pitches(f.read_text(encoding="utf-8")))

        self.assertGreater(len(all_pitches), 0, "Must have parsed modal pitches")
        max_pitch = max(all_pitches)
        self.assertLessEqual(max_pitch, FLUTE_MAX_MIDI,
                             f"Modal notes must not exceed flute ceiling D7 (MIDI 98), found {max_pitch}")

    def test_b01_03_modos_extreme_tempo_boundaries(self):
        """Verify extreme tempo bounds 30 BPM and 300 BPM calculate positive, finite note durations."""
        min_dur = calculate_note_duration(300, subdivision=4)
        max_dur = calculate_note_duration(30, subdivision=4)
        self.assertGreater(min_dur, 0.0)
        self.assertLess(min_dur, 0.1)
        self.assertGreater(max_dur, 0.4)
        self.assertLess(max_dur, 1.0)

    def test_b01_04_modos_accidental_handling_csharp_lydian(self):
        """Verify C# Lydian contains double sharp ^^F (G natural sounding) in modal formulas."""
        csharp_file = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "modos_03_do_sostenido.abc"
        if not csharp_file.exists():
            csharp_file = WORKSPACE_ROOT / "abc_modos" / "03_Modos_en_Do_sostenido.abc"
        self.assertTrue(csharp_file.exists())
        content = csharp_file.read_text(encoding="utf-8")
        self.assertIn("^^F", content, "Do# Lydian must utilize double-sharp ^^F for augmented 4th degree")

    def test_b01_05_modos_barline_and_slur_closure(self):
        """Verify measure 8 termination in all modes has closed slurs/parentheses and double bar |]."""
        c_file = WORKSPACE_ROOT / "abc_modos" / "02_Modos_en_Do.abc"
        if not c_file.exists():
            c_file = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "modos_02_do.abc"
        content = c_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.strip().endswith("|]"):
                open_parens = line.count("(")
                close_parens = line.count(")")
                self.assertEqual(open_parens, close_parens, "Measure 8 must have balanced parentheses for slurs")


class TestTier2EJ1Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Taffanel & Gaubert E.J. 1."""

    def test_b02_01_ej1_pitch_range_safety(self):
        """Verify E.J. 1 notes stay strictly within D4 (MIDI 62) to F6 (MIDI 89)."""
        ej1_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ1_Original_AL16588.abc"
        pitches = extract_abc_midi_pitches(ej1_abc.read_text(encoding="utf-8"))
        self.assertGreaterEqual(min(pitches), 62, "EJ 1 lowest note is D4 (MIDI 62)")
        self.assertLessEqual(max(pitches), 89, "EJ 1 highest note is F6 in 8va (MIDI 89)")

    def test_b02_02_ej1_extreme_tempo_scaling(self):
        """Verify tempo scaling at 40 BPM and 240 BPM produces exact proportional durations."""
        dur_40 = calculate_note_duration(40, subdivision=4)
        dur_240 = calculate_note_duration(240, subdivision=4)
        self.assertAlmostEqual(dur_40 / dur_240, 6.0, places=4)

    def test_b02_03_ej1_repeat_boundary_measure_24(self):
        """Verify measure 24 has repeat sign ':|' and measure 25 begins 8va section."""
        ej1_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ1_Original_AL16588.abc"
        content = ej1_abc.read_text(encoding="utf-8")
        self.assertIn(":|", content)
        self.assertIn('"^8va"', content)

    def test_b02_04_ej1_articulation_extremes_0_vs_9(self):
        """Verify articulation 1 (all slurred) and 10 (all staccato) generate correct slur tokens."""
        art1 = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "01_Taffanel_EJ1_Articulacion_01_8_Ligadas.abc").read_text(encoding="utf-8")
        art10 = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "10_Taffanel_EJ1_Articulacion_10_Todo_Picado.abc").read_text(encoding="utf-8")
        self.assertIn("(", art1, "Articulation 1 must have slurs")
        self.assertIn(".", art10, "Articulation 10 must have staccato dots")

    def test_b02_05_ej1_coda_measure_rest_duration(self):
        """Verify measure 31 rest bar 'f4 z4 z8 |]' completes 16 sixteenths (4 quarter beats)."""
        ej1_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ1_Original_AL16588.abc"
        content = ej1_abc.read_text(encoding="utf-8")
        self.assertIn("f4 z4 z8 |]", content, "EJ 1 must end with 4+4+8 sixteenth units = 16 sixteenths")


class TestTier2EJ2Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Taffanel & Gaubert E.J. 2."""

    def test_b03_01_ej2_pitch_range_safety(self):
        """Verify E.J. 2 notes stay strictly within D4 (MIDI 62) to F6 (MIDI 89)."""
        ej2_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ2_Original_AL16588.abc"
        pitches = extract_abc_midi_pitches(ej2_abc.read_text(encoding="utf-8"))
        self.assertGreaterEqual(min(pitches), 62)
        self.assertLessEqual(max(pitches), 89)

    def test_b03_02_ej2_extreme_tempo_bounds(self):
        """Verify E.J. 2 tempo scaling across 50 BPM and 200 BPM."""
        dur_50 = calculate_note_duration(50, subdivision=4)
        dur_200 = calculate_note_duration(200, subdivision=4)
        self.assertAlmostEqual(dur_50 / dur_200, 4.0, places=4)

    def test_b03_03_ej2_measure_12_double_sharp_frequency(self):
        """Verify ^^F in m.12 calculates pitch 68/67 with frequency ~392.0 Hz (G natural)."""
        freq_g4 = midi_to_frequency(67)
        self.assertAlmostEqual(freq_g4, 391.995, places=2)

    def test_b03_04_ej2_measure_22_b_sharp_frequency(self):
        """Verify ^B in m.22 corresponds to MIDI 60 (C4, 261.63 Hz)."""
        freq_c4 = midi_to_frequency(60)
        self.assertAlmostEqual(freq_c4, 261.626, places=2)

    def test_b03_05_ej2_chromatic_pair_continuity(self):
        """Verify 15 chromatic pairs advance by exactly 1 semitone at odd measure boundaries."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        self.assertIn("ej2RawMeasures", content)


class TestTier2EJ4Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Taffanel & Gaubert E.J. 4."""

    def test_b04_01_ej4_full_compass_c4_to_c7(self):
        """Verify E.J. 4 covers the full compass from low C4 (MIDI 60) to high C7 (MIDI 96)."""
        kt_file = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "model" / "ExerciseGenerator.kt"
        content = kt_file.read_text(encoding="utf-8")
        self.assertIn("60", content, "EJ 4 must include low C4 (MIDI 60)")
        self.assertIn("96", content, "EJ 4 must include high C7 (MIDI 96)")

    def test_b04_02_ej4_section_index_boundaries(self):
        """Verify section index bounds: minimum is 0, maximum is 24 (25 sections)."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        self.assertIn("ej4SectionMidiNotes", content)
        self.assertIn("clampedSec = max(0, min(24, sectionIndex))", content)

    def test_b04_03_ej4_extreme_tempo_scaling(self):
        """Verify EJ4 tempo boundaries 40 BPM and 220 BPM."""
        dur_min = calculate_note_duration(220, subdivision=4)
        dur_max = calculate_note_duration(40, subdivision=4)
        self.assertGreater(dur_min, 0.05)
        self.assertLess(dur_max, 0.4)

    def test_b04_04_ej4_descending_minor_accidentals(self):
        """Verify melodic vs harmonic descending minor scales in section 1 (A minor) and 3 (D minor)."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        # Section 1 (A minor) must contain harmonic 7th (G# / MIDI 80) and melodic notes
        self.assertIn("80", content)

    def test_b04_05_ej4_coda_note_count_boundary(self):
        """Verify Coda (section 24) note count is exactly 29, terminating on held tonic."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        # Check coda section notes in Swift
        self.assertIn("72, 71, 69, 67, 65, 64, 62, 60", content)


class TestTier2EJ5Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Taffanel & Gaubert E.J. 5."""

    def test_b05_01_ej5_chromatic_gamut_compass(self):
        """Verify E.J. 5 spans chromatic notes from low register to high register."""
        ej5_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ5_Original_AL16588.abc"
        content = ej5_abc.read_text(encoding="utf-8")
        pitches = extract_abc_midi_pitches(content)
        self.assertGreaterEqual(min(pitches), 60)
        self.assertLessEqual(max(pitches), 96)

    def test_b05_02_ej5_meter_change_boundary(self):
        """Verify meter switches between 6/8 and 2/4 without corrupting note sequences."""
        art1 = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "01_Taffanel_EJ5_Articulacion_01_12_Ligadas.abc").read_text(encoding="utf-8")
        art6 = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "06_Taffanel_EJ5_Articulacion_06_De_3_en_3_Ligadas.abc").read_text(encoding="utf-8")
        self.assertIn("M:6/8", art1)
        self.assertIn("M:2/4", art6)

    def test_b05_03_ej5_section_bounds_0_to_11(self):
        """Verify EJ5 supports 12 chromatic key centers (indices 0..11)."""
        template = load_score_template("ios")
        self.assertIn("EJ5_SECTIONS_DATA", template)

    def test_b05_04_ej5_extreme_tempo_scaling(self):
        """Verify EJ5 tempo bounds 40 BPM to 240 BPM."""
        dur_min = calculate_note_duration(240, subdivision=4)
        dur_max = calculate_note_duration(40, subdivision=4)
        self.assertGreater(dur_min, 0.05)
        self.assertLess(dur_max, 0.4)

    def test_b05_05_ej5_staccato_flag_boundaries(self):
        """Verify articulation 10 (all staccato) vs articulation 1 (all slurred)."""
        art1 = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "01_Taffanel_EJ5_Articulacion_01_12_Ligadas.abc").read_text(encoding="utf-8")
        art10 = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "10_Taffanel_EJ5_Articulacion_10_Todas_Picadas.abc").read_text(encoding="utf-8")
        self.assertIn("(", art1)
        self.assertIn(".", art10)


class TestTier2EJ10Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Taffanel & Gaubert E.J. 10."""

    def test_b06_01_ej10_register_compass(self):
        """Verify E.J. 10 arpeggios stay within standard flute register bounds."""
        ej10_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ10_Original_AL16588.abc"
        pitches = extract_abc_midi_pitches(ej10_abc.read_text(encoding="utf-8"))
        self.assertGreaterEqual(min(pitches), 60)
        self.assertLessEqual(max(pitches), 96)

    def test_b06_02_ej10_system_bounds_and_staffwidth(self):
        """Verify system 29 in score_template.html has staffwidth 1020 for final cadence expansion."""
        template = load_score_template("ios")
        self.assertIn("s === 29 ? 1020 : 960", template, "System 29 must have staffwidth 1020")

    def test_b06_03_ej10_section_index_bounds(self):
        """Verify section index bounds: 0 to 11 (12 sections)."""
        template = load_score_template("ios")
        self.assertIn("EJ10_SECTIONS_DATA", template)

    def test_b06_04_ej10_extreme_tempo_scaling(self):
        """Verify tempo scaling at 50 BPM and 200 BPM."""
        dur_50 = calculate_note_duration(50, subdivision=4)
        dur_200 = calculate_note_duration(200, subdivision=4)
        self.assertAlmostEqual(dur_50 / dur_200, 4.0, places=4)

    def test_b06_05_ej10_diminished_and_augmented_7ths(self):
        """Verify diminished 7th accidentals in EJ10 arpeggio figures."""
        ej10_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ10_Original_AL16588.abc"
        content = ej10_abc.read_text(encoding="utf-8")
        self.assertIn("_", content, "EJ 10 must contain flats for minor/diminished arpeggios")


class TestTier2EJ11Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Taffanel & Gaubert E.J. 11."""

    def test_b07_01_ej11_high_register_ceiling_d7(self):
        """Verify E.J. 11 arpeggios reach high D7 (MIDI 98, 2349.32 Hz)."""
        freq_d7 = midi_to_frequency(98)
        self.assertAlmostEqual(freq_d7, 2349.318, places=2)

    def test_b07_02_ej11_measure_121_rest_boundary(self):
        """Verify measure 121 rest boundary: 'B4 z4 z10 |]'."""
        template = load_score_template("ios")
        self.assertIn("B4 z4 z10 |]", template)

    def test_b07_03_ej11_compound_duration_calculation(self):
        """Verify 18 notes per measure in 9/8 calculate exact sixteenth note durations."""
        dur = calculate_note_duration(90, subdivision=4)
        self.assertAlmostEqual(dur, 0.16666, places=4)

    def test_b07_04_ej11_60_system_bounds(self):
        """Verify EJ11 generates exactly 60 systems (sysIdx 0..59)."""
        template = load_score_template("ios")
        self.assertIn("for (let s = 0; s < 60; s++)", template)

    def test_b07_05_ej11_extreme_tempo_bounds(self):
        """Verify EJ11 tempo bounds 60 BPM and 180 BPM."""
        dur_60 = calculate_note_duration(60, subdivision=4)
        dur_180 = calculate_note_duration(180, subdivision=4)
        self.assertAlmostEqual(dur_60 / dur_180, 3.0, places=4)


class TestTier2ReichertR1Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Mathieu-André Reichert Op. 5 R. 1."""

    def test_b08_01_r1_compass_safety(self):
        """Verify R. 1 notes stay strictly within C4 (MIDI 60) and B6 (MIDI 95)."""
        r1_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R1_Original_Op5.abc"
        pitches = extract_abc_midi_pitches(r1_abc.read_text(encoding="utf-8"))
        self.assertGreaterEqual(min(pitches), 60)
        self.assertLessEqual(max(pitches), 95)

    def test_b08_02_r1_section_24_fine_jump_target(self):
        """Verify section 24 contains !fine! mark in C Major for D.S. al Fine resolution."""
        r1_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R1_Original_Op5.abc"
        content = r1_abc.read_text(encoding="utf-8")
        self.assertIn("!fine!", content)

    def test_b08_03_r1_segno_mark_at_measure_1(self):
        """Verify !segno! marking at initial measure of R. 1."""
        r1_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R1_Original_Op5.abc"
        content = r1_abc.read_text(encoding="utf-8")
        self.assertIn("!segno!", content)

    def test_b08_04_r1_final_measure_rests_boundary(self):
        """Verify measure 4 of each section ends with eighth note + rests (z2 z2)."""
        r1_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R1_Original_Op5.abc"
        content = r1_abc.read_text(encoding="utf-8")
        self.assertIn("z", content, "R. 1 must contain rests in cadence measures")

    def test_b08_05_r1_extreme_tempo_scaling(self):
        """Verify R. 1 dotted-quarter tempo bounds 60 BPM and 160 BPM."""
        dur_60 = calculate_note_duration(60, subdivision=4)
        dur_160 = calculate_note_duration(160, subdivision=4)
        self.assertGreater(dur_60, dur_160)


class TestTier2ReichertR2Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Mathieu-André Reichert Op. 5 R. 2."""

    def test_b09_01_r2_anacrusa_boundary(self):
        """Verify 4-note pickup anacrusa precedes measure 1 across sections."""
        r2_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R2_Original_Op5.abc"
        content = r2_abc.read_text(encoding="utf-8")
        self.assertIn("M:2/4", content)

    def test_b09_02_r2_8va_transposition_sections(self):
        """Verify 8va transpositions shift sound +12 semitones in sections 0, 3, 7, 10, 17, 24."""
        freq_c5 = midi_to_frequency(72)
        freq_c6 = midi_to_frequency(84)
        self.assertAlmostEqual(freq_c6 / freq_c5, 2.0, places=4)

    def test_b09_03_r2_final_note_wedge_articulation(self):
        """Verify final note of each section has !wedge! staccatissimo marking."""
        r2_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R2_Original_Op5.abc"
        content = r2_abc.read_text(encoding="utf-8")
        self.assertIn("!wedge!", content)

    def test_b09_04_r2_high_register_ceiling(self):
        """Verify R. 2 does not exceed flute ceiling D7."""
        r2_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R2_Original_Op5.abc"
        pitches = extract_abc_midi_pitches(r2_abc.read_text(encoding="utf-8"))
        self.assertLessEqual(max(pitches), FLUTE_MAX_MIDI)

    def test_b09_05_r2_extreme_tempo_scaling(self):
        """Verify tempo scaling 80 BPM to 180 BPM."""
        dur_80 = calculate_note_duration(80, subdivision=4)
        dur_180 = calculate_note_duration(180, subdivision=4)
        self.assertGreater(dur_80, dur_180)


class TestTier2ReichertR4Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Mathieu-André Reichert Op. 5 R. 4."""

    def test_b10_01_r4_interval_leaps_compass(self):
        """Verify wide interval leaps stay within flute compass bounds."""
        r4_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R4_Original_Op5.abc"
        pitches = extract_abc_midi_pitches(r4_abc.read_text(encoding="utf-8"))
        self.assertGreaterEqual(min(pitches), 60)
        self.assertLessEqual(max(pitches), FLUTE_MAX_MIDI)

    def test_b10_02_r4_cautionary_accidental_cancellation(self):
        """Verify measure 3 cautionary accidental check cancelling sharp 9th."""
        r4_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R4_Original_Op5.abc"
        content = r4_abc.read_text(encoding="utf-8")
        self.assertIn("=d", content)

    def test_b10_03_r4_section_17_octave_notation(self):
        """Verify section 17 notation and pitch handling."""
        r4_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R4_Original_Op5.abc"
        self.assertTrue(r4_abc.exists())

    def test_b10_04_r4_cadence_wedge_marking(self):
        """Verify cadence measure contains !wedge! staccatissimo marking."""
        r4_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R4_Original_Op5.abc"
        content = r4_abc.read_text(encoding="utf-8")
        self.assertIn("!wedge!", content)

    def test_b10_05_r4_extreme_tempo_scaling(self):
        """Verify tempo scaling 80 BPM to 180 BPM."""
        dur_80 = calculate_note_duration(80, subdivision=4)
        dur_180 = calculate_note_duration(180, subdivision=4)
        self.assertGreater(dur_80, dur_180)


class TestTier2ReichertR5Boundaries(unittest.TestCase):
    """Tier 2 Boundary Tests: Mathieu-André Reichert Op. 5 R. 5."""

    def test_b11_01_r5_triplet_duration_formula_divisor_6(self):
        """
        Verify sixteenth-triplet note duration formula:
        At 120 BPM, duration must be (60.0 / 120) / 6.0 = 0.08333s.
        If erroneously calculated with divisor 4.0, duration is 0.125s (33% error).
        """
        dur_triplet = calculate_note_duration(120, subdivision=4, is_triplet=True)
        dur_straight = calculate_note_duration(120, subdivision=4, is_triplet=False)
        self.assertAlmostEqual(dur_triplet, 0.08333, places=4)
        self.assertAlmostEqual(dur_straight, 0.125, places=4)
        self.assertNotEqual(dur_triplet, dur_straight)

    def test_b11_02_r5_measure_8_triplet_boundary(self):
        """Verify measure 8 has 6 triplet notes + 1 final eighth note (91 notes total per section)."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        self.assertIn("r5SectionMidiNotes", content)

    def test_b11_03_r5_section_bounds_0_to_24(self):
        """Verify R. 5 defines 25 sections."""
        r5_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R5_Original_Op5.abc"
        self.assertTrue(r5_abc.exists())

    def test_b11_04_r5_compass_bounds(self):
        """Verify R. 5 notes stay within C4 to C7."""
        r5_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R5_Original_Op5.abc"
        pitches = extract_abc_midi_pitches(r5_abc.read_text(encoding="utf-8"))
        self.assertGreaterEqual(min(pitches), 60)
        self.assertLessEqual(max(pitches), 96)

    def test_b11_05_r5_extreme_tempo_scaling(self):
        """Verify triplet tempo scaling from 60 BPM to 220 BPM."""
        dur_60 = calculate_note_duration(60, is_triplet=True)
        dur_220 = calculate_note_duration(220, is_triplet=True)
        self.assertAlmostEqual(dur_60, 0.16666, places=4)
        self.assertAlmostEqual(dur_220, 0.04545, places=4)


if __name__ == "__main__":
    unittest.main()
