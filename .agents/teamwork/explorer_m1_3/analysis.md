# Technical Analysis Report: DEF-06, DEF-07 & Web Portal Link Audit

**Agent:** `explorer_m1_3`  
**Milestone:** Milestone 1 (Score Engine & Urtext Parity Fixes)  
**Date:** 2026-10-11  
**Target Recipient:** Orchestrator & Worker Agents  

---

## 1. Executive Summary

A comprehensive, automated, and manual audit was conducted across the entire FluteModes web portal (`docs/` directory), covering all 13 HTML files, dynamic JavaScript asset loaders, CSS stylesheets, asset download directories, and E2E regression tests (`tests/test_tier3_combinations.py`).

### Key Findings
1. **DEF-06 (Web Download Links Mismatch):** In `docs/index.html` lines 1060, 1066, 1072, and 1078, the download anchor tags point to lowercase filenames (`downloads/abc/reichert_r{1,2,4,5}_completo.abc`). On disk in `docs/downloads/abc/`, these files exist exclusively under TitleCase naming (`Reichert_R{1,2,4,5}_Coleccion_Completa.abc`). Clicking these links yields HTTP 404 errors.
2. **DEF-07 (Missing Master Modal ABC Collection):** The master modal exercise collection `00_Coleccion_Completa_84_Modos_EJ4.abc` exists in `abc_modos/` (32,013 bytes, 84 tunes) but was never copied to `docs/downloads/abc/`. Furthermore, in `docs/index.html` lines 1081–1085, the "Método Completo de Modos (84 Modos Paralelos)" table entry only provides a PDF download link (`metodo_completo_modos_flauta.pdf`), omitting the ABC download.
3. **Link Audit Results (119 Links Scanned):**
   - **Internal Static Links:** 93 links verified. 89 valid, 4 broken (the exact 4 Reichert links identified in DEF-06).
   - **External Links:** 16 links verified (Apple TestFlight, GitHub repository, jsdelivr CDN for abcjs, and mailto support/privacy contacts). All schemas and domains valid.
   - **Internal Fragment Anchors:** 6 links verified. All target IDs (`#preview`, `#features`, `#downloads`, `#maestro`) exist and resolve cleanly in `docs/index.html`.
   - **CSS `url()` References:** 0 broken assets.
   - **Dynamic JS Link Setters:** All dynamic file targets (`EX_ARTS[...].fname` in `r1.html`–`r5.html`, `CHROMATIC_ART_LIST[...].file1/file2` in `index.html`, and `modos_${tonicId}.abc` in `index.html`) map 100% to valid files in `docs/downloads/abc/`.

---

## 2. DEF-06 Technical Investigation

### 2.1. Root Cause Analysis
In `build_reichert_outputs.py` (lines 173–213):
- The script defines specs:
  ```python
  ("R1", ..., "reichert_r1_completo.abc")
  ("R2", ..., "reichert_r2_completo.abc")
  ("R4", ..., "reichert_r4_completo.abc")
  ("R5", ..., "reichert_r5_completo.abc")
  ```
- In lines 205–212:
  ```python
  collection_text = "\n\n".join(all_tunes)
  with open(os.path.join(ABC_DL_DIR, f"Reichert_{code}_Coleccion_Completa.abc"), "w", encoding="utf-8") as f:
      f.write(collection_text)

  # Write root_abc_name (original Urtext + all articulations) to workspace & artifacts
  for dst in [os.path.join(WORKSPACE, root_abc_name), os.path.join(ARTIFACT_DIR, root_abc_name)]:
      with open(dst, "w", encoding="utf-8") as f:
          f.write(collection_text)
  ```
- As a result, the files were written to:
  - `docs/downloads/abc/Reichert_R1_Coleccion_Completa.abc` (and R2, R4, R5)
  - `/Users/sebas/Desktop/partituras/reichert_r1_completo.abc` (in workspace root)
- A byte-by-byte comparison (`diff -s`) confirmed that `reichert_r{N}_completo.abc` in workspace root is **100% identical** to `Reichert_R{N}_Coleccion_Completa.abc` in `docs/downloads/abc/`.
- However, `docs/index.html` was authored expecting lowercase filenames in `downloads/abc/`:
  - Line 1060: `<a href="downloads/abc/reichert_r1_completo.abc" download>ABC (10 Arts.)</a>`
  - Line 1066: `<a href="downloads/abc/reichert_r2_completo.abc" download>ABC (8 Arts.)</a>`
  - Line 1072: `<a href="downloads/abc/reichert_r4_completo.abc" download>ABC (8 Arts.)</a>`
  - Line 1078: `<a href="downloads/abc/reichert_r5_completo.abc" download>ABC (10 Arts.)</a>`

