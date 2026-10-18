package com.seagomezar.flutemodes.model

enum class ExerciseType(val id: String) {
    EJ1("ej1"),
    EJ2("ej2"),
    EJ4("ej4"),
    EJ5("ej5"),
    EJ10("ej10"),
    EJ11("ej11"),
    R1("r1"),
    R2("r2"),
    R4("r4"),
    R5("r5"),
    MODOS("modos");

    val isChromaticExercise: Boolean
        get() = this == EJ1 || this == EJ2

    val isReichertExercise: Boolean
        get() = this == R1 || this == R2 || this == R4 || this == R5

    val isEJ4Exercise: Boolean
        get() = this == EJ4 || this == R2 || this == R4

    val isEJ5TypeExercise: Boolean
        get() = this == EJ5 || this == EJ10 || this == EJ11 || this == R1 || this == R5

    val isSectionedLeducExercise: Boolean
        get() = isEJ4Exercise || isEJ5TypeExercise

    val isLeducExercise: Boolean
        get() = this != MODOS

    val sectionCount: Int
        get() = if (isEJ4Exercise || isReichertExercise) 25 else 12

    val pillLabel: String
        get() = when (this) {
            EJ1 -> "E.J. 1"
            EJ2 -> "E.J. 2"
            EJ4 -> "E.J. 4"
            EJ5 -> "E.J. 5"
            EJ10 -> "E.J. 10"
            EJ11 -> "E.J. 11"
            R1 -> "R. 1"
            R2 -> "R. 2"
            R4 -> "R. 4"
            R5 -> "R. 5"
            MODOS -> "84 Modos"
        }

    val homeButtonTitle: String
        get() = when (this) {
            EJ1 -> "E.J. 1"
            EJ2 -> "E.J. 2"
            EJ4 -> "E.J. 4"
            EJ5 -> "E.J. 5"
            EJ10 -> "E.J. 10"
            EJ11 -> "E.J. 11"
            R1 -> "Reichert 1"
            R2 -> "Reichert 2"
            R4 -> "Reichert 4"
            R5 -> "Reichert 5"
            MODOS -> "84 Modos"
        }

    fun homeButtonSubtitle(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> if (isEn) "Major" else "Mayor"
            EJ2 -> if (isEn) "Minor" else "Menor"
            EJ4 -> if (isEn) "24 Keys" else "24 Ton."
            EJ5 -> if (isEn) "Chrom." else "Cromát."
            EJ10 -> if (isEn) "Arpeggios" else "Arpegios"
            EJ11 -> if (isEn) "Brk. Arp." else "Arp. Queb."
            R1 -> "Op. 5 Nº 1 (6/8)"
            R2 -> "Op. 5 Nº 2 (2/4)"
            R4 -> "Op. 5 Nº 4 (4/4)"
            R5 -> "Op. 5 Nº 5 (3plets)"
            MODOS -> if (isEn) "12 Tonics × 7 Modes" else "12 Tónicas × 7 Modos"
        }
    }

    fun displayTitle(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> if (isEn) "E.J. 1 · Major (10 Arts.)" else "E.J. 1 · Mayor (10 Arts.)"
            EJ2 -> if (isEn) "E.J. 2 · Minor (10 Arts.)" else "E.J. 2 · Menor (10 Arts.)"
            EJ4 -> if (isEn) "E.J. 4 · 24 Keys (8 Arts.)" else "E.J. 4 · 24 Ton. (8 Arts.)"
            EJ5 -> if (isEn) "E.J. 5 · Chromatic (10 Arts.)" else "E.J. 5 · Cromáticas (10 Arts.)"
            EJ10 -> if (isEn) "E.J. 10 · Arpeggios (10 Arts.)" else "E.J. 10 · Arpegios (10 Arts.)"
            EJ11 -> if (isEn) "E.J. 11 · Broken Arp. (10 Arts.)" else "E.J. 11 · Arp. Quebrados (10 Arts.)"
            R1 -> if (isEn) "R. 1 · Reichert Nº 1 (10 Arts.)" else "R. 1 · Reichert Nº 1 (10 Arts.)"
            R2 -> if (isEn) "R. 2 · Reichert Nº 2 (8 Arts.)" else "R. 2 · Reichert Nº 2 (8 Arts.)"
            R4 -> if (isEn) "R. 4 · Reichert Nº 4 (8 Arts.)" else "R. 4 · Reichert Nº 4 (8 Arts.)"
            R5 -> if (isEn) "R. 5 · Reichert Nº 5 (10 Arts.)" else "R. 5 · Reichert Nº 5 (10 Arts.)"
            MODOS -> if (isEn) "84 Parallel Modes" else "84 Modos Paralelos"
        }
    }

    fun shortLabel(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> "E.J. 1"
            EJ2 -> "E.J. 2"
            EJ4 -> "E.J. 4"
            EJ5 -> "E.J. 5"
            EJ10 -> "E.J. 10"
            EJ11 -> "E.J. 11"
            R1 -> "R. 1"
            R2 -> "R. 2"
            R4 -> "R. 4"
            R5 -> "R. 5"
            MODOS -> if (isEn) "84 Modes" else "84 Modos"
        }
    }
}

enum class EJ4Articulation(
    val id: Int,
    val formulaBadge: String
) {
    ORIGINAL(0, "Original"),
    ALL_SLURRED_8(1, "(8)"),
    SLURRED_4_AND_4(2, "(4)+(4)"),
    STACC_1_SLUR_3(3, "·(3) ·(3)"),
    SLUR_2_STACC_2(4, "(2)·· (2)··"),
    STACC_2_SLUR_2(5, "··(2) ··(2)"),
    STACC_1_SLUR_2_STACC_1(6, "·(2)· ·(2)·"),
    SLUR_PAIRS_2_BY_2(7, "(2)(2)(2)(2)"),
    SLUR_SYNCOPATED(8, "·(2)(2)(2)·");

    fun formulaBadge(exercise: ExerciseType): String {
        return formulaBadge
    }

    fun title(loc: LocalizationManager, exercise: ExerciseType = ExerciseType.EJ4): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            ORIGINAL -> if (isEn) "Original (As written)" else "Original (Como está escrito)"
            ALL_SLURRED_8 -> if (isEn) "8 slurred: (CDEFGABc)" else "8 ligadas: (CDEFGABc)"
            SLURRED_4_AND_4 -> if (isEn) "4 and 4 slurred: (CDEF)(GABc)" else "4 y 4 ligadas: (CDEF)(GABc)"
            STACC_1_SLUR_3 -> if (isEn) "1 staccato, 3 slurred: .C(DEF) .G(ABc)" else "1 picada y 3 ligadas: .C(DEF) .G(ABc)"
            SLUR_2_STACC_2 -> if (isEn) "2 slurred, 2 staccato: (CD).E.F (GA).B.c" else "2 ligadas y 2 picadas: (CD).E.F (GA).B.c"
            STACC_2_SLUR_2 -> if (isEn) "2 staccato, 2 slurred: .C.D(EF) .G.A(Bc)" else "2 picadas y 2 ligadas: .C.D(EF) .G.A(Bc)"
            STACC_1_SLUR_2_STACC_1 -> if (isEn) "1 stacc., 2 slurred, 1 stacc.: .C(DE).F .G(AB).c" else "1 picada, 2 ligadas y 1 picada: .C(DE).F .G(AB).c"
            SLUR_PAIRS_2_BY_2 -> if (isEn) "Slurred in pairs: (CD)(EF)(GA)(Bc)" else "De 2 en 2 ligadas: (CD)(EF)(GA)(Bc)"
            SLUR_SYNCOPATED -> if (isEn) "Syncopated pairs: .C(DE)(FG)(AB).c" else "De 2 en 2 sincopadas: .C(DE)(FG)(AB).c"
        }
    }

    fun shortTitle(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            ORIGINAL -> "Orig."
            ALL_SLURRED_8 -> if (isEn) "8 Slur" else "8 Lig."
            SLURRED_4_AND_4 -> "4+4"
            STACC_1_SLUR_3 -> "1P+3L"
            SLUR_2_STACC_2 -> "2L+2P"
            STACC_2_SLUR_2 -> "2P+2L"
            STACC_1_SLUR_2_STACC_1 -> "1P+2L+1P"
            SLUR_PAIRS_2_BY_2 -> if (isEn) "2+2" else "2 en 2"
            SLUR_SYNCOPATED -> if (isEn) "Sync." else "Sinc."
        }
    }

    companion object {
        val practiceCases: List<EJ4Articulation>
            get() = entries.filter { it != ORIGINAL }
    }
}

