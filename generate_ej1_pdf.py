import subprocess
import os
import shutil
import fitz

ARTIFACT_DIR = "/Users/sebas/.gemini/antigravity/brain/1df4af97-d9f4-41ae-bad2-2a31fd674ac7"

# 10 Articulaciones en 1 solo pentagrama (plicas hacia arriba, ligaduras/picados debajo, números 1..10 arriba)
ARTICULATIONS_ABC = """X:0
M:none
L:1/16
K:C
V:1 clef=treble stem=up
%%score 1
(DEF"^1"GAGFE) | (DEF"^2"G)(AGFE) | .D(EF"^3"G) .A(GFE) | (DEF)."^4"G (AGF).E | (DE).F."^5"G (AG).F.E | .D.E(F"^6"G) .A.G(FE) | .D(EF)."^7"G .A(GF).E | (DE)(F"^8"G)(AG)(FE) | .D(EF)("^9"GA)(GF)E | .D.E.F."^10"G.A.G.F.E |]"""

# Compás 1 (indentado a la izquierda, con clave de Sol, 4/2 y barra de repetición |:, plicas hacia arriba)
M1_ABC = """X:1
M:4/2
L:1/16
K:C
V:1 clef=treble stem=up
%%score 1
|: DE^FGAGFE DEFGAGFE DEFGAGFE DEFGAGFE |"""

# Página 1: Compases 2 a 14 (13 pentagramas individuales: M.2 a M.10 con plicas arriba, M.11 a M.14 con plicas abajo)
P1_MEASURES = [
    # M.2 (stem=up)
    "D_E=FG_AGFE DEFGAGFE DEFGAGFE DEFGAFED |",
    # M.3 (stem=up)
    "_EFG_A_BAGF EFGABAGF EFGABAGF EFGABAGF |",
    # M.4 (stem=up)
    "^D=E^F^G=AGFE DEFGAGFE DEFGAGFE DEFGAFED |",
    # M.5 (stem=up)
    "E^F^GABAGF EFGABAGF EFGABAGF EFGABAGF |",
    # M.6 (stem=up)
    "E=F=GA_BAGF EFGABAGF EFGABAGF EFGABGFE |",
    # M.7 (stem=up)
    "FGA_BcBAG FGABcBAG FGABcBAG FGABcBAG |",
    # M.8 (stem=up)
    "^E^F^G^A=BAGF EFGABAGF EFGABAGF EFGABGFE |",
    # M.9 (stem=up)
    "^F^G^AB^cBAG FGABcBAG FGABcBAG FGABcBAG |",
    # M.10 (stem=up)
    "^F=G=AB=cBAG FGABcBAG FGABcBAG FGABcAGF |",
    # M.11 (stem=down)
    "GABcdcBA GABcdcBA GABcdcBA GABcdcBA |",
    # M.12 (stem=down)
    "G_A_Bc_dcBA GABcdcBA GABcdcBA GABcdBAG |",
    # M.13 (stem=down)
    "_A_Bc_d_edcB ABcdedcB ABcdedcB ABcdedcB |",
    # M.14 (stem=down)
    "^G=A=B^c=dcBA GABcdcBA GABcdcBA GABcdBAG |",
]

# Página 2: Compases 15 a 24 (10 pentagramas sin 8va, plicas hacia abajo)
P2_MEASURES_LOCO = [
    # M.15
    "AB^cdedcB ABcdedcB ABcdedcB ABcdedcB |",
    # M.16
    "A_B=cd_edcB ABcdedcB ABcdedcB ABcdecBA |",
    # M.17
    "_Bcd_efedc Bcdefedc Bcdefedc Bcdefedc |",
    # M.18
    "^A=B^c^dedcB ABcdedcB ABcdedcB ABcdecBA |",
    # M.19
    "B^c^de^fedc Bcdefedc Bcdefedc Bcdefedc |",
    # M.20
    "B=c=de=fedc Bcdefedc Bcdefedc BcdefdcB |",
    # M.21
    "cdefgfed cdefgfed cdefgfed cdefgfed |",
    # M.22
    "c_d_ef_gfed cdefgfed cdefgfed cdefgedc |",
    # M.23
    "_d_ef_g_agfe defgagfe defgagfe defgagfe |",
    # M.24 (Fin de Reprise à l'octave)
    "^c=d=e^f=gfed cdefgfed cdefgfed cdefgedc :|",
]

