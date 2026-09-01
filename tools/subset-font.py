"""
Regera o subset da Host Grotesk usado na marca do cabeçalho.

A fonte vai embutida em base64 no bloco CSS de src/GradientMaker.jsx,
então não há requisição de rede — mas o subset só cobre os caracteres
de "gradient maker". Se o nome mudar, rode este script e substitua a
string base64 do @font-face.

    pip install fonttools brotli
    python tools/subset-font.py
"""

import base64
from pathlib import Path
from fontTools.subset import main as subset

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "assets/fonts/HostGrotesk-SemiBold.ttf"
SAIDA = RAIZ / "tools/host-subset.woff2"
TEXTO = "gradient maker"

subset([
    str(ORIGEM),
    f"--text={TEXTO}",
    "--flavor=woff2",
    "--layout-features=*",
    f"--output-file={SAIDA}",
])

b64 = base64.b64encode(SAIDA.read_bytes()).decode()
print(f"{SAIDA.stat().st_size} bytes / {len(b64)} caracteres em base64\n")
print(
    '@font-face{font-family:"Host Grotesk";font-style:normal;font-weight:600;'
    f'font-display:block;src:url(data:font/woff2;base64,{b64}) format("woff2")}}'
)
