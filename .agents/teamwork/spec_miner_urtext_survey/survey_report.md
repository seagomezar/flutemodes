# Informe Exhaustivo de Auditoría Musicológica Urtext y Paridad Multiplataforma
**Ecosistema FluteModes (84 Ejercicios Modales, Taffanel & Gaubert E.J. 1, 2, 4, 5, 10, 11 y Mathieu-André Reichert Op. 5 R. 1, 2, 4, 5)**

- **Autor de la Auditoría:** `spec_miner_urtext_survey` (Specification Mining Specialist)
- **Fecha:** 2026-10-11
- **Ámbito:** Repositorio `/Users/sebas/Desktop/partituras` (Fuentes Urtext, Archivos ABC, PDFs A4, Portal Web `docs/`, iOS/iPadOS `FluteModes/`, Android `FluteModesAndroid/`, Motores de Síntesis PCM WAV y Generadores de Partituras).

---

## 1. Resumen Ejecutivo y Hallazgos Críticos

Se ha llevado a cabo una investigación exhaustiva e interdisciplinar (análisis musicológico de fuentes primarias, verificación de código fuente en Swift, Kotlin, Python y JavaScript, comparación de buffers MIDI de síntesis de audio, y validación de marcado vectorial SVG/ABC) sobre la totalidad de los 95 ejercicios base del ecosistema FluteModes:
1. **84 Ejercicios Modales Paralelos** (Maestro León Giraldo: 12 tónicas × 7 modos × 8 articulaciones = 672 combinaciones).
2. **6 Ejercicios de Paul Taffanel & Philippe Gaubert** (*17 Grands Exercices Journaliers de Mécanisme*, Éditions Alphonse Leduc, París: E.J. 1, E.J. 2, E.J. 4, E.J. 5, E.J. 10 y E.J. 11).
3. **4 Ejercicios de Mathieu-André Reichert** (*7 Exercices Journaliers pour la Flûte, Op. 5*, B. Schott's Söhne, Mainz: Nº 1, Nº 2, Nº 4 y Nº 5).

### Matriz de Defectos Críticos Detectados

| ID | Gravedad | Componente / Archivo | Descripción del Defecto | Impacto Funcional / Musicológico |
|---|---|---|---|---|
| **DEF-01** | **CRÍTICO** | `FluteModes/FluteModes/Resources/score_template.html` y `FluteModesAndroid/app/src/main/assets/score_template.html` (Líneas 921–941) | Las funciones `renderR1Schott`, `renderR2Schott`, `renderR4Schott`, `renderR5Schott` y sus tablas de datos asociadas (`REICHERT_ARTS_12`, `REICHERT_ARTS_8`, `R1_SECTIONS_DATA`, etc.) **no fueron inyectadas** en `score_template.html`. Sólo están los hooks de llamada en `renderScore()`. | Al abrir cualquier ejercicio de Reichert (R.1, R.2, R.4, R.5) en iOS o Android, se lanza un error no capturado `ReferenceError: Can't find variable: renderR1Schott` y la partitura queda completamente en blanco. |
| **DEF-02** | **CRÍTICO** | `FluteModesAndroid/.../model/ExerciseGenerator.kt` (Líneas 135–160: `ej2RawMeasures`) | **Corrupción en compases de transición menor de E.J. 2:** Se copiaron accidentalmente los grados mayores de E.J. 1 en los compases pares 4, 8, 14, 18, 22, 24 y 28 (ej. M.4 tiene `^G` [Sol♯] en vez de `=G` [Sol♮]; M.8 tiene `^A` [La♯] en vez de `=A` [La♮]; M.14 tiene `^c` [Do♯] en vez de `=c` [Do♮]; M.18 tiene `^d` [Re♯] en vez de `=d` [Re♮]; M.22 tiene `^e` [Mi♯] en vez de `=e` [Mi♮]; M.24 tiene `^f` [Fa♯] en vez de `=f` [Fa♮]; M.28 tiene `^g` [Sol♯] en vez de `=g` [Sol♮]). | En Android, E.J. 2 genera compases de transición modulante mayor en vez de menor, rompiendo la tonalidad de llegada menor de Taffanel & Gaubert. Swift y `score_template.html` tienen las notas correctas. |
| **DEF-03** | **ALTO** | `FluteModesAndroid/.../audio/ScoreAudioPlayer.kt` (Línea 444) | En la síntesis de audio de E.J. 2, el acorde disminuido vii° está hardcodeado a `listOf(base, base + 1, base + 3, base + 5, base + 6)`. En modo menor, el cuarto semitono debe ser `base + 4` (Sol♭ en Re menor), tal como está en `ScoreAudioPlayer.swift` línea 402 (`let dimFourthSemitone = isMinor ? 4 : 5`). | La síntesis de audio de E.J. 2 en Android reproduce un cuarto grado mayor/aumentado en compases pares, discrepando de iOS y de la partitura Urtext. |
| **DEF-04** | **ALTO** | `FluteModes/FluteModesTests/FluteModesTests.swift` (Líneas 230, 295–312) | **Fallo de compilación en tests de iOS:** El test `testEJ4AllSectionsAndArticulationsGenerateValidAbc` invoca `sec.shortTitle` en vez de `sec.shortName`. Además, `testReichertR1ToR5PracticeStoreTracking` invoca métodos inexistentes `store.markR1Completed(art)`, `store.isR2FullyCompleted`, etc., en vez de la API real de `PracticeStore.swift` (`markEJ4Completed(art, for: .r2)`, etc.). | `xcodebuild test` falla con código 65 durante la compilación de la suite de pruebas de iOS. |
| **DEF-05** | **MEDIO** | `FluteModes/FluteModesTests/FluteModesTests.swift` | Faltan métodos de prueba unitaria para E.J. 5, E.J. 10 y E.J. 11 en iOS (mientras que en Android ya existen en `ExerciseGeneratorTest.kt`). | Cobertura asimétrica entre plataformas. |
| **DEF-06** | **MEDIO** | `docs/index.html` (Líneas 1060, 1066, 1072, 1078) | Enlaces de descarga rotos: Enlaza a `downloads/abc/reichert_r1_completo.abc`, `reichert_r2_completo.abc`, `reichert_r4_completo.abc`, `reichert_r5_completo.abc`. Sin embargo, en `docs/downloads/abc/` los archivos se llaman `Reichert_R1_Coleccion_Completa.abc`, etc. | Error 404 al intentar descargar los archivos ABC de Reichert desde el portal web. |
| **DEF-07** | **BAJO** | `docs/downloads/abc/` | Falta copiar el archivo de la colección completa de modos `00_Coleccion_Completa_84_Modos_EJ4.abc` a `docs/downloads/abc/`. | Colección maestra de modos no disponible en la carpeta de descargas web. |
| **DEF-08** | **BAJO** | `score_template.html` (Línea 310) | En E.J. 2, se omitió la indicación `Reprise à l'octave` sobre el compás 1 (`const repriseHtml = isEj2 ? "" : ...`), mientras que en la fuente Urtext Alphonse Leduc (pág. 6 / Plancha 17.204 / 16.588) está expresamente grabada. | Discrepancia visual menor con el facsímil Urtext. |

---

## 2. Fuentes Urtext Originales y Especificaciones Musicográficas

### 2.1. Paul Taffanel & Philippe Gaubert — *17 Grands Exercices Journaliers de Mécanisme*
- **Edición Documentada:** Éditions Alphonse Leduc, París.
- **Plancha:** Plancha histórica `A. L. 16.588` (compendio maestro) y plancha de la tirada independiente `A. L. 17.204` (presente en el archivo facsimilar de 62 páginas `taffanel.pdf` en raíz).
- **Módulos Requeridos:**
  1. **E.J. 1 (pp. 6–7 / facsímil pp. 2–3):**
     - **Título:** *E.J. 1 — Pentacordes majeurs*.
     - **Subtítulo:** *A travailler successivement avec chacune des dix articulations suivantes / To be practised with each of the following ten articulations*.
     - **Indicación al compás 1:** *Reprise à l'octave* con barra de repetición `|:`.
     - **Fórmula de compás:** 4/2 (4 blancas por compás, 32 semicorcheas agrupadas de 8 en 8).
     - **Estructura Tonal:** 15 parejas cromáticas ascendentes desde Re4 (MIDI 62) hasta Fa5 (MIDI 77).
       - Compás impar (1, 3, 5, ..., 29): Pentacordo Mayor `(1 2 3 4 5 4 3 2)`.
       - Compás par (2, 4, 6, ..., 30): Acorde disminuido modulante vii° hacia la siguiente tónica `(1 ♭2 ♭3 4 ♭5 4 ♭3 ♭2)` con giro final `(1 ♭2 ♭3 4 ♭5 ♭3 ♭2 1)`.
       - Compás 24: Barra de repetición `:|` hacia el compás 1.
       - Compases 25–30: Repetición con indicación *8va* (Re5 a Fa6).
       - Compás 31 (cierre): Fa5 (Fa6 en 8va) redonda `f4 z4 z8 |]`.
     - **10 Articulaciones Oficiales:**
       1. 8 ligadas: `(DEF GAGFE)`
       2. 4 y 4 ligadas: `(DEFG) (AGFE)`
       3. 1 picada y 3 ligadas: `.D(EFG) .A(GFE)`
       4. 3 ligadas y 1 picada: `(DEF).G (AGF).E`
       5. 2 ligadas y 2 picadas: `(DE).F.G (AG).F.E`
       6. 2 picadas y 2 ligadas: `.D.E(FG) .A.G(FE)`
       7. 1 picada, 2 ligadas, 1 picada: `.D(EF).G .A(GF).E`
       8. De 2 en 2 ligadas: `(DE)(FG) (AG)(FE)`
       9. De 2 en 2 sincopadas: `.D(EF)(GA) (GF).E`
       10. Todo picado (staccato): `.D.E.F.G .A.G.F.E`
     - **Hook de Integración Web/Nativa:** `% EJ1_LEDUC_ART:<artId>` (artId 0..10).

  2. **E.J. 2 (pp. 8–9 / facsímil pp. 6–7):**
     - **Título:** *E.J. 2 — Pentacordes mineurs*.
     - **Subtítulo:** Idéntico a E.J. 1.
     - **Indicación al compás 1:** *Reprise à l'octave* con barra `|:`.
     - **Fórmula de compás:** Compasillo C (representado en 4/2 para alineación exacta de semicorcheas).
     - **Estructura Tonal:** 15 parejas cromáticas en modo menor con tercera menor (Re menor a Fa menor):
       - Compás 1: Re menor `DEFGAGFE`.
       - Compás 2 (vii° a Mi♭ menor): `D _E =F _G _A G F E`.
       - Compás 4 (vii° a Mi menor): `^D =E ^F =G =A G F E`.
       - Compás 6 (vii° a Fa menor): `E =F =G _A _B A G F`.
       - Compás 8 (vii° a Fa♯ menor): `^E ^F ^G =A =B A G F`.
       - Compás 10 (vii° a Sol menor): `^F =G =A _B =c B A G`.
       - Compás 12 (vii° a Sol♯ menor): `^^F ^G ^A B ^c B A G` (Doble sostenido ^^F).
       - Compás 14 (vii° a La menor): `^G =A =B =c =d c B A`.
       - Compás 16 (vii° a Si♭ menor): `A _B =c _d _e d c B`.
       - Compás 18 (vii° a Si menor): `^A =B ^c =d =e d c B`.
       - Compás 20 (vii° a Do menor): `B =c =d _e =f e d c`.
       - Compás 22 (vii° a Do♯ menor): `^B ^c ^d =e ^f e d c` (Enarmonía ^B).
       - Compás 24 (vii° a Re menor): `^c =d =e =f =g f e d` con repetición `:|`.
       - Compases 25–30: Transcripción *8va*.
       - Compás 31 (cierre): Fa5 (Fa6) `f4 z4 z8 |]`.
     - **10 Articulaciones:** Idénticas a E.J. 1.
     - **Hook:** `% EJ2_LEDUC_ART:<artId>` (artId 0..10).

  3. **E.J. 4 (pp. 14–17 / facsímil pp. 16–19 [págs. 111–114 en compendio]):**
     - **Título:** *E.J. 4 — Gammes diatoniques*.
     - **Subtítulo:** *A travailler successivement avec chacune des articulations suivantes*.
     - **Fórmula de compás:** C / 4/2.
     - **Estructura:** 24 secciones de 8 compases (12 Mayores + 12 Menores Relativas armónicas y melódicas) + 1 Coda final de 2 compases en Do Mayor (Total: 25 secciones, 194 compases).
     - **Orden de Tonalidades:** Do M, La m, Fa M, Re m, Si♭ M, Sol m, Mi♭ M, Do m, La♭ M, Fa m, Re♭ M, Si♭ m, Sol♭ M, Mi♭ m, Si M, Sol♯ m, Mi M, Do♯ m, La M, Fa♯ m, Re M, Si m, Sol M, Mi m, Coda Do M.
     - **8 Articulaciones Oficiales:**
       1. 8 ligadas: `(8)`
       2. 4 y 4 ligadas: `(4)(4)`
       3. 1 picada y 3 ligadas: `·(3) ·(3)`
       4. 2 ligadas y 2 picadas: `(2)·· (2)··`
       5. 2 picadas y 2 ligadas: `··(2) ··(2)`
       6. Sincopadas de 4: `·(2)· ·(2)·`
       7. De 2 en 2 ligadas: `(2)(2)(2)(2)`
       8. Sincopadas de 8: `·(2)(2)(2)·`
     - **Hook:** `% EJ4_LEDUC_ART:<artId>:SEC:<secIdx>` (artId 0..8, secIdx 0..24).

  4. **E.J. 5 (p. 18 / facsímil p. 24 [pág. 115 en compendio]):**
     - **Título:** *E.J. 5 — GAMMES CHROMATIQUES*.
     - **Subtítulo:** *A travailler successivement avec chacune des dix articulations suivantes*.
     - **Fórmulas de Compás:** 6/8 (Articulaciones 1–5, 8–10) y 2/4 (Articulaciones 6–7).
     - **Estructura:** 12 escalas cromáticas por tónica (Do a Si).
     - **10 Articulaciones Oficiales:**
       1. 12 ligadas (compás completo en 6/8): `(12)`
       2. 6 y 6 ligadas (6/8): `(6)(6)`
       3. 4 ligadas y 2 picadas (6/8): `(4)·· (4)··`
       4. 2 picadas y 4 ligadas (6/8): `··(4) ··(4)`
       5. 2 ligadas y 4 picadas (6/8): `(2)···· (2)····`
       6. De 3 en 3 ligadas (2/4): `(3)(3)(3)(3)`
       7. 3 ligadas y 3 picadas (2/4): `(3)··· (3)···`
       8. De 2 en 2 ligadas (6/8): `(2)(2)(2)(2)(2)(2)`
       9. Sincopadas (6/8): `·(2)(2)(2)(2)(2)·`
       10. Todas picadas (staccato en 6/8): `·×12`
     - **Hook:** `% EJ5_LEDUC_ART:<artId>:SEC:<secIdx>` (artId 0..10, secIdx 0..11).

  5. **E.J. 10 (pp. 23–24 / facsímil pp. 34–35 [págs. 120–121 en compendio]):**
     - **Título:** *E.J. 10 — ARPÈGES*.
     - **Subtítulo:** *A travailler successivement avec chacune des dix articulations suivantes*.
     - **Fórmulas de Compás:** 6/8 y 2/4.
     - **Estructura:** 12 sistemas modulantes cubriendo las 24 tonalidades en arpegios tríadas y cuatríadas.
     - **10 Articulaciones:** Idénticas a E.J. 5.
     - **Hook:** `% EJ10_LEDUC_ART:<artId>:SEC:<secIdx>` (artId 0..10, secIdx 0..11).

  6. **E.J. 11 (pp. 25–28 / facsímil pp. 38–41 [págs. 122–125 en compendio]):**
     - **Título:** *E.J. 11 — ARPÈGES BRISÉS*.
     - **Subtítulo:** *A travailler successivement avec chacune des dix articulations suivantes*.
     - **Fórmulas de Compás:** 9/8 (18 notas por compás) y 3/4.
     - **Estructura:** 12 secciones de arpegios quebrados en 24 tonalidades.
     - **10 Articulaciones Oficiales:**
       1. 18 ligadas (compás completo en 9/8): `(18)`
       2. 6, 6 y 6 ligadas (9/8): `(6)(6)(6)`
       3. 4 ligadas y 2 picadas (9/8): `(4)·· (4)·· (4)··`
       4. 2 picadas y 4 ligadas (9/8): `··(4) ··(4) ··(4)`
       5. 2 ligadas y 4 picadas (9/8): `(2)···· (2)···· (2)····`
       6. De 3 en 3 ligadas (3/4): `(3)(3)(3)(3)(3)(3)`
       7. 3 ligadas y 3 picadas (3/4): `(3)··· (3)··· (3)···`
       8. De 2 en 2 ligadas (9/8): `(2)(2)(2)(2)(2)(2)(2)(2)(2)`
       9. Sincopadas de a 2 (9/8): `·(2)(2)(2)(2)(2)(2)(2)(2)·`
       10. Todas picadas (staccato en 9/8): `·×18`
     - **Hook:** `% EJ11_LEDUC_ART:<artId>:SEC:<secIdx>` (artId 0..10, secIdx 0..11).

---

### 2.2. Mathieu-André Reichert — *7 Exercices Journaliers pour la Flûte, Op. 5*
- **Edición Documentada:** B. Schott's Söhne, Mainz.
- **Plancha:** Plancha histórica `20623`.
- **Módulos Requeridos:**
  1. **Nº 1 (R. 1, Schott 20623, págs. 2–3):**
     - **Fórmula de compás:** 6/8.
     - **Tempo:** *De 80 à 100 ♩.* (negra con puntillo = 80–100).
     - **Estructura:** 24 tonalidades alternadas Mayor / Relativo Menor melódico + compás 97–100 en Do Mayor con `D.S. al Fine` (Total: 25 secciones de 4 compases = 100 compases).
     - **Notas por Sección:** 43 notas (12 semicorcheas en compases 1, 2, 3; 6 semicorcheas + 1 corchea en compás 4 + silencios `z2 z2`).
     - **Signos de Repetición:** *Segno* `!segno!` en compás 1; *Fine* `!fine!` en compases 4 y 100; *D.S.* `!D.S.!` en compás 96.
     - **Articulaciones:** 10 fórmulas de articulación (adaptación de las fórmulas de 6/8 de T&G / Schott).
     - **Hook:** `% R1_SCHOTT_ART:<artId>:SEC:<secIdx>` (artId 0..10, secIdx 0..24).

  2. **Nº 2 (R. 2, Schott 20623, págs. 4–5):**
     - **Fórmula de compás:** 2/4.
     - **Tempo:** *De 120 à 152 ♩* (negra = 120–152).
     - **Estructura:** 24 tonalidades + D.S. al Fine (25 secciones). Cada sección consta de una anacrusa de 4 semicorcheas (acorde de tónica `1 3 5 1`), compases 1..7 (8 semicorcheas cada uno con arpegios de V7 e I en distintas inversiones), y compás 8 (1 corchea tónica `1` con cuña `!wedge!` + silencios).
     - **Notas por Sección:** 61 notas (4 anacrusa + 7 × 8 compases + 1 corchea final).
     - **Transporte de Octava (8va):** En la plancha Schott 20623, las secciones 0 (Do M), 3 (Re m), 7 (Do m), 10 (Re♭ M), 17 (Do♯ m) y 24 (Do M Fine) están escritas en octava baja con la anotación *8va...*, por lo que las notas reales sonoras son una octava más aguda (+12 semitonos).
     - **Articulaciones:** 8 articulaciones (adaptación de las fórmulas de 2/4).
     - **Hook:** `% R2_SCHOTT_ART:<artId>:SEC:<secIdx>` (artId 0..8, secIdx 0..24).

  3. **Nº 4 (R. 4, Schott 20623, págs. 8–9):**
     - **Fórmula de compás:** C (4/4).
     - **Tempo:** *De 116 à 144 ♩* (negra = 116–144).
     - **Estructura:** 24 tonalidades + D.S. al Fine (25 secciones). Cada sección consta de compases 1..3 (16 semicorcheas con saltos diatónicos y bordaduras cromáticas inferiores `♯4`, `♯7`, `♯9`, `♯11`), y compás 4 (12 semicorcheas + 1 corchea tónica final con cuña + silencio).
     - **Notas por Sección:** 61 notas (3 × 16 + 12 + 1).
     - **Alteraciones de Precaución Urtext:** En tonalidades mayores, en el compás 3, tercer pulso, el noveno grado natural cancela el noveno grado aumentado del compás 2 (ej. en Do Mayor: Re♯ en compás 2, Re♮ de precaución en compás 3).
     - **Registro Flautístico:** Secciones 7 (Do m) y 10 (Re♭ M) están escritas iniciando en Do5 y Re♭5; sección 17 (Do♯ m) está escrita en octava 4 con indicación *8va...*.
     - **Articulaciones:** 8 articulaciones.
     - **Hook:** `% R4_SCHOTT_ART:<artId>:SEC:<secIdx>` (artId 0..8, secIdx 0..24).

  4. **Nº 5 (R. 5, Schott 20623, págs. 10–13):**
     - **Fórmula de compás:** 2/4 tresillos (tresillos de semicorchea, 12 notas por compás).
     - **Tempo:** *De 144 à 184 ♪* (corchea = 144–184).
     - **Estructura:** 24 tonalidades + D.S. al Fine (25 secciones). Compases 1..7 (12 notas de tresillo por compás = 4 tresillos) y compás 8 (6 notas de tresillo + 1 corchea tónica final con cuña + silencios).
     - **Notas por Sección:** 91 notas (7 × 12 + 6 + 1).
     - **Diseño Armónico Urtext:** M.1 (I/i), M.2 (V6/5), M.3 (V2), M.4 (I/i), M.5 (modulación a IV/VI), M.6 (acordes de paso disminuidos), M.7 (cadencia dominante), M.8 (resolución tónica).
     - **Articulaciones:** 10 articulaciones adaptadas a subdivisiones de tresillo.
     - **Hook:** `% R5_SCHOTT_ART:<artId>:SEC:<secIdx>` (artId 0..10, secIdx 0..24).

---

### 2.3. Colección Completa de 84 Modos Paralelos (Maestro León Giraldo)
- **Pedagogía:** Sistema paralelo desarrollado por el flautista y pedagogo León Giraldo sobre la estructura interválica y técnica de Taffanel & Gaubert E.J. 4.
- **Tónicas (12):**
  1. Si (B3 grave - Pata de Si, 246.94 Hz)
  2. Do (C4 flauta estándar, 261.63 Hz)
  3. Do♯ (C♯4, 277.18 Hz)
  4. Re (D4, 293.66 Hz)
  5. Mi♭ (E♭4, 311.13 Hz)
  6. Mi (E4, 329.63 Hz)
  7. Fa (F4, 349.23 Hz)
  8. Fa♯ (F♯4, 369.99 Hz)
  9. Sol (G4, 392.00 Hz)
  10. La♭ (A♭4, 415.30 Hz)
  11. La (A4 estándar, 440.00 Hz)
  12. Si♭ (B♭4, 466.16 Hz)
- **7 Modos por Tónica:**
  - **Familia Mayor (Armadura Mayor fija de la tónica):**
    1. **Jónico (Mayor natural):** Fórmula `1 - 2 - 3 - 4 - 5 - 6 - 7`. Sin alteraciones accidentales.
    2. **Lidio:** Fórmula `1 - 2 - 3 - ♯4 - 5 - 6 - 7`. Distintivo: Cuarto grado aumentado (♯4 / `^`).
    3. **Mixolidio:** Fórmula `1 - 2 - 3 - 4 - 5 - 6 - ♭7`. Distintivo: Séptimo grado menor (♭7 / `_` o natural según armadura).
  - **Familia Menor (Armadura Menor fija de la tónica):**
    4. **Dórico:** Fórmula `1 - 2 - ♭3 - 4 - 5 - 6 - ♭7`. Distintivo: Sexto grado mayor (6 / sostenido o becuadro).
    5. **Eólico (Menor natural):** Fórmula `1 - 2 - ♭3 - 4 - 5 - ♭6 - ♭7`. Sin alteraciones accidentales respecto a la armadura menor.
    6. **Frigio:** Fórmula `1 - ♭2 - ♭3 - 4 - 5 - ♭6 - ♭7`. Distintivo: Segundo grado menor (♭2 / bemol o becuadro).
    7. **Locrio:** Fórmula `1 - ♭2 - ♭3 - 4 - ♭5 - ♭6 - ♭7`. Distintivos: Segundo grado menor (♭2) y quinta disminuida (♭5).
- **Morfología del Ejercicio:** 8 compases en compás 4/2 (L:1/8, Q:1/2=90), con 16 notas por compás en C.1..C.7 y 15 notas en C.8 (Total exacto: **127 notas** por ejercicio).
- **8 Articulaciones:**
  1. Toda ligada: `(16)`
  2. 4 y 4 ligadas: `(4)(4) (4)(4)`
  3. 2 ligadas y 2 picadas: `(2)·· (2)··`
  4. 1 picada y 3 ligadas: `·(3) ·(3)`
  5. 3 ligadas y 1 picada: `(3)· (3)·`
  6. De 2 en 2 ligadas: `(2)(2)(2)(2)`
  7. De 2 en 2 sincopadas: `·(2)(2)(2)·`
  8. Toda picada (staccato): `·×16`

---

## 3. Catálogo de Características Descubiertas (Features Discovered)

| # | Categoría | Feature | Descripción | Inputs | Outputs | Error Behavior | Descubierto Vía |
|---|---|---|---|---|---|---|---|
| 1 | Modos | 84 Ejercicios Modales | Generación ABC completa de 12 tónicas × 7 modos con armaduras fijas y alteraciones accidentales | Tonic (12), ModeType (7), Articulation (8) | Cadena ABC válida con cabecera X:1, M:4/2, L:1/8, Q:1/2=90, 8 compases, 127 notas | Si la tónica o modo es inválido, excepción de índice | `ExerciseGenerator.swift:103`, `ExerciseGenerator.kt:5` |
| 2 | Modos | Síntesis PCM Modos | Síntesis acústica de 127 notas en tiempo real con armónicos de flauta/piano y afinación pitagórica/temperada | Tonic, ModeType, Articulation, BPM | Buffer `AVAudioPCMBuffer` / `ShortArray` PCM 16-bit 44.1 kHz | Retorna buffer vacío o nulo si tempo <= 0 | `ScoreAudioPlayer.swift:433`, `ScoreAudioPlayer.kt:102` |
| 3 | T&G E.J. 1 | Transcripción Pentacordos Mayores | 30 compases cromáticos + Coda en Re Mayor/Fa (Plancha A. L. 16.588) | Articulation (0..10), BPM | Partitura ABC con 10 articulaciones, indicación `Reprise à l'octave` y compases 8va | Articulación fuera de rango 0..10 usa default 0 | `generate_ej1_abc_files.py`, `score_template.html:201` |
| 4 | T&G E.J. 2 | Transcripción Pentacordos Menores | 30 compases cromáticos + Coda en Re menor/Fa (Plancha A. L. 16.588) | Articulation (0..10), BPM | Partitura ABC con doble sostenido `^^F` (M.12) y enarmonía `^B` (M.22) | Defecto en Android: compases 4, 8, 14, 18, 22, 24, 28 corrompidos con 3ª mayor | `generate_ej2_abc_files.py`, `ExerciseGenerator.kt:131` |
| 5 | T&G E.J. 4 | 24 Tonalidades Diatónicas | 194 compases (24 secciones de 8 compases + Coda de 2 compases en Do Mayor) | Articulation (0..8), Section (0..24), BPM | Partitura interactiva de 128 notas por sección (29 notas en Coda) | Índice de sección fuera de rango 0..24 lanza error | `generate_ej4_validation.py`, `ExerciseGenerator.swift:237` |
| 6 | T&G E.J. 5 | 12 Escalas Cromáticas | Escalas cromáticas en 6/8 y 2/4 con 10 articulaciones oficiales | Articulation (0..10), Section (0..11), BPM | Renderizado de partitura con cambio de compás M:6/8 y M:2/4 | Articulación desconocida usa original | `generate_ej5_validation.py`, `score_template.html:681` |
| 7 | T&G E.J. 10 | 12 Arpegios Mayores y Menores | 12 arpegios en 6/8 y 2/4 cubriendo 24 tonalidades | Articulation (0..10), Section (0..11), BPM | Partitura con notas de síntesis MIDI alineadas | Sección < 0 o > 11 arroja error | `generate_ej10_validation.py`, `score_template.html:769` |
| 8 | T&G E.J. 11 | 12 Arpegios Quebrados | 12 secciones en 9/8 (18 notas/compás) y 3/4 | Articulation (0..10), Section (0..11), BPM | Partitura con subdivisiones ternarias compuestas | Falta de soporte de articulación arroja ligadura por defecto | `generate_ej11_validation.py`, `score_template.html:866` |
| 9 | Reichert R. 1 | Exercice Journalier Nº 1 (6/8) | 24 tonalidades + D.S. al Fine (100 compases, 43 notas/sección) | Articulation (0..10), Section (0..24), BPM | Partitura Urtext Schott 20623 con Segno, Fine y D.S. | **Defecto en score_template.html: función renderR1Schott ausente** | `generate_reichert_all.py:138`, `build_reichert_outputs.py:1438` |
| 10 | Reichert R. 2 | Exercice Journalier Nº 2 (2/4) | 24 tonalidades modulantes con anacrusa + D.S. al Fine (200 compases, 61 notas/sección) | Articulation (0..8), Section (0..24), BPM | Partitura Schott 20623 con anacrusa y 8va en Do M, Re m, Do m, Re♭ M, Do♯ m | **Defecto en score_template.html: función renderR2Schott ausente** | `generate_reichert_all.py:292`, `build_reichert_outputs.py:1506` |
| 11 | Reichert R. 4 | Exercice Journalier Nº 4 (4/4) | 24 tonalidades de saltos diatónicos + D.S. al Fine (100 compases, 61 notas/sección) | Articulation (0..8), Section (0..24), BPM | Partitura Schott 20623 con alteraciones cromáticas inferiores | **Defecto en score_template.html: función renderR4Schott ausente** | `generate_reichert_all.py:476`, `build_reichert_outputs.py:1584` |
| 12 | Reichert R. 5 | Exercice Journalier Nº 5 (2/4 Tresillos) | 24 tonalidades en tresillos de semicorchea + D.S. al Fine (200 compases, 91 notas/sección) | Articulation (0..10), Section (0..24), BPM | Partitura Schott 20623 con 10 articulaciones de tresillo | **Defecto en score_template.html: función renderR5Schott ausente** | `generate_reichert_all.py:584`, `build_reichert_outputs.py:1645` |
| 13 | UI / Persistencia | PracticeStore | Seguimiento de progreso por ejercicio, tónica y articulación | Claves de persistencia SharedPreferences / UserDefaults | Conjuntos de articulaciones completadas, tónica activa y último ejercicio | Si el almacenamiento está corrupto, inicia en estado limpio | `PracticeStore.swift`, `PracticeStore.kt` |
| 14 | Localización | LocalizationManager | Gestor bilingüe español e inglés sin claves faltantes | Clave de texto (`key`) e idioma (`es`/`en`) | Cadena traducida exacta | Si no encuentra la clave, retorna la clave en crudo | `LocalizationManager.swift:43`, `LocalizationManager.kt:26` |
| 15 | Web | Portal docs/ | Portal interactivo con visores web audio y enlaces de descarga | Navegador web moderno con Web Audio y SVG | Páginas `index.html`, `ej*.html`, `r*.html` | **Defecto: 4 enlaces rotos a reichert_r*.abc** | `docs/index.html` |

---

## 4. Catálogo de Casos Límite (Edge Cases)

| # | Feature | Input | Comportamiento Observado / Especificación Requerida |
|---|---|---|---|
| 1 | Modos en Si (B3) | Tónica Si con clave de Sol | La tónica es Si3 (MIDI 59), requiriendo flauta con pata de Si (*B-footjoint*). Las notas graves bajan hasta Si3 con línea adicional inferior (`B,` en ABC). La síntesis calcula 246.94 Hz. |
| 2 | Modos en Do♯ (7 sostenidos) | Tónica Do♯ en Modo Lidio | La armadura fija es Do♯ Mayor (7 sostenidos: F# C# G# D# A# E# B#). El cuarto grado lidio (Fa) requiere doble sostenido `^^F` (Sol natural sonoro). La síntesis y el renderizador manejan correctamente el doble sostenido. |
| 3 | T&G E.J. 2 Compás 12 | Sol♯ menor (vii° a Sol♯ m) | En la entrada a Sol♯ menor, el compás requiere doble sostenido `^^F` en la primera semicorchea (`^^F^G^AB^cBAG`). El renderizador SVG y la síntesis sintetizan MIDI 68 (Sol♯) y MIDI 67 (Sol♮/F##). |
| 4 | T&G E.J. 2 Compás 22 | Do♯ menor (vii° a Do♯ m) | Requiere enarmonía `^B` (Si sostenido = Do♮ sonoro). La partitura y la síntesis interpretan MIDI 60 (Do4). |
| 5 | T&G E.J. 4 Coda Final | Sección 24 (Compases 193–194) | A diferencia de las secciones 0..23 que tienen 128 notas (8 compases de 16 semicorcheas), la Coda tiene exactamente 29 notas (2 compases con cierre en calderón/nota larga en Do). La síntesis reproduce 29 notas con duración cuádruple en la nota final. |
| 6 | Reichert R. 2 Secciones 8va | Secciones 0, 3, 7, 10, 17, 24 | Están escritas en octava 4 con signo `^8va...` en la partitura visual, pero el sonido real (MIDI) se desplaza +12 semitonos (+1 octava) para reflejar la altura real de concierto. |
| 7 | Reichert R. 4 Compás 3 | Tonalidades Mayores en compás 3 | El noveno grado del compás 3 lleva becuadro de precaución para cancelar el noveno grado sostenido del compás 2 (ej. en Do Mayor: Re♮ en compás 3 frente a Re♯ en compás 2). |
| 8 | Reichert R. 5 Tresillos | Compás 8 de cada sección | En vez de 4 tresillos completos (12 notas), el compás 8 tiene 2 tresillos (6 notas) + 1 corchea tónica final con cuña (`!wedge!`) + silencios de corchea. La síntesis ajusta la duración a corchea con staccato. |
| 9 | Salto de Articulación | Modo completado (8va articulación) | `advanceToNextArticulation()` marca la 8ª articulación como completada y cicla a la primera articulación del siguiente modo. Al completar el 7º modo, despliega diálogo de hito (*milestone*) ofreciendo avanzar a la siguiente tónica cromática. |
| 10 | Resaltado de Notas | Anacrusas en R. 2 | La anacrusa de 4 notas en R. 2 debe sincronizar los eventos de resaltado (`highlightNote`) antes de la primera barra de compás sin desfasar el contador de compases del visor. |

---

## 5. Auditoría Comparativa Detallada por Componente

### 5.1. Comparación de `score_template.html` (iOS vs Android)
- **Ruta iOS:** `FluteModes/FluteModes/Resources/score_template.html`
- **Ruta Android:** `FluteModesAndroid/app/src/main/assets/score_template.html`
- **Hash SHA-256:** `748fa33f1c5a28d1d623bde1124122e9aac2deea9ddb54630b276839f5596962` (Ambos archivos son **100% idénticos byte a byte**).
- **Problema Estructural Detectado:**
  Ambos archivos contienen en las líneas 921–941:
  ```javascript
  function renderScore(abcString) {
    const r1Match = abcString && abcString.match(/%\s*R1_SCHOTT_ART:(\d+):SEC:(\d+)/);
    if (r1Match) {
      renderR1Schott(parseInt(r1Match[1], 10) || 0, parseInt(r1Match[2], 10) || 0);
      return;
    }
    const r2Match = abcString && abcString.match(/%\s*R2_SCHOTT_ART:(\d+):SEC:(\d+)/);
    if (r2Match) {
      renderR2Schott(parseInt(r2Match[1], 10) || 0, parseInt(r2Match[2], 10) || 0);
      return;
    }
    const r4Match = abcString && abcString.match(/%\s*R4_SCHOTT_ART:(\d+):SEC:(\d+)/);
    if (r4Match) {
      renderR4Schott(parseInt(r4Match[1], 10) || 0, parseInt(r4Match[2], 10) || 0);
      return;
    }
    const r5Match = abcString && abcString.match(/%\s*R5_SCHOTT_ART:(\d+):SEC:(\d+)/);
    if (r5Match) {
      renderR5Schott(parseInt(r5Match[1], 10) || 0, parseInt(r5Match[2], 10) || 0);
      return;
    }
  ```
  Sin embargo, el script generador `build_reichert_outputs.py` falló al inyectar el bloque de código de Reichert (`reichert_js`, líneas 1380–1685 de `build_reichert_outputs.py`) debido a un desacople en el espaciado de `target_hook`: buscaba `"    function renderScore(abcString) {"` con 4 espacios mientras que en `score_template.html` la función no tenía sangría (`function renderScore(abcString) {`).
  Como resultado, ni `REICHERT_ARTS_12`, ni `REICHERT_ARTS_8`, ni `R1_SECTIONS_DATA`, ni `R2_SECTIONS_DATA`, ni `R4_SECTIONS_DATA`, ni `R5_SECTIONS_DATA`, ni las funciones `renderR1Schott`, `renderR2Schott`, `renderR4Schott`, `renderR5Schott` existen en la plantilla compartida.

### 5.2. Comparación de Generadores de Notas MIDI (`ExerciseGenerator.swift` vs `ExerciseGenerator.kt`)
Se ejecutó una verificación programática exhaustiva sobre las 8 matrices de notas MIDI:
- `ej4SectionMidiNotes` (25 secciones × 128 notas [29 en sec 24]): **100% de paridad (0 diferencias)**.
- `ej5SectionMidiNotes` (12 secciones): **100% de paridad (0 diferencias)**.
- `ej10SectionMidiNotes` (12 secciones): **100% de paridad (0 diferencias)**.
- `ej11SectionMidiNotes` (12 secciones): **100% de paridad (0 diferencias)**.
- `r1SectionMidiNotes` (25 secciones × 43 notas): **100% de paridad (0 diferencias)**.
- `r2SectionMidiNotes` (25 secciones × 61 notas): **100% de paridad (0 diferencias)**.
- `r4SectionMidiNotes` (25 secciones × 61 notas): **100% de paridad (0 diferencias)**.
- `r5SectionMidiNotes` (25 secciones × 91 notas): **100% de paridad (0 diferencias)**.
Total de secciones verificadas: **161 secciones**. Paridad en secuencias MIDI: **100%**.

### 5.3. Comparación de Compases Crudos de E.J. 1 y E.J. 2
- **E.J. 1 (`ej1RawMeasures`):** 30 compases.
  - Swift: 30 compases.
  - Kotlin: 30 compases.
  - `score_template.html`: 30 compases.
  - Paridad: **100% idénticos en alturas y alteraciones**.
- **E.J. 2 (`ej2RawMeasures`):** 30 compases.
  - Swift y `score_template.html`: **100% idénticos y conformes con Alphonse Leduc (A. L. 16.588)**.
  - Kotlin (`ExerciseGenerator.kt`): **Discrepancia en 18 notas de 7 compases pares**.
    - Compás 4: Kotlin tiene `^G` (Sol♯) vs Swift `=G` (Sol♮).
    - Compás 8: Kotlin tiene `^A` (La♯) vs Swift `=A` (La♮).
    - Compás 14: Kotlin tiene `^c` (Do♯) vs Swift `=c` (Do♮).
    - Compás 18: Kotlin tiene `^d` (Re♯) vs Swift `=d` (Re♮).
    - Compás 22: Kotlin tiene `^e` (Mi♯) vs Swift `=e` (Mi♮).
    - Compás 24: Kotlin tiene `^f` (Fa♯) vs Swift `=f` (Fa♮).
    - Compás 28: Kotlin tiene `^g` (Sol♯) vs Swift `=g` (Sol♮).
    - Causa: En Kotlin se transcribió la cadencia hacia modo mayor en lugar de menor. Requiere sincronización inmediata con Swift y `score_template.html`.

### 5.4. Comparación de Motores de Audio (`ScoreAudioPlayer.swift` vs `ScoreAudioPlayer.kt`)
- **Modos (84):** Ambos motores generan tonos PCM con síntesis aditiva de armónicos de flauta y envolvente ADSR suave. El cálculo de frecuencia `440.0 * 2^((midi - 69)/12)` es matemáticamente idéntico en Double.
- **E.J. 4, E.J. 5, E.J. 10, E.J. 11, R. 1, R. 2, R. 4, R. 5:** Ambos utilizan las matrices de notas precalculadas (`ej4SectionMidiNotes`, `r1SectionMidiNotes`, etc.), las cuales tienen 100% de paridad.
- **E.J. 1 y E.J. 2:**
  - En Swift (`generateChromaticPentachordBuffer`):
    `let dimFourthSemitone = isMinor ? 4 : 5`
    `let dim = [base, base + 1, base + 3, base + dimFourthSemitone, base + 6]`
  - En Kotlin (`generateChromaticPentachordBuffer`):
    `val dim = listOf(base, base + 1, base + 3, base + 5, base + 6)`
    El cuarto grado en Kotlin no varía según `isMinor`, produciendo una cuarta justa en E.J. 2 en vez de la cuarta disminuida / tritono `base + 4`.

### 5.5. Comparación de Localización (`LocalizationManager.swift` vs `LocalizationManager.kt`)
- Claves extraídas en Swift: **163 claves**.
- Claves extraídas en Kotlin: **163 claves**.
- Claves faltantes en Swift: **0**.
- Claves faltantes en Kotlin: **0**.
- Textos vacíos en español o inglés: **0**.
- Paridad en claves de traducción: **100% completa y sincronizada**.

### 5.6. Comparación de Archivos ABC y PDFs de Descarga
- Archivos `.abc` en raíz y carpetas:
  - `abc_ej1/`: 12 archivos (10 articulaciones + original + colección completa).
  - `abc_ej2/`: 12 archivos.
  - `abc_ej4/`: 10 archivos (8 articulaciones + original + colección completa).
  - `abc_ej5/`: 12 archivos.
  - `abc_ej10/`: 12 archivos.
  - `abc_ej11/`: 12 archivos.
  - `abc_modos/`: 13 archivos (12 tónicas + colección completa).
  - Todos coinciden con sus copias en `docs/downloads/abc/`, excepto que en `docs/downloads/abc/`:
    - Falta `00_Coleccion_Completa_84_Modos_EJ4.abc`.
    - Los archivos completos de Reichert se llaman `Reichert_R1_Coleccion_Completa.abc` (en vez de `reichert_r1_completo.abc`).
- Archivos `.pdf` en raíz y `docs/downloads/pdf/`:
  - Los 10 PDFs de transcripción (`taffanel_ej*.pdf`, `reichert_r*.pdf`) existen en ambas ubicaciones y son idénticos byte a byte.
  - Los 12 PDFs de modos (`modos_01_si.pdf` .. `modos_12_si_bemol.pdf`) y el compendio maestro `metodo_completo_modos_flauta.pdf` (6.7 MB) existen y son válidos.

---

## 6. Recomendaciones de Acción Inmediata para el Agente Implementador

1. **Reparar e Inyectar Reichert en `score_template.html`:**
   Corregir `build_reichert_outputs.py` para reemplazar limpiamente `target_hook` (independiente de espacios) y asegurar que el bloque `// === BEGIN REICHERT OP5 SCHOTT ===` quede completamente escrito en `FluteModes/FluteModes/Resources/score_template.html` y copiado a `FluteModesAndroid/app/src/main/assets/score_template.html`.
2. **Corregir E.J. 2 en `ExerciseGenerator.kt`:**
   Reemplazar `ej2RawMeasures` en Kotlin con los valores exactos de `ExerciseGenerator.swift` y `score_template.html`, restituyendo los grados menores en los compases 4, 8, 14, 18, 22, 24 y 28.
3. **Corregir Síntesis de Audio de E.J. 2 en `ScoreAudioPlayer.kt`:**
   Modificar línea 444 para usar `val dimFourthSemitone = if (isMinor) 4 else 5` y `val dim = listOf(base, base + 1, base + 3, base + dimFourthSemitone, base + 6)`.
4. **Reparar Suite de Pruebas de iOS `FluteModesTests.swift`:**
   - Cambiar `sec.shortTitle` por `sec.shortName` en línea 230.
   - Ajustar llamadas a `store.markEJ4Completed(art, for: .r2)` y `store.markEJ5TypeCompleted(art, for: .r1)` en líneas 295–312.
   - Agregar métodos de prueba para E.J. 5, E.J. 10 y E.J. 11 copiando la estructura de Android.
5. **Corregir Enlaces en `docs/index.html` y Copiar Archivos:**
   - Asegurar que `docs/downloads/abc/reichert_r*.abc` existan (o crear symlinks/copias con los nombres `reichert_r*_completo.abc`).
   - Copiar `00_Coleccion_Completa_84_Modos_EJ4.abc` a `docs/downloads/abc/`.
   - Actualizar enlaces del APK en `docs/index.html` a `FluteModes-v1.5.1-release.apk` y textos a `v1.5.1`.
6. **Despliegue y Versión v1.5.1:**
   - Subir versión a 1.5.1 (Build 10) en iOS y versionCode 9 (1.5.1) en Android.
   - Compilar APK, archivar TestFlight, crear commit y tag v1.5.1.