# Página 2: Compases 25 a 31 (6 pentagramas con línea punteada 8va, plicas hacia abajo)
P2_MEASURES_8VA = [
    # M.25
    "de^fgagfe defgagfe defgagfe defgagfe |",
    # M.26
    "d_e=fg_agfe defgagfe defgagfe defgafed |",
    # M.27
    "_efg_a_bagf efgabagf efgabagf efgabagf |",
    # M.28
    "^d=e^f^g=agfe defgagfe defgagfe defgafed |",
    # M.29
    "e^f^gabagf efgabagf efgabagf efgabagf |",
    # M.30 + M.31
    "e=f=ga_bagf efgabagf efgabagf efgabgfe | f4 z4 z8 |]",
]

def make_staff_abc(idx, notes_line):
    stem_dir = "up" if idx <= 10 else "down"
    return f"""X:{idx}
M:none
L:1/16
K:C
V:1 clef=treble stem={stem_dir}
%%score 1
{notes_line}"""

def generate_html():
    p1_divs = []
    p1_scripts = []
    for i, m_str in enumerate(P1_MEASURES, start=2):
        div_id = f"m{i}-score"
        p1_divs.append(f'      <div id="{div_id}" class="staff-row"></div>')
        abc_code = make_staff_abc(i, m_str)
        p1_scripts.append(f'  ABCJS.renderAbc("{div_id}", {repr(abc_code)}, staffOptions);')

    p2_divs = []
    p2_scripts = []
    for i, m_str in enumerate(P2_MEASURES_LOCO, start=15):
        div_id = f"m{i}-score"
        p2_divs.append(f'      <div id="{div_id}" class="staff-row p2-row"></div>')
        abc_code = make_staff_abc(i, m_str)
        p2_scripts.append(f'  ABCJS.renderAbc("{div_id}", {repr(abc_code)}, staffOptions);')

    for offset, m_str in enumerate(P2_MEASURES_8VA):
        i = 25 + offset
        div_id = f"m{i}-score"
        is_last = (i == 30)
        extra_cls = "octava-last" if is_last else "octava-full"
        hook_html = '<span class="octava-hook"></span>' if is_last else ''
        p2_divs.append(f'''      <div class="staff-row p2-row octava-wrap {extra_cls}">
        <div class="octava-line"><span class="octava-num">8</span><span class="octava-dots"></span>{hook_html}</div>
        <div id="{div_id}"></div>
      </div>''')
        abc_code = make_staff_abc(i, m_str)
        p2_scripts.append(f'  ABCJS.renderAbc("{div_id}", {repr(abc_code)}, staffOptions);')

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<title>E. J. 1 — Taffanel & Gaubert (A.L. 16.588)</title>
<script src="./abcjs-basic-min.js"></script>
<style>
  @page {{
    size: A4 portrait;
    margin: 5mm 7mm 5mm 7mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: "Times New Roman", "Didot", "Georgia", serif;
    color: #000000;
    margin: 0;
    padding: 0;
    background: #ffffff;
    -webkit-print-color-adjust: exact;
  }}
  .sheet-page {{
    width: 196mm;
    height: 286mm;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    padding: 1mm 1mm 0mm 1mm;
  }}
  .sheet-page:last-child {{
    page-break-after: avoid;
  }}

  /* Encabezado original Leduc */
  .leduc-top {{
    width: 100%;
    margin-bottom: 1px;
  }}
  .ej-title {{
    font-family: "Arial Narrow", "Helvetica Neue", sans-serif;
    font-size: 16pt;
    font-weight: 800;
    letter-spacing: 0.6px;
    margin: 0 0 3px 4px;
  }}
  .ej-subtitle {{
    font-family: "Times New Roman", "Georgia", serif;
    font-size: 9.8pt;
    letter-spacing: 0.4px;
    margin: 0 0 2px 4px;
    color: #000000;
  }}

  /* Números 1..10 en serif clásico */
  .abcjs-annotation {{
    font-family: "Times New Roman", "Didot", Georgia, serif !important;
    font-size: 11.5px !important;
    font-weight: normal !important;
  }}

  /* Pentagrama de las 10 articulaciones */
  .art-row {{
    width: 100%;
    margin-bottom: 1px;
  }}

  /* Compás 1 indentado con Reprise à l'octave */
  .m1-container {{
    position: relative;
    padding-left: 36px;
    width: 100%;
    margin-top: 3px;
  }}
  .reprise-label {{
    position: absolute;
    top: -6px;
    left: 74px;
    font-family: "Times New Roman", "Georgia", serif;
    font-size: 8.8pt;
    font-style: italic;
    font-weight: bold;
    letter-spacing: 0.2px;
    z-index: 10;
  }}

  .staves-block {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex: 1;
    width: 100%;
  }}

  .staff-row {{
    width: 100%;
    margin: 0;
    padding: 0;
    line-height: 1;
  }}

  .staff-row svg, .art-row svg {{
    display: block;
    width: 100% !important;
    height: auto !important;
  }}

  /* Línea 8va estilo Leduc */
  .octava-wrap {{
    position: relative;
  }}
  .octava-line {{
    position: absolute;
    top: -2px;
    left: 32px;
    right: 2px;
    display: flex;
    align-items: flex-start;
    z-index: 10;
    pointer-events: none;
  }}
  .octava-last .octava-line {{
    right: 104px;
  }}
  .octava-num {{
    font-family: "Times New Roman", "Didot", serif;
    font-size: 9.5pt;
    font-style: italic;
    font-weight: bold;
    line-height: 1;
    margin-right: 2px;
  }}
  .octava-dots {{
    flex: 1;
    border-top: 1.15px dashed #000000;
    height: 1px;
    margin-top: 4px;
  }}
  .octava-hook {{
    width: 1.3px;
    height: 7px;
    background: #000000;
    margin-top: 4px;
    display: inline-block;
  }}

  .plate-footer {{
    text-align: center;
    font-family: "Times New Roman", serif;
    font-size: 8pt;
    letter-spacing: 0.8px;
    margin-top: 2px;
    color: #000000;
  }}