enum class EJ5Articulation(val id: Int) {
    ORIGINAL(0),
    ALL_SLURRED(1),
    SLURRED_6_BY_6(2),
    SLUR_4_STACC_2(3),
    STACC_2_SLUR_4(4),
    SLUR_2_STACC_4(5),
    SLURRED_3_BY_3(6),
    SLUR_3_STACC_3(7),
    SLUR_PAIRS_2_BY_2(8),
    SLUR_SYNCOPATED(9),
    ALL_STACCATO(10);

    fun title(loc: LocalizationManager, exercise: ExerciseType = ExerciseType.EJ5): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        val is98 = (exercise == ExerciseType.EJ11)
        return when (this) {
            ORIGINAL -> if (isEn) "Original (As written)" else "Original (Como está escrito)"
            ALL_SLURRED -> if (is98) {
                if (isEn) "18 slurred (full measure)" else "18 ligadas (compás completo)"
            } else {
                if (isEn) "12 slurred (full measure)" else "12 ligadas (compás completo)"
            }
            SLURRED_6_BY_6 -> if (is98) {
                if (isEn) "6+6+6 slurred (by beats)" else "6+6+6 ligadas (por tiempos)"
            } else {
                if (isEn) "6 and 6 slurred (by beats)" else "6 y 6 ligadas (por tiempos)"
            }
            SLUR_4_STACC_2 -> if (isEn) "4 slurred and 2 staccato" else "4 ligadas y 2 picadas"
            STACC_2_SLUR_4 -> if (isEn) "2 staccato and 4 slurred" else "2 picadas y 4 ligadas"
            SLUR_2_STACC_4 -> if (isEn) "2 slurred and 4 staccato" else "2 ligadas y 4 picadas"
            SLURRED_3_BY_3 -> if (is98) {
                if (isEn) "Slurred in 3s (3/4)" else "De 3 en 3 ligadas (3/4)"
            } else {
                if (isEn) "Slurred in 3s (2/4)" else "De 3 en 3 ligadas (2/4)"
            }
            SLUR_3_STACC_3 -> if (is98) {
                if (isEn) "3 slurred, 3 staccato (3/4)" else "3 ligadas y 3 picadas (3/4)"
            } else {
                if (isEn) "3 slurred, 3 staccato (2/4)" else "3 ligadas y 3 picadas (2/4)"
            }
            SLUR_PAIRS_2_BY_2 -> if (isEn) "Slurred in pairs" else "De 2 en 2 ligadas"
            SLUR_SYNCOPATED -> if (isEn) "Syncopated pairs" else "De 2 en 2 sincopadas"
            ALL_STACCATO -> if (isEn) "All staccato" else "Todas picadas (Staccato)"
        }
    }

    fun shortTitle(loc: LocalizationManager, exercise: ExerciseType = ExerciseType.EJ5): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        val is98 = (exercise == ExerciseType.EJ11)
        return when (this) {
            ORIGINAL -> "Orig."
            ALL_SLURRED -> if (is98) (if (isEn) "18 Slur" else "18 Lig.") else (if (isEn) "12 Slur" else "12 Lig.")
            SLURRED_6_BY_6 -> if (is98) "6+6+6" else "6+6"
            SLUR_4_STACC_2 -> "4L+2P"
            STACC_2_SLUR_4 -> "2P+4L"
            SLUR_2_STACC_4 -> "2L+4P"
            SLURRED_3_BY_3 -> if (isEn) "3 by 3" else "3 en 3"
            SLUR_3_STACC_3 -> "3L+3P"
            SLUR_PAIRS_2_BY_2 -> if (isEn) "2 by 2" else "2 en 2"
            SLUR_SYNCOPATED -> if (isEn) "Sync." else "Sinc."
            ALL_STACCATO -> "Stacc."
        }
    }

    fun formulaBadge(exercise: ExerciseType = ExerciseType.EJ5): String {
        val is98 = (exercise == ExerciseType.EJ11)
        return when (this) {
            ORIGINAL -> if (exercise == ExerciseType.R5) "2/4" else if (exercise == ExerciseType.R1) "6/8" else if (is98) "9/8 · 3/4" else "6/8 · 2/4"
            ALL_SLURRED -> if (is98) "(18)" else "(12)"
            SLURRED_6_BY_6 -> if (is98) "(6)+(6)+(6)" else "(6)+(6)"
            SLUR_4_STACC_2 -> "(4)·· (4)··"
            STACC_2_SLUR_4 -> "··(4) ··(4)"
            SLUR_2_STACC_4 -> "(2)····"
            SLURRED_3_BY_3 -> if (is98) "(3)×6 [3/4]" else "(3)(3)(3)(3)"
            SLUR_3_STACC_3 -> "(3)···"
            SLUR_PAIRS_2_BY_2 -> "(2)(2)(2)"
            SLUR_SYNCOPATED -> "·(2)(2)·"
            ALL_STACCATO -> "······"
        }
    }

    val formulaBadge: String
        get() = formulaBadge(ExerciseType.EJ5)

    companion object {
        val practiceCases: List<EJ5Articulation>
            get() = entries.filter { it != ORIGINAL }
    }
}