### 2.2. Failure Reproduction
Running the dedicated E2E test:
```bash
python3 -m unittest tests.test_tier3_combinations.TestTier3Combinations.test_c08_web_portal_download_links_casing_integrity
```
Yields:
```
AssertionError: Lists differ: ['reichert_r1_completo.abc', 'reichert_r2_completo.abc', 'reichert_r4_completo.abc', 'reichert_r5_completo.abc'] != []
: DEF-06: Found broken/casing-mismatched download links in docs/index.html: ['reichert_r1_completo.abc', 'reichert_r2_completo.abc', 'reichert_r4_completo.abc', 'reichert_r5_completo.abc']
```

### 2.3. Solution Architecture: Defense in Depth
To guarantee 100% resilience against both web portal clicks, external scripts, automated regressors, and future rebuilds of `build_reichert_outputs.py`:
1. **HTML Alignment:** Update lines 1060, 1066, 1072, 1078 in `docs/index.html` to point to `downloads/abc/Reichert_R{N}_Coleccion_Completa.abc`. This perfectly harmonizes with the TitleCase naming convention used for all Taffanel complete collections in that same table (`11_Coleccion_Completa_Taffanel_EJ1_10_Articulaciones.abc`, etc.).
2. **Filesystem Aliases:** Provide copies or symlinks for `reichert_r{N}_completo.abc` inside `docs/downloads/abc/`.
3. **Generator Pipeline Hardening:** Update `build_reichert_outputs.py` so that line 208 also writes `root_abc_name` (`reichert_r{N}_completo.abc`) to `ABC_DL_DIR`. When `build_reichert_outputs.py` is executed (which happens during M1 for DEF-01 Schott engine injection), both files are generated simultaneously.

---

## 3. DEF-07 Technical Investigation

### 3.1. Root Cause Analysis
- `abc_modos/00_Coleccion_Completa_84_Modos_EJ4.abc` contains all 84 modal exercises (12 tonics × 7 parallel modes, exactly 1,091 lines, 32,013 bytes, tunes `X:1` to `X:84`).
- During previous releases, this master collection file was generated in `abc_modos/` and packaged in `Coleccion_Completa_PDFs_Modos_EJ4.zip`, but was omitted from the copy pipeline into `docs/downloads/abc/`.
- In `docs/index.html` lines 1081–1085:
  ```html
  <tr>
    <td style="font-weight: 700; color: #fff;">📘 Método Completo de Modos (84 Modos Paralelos)</td>
    <td class="i18n" data-es="Compendio íntegro de 36 páginas con las 12 tónicas y sus 7 modos paralelos del Maestro León Giraldo." data-en="Complete 36-page compendium covering all 12 tonics and 7 parallel modes by Maestro León Giraldo.">Compendio íntegro de 36 páginas con las 12 tónicas y sus 7 modos paralelos del Maestro León Giraldo.</td>
    <td>PDF (7.0 MB)</td>
    <td><a href="downloads/pdf/metodo_completo_modos_flauta.pdf" download>📥 Descargar PDF Maestro</a></td>
  </tr>
  ```
  Users visiting the Official Download Center could download the 7.0 MB PDF compendium and individual tonic ABC files (`modos_01_si.abc` to `modos_12_si_bemol.abc`), but had no link to download the complete 84-mode ABC collection.

### 3.2. Failure Reproduction
Running the dedicated E2E test:
```bash
python3 -m unittest tests.test_tier3_combinations.TestTier3Combinations.test_c10_master_modal_collection_abc_presence
```
Yields:
```
AssertionError: False is not true : DEF-07: 00_Coleccion_Completa_84_Modos_EJ4.abc is missing from docs/downloads/abc/
```

### 3.3. Solution Architecture
1. **Asset Copy:** Copy `abc_modos/00_Coleccion_Completa_84_Modos_EJ4.abc` to `docs/downloads/abc/00_Coleccion_Completa_84_Modos_EJ4.abc`.
2. **Workspace Root Parity:** Copy `abc_modos/00_Coleccion_Completa_84_Modos_EJ4.abc` to `/Users/sebas/Desktop/partituras/00_Coleccion_Completa_84_Modos_EJ4.abc` to mirror the standalone ABC files in root.
3. **Web Portal Download Link:** In `docs/index.html`:
   - Update line 1083 from `<td>PDF (7.0 MB)</td>` to `<td>PDF (7.0 MB) / ABC</td>`.
   - Update line 1084 to:
     `<a href="downloads/pdf/metodo_completo_modos_flauta.pdf" download>📥 Descargar PDF Maestro</a> · <a href="downloads/abc/00_Coleccion_Completa_84_Modos_EJ4.abc" download>ABC (84 Modos)</a>`.

