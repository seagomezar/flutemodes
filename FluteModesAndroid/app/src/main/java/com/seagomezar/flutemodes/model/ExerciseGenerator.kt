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

    internal data class EJ1Measure(
        val num: Int,
        val beats: List<List<String>>,
        val prefix: String,
        val suffix: String
    )

    internal val ej1RawMeasures = listOf(
        EJ1Measure(1,  listOf(listOf("D","E","^F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E")), "|:", "|"),
        EJ1Measure(2,  listOf(listOf("D","_E","=F","G","_A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(3,  listOf(listOf("_E","F","G","_A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(4,  listOf(listOf("^D","=E","^F","^G","=A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(5,  listOf(listOf("E","^F","^G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(6,  listOf(listOf("E","=F","=G","A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(7,  listOf(listOf("F","G","A","_B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(8,  listOf(listOf("^E","^F","^G","^A","=B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(9,  listOf(listOf("^F","^G","^A","B","^c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(10, listOf(listOf("^F","=G","=A","B","=c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","A","G","F")), "", "|"),
        EJ1Measure(11, listOf(listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A")), "", "|"),
        EJ1Measure(12, listOf(listOf("G","_A","_B","c","_d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","B","A","G")), "", "|"),
        EJ1Measure(13, listOf(listOf("_A","_B","c","_d","_e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B")), "", "|"),
        EJ1Measure(14, listOf(listOf("^G","=A","=B","^c","=d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","B","A","G")), "", "|"),
        EJ1Measure(15, listOf(listOf("A","B","^c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B")), "", "|"),
        EJ1Measure(16, listOf(listOf("A","_B","=c","d","_e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(17, listOf(listOf("_B","c","d","_e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(18, listOf(listOf("^A","=B","^c","^d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(19, listOf(listOf("B","^c","^d","e","^f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(20, listOf(listOf("B","=c","=d","e","=f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","d","c","B")), "", "|"),
        EJ1Measure(21, listOf(listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d")), "", "|"),
        EJ1Measure(22, listOf(listOf("c","_d","_e","f","_g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","e","d","c")), "", "|"),
        EJ1Measure(23, listOf(listOf("_d","_e","f","_g","_a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e")), "", "|"),
        EJ1Measure(24, listOf(listOf("^c","=d","=e","^f","=g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","e","d","c")), "", ":|"),
        EJ1Measure(25, listOf(listOf("d","e","^f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e")), "", "|"),
        EJ1Measure(26, listOf(listOf("d","_e","=f","g","_a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(27, listOf(listOf("_e","f","g","_a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(28, listOf(listOf("^d","=e","^f","^g","=a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(29, listOf(listOf("e","^f","^g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(30, listOf(listOf("e","=f","=g","a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","g","f","e")), "", "| f4 z4 z8 |]")
    )

    internal val ej2RawMeasures = listOf(
        EJ1Measure(1,  listOf(listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E")), "|:", "|"),
        EJ1Measure(2,  listOf(listOf("D","_E","F","G","_A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(3,  listOf(listOf("_E","F","_G","_A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(4,  listOf(listOf("^D","=E","^F","^G","=A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(5,  listOf(listOf("E","^F","=G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(6,  listOf(listOf("E","=F","G","A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(7,  listOf(listOf("F","G","_A","_B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(8,  listOf(listOf("^E","^F","^G","^A","=B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(9,  listOf(listOf("^F","^G","=A","B","^c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(10, listOf(listOf("^F","=G","A","B","=c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","A","G","F")), "", "|"),
        EJ1Measure(11, listOf(listOf("G","A","_B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A")), "", "|"),
        EJ1Measure(12, listOf(listOf("^^F","^G","^A","=B","^c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","A","G","F")), "", "|"),
        EJ1Measure(13, listOf(listOf("^G","^A","B","^c","^d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A")), "", "|"),
        EJ1Measure(14, listOf(listOf("^G","=A","B","^c","=d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","B","A","G")), "", "|"),
        EJ1Measure(15, listOf(listOf("A","B","=c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B")), "", "|"),
        EJ1Measure(16, listOf(listOf("A","_B","c","d","_e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(17, listOf(listOf("_B","c","_d","_e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(18, listOf(listOf("^A","=B","^c","^d","=e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(19, listOf(listOf("B","^c","=d","e","^f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(20, listOf(listOf("B","=c","d","e","=f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","d","c","B")), "", "|"),
        EJ1Measure(21, listOf(listOf("c","d","_e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d")), "", "|"),
        EJ1Measure(22, listOf(listOf("^B","^c","^d","^e","^f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","d","c","B")), "", "|"),
        EJ1Measure(23, listOf(listOf("^c","^d","=e","^f","^g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d")), "", "|"),
        EJ1Measure(24, listOf(listOf("^c","=d","e","^f","=g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","e","d","c")), "", ":|"),
        EJ1Measure(25, listOf(listOf("d","e","=f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e")), "", "|"),
        EJ1Measure(26, listOf(listOf("d","_e","f","g","_a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(27, listOf(listOf("_e","f","_g","_a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(28, listOf(listOf("^d","=e","^f","^g","=a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(29, listOf(listOf("e","^f","=g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(30, listOf(listOf("e","=f","g","a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","g","f","e")), "", "| f4 z4 z8 |]")
    )

    /**
     * Generates the complete Urtext ABC score for Taffanel & Gaubert E.J. 1
     * (Editions Alphonse Leduc, Plate A. L. 16.588) with the selected articulation.
     */
    fun generateEJ1ABC(
        articulation: EJ1Articulation,
        tempoBPM: Int = 80,
        loc: LocalizationManager
    ): String {
        return generateChromaticABC(
            exerciseNum = 1,
            rawMeasures = ej1RawMeasures,
            articulation = articulation,
            tempoBPM = tempoBPM,
            loc = loc
        )
    }

    /**
     * Generates the complete Urtext ABC score for Taffanel & Gaubert E.J. 2
     * (Editions Alphonse Leduc, Plate A. L. 16.588) with the selected articulation.
     */
    fun generateEJ2ABC(
        articulation: EJ1Articulation,
        tempoBPM: Int = 80,
        loc: LocalizationManager
    ): String {
        return generateChromaticABC(
            exerciseNum = 2,
            rawMeasures = ej2RawMeasures,
            articulation = articulation,
            tempoBPM = tempoBPM,
            loc = loc
        )
    }

    private fun generateChromaticABC(
        exerciseNum: Int,
        rawMeasures: List<EJ1Measure>,
        articulation: EJ1Articulation,
        tempoBPM: Int,
        loc: LocalizationManager
    ): String {
        val lines = mutableListOf(
            "X:1",
            "T:E. J. $exerciseNum — ${articulation.title(loc)}",
            "C:Paul Taffanel & Philippe Gaubert (A. L. 16.588)",
            "% EJ${exerciseNum}_LEDUC_ART:${articulation.id}",
            "%%barsperstaff 1",
            "M:4/2",
            "L:1/16",
            "Q:1/4=$tempoBPM",
            "K:C",
            "V:1 clef=treble stem=up",
            "%%score 1"
        )

        var currentStem = "up"
        for (m in rawMeasures) {
            val targetStem = if (m.num <= 10) "up" else "down"
            if (targetStem != currentStem) {
                lines.add("[V:1 stem=$targetStem]")
                currentStem = targetStem
            }
            val artBeats = m.beats.joinToString(" ") { articulation.apply(it) }
            val annot = when {
                m.num == 1 && exerciseNum == 1 -> "\"^Reprise à l'octave\""
                m.num == 25 -> "\"^8va\""
                else -> ""
            }
            if (m.prefix.isNotEmpty()) {
                lines.add("${m.prefix} $annot$artBeats ${m.suffix}")
            } else {
                lines.add("$annot$artBeats ${m.suffix}")
            }
        }

        return lines.joinToString("\n")
    }

    /**
     * Generates the marker ABC score for Taffanel & Gaubert E.J. 4
     * (Editions Alphonse Leduc, Plate A. L. 16.588, pages 111-114)
     */
    fun generateEJ4ABC(
        articulation: EJ4Articulation,
        section: EJ4Section = EJ4Section.C_MAJOR,
        tempoBPM: Int = 90
    ): String {
        return listOf(
            "X:1",
            "T:E. J. 4 — ${section.titleEs}",
            "C:Paul Taffanel & Philippe Gaubert (A. L. 16.588)",
            "% EJ4_LEDUC_ART:${articulation.id}:SEC:${section.id}",
            "M:4/2",
            "L:1/8",
            "Q:1/2=$tempoBPM",
            "K:${section.keySig}",
            "C16 |]"
        ).joinToString("\n")
    }

    /**
     * Precomputed MIDI note sequences for each of the 25 tonal sections of E.J. 4 (Urtext A. L. 16.588)
     */
    val ej4SectionMidiNotes: List<IntArray> = listOf(
        intArrayOf(60, 62, 64, 65, 67, 69, 71, 72, 74, 72, 71, 69, 67, 65, 64, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 76, 74, 72, 71, 69, 67, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 79, 77, 76, 74, 72, 71, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 83, 81, 79, 77, 76, 74, 72, 71, 72, 74, 76, 77, 79, 81, 83, 81, 79, 77, 76, 74, 72, 71, 69, 67, 69, 71, 72, 74, 76, 77, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 65, 67, 69, 71, 72, 74, 76, 74, 72, 71, 69, 67, 65, 64, 62, 60, 62, 64, 65, 67, 69, 71, 72, 71, 69, 68, 65, 64, 74, 72, 71), // 1. Do Mayor (C Major)
        intArrayOf(69, 71, 72, 74, 76, 78, 80, 81, 83, 81, 80, 77, 76, 74, 72, 71, 72, 74, 76, 78, 80, 81, 83, 84, 86, 84, 83, 81, 79, 77, 76, 74, 76, 78, 80, 81, 83, 84, 86, 88, 89, 88, 86, 84, 83, 81, 80, 78, 80, 81, 83, 84, 86, 88, 90, 92, 93, 91, 89, 88, 86, 84, 83, 81, 80, 81, 83, 84, 86, 88, 89, 91, 89, 88, 86, 84, 83, 81, 79, 77, 76, 78, 80, 81, 83, 84, 86, 88, 86, 84, 83, 81, 79, 77, 76, 74, 72, 74, 76, 78, 80, 81, 83, 84, 83, 81, 80, 77, 76, 74, 72, 71, 69, 71, 72, 74, 76, 78, 80, 81, 79, 77, 76, 74, 72, 70, 69, 67), // 2. La menor (Relatif Mineur)
        intArrayOf(65, 67, 69, 70, 72, 74, 76, 77, 79, 77, 76, 74, 72, 70, 69, 67, 69, 70, 72, 74, 76, 77, 79, 81, 82, 81, 79, 77, 76, 74, 72, 70, 72, 74, 76, 77, 79, 81, 82, 84, 86, 84, 82, 81, 79, 77, 76, 74, 76, 77, 79, 81, 82, 84, 86, 88, 89, 88, 86, 84, 82, 81, 79, 77, 76, 77, 79, 81, 82, 84, 86, 88, 86, 84, 82, 81, 79, 77, 76, 74, 72, 74, 76, 77, 79, 81, 82, 84, 82, 81, 79, 77, 76, 74, 72, 70, 69, 70, 72, 74, 76, 77, 79, 81, 79, 77, 76, 74, 72, 70, 69, 67, 65, 67, 69, 70, 72, 74, 76, 77, 76, 74, 73, 70, 69, 67, 65, 64), // 3. Fa Mayor (F Major)
        intArrayOf(62, 64, 65, 67, 69, 71, 73, 74, 76, 74, 73, 70, 69, 67, 65, 64, 65, 67, 69, 71, 73, 74, 76, 77, 79, 77, 76, 74, 72, 70, 69, 67, 69, 71, 73, 74, 76, 77, 79, 81, 82, 81, 79, 77, 76, 74, 73, 71, 73, 74, 76, 77, 79, 81, 83, 85, 86, 84, 82, 81, 79, 77, 76, 74, 73, 74, 76, 77, 79, 81, 82, 84, 82, 81, 79, 77, 76, 74, 72, 70, 69, 71, 73, 74, 76, 77, 79, 81, 79, 77, 76, 74, 72, 70, 69, 67, 65, 67, 69, 71, 73, 74, 76, 77, 76, 74, 73, 70, 69, 67, 65, 64, 62, 64, 65, 67, 69, 71, 73, 74, 72, 70, 69, 67, 65, 75, 74, 72), // 4. Re menor (Mineur)
        intArrayOf(70, 72, 74, 75, 77, 79, 81, 82, 84, 82, 81, 79, 77, 75, 74, 72, 74, 75, 77, 79, 81, 82, 84, 86, 87, 86, 84, 82, 81, 79, 77, 75, 77, 79, 81, 82, 84, 86, 87, 89, 91, 89, 87, 86, 84, 82, 81, 79, 81, 82, 84, 86, 87, 89, 91, 93, 94, 93, 91, 89, 87, 86, 84, 82, 81, 82, 84, 86, 87, 89, 91, 93, 91, 89, 87, 86, 84, 82, 81, 79, 77, 79, 81, 82, 84, 86, 87, 89, 87, 86, 84, 82, 81, 79, 77, 75, 74, 75, 77, 79, 81, 82, 84, 86, 84, 82, 81, 79, 77, 75, 74, 72, 70, 72, 74, 75, 77, 79, 81, 82, 81, 79, 78, 75, 74, 72, 70, 69), // 5. Si♭ Mayor (B♭ Major)
        intArrayOf(67, 69, 70, 72, 74, 76, 78, 79, 81, 79, 78, 75, 74, 72, 70, 69, 70, 72, 74, 76, 78, 79, 81, 82, 84, 82, 81, 79, 77, 75, 74, 72, 74, 76, 78, 79, 81, 82, 84, 86, 87, 86, 84, 82, 81, 79, 78, 76, 78, 79, 81, 82, 84, 86, 88, 90, 91, 89, 87, 86, 84, 82, 81, 79, 78, 79, 81, 82, 84, 86, 87, 89, 87, 86, 84, 82, 81, 79, 77, 75, 74, 76, 78, 79, 81, 82, 84, 86, 84, 82, 81, 79, 77, 75, 74, 72, 70, 72, 74, 76, 78, 79, 81, 82, 81, 79, 78, 75, 74, 72, 70, 69, 67, 69, 70, 72, 74, 76, 78, 79, 77, 75, 74, 72, 70, 68, 67, 65), // 6. Sol menor (Mineur)
        intArrayOf(63, 65, 67, 68, 70, 72, 74, 75, 77, 75, 74, 72, 70, 68, 67, 65, 67, 68, 70, 72, 74, 75, 77, 79, 80, 79, 77, 75, 74, 72, 70, 68, 70, 72, 74, 75, 77, 79, 80, 82, 84, 82, 80, 79, 77, 75, 74, 72, 74, 75, 77, 79, 80, 82, 84, 86, 87, 86, 84, 82, 80, 79, 77, 75, 74, 75, 77, 79, 80, 82, 84, 86, 84, 82, 80, 79, 77, 75, 74, 72, 70, 72, 74, 75, 77, 79, 80, 82, 80, 79, 77, 75, 74, 72, 70, 68, 67, 68, 70, 72, 74, 75, 77, 79, 77, 75, 74, 72, 70, 68, 67, 65, 63, 65, 67, 68, 70, 72, 74, 75, 74, 72, 71, 68, 67, 65, 63, 62), // 7. Mi♭ Mayor (E♭ Major)
        intArrayOf(60, 62, 63, 65, 67, 69, 71, 72, 74, 72, 71, 68, 67, 65, 63, 62, 63, 65, 67, 69, 71, 72, 74, 75, 77, 75, 74, 72, 70, 68, 67, 65, 67, 69, 71, 72, 74, 75, 77, 79, 80, 79, 77, 75, 74, 72, 71, 69, 71, 72, 74, 75, 77, 79, 81, 83, 84, 82, 80, 79, 77, 75, 74, 72, 71, 72, 74, 75, 77, 79, 80, 82, 80, 79, 77, 75, 74, 72, 70, 68, 67, 69, 71, 72, 74, 75, 77, 79, 77, 75, 74, 72, 70, 68, 67, 65, 63, 65, 67, 69, 71, 72, 74, 75, 74, 72, 71, 68, 67, 65, 63, 62, 60, 62, 63, 65, 67, 69, 71, 72, 70, 68, 67, 65, 63, 73, 72, 70), // 8. Do menor (Mineur)
        intArrayOf(68, 70, 72, 73, 75, 77, 79, 80, 82, 80, 79, 77, 75, 73, 72, 70, 72, 73, 75, 77, 79, 80, 82, 84, 85, 84, 82, 80, 79, 77, 75, 73, 75, 77, 79, 80, 82, 84, 85, 87, 89, 87, 85, 84, 82, 80, 79, 77, 79, 80, 82, 84, 85, 87, 89, 91, 92, 91, 89, 87, 85, 84, 82, 80, 79, 80, 82, 84, 85, 87, 89, 91, 89, 87, 85, 84, 82, 80, 79, 77, 75, 77, 79, 80, 82, 84, 85, 87, 85, 84, 82, 80, 79, 77, 75, 73, 72, 73, 75, 77, 79, 80, 82, 84, 82, 80, 79, 77, 75, 73, 72, 70, 68, 70, 72, 73, 75, 77, 79, 80, 79, 77, 76, 73, 72, 70, 68, 67), // 9. La♭ Mayor (A♭ Major)
        intArrayOf(65, 67, 68, 70, 72, 74, 76, 77, 79, 77, 76, 73, 72, 70, 68, 67, 68, 70, 72, 74, 76, 77, 79, 80, 82, 80, 79, 77, 75, 73, 72, 70, 72, 74, 76, 77, 79, 80, 82, 84, 85, 84, 82, 80, 79, 77, 76, 74, 76, 77, 79, 80, 82, 84, 86, 88, 89, 87, 85, 84, 82, 80, 79, 77, 76, 77, 79, 80, 82, 84, 85, 87, 85, 84, 82, 80, 79, 77, 75, 73, 72, 74, 76, 77, 79, 80, 82, 84, 82, 80, 79, 77, 75, 73, 72, 70, 68, 70, 72, 74, 76, 77, 79, 80, 79, 77, 76, 73, 72, 70, 68, 67, 65, 67, 68, 70, 72, 74, 76, 77, 75, 73, 72, 70, 68, 66, 65, 63), // 10. Fa menor (Mineur)
        intArrayOf(61, 63, 65, 66, 68, 70, 72, 73, 75, 73, 72, 70, 68, 66, 65, 63, 65, 66, 68, 70, 72, 73, 75, 77, 78, 77, 75, 73, 72, 70, 68, 66, 68, 70, 72, 73, 75, 77, 78, 80, 82, 80, 78, 77, 75, 73, 72, 70, 72, 73, 75, 77, 78, 80, 82, 84, 85, 84, 82, 80, 78, 77, 75, 73, 72, 73, 75, 77, 78, 80, 82, 84, 82, 80, 78, 77, 75, 73, 72, 70, 68, 70, 72, 73, 75, 77, 78, 80, 78, 77, 75, 73, 72, 70, 68, 66, 65, 66, 68, 70, 72, 73, 75, 77, 75, 73, 72, 70, 68, 66, 65, 63, 61, 63, 65, 66, 68, 70, 72, 73, 72, 70, 69, 66, 65, 75, 73, 72), // 11. Re♭ Mayor (D♭ Major)
        intArrayOf(70, 72, 73, 75, 77, 79, 81, 82, 84, 82, 81, 78, 77, 75, 73, 72, 73, 75, 77, 79, 81, 82, 84, 85, 87, 85, 84, 82, 80, 78, 77, 75, 77, 79, 81, 82, 84, 85, 87, 89, 90, 89, 87, 85, 84, 82, 81, 79, 81, 82, 84, 85, 87, 89, 91, 93, 94, 92, 90, 89, 87, 85, 84, 82, 81, 82, 84, 85, 87, 89, 90, 92, 90, 89, 87, 85, 84, 82, 80, 78, 77, 79, 81, 82, 84, 85, 87, 89, 87, 85, 84, 82, 80, 78, 77, 75, 73, 75, 77, 79, 81, 82, 84, 85, 84, 82, 81, 78, 77, 75, 73, 72, 70, 72, 73, 75, 77, 79, 81, 82, 80, 78, 77, 75, 73, 71, 70, 68), // 12. Si♭ menor (Mineur)
        intArrayOf(66, 68, 70, 71, 73, 75, 77, 78, 80, 78, 77, 75, 73, 71, 70, 68, 70, 71, 73, 75, 77, 78, 80, 82, 83, 82, 80, 78, 77, 75, 73, 71, 73, 75, 77, 78, 80, 82, 83, 85, 87, 85, 83, 82, 80, 78, 77, 75, 77, 78, 80, 82, 83, 85, 87, 89, 90, 89, 87, 85, 83, 82, 80, 78, 77, 78, 80, 82, 83, 85, 87, 89, 87, 85, 83, 82, 80, 78, 77, 75, 73, 75, 77, 78, 80, 82, 83, 85, 83, 82, 80, 78, 77, 75, 73, 71, 70, 71, 73, 75, 77, 78, 80, 82, 80, 78, 77, 75, 73, 71, 70, 68, 66, 68, 70, 71, 73, 75, 77, 78, 77, 75, 74, 71, 70, 68, 66, 65), // 13. Sol♭ Mayor (G♭ Major)
        intArrayOf(63, 65, 66, 68, 70, 72, 74, 75, 77, 75, 74, 71, 70, 68, 66, 65, 66, 68, 70, 72, 74, 75, 77, 78, 80, 78, 77, 75, 73, 71, 70, 68, 70, 72, 74, 75, 77, 78, 80, 82, 83, 82, 80, 78, 77, 75, 74, 72, 74, 75, 77, 78, 80, 82, 84, 86, 87, 85, 83, 82, 80, 78, 77, 75, 74, 75, 77, 78, 80, 82, 83, 85, 83, 82, 80, 78, 77, 75, 73, 71, 70, 72, 74, 75, 77, 78, 80, 82, 80, 78, 77, 75, 73, 71, 70, 68, 66, 68, 70, 72, 74, 75, 77, 78, 77, 75, 74, 71, 70, 68, 66, 65, 63, 65, 66, 68, 70, 72, 74, 75, 73, 71, 70, 68, 66, 76, 75, 73), // 14. Mi♭ menor (Mineur)
        intArrayOf(71, 73, 75, 76, 78, 80, 82, 83, 85, 83, 82, 80, 78, 76, 75, 73, 75, 76, 78, 80, 82, 83, 85, 87, 88, 87, 85, 83, 82, 80, 78, 76, 78, 80, 82, 83, 85, 87, 88, 90, 92, 90, 88, 87, 85, 83, 82, 80, 82, 83, 85, 87, 88, 90, 92, 94, 95, 94, 92, 90, 88, 87, 85, 83, 82, 83, 85, 87, 88, 90, 92, 94, 92, 90, 88, 87, 85, 83, 82, 80, 78, 80, 82, 83, 85, 87, 88, 90, 88, 87, 85, 83, 82, 80, 78, 76, 75, 76, 78, 80, 82, 83, 85, 87, 85, 83, 82, 80, 78, 76, 75, 73, 71, 73, 75, 76, 78, 80, 82, 83, 82, 80, 79, 76, 75, 73, 71, 70), // 15. Si Mayor (B Major)
        intArrayOf(68, 70, 71, 73, 75, 77, 79, 80, 82, 80, 79, 76, 75, 73, 71, 70, 71, 73, 75, 77, 79, 80, 82, 83, 85, 83, 82, 80, 78, 76, 75, 73, 75, 77, 79, 80, 82, 83, 85, 87, 88, 87, 85, 83, 82, 80, 79, 77, 79, 80, 82, 83, 85, 87, 89, 91, 92, 90, 88, 87, 85, 83, 82, 80, 79, 80, 82, 83, 85, 87, 88, 90, 88, 87, 85, 83, 82, 80, 78, 76, 75, 77, 79, 80, 82, 83, 85, 87, 85, 83, 82, 80, 78, 76, 75, 73, 71, 73, 75, 77, 79, 80, 82, 83, 82, 80, 79, 76, 75, 73, 71, 70, 68, 70, 71, 73, 75, 77, 79, 80, 78, 76, 75, 73, 71, 69, 68, 66), // 16. Sol♯ menor (Mineur)
        intArrayOf(64, 66, 68, 69, 71, 73, 75, 76, 78, 76, 75, 73, 71, 69, 68, 66, 68, 69, 71, 73, 75, 76, 78, 80, 81, 80, 78, 76, 75, 73, 71, 69, 71, 73, 75, 76, 78, 80, 81, 83, 85, 83, 81, 80, 78, 76, 75, 73, 75, 76, 78, 80, 81, 83, 85, 87, 88, 87, 85, 83, 81, 80, 78, 76, 75, 76, 78, 80, 81, 83, 85, 87, 85, 83, 81, 80, 78, 76, 75, 73, 71, 73, 75, 76, 78, 80, 81, 83, 81, 80, 78, 76, 75, 73, 71, 69, 68, 69, 71, 73, 75, 76, 78, 80, 78, 76, 75, 73, 71, 69, 68, 66, 64, 66, 68, 69, 71, 73, 75, 76, 75, 73, 72, 69, 68, 66, 64, 63), // 17. Mi Mayor (E Major)
        intArrayOf(61, 63, 64, 66, 68, 70, 72, 73, 75, 73, 72, 69, 68, 66, 64, 63, 64, 66, 68, 70, 72, 73, 75, 76, 78, 76, 75, 73, 71, 69, 68, 66, 68, 70, 72, 73, 75, 76, 78, 80, 81, 80, 78, 76, 75, 73, 72, 70, 72, 73, 75, 76, 78, 80, 82, 84, 85, 83, 81, 80, 78, 76, 75, 73, 72, 73, 75, 76, 78, 80, 81, 83, 81, 80, 78, 76, 75, 73, 71, 69, 68, 70, 72, 73, 75, 76, 78, 80, 78, 76, 75, 73, 71, 69, 68, 66, 64, 66, 68, 70, 72, 73, 75, 76, 75, 73, 72, 69, 68, 66, 64, 63, 61, 63, 64, 66, 68, 70, 72, 73, 71, 69, 68, 66, 64, 74, 73, 71), // 18. Do♯ menor (Mineur)
        intArrayOf(69, 71, 73, 74, 76, 78, 80, 81, 83, 81, 80, 78, 76, 74, 73, 71, 73, 74, 76, 78, 80, 81, 83, 85, 86, 85, 83, 81, 80, 78, 76, 74, 76, 78, 80, 81, 83, 85, 86, 88, 90, 88, 86, 85, 83, 81, 80, 78, 80, 81, 83, 85, 86, 88, 90, 92, 93, 92, 90, 88, 86, 85, 83, 81, 80, 81, 83, 85, 86, 88, 90, 92, 90, 88, 86, 85, 83, 81, 80, 78, 76, 78, 80, 81, 83, 85, 86, 88, 86, 85, 83, 81, 80, 78, 76, 74, 73, 74, 76, 78, 80, 81, 83, 85, 83, 81, 80, 78, 76, 74, 73, 71, 69, 71, 73, 74, 76, 78, 80, 81, 80, 78, 77, 74, 73, 71, 69, 68), // 19. La Mayor (A Major)
        intArrayOf(66, 68, 69, 71, 73, 75, 77, 78, 80, 78, 77, 74, 73, 71, 69, 68, 69, 71, 73, 75, 77, 78, 80, 81, 83, 81, 80, 78, 76, 74, 73, 71, 73, 75, 77, 78, 80, 81, 83, 85, 86, 85, 83, 81, 80, 78, 77, 75, 77, 78, 80, 81, 83, 85, 87, 89, 90, 88, 86, 85, 83, 81, 80, 78, 77, 78, 80, 81, 83, 85, 86, 88, 86, 85, 83, 81, 80, 78, 76, 74, 73, 75, 77, 78, 80, 81, 83, 85, 83, 81, 80, 78, 76, 74, 73, 71, 69, 71, 73, 75, 77, 78, 80, 81, 80, 78, 77, 74, 73, 71, 69, 68, 66, 68, 69, 71, 73, 75, 77, 78, 76, 74, 73, 71, 69, 67, 66, 64), // 20. Fa♯ menor (Mineur)
        intArrayOf(62, 64, 66, 67, 69, 71, 73, 74, 76, 74, 73, 71, 69, 67, 66, 64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 78, 76, 74, 73, 71, 69, 67, 69, 71, 73, 74, 76, 78, 79, 81, 83, 81, 79, 78, 76, 74, 73, 71, 73, 74, 76, 78, 79, 81, 83, 85, 86, 85, 83, 81, 79, 78, 76, 74, 73, 74, 76, 78, 79, 81, 83, 85, 83, 81, 79, 78, 76, 74, 73, 71, 69, 71, 73, 74, 76, 78, 79, 81, 79, 78, 76, 74, 73, 71, 69, 67, 66, 67, 69, 71, 73, 74, 76, 78, 76, 74, 73, 71, 69, 67, 66, 64, 62, 64, 66, 67, 69, 71, 73, 74, 73, 71, 70, 67, 66, 76, 74, 73), // 21. Re Mayor (D Major)
        intArrayOf(71, 73, 74, 76, 78, 80, 82, 83, 85, 83, 82, 79, 78, 76, 74, 73, 74, 76, 78, 80, 82, 83, 85, 86, 88, 86, 85, 83, 81, 79, 78, 76, 78, 80, 82, 83, 85, 86, 88, 90, 91, 90, 88, 86, 85, 83, 82, 80, 82, 83, 85, 86, 88, 90, 92, 94, 95, 93, 91, 90, 88, 86, 85, 83, 82, 83, 85, 86, 88, 90, 91, 93, 91, 90, 88, 86, 85, 83, 81, 79, 78, 80, 82, 83, 85, 86, 88, 90, 88, 86, 85, 83, 81, 79, 78, 76, 74, 76, 78, 80, 82, 83, 85, 86, 85, 83, 82, 79, 78, 76, 74, 73, 71, 73, 74, 76, 78, 80, 82, 83, 81, 79, 78, 76, 74, 72, 71, 69), // 22. Si menor (Mineur)
        intArrayOf(67, 69, 71, 72, 74, 76, 78, 79, 81, 79, 78, 76, 74, 72, 71, 69, 71, 72, 74, 76, 78, 79, 81, 83, 84, 83, 81, 79, 78, 76, 74, 72, 74, 76, 78, 79, 81, 83, 84, 86, 88, 86, 84, 83, 81, 79, 78, 76, 78, 79, 81, 83, 84, 86, 88, 90, 91, 90, 88, 86, 84, 83, 81, 79, 78, 79, 81, 83, 84, 86, 88, 90, 88, 86, 84, 83, 81, 79, 78, 76, 74, 76, 78, 79, 81, 83, 84, 86, 84, 83, 81, 79, 78, 76, 74, 72, 71, 72, 74, 76, 78, 79, 81, 83, 81, 79, 78, 76, 74, 72, 71, 69, 67, 69, 71, 72, 74, 76, 78, 79, 78, 76, 75, 72, 71, 69, 67, 66), // 23. Sol Mayor (G Major)
        intArrayOf(64, 66, 67, 69, 71, 73, 75, 76, 78, 76, 75, 72, 71, 69, 67, 66, 67, 69, 71, 73, 75, 76, 78, 79, 81, 79, 78, 76, 74, 72, 71, 69, 71, 73, 75, 76, 78, 79, 81, 83, 84, 83, 81, 79, 78, 76, 75, 73, 75, 76, 78, 79, 81, 83, 85, 87, 88, 86, 84, 83, 81, 79, 78, 76, 75, 76, 78, 79, 81, 83, 84, 86, 84, 83, 81, 79, 78, 76, 74, 72, 71, 73, 75, 76, 78, 79, 81, 83, 81, 79, 78, 76, 74, 72, 71, 69, 67, 69, 71, 73, 75, 76, 78, 79, 78, 76, 75, 72, 71, 69, 67, 66, 64, 66, 67, 69, 71, 73, 75, 76, 74, 72, 71, 69, 67, 65, 64, 62), // 24. Mi menor (Mineur)
        intArrayOf(60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 83, 81, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 62, 60) // 25. Do Mayor (Coda Final)
    )
}
