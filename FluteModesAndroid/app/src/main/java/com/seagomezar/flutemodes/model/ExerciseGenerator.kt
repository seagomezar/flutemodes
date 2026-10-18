package com.seagomezar.flutemodes.model

object ExerciseGenerator {

    /**
     * Returns (sBase, sAcc) for the 16 diatonic scale positions (0..15) of a Parallel Mode,
     * including Urtext double flats (__B, __E) for Mi♭ Locrian and La♭ Phrygian/Locrian.
     */
    fun getModalScaleNotesPair(tonic: Tonic, mode: ModeType): Pair<List<String>, List<String>> {
        val sBase = tonic.abcNoteSequence
        val accMap = tonic.accidentalMap(mode).toMutableMap()
        if (tonic == Tonic.MI_BEMOL && mode == ModeType.LOCRIAN) {
            accMap[4] = "__"
        } else if (tonic == Tonic.LA_BEMOL && mode == ModeType.PHRYGIAN) {
            accMap[1] = "__"
        } else if (tonic == Tonic.LA_BEMOL && mode == ModeType.LOCRIAN) {
            accMap[1] = "__"
            accMap[4] = "__"
        }
        val sAcc = sBase.mapIndexed { idx, note ->
            val degree = idx % 7
            val acc = accMap[degree]
            if (acc != null) "$acc$note" else note
        }
        return Pair(sBase, sAcc)
    }

    /**
     * Applies Urtext engraving rule within a single measure: the first occurrence of an altered
     * scale position `d` in the measure carries its accidental (`sAcc[d]`), and subsequent
     * occurrences of the same `d` within that measure use `sBase[d]`.
     */
    fun resolveMeasureGroups(
        groupsOfIndices: List<List<Int>>,
        sBase: List<String>,
        sAcc: List<String>
    ): List<List<String>> {
        val seenInMeasure = mutableSetOf<Int>()
        return groupsOfIndices.map { idxList ->
            idxList.map { d ->
                if (seenInMeasure.add(d)) sAcc[d] else sBase[d]
            }
        }
    }

    /**
     * Generates both the exact scale degree indices (0..15) and the ABC body lines for any of the 10 ModalSchemes.
     */
    fun generateModalSchemeDegreesAndLines(
        tonic: Tonic,
        mode: ModeType,
        scheme: ModalScheme,
        articulation: ArticulationPattern
    ): Pair<List<Int>, List<String>> {
        val (sBase, sAcc) = getModalScaleNotesPair(tonic, mode)
        val degrees = mutableListOf<Int>()

        when (scheme) {
            ModalScheme.EJ1 -> {
                val lines = mutableListOf<String>()
                for (d in 0 until 8) {
                    val idxStd = listOf(d, d + 1, d + 2, d + 3, d + 4, d + 3, d + 2, d + 1)
                    val beatsIdx: List<List<Int>>
                    val barEnd: String
                    if (d < 7) {
                        beatsIdx = listOf(idxStd, idxStd, idxStd, idxStd)
                        barEnd = "|"
                    } else {
                        val idxTurn = listOf(d, d + 1, d + 2, d + 3, d + 4, d + 2, d + 1, d)
                        beatsIdx = listOf(idxStd, idxStd, idxStd, idxTurn)
                        barEnd = "| ${sAcc[7]}4 z4 z8 |]"
                    }
                    for (b in beatsIdx) degrees.addAll(b)
                    val beats = resolveMeasureGroups(beatsIdx, sBase, sAcc)
                    val artStr = beats.joinToString(" ") { articulation.apply16ths8(it) }
                    lines.add("$artStr $barEnd")
                }
                degrees.add(7)
                return Pair(degrees, lines)
            }

            ModalScheme.EJ2 -> {
                val degreesArch = listOf(0, 2, 4, 7, 10, 5, 3)
                val lines = mutableListOf<String>()
                for (d in degreesArch) {
                    val idxStd = listOf(d, d + 1, d + 2, d + 3, d + 4, d + 3, d + 2, d + 1)
                    val idxTurn = listOf(d, d + 1, d + 2, d + 3, d + 4, d + 2, d + 1, d)
                    val beatsIdx = listOf(idxStd, idxStd, idxStd, idxTurn)
                    for (b in beatsIdx) degrees.addAll(b)
                    val beats = resolveMeasureGroups(beatsIdx, sBase, sAcc)
                    val artStr = beats.joinToString(" ") { articulation.apply16ths8(it) }
                    lines.add("$artStr |")
                }
                val idxII = listOf(1, 2, 3, 4, 5, 4, 3, 2)
                val idxI = listOf(0, 1, 2, 3, 4, 3, 2, 1)
                val idxITurn = listOf(0, 1, 2, 3, 4, 2, 1, 0)
                val c8BeatsIdx = listOf(idxII, idxII, idxI, idxITurn)
                for (b in c8BeatsIdx) degrees.addAll(b)
                degrees.add(0)
                val c8Beats = resolveMeasureGroups(c8BeatsIdx, sBase, sAcc)
                val artC8 = c8Beats.joinToString(" ") { articulation.apply16ths8(it) }
                lines.add("$artC8 | ${sAcc[0]}4 z4 z8 |]")
                return Pair(degrees, lines)
            }

            ModalScheme.EJ4 -> {
                val groupsIdx = listOf(
                    Pair((0 until 8).toList(),  listOf(8, 7, 6, 5, 4, 3, 2, 1)),
                    Pair((2 until 10).toList(), listOf(10, 9, 8, 7, 6, 5, 4, 3)),
                    Pair((4 until 12).toList(), listOf(12, 11, 10, 9, 8, 7, 6, 5)),
                    Pair((6 until 14).toList(), listOf(14, 13, 12, 11, 10, 9, 8, 7)),
                    Pair((6 until 14).toList(), listOf(12, 11, 10, 9, 8, 7, 6, 5)),
                    Pair((4 until 12).toList(), listOf(10, 9, 8, 7, 6, 5, 4, 3)),
                    Pair((2 until 10).toList(), listOf(8, 7, 6, 5, 4, 3, 2, 1))
                )
                val bars = mutableListOf<String>()
                for ((gAsc, gDesc) in groupsIdx) {
                    degrees.addAll(gAsc)
                    degrees.addAll(gDesc)
                    val resolved = resolveMeasureGroups(listOf(gAsc, gDesc), sBase, sAcc)
                    bars.add("${articulation.apply(resolved[0])} ${articulation.apply(resolved[1])}")
                }
                val c8AscIdx = (0 until 8).toList()
                val c8DescIdx = listOf(6, 5, 4, 3, 2, 1, 0)
                degrees.addAll(c8AscIdx)
                degrees.addAll(c8DescIdx)
                val resolved8 = resolveMeasureGroups(listOf(c8AscIdx, c8DescIdx), sBase, sAcc)
                val n8Asc = resolved8[0]
                val n8Desc = resolved8[1]
                val c8Asc = articulation.apply(n8Asc)
                val c8Desc = if (articulation == ArticulationPattern.ALL_STACCATO) {
                    ".${n8Desc[0]}.${n8Desc[1]}.${n8Desc[2]}.${n8Desc[3]} .${n8Desc[4]}.${n8Desc[5]}.${n8Desc[6]}2"
                } else {
                    "(${n8Desc[0]}${n8Desc[1]}${n8Desc[2]}${n8Desc[3]}${n8Desc[4]}${n8Desc[5]} ${n8Desc[6]}2)"
                }
                bars.add("$c8Asc $c8Desc")
                return Pair(
                    degrees,
                    listOf(
                        "${bars[0]} | ${bars[1]} |",
                        "${bars[2]} | ${bars[3]} |",
                        "${bars[4]} | ${bars[5]} |",
                        "${bars[6]} | ${bars[7]} |]"
                    )
                )
            }

            ModalScheme.EJ5 -> {
                val measurePairs = listOf(
                    Pair(listOf(0, 1, 2, 3, 4, 5), listOf(6, 7, 8, 9, 10, 11)),
                    Pair(listOf(12, 13, 14, 13, 12, 11), listOf(10, 9, 8, 7, 6, 5)),
                    Pair(listOf(4, 5, 6, 7, 8, 9), listOf(10, 11, 12, 13, 14, 13)),
                    Pair(listOf(12, 11, 10, 9, 8, 7), listOf(6, 5, 4, 3, 2, 1))
                )
                val fmtBars = mutableListOf<String>()
                for ((g1, g2) in measurePairs) {
                    degrees.addAll(g1)
                    degrees.addAll(g2)
                    val res = resolveMeasureGroups(listOf(g1, g2), sBase, sAcc)
                    fmtBars.add("${articulation.apply16ths6(res[0])} ${articulation.apply16ths6(res[1])}")
                }
                degrees.add(0)
                return Pair(
                    degrees,
                    listOf(
                        "${fmtBars[0]} | ${fmtBars[1]} |",
                        "${fmtBars[2]} | ${fmtBars[3]} | ${sAcc[0]}4 z2 z6 |]"
                    )
                )
            }

            ModalScheme.EJ10, ModalScheme.EJ11 -> {
                val chordDegrees = listOf(
                    listOf(0, 2, 4, 7, 9, 11, 14),
                    listOf(1, 3, 5, 8, 10, 12, 15),
                    listOf(0, 2, 4, 6, 9, 11, 13),
                    listOf(0, 3, 5, 7, 10, 12, 14),
                    listOf(1, 4, 6, 8, 11, 13, 15),
                    listOf(0, 2, 5, 7, 9, 12, 14),
                    listOf(1, 3, 6, 8, 10, 13, 15),
                    listOf(0, 2, 4, 7, 9, 11, 14)
                )
                val bars = mutableListOf<String>()
                for (cd in chordDegrees) {
                    val d1 = cd[0]; val d2 = cd[1]; val d3 = cd[2]; val d4 = cd[3]
                    val d5 = cd[4]; val d6 = cd[5]; val d7 = cd[6]
                    if (scheme == ModalScheme.EJ10) {
                        val g1Idx = listOf(d1, d2, d3, d4, d5, d6)
                        val g2Idx = listOf(d7, d6, d5, d4, d3, d2)
                        degrees.addAll(g1Idx)
                        degrees.addAll(g2Idx)
                        val res = resolveMeasureGroups(listOf(g1Idx, g2Idx), sBase, sAcc)
                        bars.add("${articulation.apply16ths6(res[0])} ${articulation.apply16ths6(res[1])}")
                    } else {
                        val g1Idx = listOf(d1, d3, d2, d4, d3, d5)
                        val g2Idx = listOf(d4, d6, d5, d7, d5, d6)
                        val g3Idx = listOf(d4, d5, d3, d4, d2, d3)
                        degrees.addAll(g1Idx)
                        degrees.addAll(g2Idx)
                        degrees.addAll(g3Idx)
                        val res = resolveMeasureGroups(listOf(g1Idx, g2Idx, g3Idx), sBase, sAcc)
                        bars.add("${articulation.apply16ths6(res[0])} ${articulation.apply16ths6(res[1])} ${articulation.apply16ths6(res[2])}")
                    }
                }
                degrees.add(0)
                val closing = if (scheme == ModalScheme.EJ10) "${sAcc[0]}4 z2 z6 |]" else "${sAcc[0]}6 z3 z9 |]"
                return Pair(
                    degrees,
                    listOf(
                        "${bars[0]} | ${bars[1]} |",
                        "${bars[2]} | ${bars[3]} |",
                        "${bars[4]} | ${bars[5]} |",
                        "${bars[6]} | ${bars[7]} | $closing"
                    )
                )
            }

            ModalScheme.R1 -> {
                val m1G = listOf(listOf(7, 4, 5, 6, 7, 8), listOf(9, 7, 8, 9, 10, 11))
                val m2G = listOf(listOf(11, 9, 10, 11, 12, 13), listOf(14, 13, 12, 11, 10, 9))
                val m3G = listOf(listOf(12, 11, 10, 9, 8, 7), listOf(6, 5, 4, 3, 2, 1))
                val m4G = listOf(listOf(0, 2, 4, 7, 9, 11), listOf(14))
                for (mG in listOf(m1G, m2G, m3G, m4G)) {
                    for (g in mG) degrees.addAll(g)
                }
                val m1N = resolveMeasureGroups(m1G, sBase, sAcc)
                val m2N = resolveMeasureGroups(m2G, sBase, sAcc)
                val m3N = resolveMeasureGroups(m3G, sBase, sAcc)
                val m4N = resolveMeasureGroups(m4G, sBase, sAcc)
                return Pair(
                    degrees,
                    listOf(
                        "${articulation.apply16ths6(m1N[0])} ${articulation.apply16ths6(m1N[1])} | ${articulation.apply16ths6(m2N[0])} ${articulation.apply16ths6(m2N[1])} |",
                        "${articulation.apply16ths6(m3N[0])} ${articulation.apply16ths6(m3N[1])} | ${articulation.apply16ths6(m4N[0])} .${m4N[1][0]}2 z2 z2 |]"
                    )
                )
            }

            ModalScheme.R2 -> {
                val pickupIdx = listOf(0, 2, 4, 7)
                val measuresIdx = listOf(
                    listOf(6, 4, 3, 1, 3, 4, 6, 8),
                    listOf(7, 4, 2, 0, 2, 4, 7, 9),
                    listOf(8, 6, 4, 3, 4, 6, 8, 10),
                    listOf(9, 7, 4, 2, 4, 7, 9, 11),
                    listOf(10, 8, 6, 4, 6, 8, 10, 11),
                    listOf(11, 9, 7, 4, 7, 9, 11, 14),
                    listOf(8, 6, 4, 3, 1, 3, 4, 6)
                )
                degrees.addAll(pickupIdx)
                for (mIdx in measuresIdx) degrees.addAll(mIdx)
                degrees.add(7)
                val pkNotes = resolveMeasureGroups(listOf(pickupIdx), sBase, sAcc)[0]
                val pickup = articulation.apply16ths4(pkNotes)
                val mStrs = measuresIdx.map { mIdx ->
                    val notes = resolveMeasureGroups(listOf(mIdx), sBase, sAcc)[0]
                    articulation.apply(notes)
                }
                return Pair(
                    degrees,
                    listOf(
                        "$pickup | ${mStrs[0]} | ${mStrs[1]} | ${mStrs[2]} |",
                        "${mStrs[3]} | ${mStrs[4]} | ${mStrs[5]} | ${mStrs[6]} | .${sAcc[7]}2 z2 |]"
                    )
                )
            }

            ModalScheme.R4 -> {
                val barsIdx = listOf(
                    Pair(listOf(0, 2, 4, 5, 4, 3, 4, 2), listOf(2, 4, 7, 8, 7, 6, 7, 4)),
                    Pair(listOf(4, 7, 9, 10, 9, 8, 9, 7), listOf(7, 9, 11, 12, 11, 10, 11, 9)),
                    Pair(listOf(4, 7, 9, 10, 9, 8, 9, 7), listOf(2, 4, 7, 8, 7, 6, 7, 4))
                )
                val m4Hb1Idx = listOf(0, 2, 4, 7, 9, 11, 7, 9)
                val m4TailIdx = listOf(4, 7, 2, 4)
                val m4EndIdx = listOf(0)

                val barStrs = mutableListOf<String>()
                for ((hb1, hb2) in barsIdx) {
                    degrees.addAll(hb1)
                    degrees.addAll(hb2)
                    val res = resolveMeasureGroups(listOf(hb1, hb2), sBase, sAcc)
                    barStrs.add("${articulation.apply(res[0])} ${articulation.apply(res[1])}")
                }
                degrees.addAll(m4Hb1Idx)
                degrees.addAll(m4TailIdx)
                degrees.addAll(m4EndIdx)
                val res4 = resolveMeasureGroups(listOf(m4Hb1Idx, m4TailIdx, m4EndIdx), sBase, sAcc)
                val m4Str = "${articulation.apply(res4[0])} ${articulation.apply16ths4(res4[1])} .${res4[2][0]}2 z2 |]"
                return Pair(
                    degrees,
                    listOf(
                        "${barStrs[0]} | ${barStrs[1]} |",
                        "${barStrs[2]} | $m4Str"
                    )
                )
            }

            ModalScheme.R5 -> {
                val tripletPairsIdx = listOf(
                    Pair(listOf(7, 9, 11, 14, 9, 11), listOf(7, 9, 11, 4, 9, 11)),
                    Pair(listOf(8, 10, 11, 13, 10, 11), listOf(8, 10, 11, 4, 10, 11)),
                    Pair(listOf(6, 10, 11, 15, 10, 11), listOf(6, 10, 11, 4, 10, 11)),
                    Pair(listOf(7, 9, 11, 14, 9, 11), listOf(7, 9, 11, 4, 9, 11)),
                    Pair(listOf(7, 9, 12, 14, 9, 12), listOf(6, 9, 11, 15, 9, 11)),
                    Pair(listOf(5, 9, 12, 14, 9, 12), listOf(3, 8, 11, 15, 8, 11)),
                    Pair(listOf(4, 9, 11, 14, 9, 11), listOf(4, 10, 11, 13, 10, 11))
                )
                val m8Idx = listOf(7, 9, 11, 14, 9, 11)
                val m8EndIdx = listOf(7)
                val mStrs = mutableListOf<String>()
                for ((p1, p2) in tripletPairsIdx) {
                    degrees.addAll(p1)
                    degrees.addAll(p2)
                    val res = resolveMeasureGroups(listOf(p1, p2), sBase, sAcc)
                    mStrs.add("${articulation.applyTripletPair(res[0])} ${articulation.applyTripletPair(res[1])}")
                }
                degrees.addAll(m8Idx)
                degrees.addAll(m8EndIdx)
                val res8 = resolveMeasureGroups(listOf(m8Idx, m8EndIdx), sBase, sAcc)
                val m8Str = "${articulation.applyTripletPair(res8[0])} .${res8[1][0]}2 z2"
                return Pair(
                    degrees,
                    listOf(
                        "${mStrs[0]} | ${mStrs[1]} | ${mStrs[2]} | ${mStrs[3]} |",
                        "${mStrs[4]} | ${mStrs[5]} | ${mStrs[6]} | $m8Str |]"
                    )
                )
            }
        }
    }