---

## 4. Comprehensive Link Audit

### 4.1. Audit Methodology
Every HTML file in `docs/` was parsed using Python's `html.parser.HTMLParser` and regex DOM inspectors. Every attribute capable of accepting URIs (`href`, `src`, `poster`, `action`, `data-src`) and inline CSS `url(...)` declarations was resolved against the filesystem or validated against URI schemes.

### 4.2. File-by-File Audit Inventory

| File | Tag | Attribute | Target Value | Category | Verification Result |
|---|---|---|---|---|---|
| `docs/ej1.html` | `<script>` | `src` | `./abcjs-basic-min.js` | Internal Script | **OK** (file exists: 468,158 bytes) |
| `docs/ej2.html` | (none) | (none) | Self-contained inline SVGs & Web Audio | Standalone App | **OK** (0 broken links) |
| `docs/ej4.html` | `<script>` | `src` | `https://cdn.jsdelivr.net/npm/abcjs@6.2.2/dist/abcjs-basic-min.js` | External CDN | **OK** (valid URL) |
| `docs/ej4.html` | `<a>` | `href` | `index.html` | Navigation | **OK** (file exists: 87,418 bytes) |
| `docs/ej5.html` | `<script>` | `src` | `https://cdn.jsdelivr.net/npm/abcjs@6.4.4/dist/abcjs-basic-min.js` | External CDN | **OK** (valid URL) |
| `docs/ej5.html` | `<a>` | `href` | `downloads/abc/00_Taffanel_EJ5_Original_AL16588.abc` | Asset Download | **OK** (file exists: 1,686 bytes) |
| `docs/ej10.html` | `<script>` | `src` | `https://cdn.jsdelivr.net/npm/abcjs@6.4.4/dist/abcjs-basic-min.js` | External CDN | **OK** (valid URL) |
| `docs/ej10.html` | `<a>` | `href` | `downloads/abc/00_Taffanel_EJ10_Original_AL16588.abc` | Asset Download | **OK** (file exists: 3,062 bytes) |
| `docs/ej11.html` | `<script>` | `src` | `https://cdn.jsdelivr.net/npm/abcjs@6.4.4/dist/abcjs-basic-min.js` | External CDN | **OK** (valid URL) |
| `docs/ej11.html` | `<a>` | `href` | `downloads/abc/00_Taffanel_EJ11_Original_AL16588.abc` | Asset Download | **OK** (file exists: 3,966 bytes) |
| `docs/r1.html` | `<script>` | `src` | `https://cdn.jsdelivr.net/npm/abcjs@6.4.4/dist/abcjs-basic-min.js` | External CDN | **OK** (valid URL) |
| `docs/r1.html` | `<a>` | `href` | `downloads/abc/00_Reichert_R1_Original_Op5.abc` | Asset Download | **OK** (file exists: 3,594 bytes) |
| `docs/r1.html` | `<a>` | `href` | `downloads/pdf/reichert_r1_transcripcion.pdf` | Asset Download | **OK** (file exists: 627,989 bytes) |
| `docs/r1.html` | `<a>` | `href` | `index.html` | Navigation | **OK** (file exists) |
| `docs/r2.html` | `<script>` | `src` | `https://cdn.jsdelivr.net/npm/abcjs@6.4.4/dist/abcjs-basic-min.js` | External CDN | **OK** (valid URL) |
| `docs/r2.html` | `<a>` | `href` | `downloads/abc/00_Reichert_R2_Original_Op5.abc` | Asset Download | **OK** (file exists: 4,323 bytes) |
| `docs/r2.html` | `<a>` | `href` | `downloads/pdf/reichert_r2_transcripcion.pdf` | Asset Download | **OK** (file exists: 695,956 bytes) |
| `docs/r2.html` | `<a>` | `href` | `index.html` | Navigation | **OK** (file exists) |
| `docs/r4.html` | `<script>` | `src` | `https://cdn.jsdelivr.net/npm/abcjs@6.4.4/dist/abcjs-basic-min.js` | External CDN | **OK** (valid URL) |
| `docs/r4.html` | `<a>` | `href` | `downloads/abc/00_Reichert_R4_Original_Op5.abc` | Asset Download | **OK** (file exists: 4,165 bytes) |
| `docs/r4.html` | `<a>` | `href` | `downloads/pdf/reichert_r4_transcripcion.pdf` | Asset Download | **OK** (file exists: 743,572 bytes) |
| `docs/r4.html` | `<a>` | `href` | `index.html` | Navigation | **OK** (file exists) |
| `docs/r5.html` | `<script>` | `src` | `https://cdn.jsdelivr.net/npm/abcjs@6.4.4/dist/abcjs-basic-min.js` | External CDN | **OK** (valid URL) |
| `docs/r5.html` | `<a>` | `href` | `downloads/abc/00_Reichert_R5_Original_Op5.abc` | Asset Download | **OK** (file exists: 5,564 bytes) |
| `docs/r5.html` | `<a>` | `href` | `downloads/pdf/reichert_r5_transcripcion.pdf` | Asset Download | **OK** (file exists: 1,141,136 bytes) |
| `docs/r5.html` | `<a>` | `href` | `index.html` | Navigation | **OK** (file exists) |
| `docs/privacy.html` | `<a>` | `href` | `mailto:seagomezar@gmail.com` | Email Contact | **OK** (valid URI scheme) |
| `docs/privacy.html` | `<a>` | `href` | `https://seagomezar.github.io/flutemodes/` | Web Landing | **OK** (valid URL) |
| `docs/privacy.html` | `<a>` | `href` | `index.html` | Navigation | **OK** (file exists) |
| `docs/privacy.html` | `<a>` | `href` | `support.html` | Navigation | **OK** (file exists: 10,187 bytes) |
| `docs/support.html` | `<a>` | `href` | `mailto:seagomezar@gmail.com?...` | Email Contact | **OK** (valid URI scheme) |
| `docs/support.html` | `<a>` | `href` | `index.html` | Navigation | **OK** (file exists) |
| `docs/support.html` | `<a>` | `href` | `privacy.html` | Navigation | **OK** (file exists) |

