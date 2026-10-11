package com.seagomezar.flutemodes.model

enum class ExerciseType(val id: String) {
    EJ1("ej1"),
    EJ2("ej2"),
    EJ4("ej4"),
    MODOS("modos");

    val isChromaticExercise: Boolean
        get() = this == EJ1 || this == EJ2

    val isEJ4Exercise: Boolean
        get() = this == EJ4

    val isLeducExercise: Boolean
        get() = this == EJ1 || this == EJ2 || this == EJ4

    val pillLabel: String
        get() = when (this) {
            EJ1 -> "E.J. 1"
            EJ2 -> "E.J. 2"
            EJ4 -> "E.J. 4"
            MODOS -> "84 Modos"
        }

    fun displayTitle(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> if (isEn) "E.J. 1 · Major (10 Arts.)" else "E.J. 1 · Mayor (10 Arts.)"
            EJ2 -> if (isEn) "E.J. 2 · Minor (10 Arts.)" else "E.J. 2 · Menor (10 Arts.)"
            EJ4 -> if (isEn) "E.J. 4 · 24 Keys (8 Arts.)" else "E.J. 4 · 24 Ton. (8 Arts.)"
            MODOS -> if (isEn) "84 Parallel Modes" else "84 Modos Paralelos"
        }
    }

    fun shortLabel(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> "E.J. 1"
            EJ2 -> "E.J. 2"
            EJ4 -> "E.J. 4"
            MODOS -> if (isEn) "84 Modes" else "84 Modos"
        }
    }
}

enum class EJ4Articulation(
    val id: Int,
    val formulaBadge: String
) {
    ORIGINAL(0, "A.L. 16.588"),
    ALL_SLURRED_8(1, "(8)"),
    SLURRED_4_AND_4(2, "(4)+(4)"),
    STACC_1_SLUR_3(3, "·(3) ·(3)"),
    SLUR_2_STACC_2(4, "(2)·· (2)··"),
    STACC_2_SLUR_2(5, "··(2) ··(2)"),
    STACC_1_SLUR_2_STACC_1(6, "·(2)· ·(2)·"),
    SLUR_PAIRS_2_BY_2(7, "(2)(2)(2)(2)"),
    SLUR_SYNCOPATED(8, "·(2)(2)(2)·");

    fun title(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            ORIGINAL -> if (isEn) "0. Original (As written — A. L. 16.588)" else "0. Original (Como está escrito — A. L. 16.588)"
            ALL_SLURRED_8 -> if (isEn) "1. 8 slurred: (CDEFGABc)" else "1. 8 ligadas: (CDEFGABc)"
            SLURRED_4_AND_4 -> if (isEn) "2. 4 and 4 slurred: (CDEF)(GABc)" else "2. 4 y 4 ligadas: (CDEF)(GABc)"
            STACC_1_SLUR_3 -> if (isEn) "3. 1 staccato, 3 slurred: .C(DEF) .G(ABc)" else "3. 1 picada y 3 ligadas: .C(DEF) .G(ABc)"
            SLUR_2_STACC_2 -> if (isEn) "4. 2 slurred, 2 staccato: (CD).E.F (GA).B.c" else "4. 2 ligadas y 2 picadas: (CD).E.F (GA).B.c"
            STACC_2_SLUR_2 -> if (isEn) "5. 2 staccato, 2 slurred: .C.D(EF) .G.A(Bc)" else "5. 2 picadas y 2 ligadas: .C.D(EF) .G.A(Bc)"
            STACC_1_SLUR_2_STACC_1 -> if (isEn) "6. 1 stacc., 2 slurred, 1 stacc.: .C(DE).F .G(AB).c" else "6. 1 picada, 2 ligadas y 1 picada: .C(DE).F .G(AB).c"
            SLUR_PAIRS_2_BY_2 -> if (isEn) "7. Slurred in pairs: (CD)(EF)(GA)(Bc)" else "7. De 2 en 2 ligadas: (CD)(EF)(GA)(Bc)"
            SLUR_SYNCOPATED -> if (isEn) "8. Syncopated pairs: .C(DE)(FG)(AB).c" else "8. De 2 en 2 sincopadas: .C(DE)(FG)(AB).c"
        }
    }

    fun shortTitle(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            ORIGINAL -> "Orig."
            ALL_SLURRED_8 -> if (isEn) "1: 8 Slur" else "1: 8 Lig."
            SLURRED_4_AND_4 -> "2: 4+4"
            STACC_1_SLUR_3 -> "3: 1P+3L"
            SLUR_2_STACC_2 -> "4: 2L+2P"
            STACC_2_SLUR_2 -> "5: 2P+2L"
            STACC_1_SLUR_2_STACC_1 -> "6: 1P+2L+1P"
            SLUR_PAIRS_2_BY_2 -> if (isEn) "7: 2+2" else "7: 2 en 2"
            SLUR_SYNCOPATED -> if (isEn) "8: Sync." else "8: Sinc."
        }
    }

    companion object {
        val practiceCases: List<EJ4Articulation>
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

    fun title(loc: LocalizationManager): String =
        if (loc.currentLanguage == AppLanguage.ENGLISH) titleEn else titleEs
}

enum class EJ1Articulation(
    val id: Int,
    val formulaBadge: String
) {
    ORIGINAL(0, "A.L. 16.588"),
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
    ALL_SLURRED(1, "1. Toda ligada"),
    SLURRED_FOUR_AND_FOUR(2, "2. Ligado 4 y 4"),
    SLUR_TWO_STACCATO_TWO(3, "3. Ligado 2, picado 2"),
    STACCATO_SLUR_TWO_STACCATO(4, "4. Picado 1, ligado 2, picado 1"),
    STACCATO_TWO_SLUR_TWO(5, "5. Picado 2, ligado 2"),
    STACCATO_ONE_SLUR_THREE(6, "6. Picado 1, ligado 3"),
    SLUR_THREE_STACCATO_ONE(7, "7. Ligado 3, picado 1"),
    ALL_STACCATO(8, "8. Toda picada (Staccato)");

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
}
