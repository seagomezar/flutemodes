#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de verificación profunda para:
  1. Las 840 variaciones modales (12 tónicas × 7 modos × 10 esquemas: Taffanel E.J. 1, 2, 4, 5, 10, 11 y Reichert R. 1, 2, 4, 5)
     y sus 7,896 variantes articuladas.
  2. Las 4 opciones de UX/UI generadas en Stitch (Project ID 14323574806802443450) para Dashboard, Practice Wizard y Modos.
"""

import json
import math
import re
import unittest
from pathlib import Path
from tests.test_helpers import (
    WORKSPACE_ROOT,
    FLUTE_MIN_MIDI,
    FLUTE_MAX_MIDI,
    count_abc_notes_in_body,
    parse_abc_headers,
    midi_to_frequency,
)

EXPECTED_SCHEME_NOTES = {
    "ej1": 257,
    "ej2": 257,
    "ej4": 127,
    "ej5": 49,
    "ej10": 97,
    "ej11": 145,
    "r1": 43,
    "r2": 61,
    "r4": 61,
    "r5": 91,
}

EXPECTED_SCHEME_METERS = {
    "ej1": "4/2",
    "ej2": "4/2",
    "ej4": "4/2",
    "ej5": "6/8",
    "ej10": "6/8",
    "ej11": "9/8",
    "r1": "6/8",
    "r2": "2/4",
    "r4": "C",
    "r5": "2/4",
}


class TestModalVariationsAndStitchUX(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        json_path = WORKSPACE_ROOT / "docs" / "modes_variations_data.json"
        cls.data = json.loads(json_path.read_text(encoding="utf-8"))

    def test_01_catalog_completeness_840_exercises(self):
        """Verifica que existan exactamente 10 esquemas, 12 tónicas, 7 modos y 840 ejercicios modales."""
        self.assertEqual(len(self.data["schemes"]), 10)
        self.assertEqual(len(self.data["tonics"]), 12)
        self.assertEqual(len(self.data["modes"]), 7)
        self.assertEqual(len(self.data["exercises"]), 840)

        for scheme_id in EXPECTED_SCHEME_NOTES:
            for tonic in self.data["tonics"]:
                for mode in self.data["modes"]:
                    key = f"{scheme_id}__{tonic['id']}__{mode['num']}"
                    self.assertIn(key, self.data["exercises"], f"Falta variación modal: {key}")

    def test_02_exact_note_counts_and_balanced_slurs_all_7896_variants(self):
        """Verifica conteo exacto de notas, cabeceras ABC y paréntesis de ligadura balanceados en las 7,896 variantes."""
        total_variants = 0
        for key, ex in self.data["exercises"].items():
            scheme_id = ex["schemeId"]
            expected_n = EXPECTED_SCHEME_NOTES[scheme_id]
            self.assertEqual(ex["totalNotes"], expected_n, f"totalNotes incorrecto en {key}")
            self.assertEqual(len(ex["midiNotes"]), expected_n, f"len(midiNotes) incorrecto en {key}")
            self.assertEqual(len(ex["frequencies"]), expected_n, f"len(frequencies) incorrecto en {key}")

            headers = parse_abc_headers(ex["abc"])
            self.assertEqual(headers.get("M"), EXPECTED_SCHEME_METERS[scheme_id])

            for art_id, abc_str in ex["abcByArticulation"].items():
                n_notes = count_abc_notes_in_body(abc_str)
                self.assertEqual(
                    n_notes, expected_n,
                    f"Conteo ABC incorrecto en {key} art={art_id}: esperado {expected_n}, obtenido {n_notes}"
                )
                # Verificar ligaduras balanceadas (descontando '(3' de tresillos en r5)
                cleaned_slurs = abc_str.replace("(3", "")
                self.assertEqual(
                    cleaned_slurs.count("("),
                    cleaned_slurs.count(")"),
                    f"Paréntesis de ligadura desbalanceados en {key} art={art_id}"
                )
                total_variants += 1

        self.assertEqual(total_variants, 7896)

    def test_03_boehm_flute_tessitura_and_frequency_math(self):
        """Verifica que las 840 variaciones estén dentro del registro Boehm [59..98] y las frecuencias cumplan A4=440Hz."""
        for key, ex in self.data["exercises"].items():
            midis = ex["midiNotes"]
            freqs = ex["frequencies"]
            self.assertGreaterEqual(min(midis), FLUTE_MIN_MIDI, f"Nota bajo B3 en {key}")
            self.assertLessEqual(max(midis), FLUTE_MAX_MIDI, f"Nota sobre D7 en {key}")
            for m, f in zip(midis, freqs):
                expected_f = midi_to_frequency(m)
                self.assertAlmostEqual(f, expected_f, delta=0.05, msg=f"Frecuencia inválida en {key}")

    def test_04_musicological_invariants_per_scheme(self):
        """Verifica invariantes musicológicas de E.J. 1, E.J. 5, E.J. 10, R. 1 y R. 5."""
        # 1. En E.J. 5 todos los intervalos entre las 48 semicorcheas son de grado conjunto (1 o 2 semitonos)
        for t in self.data["tonics"]:
            for m in self.data["modes"]:
                ex_ej5 = self.data["exercises"][f"ej5__{t['id']}__{m['num']}"]
                midis = ex_ej5["midiNotes"]
                for i in range(48):
                    diff = abs(midis[i + 1] - midis[i])
                    self.assertIn(diff, (1, 2), f"Salto no conjunto ({diff} semitonos) en ej5 {t['id']} modo {m['num']} paso {i}")
                # Empieza y termina en la tónica grave
                self.assertEqual(midis[0], midis[-1])

                # 2. En E.J. 10 cada compás de 12 notas sube estrictamente en las primeras 7 notas (a1 < a2 < ... < a7)
                ex_ej10 = self.data["exercises"][f"ej10__{t['id']}__{m['num']}"]
                m10 = ex_ej10["midiNotes"]
                for bar in range(8):
                    chunk = m10[bar * 12 : (bar + 1) * 12]
                    asc = chunk[:7]
                    self.assertEqual(asc, sorted(asc), f"Arpegio no ascendente en ej10 {t['id']} modo {m['num']} compás {bar+1}")
                    self.assertEqual(len(set(asc)), 7, f"Notas repetidas en ascenso de arpegio ej10 {t['id']} modo {m['num']}")

        # 3. Do Jónico en R. 1, R. 2, R. 4 y R. 5 coincide exactamente con la sección 1 (Do Mayor) de Reichert Op. 5
        r1_do_jonico = self.data["exercises"]["r1__02_do__1"]["midiNotes"]
        expected_r1_c = [
            72, 67, 69, 71, 72, 74, 76, 72, 74, 76, 77, 79,
            79, 76, 77, 79, 81, 83, 84, 83, 81, 79, 77, 76,
            81, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 62,
            60, 64, 67, 72, 76, 79, 84,
        ]
        self.assertEqual(r1_do_jonico, expected_r1_c)

        r2_do_jonico = self.data["exercises"]["r2__02_do__1"]["midiNotes"]
        expected_r2_c = [
            60, 64, 67, 72,
            71, 67, 65, 62, 65, 67, 71, 74,
            72, 67, 64, 60, 64, 67, 72, 76,
            74, 71, 67, 65, 67, 71, 74, 77,
            76, 72, 67, 64, 67, 72, 76, 79,
            77, 74, 71, 67, 71, 74, 77, 79,
            79, 76, 72, 67, 72, 76, 79, 84,
            74, 71, 67, 65, 62, 65, 67, 71,
            72,
        ]
        self.assertEqual(r2_do_jonico, expected_r2_c)

        r4_do_jonico = self.data["exercises"]["r4__02_do__1"]["midiNotes"]
        expected_r4_c = [
            60, 64, 67, 69, 67, 65, 67, 64, 64, 67, 72, 74, 72, 71, 72, 67,
            67, 72, 76, 77, 76, 74, 76, 72, 72, 76, 79, 81, 79, 77, 79, 76,
            67, 72, 76, 77, 76, 74, 76, 72, 64, 67, 72, 74, 72, 71, 72, 67,
            60, 64, 67, 72, 76, 79, 72, 76, 67, 72, 64, 67, 60,
        ]
        self.assertEqual(r4_do_jonico, expected_r4_c)

        r5_do_jonico = self.data["exercises"]["r5__02_do__1"]["midiNotes"]
        self.assertEqual(r5_do_jonico[:12], [72, 76, 79, 84, 76, 79, 72, 76, 79, 67, 76, 79])
        self.assertEqual(r5_do_jonico[-7:], [72, 76, 79, 84, 76, 79, 72])

    def test_05_master_and_per_tonic_abc_files(self):
        """Verifica las 10 colecciones maestras ABC (84 tunes c/u) y los 120 archivos por tónica (7 tunes c/u)."""
        master_codes = ["EJ1", "EJ2", "EJ4", "EJ5", "EJ10", "EJ11", "R1", "R2", "R4", "R5"]
        for code in master_codes:
            for folder in [WORKSPACE_ROOT, WORKSPACE_ROOT / "abc_modos_variaciones", WORKSPACE_ROOT / "docs" / "downloads" / "abc"]:
                p = folder / f"00_Coleccion_84_Modos_{code}.abc"
                self.assertTrue(p.exists(), f"Falta archivo maestro {p}")
                content = p.read_text(encoding="utf-8")
                tunes = re.findall(r"^X:\s*\d+", content, re.MULTILINE)
                self.assertEqual(len(tunes), 84, f"El archivo {p.name} debe tener 84 modos, tiene {len(tunes)}")

        for scheme_id in EXPECTED_SCHEME_NOTES:
            subdir = WORKSPACE_ROOT / "abc_modos_variaciones" / scheme_id
            self.assertTrue(subdir.is_dir())
            abc_files = sorted(subdir.glob("modos_*.abc"))
            self.assertEqual(len(abc_files), 12)
            for af in abc_files:
                tunes = re.findall(r"^X:\s*\d+", af.read_text(encoding="utf-8"), re.MULTILINE)
                self.assertEqual(len(tunes), 7)

    def test_06_stitch_ux_options_and_validation_portals(self):
        """Verifica las 4 capturas de Stitch, el atributo closedby='any' del Wizard y los portales HTML."""
        stitch_imgs = [
            "option1_conservatory_coach.png",
            "option2_dark_stage_studio.png",
            "option3_editorial_workbench.png",
            "option4_nordic_mastery_rings.png",
        ]
        for img in stitch_imgs:
            p = WORKSPACE_ROOT / "docs" / "stitch_options" / img
            self.assertTrue(p.exists(), f"Falta imagen de Stitch: {p}")
            self.assertGreater(p.stat().st_size, 20000, f"Imagen de Stitch demasiado pequeña: {p}")

        ux_html = (WORKSPACE_ROOT / "docs" / "propuestas_ux_wizard_modos.html").read_text(encoding="utf-8")
        self.assertIn('closedby="any"', ux_html, "El diálogo del Wizard debe incluir closedby='any'")
        for img in stitch_imgs:
            self.assertIn(img, ux_html)

        var_html = (WORKSPACE_ROOT / "docs" / "modos_variaciones.html").read_text(encoding="utf-8")
        self.assertIn("modes_variations_data.js", var_html)
        self.assertIn("taffanel-scheme-pills", var_html)
        self.assertIn("reichert-scheme-pills", var_html)

    def test_07_double_flats_and_single_accidental_per_measure(self):
        """Verifica que Mi♭ Lócrio y La♭ Frigio/Lócrio usen doble bemol (__B, __e) y que no se repitan alteraciones en el mismo compás."""
        for scheme_id in EXPECTED_SCHEME_NOTES:
            # Mi♭ Lócrio (K:Ebm, b5 = Si doble bemol = __B / __b)
            eb_loc = self.data["exercises"][f"{scheme_id}__05_mi_bemol__7"]["abc"]
            self.assertIn("__B", eb_loc, f"Falta __B en {scheme_id} Mi♭ Lócrio")
            self.assertNotRegex(eb_loc, r"(?<!_)_B", f"No debe haber _B simple en {scheme_id} Mi♭ Lócrio")

            # La♭ Frigio (K:Abm, b2 = Si doble bemol = __B / __b)
            ab_phr = self.data["exercises"][f"{scheme_id}__10_la_bemol__6"]["abc"]
            self.assertRegex(ab_phr, r"__[Bb]", f"Falta __B/__b en {scheme_id} La♭ Frigio")
            self.assertNotRegex(ab_phr, r"(?<!_)_[Bb]", f"No debe haber _B/_b simple en {scheme_id} La♭ Frigio")

            # La♭ Lócrio (K:Abm, b2 = __B/__b y b5 = __e/__e')
            ab_loc = self.data["exercises"][f"{scheme_id}__10_la_bemol__7"]["abc"]
            self.assertRegex(ab_loc, r"__[Bb]", f"Falta __B/__b en {scheme_id} La♭ Lócrio")
            self.assertRegex(ab_loc, r"__[Ee]", f"Falta __E/__e en {scheme_id} La♭ Lócrio")
            self.assertNotRegex(ab_loc, r"(?<!_)_[Bb]", f"No debe haber _B/_b simple en {scheme_id} La♭ Lócrio")
            self.assertNotRegex(ab_loc, r"(?<!_)_[Ee]", f"No debe haber _E/_e simple en {scheme_id} La♭ Lócrio")

        # Verificar en las 840 variaciones que ningún compás repita la misma alteración modal en la misma octava
        acc_note_re = re.compile(r"(\^\^|__|[\^_=])([A-Ga-g][',]*)")
        for key, ex in self.data["exercises"].items():
            # En R. 4 (modo 1 Jónico) las bordaduras cromáticas llevan becuadro/sostenido de regreso en otra nota,
            # pero ninguna nota con exactamente la misma letra+octava repite la misma alteración dentro de un compás.
            body_lines = [
                line.strip().rstrip("\\")
                for line in ex["abc"].splitlines()
                if line.strip() and not re.match(r"^[XTCMQLK]:|^%", line.strip())
            ]
            full_body = " ".join(body_lines).replace("|]", "|")
            measures = [m.strip() for m in full_body.split("|") if m.strip()]
            for m_idx, measure in enumerate(measures):
                seen_in_measure = set()
                for match in acc_note_re.finditer(measure):
                    acc, pitch_oct = match.groups()
                    token = f"{acc}{pitch_oct}"
                    self.assertNotIn(
                        token,
                        seen_in_measure,
                        f"Alteración redundante '{token}' repetida dentro del compás {m_idx + 1} en {key}: {measure}"
                    )
                    seen_in_measure.add(token)

    def test_08_offline_abcjs_and_per_note_staccato_playback(self):
        """Verifica que los portales HTML usen abcjs-basic-min.js local (100% offline) y parseo por nota de staccato."""
        for html_rel in [
            "docs/modos_variaciones.html",
            "docs/propuestas_ux_wizard_modos.html",
            "validacion_modos_taffanel_reichert.html",
            "propuestas_ux_wizard_modos.html",
        ]:
            content = (WORKSPACE_ROOT / html_rel).read_text(encoding="utf-8")
            self.assertIn('src="abcjs-basic-min.js"', content, f"{html_rel} debe cargar abcjs-basic-min.js local")
            self.assertNotIn("cdn.jsdelivr.net", content, f"{html_rel} no debe depender de CDN externo")

        var_html = (WORKSPACE_ROOT / "docs" / "modos_variaciones.html").read_text(encoding="utf-8")
        self.assertIn("noteStaccatos", var_html)
        self.assertNotIn('state.artId === "h" || state.artId === "j"', var_html)

    def test_09_cross_platform_option1_conservatory_coach_and_840_modes_parity(self):
        """Verifica que Opción 1 (Conservatory Coach), el Practice Wizard (3 pasos) y los 10 esquemas modales (840 modos) estén implementados en iOS, Android y Web."""
        # 1. iOS Swift checks
        swift_art = (WORKSPACE_ROOT / "FluteModes/FluteModes/Models/ArticulationPattern.swift").read_text(encoding="utf-8")
        self.assertIn("public enum ModalScheme", swift_art)
        self.assertIn("public enum PracticeWizardDuration", swift_art)
        self.assertIn("public enum PracticeWizardFocus", swift_art)
        self.assertIn("public enum CoachStrings", swift_art)

        swift_gen = (WORKSPACE_ROOT / "FluteModes/FluteModes/Models/ExerciseGenerator.swift").read_text(encoding="utf-8")
        self.assertIn("generateModalSchemeDegreesAndLines", swift_gen)
        self.assertIn("generateModalSchemeMidiNotes", swift_gen)
        self.assertIn("resolveMeasureGroups", swift_gen)

        swift_home = (WORKSPACE_ROOT / "FluteModes/FluteModes/Views/HomeView.swift").read_text(encoding="utf-8")
        self.assertIn("conservatoryCoachHeroCard", swift_home)
        self.assertIn("modalSchemesSelectorCard", swift_home)
        self.assertIn("practiceWizardSheet", swift_home)

        swift_practice = (WORKSPACE_ROOT / "FluteModes/FluteModes/Views/PracticeView.swift").read_text(encoding="utf-8")
        self.assertIn("ModalScheme.allCases", swift_practice)
        self.assertIn("selectModalScheme", swift_practice)

        # 2. Android Kotlin checks
        kt_art = (WORKSPACE_ROOT / "FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/ArticulationPattern.kt").read_text(encoding="utf-8")
        self.assertIn("enum class ModalScheme", kt_art)
        self.assertIn("enum class PracticeWizardDuration", kt_art)
        self.assertIn("enum class PracticeWizardFocus", kt_art)
        self.assertIn("object CoachStrings", kt_art)

        kt_gen = (WORKSPACE_ROOT / "FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/ExerciseGenerator.kt").read_text(encoding="utf-8")
        self.assertIn("generateModalSchemeDegreesAndLines", kt_gen)
        self.assertIn("generateModalSchemeMidiNotes", kt_gen)
        self.assertIn("resolveMeasureGroups", kt_gen)

        kt_home = (WORKSPACE_ROOT / "FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/HomeScreen.kt").read_text(encoding="utf-8")
        self.assertIn("ConservatoryCoachHeroCard", kt_home)
        self.assertIn("ModalSchemesSelectorCard", kt_home)
        self.assertIn("PracticeWizardDialog", kt_home)

        kt_practice = (WORKSPACE_ROOT / "FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/PracticeScreen.kt").read_text(encoding="utf-8")
        self.assertIn("ModalScheme.entries", kt_practice)
        self.assertIn("currentModalScheme", kt_practice)

        # 3. Web (docs/index.html & docs/propuestas_ux_wizard_modos.html) checks
        web_index = (WORKSPACE_ROOT / "docs/index.html").read_text(encoding="utf-8")
        self.assertIn('src="modes_variations_data.js"', web_index)
        self.assertIn('id="coach"', web_index)
        self.assertIn('dialog id="coach-wizard-dialog" closedby="any" aria-labelledby="coach-wizard-title"', web_index)
        self.assertIn("overscroll-behavior: contain", web_index)
        self.assertIn('"closedBy" in HTMLDialogElement.prototype', web_index)
        self.assertIn("add_classes: true", web_index)
        self.assertIn("abcjs-highlight", web_index)
        self.assertIn("parseAbcNoteStaccatos", web_index)
        self.assertIn("flutemodes_web_session_v1", web_index)
        self.assertIn('id="modal-scheme-buttons-container"', web_index)
        self.assertIn('id="modal-art-buttons-container"', web_index)
        self.assertIn("openCoachWizard", web_index)
        self.assertIn("buildWizardRoutineBlocks", web_index)

        ux_html = (WORKSPACE_ROOT / "docs/propuestas_ux_wizard_modos.html").read_text(encoding="utf-8")
        self.assertIn('dialog id="practice-wizard-dialog" closedby="any" aria-labelledby="practice-wizard-title"', ux_html)
        self.assertIn("overscroll-behavior: contain", ux_html)
        self.assertIn('"closedBy" in HTMLDialogElement.prototype', ux_html)

        # 4. LocalizationManager parity checks across iOS and Android
        swift_loc = (WORKSPACE_ROOT / "FluteModes/FluteModes/Models/LocalizationManager.swift").read_text(encoding="utf-8")
        kt_loc = (WORKSPACE_ROOT / "FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/LocalizationManager.kt").read_text(encoding="utf-8")
        for required_key in [
            "coach_badge",
            "coach_title",
            "coach_subtitle",
            "coach_open_wizard",
            "coach_wizard_title",
            "coach_resume_banner",
            "coach_resume_action",
            "coach_step1_title",
            "coach_step2_title",
            "coach_step3_title",
            "coach_launch_routine",
            "coach_level1_tonic",
            "coach_level2_mode",
            "coach_level3_scheme",
        ]:
            self.assertIn(f'"{required_key}"', swift_loc, f"Missing {required_key} in LocalizationManager.swift")
            self.assertIn(f'"{required_key}"', kt_loc, f"Missing {required_key} in LocalizationManager.kt")

        # 5. Concise ABC T: title (no mobile SVG clipping) & production badge clean of internal "OPCIÓN 1"
        self.assertIn("T:Modo \\(mode.rawValue): \\(tonic.rawValue) \\(mode.shortName) (\\(scheme.pillLabel))", swift_gen)
        self.assertIn("T:Modo ${mode.id}: ${tonic.displayName} ${mode.getShortName(loc)} (${scheme.pillLabel})", kt_gen)
        self.assertIn('"CONSERVATORY COACH · ASISTENTE GUIADO"', swift_loc)
        self.assertIn('"CONSERVATORY COACH · GUIDED ASSISTANT"', swift_loc)
        self.assertIn('"CONSERVATORY COACH · ASISTENTE GUIADO"', kt_loc)
        self.assertIn('"CONSERVATORY COACH · GUIDED ASSISTANT"', kt_loc)
        self.assertIn('data-es="CONSERVATORY COACH · ASISTENTE GUIADO" data-en="CONSERVATORY COACH · GUIDED ASSISTANT"', web_index)
        self.assertNotIn("OPCIÓN 1 · CONSERVATORY COACH", swift_loc)
        self.assertNotIn("OPTION 1 · CONSERVATORY COACH", swift_loc)
        self.assertNotIn("OPCIÓN 1 · CONSERVATORY COACH", kt_loc)
        self.assertNotIn("OPCIÓN 1 · CONSERVATORY COACH", web_index)
        self.assertNotIn("OPTION 1 · CONSERVATORY COACH", web_index)
        for removed_label in ["15m Express", "30m Conservatorio", "30m Conservatory", "45m Maestría", "45m Mastery"]:
            self.assertNotIn(removed_label, swift_art)
            self.assertNotIn(removed_label, kt_art)
        for removed_web_label in ["Calentamiento Express", "Rutina Conservatorio", "Sesión de Maestría", "15 min · Express", "30 min · Conservatorio", "45 min · Maestría"]:
            self.assertNotIn(removed_web_label, web_index)
        for removed_editorial in ["Urtext", "Alphonse Leduc", "A. L. 16.588", "B. Schott's Söhne", "B. Schott 20623", "Schott 20623"]:
            self.assertNotIn(removed_editorial, swift_loc)
            self.assertNotIn(removed_editorial, kt_loc)
            self.assertNotIn(removed_editorial, swift_home)
            self.assertNotIn(removed_editorial, kt_home)
            self.assertNotIn(removed_editorial, swift_practice)
            self.assertNotIn(removed_editorial, kt_practice)
            self.assertNotIn(removed_editorial, web_index)
        for tpl_rel in ["FluteModes/FluteModes/Resources/score_template.html", "FluteModesAndroid/app/src/main/assets/score_template.html"]:
            tpl_content = (WORKSPACE_ROOT / tpl_rel).read_text(encoding="utf-8")
            self.assertNotIn("Compases ${", tpl_content)
            for num_art in ["0: Orig.", "1: 8 Lig.", "1: 12 Lig.", "1: 18 Lig.", "Art. 1 ·", "0. Original"]:
                self.assertNotIn(num_art, tpl_content)
        for num_art in ["0: Orig.", "1: 8 Lig.", "1: 12 Lig.", "1: 18 Lig.", "2: 6+6", "3: 4L+2P", "0. Original", "1. 8 Ligadas"]:
            self.assertNotIn(num_art, swift_art)
            self.assertNotIn(num_art, kt_art)
            self.assertNotIn(num_art, swift_loc)
            self.assertNotIn(num_art, kt_loc)
            self.assertNotIn(num_art, web_index)
        self.assertNotIn("de \\(totalMeas)", swift_practice)


        for key, ex in self.data["exercises"].items():
            t_lines = [line for line in ex["abc"].splitlines() if line.startswith("T:")]
            self.assertEqual(len(t_lines), 1, f"Falta línea T: en {key}")
            visible_title = t_lines[0][2:]
            self.assertTrue(visible_title.startswith("Modo "), f"Título ABC debe iniciar con 'Modo ' en {key}: {visible_title}")
            self.assertLessEqual(len(visible_title), 32, f"Título ABC demasiado largo ({len(visible_title)} chars) en {key}: {visible_title}")


if __name__ == "__main__":
    unittest.main(verbosity=2)