enum class EJ4Section(
    val id: Int,
    val shortBadge: String,
    val titleEs: String,
    val titleEn: String,
    val measureRange: String,
    val keySig: String
) {
    C_MAJOR(0,   "1. Do M",    "1. Do Mayor (C Major)",           "1. C Major",                    "c. 1–8",     "C"),
    A_MINOR(1,   "2. La m",    "2. La menor (Relatif Mineur)",    "2. A minor (Relative Minor)",   "c. 9–16",    "C"),
    F_MAJOR(2,   "3. Fa M",    "3. Fa Mayor (F Major)",           "3. F Major",                    "c. 17–24",   "F"),
    D_MINOR(3,   "4. Re m",    "4. Re menor (Mineur)",            "4. D minor (Relative Minor)",   "c. 25–32",   "F"),
    BB_MAJOR(4,  "5. Si♭ M",   "5. Si♭ Mayor (B♭ Major)",         "5. B♭ Major",                   "c. 33–40",   "Bb"),
    G_MINOR(5,   "6. Sol m",   "6. Sol menor (Mineur)",           "6. G minor (Relative Minor)",   "c. 41–48",   "Bb"),
    EB_MAJOR(6,  "7. Mi♭ M",   "7. Mi♭ Mayor (E♭ Major)",         "7. E♭ Major",                   "c. 49–56",   "Eb"),
    C_MINOR(7,   "8. Do m",    "8. Do menor (Mineur)",            "8. C minor (Relative Minor)",   "c. 57–64",   "Eb"),
    AB_MAJOR(8,  "9. La♭ M",   "9. La♭ Mayor (A♭ Major)",         "9. A♭ Major",                   "c. 65–72",   "Ab"),
    F_MINOR(9,   "10. Fa m",   "10. Fa menor (Mineur)",           "10. F minor (Relative Minor)",  "c. 73–80",   "Ab"),
    DB_MAJOR(10, "11. Re♭ M",  "11. Re♭ Mayor (D♭ Major)",        "11. D♭ Major",                  "c. 81–88",   "Db"),
    BB_MINOR(11, "12. Si♭ m",  "12. Si♭ menor (Mineur)",          "12. B♭ minor (Relative Minor)", "c. 89–96",   "Db"),
    GB_MAJOR(12, "13. Sol♭ M", "13. Sol♭ Mayor (G♭ Major)",       "13. G♭ Major",                  "c. 97–104",  "Gb"),
    EB_MINOR(13, "14. Mi♭ m",  "14. Mi♭ menor (Mineur)",          "14. E♭ minor (Relative Minor)", "c. 105–112", "Gb"),
    B_MAJOR(14,  "15. Si M",   "15. Si Mayor (B Major)",          "15. B Major",                   "c. 113–120", "B"),
    GS_MINOR(15, "16. Sol♯ m", "16. Sol♯ menor (Mineur)",         "16. G♯ minor (Relative Minor)", "c. 121–128", "B"),
    E_MAJOR(16,  "17. Mi M",   "17. Mi Mayor (E Major)",          "17. E Major",                   "c. 129–136", "E"),
    CS_MINOR(17, "18. Do♯ m",  "18. Do♯ menor (Mineur)",          "18. C♯ minor (Relative Minor)", "c. 137–144", "E"),
    A_MAJOR(18,  "19. La M",   "19. La Mayor (A Major)",          "19. A Major",                   "c. 145–152", "A"),
    FS_MINOR(19, "20. Fa♯ m",  "20. Fa♯ menor (Mineur)",          "20. F♯ minor (Relative Minor)", "c. 153–160", "A"),
    D_MAJOR(20,  "21. Re M",   "21. Re Mayor (D Major)",          "21. D Major",                   "c. 161–168", "D"),
    B_MINOR(21,  "22. Si m",   "22. Si menor (Mineur)",           "22. B minor (Relative Minor)",  "c. 169–176", "D"),
    G_MAJOR(22,  "23. Sol M",  "23. Sol Mayor (G Major)",         "23. G Major",                   "c. 177–184", "G"),
    E_MINOR(23,  "24. Mi m",   "24. Mi menor (Mineur)",           "24. E minor (Relative Minor)",  "c. 185–192", "G"),
    C_CODA(24,   "25. Coda",   "25. Do Mayor (Coda Final)",       "25. C Major (Final Coda)",      "c. 193–194", "C");

    fun title(loc: LocalizationManager, exercise: ExerciseType = ExerciseType.EJ4): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        if (exercise.isReichertExercise) {
            if (id == 12) return if (isEn) "13. F♯ Major" else "13. Fa♯ Mayor (F♯ Major)"
            if (id == 13) return if (isEn) "14. D♯ minor (Relative Minor)" else "14. Re♯ menor (D♯ minor)"
            if (id == 24) return if (isEn) "25. C Major (D.S. al Fine)" else "25. Do Mayor (D.S. al Fine)"
        }
        return if (isEn) titleEn else titleEs
    }

    fun shortBadge(exercise: ExerciseType): String {
        if (exercise.isReichertExercise) {
            if (id == 12) return "13. Fa♯ M"
            if (id == 13) return "14. Re♯ m"
            if (id == 24) return "25. D.S. Fine"
        }
        return shortBadge
    }

    fun measureRange(exercise: ExerciseType): String {
        return when (exercise) {
            ExerciseType.R1, ExerciseType.R4 -> {
                val s = id * 4 + 1
                "c. $s–${s + 3}"
            }
            ExerciseType.R2, ExerciseType.R5 -> {
                val s = id * 8 + 1
                "c. $s–${s + 7}"
            }
            else -> measureRange
        }
    }

    val r1MeasureRange: String
        get() = measureRange(ExerciseType.R1)

    val r2MeasureRange: String
        get() = measureRange(ExerciseType.R2)

    val r5MeasureRange: String
        get() = measureRange(ExerciseType.R5)
}

enum class EJ5Section(
    val id: Int,
    val shortBadge: String,
    val titleEs: String,
    val titleEn: String,
    val measureRange: String
) {
    C_CHROM(0,   "A. Do",   "A. Escala cromática desde Do (C4–C6)",     "A. Chromatic scale from C (C4–C6)",     "c. 1–5"),
    DB_CHROM(1,  "B. Re♭",  "B. Escala cromática desde Re♭ (D♭4–D♭6)",  "B. Chromatic scale from D♭ (D♭4–D♭6)",  "c. 6–10"),
    D_CHROM(2,   "C. Re",   "C. Escala cromática desde Re (D4–D6)",     "C. Chromatic scale from D (D4–D6)",     "c. 11–15"),
    EB_CHROM(3,  "D. Mi♭",  "D. Escala cromática desde Mi♭ (E♭4–E♭6)",  "D. Chromatic scale from E♭ (E♭4–E♭6)",  "c. 16–20"),
    E_CHROM(4,   "E. Mi",   "E. Escala cromática desde Mi (E4–E6)",     "E. Chromatic scale from E (E4–E6)",     "c. 21–25"),
    F_CHROM(5,   "F. Fa",   "F. Escala cromática desde Fa (F4–F6)",     "F. Chromatic scale from F (F4–F6)",     "c. 26–30"),
    GB_CHROM(6,  "G. Sol♭", "G. Escala cromática desde Sol♭ (G♭4–G♭6)", "G. Chromatic scale from G♭ (G♭4–G♭6)",  "c. 31–35"),
    G_CHROM(7,   "H. Sol",  "H. Escala cromática desde Sol (G4–G6)",    "H. Chromatic scale from G (G4–G6)",     "c. 36–40"),
    AB_CHROM(8,  "I. La♭",  "I. Escala cromática desde La♭ (A♭4–A♭6)",  "I. Chromatic scale from A♭ (A♭4–A♭6)",  "c. 41–45"),
    A_CHROM(9,   "J. La",   "J. Escala cromática desde La (A4–A6)",     "J. Chromatic scale from A (A4–A6)",     "c. 46–50"),
    BB_CHROM(10, "K. Si♭",  "K. Escala cromática desde Si♭ (B♭4–B♭6)",  "K. Chromatic scale from B♭ (B♭4–B♭6)",  "c. 51–55"),
    B_CHROM(11,  "L. Si",   "L. Escala cromática desde Si (B4–B6)",     "L. Chromatic scale from B (B4–B6)",     "c. 56–60");

    fun title(loc: LocalizationManager): String =
        if (loc.currentLanguage == AppLanguage.ENGLISH) titleEn else titleEs
}

