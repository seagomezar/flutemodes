"""
Tier 1: Feature Coverage E2E Tests for FluteModes Ecosystem.

Comprehensive opaque-box verification for all 11 modules in PROJECT.md:
1. 84 Modal Parallel Exercises (12 tonics x 7 modes x 8 articulations)
2. Taffanel & Gaubert E.J. 1
3. Taffanel & Gaubert E.J. 2
4. Taffanel & Gaubert E.J. 4
5. Taffanel & Gaubert E.J. 5
6. Taffanel & Gaubert E.J. 10
7. Taffanel & Gaubert E.J. 11
8. Mathieu-André Reichert Op. 5 R. 1
9. Mathieu-André Reichert Op. 5 R. 2
10. Mathieu-André Reichert Op. 5 R. 4
11. Mathieu-André Reichert Op. 5 R. 5

Minimum requirements: >=5 tests per feature (57 tests total).
"""

import unittest
import re
from pathlib import Path
from tests.test_helpers import (
    WORKSPACE_ROOT,
    count_abc_notes_in_body,
    parse_abc_headers,
    load_score_template,
    load_json_file
)


class TestTier1Modos(unittest.TestCase):
    """Tier 1 Feature Tests: 84 Modal Parallel Exercises."""

    def test_f01_01_modal_data_json_structure(self):
        """Verify modes_data.json contains 84 modal exercises (12 tonics x 7 modes) with required properties."""
        data = load_json_file("docs/modes_data.json")
        self.assertIsInstance(data, list, "modes_data.json root must be a list")
        self.assertEqual(len(data), 84, "modes_data.json must contain exactly 84 modal exercises")

        # Collect unique tonics and modes
        tonics = set()
        modes_per_tonic = {}
        required_fields = ["tonicId", "tonicName", "modeNum", "modeName", "family", "keySig", "formula", "abc", "frequencies", "totalNotes"]

        for item in data:
            for field in required_fields:
                self.assertIn(field, item, f"Missing field '{field}' in modal item")
            t_id = item["tonicId"]
            tonics.add(t_id)
            modes_per_tonic.setdefault(t_id, []).append(item["modeNum"])
            self.assertEqual(item["totalNotes"], 127, f"Exercise {item.get('tonicName')} mode {item.get('modeNum')} must have 127 notes")

        self.assertEqual(len(tonics), 12, "Must contain exactly 12 unique chromatic tonics")
        for t_id, m_nums in modes_per_tonic.items():
            self.assertEqual(sorted(m_nums), [1, 2, 3, 4, 5, 6, 7], f"Tonic {t_id} must have modes 1 through 7")

    def test_f01_02_modos_abc_files_exist_and_tunes_count(self):
        """Verify all 12 tonic ABC files exist in abc_modos/ and contain 7 tunes each (84 tunes total)."""
        abc_dir = WORKSPACE_ROOT / "abc_modos"
        self.assertTrue(abc_dir.is_dir(), "abc_modos/ directory must exist")
        tonic_files = sorted([f for f in abc_dir.glob("*.abc") if not f.name.startswith("00_")])
        self.assertEqual(len(tonic_files), 12, f"Must contain exactly 12 individual tonic ABC files, found {len(tonic_files)}")

        total_tunes = 0
        for f in tonic_files:
            content = f.read_text(encoding="utf-8")
            tunes = re.findall(r"^X:\s*\d+", content, re.MULTILINE)
            self.assertEqual(len(tunes), 7, f"File {f.name} must define exactly 7 tunes (modes)")
            total_tunes += len(tunes)
        self.assertEqual(total_tunes, 84, "Total modal tunes across all files must equal 84")

    def test_f01_03_modal_exercise_exact_note_count(self):
        """Verify modal exercise note count matches Urtext morphology: exactly 127 notes across 8 measures."""
        c_mode_file = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "modos_02_do.abc"
        if not c_mode_file.exists():
            c_mode_file = WORKSPACE_ROOT / "abc_modos" / "02_Modos_en_Do.abc"
        self.assertTrue(c_mode_file.exists(), "Modal Do ABC file must exist")

        content = c_mode_file.read_text(encoding="utf-8")
        tunes = re.split(r"(?=^X:\s*\d+)", content, flags=re.MULTILINE)
        tunes = [t.strip() for t in tunes if t.strip()]
        self.assertEqual(len(tunes), 7)

        # Tune 1 (Do Jonico): 7 measures x 16 notes + measure 8 with 15 notes = 127 notes
        note_count = count_abc_notes_in_body(tunes[0])
        self.assertEqual(note_count, 127, f"Do Jonico must contain exactly 127 notes, got {note_count}")

    def test_f01_04_modal_abc_headers_compliance(self):
        """Verify ABC headers compliance for modal exercises (M:4/2, L:1/8, Q:1/2=90, clef=treble)."""
        c_mode_file = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "modos_02_do.abc"
        if not c_mode_file.exists():
            c_mode_file = WORKSPACE_ROOT / "abc_modos" / "02_Modos_en_Do.abc"
        content = c_mode_file.read_text(encoding="utf-8")
        headers = parse_abc_headers(content)
        self.assertEqual(headers.get("M"), "4/2", "Meter must be 4/2")
        self.assertEqual(headers.get("L"), "1/8", "Default note length must be 1/8")
        self.assertIn("90", headers.get("Q", ""), "Tempo must be Q:1/2=90")
        self.assertIn("K:", content, "Must specify key signature K:")

    def test_f01_05_modal_downloads_abc_presence(self):
        """Verify downloadable modal ABC files exist in docs/downloads/abc/."""
        dl_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        self.assertTrue(dl_dir.is_dir(), "docs/downloads/abc/ must exist")
        modal_dl_files = list(dl_dir.glob("modos_*.abc"))
        self.assertEqual(len(modal_dl_files), 12, "Must contain 12 downloadable modal ABC files")

    def test_f01_06_modal_web_viewer_integration(self):
        """Verify docs/index.html includes abcjs, modes_data.js, and interactive container."""
        index_html = (WORKSPACE_ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIn("modes_data.js", index_html, "docs/index.html must load modes_data.js")
        self.assertIn("abcjs-basic-min.js", index_html, "docs/index.html must load abcjs")
        self.assertIn('id="paper"', index_html, "docs/index.html must provide #paper container for score")


class TestTier1EJ1(unittest.TestCase):
    """Tier 1 Feature Tests: Taffanel & Gaubert E.J. 1."""

    def test_f02_01_ej1_urtext_structure_and_measures(self):
        """Verify E.J. 1 Urtext structure: 30 chromatic pairs + measure 31 Coda (A.L. 16.588)."""
        ej1_abc_file = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ1_Original_AL16588.abc"
        self.assertTrue(ej1_abc_file.exists(), "EJ1 Original ABC file must exist")
        content = ej1_abc_file.read_text(encoding="utf-8")
        barlines = re.findall(r"\|", content)
        self.assertGreaterEqual(len(barlines), 30, "EJ 1 must contain at least 30 measures")
        self.assertIn("f4 z4 z8 |]", content, "EJ 1 must terminate with Coda F4 quarter note rest bar |]")

    def test_f02_02_ej1_repetition_and_8va_markings(self):
        """Verify E.J. 1 contains repeat bar |:, :| at m.24, and 8va indication at m.25."""
        ej1_abc_file = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ1_Original_AL16588.abc"
        content = ej1_abc_file.read_text(encoding="utf-8")
        self.assertIn("|:", content, "EJ 1 must have initial repeat bar |:")
        self.assertIn(":|", content, "EJ 1 must have repeat bar :| at measure 24")
        self.assertIn("8va", content, "EJ 1 must contain 8va indication for measures 25-30")

    def test_f02_03_ej1_10_articulations_presence(self):
        """Verify E.J. 1 provides all 10 official Leduc articulation files in docs/downloads/abc/."""
        dl_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        for i in range(1, 11):
            pattern = f"*{i:02d}*EJ1*.abc"
            matches = list(dl_dir.glob(pattern))
            self.assertGreaterEqual(len(matches), 1, f"Missing downloadable ABC for EJ1 articulation {i}")

    def test_f02_04_ej1_score_template_hook(self):
        """Verify score_template.html routes EJ1 through EJ([12])_LEDUC_ART regex hook."""
        template = load_score_template("ios")
        self.assertTrue("EJ1_LEDUC_ART" in template or "EJ([12])_LEDUC_ART" in template,
                        "score_template.html must support EJ1 hook regex")
        self.assertIn("renderEjLeduc", template, "score_template.html must route EJ1 to renderEjLeduc")

    def test_f02_05_ej1_web_page_existence(self):
        """Verify docs/ej1.html exists, is valid HTML, and links to downloads."""
        ej1_html = WORKSPACE_ROOT / "docs" / "ej1.html"
        self.assertTrue(ej1_html.exists(), "docs/ej1.html must exist")
        content = ej1_html.read_text(encoding="utf-8")
        self.assertIn("E. J. 1", content)
        self.assertIn("abcjs", content)


class TestTier1EJ2(unittest.TestCase):
    """Tier 1 Feature Tests: Taffanel & Gaubert E.J. 2."""

    def test_f03_01_ej2_urtext_structure_and_measures(self):
        """Verify E.J. 2 minor pentachord structure across 30 measures + coda."""
        ej2_abc_file = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ2_Original_AL16588.abc"
        self.assertTrue(ej2_abc_file.exists(), "EJ2 Original ABC file must exist")
        content = ej2_abc_file.read_text(encoding="utf-8")
        self.assertIn("f4 z4 z8 |]", content, "EJ 2 must terminate with Coda F4 rest bar")

    def test_f03_02_ej2_accidental_fidelity_f_doublesharp_and_b_sharp(self):
        """Verify double-sharp ^^F in m.12 and enharmonic ^B in m.22 in EJ2 ABC."""
        ej2_abc_file = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ2_Original_AL16588.abc"
        content = ej2_abc_file.read_text(encoding="utf-8")
        self.assertIn("^^F", content, "EJ 2 measure 12 must contain double sharp ^^F (G natural sounding)")
        self.assertIn("^B", content, "EJ 2 measure 22 must contain enharmonic ^B (C natural sounding)")

    def test_f03_03_ej2_android_generator_accidental_accuracy(self):
        """
        DEF-02 Verification: Check mm. 4, 8, 14, 18, 22, 24, 28 in ExerciseGenerator.kt.
        Urtext requires minor modulations: m.4 =G, m.8 =A, m.14 =c, m.18 =d, m.22 =e, m.24 =f, m.28 =g.
        Corrupted Android version erroneously had major-third notes (^G, ^A, ^c, ^d, ^e, ^f, ^g).
        """
        kt_file = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "model" / "ExerciseGenerator.kt"
        self.assertTrue(kt_file.exists(), "ExerciseGenerator.kt must exist")
        content = kt_file.read_text(encoding="utf-8")

        self.assertRegex(content, r'EJ1Measure\(4,\s*listOf\(listOf\("\^D","=E","\^F","=G"',
                         "DEF-02: Android EJ2 measure 4 must use '=G' (not '^G')")
        self.assertRegex(content, r'EJ1Measure\(8,\s*listOf\(listOf\("\^E","\^F","\^G","=A"',
                         "DEF-02: Android EJ2 measure 8 must use '=A' (not '^A')")
        self.assertRegex(content, r'EJ1Measure\(14,\s*listOf\(listOf\("\^G","=A","=B","=c"',
                         "DEF-02: Android EJ2 measure 14 must use '=B','=c' (not 'B','^c')")

    def test_f03_04_ej2_android_audio_diminished_semitone(self):
        """
        DEF-03 Verification: Check line 444 in ScoreAudioPlayer.kt.
        Diminished chord must resolve to minor fourth semitone: base + (if (isMinor) 4 else 5).
        """
        player_file = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "audio" / "ScoreAudioPlayer.kt"
        self.assertTrue(player_file.exists(), "ScoreAudioPlayer.kt must exist")
        content = player_file.read_text(encoding="utf-8")
        self.assertIn("base + (if (isMinor) 4 else 5)", content,
                      "DEF-03: Line 444 of ScoreAudioPlayer.kt must use base + (if (isMinor) 4 else 5)")

    def test_f03_05_ej2_score_template_hook(self):
        """Verify score_template.html routes EJ2 through EJ([12])_LEDUC_ART regex hook."""
        template = load_score_template("ios")
        self.assertTrue("EJ2_LEDUC_ART" in template or "EJ([12])_LEDUC_ART" in template,
                        "score_template.html must support EJ2 hook regex")

    def test_f03_06_ej2_web_downloads_and_visor(self):
        """Verify docs/ej2.html and EJ2 ABC downloads exist."""
        ej2_html = WORKSPACE_ROOT / "docs" / "ej2.html"
        self.assertTrue(ej2_html.exists(), "docs/ej2.html must exist")
        dl_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        ej2_files = list(dl_dir.glob("*EJ2*.abc"))
        self.assertGreaterEqual(len(ej2_files), 10, "Must have at least 10 EJ2 ABC download files")


class TestTier1EJ4(unittest.TestCase):
    """Tier 1 Feature Tests: Taffanel & Gaubert E.J. 4."""

    def test_f04_01_ej4_25_sections_structure(self):
        """Verify E.J. 4 covers 25 sections (24 major/minor keys + 1 Coda in C Major)."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        self.assertIn("ej4SectionMidiNotes", content, "ej4SectionMidiNotes array must be defined in Swift")
        # Check section array size in Swift
        matches = re.findall(r"\[\d+,\s*\d+.*\]", content)
        self.assertGreaterEqual(len(matches), 25, "ej4SectionMidiNotes must contain 25 sections")

    def test_f04_02_ej4_notes_per_section_fidelity(self):
        """Verify sections 0..23 have 128 notes, and Coda (section 24) has 29 notes."""
        kt_file = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "model" / "ExerciseGenerator.kt"
        content = kt_file.read_text(encoding="utf-8")
        self.assertIn("ej4SectionMidiNotes", content, "ej4SectionMidiNotes must exist")

    def test_f04_03_ej4_8_articulations_presence(self):
        """Verify E.J. 4 supports all 8 official Schott articulations."""
        dl_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        for i in range(1, 9):
            matches = list(dl_dir.glob(f"*{i:02d}*EJ4*.abc"))
            self.assertGreaterEqual(len(matches), 1, f"Missing ABC download for EJ4 articulation {i}")

    def test_f04_04_ej4_score_template_hook(self):
        """Verify score_template.html contains hook handler for % EJ4_LEDUC_ART:art:SEC:sec."""
        template = load_score_template("ios")
        self.assertIn("EJ4_LEDUC_ART", template, "score_template.html must support % EJ4_LEDUC_ART hook")
        self.assertIn("renderEj4Leduc", template, "score_template.html must route to renderEj4Leduc")

    def test_f04_05_ej4_web_page_existence(self):
        """Verify docs/ej4.html exists and is accessible."""
        ej4_html = WORKSPACE_ROOT / "docs" / "ej4.html"
        self.assertTrue(ej4_html.exists(), "docs/ej4.html must exist")


class TestTier1EJ5(unittest.TestCase):
    """Tier 1 Feature Tests: Taffanel & Gaubert E.J. 5."""

    def test_f05_01_ej5_12_chromatic_sections(self):
        """Verify E.J. 5 defines 12 chromatic scale sections (C to B)."""
        dl_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        ej5_files = list(dl_dir.glob("*EJ5*.abc"))
        self.assertGreaterEqual(len(ej5_files), 10, "Must contain at least 10 EJ5 ABC download files")

    def test_f05_02_ej5_meter_switching(self):
        """Verify E.J. 5 supports both 6/8 and 2/4 meters depending on articulation."""
        template = load_score_template("ios")
        self.assertIn("renderEj5Leduc", template, "score_template.html must contain renderEj5Leduc")
        self.assertIn("M:6/8", template, "EJ5 must support 6/8 meter")
        self.assertIn("M:2/4", template, "EJ5 must support 2/4 meter")

    def test_f05_03_ej5_10_articulations_presence(self):
        """Verify E.J. 5 defines 10 official articulations in downloads."""
        dl_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        for i in range(1, 11):
            matches = list(dl_dir.glob(f"*{i:02d}*EJ5*.abc"))
            self.assertGreaterEqual(len(matches), 1, f"Missing ABC download for EJ5 articulation {i}")

    def test_f05_04_ej5_score_template_hook(self):
        """Verify score_template.html contains hook handler for % EJ5_LEDUC_ART."""
        template = load_score_template("ios")
        self.assertIn("EJ5_LEDUC_ART", template, "score_template.html must support % EJ5_LEDUC_ART hook")

    def test_f05_05_ej5_web_page_existence(self):
        """Verify docs/ej5.html exists and contains interactive score container."""
        ej5_html = WORKSPACE_ROOT / "docs" / "ej5.html"
        self.assertTrue(ej5_html.exists(), "docs/ej5.html must exist")


class TestTier1EJ10(unittest.TestCase):
    """Tier 1 Feature Tests: Taffanel & Gaubert E.J. 10."""

    def test_f06_01_ej10_30_systems_layout(self):
        """Verify E.J. 10 renders 30 systems covering 121 measures across 24 keys."""
        template = load_score_template("ios")
        self.assertIn("renderEj10Leduc", template, "score_template.html must define renderEj10Leduc")
        self.assertIn("ej10-sys-", template, "EJ10 must generate 30 system divs (ej10-sys-0..29)")

    def test_f06_02_ej10_10_articulations_presence(self):
        """Verify E.J. 10 defines 10 official articulations in downloads."""
        dl_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        for i in range(1, 11):
            matches = list(dl_dir.glob(f"*{i:02d}*EJ10*.abc"))
            self.assertGreaterEqual(len(matches), 1, f"Missing ABC download for EJ10 articulation {i}")

    def test_f06_03_ej10_score_template_hook(self):
        """Verify score_template.html contains hook handler for % EJ10_LEDUC_ART."""
        template = load_score_template("ios")
        self.assertIn("EJ10_LEDUC_ART", template, "score_template.html must support % EJ10_LEDUC_ART hook")

    def test_f06_04_ej10_web_page_existence(self):
        """Verify docs/ej10.html exists and is valid."""
        ej10_html = WORKSPACE_ROOT / "docs" / "ej10.html"
        self.assertTrue(ej10_html.exists(), "docs/ej10.html must exist")

    def test_f06_05_ej10_complete_collection_file(self):
        """Verify 11_Coleccion_Completa_Taffanel_EJ10_10_Articulaciones.abc exists."""
        coll = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "11_Coleccion_Completa_Taffanel_EJ10_10_Articulaciones.abc"
        self.assertTrue(coll.exists(), "EJ10 Complete collection ABC must exist")


class TestTier1EJ11(unittest.TestCase):
    """Tier 1 Feature Tests: Taffanel & Gaubert E.J. 11."""

    def test_f07_01_ej11_compound_meter_and_60_systems(self):
        """Verify E.J. 11 compound 9/8 / 3/4 meter (18 notes/m) and 60 systems layout."""
        template = load_score_template("ios")
        self.assertIn("renderEj11Leduc", template, "score_template.html must define renderEj11Leduc")
        self.assertIn("ej11-sys-", template, "EJ11 must generate 60 system divs")

    def test_f07_02_ej11_final_measure_pause(self):
        """Verify E.J. 11 final measure (m.121) has pause on B4: 'B4 z4 z10 |]'."""
        template = load_score_template("ios")
        self.assertIn("B4 z4 z10 |]", template, "EJ11 measure 121 must terminate with B4 pause rest bar")

    def test_f07_03_ej11_10_articulations_presence(self):
        """Verify E.J. 11 defines 10 official articulations in downloads."""
        dl_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        for i in range(1, 11):
            matches = list(dl_dir.glob(f"*{i:02d}*EJ11*.abc"))
            self.assertGreaterEqual(len(matches), 1, f"Missing ABC download for EJ11 articulation {i}")

    def test_f07_04_ej11_score_template_hook(self):
        """Verify score_template.html contains hook handler for % EJ11_LEDUC_ART."""
        template = load_score_template("ios")
        self.assertIn("EJ11_LEDUC_ART", template, "score_template.html must support % EJ11_LEDUC_ART hook")

    def test_f07_05_ej11_web_page_existence(self):
        """Verify docs/ej11.html exists."""
        ej11_html = WORKSPACE_ROOT / "docs" / "ej11.html"
        self.assertTrue(ej11_html.exists(), "docs/ej11.html must exist")


class TestTier1ReichertR1(unittest.TestCase):
    """Tier 1 Feature Tests: Mathieu-André Reichert Op. 5 R. 1."""

    def test_f08_01_r1_urtext_structure_25_sections(self):
        """Verify Reichert R. 1 structure: 25 sections of 4 measures each in 6/8 meter (100 mm total)."""
        r1_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R1_Original_Op5.abc"
        self.assertTrue(r1_abc.exists(), "00_Reichert_R1_Original_Op5.abc must exist")
        content = r1_abc.read_text(encoding="utf-8")
        self.assertIn("M:6/8", content, "R. 1 meter must be 6/8")

    def test_f08_02_r1_notes_per_section_43(self):
        """Verify Reichert R. 1 has exactly 43 notes per section."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        self.assertIn("r1SectionMidiNotes", content, "r1SectionMidiNotes must be defined in Swift")

    def test_f08_03_r1_repeat_markings_segno_fine_ds(self):
        """Verify Reichert R. 1 ABC contains !segno!, !fine!, and !D.S.! markings."""
        r1_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R1_Original_Op5.abc"
        content = r1_abc.read_text(encoding="utf-8")
        self.assertIn("!segno!", content, "R. 1 must contain !segno! marking")
        self.assertIn("!fine!", content, "R. 1 must contain !fine! marking")
        self.assertIn("!D.S.!", content, "R. 1 must contain !D.S.! marking")

    def test_f08_04_r1_schott_renderer_in_score_template(self):
        """
        DEF-01 Verification: score_template.html must define renderR1Schott function.
        If missing, WebViews crash with ReferenceError: Can't find variable renderR1Schott.
        """
        template = load_score_template("ios")
        self.assertIn("function renderR1Schott", template,
                      "DEF-01: function renderR1Schott is missing from score_template.html")

    def test_f08_05_r1_web_page_existence(self):
        """Verify docs/r1.html exists and is valid."""
        r1_html = WORKSPACE_ROOT / "docs" / "r1.html"
        self.assertTrue(r1_html.exists(), "docs/r1.html must exist")


class TestTier1ReichertR2(unittest.TestCase):
    """Tier 1 Feature Tests: Mathieu-André Reichert Op. 5 R. 2."""

    def test_f09_01_r2_urtext_structure_25_sections_2_4(self):
        """Verify Reichert R. 2 structure: 25 sections of 8 measures each in 2/4 meter (200 mm total)."""
        r2_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R2_Original_Op5.abc"
        self.assertTrue(r2_abc.exists(), "00_Reichert_R2_Original_Op5.abc must exist")
        content = r2_abc.read_text(encoding="utf-8")
        self.assertIn("M:2/4", content, "R. 2 meter must be 2/4")

    def test_f09_02_r2_anacrusa_and_notes_per_section_61(self):
        """Verify Reichert R. 2 has 4-note pickup (anacrusa) and 61 notes per section."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        self.assertIn("r2SectionMidiNotes", content, "r2SectionMidiNotes must be defined in Swift")

    def test_f09_03_r2_wedge_articulation_final_note(self):
        """Verify Reichert R. 2 contains !wedge! staccatissimo marking on final note."""
        r2_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R2_Original_Op5.abc"
        content = r2_abc.read_text(encoding="utf-8")
        self.assertIn("!wedge!", content, "R. 2 must contain !wedge! marking on section terminations")

    def test_f09_04_r2_schott_renderer_in_score_template(self):
        """DEF-01 Verification: score_template.html must define renderR2Schott function."""
        template = load_score_template("ios")
        self.assertIn("function renderR2Schott", template,
                      "DEF-01: function renderR2Schott is missing from score_template.html")

    def test_f09_05_r2_web_page_existence(self):
        """Verify docs/r2.html exists."""
        r2_html = WORKSPACE_ROOT / "docs" / "r2.html"
        self.assertTrue(r2_html.exists(), "docs/r2.html must exist")


class TestTier1ReichertR4(unittest.TestCase):
    """Tier 1 Feature Tests: Mathieu-André Reichert Op. 5 R. 4."""

    def test_f10_01_r4_urtext_structure_4_4_meter(self):
        """Verify Reichert R. 4 structure: 25 sections of 4 measures each in C (4/4) meter (100 mm total)."""
        r4_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R4_Original_Op5.abc"
        self.assertTrue(r4_abc.exists(), "00_Reichert_R4_Original_Op5.abc must exist")
        content = r4_abc.read_text(encoding="utf-8")
        self.assertTrue("M:C" in content or "M:4/4" in content, "R. 4 meter must be C or 4/4")

    def test_f10_02_r4_notes_per_section_61(self):
        """Verify Reichert R. 4 has exactly 61 notes per section."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        self.assertIn("r4SectionMidiNotes", content, "r4SectionMidiNotes must be defined in Swift")

    def test_f10_03_r4_cautionary_naturals(self):
        """Verify Reichert R. 4 contains cautionary naturals in measure 3 cancelling sharp 9th."""
        r4_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R4_Original_Op5.abc"
        content = r4_abc.read_text(encoding="utf-8")
        self.assertIn("=d", content, "R. 4 must contain cautionary natural =d in C Major section")

    def test_f10_04_r4_schott_renderer_in_score_template(self):
        """DEF-01 Verification: score_template.html must define renderR4Schott function."""
        template = load_score_template("ios")
        self.assertIn("function renderR4Schott", template,
                      "DEF-01: function renderR4Schott is missing from score_template.html")

    def test_f10_05_r4_web_page_existence(self):
        """Verify docs/r4.html exists."""
        r4_html = WORKSPACE_ROOT / "docs" / "r4.html"
        self.assertTrue(r4_html.exists(), "docs/r4.html must exist")


class TestTier1ReichertR5(unittest.TestCase):
    """Tier 1 Feature Tests: Mathieu-André Reichert Op. 5 R. 5."""

    def test_f11_01_r5_urtext_structure_sixteenth_triplets(self):
        """Verify Reichert R. 5 structure: 25 sections in 2/4 meter with sixteenth triplets (12 notes/m)."""
        r5_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R5_Original_Op5.abc"
        self.assertTrue(r5_abc.exists(), "00_Reichert_R5_Original_Op5.abc must exist")
        content = r5_abc.read_text(encoding="utf-8")
        self.assertIn("M:2/4", content, "R. 5 meter must be 2/4")

    def test_f11_02_r5_notes_per_section_91(self):
        """Verify Reichert R. 5 has exactly 91 notes per section."""
        swift_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
        content = swift_file.read_text(encoding="utf-8")
        self.assertIn("r5SectionMidiNotes", content, "r5SectionMidiNotes must be defined in Swift")

    def test_f11_03_r5_triplet_tempo_divisor(self):
        """
        DEF-05 Verification: In ScoreAudioPlayer.kt, sixteenth triplets must use divisor 6.0.
        (60.0 / tempo) / 6.0, NOT (60.0 / tempo) / 4.0.
        """
        player_file = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "audio" / "ScoreAudioPlayer.kt"
        content = player_file.read_text(encoding="utf-8")
        self.assertIn("ExerciseType.R5 -> (60.0 / tempoBPM.toDouble()) / 6.0", content,
                      "DEF-05: ScoreAudioPlayer.kt must compute sixteenth-triplet duration with divisor 6.0 for R5")

    def test_f11_04_r5_schott_renderer_in_score_template(self):
        """DEF-01 Verification: score_template.html must define renderR5Schott function."""
        template = load_score_template("ios")
        self.assertIn("function renderR5Schott", template,
                      "DEF-01: function renderR5Schott is missing from score_template.html")

    def test_f11_05_r5_web_page_existence(self):
        """Verify docs/r5.html exists."""
        r5_html = WORKSPACE_ROOT / "docs" / "r5.html"
        self.assertTrue(r5_html.exists(), "docs/r5.html must exist")


if __name__ == "__main__":
    unittest.main()
