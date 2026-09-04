package com.seagomezar.flutemodes.model

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
