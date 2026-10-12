# Handoff Report: DEF-06, DEF-07 & Web Portal Link Audit

**Agent:** `explorer_m1_3`  
**Handoff Type:** Hard (Task Complete)  
**Milestone:** Milestone 1 (Score Engine & Urtext Parity Fixes)  
**Date:** 2026-10-11  
**Recipient:** Caller Orchestrator (`2c224607-5456-4eac-ad55-0172dee3d36d`) / Worker Agents  

---

## 1. Observation

Direct observations obtained during the systematic investigation:

1. **DEF-06: Web Download Links in `docs/index.html`:**
   - File: `/Users/sebas/Desktop/partituras/docs/index.html` lines 1060, 1066, 1072, 1078.
   - Verbatim contents:
     ```html
     1060: <td><a href="downloads/pdf/reichert_r1_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/reichert_r1_completo.abc" download>ABC (10 Arts.)</a> · <a href="r1.html">Visor</a></td>
     1066: <td><a href="downloads/pdf/reichert_r2_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/reichert_r2_completo.abc" download>ABC (8 Arts.)</a> · <a href="r2.html">Visor</a></td>
     1072: <td><a href="downloads/pdf/reichert_r4_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/reichert_r4_completo.abc" download>ABC (8 Arts.)</a> · <a href="r4.html">Visor</a></td>
     1078: <td><a href="downloads/pdf/reichert_r5_transcripcion.pdf" download>📥 PDF</a> · <a href="downloads/abc/reichert_r5_completo.abc" download>ABC (10 Arts.)</a> · <a href="r5.html">Visor</a></td>
     ```
   - Directory contents in `docs/downloads/abc/`:
     Files are named in TitleCase:
     - `Reichert_R1_Coleccion_Completa.abc` (46,543 bytes)
     - `Reichert_R2_Coleccion_Completa.abc` (47,697 bytes)
     - `Reichert_R4_Coleccion_Completa.abc` (46,275 bytes)
     - `Reichert_R5_Coleccion_Completa.abc` (76,443 bytes)
   - Workspace root `/Users/sebas/Desktop/partituras/` contains:
     - `reichert_r1_completo.abc` (46,543 bytes)
     - `reichert_r2_completo.abc` (47,697 bytes)
     - `reichert_r4_completo.abc` (46,275 bytes)
     - `reichert_r5_completo.abc` (76,443 bytes)
   - Command `diff -s` confirmed byte-for-byte identity between `reichert_r{N}_completo.abc` and `Reichert_R{N}_Coleccion_Completa.abc`.
   - Tool execution `python3 -m unittest tests.test_tier3_combinations.TestTier3Combinations.test_c08_web_portal_download_links_casing_integrity` output:
     ```
     FAIL: test_c08_web_portal_download_links_casing_integrity
     AssertionError: Lists differ: ['reichert_r1_completo.abc', 'reichert_r2_completo.abc', 'reichert_r4_completo.abc', 'reichert_r5_completo.abc'] != []
     : DEF-06: Found broken/casing-mismatched download links in docs/index.html: ['reichert_r1_completo.abc', 'reichert_r2_completo.abc', 'reichert_r4_completo.abc', 'reichert_r5_completo.abc']
     ```

2. **DEF-07: Missing Master Modal ABC Collection in `docs/downloads/abc/`:**
   - File: `/Users/sebas/Desktop/partituras/abc_modos/00_Coleccion_Completa_84_Modos_EJ4.abc` exists (32,013 bytes, 1,091 lines, tunes `X:1` to `X:84`).
   - File is completely absent from `docs/downloads/abc/`.
   - In `docs/index.html` lines 1081–1085:
     ```html
     1081: <tr>
     1082:   <td style="font-weight: 700; color: #fff;">📘 Método Completo de Modos (84 Modos Paralelos)</td>
     1083:   <td class="i18n" data-es="Compendio íntegro de 36 páginas con las 12 tónicas y sus 7 modos paralelos del Maestro León Giraldo." data-en="Complete 36-page compendium covering all 12 tonics and 7 parallel modes by Maestro León Giraldo.">Compendio íntegro de 36 páginas con las 12 tónicas y sus 7 modos paralelos del Maestro León Giraldo.</td>
     1084:   <td>PDF (7.0 MB)</td>
     1085:   <td><a href="downloads/pdf/metodo_completo_modos_flauta.pdf" download>📥 Descargar PDF Maestro</a></td>
     1086: </tr>
     ```
   - Tool execution `python3 -m unittest tests.test_tier3_combinations.TestTier3Combinations.test_c10_master_modal_collection_abc_presence` output:
     ```
     FAIL: test_c10_master_modal_collection_abc_presence
     AssertionError: False is not true : DEF-07: 00_Coleccion_Completa_84_Modos_EJ4.abc is missing from docs/downloads/abc/
     ```

3. **Complete Link Audit across `docs/` (All 13 HTML files):**
   - Scanned all 13 HTML files: `ej1.html`, `ej2.html`, `ej4.html`, `ej5.html`, `ej10.html`, `ej11.html`, `index.html`, `privacy.html`, `r1.html`, `r2.html`, `r4.html`, `r5.html`, `support.html`.
   - Total links extracted: 119 links.
     - Internal valid static links: 89
     - Broken static links: 4 (the 4 DEF-06 Reichert links in `index.html`)
     - External links: 16 (all valid URLs and mailto schemas)
     - Internal fragment anchors: 6 (all target IDs `#maestro`, `#preview`, `#features`, `#downloads` exist in `index.html`)
     - Dynamic JavaScript asset references: Verified all `EX_ARTS[...].fname`, `CHROMATIC_ART_LIST[...].file1/file2`, and `modos_${tonicId}.abc` targets against `docs/downloads/abc/` (100% exist).
     - CSS stylesheets & inline style `url()`: 0 broken assets.