enum class EJ10Section(
    val id: Int,
    val shortBadge: String,
    val titleEs: String,
    val titleEn: String,
    val measureRange: String
) {
    C_ARP(0,   "1. Do",       "1. Serie sobre Do (C)",               "1. Series on C",               "c. 1–10"),
    CS_ARP(1,  "2. Do♯/Re♭",  "2. Serie sobre Do♯ / Re♭ (C♯ / D♭)",  "2. Series on C♯ / D♭",         "c. 11–20"),
    D_ARP(2,   "3. Re",       "3. Serie sobre Re (D)",               "3. Series on D",               "c. 21–30"),
    DS_ARP(3,  "4. Re♯/Mi♭",  "4. Serie sobre Re♯ / Mi♭ (D♯ / E♭)",  "4. Series on D♯ / E♭",         "c. 31–40"),
    E_ARP(4,   "5. Mi",       "5. Serie sobre Mi (E)",               "5. Series on E",               "c. 41–50"),
    F_ARP(5,   "6. Fa",       "6. Serie sobre Fa (F)",               "6. Series on F",               "c. 51–60"),
    FS_ARP(6,  "7. Fa♯/Sol♭", "7. Serie sobre Fa♯ / Sol♭ (F♯ / G♭)", "7. Series on F♯ / G♭",         "c. 61–70"),
    G_ARP(7,   "8. Sol",      "8. Serie sobre Sol (G)",              "8. Series on G",               "c. 71–80"),
    GS_ARP(8,  "9. Sol♯/La♭", "9. Serie sobre Sol♯ / La♭ (G♯ / A♭)", "9. Series on G♯ / A♭",         "c. 81–90"),
    A_ARP(9,   "10. La",      "10. Serie sobre La (A)",              "10. Series on A",              "c. 91–100"),
    AS_ARP(10, "11. La♯/Si♭", "11. Serie sobre La♯ / Si♭ (A♯ / B♭)", "11. Series on A♯ / B♭",        "c. 101–110"),
    B_ARP(11,  "12. Si",      "12. Serie sobre Si + Coda (B)",       "12. Series on B + Coda",       "c. 111–121");

    fun title(loc: LocalizationManager): String =
        if (loc.currentLanguage == AppLanguage.ENGLISH) titleEn else titleEs
}

enum class EJ1Articulation(
    val id: Int,
    val formulaBadge: String
) {
    ORIGINAL(0, "Original"),
    ALL_SLURRED_8(1, "(8)"),
    SLURRED_4_AND_4(2, "(4)+(4)"),
    STACC_1_SLUR_3(3, "·(3) ·(3)"),
    SLUR_3_STACC_1(4, "(3)· (3)·"),
    SLUR_2_STACC_2(5, "(2)·· (2)··"),
    STACC_2_SLUR_2(6, "··(2) ··(2)"),
    STACC_1_SLUR_2_STACC_1(7, "·(2)· ·(2)·"),
    SLUR_PAIRS_2_BY_2(8, "(2)(2)(2)(2)"),
    SLUR_SYNCOPATED(9, "·(2)(2)(2)·"),
    ALL_STACCATO(10, "········");

    fun title(loc: LocalizationManager): String = loc.t("ej1_art_${id}_title")
    fun shortTitle(loc: LocalizationManager): String = loc.t("ej1_art_${id}_short")

    fun apply(notes: List<String>): String {
        if (notes.size != 8) return notes.joinToString("")
        val n = notes
        return when (this) {
            ORIGINAL -> n.joinToString("")
            ALL_SLURRED_8 -> "(${n[0]}${n[1]}${n[2]}${n[3]}${n[4]}${n[5]}${n[6]}${n[7]})"
            SLURRED_4_AND_4 -> "(${n[0]}${n[1]}${n[2]}${n[3]})(${n[4]}${n[5]}${n[6]}${n[7]})"
            STACC_1_SLUR_3 -> ".${n[0]}(${n[1]}${n[2]}${n[3]}).${n[4]}(${n[5]}${n[6]}${n[7]})"
            SLUR_3_STACC_1 -> "(${n[0]}${n[1]}${n[2]}).${n[3]}(${n[4]}${n[5]}${n[6]}).${n[7]}"
            SLUR_2_STACC_2 -> "(${n[0]}${n[1]}).${n[2]}.${n[3]}(${n[4]}${n[5]}).${n[6]}.${n[7]}"
            STACC_2_SLUR_2 -> ".${n[0]}.${n[1]}(${n[2]}${n[3]}).${n[4]}.${n[5]}(${n[6]}${n[7]})"
            STACC_1_SLUR_2_STACC_1 -> ".${n[0]}(${n[1]}${n[2]}).${n[3]}.${n[4]}(${n[5]}${n[6]}).${n[7]}"
            SLUR_PAIRS_2_BY_2 -> "(${n[0]}${n[1]})(${n[2]}${n[3]})(${n[4]}${n[5]})(${n[6]}${n[7]})"
            SLUR_SYNCOPATED -> ".${n[0]}(${n[1]}${n[2]})(${n[3]}${n[4]})(${n[5]}${n[6]}).${n[7]}"
            ALL_STACCATO -> ".${n[0]}.${n[1]}.${n[2]}.${n[3]}.${n[4]}.${n[5]}.${n[6]}.${n[7]}"
        }
    }

    companion object {
        val practiceCases: List<EJ1Articulation>
            get() = entries.filter { it != ORIGINAL }
    }
}