### 4.3. `docs/index.html` Audit Inventory (Highlights)

- **Head & Assets:**
  - L7: `<link rel="icon" type="image/jpeg" href="app_icon.jpg" />` -> **OK**
  - L8: `<script src="abcjs-basic-min.js"></script>` -> **OK**
  - L9: `<script src="modes_data.js"></script>` -> **OK**
  - L715: `<img src="app_icon.jpg">` -> **OK**
- **Navigation Bars & Module Launchers:**
  - L723: `<a href="support.html">` -> **OK**
  - L755–L791: `<a href="ej1.html">` .. `<a href="r5.html">` (all 10 module links) -> **OK**
  - L862–L869: `onclick="window.location.href='ej4.html'"` .. `r5.html` -> **OK**
  - L916: `<a id="open-urtext-btn" href="ej1.html">` -> **OK**
  - L920: `<a id="download-abc-btn" href="downloads/abc/00_Taffanel_EJ1_Original_AL16588.abc">` -> **OK**
  - L795: `<a href="https://testflight.apple.com">` -> **OK**
  - L799: `<a href="downloads/apk/FluteModes-v1.5.0-release.apk">` -> **OK** (file exists on disk; see M4 note below)
  - L1167–L1170: `privacy.html`, `support.html`, `https://github.com/seagomezar/flutemodes`, `downloads/pdf/metodo_completo_modos_flauta.pdf` -> **OK**