---

## 2. Logic Chain

1. **DEF-06 Reasoning:**
   - *Observation 1.1:* `build_reichert_outputs.py` generates `Reichert_R{N}_Coleccion_Completa.abc` into `docs/downloads/abc/` and writes `reichert_r{N}_completo.abc` to workspace root.
   - *Observation 1.2:* `docs/index.html` links to `downloads/abc/reichert_r{N}_completo.abc`.
   - *Inference:* The filename mismatch results in HTTP 404 when clicking Reichert ABC download links.
   - *Conclusion:* Updating `docs/index.html` to point to `downloads/abc/Reichert_R{N}_Coleccion_Completa.abc`, copying `reichert_r{N}_completo.abc` into `docs/downloads/abc/` as an alias, and updating `build_reichert_outputs.py` to write both names ensures complete parity, backwards compatibility, and prevents regressions upon re-running the generator script.

2. **DEF-07 Reasoning:**
   - *Observation 1.3:* `00_Coleccion_Completa_84_Modos_EJ4.abc` exists in `abc_modos/` but not in `docs/downloads/abc/`.
   - *Observation 1.4:* `test_c10_master_modal_collection_abc_presence` explicitly asserts `(WORKSPACE_ROOT / "docs" / "downloads" / "abc" / "00_Coleccion_Completa_84_Modos_EJ4.abc").exists()`.
   - *Observation 1.5:* `docs/index.html` line 1084 offers a PDF download for the Maestro's 84 modes but omits the corresponding complete ABC compendium.
   - *Inference:* Copying `00_Coleccion_Completa_84_Modos_EJ4.abc` into `docs/downloads/abc/` and adding ` · <a href="downloads/abc/00_Coleccion_Completa_84_Modos_EJ4.abc" download>ABC (84 Modos)</a>` satisfies both the automated test and web portal feature parity.

3. **Link Audit Reasoning:**
   - *Observation 1.6:* Exhaustive scanning of all 13 HTML files revealed zero broken links beyond DEF-06.
   - *Inference:* Fixing DEF-06 and DEF-07 completely resolves all link integrity defects across the web ecosystem.

---

## 3. Caveats

- **Read-Only Investigation:** In accordance with the Explorer archetype rules, no source or asset files were modified during this investigation. All specifications are provided as drop-in blocks for Worker execution.
- **Milestone 4 Dependency (Release APK Link):** In `docs/index.html` line 799, the APK download link points to `downloads/apk/FluteModes-v1.5.0-release.apk` (which currently exists on disk). In Milestone 4, this must be bumped to `FluteModes-v1.5.1-release.apk` once the release APK is compiled.
- **No other caveats:** Every link, anchor, stylesheet, and dynamic loader in `docs/` has been verified directly against disk.

---

## 4. Conclusion

The exact technical specifications for the Worker are defined as follows:

1. **Edit `docs/index.html`:**
   - Lines 1060, 1066, 1072, 1078: Change `reichert_r{1,2,4,5}_completo.abc` to `Reichert_R{1,2,4,5}_Coleccion_Completa.abc`.
   - Lines 1083–1084: Update format to `PDF (7.0 MB) / ABC` and add ` · <a href="downloads/abc/00_Coleccion_Completa_84_Modos_EJ4.abc" download>ABC (84 Modos)</a>`.
2. **Execute File Copies:**
   - `cp abc_modos/00_Coleccion_Completa_84_Modos_EJ4.abc docs/downloads/abc/00_Coleccion_Completa_84_Modos_EJ4.abc`
   - `cp abc_modos/00_Coleccion_Completa_84_Modos_EJ4.abc 00_Coleccion_Completa_84_Modos_EJ4.abc`
   - `cp docs/downloads/abc/Reichert_R1_Coleccion_Completa.abc docs/downloads/abc/reichert_r1_completo.abc` (and R2, R4, R5)
3. **Harden `build_reichert_outputs.py`:**
   - Add line 208 to write `root_abc_name` directly to `ABC_DL_DIR`.
4. Detailed specifications and before/after code blocks are documented in `/Users/sebas/Desktop/partituras/.agents/teamwork/explorer_m1_3/analysis.md`.

---

## 5. Verification Method

To independently verify the implementation once applied by the Worker:

1. **Verify E2E Unit Tests:**
   ```bash
   python3 -m unittest \
     tests.test_tier3_combinations.TestTier3Combinations.test_c07_web_portal_navigation_links_integrity \
     tests.test_tier3_combinations.TestTier3Combinations.test_c08_web_portal_download_links_casing_integrity \
     tests.test_tier3_combinations.TestTier3Combinations.test_c09_web_portal_apk_download_link_validity \
     tests.test_tier3_combinations.TestTier3Combinations.test_c10_master_modal_collection_abc_presence
   ```
   *Expected:* `Ran 4 tests in ...s` -> `OK` (0 failures, 0 errors).

2. **Verify Zero Broken Links Across `docs/`:**
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
       print(f'FAILED: {len(broken)} broken links detected: {broken}')
       exit(1)
   else:
       print('SUCCESS: Zero broken links across docs/*.html!')
   "
   ```
   *Expected:* `SUCCESS: Zero broken links across docs/*.html!`