enum class ArticulationPattern(
    val id: Int,
    val title: String
) {
    ALL_SLURRED(1, "Toda ligada"),
    SLURRED_FOUR_AND_FOUR(2, "Ligado 4 y 4"),
    SLUR_TWO_STACCATO_TWO(3, "Ligado 2, picado 2"),
    STACCATO_SLUR_TWO_STACCATO(4, "Picado 1, ligado 2, picado 1"),
    STACCATO_TWO_SLUR_TWO(5, "Picado 2, ligado 2"),
    STACCATO_ONE_SLUR_THREE(6, "Picado 1, ligado 3"),
    SLUR_THREE_STACCATO_ONE(7, "Ligado 3, picado 1"),
    ALL_STACCATO(8, "Toda picada (Staccato)");

    fun shortTitle(loc: LocalizationManager): String {
        return loc.t("art_${id}_short")
    }

    fun apply(notes: List<String>): String {
        if (notes.size != 8) return notes.joinToString("")
        val n = notes
        return when (this) {
            ALL_SLURRED -> "(${n[0]}${n[1]}${n[2]}${n[3]} ${n[4]}${n[5]}${n[6]}${n[7]})"
            SLURRED_FOUR_AND_FOUR -> "(${n[0]}${n[1]}${n[2]}${n[3]}) (${n[4]}${n[5]}${n[6]}${n[7]})"
            SLUR_TWO_STACCATO_TWO -> "(${n[0]}${n[1]}).${n[2]}.${n[3]} (${n[4]}${n[5]}).${n[6]}.${n[7]}"
            STACCATO_SLUR_TWO_STACCATO -> ".${n[0]}(${n[1]}${n[2]}).${n[3]} .${n[4]}(${n[5]}${n[6]}).${n[7]}"
            STACCATO_TWO_SLUR_TWO -> ".${n[0]}.${n[1]}(${n[2]}${n[3]}) .${n[4]}.${n[5]}(${n[6]}${n[7]})"
            STACCATO_ONE_SLUR_THREE -> ".${n[0]}(${n[1]}${n[2]}${n[3]}) .${n[4]}(${n[5]}${n[6]}${n[7]})"
            SLUR_THREE_STACCATO_ONE -> "(${n[0]}${n[1]}${n[2]}).${n[3]} (${n[4]}${n[5]}${n[6]}).${n[7]}"
            ALL_STACCATO -> ".${n[0]}.${n[1]}.${n[2]}.${n[3]} .${n[4]}.${n[5]}.${n[6]}.${n[7]}"
        }
    }

    /** Formats an 8-sixteenth-note group (2 beats in 4/4, L:1/16) with this articulation pattern */
    fun apply16ths8(notes: List<String>): String {
        if (notes.size != 8) return notes.joinToString("")
        val n = notes
        return when (this) {
            ALL_SLURRED -> "(${n[0]}${n[1]}${n[2]}${n[3]}) (${n[4]}${n[5]}${n[6]}${n[7]})"
            SLURRED_FOUR_AND_FOUR -> "(${n[0]}${n[1]}${n[2]}${n[3]}) (${n[4]}${n[5]}${n[6]}${n[7]})"
            SLUR_TWO_STACCATO_TWO -> "(${n[0]}${n[1]}).${n[2]}.${n[3]} (${n[4]}${n[5]}).${n[6]}.${n[7]}"
            STACCATO_SLUR_TWO_STACCATO -> ".${n[0]}(${n[1]}${n[2]}).${n[3]} .${n[4]}(${n[5]}${n[6]}).${n[7]}"
            STACCATO_TWO_SLUR_TWO -> ".${n[0]}.${n[1]}(${n[2]}${n[3]}) .${n[4]}.${n[5]}(${n[6]}${n[7]})"
            STACCATO_ONE_SLUR_THREE -> ".${n[0]}(${n[1]}${n[2]}${n[3]}) .${n[4]}(${n[5]}${n[6]}${n[7]})"
            SLUR_THREE_STACCATO_ONE -> "(${n[0]}${n[1]}${n[2]}).${n[3]} (${n[4]}${n[5]}${n[6]}).${n[7]}"
            ALL_STACCATO -> ".${n[0]}.${n[1]}.${n[2]}.${n[3]} .${n[4]}.${n[5]}.${n[6]}.${n[7]}"
        }
    }

    /** Formats a 4-sixteenth-note beat (L:1/16) with this articulation pattern */
    fun apply16ths4(notes: List<String>): String {
        if (notes.size != 4) return notes.joinToString("")
        val n = notes
        return when (this) {
            ALL_SLURRED, SLURRED_FOUR_AND_FOUR -> "(${n[0]}${n[1]}${n[2]}${n[3]})"
            SLUR_TWO_STACCATO_TWO -> "(${n[0]}${n[1]}).${n[2]}.${n[3]}"
            STACCATO_SLUR_TWO_STACCATO -> ".${n[0]}(${n[1]}${n[2]}).${n[3]}"
            STACCATO_TWO_SLUR_TWO -> ".${n[0]}.${n[1]}(${n[2]}${n[3]})"
            STACCATO_ONE_SLUR_THREE -> ".${n[0]}(${n[1]}${n[2]}${n[3]})"
            SLUR_THREE_STACCATO_ONE -> "(${n[0]}${n[1]}${n[2]}).${n[3]}"
            ALL_STACCATO -> ".${n[0]}.${n[1]}.${n[2]}.${n[3]}"
        }
    }

    /** Formats a 6-sixteenth-note dotted-quarter group (6/8 or 9/8, L:1/16) with this articulation pattern */
    fun apply16ths6(notes: List<String>): String {
        if (notes.size != 6) return notes.joinToString("")
        val n = notes
        return when (this) {
            ALL_SLURRED -> "(${n[0]}${n[1]}${n[2]}${n[3]}${n[4]}${n[5]})"
            SLURRED_FOUR_AND_FOUR -> "(${n[0]}${n[1]}${n[2]})(${n[3]}${n[4]}${n[5]})"
            SLUR_TWO_STACCATO_TWO -> "(${n[0]}${n[1]}).${n[2]}(${n[3]}${n[4]}).${n[5]}"
            STACCATO_SLUR_TWO_STACCATO -> ".${n[0]}(${n[1]}${n[2]}).${n[3]}(${n[4]}${n[5]})"
            STACCATO_TWO_SLUR_TWO -> ".${n[0]}.${n[1]}(${n[2]}${n[3]}${n[4]}${n[5]})"
            STACCATO_ONE_SLUR_THREE -> ".${n[0]}(${n[1]}${n[2]}) .${n[3]}(${n[4]}${n[5]})"
            SLUR_THREE_STACCATO_ONE -> "(${n[0]}${n[1]}${n[2]}).${n[3]}.${n[4]}.${n[5]}"
            ALL_STACCATO -> ".${n[0]}.${n[1]}.${n[2]}.${n[3]}.${n[4]}.${n[5]}"
        }
    }

    /** Formats a 6-note triplet-pair group in 2/4 (`(3abc (3def`) with this articulation pattern */
    fun applyTripletPair(notes: List<String>): String {
        if (notes.size != 6) return notes.joinToString("")
        val n = notes
        return when (this) {
            ALL_SLURRED -> "((3${n[0]}${n[1]}${n[2]} (3${n[3]}${n[4]}${n[5]})"
            SLURRED_FOUR_AND_FOUR -> "((3${n[0]}${n[1]}${n[2]}) ((3${n[3]}${n[4]}${n[5]})"
            SLUR_TWO_STACCATO_TWO -> "(3(${n[0]}${n[1]}).${n[2]} (3(${n[3]}${n[4]}).${n[5]}"
            STACCATO_SLUR_TWO_STACCATO -> "(3.${n[0]}(${n[1]}${n[2]}) (3.${n[3]}(${n[4]}${n[5]})"
            STACCATO_TWO_SLUR_TWO -> "(3.${n[0]}.${n[1]}${n[2]} (3.${n[3]}.${n[4]}${n[5]}"
            STACCATO_ONE_SLUR_THREE -> "(3.${n[0]}(${n[1]}${n[2]}) (3.${n[3]}(${n[4]}${n[5]})"
            SLUR_THREE_STACCATO_ONE -> "((3${n[0]}${n[1]}${n[2]}) (3.${n[3]}.${n[4]}.${n[5]}"
            ALL_STACCATO -> "(3.${n[0]}.${n[1]}.${n[2]} (3.${n[3]}.${n[4]}.${n[5]}"
        }
    }
}