- **Download Center Table:**
  - L1024 (E.J. 1): `downloads/pdf/taffanel_ej1_transcripcion.pdf` (**OK**) · `downloads/abc/11_Coleccion_Completa_Taffanel_EJ1_10_Articulaciones.abc` (**OK**) · `ej1.html` (**OK**)
  - L1030 (E.J. 2): `downloads/pdf/taffanel_ej2_transcripcion.pdf` (**OK**) · `downloads/abc/11_Coleccion_Completa_Taffanel_EJ2_10_Articulaciones.abc` (**OK**) · `ej2.html` (**OK**)
  - L1036 (E.J. 4): `downloads/pdf/taffanel_ej4_transcripcion.pdf` (**OK**) · `downloads/abc/09_Coleccion_Completa_Taffanel_EJ4_8_Articulaciones.abc` (**OK**) · `ej4.html` (**OK**)
  - L1042 (E.J. 5): `downloads/pdf/taffanel_ej5_transcripcion.pdf` (**OK**) · `downloads/abc/11_Coleccion_Completa_Taffanel_EJ5_10_Articulaciones.abc` (**OK**) · `ej5.html` (**OK**)
  - L1048 (E.J. 10): `downloads/pdf/taffanel_ej10_transcripcion.pdf` (**OK**) · `downloads/abc/11_Coleccion_Completa_Taffanel_EJ10_10_Articulaciones.abc` (**OK**) · `ej10.html` (**OK**)
  - L1054 (E.J. 11): `downloads/pdf/taffanel_ej11_transcripcion.pdf` (**OK**) · `downloads/abc/11_Coleccion_Completa_Taffanel_EJ11_10_Articulaciones.abc` (**OK**) · `ej11.html` (**OK**)
  - L1060 (R. 1): `downloads/pdf/reichert_r1_transcripcion.pdf` (**OK**) · `downloads/abc/reichert_r1_completo.abc` (**BROKEN - DEF-06**) · `r1.html` (**OK**)
  - L1066 (R. 2): `downloads/pdf/reichert_r2_transcripcion.pdf` (**OK**) · `downloads/abc/reichert_r2_completo.abc` (**BROKEN - DEF-06**) · `r2.html` (**OK**)
  - L1072 (R. 4): `downloads/pdf/reichert_r4_transcripcion.pdf` (**OK**) · `downloads/abc/reichert_r4_completo.abc` (**BROKEN - DEF-06**) · `r4.html` (**OK**)
  - L1078 (R. 5): `downloads/pdf/reichert_r5_transcripcion.pdf` (**OK**) · `downloads/abc/reichert_r5_completo.abc` (**BROKEN - DEF-06**) · `r5.html` (**OK**)
  - L1084 (84 Modos): `downloads/pdf/metodo_completo_modos_flauta.pdf` (**OK**) · (missing ABC link - **DEF-07**)
  - L1090–L1156 (12 Tonics): `downloads/pdf/modos_01_si.pdf` .. `modos_12_si_bemol.pdf` (all 12 **OK**) · `downloads/abc/modos_01_si.abc` .. `modos_12_si_bemol.abc` (all 12 **OK**)

### 4.4. Milestone 4 Notice: Release APK Reference
In `docs/index.html` line 799:
`<a href="downloads/apk/FluteModes-v1.5.0-release.apk" download class="btn btn-secondary">`
Currently points to `FluteModes-v1.5.0-release.apk`, which is valid on disk. In Milestone 4 (F14/F15 Release), once `./gradlew assembleRelease` compiles `FluteModes-v1.5.1-release.apk`, this link and line 801 text must be updated to `FluteModes-v1.5.1-release.apk`. This is tracked in M4 and does not break in M1.

---

## 5. Concrete Drop-in Implementation Specifications for Worker

### Specification 1: `docs/index.html` Edits
**Target File:** `/Users/sebas/Desktop/partituras/docs/index.html`  
**Lines 1057–1085:**

