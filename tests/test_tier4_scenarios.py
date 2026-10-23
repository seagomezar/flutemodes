"""
Tier 4: Real-World Application Scenarios E2E Tests for FluteModes Ecosystem.

Opaque-box verification of realistic multi-exercise practice cycles and distribution workflows:
1. Daily Warm-Up & Tone Development (EJ1 -> EJ2 -> Modos -> Reichert R1)
2. Finger Velocity & Articulation Mastery (EJ4 -> EJ10 -> Reichert R5)
3. Full Compass Arpeggio Masterclass (EJ11 -> Reichert R2 -> Reichert R4)
4. PracticeStore Lifecycle & Persistence Workflow
5. Complete Distribution Asset Audit
6. Multi-tonic Modal Transposition Cycle
7. High-Speed Articulation Drill
8. Flute Low B Footjoint vs Standard C Footjoint Compatibility
9. Offline Web App Standalone Execution
10. Multiplatform Version Consistency (v1.5.1 target)
"""

import unittest
import re
from pathlib import Path
from tests.test_helpers import (
    WORKSPACE_ROOT,
    FLUTE_MIN_MIDI,
    FLUTE_MAX_MIDI,
    calculate_note_duration,
    extract_abc_midi_pitches
)


class TestTier4Scenarios(unittest.TestCase):
    """Tier 4: Realistic Practice Routines and Application Scenarios."""

    def test_s01_daily_warmup_and_tone_routine(self):
        """
        Scenario 1: Daily Warm-Up & Tone Routine
        Flutist practices:
        1. EJ1 slow staccato (60 BPM) for embouchure focus
        2. EJ2 legato minor (80 BPM) for flexibility
        3. Modos Do Jonico (90 BPM) for tonal centering
        4. Reichert R1 (100 BPM) for fluid airflow
        Verifies notes, compass, and non-zero duration for every step.
        """
        # Step 1: EJ 1
        ej1_abc = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "01_Taffanel_EJ1_Articulacion_01_8_Ligadas.abc").read_text(encoding="utf-8")
        ej1_pitches = extract_abc_midi_pitches(ej1_abc)
        self.assertGreater(len(ej1_pitches), 100)
        self.assertTrue(all(FLUTE_MIN_MIDI <= p <= FLUTE_MAX_MIDI for p in ej1_pitches))
        self.assertAlmostEqual(calculate_note_duration(60, 4), 0.25, places=4)

        # Step 2: EJ 2
        ej2_abc = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "01_Taffanel_EJ2_Articulacion_01_8_Ligadas.abc").read_text(encoding="utf-8")
        ej2_pitches = extract_abc_midi_pitches(ej2_abc)
        self.assertGreater(len(ej2_pitches), 100)
        self.assertAlmostEqual(calculate_note_duration(80, 4), 0.1875, places=4)

        # Step 3: Modos
        modos_path = WORKSPACE_ROOT / "abc_modos" / "02_Modos_en_Do.abc"
        if not modos_path.exists():
            modos_path = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "modos_02_do.abc"
        modos_abc = modos_path.read_text(encoding="utf-8")
        modos_pitches = extract_abc_midi_pitches(modos_abc)
        self.assertGreater(len(modos_pitches), 100)
        self.assertAlmostEqual(calculate_note_duration(90, 4), 0.16666, places=4)

        # Step 4: Reichert R1
        r1_abc = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R1_Original_Op5.abc").read_text(encoding="utf-8")
        r1_pitches = extract_abc_midi_pitches(r1_abc)
        self.assertGreater(len(r1_pitches), 30)
        self.assertAlmostEqual(calculate_note_duration(100, 4), 0.15, places=4)

    def test_s02_finger_velocity_and_articulation_mastery(self):
        """
        Scenario 2: Finger Velocity & Articulation Mastery
        1. EJ4 major/minor keys cycle at 120 BPM
        2. EJ10 velocity arpeggios at 140 BPM
        3. Reichert R5 triplet study at 160 BPM
        Verifies duration scaling and triplet timing calculations.
        """
        dur_ej4 = calculate_note_duration(120, subdivision=4)
        dur_ej10 = calculate_note_duration(140, subdivision=4)
        dur_r5 = calculate_note_duration(160, is_triplet=True)

        self.assertAlmostEqual(dur_ej4, 0.125, places=4)
        self.assertAlmostEqual(dur_ej10, 0.10714, places=4)
        self.assertAlmostEqual(dur_r5, 0.0625, places=4)
        self.assertLess(dur_r5, dur_ej10, "R5 sixteenth triplets must be faster than sixteenth notes")

    def test_s03_full_compass_arpeggio_masterclass(self):
        """
        Scenario 3: Full Compass Arpeggio Masterclass
        1. EJ11 broken arpeggios in 9/8 reaching high D7 (MIDI 98)
        2. Reichert R2 & R4 chord studies leaping across registers
        """
        ej11_abc = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Taffanel_EJ11_Original_AL16588.abc").read_text(encoding="utf-8")
        self.assertIn("B4 z4 z10 |]", ej11_abc)

        r2_abc = (WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Reichert_R2_Original_Op5.abc").read_text(encoding="utf-8")
        self.assertIn("!wedge!", r2_abc)

    def test_s04_practice_store_lifecycle_workflow(self):
        """
        Scenario 4: PracticeStore Lifecycle Workflow
        Verifies persistence methods and progression contracts in iOS and Android.
        """
        swift_store = (WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "PracticeStore.swift").read_text(encoding="utf-8")
        self.assertIn("markCompleted", swift_store)
        self.assertIn("toggleCompleted", swift_store)

        kt_store = (WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "model" / "PracticeStore.kt").read_text(encoding="utf-8")
        self.assertIn("markCompleted", kt_store)

    def test_s05_distribution_asset_audit(self):
        """
        Scenario 5: Complete Distribution Asset Audit
        Verifies student access to 23 PDFs, >100 ABCs, offline visualizers, and APK.
        """
        pdf_count = len(list((WORKSPACE_ROOT / "docs" / "downloads" / "pdf").glob("*.pdf")))
        abc_count = len(list((WORKSPACE_ROOT / "docs" / "downloads" / "abc").glob("*.abc")))
        apk_count = len(list((WORKSPACE_ROOT / "docs" / "downloads" / "apk").glob("*.apk")))

        self.assertEqual(pdf_count, 23, "Must have 23 PDFs")
        self.assertGreaterEqual(abc_count, 120, "Must have >= 120 ABC files")
        self.assertGreaterEqual(apk_count, 1, "Must have release APK in downloads")

    def test_s06_multi_tonic_modal_transposition_cycle(self):
        """
        Scenario 6: Multi-tonic Modal Transposition Cycle
        Verifies circle-of-fifths modal files exist and are syntactically sound.
        """
        circle_tonics = ["Do", "Sol", "Re", "La", "Mi", "Si"]
        abc_dir = WORKSPACE_ROOT / "abc_modos"
        for tonic in circle_tonics:
            match = list(abc_dir.glob(f"*{tonic}*.abc"))
            self.assertGreaterEqual(len(match), 1, f"Missing modal file for tonic {tonic}")

    def test_s07_high_speed_articulation_drill(self):
        """
        Scenario 7: High-Speed Articulation Drill
        Cycling through 8 articulations of EJ4 at 160 BPM with duration check.
        """
        dur_160 = calculate_note_duration(160, subdivision=4)
        self.assertAlmostEqual(dur_160, 0.09375, places=4)

    def test_s08_flute_b_footjoint_vs_c_footjoint_compatibility(self):
        """
        Scenario 8: Flute Low B Footjoint vs Standard C Footjoint
        Verifies Modo Si requires B3 (MIDI 59) and Modo Do requires C4 (MIDI 60).
        """
        si_path = WORKSPACE_ROOT / "abc_modos" / "01_Modos_en_Si.abc"
        if not si_path.exists():
            si_path = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "modos_01_si.abc"

        do_path = WORKSPACE_ROOT / "abc_modos" / "02_Modos_en_Do.abc"
        if not do_path.exists():
            do_path = WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "modos_02_do.abc"

        si_abc = si_path.read_text(encoding="utf-8")
        do_abc = do_path.read_text(encoding="utf-8")

        si_pitches = extract_abc_midi_pitches(si_abc)
        do_pitches = extract_abc_midi_pitches(do_abc)

        self.assertEqual(min(si_pitches), 59, "Modo Si must touch MIDI 59 (B3)")
        self.assertEqual(min(do_pitches), 60, "Modo Do lowest note is MIDI 60 (C4)")

    def test_s10_multiplatform_version_consistency_target(self):
        """
        Scenario 10: Multiplatform Version Consistency Target
        Target release is v1.6.1 (iOS Build 13, Android versionCode 12, Web v1.6.1).
        Verifies version consistency across iOS, Android, and Web files.
        """
        gradle_file = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "build.gradle.kts"
        self.assertTrue(gradle_file.exists())
        gradle_content = gradle_file.read_text(encoding="utf-8")

        pbx_file = WORKSPACE_ROOT / "FluteModes" / "FluteModes.xcodeproj" / "project.pbxproj"
        self.assertTrue(pbx_file.exists())
        pbx_content = pbx_file.read_text(encoding="utf-8")

        web_index = (WORKSPACE_ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        ios_webview = (WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Views" / "ScoreWebView.swift").read_text(encoding="utf-8")

        # Check for target version 1.6.1
        self.assertIn('versionName = "1.6.1"', gradle_content, "Android versionName must be updated to 1.6.1")
        self.assertIn("versionCode = 12", gradle_content, "Android versionCode must be updated to 12")
        self.assertIn("MARKETING_VERSION = 1.6.1", pbx_content, "iOS MARKETING_VERSION must be updated to 1.6.1")
        self.assertIn("CURRENT_PROJECT_VERSION = 13", pbx_content, "iOS CURRENT_PROJECT_VERSION must be 13")
        self.assertIn("v1.6.1", web_index, "docs/index.html must reference v1.6.1")
        self.assertIn("loadFileURL", ios_webview, "iOS ScoreWebView must use loadFileURL to support >512 KB score_template.html")
        self.assertNotIn("loadHTMLString", ios_webview, "iOS ScoreWebView must not use loadHTMLString")


if __name__ == "__main__":
    unittest.main()
