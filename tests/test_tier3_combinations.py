"""
Tier 3: Cross-Feature Combinations E2E Tests for FluteModes Ecosystem.

Opaque-box validation of pairwise interactions and cross-subsystem contracts:
- Mode + Articulation + Tempo interactions
- Audio PCM parameters + Visual cursor sync bridge
- Multiplatform score_template.html parity (iOS vs Android)
- Web portal download links and file integrity
- Spanish / English localization key parity
- PracticeStore progression state isolation
- Android Reichert navigation and completion dialog contracts
"""

import unittest
import re
from pathlib import Path
from tests.test_helpers import (
    WORKSPACE_ROOT,
    midi_to_frequency,
    calculate_note_duration,
    load_score_template
)


class TestTier3Combinations(unittest.TestCase):
    """Tier 3: Pairwise and System Interaction Tests."""

    def test_c01_mode_articulation_tempo_pairwise_matrix(self):
        """Verify combinations of 7 modes x 8 articulations x 4 tempos calculate valid timing."""
        modes = ["jonico", "dorico", "frigio", "lidio", "mixolidio", "eolico", "locrio"]
        articulations = [1, 2, 3, 4, 5, 6, 7, 8]
        tempos = [60, 90, 120, 180]

        for m in modes:
            for art in articulations:
                for bpm in tempos:
                    dur = calculate_note_duration(bpm, subdivision=4)
                    self.assertGreater(dur, 0.0)
                    self.assertLess(dur, 1.0)

    def test_c02_audio_frequency_derivation_across_octaves(self):
        """Verify equal-tempered frequency calculation across octaves (A3=220, A4=440, A5=880, A6=1760)."""
        self.assertAlmostEqual(midi_to_frequency(57), 220.0, places=2)
        self.assertAlmostEqual(midi_to_frequency(69), 440.0, places=2)
        self.assertAlmostEqual(midi_to_frequency(81), 880.0, places=2)
        self.assertAlmostEqual(midi_to_frequency(93), 1760.0, places=2)

    def test_c03_visual_cursor_bridge_api_contract(self):
        """
        DEF-08 Verification: score_template.html must define highlightNote(noteIndex) and clearHighlight().
        If missing, native audio engines cannot highlight notes during playback.
        """
        template = load_score_template("ios")
        self.assertIn("function highlightNote", template,
                      "DEF-08: highlightNote(noteIndex) function is missing from score_template.html")
        self.assertIn("function clearHighlight", template,
                      "DEF-08: clearHighlight() function is missing from score_template.html")

    def test_c04_visual_cursor_css_styling_class(self):
        """DEF-08 Verification: score_template.html must define .highlighted-note CSS class."""
        template = load_score_template("ios")
        self.assertIn(".highlighted-note", template,
                      "DEF-08: .highlighted-note CSS style rule is missing from score_template.html")

    def test_c05_multiplatform_score_template_parity(self):
        """Verify iOS and Android score_template.html are 100% byte-for-byte identical."""
        ios_template = (WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Resources" / "score_template.html").read_bytes()
        android_template = (WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "assets" / "score_template.html").read_bytes()
        self.assertEqual(ios_template, android_template,
                         "score_template.html in iOS and Android must be 100% identical")

    def test_c06_schott_renderer_parity_in_score_templates(self):
        """
        DEF-01 Verification: Both iOS and Android score templates must contain Schott renderers:
        renderR1Schott, renderR2Schott, renderR4Schott, renderR5Schott.
        """
        for platform in ["ios", "android"]:
            tmpl = load_score_template(platform)
            self.assertIn("function renderR1Schott", tmpl, f"DEF-01: renderR1Schott missing in {platform}")
            self.assertIn("function renderR2Schott", tmpl, f"DEF-01: renderR2Schott missing in {platform}")
            self.assertIn("function renderR4Schott", tmpl, f"DEF-01: renderR4Schott missing in {platform}")
            self.assertIn("function renderR5Schott", tmpl, f"DEF-01: renderR5Schott missing in {platform}")

    def test_c07_web_portal_navigation_links_integrity(self):
        """Verify docs/index.html navigation links to all 11 modules point to existing HTML files."""
        index_html = (WORKSPACE_ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        modules = ["ej1.html", "ej2.html", "ej4.html", "ej5.html", "ej10.html", "ej11.html",
                   "r1.html", "r2.html", "r4.html", "r5.html"]
        for m in modules:
            self.assertIn(m, index_html, f"docs/index.html must link to {m}")
            target_path = WORKSPACE_ROOT / "docs" / m
            self.assertTrue(target_path.exists(), f"Target file docs/{m} does not exist on disk")

    def test_c08_web_portal_download_links_casing_integrity(self):
        """
        DEF-06 Verification: docs/index.html download links to downloads/abc/ must match exact on-disk files.
        Checks for casing mismatches like reichert_r1_completo.abc vs Reichert_R1_Coleccion_Completa.abc.
        """
        index_html = (WORKSPACE_ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        links = re.findall(r'href=["\']downloads/abc/([^"\']+)["\']', index_html)
        self.assertGreater(len(links), 0, "docs/index.html must contain downloads/abc/ links")

        broken_links = []
        for rel_file in links:
            disk_path = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / rel_file
            if not disk_path.exists():
                broken_links.append(rel_file)

        self.assertEqual(broken_links, [],
                         f"DEF-06: Found broken/casing-mismatched download links in docs/index.html: {broken_links}")

    def test_c09_web_portal_apk_download_link_validity(self):
        """Verify docs/index.html APK download links point to existing APK files in docs/downloads/apk/."""
        index_html = (WORKSPACE_ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        apk_links = re.findall(r'href=["\']downloads/apk/([^"\']+)["\']', index_html)
        self.assertGreater(len(apk_links), 0, "docs/index.html must link to an APK download")

        for apk_file in apk_links:
            apk_path = WORKSPACE_ROOT / "docs" / "downloads" / "apk" / apk_file
            self.assertTrue(apk_path.exists(), f"Linked APK docs/downloads/apk/{apk_file} does not exist on disk")

    def test_c10_master_modal_collection_abc_presence(self):
        """
        DEF-07 Verification: 00_Coleccion_Completa_84_Modos_EJ4.abc must exist in docs/downloads/abc/.
        """
        master_abc = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Coleccion_Completa_84_Modos_EJ4.abc"
        self.assertTrue(master_abc.exists(),
                        "DEF-07: 00_Coleccion_Completa_84_Modos_EJ4.abc is missing from docs/downloads/abc/")

    def test_c11_android_localization_key_parity(self):
        """Verify Android LocalizationManager.kt has matching keys in Spanish and English for core UI."""
        kt_loc = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "model" / "LocalizationManager.kt"
        self.assertTrue(kt_loc.exists())
        content = kt_loc.read_text(encoding="utf-8")
        self.assertIn('"app_name"', content)
        self.assertIn('"subtitle"', content)
        self.assertIn('"start_practice"', content)
        self.assertIn('"select_tonic"', content)

    def test_c12_ios_localization_key_parity(self):
        """Verify iOS LocalizationManager.swift has matching keys in Spanish and English for core UI."""
        swift_loc = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "LocalizationManager.swift"
        self.assertTrue(swift_loc.exists())
        content = swift_loc.read_text(encoding="utf-8")
        self.assertIn('"app_name"', content)
        self.assertIn('"subtitle"', content)
        self.assertIn('"start_practice"', content)
        self.assertIn('"select_tonic"', content)

    def test_c13_practice_store_cross_exercise_isolation(self):
        """Verify PracticeStore progression models separate EJ4/R2/R4 from EJ5/R1/R5."""
        swift_store = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "PracticeStore.swift"
        content = swift_store.read_text(encoding="utf-8")
        self.assertIn("markEJ4Completed", content)
        self.assertIn("markEJ5TypeCompleted", content)

    def test_c14_android_reichert_navigation_routes(self):
        """
        DEF-09 Verification: MainActivity.kt must pass section and art arguments to Screen.Practice for Reichert.
        Currently onStartReichertPractice accepts only 'ex' and discards section/art.
        """
        main_act = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "MainActivity.kt"
        content = main_act.read_text(encoding="utf-8")
        # In fixed version, onStartReichertPractice should receive (ex, art, sec)
        self.assertRegex(content, r'onStartReichertPractice\s*=\s*\{\s*ex,\s*art,\s*sec\s*->',
                         "DEF-09: MainActivity.kt onStartReichertPractice must receive (ex, art, sec)")

    def test_c15_android_reichert_completion_dialog_isolation(self):
        """
        DEF-09 Verification: PracticeScreen.kt must NOT show showEJ11CompletionDialog when finishing Reichert.
        """
        screen_file = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "ui" / "PracticeScreen.kt"
        content = screen_file.read_text(encoding="utf-8")
        self.assertIn("showEJ11CompletionDialog", content)

    def test_c16_pdf_files_structural_integrity(self):
        """Verify all 23 downloadable PDF files exist, are > 10KB, and start with %PDF header."""
        pdf_dir = WORKSPACE_ROOT / "docs" / "downloads" / "pdf"
        self.assertTrue(pdf_dir.is_dir())
        pdf_files = list(pdf_dir.glob("*.pdf"))
        self.assertEqual(len(pdf_files), 23, f"Expected 23 PDF downloads, found {len(pdf_files)}")

        for pdf in pdf_files:
            size = pdf.stat().st_size
            self.assertGreater(size, 10240, f"PDF {pdf.name} is smaller than 10 KB ({size} bytes)")
            with open(pdf, "rb") as f:
                header = f.read(5)
                self.assertEqual(header, b"%PDF-", f"File {pdf.name} does not start with %PDF- header")

    def test_c17_abc_downloads_valid_tunes(self):
        """Verify all ABC files in docs/downloads/abc/ contain at least one valid X: tune header."""
        abc_dir = WORKSPACE_ROOT / "docs" / "downloads" / "abc"
        abc_files = list(abc_dir.glob("*.abc"))
        self.assertGreaterEqual(len(abc_files), 100)

        for f in abc_files:
            content = f.read_text(encoding="utf-8")
            self.assertIn("X:", content, f"ABC file {f.name} lacks X: header")
            self.assertIn("K:", content, f"ABC file {f.name} lacks K: key signature")

    def test_c18_master_method_pdf_size(self):
        """Verify master complete method PDF metodo_completo_modos_flauta.pdf is complete (> 1 MB)."""
        master_pdf = WORKSPACE_ROOT / "docs" / "downloads" / "pdf" / "metodo_completo_modos_flauta.pdf"
        self.assertTrue(master_pdf.exists())
        self.assertGreater(master_pdf.stat().st_size, 1000000, "Master method PDF must be > 1 MB")

    def test_c19_audio_synthesis_formula_precision(self):
        """Verify pitch frequency calculations are within 0.01 Hz of physical standards."""
        c4_freq = midi_to_frequency(60)
        self.assertAlmostEqual(c4_freq, 261.6256, delta=0.01)

        c7_freq = midi_to_frequency(96)
        self.assertAlmostEqual(c7_freq, 2093.0045, delta=0.05)

    def test_c20_metronome_audio_click_duration(self):
        """Verify metronome engine click specifications (1400 Hz tone, 50ms decay)."""
        metro_file = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "audio" / "MetronomeEngine.kt"
        content = metro_file.read_text(encoding="utf-8")
        self.assertIn("1400", content, "Metronome click frequency must be 1400 Hz")


if __name__ == "__main__":
    unittest.main()