/**
 * The 10 technical exercise patterns that can be applied to any of the 84 parallel modes
 * (12 Tonics x 7 Parallel Modes x 10 Technical Schemes = 840 Modal Exercises).
 */
enum class ModalScheme(val id: String) {
    EJ1("EJ1"),
    EJ2("EJ2"),
    EJ4("EJ4"),
    EJ5("EJ5"),
    EJ10("EJ10"),
    EJ11("EJ11"),
    R1("R1"),
    R2("R2"),
    R4("R4"),
    R5("R5");

    val code: String
        get() = id

    val isReichert: Boolean
        get() = this == R1 || this == R2 || this == R4 || this == R5

    val shortName: String
        get() = when (this) {
            EJ1 -> "E.J. 1"
            EJ2 -> "E.J. 2"
            EJ4 -> "E.J. 4"
            EJ5 -> "E.J. 5"
            EJ10 -> "E.J. 10"
            EJ11 -> "E.J. 11"
            R1 -> "R. 1"
            R2 -> "R. 2"
            R4 -> "R. 4"
            R5 -> "R. 5"
        }

    val shortLabel: String
        get() = shortName

    val pillLabel: String
        get() = shortName

    fun subtitle(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> if (isEn) "Pentachords" else "Pentacordios"
            EJ2 -> if (isEn) "Prog. Pent." else "Progresión"
            EJ4 -> if (isEn) "2-Oct Scale" else "Escala 2 Oct."
            EJ5 -> if (isEn) "6/8 Fluency" else "Fluidez 6/8"
            EJ10 -> if (isEn) "Modal 7ths" else "Acordes 7ª"
            EJ11 -> if (isEn) "Broken 9/8" else "Quebrados 9/8"
            R1 -> "Op. 5 Nº 1"
            R2 -> "Op. 5 Nº 2"
            R4 -> "Op. 5 Nº 4"
            R5 -> "Op. 5 Nº 5"
        }
    }

    fun title(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> if (isEn) "E.J. 1 · Modal Pentachords by Degree" else "E.J. 1 · Pentacordios Modales por Grados"
            EJ2 -> if (isEn) "E.J. 2 · Harmonic Modal Pentachords" else "E.J. 2 · Pentacordios Modales en Progresión"
            EJ4 -> if (isEn) "E.J. 4 · Canonical 2-Octave Modal Scale" else "E.J. 4 · Escala Modal Canónica en 2 Octavas"
            EJ5 -> if (isEn) "E.J. 5 · Continuous 6/8 Modal Scale" else "E.J. 5 · Escala Modal Continua en 6/8"
            EJ10 -> if (isEn) "E.J. 10 · 2-Octave Modal Arpeggios" else "E.J. 10 · Arpegios Modales de 2 Octavas"
            EJ11 -> if (isEn) "E.J. 11 · Broken Modal Arpeggios (9/8)" else "E.J. 11 · Arpegios Modales Quebrados (9/8)"
            R1 -> if (isEn) "R. 1 · Reichert Op. 5 No. 1 Gruppetti (6/8)" else "R. 1 · Grupetos Modales Reichert Nº 1 (6/8)"
            R2 -> if (isEn) "R. 2 · Reichert Op. 5 No. 2 Arpeggios (2/4)" else "R. 2 · Arpegios con Anacrusa Reichert Nº 2 (2/4)"
            R4 -> if (isEn) "R. 4 · Reichert Op. 5 No. 4 Diatonic Leaps" else "R. 4 · Saltos Diatónicos Reichert Nº 4 (4/4)"
            R5 -> if (isEn) "R. 5 · Reichert Op. 5 No. 5 Triplets (2/4)" else "R. 5 · Tresillos Modales Reichert Nº 5 (2/4)"
        }
    }

    fun displayTitle(loc: LocalizationManager): String = title(loc)

    fun pedagogy(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> if (isEn) "5-note modal cells ascending step-by-step I–VIII (257 notes · 4/2)" else "Células de 5 notas sobre los 8 grados del modo I–VIII (257 notas · 4/2)"
            EJ2 -> if (isEn) "Modal pentachords over degrees I–III–V–I8–IV8–VI–IV–II–I (257 notes)" else "Pentacordios modales sobre grados I–III–V–I8–IV8–VI–IV–II–I (257 notas)"
            EJ4 -> if (isEn) "Taffanel E.J. 4 overlapping 8-note waves across 2 octaves (127 notes)" else "Olas progresivas de 8 corcheas de Taffanel E.J. 4 en 2 octavas (127 notas)"
            EJ5 -> if (isEn) "Uninterrupted 2-octave modal velocity stream in 6/8 (49 notes)" else "Flujo modal ininterrumpido de 2 octavas en 6/8 (49 notas)"
            EJ10 -> if (isEn) "7th chords built on every degree of the parallel mode (97 notes · 6/8)" else "Acordes de 7ª sobre los 7 grados del modo paralelo (97 notas · 6/8)"
            EJ11 -> if (isEn) "Broken thirds & fourths across all 7 modal chords (145 notes · 9/8)" else "Arpegios quebrados sobre los 7 acordes del modo (145 notas · 9/8)"
            R1 -> if (isEn) "Turn figures & register leaps culminating in a 2-octave tonic arpeggio" else "Giros melódicos en 6/8 culminando en gran arpegio modal de 2 octavas"
            R2 -> if (isEn) "Pickup arpeggio waves alternating I and VII across 2 octaves (61 notes)" else "Arpegios con anacrusa de 4 semicorcheas en 2/4 (61 notas)"
            R4 -> if (isEn) "Arpeggio ascents with upper neighbor turns & cascade resolution (61 notes)" else "Ascenso arpegiado con bordadura superior y cascada final (61 notas)"
            R5 -> if (isEn) "Wide-interval sixteenth triplets testing embouchure flexibility (91 notes)" else "Tresillos de semicorchea con grandes intervalos de embocadura (91 notas)"
        }
    }

    val sourceRef: String
        get() = if (isReichert) "M.-A. Reichert Op. 5" else "Taffanel & Gaubert"

    fun catalogBadge(loc: LocalizationManager): String = sourceRef

    val meter: String
        get() = when (this) {
            EJ1, EJ2, EJ4 -> "4/2"
            EJ5, EJ10, R1 -> "6/8"
            EJ11 -> "9/8"
            R2, R5 -> "2/4"
            R4 -> "C"
        }

    val unitLen: String
        get() = if (this == EJ4) "1/8" else "1/16"

    val unitLength: String
        get() = unitLen

    val barsPerStaff: Int
        get() = when (this) {
            EJ1, EJ2 -> 1
            EJ4, EJ5, EJ10, EJ11, R1, R4 -> 2
            R2, R5 -> 4
        }

    val totalNotes: Int
        get() = when (this) {
            EJ1, EJ2 -> 257
            EJ4 -> 127
            EJ5 -> 49
            EJ10 -> 97
            EJ11 -> 145
            R1 -> 43
            R2, R4 -> 61
            R5 -> 91
        }

    val measuresCount: Int
        get() = when (this) {
            EJ1, EJ2, EJ10, EJ11 -> 9
            EJ4, R2, R5 -> 8
            EJ5 -> 5
            R1, R4 -> 4
        }

    companion object {
        val taffanelSchemes: List<ModalScheme>
            get() = listOf(EJ1, EJ2, EJ4, EJ5, EJ10, EJ11)

        val reichertSchemes: List<ModalScheme>
            get() = listOf(R1, R2, R4, R5)
    }
}

