package com.seagomezar.flutemodes.model

enum class ExerciseType(val id: String) {
    EJ1("ej1"),
    EJ2("ej2"),
    EJ4("ej4");

    val isChromaticExercise: Boolean
        get() = this == EJ1 || this == EJ2

    val pillLabel: String
        get() = when (this) {
            EJ1 -> "E.J. 1"
            EJ2 -> "E.J. 2"
            EJ4 -> "E.J. 4"
        }

    fun displayTitle(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> if (isEn) "E.J. 1 · Major (10 Arts.)" else "E.J. 1 · Mayor (10 Arts.)"
            EJ2 -> if (isEn) "E.J. 2 · Minor (10 Arts.)" else "E.J. 2 · Menor (10 Arts.)"
            EJ4 -> if (isEn) "E.J. 4 · 84 Parallel Modes" else "E.J. 4 · 84 Modos Paralelos"
        }
    }

    fun shortLabel(loc: LocalizationManager): String {
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH
        return when (this) {
            EJ1 -> if (isEn) "E.J. 1 (Maj)" else "E.J. 1 (May)"
            EJ2 -> if (isEn) "E.J. 2 (Min)" else "E.J. 2 (Men)"
            EJ4 -> if (isEn) "E.J. 4 (84)" else "E.J. 4 (84)"
        }
    }
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
