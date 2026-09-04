package com.seagomezar.flutemodes.model

enum class Tonic(
    val displayName: String,
    val majorKey: String,
    val minorKey: String,
    val majorDesc: String,
    val minorDesc: String,
    val rootMidi: Int,
    val abcNoteSequence: List<String>
) {
    SI(
        "Si", "B", "Bm",
        "5 sostenidos (Fa♯, Do♯, Sol♯, Re♯, La♯)",
        "2 sostenidos (Fa♯, Do♯)",
        59,
        listOf("B,", "C", "D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'")
    ),
    DO_NATURAL(
        "Do", "C", "Cm",
        "Sin alteraciones",
        "3 bemoles (Si♭, Mi♭, La♭)",
        60,
        listOf("C", "D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'")
    ),
    DO_SOSTENIDO(
        "Do♯", "C#", "C#m",
        "7 sostenidos",
        "4 sostenidos (Fa♯, Do♯, Sol♯, Re♯)",
        61,
        listOf("C", "D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'")
    ),
    RE(
        "Re", "D", "Dm",
        "2 sostenidos (Fa♯, Do♯)",
        "1 bemol (Si♭)",
        62,
        listOf("D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'")
    ),
    MI_BEMOL(
        "Mi♭", "Eb", "Ebm",
        "3 bemoles (Si♭, Mi♭, La♭)",
        "6 bemoles",
        63,
        listOf("E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'")
    ),
    MI(
        "Mi", "E", "Em",
        "4 sostenidos (Fa♯, Do♯, Sol♯, Re♯)",
        "1 sostenido (Fa♯)",
        64,
        listOf("E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'")
    ),
    FA(
        "Fa", "F", "Fm",
        "1 bemol (Si♭)",
        "4 bemoles (Si♭, Mi♭, La♭, Re♭)",
        65,
        listOf("F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'")
    ),
    FA_SOSTENIDO(
        "Fa♯", "F#", "F#m",
        "6 sostenidos",
        "3 sostenidos (Fa♯, Do♯, Sol♯)",
        66,
        listOf("F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'")
    ),
    SOL(
        "Sol", "G", "Gm",
        "1 sostenido (Fa♯)",
        "2 bemoles (Si♭, Mi♭)",
        67,
        listOf("G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'")
    ),
    LA_BEMOL(
        "La♭", "Ab", "Abm",
        "4 bemoles (Si♭, Mi♭, La♭, Re♭)",
        "7 bemoles",
        68,
        listOf("A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'")
    ),
    LA(
        "La", "A", "Am",
        "3 sostenidos (Fa♯, Do♯, Sol♯)",
        "Sin alteraciones",
        69,
        listOf("A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'")
    ),
    SI_BEMOL(
        "Si♭", "Bb", "Bbm",
        "2 bemoles (Si♭, Mi♭)",
        "5 bemoles",
        70,
        listOf("B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''")
    );

    fun accidentalMap(mode: ModeType): Map<Int, String> {
        return when (mode) {
            ModeType.IONIAN, ModeType.AEOLIAN -> emptyMap()
            ModeType.LYDIAN -> when (this) {
                DO_NATURAL, RE, MI, FA_SOSTENIDO, SOL, LA, SI -> mapOf(3 to "^")
                DO_SOSTENIDO -> mapOf(3 to "^^")
                MI_BEMOL, FA, LA_BEMOL, SI_BEMOL -> mapOf(3 to "=")
            }
            ModeType.MIXOLYDIAN -> when (this) {
                SI, DO_SOSTENIDO, RE, MI, FA_SOSTENIDO, SOL, LA -> mapOf(6 to "=")
                DO_NATURAL, MI_BEMOL, FA, LA_BEMOL, SI_BEMOL -> mapOf(6 to "_")
            }
            ModeType.DORIAN -> when (this) {
                SI, DO_SOSTENIDO, MI, FA_SOSTENIDO, LA -> mapOf(5 to "^")
                DO_NATURAL, RE, MI_BEMOL, FA, SOL, LA_BEMOL, SI_BEMOL -> mapOf(5 to "=")
            }
            ModeType.PHRYGIAN -> when (this) {
                SI, DO_SOSTENIDO, MI, FA_SOSTENIDO, LA -> mapOf(1 to "=")
                DO_NATURAL, RE, MI_BEMOL, FA, SOL, LA_BEMOL, SI_BEMOL -> mapOf(1 to "_")
            }
            ModeType.LOCRIAN -> when (this) {
                SI, DO_SOSTENIDO, FA_SOSTENIDO -> mapOf(1 to "=", 4 to "=")
                MI -> mapOf(1 to "=", 4 to "_")
                LA -> mapOf(1 to "^", 4 to "_")
                else -> mapOf(1 to "_", 4 to "_")
            }
        }
    }
}