// MARK: - Conservatory Coach & Practice Wizard Models (Option 1 UX)

enum class PracticeWizardDuration(val minutes: Int) {
    MIN_15(15),
    MIN_30(30),
    MIN_45(45);

    fun title(loc: LocalizationManager): String {
        return "${minutes} min"
    }

    fun subtitle(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            MIN_15 -> if (isEn) "Warm-up + 1 core block" else "Calentamiento + 1 bloque"
            MIN_30 -> if (isEn) "Balanced 3-stage routine" else "Rutina equilibrada 3 bloques"
            MIN_45 -> if (isEn) "Full technical immersion" else "Inmersión técnica completa"
        }
    }
}

enum class PracticeWizardFocus(val id: String) {
    SCALES("scales"),
    ARPEGGIOS("arpeggios"),
    REICHERT("reichert"),
    MODES840("modes840");

    fun title(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            SCALES -> if (isEn) "Scales & Finger Evenness" else "Escalas e Igualdad Digital"
            ARPEGGIOS -> if (isEn) "Arpeggios & Register leaps" else "Arpegios y Flexibilidad"
            REICHERT -> if (isEn) "Reichert Op. 5 Agility" else "Agilidad Reichert Op. 5"
            MODES840 -> if (isEn) "840 Parallel Modes Lab" else "Laboratorio 840 Modos"
        }
    }

    fun subtitle(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            SCALES -> "T&G E.J. 1, 2, 4, 5"
            ARPEGGIOS -> "T&G E.J. 10, 11 · Reichert 2, 4"
            REICHERT -> "Op. 5 · Nº 1, 2, 4, 5"
            MODES840 -> if (isEn) "12 Tonics × 7 Modes × 10 Schemes" else "12 Tónicas × 7 Modos × 10 Esquemas"
        }
    }

    val icon: String
        get() = when (this) {
            SCALES -> "🎼"
            ARPEGGIOS -> "🎹"
            REICHERT -> "⚡"
            MODES840 -> "🧭"
        }
}