    /**
     * Computes the exact MIDI note sequence for any of the 840 modal combinations (12 tonics x 7 modes x 10 schemes).
     */
    fun generateModalSchemeMidiNotes(
        tonic: Tonic,
        mode: ModeType,
        scheme: ModalScheme = ModalScheme.EJ4
    ): List<Int> {
        val (degrees, _) = generateModalSchemeDegreesAndLines(
            tonic = tonic,
            mode = mode,
            scheme = scheme,
            articulation = ArticulationPattern.ALL_SLURRED
        )
        val intervals = mode.intervals
        val rootMidi = tonic.rootMidi
        return degrees.map { deg ->
            val octave = deg / 7
            val step = deg % 7
            rootMidi + octave * 12 + intervals[step]
        }
    }

    fun generateABC(
        tonic: Tonic,
        mode: ModeType,
        articulation: ArticulationPattern,
        tempoBPM: Int = 90,
        loc: LocalizationManager,
        scheme: ModalScheme = ModalScheme.EJ4
    ): String {
        val keySig = mode.keySignature(tonic)
        val (_, bodyLines) = generateModalSchemeDegreesAndLines(
            tonic = tonic,
            mode = mode,
            scheme = scheme,
            articulation = articulation
        )
        val tempoHeader = when (scheme) {
            ModalScheme.EJ4 -> "Q:1/2=$tempoBPM"
            ModalScheme.EJ5, ModalScheme.EJ10, ModalScheme.EJ11, ModalScheme.R1 -> "Q:3/8=$tempoBPM"
            else -> "Q:1/4=$tempoBPM"
        }
        val headerLines = mutableListOf(
            "X:1",
            "T:Modo ${mode.id}: ${tonic.displayName} ${mode.getShortName(loc)} (${scheme.pillLabel})",
            "% ${mode.family.displayName} | ${mode.accidentalBadge(loc)} | Fórmula: ${mode.formula} | Esquema: ${scheme.code}",
            "%%barsperstaff ${scheme.barsPerStaff}",
            "M:${scheme.meter}",
            "L:${scheme.unitLen}",
            tempoHeader,
            "K:$keySig",
            "V:1 clef=treble",
            "%%score 1"
        )
        headerLines.addAll(bodyLines)
        return headerLines.joinToString("\n")
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
        EJ1Measure(2,  listOf(listOf("D","_E","=F","_G","_A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(3,  listOf(listOf("_E","F","_G","_A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(4,  listOf(listOf("^D","=E","^F","=G","=A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(5,  listOf(listOf("E","^F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(6,  listOf(listOf("E","=F","=G","_A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(7,  listOf(listOf("F","G","_A","_B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(8,  listOf(listOf("^E","^F","^G","=A","=B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(9,  listOf(listOf("^F","^G","A","B","^c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(10, listOf(listOf("^F","=G","=A","_B","=c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","A","G","F")), "", "|"),
        EJ1Measure(11, listOf(listOf("G","A","_B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A")), "", "|"),
        EJ1Measure(12, listOf(listOf("^^F","^G","^A","B","^c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","A","G","F")), "", "|"),
        EJ1Measure(13, listOf(listOf("^G","^A","B","^c","^d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A")), "", "|"),
        EJ1Measure(14, listOf(listOf("^G","=A","=B","=c","=d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","B","A","G")), "", "|"),
        EJ1Measure(15, listOf(listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B")), "", "|"),
        EJ1Measure(16, listOf(listOf("A","_B","=c","_d","_e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(17, listOf(listOf("_B","c","_d","_e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(18, listOf(listOf("^A","=B","^c","=d","=e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(19, listOf(listOf("B","^c","d","e","^f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(20, listOf(listOf("B","=c","=d","_e","=f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","d","c","B")), "", "|"),
        EJ1Measure(21, listOf(listOf("c","d","_e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d")), "", "|"),
        EJ1Measure(22, listOf(listOf("^B","^c","^d","=e","^f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","d","c","B")), "", "|"),
        EJ1Measure(23, listOf(listOf("^c","^d","e","^f","^g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d")), "", "|"),
        EJ1Measure(24, listOf(listOf("^c","=d","=e","=f","=g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","e","d","c")), "", ":|"),
        EJ1Measure(25, listOf(listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e")), "", "|"),
        EJ1Measure(26, listOf(listOf("d","_e","=f","_g","_a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(27, listOf(listOf("_e","f","_g","_a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(28, listOf(listOf("^d","=e","^f","=g","=a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(29, listOf(listOf("e","^f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(30, listOf(listOf("e","=f","=g","_a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","g","f","e")), "", "| f4 z4 z8 |]")
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
            "C:Paul Taffanel & Philippe Gaubert",
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
            "C:Paul Taffanel & Philippe Gaubert",
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
    val ej4SectionMidiNotes: List<IntArray> by lazy { listOf(
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
    ) }

    /**
     * Generates the marker ABC score for Taffanel & Gaubert E.J. 5
     * (Editions Alphonse Leduc, Plate A. L. 16.588, page 115)
     */
    fun generateEJ5ABC(
        articulation: EJ5Articulation,
        section: EJ5Section = EJ5Section.C_CHROM,
        tempoBPM: Int = 90
    ): String {
        return listOf(
            "X:1",
            "T:E. J. 5 — ${section.titleEs}",
            "C:Paul Taffanel & Philippe Gaubert",
            "% EJ5_LEDUC_ART:${articulation.id}:SEC:${section.id}",
            "M:6/8",
            "L:1/16",
            "Q:1/4=$tempoBPM",
            "K:C",
            "C12 |]"
        ).joinToString("\n")
    }

    val ej5SectionMidiNotes: List<IntArray> by lazy { listOf(
        intArrayOf(60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60),
        intArrayOf(61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61),
        intArrayOf(62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62),
        intArrayOf(63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63),
        intArrayOf(64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64),
        intArrayOf(65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65),
        intArrayOf(66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66),
        intArrayOf(67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67),
        intArrayOf(68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68),
        intArrayOf(69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69),
        intArrayOf(70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70),
        intArrayOf(71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71)
    ) }

    /**
     * Generates the marker ABC score for Taffanel & Gaubert E.J. 10
     * (Editions Alphonse Leduc, Plate A. L. 16.588, pages 120-121)
     */
    fun generateEJ10ABC(
        articulation: EJ5Articulation,
        section: EJ10Section = EJ10Section.C_ARP,
        tempoBPM: Int = 90
    ): String {
        return listOf(
            "X:1",
            "T:E. J. 10 — ${section.titleEs}",
            "C:Paul Taffanel & Philippe Gaubert",
            "% EJ10_LEDUC_ART:${articulation.id}:SEC:${section.id}",
            "M:6/8",
            "L:1/16",
            "Q:1/4=$tempoBPM",
            "K:C",
            "C12 |]"
        ).joinToString("\n")
    }

    val ej10SectionMidiNotes: List<IntArray> by lazy { listOf(
        intArrayOf(60, 63, 68, 72, 75, 80, 84, 80, 75, 72, 68, 63, 60, 63, 69, 72, 75, 81, 84, 81, 75, 72, 69, 63, 60, 63, 66, 72, 75, 78, 84, 78, 75, 72, 66, 63, 60, 64, 68, 72, 76, 80, 84, 80, 76, 72, 68, 64, 60, 64, 67, 72, 76, 79, 84, 79, 76, 72, 67, 64, 60, 65, 69, 72, 77, 81, 84, 81, 77, 72, 69, 65, 60, 63, 67, 72, 75, 79, 84, 79, 75, 72, 67, 63, 60, 66, 69, 72, 78, 81, 84, 81, 78, 72, 69, 66, 60, 65, 68, 72, 77, 80, 84, 80, 77, 72, 68, 65, 60, 64, 69, 72, 76, 81, 84, 81, 76, 72, 69, 64),
        intArrayOf(61, 64, 67, 73, 76, 79, 85, 79, 76, 73, 67, 64, 61, 64, 68, 73, 76, 80, 85, 80, 76, 73, 68, 64, 61, 64, 69, 73, 76, 81, 85, 81, 76, 73, 69, 64, 61, 65, 70, 73, 77, 82, 85, 82, 77, 73, 70, 65, 61, 66, 70, 73, 78, 82, 85, 82, 78, 73, 70, 66, 61, 64, 70, 73, 76, 82, 85, 82, 76, 73, 70, 64, 61, 65, 69, 73, 77, 81, 85, 81, 77, 73, 69, 65, 61, 67, 70, 73, 79, 82, 85, 82, 79, 73, 70, 67, 61, 66, 69, 73, 78, 81, 85, 81, 78, 73, 69, 66, 61, 65, 68, 73, 77, 80, 85, 80, 77, 73, 68, 65),
        intArrayOf(62, 65, 70, 74, 77, 82, 86, 82, 77, 74, 70, 65, 62, 65, 71, 74, 77, 83, 86, 83, 77, 74, 71, 65, 62, 67, 70, 74, 79, 82, 86, 82, 79, 74, 70, 67, 62, 66, 70, 74, 78, 82, 86, 82, 78, 74, 70, 66, 62, 66, 69, 74, 78, 81, 86, 81, 78, 74, 69, 66, 62, 67, 71, 74, 79, 83, 86, 83, 79, 74, 71, 67, 62, 65, 69, 74, 77, 81, 86, 81, 77, 74, 69, 65, 62, 68, 71, 74, 80, 83, 86, 83, 80, 74, 71, 68, 62, 65, 68, 74, 77, 80, 86, 80, 77, 74, 68, 65, 62, 66, 71, 74, 78, 83, 86, 83, 78, 74, 71, 66),
        intArrayOf(63, 66, 69, 75, 78, 81, 87, 81, 78, 75, 69, 66, 63, 66, 70, 75, 78, 82, 87, 82, 78, 75, 70, 66, 63, 66, 71, 75, 78, 83, 87, 83, 78, 75, 71, 66, 63, 67, 70, 75, 79, 82, 87, 82, 79, 75, 70, 67, 63, 67, 72, 75, 79, 84, 87, 84, 79, 75, 72, 67, 63, 68, 72, 75, 80, 84, 87, 84, 80, 75, 72, 68, 63, 66, 72, 75, 78, 84, 87, 84, 78, 75, 72, 66, 63, 69, 72, 75, 81, 84, 87, 84, 81, 75, 72, 69, 63, 68, 71, 75, 80, 83, 87, 83, 80, 75, 71, 68, 63, 67, 71, 75, 79, 83, 87, 83, 79, 75, 71, 67),
        intArrayOf(64, 67, 70, 76, 79, 82, 88, 82, 79, 76, 70, 67, 64, 67, 71, 76, 79, 83, 88, 83, 79, 76, 71, 67, 64, 67, 72, 76, 79, 84, 88, 84, 79, 76, 72, 67, 64, 68, 72, 76, 80, 84, 88, 84, 80, 76, 72, 68, 64, 68, 73, 76, 80, 85, 88, 85, 80, 76, 73, 68, 64, 69, 73, 76, 81, 85, 88, 85, 81, 76, 73, 69, 64, 67, 73, 76, 79, 85, 88, 85, 79, 76, 73, 67, 64, 70, 73, 76, 82, 85, 88, 85, 82, 76, 73, 70, 64, 69, 72, 76, 81, 84, 88, 84, 81, 76, 72, 69, 64, 68, 71, 76, 80, 83, 88, 83, 80, 76, 71, 68),
        intArrayOf(65, 68, 73, 77, 80, 85, 89, 85, 80, 77, 73, 68, 65, 68, 74, 77, 80, 86, 89, 86, 80, 77, 74, 68, 65, 68, 71, 77, 80, 83, 89, 83, 80, 77, 71, 68, 65, 69, 73, 77, 81, 85, 89, 85, 81, 77, 73, 69, 65, 69, 72, 77, 81, 84, 89, 84, 81, 77, 72, 69, 65, 70, 74, 77, 82, 86, 89, 86, 82, 77, 74, 70, 65, 68, 72, 77, 80, 84, 89, 84, 80, 77, 72, 68, 65, 71, 74, 77, 83, 86, 89, 86, 83, 77, 74, 71, 65, 70, 73, 77, 82, 85, 89, 85, 82, 77, 73, 70, 65, 69, 74, 77, 81, 86, 89, 86, 81, 77, 74, 69),
        intArrayOf(66, 69, 73, 78, 81, 85, 90, 85, 81, 78, 73, 69, 66, 70, 73, 78, 82, 85, 90, 85, 82, 78, 73, 70, 66, 69, 74, 78, 81, 86, 90, 86, 81, 78, 74, 69, 66, 70, 74, 78, 82, 86, 90, 86, 82, 78, 74, 70, 66, 70, 75, 78, 82, 87, 90, 87, 82, 78, 75, 70, 66, 71, 75, 78, 83, 87, 90, 87, 83, 78, 75, 71, 66, 69, 75, 78, 81, 87, 90, 87, 81, 78, 75, 69, 66, 71, 74, 78, 83, 86, 90, 86, 83, 78, 74, 71, 66, 69, 72, 78, 81, 84, 90, 84, 81, 78, 72, 69, 66, 72, 75, 78, 84, 87, 90, 87, 84, 78, 75, 72),
        intArrayOf(67, 70, 75, 79, 82, 87, 91, 87, 82, 79, 75, 70, 67, 70, 76, 79, 82, 88, 91, 88, 82, 79, 76, 70, 67, 70, 73, 79, 82, 85, 91, 85, 82, 79, 73, 70, 67, 71, 75, 79, 83, 87, 91, 87, 83, 79, 75, 71, 67, 71, 74, 79, 83, 86, 91, 86, 83, 79, 74, 71, 67, 72, 76, 79, 84, 88, 91, 88, 84, 79, 76, 72, 67, 70, 74, 79, 82, 86, 91, 86, 82, 79, 74, 70, 67, 73, 76, 79, 85, 88, 91, 88, 85, 79, 76, 73, 67, 72, 75, 79, 84, 87, 91, 87, 84, 79, 75, 72, 67, 71, 76, 79, 83, 88, 91, 88, 83, 79, 76, 71),
        intArrayOf(68, 71, 74, 80, 83, 86, 92, 86, 83, 80, 74, 71, 68, 72, 75, 80, 84, 87, 92, 87, 84, 80, 75, 72, 68, 71, 76, 80, 83, 88, 92, 88, 83, 80, 76, 71, 68, 72, 77, 80, 84, 89, 92, 89, 84, 80, 77, 72, 68, 73, 77, 80, 85, 89, 92, 89, 85, 80, 77, 73, 68, 71, 77, 80, 83, 89, 92, 89, 83, 80, 77, 71, 68, 73, 76, 80, 85, 88, 92, 88, 85, 80, 76, 73, 68, 74, 77, 80, 86, 89, 92, 89, 86, 80, 77, 74, 68, 71, 75, 80, 83, 87, 92, 87, 83, 80, 75, 71, 68, 72, 76, 80, 84, 88, 92, 88, 84, 80, 76, 72),
        intArrayOf(69, 72, 75, 81, 84, 87, 93, 87, 84, 81, 75, 72, 69, 72, 76, 81, 84, 88, 93, 88, 84, 81, 76, 72, 69, 72, 77, 81, 84, 89, 93, 89, 84, 81, 77, 72, 69, 73, 77, 81, 85, 89, 93, 89, 85, 81, 77, 73, 69, 73, 78, 81, 85, 90, 93, 90, 85, 81, 78, 73, 69, 74, 78, 81, 86, 90, 93, 90, 86, 81, 78, 74, 69, 72, 78, 81, 84, 90, 93, 90, 84, 81, 78, 72, 69, 75, 78, 81, 87, 90, 93, 90, 87, 81, 78, 75, 69, 74, 77, 81, 86, 89, 93, 89, 86, 81, 77, 74, 69, 73, 76, 81, 85, 88, 93, 88, 85, 81, 76, 73),
        intArrayOf(70, 73, 78, 82, 85, 90, 94, 90, 85, 82, 78, 73, 70, 73, 79, 82, 85, 91, 94, 91, 85, 82, 79, 73, 70, 73, 76, 82, 85, 88, 94, 88, 85, 82, 76, 73, 70, 74, 78, 82, 86, 90, 94, 90, 86, 82, 78, 74, 70, 74, 77, 82, 86, 89, 94, 89, 86, 82, 77, 74, 70, 75, 79, 82, 87, 91, 94, 91, 87, 82, 79, 75, 70, 73, 77, 82, 85, 89, 94, 89, 85, 82, 77, 73, 70, 76, 79, 82, 88, 91, 94, 91, 88, 82, 79, 76, 70, 75, 78, 82, 87, 90, 94, 90, 87, 82, 78, 75, 70, 74, 79, 82, 86, 91, 94, 91, 86, 82, 79, 74),
        intArrayOf(71, 74, 77, 83, 86, 89, 95, 89, 86, 83, 77, 74, 71, 74, 78, 83, 86, 90, 95, 90, 86, 83, 78, 74, 71, 74, 79, 83, 86, 91, 95, 91, 86, 83, 79, 74, 71, 75, 78, 83, 87, 90, 95, 90, 87, 83, 78, 75, 71, 75, 80, 83, 87, 92, 95, 92, 87, 83, 80, 75, 71, 76, 80, 83, 88, 92, 95, 92, 88, 83, 80, 76, 71, 74, 80, 83, 86, 92, 95, 92, 86, 83, 80, 74, 71, 77, 80, 83, 89, 92, 95, 92, 89, 83, 80, 77, 71, 76, 79, 83, 88, 91, 95, 91, 88, 83, 79, 76, 71, 75, 78, 83, 87, 90, 95, 90, 87, 83, 78, 75, 71)
    ) }

    /**
     * Generates the marker ABC score for Taffanel & Gaubert E.J. 11
     * (Editions Alphonse Leduc, Plate A. L. 16.588, pages 122-125)
     */
    fun generateEJ11ABC(
        articulation: EJ5Articulation,
        section: EJ10Section = EJ10Section.C_ARP,
        tempoBPM: Int = 90
    ): String {
        return listOf(
            "X:1",
            "T:E. J. 11 — ${section.titleEs}",
            "C:Paul Taffanel & Philippe Gaubert",
            "% EJ11_LEDUC_ART:${articulation.id}:SEC:${section.id}",
            "M:9/8",
            "L:1/16",
            "Q:1/4=$tempoBPM",
            "K:C",
            "C18 |]"
        ).joinToString("\n")
    }

    val ej11SectionMidiNotes: List<IntArray> by lazy { listOf(
        intArrayOf(60, 68, 63, 72, 68, 75, 72, 80, 75, 84, 75, 80, 72, 75, 68, 72, 63, 68, 60, 69, 63, 72, 69, 75, 72, 81, 75, 84, 75, 81, 72, 75, 69, 72, 63, 69, 60, 66, 63, 72, 66, 75, 72, 78, 75, 84, 75, 78, 72, 75, 66, 72, 63, 66, 60, 68, 64, 72, 68, 76, 72, 80, 76, 84, 76, 80, 72, 76, 68, 72, 64, 68, 60, 67, 64, 72, 67, 76, 72, 79, 76, 84, 76, 79, 72, 76, 67, 72, 64, 67, 60, 69, 65, 72, 69, 77, 72, 81, 77, 84, 77, 81, 72, 77, 69, 72, 65, 69, 60, 67, 63, 72, 67, 75, 72, 79, 75, 84, 75, 79, 72, 75, 67, 72, 63, 67, 60, 69, 66, 72, 69, 78, 72, 81, 78, 84, 78, 81, 72, 78, 69, 72, 66, 69, 60, 68, 65, 72, 68, 77, 72, 80, 77, 84, 77, 80, 72, 77, 68, 72, 65, 68, 60, 69, 64, 72, 69, 76, 72, 81, 76, 84, 76, 81, 72, 76, 69, 72, 64, 69),
        intArrayOf(61, 67, 64, 73, 67, 76, 73, 79, 76, 85, 76, 79, 73, 76, 67, 73, 64, 67, 61, 68, 64, 73, 68, 76, 73, 80, 76, 85, 76, 80, 73, 76, 68, 73, 64, 68, 61, 69, 64, 73, 69, 76, 73, 81, 76, 85, 76, 81, 73, 76, 69, 73, 64, 69, 61, 70, 65, 73, 70, 77, 73, 82, 77, 85, 77, 82, 73, 77, 70, 73, 65, 70, 61, 70, 66, 73, 70, 78, 73, 82, 78, 85, 78, 82, 73, 78, 70, 73, 66, 70, 61, 70, 64, 73, 70, 76, 73, 82, 76, 85, 76, 82, 73, 76, 70, 73, 64, 70, 61, 69, 65, 73, 69, 77, 73, 81, 77, 85, 77, 81, 73, 77, 69, 73, 65, 69, 61, 70, 67, 73, 70, 79, 73, 82, 79, 85, 79, 82, 73, 79, 70, 73, 67, 70, 61, 69, 66, 73, 69, 78, 73, 81, 78, 85, 78, 81, 73, 78, 69, 73, 66, 69, 61, 68, 65, 73, 68, 77, 73, 80, 77, 85, 77, 80, 73, 77, 68, 73, 65, 68),
        intArrayOf(62, 70, 65, 74, 70, 77, 74, 82, 77, 86, 77, 82, 74, 77, 70, 74, 65, 70, 62, 71, 65, 74, 71, 77, 74, 83, 77, 86, 77, 83, 74, 77, 71, 74, 65, 71, 62, 70, 67, 74, 70, 79, 74, 82, 79, 86, 79, 82, 74, 79, 70, 74, 67, 70, 62, 70, 66, 74, 70, 78, 74, 82, 78, 86, 78, 82, 74, 78, 70, 74, 66, 70, 62, 69, 66, 74, 69, 78, 74, 81, 78, 86, 78, 81, 74, 78, 69, 74, 66, 69, 62, 71, 67, 74, 71, 79, 74, 83, 79, 86, 79, 83, 74, 79, 71, 74, 67, 71, 62, 69, 65, 74, 69, 77, 74, 81, 77, 86, 77, 81, 74, 77, 69, 74, 65, 69, 62, 71, 68, 74, 71, 80, 74, 83, 80, 86, 80, 83, 74, 80, 71, 74, 68, 71, 62, 68, 65, 74, 68, 77, 74, 80, 77, 86, 77, 80, 74, 77, 68, 74, 65, 68, 62, 71, 66, 74, 71, 78, 74, 83, 78, 86, 78, 83, 74, 78, 71, 74, 66, 71),
        intArrayOf(63, 69, 66, 75, 69, 78, 75, 81, 78, 87, 78, 81, 75, 78, 69, 75, 66, 69, 63, 70, 66, 75, 70, 78, 75, 82, 78, 87, 78, 82, 75, 78, 70, 75, 66, 70, 63, 71, 66, 75, 71, 78, 75, 83, 78, 87, 78, 83, 75, 78, 71, 75, 66, 71, 63, 70, 67, 75, 70, 79, 75, 82, 79, 87, 79, 82, 75, 79, 70, 75, 67, 70, 63, 72, 67, 75, 72, 79, 75, 84, 79, 87, 79, 84, 75, 79, 72, 75, 67, 72, 63, 72, 68, 75, 72, 80, 75, 84, 80, 87, 80, 84, 75, 80, 72, 75, 68, 72, 63, 72, 66, 75, 72, 78, 75, 84, 78, 87, 78, 84, 75, 78, 72, 75, 66, 72, 63, 72, 69, 75, 72, 81, 75, 84, 81, 87, 81, 84, 75, 81, 72, 75, 69, 72, 63, 71, 68, 75, 71, 80, 75, 83, 80, 87, 80, 83, 75, 80, 71, 75, 68, 71, 63, 71, 67, 75, 71, 79, 75, 83, 79, 87, 79, 83, 75, 79, 71, 75, 67, 71),
        intArrayOf(64, 70, 67, 76, 70, 79, 76, 82, 79, 88, 79, 82, 76, 79, 70, 76, 67, 70, 64, 71, 67, 76, 71, 79, 76, 83, 79, 88, 79, 83, 76, 79, 71, 76, 67, 71, 64, 72, 67, 76, 72, 79, 76, 84, 79, 88, 79, 84, 76, 79, 72, 76, 67, 72, 64, 72, 68, 76, 72, 80, 76, 84, 80, 88, 80, 84, 76, 80, 72, 76, 68, 72, 64, 73, 68, 76, 73, 80, 76, 85, 80, 88, 80, 85, 76, 80, 73, 76, 68, 73, 64, 73, 69, 76, 73, 81, 76, 85, 81, 88, 81, 85, 76, 81, 73, 76, 69, 73, 64, 73, 67, 76, 73, 79, 76, 85, 79, 88, 79, 85, 76, 79, 73, 76, 67, 73, 64, 73, 70, 76, 73, 82, 76, 85, 82, 88, 82, 85, 76, 82, 73, 76, 70, 73, 64, 72, 69, 76, 72, 81, 76, 84, 81, 88, 81, 84, 76, 81, 72, 76, 69, 72, 64, 71, 68, 76, 71, 80, 76, 83, 80, 88, 80, 83, 76, 80, 71, 76, 68, 71),
        intArrayOf(65, 73, 68, 77, 73, 80, 77, 85, 80, 89, 80, 85, 77, 80, 73, 77, 68, 73, 65, 74, 68, 77, 74, 80, 77, 86, 80, 89, 80, 86, 77, 80, 74, 77, 68, 74, 65, 71, 68, 77, 71, 80, 77, 83, 80, 89, 80, 83, 77, 80, 71, 77, 68, 71, 65, 73, 69, 77, 73, 81, 77, 85, 81, 89, 81, 85, 77, 81, 73, 77, 69, 73, 65, 72, 69, 77, 72, 81, 77, 84, 81, 89, 81, 84, 77, 81, 72, 77, 69, 72, 65, 74, 70, 77, 74, 82, 77, 86, 82, 89, 82, 86, 77, 82, 74, 77, 70, 74, 65, 72, 68, 77, 72, 80, 77, 84, 80, 89, 80, 84, 77, 80, 72, 77, 68, 72, 65, 74, 71, 77, 74, 83, 77, 86, 83, 89, 83, 86, 77, 83, 74, 77, 71, 74, 65, 73, 70, 77, 73, 82, 77, 85, 82, 89, 82, 85, 77, 82, 73, 77, 70, 73, 65, 74, 69, 77, 74, 81, 77, 86, 81, 89, 81, 86, 77, 81, 74, 77, 69, 74),
        intArrayOf(66, 73, 69, 78, 73, 81, 78, 85, 81, 90, 81, 85, 78, 81, 73, 78, 69, 73, 66, 73, 70, 78, 73, 82, 78, 85, 82, 90, 82, 85, 78, 82, 73, 78, 70, 73, 66, 74, 69, 78, 74, 81, 78, 86, 81, 90, 81, 86, 78, 81, 74, 78, 69, 74, 66, 74, 70, 78, 74, 82, 78, 86, 82, 90, 82, 86, 78, 82, 74, 78, 70, 74, 66, 75, 70, 78, 75, 82, 78, 87, 82, 90, 82, 87, 78, 82, 75, 78, 70, 75, 66, 75, 71, 78, 75, 83, 78, 87, 83, 90, 83, 87, 78, 83, 75, 78, 71, 75, 66, 75, 69, 78, 75, 81, 78, 87, 81, 90, 81, 87, 78, 81, 75, 78, 69, 75, 66, 74, 71, 78, 74, 83, 78, 86, 83, 90, 83, 86, 78, 83, 74, 78, 71, 74, 66, 72, 69, 78, 72, 81, 78, 84, 81, 90, 81, 84, 78, 81, 72, 78, 69, 72, 66, 75, 72, 78, 75, 84, 78, 87, 84, 90, 84, 87, 78, 84, 75, 78, 72, 75),
        intArrayOf(67, 75, 70, 79, 75, 82, 79, 87, 82, 91, 82, 87, 79, 82, 75, 79, 70, 75, 67, 76, 70, 79, 76, 82, 79, 88, 82, 91, 82, 88, 79, 82, 76, 79, 70, 76, 67, 73, 70, 79, 73, 82, 79, 85, 82, 91, 82, 85, 79, 82, 73, 79, 70, 73, 67, 75, 71, 79, 75, 83, 79, 87, 83, 91, 83, 87, 79, 83, 75, 79, 71, 75, 67, 74, 71, 79, 74, 83, 79, 86, 83, 91, 83, 86, 79, 83, 74, 79, 71, 74, 67, 76, 72, 79, 76, 84, 79, 88, 84, 91, 84, 88, 79, 84, 76, 79, 72, 76, 67, 74, 70, 79, 74, 82, 79, 86, 82, 91, 82, 86, 79, 82, 74, 79, 70, 74, 67, 76, 73, 79, 76, 85, 79, 88, 85, 91, 85, 88, 79, 85, 76, 79, 73, 76, 67, 75, 72, 79, 75, 84, 79, 87, 84, 91, 84, 87, 79, 84, 75, 79, 72, 75, 67, 76, 71, 79, 76, 83, 79, 88, 83, 91, 83, 88, 79, 83, 76, 79, 71, 76),
        intArrayOf(68, 74, 71, 80, 74, 83, 80, 86, 83, 92, 83, 86, 80, 83, 74, 80, 71, 74, 68, 75, 72, 80, 75, 84, 80, 87, 84, 92, 84, 87, 80, 84, 75, 80, 72, 75, 68, 76, 71, 80, 76, 83, 80, 88, 83, 92, 83, 88, 80, 83, 76, 80, 71, 76, 68, 77, 72, 80, 77, 84, 80, 89, 84, 92, 84, 89, 80, 84, 77, 80, 72, 77, 68, 77, 73, 80, 77, 85, 80, 89, 85, 92, 85, 89, 80, 85, 77, 80, 73, 77, 68, 77, 71, 80, 77, 83, 80, 89, 83, 92, 83, 89, 80, 83, 77, 80, 71, 77, 68, 76, 73, 80, 76, 85, 80, 88, 85, 92, 85, 88, 80, 85, 76, 80, 73, 76, 68, 77, 74, 80, 77, 86, 80, 89, 86, 92, 86, 89, 80, 86, 77, 80, 74, 77, 68, 75, 71, 80, 75, 83, 80, 87, 83, 92, 83, 87, 80, 83, 75, 80, 71, 75, 68, 76, 72, 80, 76, 84, 80, 88, 84, 92, 84, 88, 80, 84, 76, 80, 72, 76),
        intArrayOf(69, 75, 72, 81, 75, 84, 81, 87, 84, 93, 84, 87, 81, 84, 75, 81, 72, 75, 69, 76, 72, 81, 76, 84, 81, 88, 84, 93, 84, 88, 81, 84, 76, 81, 72, 76, 69, 77, 72, 81, 77, 84, 81, 89, 84, 93, 84, 89, 81, 84, 77, 81, 72, 77, 69, 77, 73, 81, 77, 85, 81, 89, 85, 93, 85, 89, 81, 85, 77, 81, 73, 77, 69, 78, 73, 81, 78, 85, 81, 90, 85, 93, 85, 90, 81, 85, 78, 81, 73, 78, 69, 78, 74, 81, 78, 86, 81, 90, 86, 93, 86, 90, 81, 86, 78, 81, 74, 78, 69, 78, 72, 81, 78, 84, 81, 90, 84, 93, 84, 90, 81, 84, 78, 81, 72, 78, 69, 78, 75, 81, 78, 87, 81, 90, 87, 93, 87, 90, 81, 87, 78, 81, 75, 78, 69, 77, 74, 81, 77, 86, 81, 89, 86, 93, 86, 89, 81, 86, 77, 81, 74, 77, 69, 76, 73, 81, 76, 85, 81, 88, 85, 93, 85, 88, 81, 85, 76, 81, 73, 76),
        intArrayOf(70, 78, 73, 82, 78, 85, 82, 90, 85, 94, 85, 90, 82, 85, 78, 82, 73, 78, 70, 79, 73, 82, 79, 85, 82, 91, 85, 94, 85, 91, 82, 85, 79, 82, 73, 79, 70, 76, 73, 82, 76, 85, 82, 88, 85, 94, 85, 88, 82, 85, 76, 82, 73, 76, 70, 78, 74, 82, 78, 86, 82, 90, 86, 94, 86, 90, 82, 86, 78, 82, 74, 78, 70, 77, 74, 82, 77, 86, 82, 89, 86, 94, 86, 89, 82, 86, 77, 82, 74, 77, 70, 79, 75, 82, 79, 87, 82, 91, 87, 94, 87, 91, 82, 87, 79, 82, 75, 79, 70, 77, 73, 82, 77, 85, 82, 89, 85, 94, 85, 89, 82, 85, 77, 82, 73, 77, 70, 79, 76, 82, 79, 88, 82, 91, 88, 94, 88, 91, 82, 88, 79, 82, 76, 79, 70, 78, 75, 82, 78, 87, 82, 90, 87, 94, 87, 90, 82, 87, 78, 82, 75, 78, 70, 79, 74, 82, 79, 86, 82, 91, 86, 94, 86, 91, 82, 86, 79, 82, 74, 79),
        intArrayOf(71, 77, 74, 83, 77, 86, 83, 89, 86, 95, 86, 89, 83, 86, 77, 83, 74, 77, 71, 78, 74, 83, 78, 86, 83, 90, 86, 95, 86, 90, 83, 86, 78, 83, 74, 78, 71, 79, 74, 83, 79, 86, 83, 91, 86, 95, 86, 91, 83, 86, 79, 83, 74, 79, 71, 78, 75, 83, 78, 87, 83, 90, 87, 95, 87, 90, 83, 87, 78, 83, 75, 78, 71, 80, 75, 83, 80, 87, 83, 92, 87, 95, 87, 92, 83, 87, 80, 83, 75, 80, 71, 80, 76, 83, 80, 88, 83, 92, 88, 95, 88, 92, 83, 88, 80, 83, 76, 80, 71, 80, 74, 83, 80, 86, 83, 92, 86, 95, 86, 92, 83, 86, 80, 83, 74, 80, 71, 80, 77, 83, 80, 89, 83, 92, 89, 95, 89, 92, 83, 89, 80, 83, 77, 80, 71, 79, 76, 83, 79, 88, 83, 91, 88, 95, 88, 91, 83, 88, 79, 83, 76, 79, 71, 78, 75, 83, 78, 87, 83, 90, 87, 95, 87, 90, 83, 87, 78, 83, 75, 78, 71)
    ) }

    // Reichert Op. 5, Nº 1 (B. Schott's Söhne Plate 20623, pp. 2–3)
    fun generateR1ABC(
        articulation: EJ5Articulation,
        section: EJ4Section = EJ4Section.C_MAJOR,
        tempoBPM: Int = 92
    ): String {
        return listOf(
            "X:1",
            "T:Reichert Op. 5 Nº 1 — ${section.titleEs}",
            "C:Mathieu-André Reichert (Op. 5)",
            "% R1_SCHOTT_ART:${articulation.id}:SEC:${section.id}",
            "M:6/8",
            "L:1/16",
            "Q:1/4=$tempoBPM",
            "K:${section.keySig}",
            "C16 |]"
        ).joinToString("\n")
    }

    val r1SectionMidiNotes: List<IntArray> by lazy { listOf(
        intArrayOf(72, 67, 69, 71, 72, 74, 76, 72, 74, 76, 77, 79, 79, 76, 77, 79, 81, 83, 84, 83, 81, 79, 77, 76, 81, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 62, 60, 64, 67, 72, 76, 79, 84),
        intArrayOf(81, 76, 78, 80, 81, 83, 84, 81, 83, 84, 86, 88, 88, 84, 86, 88, 90, 92, 93, 91, 89, 88, 86, 84, 89, 88, 86, 84, 83, 81, 79, 77, 76, 74, 72, 71, 69, 72, 76, 81, 84, 88, 93),
        intArrayOf(77, 72, 74, 76, 77, 79, 81, 77, 79, 81, 82, 84, 84, 81, 82, 84, 86, 88, 89, 88, 86, 84, 82, 81, 86, 84, 82, 81, 79, 77, 76, 74, 72, 70, 69, 67, 65, 69, 72, 77, 81, 84, 89),
        intArrayOf(74, 69, 71, 73, 74, 76, 77, 74, 76, 77, 79, 81, 81, 77, 79, 81, 83, 85, 86, 84, 82, 81, 79, 77, 82, 81, 79, 77, 76, 74, 72, 70, 69, 67, 65, 64, 62, 65, 69, 74, 77, 81, 86),
        intArrayOf(82, 77, 79, 81, 82, 84, 86, 82, 84, 86, 87, 89, 89, 86, 87, 89, 91, 93, 94, 93, 91, 89, 87, 86, 91, 89, 87, 86, 84, 82, 81, 79, 77, 75, 74, 72, 70, 74, 77, 82, 86, 89, 94),
        intArrayOf(79, 74, 76, 78, 79, 81, 82, 79, 81, 82, 84, 86, 86, 82, 84, 86, 88, 90, 91, 89, 87, 86, 84, 82, 87, 86, 84, 82, 81, 79, 77, 75, 74, 72, 70, 69, 67, 70, 74, 79, 82, 86, 91),
        intArrayOf(75, 70, 72, 74, 75, 77, 79, 75, 77, 79, 80, 82, 82, 79, 80, 82, 84, 86, 87, 86, 84, 82, 80, 79, 84, 82, 80, 79, 77, 75, 74, 72, 70, 68, 67, 65, 63, 67, 70, 75, 79, 82, 87),
        intArrayOf(72, 67, 69, 71, 72, 74, 75, 72, 74, 75, 77, 79, 79, 75, 77, 79, 81, 83, 84, 82, 80, 79, 77, 75, 80, 79, 77, 75, 74, 72, 70, 68, 67, 65, 63, 62, 60, 63, 67, 72, 75, 79, 84),
        intArrayOf(80, 75, 77, 79, 80, 82, 84, 80, 82, 84, 85, 87, 87, 84, 85, 87, 89, 91, 92, 91, 89, 87, 85, 84, 89, 87, 85, 84, 82, 80, 79, 77, 75, 73, 72, 70, 68, 72, 75, 80, 84, 87, 92),
        intArrayOf(77, 72, 74, 76, 77, 79, 80, 77, 79, 80, 82, 84, 84, 80, 82, 84, 86, 88, 89, 87, 85, 84, 82, 80, 85, 84, 82, 80, 79, 77, 75, 73, 72, 70, 68, 67, 65, 68, 72, 77, 80, 84, 89),
        intArrayOf(73, 68, 70, 72, 73, 75, 77, 73, 75, 77, 78, 80, 80, 77, 78, 80, 82, 84, 85, 84, 82, 80, 78, 77, 82, 80, 78, 77, 75, 73, 72, 70, 68, 66, 65, 63, 61, 65, 68, 73, 77, 80, 85),
        intArrayOf(82, 77, 79, 81, 82, 84, 85, 82, 84, 85, 87, 89, 89, 85, 87, 89, 91, 93, 94, 92, 90, 89, 87, 85, 90, 89, 87, 85, 84, 82, 80, 78, 77, 75, 73, 72, 70, 73, 77, 82, 85, 89, 94),
        intArrayOf(78, 73, 75, 77, 78, 80, 82, 78, 80, 82, 83, 85, 85, 82, 83, 85, 87, 89, 90, 89, 87, 85, 83, 82, 87, 85, 83, 82, 80, 78, 77, 75, 73, 71, 70, 68, 66, 70, 73, 78, 82, 85, 90),
        intArrayOf(75, 70, 72, 74, 75, 77, 78, 75, 77, 78, 80, 82, 82, 78, 80, 82, 84, 86, 87, 85, 83, 82, 80, 78, 83, 82, 80, 78, 77, 75, 73, 71, 70, 68, 66, 65, 63, 66, 70, 75, 78, 82, 87),
        intArrayOf(83, 78, 80, 82, 83, 85, 87, 83, 85, 87, 88, 90, 90, 87, 88, 90, 92, 94, 95, 94, 92, 90, 88, 87, 92, 90, 88, 87, 85, 83, 82, 80, 78, 76, 75, 73, 71, 75, 78, 83, 87, 90, 95),
        intArrayOf(80, 75, 77, 79, 80, 82, 83, 80, 82, 83, 85, 87, 87, 83, 85, 87, 89, 91, 92, 90, 88, 87, 85, 83, 88, 87, 85, 83, 82, 80, 78, 76, 75, 73, 71, 70, 68, 71, 75, 80, 83, 87, 92),
        intArrayOf(76, 71, 73, 75, 76, 78, 80, 76, 78, 80, 81, 83, 83, 80, 81, 83, 85, 87, 88, 87, 85, 83, 81, 80, 85, 83, 81, 80, 78, 76, 75, 73, 71, 69, 68, 66, 64, 68, 71, 76, 80, 83, 88),
        intArrayOf(73, 68, 70, 72, 73, 75, 76, 73, 75, 76, 78, 80, 80, 76, 78, 80, 82, 84, 85, 83, 81, 80, 78, 76, 81, 80, 78, 76, 75, 73, 71, 69, 68, 66, 64, 63, 61, 64, 68, 73, 76, 80, 85),
        intArrayOf(81, 76, 78, 80, 81, 83, 85, 81, 83, 85, 86, 88, 88, 85, 86, 88, 90, 92, 93, 92, 90, 88, 86, 85, 90, 88, 86, 85, 83, 81, 80, 78, 76, 74, 73, 71, 69, 73, 76, 81, 85, 88, 93),
        intArrayOf(78, 73, 75, 77, 78, 80, 81, 78, 80, 81, 83, 85, 85, 81, 83, 85, 87, 89, 90, 88, 86, 85, 83, 81, 86, 85, 83, 81, 80, 78, 76, 74, 73, 71, 69, 68, 66, 69, 73, 78, 81, 85, 90),
        intArrayOf(74, 69, 71, 73, 74, 76, 78, 74, 76, 78, 79, 81, 81, 78, 79, 81, 83, 85, 86, 85, 83, 81, 79, 78, 83, 81, 79, 78, 76, 74, 73, 71, 69, 67, 66, 64, 62, 66, 69, 74, 78, 81, 86),
        intArrayOf(83, 78, 80, 82, 83, 85, 86, 83, 85, 86, 88, 90, 90, 86, 88, 90, 92, 94, 95, 93, 91, 90, 88, 86, 91, 90, 88, 86, 85, 83, 81, 79, 78, 76, 74, 73, 71, 74, 78, 83, 86, 90, 95),
        intArrayOf(79, 74, 76, 78, 79, 81, 83, 79, 81, 83, 84, 86, 86, 83, 84, 86, 88, 90, 91, 90, 88, 86, 84, 83, 88, 86, 84, 83, 81, 79, 78, 76, 74, 72, 71, 69, 67, 71, 74, 79, 83, 86, 91),
        intArrayOf(76, 71, 73, 75, 76, 78, 79, 76, 78, 79, 81, 83, 83, 79, 81, 83, 85, 87, 88, 86, 84, 83, 81, 79, 84, 83, 81, 79, 78, 76, 74, 72, 71, 69, 67, 66, 64, 67, 71, 76, 79, 83, 88),
        intArrayOf(72, 67, 69, 71, 72, 74, 76, 72, 74, 76, 77, 79, 79, 76, 77, 79, 81, 83, 84, 83, 81, 79, 77, 76, 81, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 62, 60, 64, 67, 72, 76, 79, 84)
    ) }

    // Reichert Op. 5, Nº 2 (B. Schott's Söhne Plate 20623, pp. 4–5)
    fun generateR2ABC(
        articulation: EJ4Articulation,
        section: EJ4Section = EJ4Section.C_MAJOR,
        tempoBPM: Int = 128
    ): String {
        return listOf(
            "X:1",
            "T:Reichert Op. 5 Nº 2 — ${section.titleEs}",
            "C:Mathieu-André Reichert (Op. 5)",
            "% R2_SCHOTT_ART:${articulation.id}:SEC:${section.id}",
            "M:2/4",
            "L:1/16",
            "Q:1/4=$tempoBPM",
            "K:${section.keySig}",
            "C16 |]"
        ).joinToString("\n")
    }

    val r2SectionMidiNotes: List<IntArray> by lazy { listOf(
        intArrayOf(72, 76, 79, 84, 83, 79, 77, 74, 77, 79, 83, 86, 84, 79, 76, 72, 76, 79, 84, 88, 86, 83, 79, 77, 79, 83, 86, 89, 88, 84, 79, 76, 79, 84, 88, 91, 89, 86, 83, 79, 83, 86, 89, 91, 91, 88, 84, 79, 84, 88, 91, 96, 86, 83, 79, 77, 74, 77, 79, 83, 84),
        intArrayOf(69, 72, 76, 81, 80, 76, 74, 71, 74, 76, 80, 83, 81, 76, 72, 69, 72, 76, 81, 84, 83, 80, 76, 74, 76, 80, 83, 86, 84, 81, 76, 72, 76, 81, 84, 88, 86, 83, 80, 76, 80, 83, 86, 88, 88, 84, 81, 76, 81, 84, 88, 93, 83, 80, 76, 74, 71, 74, 76, 80, 81),
        intArrayOf(65, 69, 72, 77, 76, 72, 70, 67, 70, 72, 76, 79, 77, 72, 69, 65, 69, 72, 77, 81, 79, 76, 72, 70, 72, 76, 79, 82, 81, 77, 72, 69, 72, 77, 81, 84, 82, 79, 76, 72, 76, 79, 82, 84, 84, 81, 77, 72, 77, 81, 84, 89, 79, 76, 72, 70, 67, 70, 72, 76, 77),
        intArrayOf(74, 77, 81, 86, 85, 81, 79, 76, 79, 81, 85, 88, 86, 81, 77, 74, 77, 81, 86, 89, 88, 85, 81, 79, 81, 85, 88, 91, 89, 86, 81, 77, 81, 86, 89, 93, 91, 88, 85, 81, 85, 88, 91, 93, 93, 89, 86, 81, 86, 89, 93, 98, 88, 85, 81, 79, 76, 79, 81, 85, 86),
        intArrayOf(70, 74, 77, 82, 81, 77, 75, 72, 75, 77, 81, 84, 82, 77, 74, 70, 74, 77, 82, 86, 84, 81, 77, 75, 77, 81, 84, 87, 86, 82, 77, 74, 77, 82, 86, 89, 87, 84, 81, 77, 81, 84, 87, 89, 89, 86, 82, 77, 82, 86, 89, 94, 84, 81, 77, 75, 72, 75, 77, 81, 82),
        intArrayOf(67, 70, 74, 79, 78, 74, 72, 69, 72, 74, 78, 81, 79, 74, 70, 67, 70, 74, 79, 82, 81, 78, 74, 72, 74, 78, 81, 84, 82, 79, 74, 70, 74, 79, 82, 86, 84, 81, 78, 74, 78, 81, 84, 86, 86, 82, 79, 74, 79, 82, 86, 91, 81, 78, 74, 72, 69, 72, 74, 78, 79),
        intArrayOf(63, 67, 70, 75, 74, 70, 68, 65, 68, 70, 74, 77, 75, 70, 67, 63, 67, 70, 75, 79, 77, 74, 70, 68, 70, 74, 77, 80, 79, 75, 70, 67, 70, 75, 79, 82, 80, 77, 74, 70, 74, 77, 80, 82, 82, 79, 75, 70, 75, 79, 82, 87, 77, 74, 70, 68, 65, 68, 70, 74, 75),
        intArrayOf(72, 75, 79, 84, 83, 79, 77, 74, 77, 79, 83, 86, 84, 79, 75, 72, 75, 79, 84, 87, 86, 83, 79, 77, 79, 83, 86, 89, 87, 84, 79, 75, 79, 84, 87, 91, 89, 86, 83, 79, 83, 86, 89, 91, 91, 87, 84, 79, 84, 87, 91, 96, 86, 83, 79, 77, 74, 77, 79, 83, 84),
        intArrayOf(68, 72, 75, 80, 79, 75, 73, 70, 73, 75, 79, 82, 80, 75, 72, 68, 72, 75, 80, 84, 82, 79, 75, 73, 75, 79, 82, 85, 84, 80, 75, 72, 75, 80, 84, 87, 85, 82, 79, 75, 79, 82, 85, 87, 87, 84, 80, 75, 80, 84, 87, 92, 82, 79, 75, 73, 70, 73, 75, 79, 80),
        intArrayOf(65, 68, 72, 77, 76, 72, 70, 67, 70, 72, 76, 79, 77, 72, 68, 65, 68, 72, 77, 80, 79, 76, 72, 70, 72, 76, 79, 82, 80, 77, 72, 68, 72, 77, 80, 84, 82, 79, 76, 72, 76, 79, 82, 84, 84, 80, 77, 72, 77, 80, 84, 89, 79, 76, 72, 70, 67, 70, 72, 76, 77),
        intArrayOf(73, 77, 80, 85, 84, 80, 78, 75, 78, 80, 84, 87, 85, 80, 77, 73, 77, 80, 85, 89, 87, 84, 80, 78, 80, 84, 87, 90, 89, 85, 80, 77, 80, 85, 89, 92, 90, 87, 84, 80, 84, 87, 90, 92, 92, 89, 85, 80, 85, 89, 92, 97, 87, 84, 80, 78, 75, 78, 80, 84, 85),
        intArrayOf(70, 73, 77, 82, 81, 77, 75, 72, 75, 77, 81, 84, 82, 77, 73, 70, 73, 77, 82, 85, 84, 81, 77, 75, 77, 81, 84, 87, 85, 82, 77, 73, 77, 82, 85, 89, 87, 84, 81, 77, 81, 84, 87, 89, 89, 85, 82, 77, 82, 85, 89, 94, 84, 81, 77, 75, 72, 75, 77, 81, 82),
        intArrayOf(66, 70, 73, 78, 77, 73, 71, 68, 71, 73, 77, 80, 78, 73, 70, 66, 70, 73, 78, 82, 80, 77, 73, 71, 73, 77, 80, 83, 82, 78, 73, 70, 73, 78, 82, 85, 83, 80, 77, 73, 77, 80, 83, 85, 85, 82, 78, 73, 78, 82, 85, 90, 80, 77, 73, 71, 68, 71, 73, 77, 78),
        intArrayOf(63, 66, 70, 75, 74, 70, 68, 65, 68, 70, 74, 77, 75, 70, 66, 63, 66, 70, 75, 78, 77, 74, 70, 68, 70, 74, 77, 80, 78, 75, 70, 66, 70, 75, 78, 82, 80, 77, 74, 70, 74, 77, 80, 82, 82, 78, 75, 70, 75, 78, 82, 87, 77, 74, 70, 68, 65, 68, 70, 74, 75),
        intArrayOf(71, 75, 78, 83, 82, 78, 76, 73, 76, 78, 82, 85, 83, 78, 75, 71, 75, 78, 83, 87, 85, 82, 78, 76, 78, 82, 85, 88, 87, 83, 78, 75, 78, 83, 87, 90, 88, 85, 82, 78, 82, 85, 88, 90, 90, 87, 83, 78, 83, 87, 90, 95, 85, 82, 78, 76, 73, 76, 78, 82, 83),
        intArrayOf(68, 71, 75, 80, 79, 75, 73, 70, 73, 75, 79, 82, 80, 75, 71, 68, 71, 75, 80, 83, 82, 79, 75, 73, 75, 79, 82, 85, 83, 80, 75, 71, 75, 80, 83, 87, 85, 82, 79, 75, 79, 82, 85, 87, 87, 83, 80, 75, 80, 83, 87, 92, 82, 79, 75, 73, 70, 73, 75, 79, 80),
        intArrayOf(64, 68, 71, 76, 75, 71, 69, 66, 69, 71, 75, 78, 76, 71, 68, 64, 68, 71, 76, 80, 78, 75, 71, 69, 71, 75, 78, 81, 80, 76, 71, 68, 71, 76, 80, 83, 81, 78, 75, 71, 75, 78, 81, 83, 83, 80, 76, 71, 76, 80, 83, 88, 78, 75, 71, 69, 66, 69, 71, 75, 76),
        intArrayOf(73, 76, 80, 85, 84, 80, 78, 75, 78, 80, 84, 87, 85, 80, 76, 73, 76, 80, 85, 88, 87, 84, 80, 78, 80, 84, 87, 90, 88, 85, 80, 76, 80, 85, 88, 92, 90, 87, 84, 80, 84, 87, 90, 92, 92, 88, 85, 80, 85, 88, 92, 97, 87, 84, 80, 78, 75, 78, 80, 84, 85),
        intArrayOf(69, 73, 76, 81, 80, 76, 74, 71, 74, 76, 80, 83, 81, 76, 73, 69, 73, 76, 81, 85, 83, 80, 76, 74, 76, 80, 83, 86, 85, 81, 76, 73, 76, 81, 85, 88, 86, 83, 80, 76, 80, 83, 86, 88, 88, 85, 81, 76, 81, 85, 88, 93, 83, 80, 76, 74, 71, 74, 76, 80, 81),
        intArrayOf(66, 69, 73, 78, 77, 73, 71, 68, 71, 73, 77, 80, 78, 73, 69, 66, 69, 73, 78, 81, 80, 77, 73, 71, 73, 77, 80, 83, 81, 78, 73, 69, 73, 78, 81, 85, 83, 80, 77, 73, 77, 80, 83, 85, 85, 81, 78, 73, 78, 81, 85, 90, 80, 77, 73, 71, 68, 71, 73, 77, 78),
        intArrayOf(62, 66, 69, 74, 73, 69, 67, 64, 67, 69, 73, 76, 74, 69, 66, 62, 66, 69, 74, 78, 76, 73, 69, 67, 69, 73, 76, 79, 78, 74, 69, 66, 69, 74, 78, 81, 79, 76, 73, 69, 73, 76, 79, 81, 81, 78, 74, 69, 74, 78, 81, 86, 76, 73, 69, 67, 64, 67, 69, 73, 74),
        intArrayOf(71, 74, 78, 83, 82, 78, 76, 73, 76, 78, 82, 85, 83, 78, 74, 71, 74, 78, 83, 86, 85, 82, 78, 76, 78, 82, 85, 88, 86, 83, 78, 74, 78, 83, 86, 90, 88, 85, 82, 78, 82, 85, 88, 90, 90, 86, 83, 78, 83, 86, 90, 95, 85, 82, 78, 76, 73, 76, 78, 82, 83),
        intArrayOf(67, 71, 74, 79, 78, 74, 72, 69, 72, 74, 78, 81, 79, 74, 71, 67, 71, 74, 79, 83, 81, 78, 74, 72, 74, 78, 81, 84, 83, 79, 74, 71, 74, 79, 83, 86, 84, 81, 78, 74, 78, 81, 84, 86, 86, 83, 79, 74, 79, 83, 86, 91, 81, 78, 74, 72, 69, 72, 74, 78, 79),
        intArrayOf(64, 67, 71, 76, 75, 71, 69, 66, 69, 71, 75, 78, 76, 71, 67, 64, 67, 71, 76, 79, 78, 75, 71, 69, 71, 75, 78, 81, 79, 76, 71, 67, 71, 76, 79, 83, 81, 78, 75, 71, 75, 78, 81, 83, 83, 79, 76, 71, 76, 79, 83, 88, 78, 75, 71, 69, 66, 69, 71, 75, 76),
        intArrayOf(72, 76, 79, 84, 83, 79, 77, 74, 77, 79, 83, 86, 84, 79, 76, 72, 76, 79, 84, 88, 86, 83, 79, 77, 79, 83, 86, 89, 88, 84, 79, 76, 79, 84, 88, 91, 89, 86, 83, 79, 83, 86, 89, 91, 91, 88, 84, 79, 84, 88, 91, 96, 86, 83, 79, 77, 74, 77, 79, 83, 84)
    ) }

    // Reichert Op. 5, Nº 4 (B. Schott's Söhne Plate 20623, pp. 8–9)
    fun generateR4ABC(
        articulation: EJ4Articulation,
        section: EJ4Section = EJ4Section.C_MAJOR,
        tempoBPM: Int = 120
    ): String {
        return listOf(
            "X:1",
            "T:Reichert Op. 5 Nº 4 — ${section.titleEs}",
            "C:Mathieu-André Reichert (Op. 5)",
            "% R4_SCHOTT_ART:${articulation.id}:SEC:${section.id}",
            "M:C",
            "L:1/16",
            "Q:1/4=$tempoBPM",
            "K:${section.keySig}",
            "C16 |]"
        ).joinToString("\n")
    }

    val r4SectionMidiNotes: List<IntArray> by lazy { listOf(
        intArrayOf(60, 64, 67, 69, 67, 66, 67, 64, 64, 67, 72, 74, 72, 71, 72, 67, 67, 72, 76, 77, 76, 75, 76, 72, 72, 76, 79, 81, 79, 78, 79, 76, 67, 72, 76, 77, 76, 75, 76, 72, 64, 67, 72, 74, 72, 71, 72, 67, 60, 64, 67, 72, 76, 79, 72, 76, 67, 72, 64, 67, 60),
        intArrayOf(69, 72, 76, 77, 76, 75, 76, 72, 72, 76, 81, 83, 81, 80, 81, 76, 76, 81, 84, 86, 84, 83, 84, 81, 81, 84, 88, 89, 88, 87, 88, 84, 76, 81, 84, 86, 84, 83, 84, 81, 72, 76, 81, 83, 81, 80, 81, 76, 69, 72, 76, 81, 84, 88, 81, 84, 76, 81, 72, 76, 69),
        intArrayOf(65, 69, 72, 74, 72, 71, 72, 69, 69, 72, 77, 79, 77, 76, 77, 72, 72, 77, 81, 82, 81, 80, 81, 77, 77, 81, 84, 86, 84, 83, 84, 81, 72, 77, 81, 82, 81, 80, 81, 77, 69, 72, 77, 79, 77, 76, 77, 72, 65, 69, 72, 77, 81, 84, 77, 81, 72, 77, 69, 72, 65),
        intArrayOf(62, 65, 69, 70, 69, 68, 69, 65, 65, 69, 74, 76, 74, 73, 74, 69, 69, 74, 77, 79, 77, 76, 77, 74, 74, 77, 81, 82, 81, 80, 81, 77, 69, 74, 77, 79, 77, 76, 77, 74, 65, 69, 74, 76, 74, 73, 74, 69, 62, 65, 69, 74, 77, 81, 74, 77, 69, 74, 65, 69, 62),
        intArrayOf(70, 74, 77, 79, 77, 76, 77, 74, 74, 77, 82, 84, 82, 81, 82, 77, 77, 82, 86, 87, 86, 85, 86, 82, 82, 86, 89, 91, 89, 88, 89, 86, 77, 82, 86, 87, 86, 85, 86, 82, 74, 77, 82, 84, 82, 81, 82, 77, 70, 74, 77, 82, 86, 89, 82, 86, 77, 82, 74, 77, 70),
        intArrayOf(67, 70, 74, 75, 74, 73, 74, 70, 70, 74, 79, 81, 79, 78, 79, 74, 74, 79, 82, 84, 82, 81, 82, 79, 79, 82, 86, 87, 86, 85, 86, 82, 74, 79, 82, 84, 82, 81, 82, 79, 70, 74, 79, 81, 79, 78, 79, 74, 67, 70, 74, 79, 82, 86, 79, 82, 74, 79, 70, 74, 67),
        intArrayOf(63, 67, 70, 72, 70, 69, 70, 67, 67, 70, 75, 77, 75, 74, 75, 70, 70, 75, 79, 80, 79, 78, 79, 75, 75, 79, 82, 84, 82, 81, 82, 79, 70, 75, 79, 80, 79, 78, 79, 75, 67, 70, 75, 77, 75, 74, 75, 70, 63, 67, 70, 75, 79, 82, 75, 79, 70, 75, 67, 70, 63),
        intArrayOf(72, 75, 79, 80, 79, 78, 79, 75, 75, 79, 84, 86, 84, 83, 84, 79, 79, 84, 87, 89, 87, 86, 87, 84, 84, 87, 91, 92, 91, 90, 91, 87, 79, 84, 87, 89, 87, 86, 87, 84, 75, 79, 84, 86, 84, 83, 84, 79, 72, 75, 79, 84, 87, 91, 84, 87, 79, 84, 75, 79, 72),
        intArrayOf(68, 72, 75, 77, 75, 74, 75, 72, 72, 75, 80, 82, 80, 79, 80, 75, 75, 80, 84, 85, 84, 83, 84, 80, 80, 84, 87, 89, 87, 86, 87, 84, 75, 80, 84, 85, 84, 83, 84, 80, 72, 75, 80, 82, 80, 79, 80, 75, 68, 72, 75, 80, 84, 87, 80, 84, 75, 80, 72, 75, 68),
        intArrayOf(65, 68, 72, 73, 72, 71, 72, 68, 68, 72, 77, 79, 77, 76, 77, 72, 72, 77, 80, 82, 80, 79, 80, 77, 77, 80, 84, 85, 84, 83, 84, 80, 72, 77, 80, 82, 80, 79, 80, 77, 68, 72, 77, 79, 77, 76, 77, 72, 65, 68, 72, 77, 80, 84, 77, 80, 72, 77, 68, 72, 65),
        intArrayOf(73, 77, 80, 82, 80, 79, 80, 77, 77, 80, 85, 87, 85, 84, 85, 80, 80, 85, 89, 90, 89, 88, 89, 85, 85, 89, 92, 94, 92, 91, 92, 89, 80, 85, 89, 90, 89, 88, 89, 85, 77, 80, 85, 87, 85, 84, 85, 80, 73, 77, 80, 85, 89, 92, 85, 89, 80, 85, 77, 80, 73),
        intArrayOf(70, 73, 77, 78, 77, 76, 77, 73, 73, 77, 82, 84, 82, 81, 82, 77, 77, 82, 85, 87, 85, 84, 85, 82, 82, 85, 89, 90, 89, 88, 89, 85, 77, 82, 85, 87, 85, 84, 85, 82, 73, 77, 82, 84, 82, 81, 82, 77, 70, 73, 77, 82, 85, 89, 82, 85, 77, 82, 73, 77, 70),
        intArrayOf(66, 70, 73, 75, 73, 72, 73, 70, 70, 73, 78, 80, 78, 77, 78, 73, 73, 78, 82, 83, 82, 81, 82, 78, 78, 82, 85, 87, 85, 84, 85, 82, 73, 78, 82, 83, 82, 81, 82, 78, 70, 73, 78, 80, 78, 77, 78, 73, 66, 70, 73, 78, 82, 85, 78, 82, 73, 78, 70, 73, 66),
        intArrayOf(63, 66, 70, 71, 70, 69, 70, 66, 66, 70, 75, 77, 75, 74, 75, 70, 70, 75, 78, 80, 78, 77, 78, 75, 75, 78, 82, 83, 82, 81, 82, 78, 70, 75, 78, 80, 78, 77, 78, 75, 66, 70, 75, 77, 75, 74, 75, 70, 63, 66, 70, 75, 78, 82, 75, 78, 70, 75, 66, 70, 63),
        intArrayOf(71, 75, 78, 80, 78, 77, 78, 75, 75, 78, 83, 85, 83, 82, 83, 78, 78, 83, 87, 88, 87, 86, 87, 83, 83, 87, 90, 92, 90, 89, 90, 87, 78, 83, 87, 88, 87, 86, 87, 83, 75, 78, 83, 85, 83, 82, 83, 78, 71, 75, 78, 83, 87, 90, 83, 87, 78, 83, 75, 78, 71),
        intArrayOf(68, 71, 75, 76, 75, 74, 75, 71, 71, 75, 80, 82, 80, 79, 80, 75, 75, 80, 83, 85, 83, 82, 83, 80, 80, 83, 87, 88, 87, 86, 87, 83, 75, 80, 83, 85, 83, 82, 83, 80, 71, 75, 80, 82, 80, 79, 80, 75, 68, 71, 75, 80, 83, 87, 80, 83, 75, 80, 71, 75, 68),
        intArrayOf(64, 68, 71, 73, 71, 70, 71, 68, 68, 71, 76, 78, 76, 75, 76, 71, 71, 76, 80, 81, 80, 79, 80, 76, 76, 80, 83, 85, 83, 82, 83, 80, 71, 76, 80, 81, 80, 79, 80, 76, 68, 71, 76, 78, 76, 75, 76, 71, 64, 68, 71, 76, 80, 83, 76, 80, 71, 76, 68, 71, 64),
        intArrayOf(73, 76, 80, 81, 80, 79, 80, 76, 76, 80, 85, 87, 85, 84, 85, 80, 80, 85, 88, 90, 88, 87, 88, 85, 85, 88, 92, 93, 92, 91, 92, 88, 80, 85, 88, 90, 88, 87, 88, 85, 76, 80, 85, 87, 85, 84, 85, 80, 73, 76, 80, 85, 88, 92, 85, 88, 80, 85, 76, 80, 73),
        intArrayOf(69, 73, 76, 78, 76, 75, 76, 73, 73, 76, 81, 83, 81, 80, 81, 76, 76, 81, 85, 86, 85, 84, 85, 81, 81, 85, 88, 90, 88, 87, 88, 85, 76, 81, 85, 86, 85, 84, 85, 81, 73, 76, 81, 83, 81, 80, 81, 76, 69, 73, 76, 81, 85, 88, 81, 85, 76, 81, 73, 76, 69),
        intArrayOf(66, 69, 73, 74, 73, 72, 73, 69, 69, 73, 78, 80, 78, 77, 78, 73, 73, 78, 81, 83, 81, 80, 81, 78, 78, 81, 85, 86, 85, 84, 85, 81, 73, 78, 81, 83, 81, 80, 81, 78, 69, 73, 78, 80, 78, 77, 78, 73, 66, 69, 73, 78, 81, 85, 78, 81, 73, 78, 69, 73, 66),
        intArrayOf(62, 66, 69, 71, 69, 68, 69, 66, 66, 69, 74, 76, 74, 73, 74, 69, 69, 74, 78, 79, 78, 77, 78, 74, 74, 78, 81, 83, 81, 80, 81, 78, 69, 74, 78, 79, 78, 77, 78, 74, 66, 69, 74, 76, 74, 73, 74, 69, 62, 66, 69, 74, 78, 81, 74, 78, 69, 74, 66, 69, 62),
        intArrayOf(71, 74, 78, 79, 78, 77, 78, 74, 74, 78, 83, 85, 83, 82, 83, 78, 78, 83, 86, 88, 86, 85, 86, 83, 83, 86, 90, 91, 90, 89, 90, 86, 78, 83, 86, 88, 86, 85, 86, 83, 74, 78, 83, 85, 83, 82, 83, 78, 71, 74, 78, 83, 86, 90, 83, 86, 78, 83, 74, 78, 71),
        intArrayOf(67, 71, 74, 76, 74, 73, 74, 71, 71, 74, 79, 81, 79, 78, 79, 74, 74, 79, 83, 84, 83, 82, 83, 79, 79, 83, 86, 88, 86, 85, 86, 83, 74, 79, 83, 84, 83, 82, 83, 79, 71, 74, 79, 81, 79, 78, 79, 74, 67, 71, 74, 79, 83, 86, 79, 83, 74, 79, 71, 74, 67),
        intArrayOf(64, 67, 71, 72, 71, 70, 71, 67, 67, 71, 76, 78, 76, 75, 76, 71, 71, 76, 79, 81, 79, 78, 79, 76, 76, 79, 83, 84, 83, 82, 83, 79, 71, 76, 79, 81, 79, 78, 79, 76, 67, 71, 76, 78, 76, 75, 76, 71, 64, 67, 71, 76, 79, 83, 76, 79, 71, 76, 67, 71, 64),
        intArrayOf(60, 64, 67, 69, 67, 66, 67, 64, 64, 67, 72, 74, 72, 71, 72, 67, 67, 72, 76, 77, 76, 75, 76, 72, 72, 76, 79, 81, 79, 78, 79, 76, 67, 72, 76, 77, 76, 75, 76, 72, 64, 67, 72, 74, 72, 71, 72, 67, 60, 64, 67, 72, 76, 79, 72, 76, 67, 72, 64, 67, 60)
    ) }

    // Reichert Op. 5, Nº 5 (B. Schott's Söhne Plate 20623, pp. 10–13)
    fun generateR5ABC(
        articulation: EJ5Articulation,
        section: EJ4Section = EJ4Section.C_MAJOR,
        tempoBPM: Int = 80
    ): String {
        return listOf(
            "X:1",
            "T:Reichert Op. 5 Nº 5 — ${section.titleEs}",
            "C:Mathieu-André Reichert (Op. 5)",
            "% R5_SCHOTT_ART:${articulation.id}:SEC:${section.id}",
            "M:2/4",
            "L:1/16",
            "Q:1/4=$tempoBPM",
            "K:${section.keySig}",
            "C16 |]"
        ).joinToString("\n")
    }

    val r5SectionMidiNotes: List<IntArray> by lazy { listOf(
        intArrayOf(72, 76, 79, 84, 76, 79, 72, 76, 79, 67, 76, 79, 74, 77, 79, 83, 77, 79, 74, 77, 79, 67, 77, 79, 71, 77, 79, 86, 77, 79, 71, 77, 79, 67, 77, 79, 72, 76, 79, 84, 76, 79, 72, 76, 79, 67, 76, 79, 72, 76, 79, 88, 76, 79, 71, 76, 80, 86, 76, 80, 69, 76, 81, 84, 76, 81, 65, 74, 80, 86, 74, 80, 67, 76, 79, 84, 76, 79, 67, 77, 79, 83, 77, 79, 72, 76, 79, 84, 76, 79, 72),
        intArrayOf(69, 72, 76, 81, 72, 76, 69, 72, 76, 64, 72, 76, 71, 74, 76, 80, 74, 76, 71, 74, 76, 64, 74, 76, 68, 74, 76, 83, 74, 76, 68, 74, 76, 64, 74, 76, 69, 72, 76, 81, 72, 76, 69, 72, 76, 64, 72, 76, 69, 72, 76, 84, 72, 76, 67, 73, 76, 82, 73, 76, 65, 74, 77, 81, 74, 77, 62, 74, 77, 83, 74, 77, 64, 72, 76, 81, 72, 76, 64, 74, 76, 80, 74, 76, 69, 72, 76, 81, 72, 76, 69),
        intArrayOf(77, 81, 84, 89, 81, 84, 77, 81, 84, 72, 81, 84, 79, 82, 84, 88, 82, 84, 79, 82, 84, 72, 82, 84, 76, 82, 84, 91, 82, 84, 76, 82, 84, 72, 82, 84, 77, 81, 84, 89, 81, 84, 77, 81, 84, 72, 81, 84, 77, 81, 84, 93, 81, 84, 76, 81, 85, 91, 81, 85, 74, 81, 86, 89, 81, 86, 70, 79, 85, 91, 79, 85, 72, 81, 84, 89, 81, 84, 72, 82, 84, 88, 82, 84, 77, 81, 84, 89, 81, 84, 77),
        intArrayOf(74, 77, 81, 86, 77, 81, 74, 77, 81, 69, 77, 81, 76, 79, 81, 85, 79, 81, 76, 79, 81, 69, 79, 81, 73, 79, 81, 88, 79, 81, 73, 79, 81, 69, 79, 81, 74, 77, 81, 86, 77, 81, 74, 77, 81, 69, 77, 81, 74, 77, 81, 89, 77, 81, 72, 78, 81, 87, 78, 81, 70, 79, 82, 86, 79, 82, 67, 79, 82, 88, 79, 82, 69, 77, 81, 86, 77, 81, 69, 79, 81, 85, 79, 81, 74, 77, 81, 86, 77, 81, 74),
        intArrayOf(70, 74, 77, 82, 74, 77, 70, 74, 77, 65, 74, 77, 72, 75, 77, 81, 75, 77, 72, 75, 77, 65, 75, 77, 69, 75, 77, 84, 75, 77, 69, 75, 77, 65, 75, 77, 70, 74, 77, 82, 74, 77, 70, 74, 77, 65, 74, 77, 70, 74, 77, 86, 74, 77, 69, 74, 78, 84, 74, 78, 67, 74, 79, 82, 74, 79, 63, 72, 78, 84, 72, 78, 65, 74, 77, 82, 74, 77, 65, 75, 77, 81, 75, 77, 70, 74, 77, 82, 74, 77, 70),
        intArrayOf(67, 70, 74, 79, 70, 74, 67, 70, 74, 62, 70, 74, 69, 72, 74, 78, 72, 74, 69, 72, 74, 62, 72, 74, 66, 72, 74, 81, 72, 74, 66, 72, 74, 62, 72, 74, 67, 70, 74, 79, 70, 74, 67, 70, 74, 62, 70, 74, 67, 70, 74, 82, 70, 74, 65, 71, 74, 80, 71, 74, 63, 72, 75, 79, 72, 75, 60, 72, 75, 81, 72, 75, 62, 70, 74, 79, 70, 74, 62, 72, 74, 78, 72, 74, 67, 70, 74, 79, 70, 74, 67),
        intArrayOf(75, 79, 82, 87, 79, 82, 75, 79, 82, 70, 79, 82, 77, 80, 82, 86, 80, 82, 77, 80, 82, 70, 80, 82, 74, 80, 82, 89, 80, 82, 74, 80, 82, 70, 80, 82, 75, 79, 82, 87, 79, 82, 75, 79, 82, 70, 79, 82, 75, 79, 82, 91, 79, 82, 74, 79, 83, 89, 79, 83, 72, 79, 84, 87, 79, 84, 68, 77, 83, 89, 77, 83, 70, 79, 82, 87, 79, 82, 70, 80, 82, 86, 80, 82, 75, 79, 82, 87, 79, 82, 75),
        intArrayOf(72, 75, 79, 84, 75, 79, 72, 75, 79, 67, 75, 79, 74, 77, 79, 83, 77, 79, 74, 77, 79, 67, 77, 79, 71, 77, 79, 86, 77, 79, 71, 77, 79, 67, 77, 79, 72, 75, 79, 84, 75, 79, 72, 75, 79, 67, 75, 79, 72, 75, 79, 87, 75, 79, 70, 76, 79, 85, 76, 79, 68, 77, 80, 84, 77, 80, 65, 77, 80, 86, 77, 80, 67, 75, 79, 84, 75, 79, 67, 77, 79, 83, 77, 79, 72, 75, 79, 84, 75, 79, 72),
        intArrayOf(68, 72, 75, 80, 72, 75, 68, 72, 75, 63, 72, 75, 70, 73, 75, 79, 73, 75, 70, 73, 75, 63, 73, 75, 67, 73, 75, 82, 73, 75, 67, 73, 75, 63, 73, 75, 68, 72, 75, 80, 72, 75, 68, 72, 75, 63, 72, 75, 68, 72, 75, 84, 72, 75, 67, 72, 76, 82, 72, 76, 65, 72, 77, 80, 72, 77, 61, 70, 76, 82, 70, 76, 63, 72, 75, 80, 72, 75, 63, 73, 75, 79, 73, 75, 68, 72, 75, 80, 72, 75, 68),
        intArrayOf(77, 80, 84, 89, 80, 84, 77, 80, 84, 72, 80, 84, 79, 82, 84, 88, 82, 84, 79, 82, 84, 72, 82, 84, 76, 82, 84, 91, 82, 84, 76, 82, 84, 72, 82, 84, 77, 80, 84, 89, 80, 84, 77, 80, 84, 72, 80, 84, 77, 80, 84, 92, 80, 84, 75, 81, 84, 90, 81, 84, 73, 82, 85, 89, 82, 85, 70, 82, 85, 91, 82, 85, 72, 80, 84, 89, 80, 84, 72, 82, 84, 88, 82, 84, 77, 80, 84, 89, 80, 84, 77),
        intArrayOf(73, 77, 80, 85, 77, 80, 73, 77, 80, 68, 77, 80, 75, 78, 80, 84, 78, 80, 75, 78, 80, 68, 78, 80, 72, 78, 80, 87, 78, 80, 72, 78, 80, 68, 78, 80, 73, 77, 80, 85, 77, 80, 73, 77, 80, 68, 77, 80, 73, 77, 80, 89, 77, 80, 72, 77, 81, 87, 77, 81, 70, 77, 82, 85, 77, 82, 66, 75, 81, 87, 75, 81, 68, 77, 80, 85, 77, 80, 68, 78, 80, 84, 78, 80, 73, 77, 80, 85, 77, 80, 73),
        intArrayOf(70, 73, 77, 82, 73, 77, 70, 73, 77, 65, 73, 77, 72, 75, 77, 81, 75, 77, 72, 75, 77, 65, 75, 77, 69, 75, 77, 84, 75, 77, 69, 75, 77, 65, 75, 77, 70, 73, 77, 82, 73, 77, 70, 73, 77, 65, 73, 77, 70, 73, 77, 85, 73, 77, 68, 74, 77, 83, 74, 77, 66, 75, 78, 82, 75, 78, 63, 75, 78, 84, 75, 78, 65, 73, 77, 82, 73, 77, 65, 75, 77, 81, 75, 77, 70, 73, 77, 82, 73, 77, 70),
        intArrayOf(78, 82, 85, 90, 82, 85, 78, 82, 85, 73, 82, 85, 80, 83, 85, 89, 83, 85, 80, 83, 85, 73, 83, 85, 77, 83, 85, 92, 83, 85, 77, 83, 85, 73, 83, 85, 78, 82, 85, 90, 82, 85, 78, 82, 85, 73, 82, 85, 78, 82, 85, 94, 82, 85, 77, 82, 86, 92, 82, 86, 75, 82, 87, 90, 82, 87, 71, 80, 86, 92, 80, 86, 73, 82, 85, 90, 82, 85, 73, 83, 85, 89, 83, 85, 78, 82, 85, 90, 82, 85, 78),
        intArrayOf(75, 78, 82, 87, 78, 82, 75, 78, 82, 70, 78, 82, 77, 80, 82, 86, 80, 82, 77, 80, 82, 70, 80, 82, 74, 80, 82, 89, 80, 82, 74, 80, 82, 70, 80, 82, 75, 78, 82, 87, 78, 82, 75, 78, 82, 70, 78, 82, 75, 78, 82, 90, 78, 82, 73, 79, 82, 88, 79, 82, 71, 80, 83, 87, 80, 83, 68, 80, 83, 89, 80, 83, 70, 78, 82, 87, 78, 82, 70, 80, 82, 86, 80, 82, 75, 78, 82, 87, 78, 82, 75),
        intArrayOf(71, 75, 78, 83, 75, 78, 71, 75, 78, 66, 75, 78, 73, 76, 78, 82, 76, 78, 73, 76, 78, 66, 76, 78, 70, 76, 78, 85, 76, 78, 70, 76, 78, 66, 76, 78, 71, 75, 78, 83, 75, 78, 71, 75, 78, 66, 75, 78, 71, 75, 78, 87, 75, 78, 70, 75, 79, 85, 75, 79, 68, 75, 80, 83, 75, 80, 64, 73, 79, 85, 73, 79, 66, 75, 78, 83, 75, 78, 66, 76, 78, 82, 76, 78, 71, 75, 78, 83, 75, 78, 71),
        intArrayOf(68, 71, 75, 80, 71, 75, 68, 71, 75, 63, 71, 75, 70, 73, 75, 79, 73, 75, 70, 73, 75, 63, 73, 75, 67, 73, 75, 82, 73, 75, 67, 73, 75, 63, 73, 75, 68, 71, 75, 80, 71, 75, 68, 71, 75, 63, 71, 75, 68, 71, 75, 83, 71, 75, 66, 72, 75, 81, 72, 75, 64, 73, 76, 80, 73, 76, 61, 73, 76, 82, 73, 76, 63, 71, 75, 80, 71, 75, 63, 73, 75, 79, 73, 75, 68, 71, 75, 80, 71, 75, 68),
        intArrayOf(76, 80, 83, 88, 80, 83, 76, 80, 83, 71, 80, 83, 78, 81, 83, 87, 81, 83, 78, 81, 83, 71, 81, 83, 75, 81, 83, 90, 81, 83, 75, 81, 83, 71, 81, 83, 76, 80, 83, 88, 80, 83, 76, 80, 83, 71, 80, 83, 76, 80, 83, 92, 80, 83, 75, 80, 84, 90, 80, 84, 73, 80, 85, 88, 80, 85, 69, 78, 84, 90, 78, 84, 71, 80, 83, 88, 80, 83, 71, 81, 83, 87, 81, 83, 76, 80, 83, 88, 80, 83, 76),
        intArrayOf(73, 76, 80, 85, 76, 80, 73, 76, 80, 68, 76, 80, 75, 78, 80, 84, 78, 80, 75, 78, 80, 68, 78, 80, 72, 78, 80, 87, 78, 80, 72, 78, 80, 68, 78, 80, 73, 76, 80, 85, 76, 80, 73, 76, 80, 68, 76, 80, 73, 76, 80, 88, 76, 80, 71, 77, 80, 86, 77, 80, 69, 78, 81, 85, 78, 81, 66, 78, 81, 87, 78, 81, 68, 76, 80, 85, 76, 80, 68, 78, 80, 84, 78, 80, 73, 76, 80, 85, 76, 80, 73),
        intArrayOf(69, 73, 76, 81, 73, 76, 69, 73, 76, 64, 73, 76, 71, 74, 76, 80, 74, 76, 71, 74, 76, 64, 74, 76, 68, 74, 76, 83, 74, 76, 68, 74, 76, 64, 74, 76, 69, 73, 76, 81, 73, 76, 69, 73, 76, 64, 73, 76, 69, 73, 76, 85, 73, 76, 68, 73, 77, 83, 73, 77, 66, 73, 78, 81, 73, 78, 62, 71, 77, 83, 71, 77, 64, 73, 76, 81, 73, 76, 64, 74, 76, 80, 74, 76, 69, 73, 76, 81, 73, 76, 69),
        intArrayOf(78, 81, 85, 90, 81, 85, 78, 81, 85, 73, 81, 85, 80, 83, 85, 89, 83, 85, 80, 83, 85, 73, 83, 85, 77, 83, 85, 92, 83, 85, 77, 83, 85, 73, 83, 85, 78, 81, 85, 90, 81, 85, 78, 81, 85, 73, 81, 85, 78, 81, 85, 93, 81, 85, 76, 82, 85, 91, 82, 85, 74, 83, 86, 90, 83, 86, 71, 83, 86, 92, 83, 86, 73, 81, 85, 90, 81, 85, 73, 83, 85, 89, 83, 85, 78, 81, 85, 90, 81, 85, 78),
        intArrayOf(74, 78, 81, 86, 78, 81, 74, 78, 81, 69, 78, 81, 76, 79, 81, 85, 79, 81, 76, 79, 81, 69, 79, 81, 73, 79, 81, 88, 79, 81, 73, 79, 81, 69, 79, 81, 74, 78, 81, 86, 78, 81, 74, 78, 81, 69, 78, 81, 74, 78, 81, 90, 78, 81, 73, 78, 82, 88, 78, 82, 71, 78, 83, 86, 78, 83, 67, 76, 82, 88, 76, 82, 69, 78, 81, 86, 78, 81, 69, 79, 81, 85, 79, 81, 74, 78, 81, 86, 78, 81, 74),
        intArrayOf(71, 74, 78, 83, 74, 78, 71, 74, 78, 66, 74, 78, 73, 76, 78, 82, 76, 78, 73, 76, 78, 66, 76, 78, 70, 76, 78, 85, 76, 78, 70, 76, 78, 66, 76, 78, 71, 74, 78, 83, 74, 78, 71, 74, 78, 66, 74, 78, 71, 74, 78, 86, 74, 78, 69, 75, 78, 84, 75, 78, 67, 76, 79, 83, 76, 79, 64, 76, 79, 85, 76, 79, 66, 74, 78, 83, 74, 78, 66, 76, 78, 82, 76, 78, 71, 74, 78, 83, 74, 78, 71),
        intArrayOf(67, 71, 74, 79, 71, 74, 67, 71, 74, 62, 71, 74, 69, 72, 74, 78, 72, 74, 69, 72, 74, 62, 72, 74, 66, 72, 74, 81, 72, 74, 66, 72, 74, 62, 72, 74, 67, 71, 74, 79, 71, 74, 67, 71, 74, 62, 71, 74, 67, 71, 74, 83, 71, 74, 66, 71, 75, 81, 71, 75, 64, 71, 76, 79, 71, 76, 60, 69, 75, 81, 69, 75, 62, 71, 74, 79, 71, 74, 62, 72, 74, 78, 72, 74, 67, 71, 74, 79, 71, 74, 67),
        intArrayOf(76, 79, 83, 88, 79, 83, 76, 79, 83, 71, 79, 83, 78, 81, 83, 87, 81, 83, 78, 81, 83, 71, 81, 83, 75, 81, 83, 90, 81, 83, 75, 81, 83, 71, 81, 83, 76, 79, 83, 88, 79, 83, 76, 79, 83, 71, 79, 83, 76, 79, 83, 91, 79, 83, 74, 80, 83, 89, 80, 83, 72, 81, 84, 88, 81, 84, 69, 81, 84, 90, 81, 84, 71, 79, 83, 88, 79, 83, 71, 81, 83, 87, 81, 83, 76, 79, 83, 88, 79, 83, 76),
        intArrayOf(72, 76, 79, 84, 76, 79, 72, 76, 79, 67, 76, 79, 74, 77, 79, 83, 77, 79, 74, 77, 79, 67, 77, 79, 71, 77, 79, 86, 77, 79, 71, 77, 79, 67, 77, 79, 72, 76, 79, 84, 76, 79, 72, 76, 79, 67, 76, 79, 72, 76, 79, 88, 76, 79, 71, 76, 80, 86, 76, 80, 69, 76, 81, 84, 76, 81, 65, 74, 80, 86, 74, 80, 67, 76, 79, 84, 76, 79, 67, 77, 79, 83, 77, 79, 72, 76, 79, 84, 76, 79, 72)
    ) }
}
