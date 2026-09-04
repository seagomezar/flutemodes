package com.seagomezar.flutemodes.model

object ExerciseGenerator {

    fun generateABC(
        tonic: Tonic,
        mode: ModeType,
        articulation: ArticulationPattern,
        tempoBPM: Int = 90,
        loc: LocalizationManager
    ): String {
        val keySig = mode.keySignature(tonic)
        val accMap = tonic.accidentalMap(mode)
        val baseNotes = tonic.abcNoteSequence

        val s = mutableListOf<String>()
        for ((idx, note) in baseNotes.withIndex()) {
            val degree = idx % 7
            val acc = accMap[degree]
            if (acc != null) {
                s.add("$acc$note")
            } else {
                s.add(note)
            }
        }

        fun art(notes: List<String>): String {
            return articulation.apply(notes)
        }

        // Measure 1
        val c1Asc = s.subList(0, 8)
        val c1Desc = listOf(s[8], s[7], s[6], s[5], s[4], s[3], s[2], s[1])
        val c1 = "${art(c1Asc)} ${art(c1Desc)}"

        // Measure 2
        val c2Asc = s.subList(2, 10)
        val c2Desc = listOf(s[10], s[9], s[8], s[7], s[6], s[5], s[4], s[3])
        val c2 = "${art(c2Asc)} ${art(c2Desc)}"

        // Measure 3
        val c3Asc = s.subList(4, 12)
        val c3Desc = listOf(s[12], s[11], s[10], s[9], s[8], s[7], s[6], s[5])
        val c3 = "${art(c3Asc)} ${art(c3Desc)}"

        // Measure 4 (Peak)
        val c4Asc = s.subList(6, 14)
        val c4Desc = listOf(s[14], s[13], s[12], s[11], s[10], s[9], s[8], s[7])
        val c4 = "${art(c4Asc)} ${art(c4Desc)}"

        // Measure 5
        val c5Asc = s.subList(6, 14)
        val c5Desc = listOf(s[12], s[11], s[10], s[9], s[8], s[7], s[6], s[5])
        val c5 = "${art(c5Asc)} ${art(c5Desc)}"

        // Measure 6
        val c6Asc = s.subList(4, 12)
        val c6Desc = listOf(s[10], s[9], s[8], s[7], s[6], s[5], s[4], s[3])
        val c6 = "${art(c6Asc)} ${art(c6Desc)}"

        // Measure 7
        val c7Asc = s.subList(2, 10)
        val c7Desc = listOf(s[8], s[7], s[6], s[5], s[4], s[3], s[2], s[1])
        val c7 = "${art(c7Asc)} ${art(c7Desc)}"

        // Measure 8
        val c8Asc = s.subList(0, 8)
        val c8DescNotes = listOf(s[6], s[5], s[4], s[3], s[2], s[1])
        val finalTonic = "${s[0]}2"
        val c8DescStr = "(${c8DescNotes.joinToString("")} $finalTonic)"
        val c8 = "${art(c8Asc)} $c8DescStr"

        return """
            X:1
            T:Modo ${mode.id}: ${tonic.displayName} ${mode.getName(loc)}
            % ${mode.family.displayName} | ${mode.accidentalBadge(loc)} | Fórmula: ${mode.formula}
            %%barsperstaff 2
            M:4/2
            L:1/8
            Q:1/2=$tempoBPM
            K:$keySig
            V:1 clef=treble
            %%score 1
            $c1 | $c2 |
            $c3 | $c4 |
            $c5 | $c6 |
            $c7 | $c8 |]
        """.trimIndent()
    }
}