data class PracticeRoutineBlock(
    val stepNumber: Int,
    val minutes: Int,
    val title: String,
    val detail: String,
    val exercise: ExerciseType,
    val modalScheme: ModalScheme,
    val tonic: Tonic,
    val mode: ModeType,
    val sectionIndex: Int
) {
    companion object {
        fun generateRoutine(
            duration: PracticeWizardDuration,
            focus: PracticeWizardFocus,
            tonic: Tonic,
            mode: ModeType,
            loc: LocalizationManager? = null
        ): List<PracticeRoutineBlock> {
            val isEn = loc?.currentLanguage == AppLanguage.ENGLISH
            val modeName = loc?.let { mode.getName(it) } ?: when (mode) {
                ModeType.IONIAN -> "Jónico"
                ModeType.LYDIAN -> "Lidio"
                ModeType.MIXOLYDIAN -> "Mixolidio"
                ModeType.DORIAN -> "Dórico"
                ModeType.AEOLIAN -> "Eólico"
                ModeType.PHRYGIAN -> "Frigio"
                ModeType.LOCRIAN -> "Lócrio"
            }
            val (m1, m2, m3) = when (duration) {
                PracticeWizardDuration.MIN_15 -> Triple(4, 6, 5)
                PracticeWizardDuration.MIN_30 -> Triple(8, 12, 10)
                PracticeWizardDuration.MIN_45 -> Triple(12, 18, 15)
            }
            val secIdx = when (tonic) {
                Tonic.DO_NATURAL -> 0
                Tonic.FA -> 2
                Tonic.SI_BEMOL -> 4
                Tonic.MI_BEMOL -> 6
                Tonic.LA_BEMOL -> 8
                Tonic.DO_SOSTENIDO -> 10
                Tonic.FA_SOSTENIDO -> 12
                Tonic.SI -> 14
                Tonic.MI -> 16
                Tonic.LA -> 18
                Tonic.RE -> 20
                Tonic.SOL -> 22
            }

            return when (focus) {
                PracticeWizardFocus.SCALES -> listOf(
                    PracticeRoutineBlock(
                        stepNumber = 1,
                        minutes = m1,
                        title = if (isEn) "1. Sound & Diatonic Scale (E.J. 1)" else "1. Sonido y Escala Diatónica (E.J. 1)",
                        detail = if (isEn) "Long tones & legato equality in ${tonic.displayName}" else "Sonoridad e igualdad ligada sobre ${tonic.displayName}",
                        exercise = ExerciseType.EJ1,
                        modalScheme = ModalScheme.EJ1,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = 0
                    ),
                    PracticeRoutineBlock(
                        stepNumber = 2,
                        minutes = m2,
                        title = if (isEn) "2. Interrupted Scales & 3rds (E.J. 4)" else "2. Escalas en Terceras (E.J. 4)",
                        detail = if (isEn) "24 Keys · Section ${secIdx + 1} (${tonic.displayName})" else "24 Tonalidades · Sección ${secIdx + 1} (${tonic.displayName})",
                        exercise = ExerciseType.EJ4,
                        modalScheme = ModalScheme.EJ4,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = secIdx
                    ),
                    PracticeRoutineBlock(
                        stepNumber = 3,
                        minutes = m3,
                        title = if (isEn) "3. Modal Application (${tonic.displayName} $modeName)" else "3. Aplicación Modal (${tonic.displayName} $modeName)",
                        detail = if (isEn) "Parallel mode in E.J. 5 (6/8 fluency)" else "Modo paralelo con esquema E.J. 5 (6/8)",
                        exercise = ExerciseType.MODOS,
                        modalScheme = ModalScheme.EJ5,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = 0
                    )
                )
                PracticeWizardFocus.ARPEGGIOS -> listOf(
                    PracticeRoutineBlock(
                        stepNumber = 1,
                        minutes = m1,
                        title = if (isEn) "1. Progressive Arpeggios (E.J. 10)" else "1. Arpegios Progresivos (E.J. 10)",
                        detail = if (isEn) "6/8 flexible embouchure across 12 series" else "Flexibilidad de embocadura en 6/8",
                        exercise = ExerciseType.EJ10,
                        modalScheme = ModalScheme.EJ10,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = secIdx % 12
                    ),
                    PracticeRoutineBlock(
                        stepNumber = 2,
                        minutes = m2,
                        title = if (isEn) "2. Broken 7th Chords (E.J. 11)" else "2. Arpegios Quebrados (E.J. 11)",
                        detail = if (isEn) "9/8 wide intervals & register control" else "Control de intervalos amplios en 9/8",
                        exercise = ExerciseType.EJ11,
                        modalScheme = ModalScheme.EJ11,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = secIdx % 12
                    ),
                    PracticeRoutineBlock(
                        stepNumber = 3,
                        minutes = m3,
                        title = if (isEn) "3. Modal Arpeggio (${tonic.displayName} $modeName · E.J. 10)" else "3. Arpegio Modal (${tonic.displayName} $modeName · E.J. 10)",
                        detail = if (isEn) "Modal triads in parallel system" else "Tríadas del modo en sistema paralelo",
                        exercise = ExerciseType.MODOS,
                        modalScheme = ModalScheme.EJ10,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = 0
                    )
                )
                PracticeWizardFocus.REICHERT -> listOf(
                    PracticeRoutineBlock(
                        stepNumber = 1,
                        minutes = m1,
                        title = if (isEn) "1. Reichert Op. 5 Nº 1 (6/8 Fluency)" else "1. Reichert Op. 5 Nº 1 (Fluidez 6/8)",
                        detail = if (isEn) "Op. 5 · Key ${secIdx + 1}/25" else "Op. 5 · Tonalidad ${secIdx + 1}/25",
                        exercise = ExerciseType.R1,
                        modalScheme = ModalScheme.R1,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = secIdx
                    ),
                    PracticeRoutineBlock(
                        stepNumber = 2,
                        minutes = m2,
                        title = if (isEn) "2. Reichert Op. 5 Nº 2 & Nº 4 (Intervals)" else "2. Reichert Op. 5 Nº 2 y Nº 4 (Intervalos)",
                        detail = if (isEn) "Wide leaps & diatonic thirds" else "Saltos de octava y terceras diatónicas",
                        exercise = ExerciseType.R2,
                        modalScheme = ModalScheme.R2,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = secIdx
                    ),
                    PracticeRoutineBlock(
                        stepNumber = 3,
                        minutes = m3,
                        title = if (isEn) "3. Modal Reichert (${tonic.displayName} $modeName · R. 5)" else "3. Reichert Modal (${tonic.displayName} $modeName · R. 5)",
                        detail = if (isEn) "Op. 5 Nº 5 triplets adapted to ${tonic.displayName} $modeName" else "Tresillos Op. 5 Nº 5 en ${tonic.displayName} $modeName",
                        exercise = ExerciseType.MODOS,
                        modalScheme = ModalScheme.R5,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = 0
                    )
                )
                PracticeWizardFocus.MODES840 -> listOf(
                    PracticeRoutineBlock(
                        stepNumber = 1,
                        minutes = m1,
                        title = if (isEn) "1. Modal Scale (${tonic.displayName} $modeName · E.J. 1)" else "1. Escala Modal (${tonic.displayName} $modeName · E.J. 1)",
                        detail = if (isEn) "Intonation & characteristic modal degrees" else "Afinación y grados característicos del modo",
                        exercise = ExerciseType.MODOS,
                        modalScheme = ModalScheme.EJ1,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = 0
                    ),
                    PracticeRoutineBlock(
                        stepNumber = 2,
                        minutes = m2,
                        title = if (isEn) "2. Modal Thirds & Arpeggios (E.J. 4 & E.J. 10)" else "2. Terceras y Arpegios Modales (E.J. 4 / E.J. 10)",
                        detail = if (isEn) "Taffanel & Gaubert patterns in ${tonic.displayName} $modeName" else "Patrones Taffanel & Gaubert en ${tonic.displayName} $modeName",
                        exercise = ExerciseType.MODOS,
                        modalScheme = ModalScheme.EJ4,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = 0
                    ),
                    PracticeRoutineBlock(
                        stepNumber = 3,
                        minutes = m3,
                        title = if (isEn) "3. Modal Reichert Op. 5 (${tonic.displayName} $modeName · R. 1)" else "3. Reichert Op. 5 Modal (${tonic.displayName} $modeName · R. 1)",
                        detail = if (isEn) "6/8 virtuoso pattern in parallel mode" else "Virtuosismo en 6/8 sobre modo paralelo",
                        exercise = ExerciseType.MODOS,
                        modalScheme = ModalScheme.R1,
                        tonic = tonic,
                        mode = mode,
                        sectionIndex = 0
                    )
                )
            }
        }
    }
}

object CoachStrings {
    fun coachBadge(loc: LocalizationManager) = loc.t("coach_badge")
    fun coachHeroTitle(loc: LocalizationManager) = loc.t("coach_title")
    fun coachHeroSubtitle(loc: LocalizationManager) = loc.t("coach_subtitle")
    fun resumeLastSession(loc: LocalizationManager) = loc.t("coach_resume_banner")
    fun openWizardButton(loc: LocalizationManager) = loc.t("coach_open_wizard")
    fun wizardTitle(loc: LocalizationManager) = loc.t("coach_wizard_title")
    fun step1Title(loc: LocalizationManager) = loc.t("coach_step1_title")
    fun step2Title(loc: LocalizationManager) = loc.t("coach_step2_title")
    fun step3Title(loc: LocalizationManager) = loc.t("coach_step3_title")
    fun startBlockButton(loc: LocalizationManager) = loc.t("coach_resume_action")
    fun level1TonicHeader(loc: LocalizationManager) = loc.t("coach_level1_tonic")
    fun level2ModeHeader(loc: LocalizationManager) = loc.t("coach_level2_mode")
    fun level3SchemeHeader(loc: LocalizationManager) = loc.t("coach_level3_scheme")
    fun level3SchemeSubtitle(loc: LocalizationManager) = loc.t("coach_level3_subtitle")
}