#### Before (Lines 1057–1085):
```html
          <tr>
            <td style="font-weight: 700; color: #fff;">🎵 M. A. Reichert — Op. 5 Nº 1 (R. 1 · Schott 20623)</td>
            <td class="i18n" data-es="7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 1 en 6/8 (♩. = 80–100): 24 Tonalidades Mayores y Menores + D.S. al Fine (100 compases, págs. 2–3 y 10 articulaciones)." data-en="7 Exercices Journaliers pour la Flûte, Op. 5 — No. 1 in 6/8 (♩. = 80–100): 24 Major & Minor Keys + D.S. al Fine (100 measures, pp. 2–3, and 10 articulations).">7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 1 en 6/8 (♩. = 80–100): 24 Tonalidades Mayores y Menores + D.S. al Fine (100 compases, págs. 2–3 y 10 articulaciones).</td>
            <td>PDF / ABC / Web</td>
            <td><a href="downloads/pdf/reichert_r1_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/reichert_r1_completo.abc" download>ABC (10 Arts.)</a> · <a href="r1.html">Visor</a></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">🎶 M. A. Reichert — Op. 5 Nº 2 (R. 2 · Schott 20623)</td>
            <td class="i18n" data-es="7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 2 en 2/4 (♩ = 120–152): Arpegios modulantes con anacrusa en 24 Tonalidades + D.S. al Fine (200 compases, págs. 4–5 y 8 articulaciones)." data-en="7 Exercices Journaliers pour la Flûte, Op. 5 — No. 2 in 2/4 (♩ = 120–152): Modulating arpeggios with pickup across 24 Keys + D.S. al Fine (200 measures, pp. 4–5, and 8 articulations).">7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 2 en 2/4 (♩ = 120–152): Arpegios modulantes con anacrusa en 24 Tonalidades + D.S. al Fine (200 compases, págs. 4–5 y 8 articulaciones).</td>
            <td>PDF / ABC / Web</td>
            <td><a href="downloads/pdf/reichert_r2_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/reichert_r2_completo.abc" download>ABC (8 Arts.)</a> · <a href="r2.html">Visor</a></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">🎼 M. A. Reichert — Op. 5 Nº 4 (R. 4 · Schott 20623)</td>
            <td class="i18n" data-es="7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 4 en 4/4 (♩ = 116–144): Escalas y saltos diatónicos en 24 Tonalidades + D.S. al Fine (100 compases, págs. 8–9 y 8 articulaciones)." data-en="7 Exercices Journaliers pour la Flûte, Op. 5 — No. 4 in 4/4 (♩ = 116–144): Diatonic scales and leaps across 24 Keys + D.S. al Fine (100 measures, pp. 8–9, and 8 articulations).">7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 4 en 4/4 (♩ = 116–144): Escalas y saltos diatónicos en 24 Tonalidades + D.S. al Fine (100 compases, págs. 8–9 y 8 articulaciones).</td>
            <td>PDF / ABC / Web</td>
            <td><a href="downloads/pdf/reichert_r4_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/reichert_r4_completo.abc" download>ABC (8 Arts.)</a> · <a href="r4.html">Visor</a></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">🎹 M. A. Reichert — Op. 5 Nº 5 (R. 5 · Schott 20623)</td>
            <td class="i18n" data-es="7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 5 en 2/4 Tresillos (♪ = 144–184): Diseño en tresillos de semicorchea en 24 Tonalidades + D.S. al Fine (200 compases, págs. 10–13 y 10 articulaciones)." data-en="7 Exercices Journaliers pour la Flûte, Op. 5 — No. 5 in 2/4 Triplets (♪ = 144–184): Sixteenth-note triplet patterns across 24 Keys + D.S. al Fine (200 measures, pp. 10–13, and 10 articulations).">7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 5 en 2/4 Tresillos (♪ = 144–184): Diseño en tresillos de semicorchea en 24 Tonalidades + D.S. al Fine (200 compases, págs. 10–13 y 10 articulaciones)."</td>
            <td>PDF / ABC / Web</td>
            <td><a href="downloads/pdf/reichert_r5_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/reichert_r5_completo.abc" download>ABC (10 Arts.)</a> · <a href="r5.html">Visor</a></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">📘 Método Completo de Modos (84 Modos Paralelos)</td>
            <td class="i18n" data-es="Compendio íntegro de 36 páginas con las 12 tónicas y sus 7 modos paralelos del Maestro León Giraldo." data-en="Complete 36-page compendium covering all 12 tonics and 7 parallel modes by Maestro León Giraldo.">Compendio íntegro de 36 páginas con las 12 tónicas y sus 7 modos paralelos del Maestro León Giraldo.</td>
            <td>PDF (7.0 MB)</td>
            <td><a href="downloads/pdf/metodo_completo_modos_flauta.pdf" download>📥 Descargar PDF Maestro</a></td>
          </tr>
```

