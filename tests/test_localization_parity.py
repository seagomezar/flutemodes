#!/usr/bin/env python3
"""
Empirical Verification Test Suite: Localization Parity and Key Coverage
Author: challenger_m2_2 (Empirical Challenger)
Milestone: Milestone 2 (App UI, Navigation & Localization Parity)

Validates:
1. Exact bilingual dictionary completeness and 100% mutual key identity between:
   - FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/LocalizationManager.kt
   - FluteModes/FluteModes/Models/LocalizationManager.swift
2. Zero empty strings or whitespace-only strings in both Spanish and English.
3. 100% of all static and dynamically queried localization keys in both Android and iOS
   exist in both LocalizationManager files.
4. Format string specifier parity between languages.
"""

import sys
import os
import re
from pathlib import Path
import unittest

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

KT_LOC_PATH = (
    WORKSPACE_ROOT
    / "FluteModesAndroid"
    / "app"
    / "src"
    / "main"
    / "java"
    / "com"
    / "seagomezar"
    / "flutemodes"
    / "model"
    / "LocalizationManager.kt"
)

SWIFT_LOC_PATH = (
    WORKSPACE_ROOT
    / "FluteModes"
    / "FluteModes"
    / "Models"
    / "LocalizationManager.swift"
)


class TestLocalizationParity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assertTrue(cls, KT_LOC_PATH.exists(), f"Missing {KT_LOC_PATH}")
        cls.assertTrue(cls, SWIFT_LOC_PATH.exists(), f"Missing {SWIFT_LOC_PATH}")

        # Parse Kotlin dictionary
        kt_content = KT_LOC_PATH.read_text(encoding="utf-8")
        cls.kt_dict = {}
        for m in re.finditer(
            r'\"([a-zA-Z0-9_]+)\"\s*to\s*Pair\s*\(\s*\"(.*?)\"\s*,\s*\"(.*?)\"\s*\)',
            kt_content,
            re.DOTALL,
        ):
            key = m.group(1)
            es = m.group(2).strip()
            en = m.group(3).strip()
            cls.kt_dict[key] = (es, en)

        # Parse Swift dictionary
        swift_content = SWIFT_LOC_PATH.read_text(encoding="utf-8")
        cls.swift_dict = {}
        for m in re.finditer(
            r'\"([a-zA-Z0-9_]+)\"\s*:\s*\[\s*\"(.*?)\"\s*,\s*\"(.*?)\"\s*\]',
            swift_content,
            re.DOTALL,
        ):
            key = m.group(1)
            es = m.group(2).strip()
            en = m.group(3).strip()
            cls.swift_dict[key] = (es, en)

    def test_01_dictionary_counts_and_mutual_identity(self):
        """Verify both dictionaries have identical key sets and expected count."""
        kt_keys = set(self.kt_dict.keys())
        swift_keys = set(self.swift_dict.keys())

        self.assertGreaterEqual(len(kt_keys), 209, f"Expected at least 209 keys, got {len(kt_keys)}")
        self.assertEqual(len(kt_keys), len(swift_keys), "Key count mismatch between Kotlin and Swift")

        diff_kt_minus_swift = kt_keys - swift_keys
        diff_swift_minus_kt = swift_keys - kt_keys

        self.assertEqual(
            diff_kt_minus_swift,
            set(),
            f"Keys in Kotlin but missing in Swift: {diff_kt_minus_swift}",
        )
        self.assertEqual(
            diff_swift_minus_kt,
            set(),
            f"Keys in Swift but missing in Kotlin: {diff_swift_minus_kt}",
        )

    def test_02_zero_empty_translations(self):
        """Verify zero empty or whitespace-only translations in Spanish and English."""
        kt_empty_es = [k for k, (es, _) in self.kt_dict.items() if not es]
        kt_empty_en = [k for k, (_, en) in self.kt_dict.items() if not en]
        swift_empty_es = [k for k, (es, _) in self.swift_dict.items() if not es]
        swift_empty_en = [k for k, (_, en) in self.swift_dict.items() if not en]

        self.assertEqual(kt_empty_es, [], f"Kotlin keys with empty ES: {kt_empty_es}")
        self.assertEqual(kt_empty_en, [], f"Kotlin keys with empty EN: {kt_empty_en}")
        self.assertEqual(swift_empty_es, [], f"Swift keys with empty ES: {swift_empty_es}")
        self.assertEqual(swift_empty_en, [], f"Swift keys with empty EN: {swift_empty_en}")

    def test_03_zero_placeholder_artifacts(self):
        """Verify translations do not contain placeholder artifacts like TODO, FIXME, or TBD."""
        forbidden_regex = re.compile(r"\b(FIXME|TBD|UNDEFINED|MISSING_TRANSLATION|TODO:)\b", re.IGNORECASE)
        for key, (es, en) in self.kt_dict.items():
            self.assertFalse(
                bool(forbidden_regex.search(es)),
                f"Kotlin key '{key}' ES contains forbidden placeholder: '{es}'",
            )
            self.assertFalse(
                bool(forbidden_regex.search(en) or re.search(r"\bTODO\b", en, re.IGNORECASE)),
                f"Kotlin key '{key}' EN contains forbidden placeholder: '{en}'",
            )

        for key, (es, en) in self.swift_dict.items():
            self.assertFalse(
                bool(forbidden_regex.search(es)),
                f"Swift key '{key}' ES contains forbidden placeholder: '{es}'",
            )
            self.assertFalse(
                bool(forbidden_regex.search(en) or re.search(r"\bTODO\b", en, re.IGNORECASE)),
                f"Swift key '{key}' EN contains forbidden placeholder: '{en}'",
            )

    def test_04_format_specifier_parity(self):
        """Verify printf / String.format specifiers (%s, %d, etc.) match between ES and EN."""
        specifier_pattern = re.compile(r"%(\d+\$)?[sdf]")
        for key, (es, en) in self.kt_dict.items():
            es_specs = sorted(specifier_pattern.findall(es))
            en_specs = sorted(specifier_pattern.findall(en))
            self.assertEqual(
                len(es_specs),
                len(en_specs),
                f"Specifier count mismatch in Kotlin key '{key}': ES '{es}' vs EN '{en}'",
            )

        for key, (es, en) in self.swift_dict.items():
            es_specs = sorted(specifier_pattern.findall(es))
            en_specs = sorted(specifier_pattern.findall(en))
            self.assertEqual(
                len(es_specs),
                len(en_specs),
                f"Specifier count mismatch in Swift key '{key}': ES '{es}' vs EN '{en}'",
            )

    def test_05_kotlin_codebase_queried_keys_exist(self):
        """Extract all keys queried across all Kotlin source files and verify they exist in both dictionaries."""
        kt_source_files = list((WORKSPACE_ROOT / "FluteModesAndroid").glob("**/*.kt"))
        queried_keys = set()

        for f in kt_source_files:
            # Exclude unit tests from production call extraction (tested separately)
            if "Test" in f.name or "test" in f.parts:
                continue
            content = f.read_text(encoding="utf-8")
            for m in re.finditer(r"loc\.t\s*\((.*?)\)", content, re.DOTALL):
                arg = m.group(1).strip()
                # Find all string literals inside the argument
                literals = re.findall(r'\"([a-zA-Z0-9_]+)\"', arg)
                for lit in literals:
                    queried_keys.add(lit)

        # Expand known dynamic patterns in Android
        # 1. ExerciseType interpolations: "${ex.id}_start_practice", "${ex.id}_select_art", "${ex.id}_header_info"
        for ex in ["ej1", "ej2", "ej4", "ej5", "ej10", "ej11", "r1", "r2", "r4", "r5"]:
            queried_keys.add(f"{ex}_start_practice")
            queried_keys.add(f"{ex}_select_art")
            queried_keys.add(f"{ex}_header_info")

        # 2. Sectioned ExerciseType interpolations: "${ex.id}_select_section"
        for ex in ["ej4", "ej5", "ej10", "ej11", "r1", "r2", "r4", "r5"]:
            queried_keys.add(f"{ex}_select_section")

        # 3. ArticulationPattern: "ej1_art_${id}_title", "ej1_art_${id}_short" (id 0..10)
        for i in range(11):
            queried_keys.add(f"ej1_art_{i}_title")
            queried_keys.add(f"ej1_art_{i}_short")

        # 4. ArticulationPattern: "art_${id}_short" (id 1..8)
        for i in range(1, 9):
            queried_keys.add(f"art_{i}_short")

        # Verify against both dictionaries
        missing_in_kt = queried_keys - set(self.kt_dict.keys())
        missing_in_swift = queried_keys - set(self.swift_dict.keys())

        self.assertEqual(
            missing_in_kt,
            set(),
            f"Kotlin code queries keys missing in LocalizationManager.kt: {missing_in_kt}",
        )
        self.assertEqual(
            missing_in_swift,
            set(),
            f"Kotlin code queries keys missing in LocalizationManager.swift: {missing_in_swift}",
        )
        self.assertGreaterEqual(
            len(queried_keys),
            170,
            f"Expected at least 170 queried Kotlin keys, got {len(queried_keys)}",
        )

    def test_06_swift_codebase_queried_keys_exist(self):
        """Extract all keys queried across all Swift source files and verify they exist in both dictionaries."""
        swift_source_files = list((WORKSPACE_ROOT / "FluteModes").glob("**/*.swift"))
        queried_keys = set()

        for f in swift_source_files:
            if "Test" in f.name or "test" in f.parts:
                continue
            content = f.read_text(encoding="utf-8")
            for m in re.finditer(
                r"(?:loc|LocalizationManager\.shared)\.t\s*\((.*?)\)", content, re.DOTALL
            ):
                arg = m.group(1).strip()
                literals = re.findall(r'\"([a-zA-Z0-9_]+)\"', arg)
                for lit in literals:
                    queried_keys.add(lit)

        # Expand known dynamic variables in Swift:
        # 1. EJ4 exercises: "ej4", "r2", "r4"
        for ex in ["ej4", "r2", "r4"]:
            queried_keys.add(f"{ex}_select_section")
            queried_keys.add(f"{ex}_start_practice")
            queried_keys.add(f"{ex}_select_art")
            queried_keys.add(f"{ex}_header_info")

        # 2. EJ5-type exercises: "ej5", "ej10", "ej11", "r1", "r5"
        for ex in ["ej5", "ej10", "ej11", "r1", "r5"]:
            queried_keys.add(f"{ex}_select_section")
            queried_keys.add(f"{ex}_start_practice")
            queried_keys.add(f"{ex}_select_art")
            queried_keys.add(f"{ex}_header_info")

        # 3. ArticulationPattern rawValue expansions (0..10 for ej1, 1..8 for modal)
        for i in range(11):
            queried_keys.add(f"ej1_art_{i}_title")
            queried_keys.add(f"ej1_art_{i}_short")
        for i in range(1, 9):
            queried_keys.add(f"art_{i}_short")

        missing_in_kt = queried_keys - set(self.kt_dict.keys())
        missing_in_swift = queried_keys - set(self.swift_dict.keys())

        self.assertEqual(
            missing_in_kt,
            set(),
            f"Swift code queries keys missing in LocalizationManager.kt: {missing_in_kt}",
        )
        self.assertEqual(
            missing_in_swift,
            set(),
            f"Swift code queries keys missing in LocalizationManager.swift: {missing_in_swift}",
        )
        self.assertGreaterEqual(
            len(queried_keys),
            150,
            f"Expected at least 150 queried Swift keys, got {len(queried_keys)}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
