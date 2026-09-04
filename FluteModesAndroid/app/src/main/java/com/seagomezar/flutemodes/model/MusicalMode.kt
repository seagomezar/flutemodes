package com.seagomezar.flutemodes.model

enum class ModeFamily(val displayName: String) {
    MAJOR("Familia Mayor"),
    MINOR("Familia Menor")
}

enum class ModeType(
    val id: Int,
    val family: ModeFamily,
    val intervals: List<Int>, // semitone intervals from root
    val formula: String,
    val character: String
) {
    IONIAN(1, ModeFamily.MAJOR, listOf(0, 2, 4, 5, 7, 9, 11), "1 - 2 - 3 - 4 - 5 - 6 - 7", "Brillante y luminoso"),
    LYDIAN(2, ModeFamily.MAJOR, listOf(0, 2, 4, 6, 7, 9, 11), "1 - 2 - 3 - ♯4 - 5 - 6 - 7", "Etéreo y soñador"),
    MIXOLYDIAN(3, ModeFamily.MAJOR, listOf(0, 2, 4, 5, 7, 9, 10), "1 - 2 - 3 - 4 - 5 - 6 - ♭7", "Festivo y folclórico"),
    DORIAN(4, ModeFamily.MINOR, listOf(0, 2, 3, 5, 7, 9, 10), "1 - 2 - ♭3 - 4 - 5 - 6 - ♭7", "Melancólico y noble"),
    AEOLIAN(5, ModeFamily.MINOR, listOf(0, 2, 3, 5, 7, 8, 10), "1 - 2 - ♭3 - 4 - 5 - ♭6 - ♭7", "Triste e introspectivo"),
    PHRYGIAN(6, ModeFamily.MINOR, listOf(0, 1, 3, 5, 7, 8, 10), "1 - ♭2 - ♭3 - 4 - 5 - ♭6 - ♭7", "Oscuro y exótico"),
    LOCRIAN(7, ModeFamily.MINOR, listOf(0, 1, 3, 5, 6, 8, 10), "1 - ♭2 - ♭3 - 4 - ♭5 - ♭6 - ♭7", "Inestable y tenso");

    fun getName(loc: LocalizationManager): String {
        return when (this) {
            IONIAN -> loc.t("mode_1_name")
            LYDIAN -> loc.t("mode_2_name")
            MIXOLYDIAN -> loc.t("mode_3_name")
            DORIAN -> loc.t("mode_4_name")
            AEOLIAN -> loc.t("mode_5_name")
            PHRYGIAN -> loc.t("mode_6_name")
            LOCRIAN -> loc.t("mode_7_name")
        }
    }

    fun accidentalBadge(loc: LocalizationManager): String {
        return when (this) {
            IONIAN -> loc.t("acc_ionian")
            LYDIAN -> loc.t("acc_lydian")
            MIXOLYDIAN -> loc.t("acc_mixolydian")
            DORIAN -> loc.t("acc_dorian")
            AEOLIAN -> loc.t("acc_aeolian")
            PHRYGIAN -> loc.t("acc_phrygian")
            LOCRIAN -> loc.t("acc_locrian")
        }
    }

    fun keySignature(tonic: Tonic): String {
        return when (family) {
            ModeFamily.MAJOR -> tonic.majorKey
            ModeFamily.MINOR -> tonic.minorKey
        }
    }

    fun keyDescription(tonic: Tonic): String {
        return when (family) {
            ModeFamily.MAJOR -> "Armadura fija: ${tonic.majorKey} Mayor (${tonic.majorDesc})"
            ModeFamily.MINOR -> "Armadura fija: ${tonic.minorKey} Menor (${tonic.minorDesc})"
        }
    }
}
