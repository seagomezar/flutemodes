# Original User Request

## Initial Request — 2026-10-11T13:57:20Z

Realizar una auditoría exhaustiva de calidad musicológica (Urtext) y funcional de todas las transcripciones y aplicaciones del ecosistema FluteModes (84 Ejercicios Modales, Taffanel & Gaubert E.J. 1, 2, 4, 5, 10, 11 y Mathieu-André Reichert Op. 5 R. 1, 2, 4, 5 en ABC, PDFs A4, Web interactiva, iOS/iPadOS y Android), corregir automáticamente cualquier discrepancia o defecto detectado, y desplegar la versión v1.5.1 en todas las plataformas (incluyendo subida a TestFlight con Build 10, compilación de APK firmado versionCode 9 y publicación en GitHub con tag v1.5.1).

Working directory: /Users/sebas/Desktop/partituras
Integrity mode: development

## Reference Material & Verification Resources

- **Fuentes Urtext Originales en el Repositorio:**
  - `Taffanel & Gaubert - 17 Grands Exercices Journaliers de Mecanisme.pdf` (Editions Alphonse Leduc, Paris, Plate A. L. 16.588: E.J. 1 págs. 6–7, E.J. 2 págs. 8–9, E.J. 4 págs. 14–17 [111–114], E.J. 5 pág. 18 [115], E.J. 10 págs. 23–24 [120–121], E.J. 11 págs. 25–28 [122–125]).
  - `Reichert_7_Daily_Exercises_Op5.pdf` (Edición B. Schott's Söhne, Mainz, Plate 20623: Nº 1 págs. 2–3, Nº 2 págs. 4–5, Nº 4 págs. 8–9, Nº 5 págs. 10–13).
- **Entregables Web, ABC y PDF:**
  - Portal web: `docs/index.html`, `docs/ej1.html`, `docs/ej2.html`, `docs/ej4.html`, `docs/ej5.html`, `docs/ej10.html`, `docs/ej11.html`, `docs/r1.html`, `docs/r2.html`, `docs/r4.html`, `docs/r5.html`.
  - Archivos ABC y PDFs A4 en raíz (`*.abc`, `*_transcripcion.pdf`, `*_validacion.html`) y en `docs/downloads/abc/` y `docs/downloads/pdf/`.
- **Aplicaciones Nativas y Suites de Pruebas:**
  - **iOS/iPadOS (`FluteModes/`):** Proyecto Xcode (`FluteModes.xcodeproj`, `project.yml`), motor compartido `FluteModes/FluteModes/Resources/score_template.html`, modelos/generadores en `FluteModes/FluteModes/Models/`, sintetizador en `FluteModes/FluteModes/Audio/ScoreAudioPlayer.swift`, vistas en `FluteModes/FluteModes/Views/` y suite de pruebas `FluteModes/FluteModesTests/FluteModesTests.swift`.
  - **Android (`FluteModesAndroid/`):** Proyecto Gradle (`app/build.gradle.kts`), motor compartido `FluteModesAndroid/app/src/main/assets/score_template.html`, código fuente en `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/` y pruebas unitarias en `FluteModesAndroid/app/src/test/java/com/seagomezar/flutemodes/`.

## Requirements

### R1. Auditoría de Fidelidad Musicológica Urtext y Paridad Multiplataforma
Auditar de forma programática y visual todo el repertorio:
1. **84 Ejercicios Modales** (12 tónicas × 7 modos × 8 articulaciones = 672 combinaciones).
2. **Taffanel & Gaubert** (E.J. 1, E.J. 2, E.J. 4, E.J. 5, E.J. 10 y E.J. 11) frente al original de Alphonse Leduc (Plate A. L. 16.588).
3. **Mathieu-André Reichert Op. 5** (R. 1, R. 2, R. 4 y R. 5) frente al original de B. Schott's Söhne (Plate 20623).

Verificar nota por nota las alturas, octavas, armaduras, fórmulas de compás, indicaciones metronómicas, alteraciones de precaución, signos de repetición (`D.S. al Fine`, Fine, anacrusas, acordes/arpegios finales y codas) y patrones de articulación/ligaduras en los archivos `.abc`, los PDFs A4, las páginas interactivas de `docs/`, los diccionarios de `score_template.html` (iOS y Android) y los arreglos MIDI de síntesis de audio (`ExerciseGenerator.swift` y `ExerciseGenerator.kt`). Si se detecta cualquier discrepancia o inconsistencia entre plataformas, corregirla y regenerar los artefactos correspondientes.

### R2. Auditoría Funcional Completa de las Aplicaciones (iOS/iPadOS, Android y Web)
Auditar toda la funcionalidad de las aplicaciones nativas y web:
- Navegación fluida y sin errores entre los 11 módulos de estudio (`Modos`, `E.J. 1`, `E.J. 2`, `E.J. 4`, `E.J. 5`, `E.J. 10`, `E.J. 11`, `R. 1`, `R. 2`, `R. 4`, `R. 5`).
- Renderizado SVG en `score_template.html` (iOS y Android) y páginas web (`docs/`): verificar que todas las secciones y articulaciones se rendericen completas sin recortes horizontales ni verticales, con los hooks `% EJ...` y `% R...` funcionando correctamente.
- Reproducción de audio WAV PCM en tiempo real (`ScoreAudioPlayer.swift` y `ScoreAudioPlayer.kt`) y sincronización exacta del cursor/resaltado visual nota por nota (`highlightNote` / `clearHighlight`), incluyendo anacrusas, tresillos, notas con puntillo y calderones finales.
- Persistencia del progreso de estudio (`PracticeStore`), avance automático/manual de articulaciones y secciones, metrónomo, temporizador, modo pantalla encendida y traducciones completas Español/Inglés (`LocalizationManager`) sin claves faltantes.

### R3. Actualización a `v1.5.1`, Verificación Automatizada y Despliegue (TestFlight, APK y GitHub)
- Ampliar las pruebas unitarias en `FluteModesTests.swift` (iOS) y `ExerciseGeneratorTest.kt` / `PracticeStoreTest.kt` (Android) para cubrir exhaustivamente todos los ejercicios (Modos, E.J. 1/2/4/5/10/11 y R. 1/2/4/5), verificando paridad de notas MIDI, cabeceras ABC, rangos de flauta y persistencia de estado.
- Actualizar la versión a **`v1.5.1`**:
  - **iOS/iPadOS:** `MARKETING_VERSION = 1.5.1` y `CURRENT_PROJECT_VERSION = 10` en `FluteModes.xcodeproj/project.pbxproj` y `FluteModes/project.yml`.
  - **Android:** `versionCode = 9` y `versionName = "1.5.1"` en `FluteModesAndroid/app/build.gradle.kts`.
  - **Web:** Actualizar referencias y enlaces de descarga en `docs/index.html` a `v1.5.1` y `FluteModes-v1.5.1-release.apk`.
- Compilar el APK firmado de lanzamiento (`./gradlew testDebugUnitTest assembleRelease`) y copiarlo a `docs/downloads/apk/FluteModes-v1.5.1-release.apk`.
- Archivar y subir la versión `v1.5.1` (Build `10`) de iOS/iPadOS a **App Store Connect / TestFlight** (`xcodebuild ... archive` y `xcodebuild -exportArchive ... -allowProvisioningUpdates`).
- Realizar commit de todos los cambios, crear el tag anotado `v1.5.1` y hacer push a `origin main --tags`.

## Acceptance Criteria

### Auditoría Musicológica y Paridad de Datos
- [ ] Un script o suite de verificación programática confirma 100% de paridad entre las notas de `score_template.html` (iOS y Android), las secuencias MIDI de `ExerciseGenerator.swift` y `ExerciseGenerator.kt`, y los archivos `.abc` para E.J. 1, 2, 4, 5, 10, 11 y R. 1, 2, 4, 5.
- [ ] `FluteModes/FluteModes/Resources/score_template.html` y `FluteModesAndroid/app/src/main/assets/score_template.html` están sincronizados al 100% sin diferencias involuntarias.
- [ ] Todas las claves de traducción (`LocalizationManager.swift` y `LocalizationManager.kt`) existen tanto en español (`es`) como en inglés (`en`) sin valores vacíos ni claves sin traducir.

### Pruebas Unitarias e Integridad Web
- [ ] `./gradlew testDebugUnitTest` en `FluteModesAndroid/` pasa con 0 fallos.
- [ ] `xcodebuild test` (o compilación y verificación de `FluteModesTests`) en `FluteModes/` pasa con 0 fallos.
- [ ] Todos los enlaces (`href` / `src`) en `docs/index.html`, `docs/ej*.html` y `docs/r*.html` apuntan a archivos existentes y válidos en `docs/`.

### Despliegue `v1.5.1` (Android APK, iOS TestFlight y GitHub)
- [ ] El archivo `docs/downloads/apk/FluteModes-v1.5.1-release.apk` existe, está firmado para producción y `docs/index.html` enlaza a él.
- [ ] El archivo de iOS `v1.5.1` (Build `10`) se archiva (`** ARCHIVE SUCCEEDED **`) y se sube exitosamente a App Store Connect / TestFlight (`Uploaded FluteModes` / `** EXPORT SUCCEEDED **`).
- [ ] `git status` muestra el árbol de trabajo limpio y `git push origin main --tags` publica el commit y el tag `v1.5.1` en GitHub.