</style>
</head>
<body>

  <!-- ================= PÁGINA 1 ================= -->
  <div class="sheet-page">
    <div class="leduc-top">
      <div class="ej-title">E. J. 1</div>
      <div class="ej-subtitle">A travailler successivement avec chacune des dix articulations suivantes:</div>
      <div id="art-score" class="art-row"></div>
    </div>

    <div class="staves-block">
      <div class="m1-container staff-row">
        <div class="reprise-label">Reprise à l'octave</div>
        <div id="m1-score"></div>
      </div>
{chr(10).join(p1_divs)}
    </div>

    <div class="plate-footer">A. L. 16.588</div>
  </div>

  <!-- ================= PÁGINA 2 ================= -->
  <div class="sheet-page">
    <div class="staves-block">
{chr(10).join(p2_divs)}
    </div>

    <div class="plate-footer">A. L. 16.588</div>
  </div>

<script>
  const artOptions = {{
    staffwidth: 900,
    paddingtop: 2,
    paddingbottom: 2,
    paddingleft: 0,
    paddingright: 0,
    responsive: "resize"
  }};
  const m1Options = {{
    staffwidth: 855,
    paddingtop: 1,
    paddingbottom: 1,
    paddingleft: 0,
    paddingright: 0,
    responsive: "resize"
  }};
  const staffOptions = {{
    staffwidth: 900,
    paddingtop: 1,
    paddingbottom: 1,
    paddingleft: 0,
    paddingright: 0,
    responsive: "resize"
  }};

  ABCJS.renderAbc("art-score", {repr(ARTICULATIONS_ABC)}, artOptions);
  // Añadir la pequeña ligadura saliente bajo la 8.ª nota (Mi) del compás 9 de articulaciones
  const artSvg = document.querySelector("#art-score svg");
  if (artSvg) {{
    const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
    p.setAttribute("d", "M 800 57 C 804 62, 809 62, 813 57");
    p.setAttribute("stroke", "#000000");
    p.setAttribute("stroke-width", "1.2");
    p.setAttribute("fill", "none");
    artSvg.appendChild(p);
  }}

  ABCJS.renderAbc("m1-score", {repr(M1_ABC)}, m1Options);
{chr(10).join(p1_scripts)}
{chr(10).join(p2_scripts)}
</script>
</body>
</html>"""

def main():
    html_file = "taffanel_ej1_transcripcion.html"
    pdf_file = "taffanel_ej1_transcripcion.pdf"
    with open(html_file, "w") as f:
        f.write(generate_html())
    
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    abs_html = os.path.abspath(html_file)
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        f"file://{abs_html}"
    ]
    subprocess.run(cmd, check=True)
    print(f"Compiled {pdf_file}")

    doc = fitz.open(pdf_file)
    print(f"Total pages: {len(doc)}")
    for i, page in enumerate(doc):
        png_path = os.path.join(ARTIFACT_DIR, f"taffanel_ej1_transcripcion_p{i+1}.png")
        page.get_pixmap(dpi=200).save(png_path)
        print(f"Saved {png_path}")

    shutil.copy(pdf_file, os.path.join(ARTIFACT_DIR, pdf_file))

if __name__ == "__main__":
    main()