#### After (Lines 1057–1085):
```html
          <tr>
            <td style="font-weight: 700; color: #fff;">🎵 M. A. Reichert — Op. 5 Nº 1 (R. 1 · Schott 20623)</td>
            <td class="i18n" data-es="7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 1 en 6/8 (♩. = 80–100): 24 Tonalidades Mayores y Menores + D.S. al Fine (100 compases, págs. 2–3 y 10 articulaciones)." data-en="7 Exercices Journaliers pour la Flûte, Op. 5 — No. 1 in 6/8 (♩. = 80–100): 24 Major & Minor Keys + D.S. al Fine (100 measures, pp. 2–3, and 10 articulations).">7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 1 en 6/8 (♩. = 80–100): 24 Tonalidades Mayores y Menores + D.S. al Fine (100 compases, págs. 2–3 y 10 articulaciones).</td>
            <td>PDF / ABC / Web</td>
            <td><a href="downloads/pdf/reichert_r1_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/Reichert_R1_Coleccion_Completa.abc" download>ABC (10 Arts.)</a> · <a href="r1.html">Visor</a></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">🎶 M. A. Reichert — Op. 5 Nº 2 (R. 2 · Schott 20623)</td>
            <td class="i18n" data-es="7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 2 en 2/4 (♩ = 120–152): Arpegios modulantes con anacrusa en 24 Tonalidades + D.S. al Fine (200 compases, págs. 4–5 y 8 articulaciones)." data-en="7 Exercices Journaliers pour la Flûte, Op. 5 — No. 2 in 2/4 (♩ = 120–152): Modulating arpeggios with pickup across 24 Keys + D.S. al Fine (200 measures, pp. 4–5, and 8 articulations).">7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 2 en 2/4 (♩ = 120–152): Arpegios modulantes con anacrusa en 24 Tonalidades + D.S. al Fine (200 compases, págs. 4–5 y 8 articulaciones).</td>
            <td>PDF / ABC / Web</td>
            <td><a href="downloads/pdf/reichert_r2_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/Reichert_R2_Coleccion_Completa.abc" download>ABC (8 Arts.)</a> · <a href="r2.html">Visor</a></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">🎼 M. A. Reichert — Op. 5 Nº 4 (R. 4 · Schott 20623)</td>
            <td class="i18n" data-es="7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 4 en 4/4 (♩ = 116–144): Escalas y saltos diatónicos en 24 Tonalidades + D.S. al Fine (100 compases, págs. 8–9 y 8 articulaciones)." data-en="7 Exercices Journaliers pour la Flûte, Op. 5 — No. 4 in 4/4 (♩ = 116–144): Diatonic scales and leaps across 24 Keys + D.S. al Fine (100 measures, pp. 8–9, and 8 articulations).">7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 4 en 4/4 (♩ = 116–144): Escalas y saltos diatónicos en 24 Tonalidades + D.S. al Fine (100 compases, págs. 8–9 y 8 articulaciones).</td>
            <td>PDF / ABC / Web</td>
            <td><a href="downloads/pdf/reichert_r4_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/Reichert_R4_Coleccion_Completa.abc" download>ABC (8 Arts.)</a> · <a href="r4.html">Visor</a></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">🎹 M. A. Reichert — Op. 5 Nº 5 (R. 5 · Schott 20623)</td>
            <td class="i18n" data-es="7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 5 en 2/4 Tresillos (♪ = 144–184): Diseño en tresillos de semicorchea en 24 Tonalidades + D.S. al Fine (200 compases, págs. 10–13 y 10 articulaciones)." data-en="7 Exercices Journaliers pour la Flûte, Op. 5 — No. 5 in 2/4 Triplets (♪ = 144–184): Sixteenth-note triplet patterns across 24 Keys + D.S. al Fine (200 measures, pp. 10–13, and 10 articulations).">7 Exercices Journaliers pour la Flûte, Op. 5 — Nº 5 en 2/4 Tresillos (♪ = 144–184): Diseño en tresillos de semicorchea en 24 Tonalidades + D.S. al Fine (200 compases, págs. 10–13 y 10 articulaciones)."</td>
            <td>PDF / ABC / Web</td>
            <td><a href="downloads/pdf/reichert_r5_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/Reichert_R5_Coleccion_Completa.abc" download>ABC (10 Arts.)</a> · <a href="r5.html">Visor</a></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">📘 Método Completo de Modos (84 Modos Paralelos)</td>
            <td class="i18n" data-es="Compendio íntegro de 36 páginas con las 12 tónicas y sus 7 modos paralelos del Maestro León Giraldo." data-en="Complete 36-page compendium covering all 12 tonics and 7 parallel modes by Maestro León Giraldo.">Compendio íntegro de 36 páginas con las 12 tónicas y sus 7 modos paralelos del Maestro León Giraldo.</td>
            <td>PDF (7.0 MB) / ABC</td>
            <td><a href="downloads/pdf/metodo_completo_modos_flauta.pdf" download>📥 Descargar PDF Maestro</a> · <a href="downloads/abc/00_Coleccion_Completa_84_Modos_EJ4.abc" download>ABC (84 Modos)</a></td>
          </tr>
```

---

### Specification 2: Filesystem Operations
Execute from workspace root `/Users/sebas/Desktop/partituras`:

```bash
# DEF-07: Copy Master Modal ABC Collection into docs/downloads/abc/ and workspace root
cp abc_modos/00_Coleccion_Completa_84_Modos_EJ4.abc docs/downloads/abc/00_Coleccion_Completa_84_Modos_EJ4.abc
cp abc_modos/00_Coleccion_Completa_84_Modos_EJ4.abc 00_Coleccion_Completa_84_Modos_EJ4.abc

# DEF-06: Create lowercase aliases in docs/downloads/abc/ for backwards compatibility
cp docs/downloads/abc/Reichert_R1_Coleccion_Completa.abc docs/downloads/abc/reichert_r1_completo.abc
cp docs/downloads/abc/Reichert_R2_Coleccion_Completa.abc docs/downloads/abc/reichert_r2_completo.abc
cp docs/downloads/abc/Reichert_R4_Coleccion_Completa.abc docs/downloads/abc/reichert_r4_completo.abc
cp docs/downloads/abc/Reichert_R5_Coleccion_Completa.abc docs/downloads/abc/reichert_r5_completo.abc
```

---

### Specification 3: `build_reichert_outputs.py` Hardening
**Target File:** `/Users/sebas/Desktop/partituras/build_reichert_outputs.py`  
**Lines 205–213:**

#### Before (Lines 205–213):
```python
        collection_text = "\n\n".join(all_tunes)
        with open(os.path.join(ABC_DL_DIR, f"Reichert_{code}_Coleccion_Completa.abc"), "w", encoding="utf-8") as f:
            f.write(collection_text)

        # Write root_abc_name (original Urtext + all articulations) to workspace & artifacts
        for dst in [os.path.join(WORKSPACE, root_abc_name), os.path.join(ARTIFACT_DIR, root_abc_name)]:
            with open(dst, "w", encoding="utf-8") as f:
                f.write(collection_text)
```

#### After (Lines 205–214):
```python
        collection_text = "\n\n".join(all_tunes)
        with open(os.path.join(ABC_DL_DIR, f"Reichert_{code}_Coleccion_Completa.abc"), "w", encoding="utf-8") as f:
            f.write(collection_text)
        with open(os.path.join(ABC_DL_DIR, root_abc_name), "w", encoding="utf-8") as f:
            f.write(collection_text)

        # Write root_abc_name (original Urtext + all articulations) to workspace & artifacts
        for dst in [os.path.join(WORKSPACE, root_abc_name), os.path.join(ARTIFACT_DIR, root_abc_name)]:
            with open(dst, "w", encoding="utf-8") as f:
                f.write(collection_text)
```
*(This ensures that whenever `build_reichert_outputs.py` is re-run during DEF-01 fixes, both TitleCase and lowercase files are written directly into `docs/downloads/abc/`).*

---

## 6. Verification and Acceptance Criteria

### Automated Test Command
Run from workspace root:
```bash
python3 -m unittest \
  tests.test_tier3_combinations.TestTier3Combinations.test_c07_web_portal_navigation_links_integrity \
  tests.test_tier3_combinations.TestTier3Combinations.test_c08_web_portal_download_links_casing_integrity \
  tests.test_tier3_combinations.TestTier3Combinations.test_c09_web_portal_apk_download_link_validity \
  tests.test_tier3_combinations.TestTier3Combinations.test_c10_master_modal_collection_abc_presence
```
**Expected Result:** `Ran 4 tests ... OK` (0 failures, 0 errors).

### Complete Link Integrity Command
```bash
python3 -c "
import os, glob
from html.parser import HTMLParser
from urllib.parse import urlparse

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for attr, val in attrs:
            if attr in ('href', 'src'):
                self.links.append((tag, attr, val, self.getpos()))

docs_dir = '/Users/sebas/Desktop/partituras/docs'
html_files = sorted(glob.glob(os.path.join(docs_dir, '*.html')))
broken = []

for filepath in html_files:
    fname = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    parser = LinkExtractor()
    parser.feed(content)
    for tag, attr, val, pos in parser.links:
        v = (val or '').strip()
        if not v or v.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', '#')):
            continue
        parsed = urlparse(v)
        target = os.path.normpath(os.path.join(os.path.dirname(filepath), parsed.path))
        if not os.path.exists(target):
            broken.append((fname, pos[0], tag, attr, v, target))

if broken:
    print(f'FAILED: {len(broken)} broken links detected:')
    for b in broken:
        print(f'  {b[0]}:{b[1]} <{b[2]} {b[3]}=\"{b[4]}\"> -> {b[5]}')
    exit(1)
else:
    print('SUCCESS: 100% of links across all docs/*.html resolve to valid files!')
"
```
**Expected Result:** `SUCCESS: 100% of links across all docs/*.html resolve to valid files!`
