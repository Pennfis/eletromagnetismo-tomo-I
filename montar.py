"""Monta o pacote offline do Tomo I: os sete laboratórios como páginas completas, um índice,
os QR codes provisórios (links dos artefatos) e as figuras do texto."""
import os, re, shutil, zipfile
import qrcode
from PIL import Image, ImageDraw, ImageFont

ROOT = "/home/claude"
OUT = os.path.join(ROOT, "pacote", "tomo-I-eletrostatica")
BASE = os.environ.get("BASE_URL", "https://pennfis.github.io/eletromagnetismo-tomo-I")
LABS = [
    (0, "Escalas e interações", "lab0/laboratorio-escalas.html", "https://claude.ai/artifact/9HT1aCtz8PHN62ihNf3U5e",
     "Escala do macro ao microcosmo, razão entre forças elétrica e gravitacional, neutralidade e corpos esféricos."),
    (1, "Lei de Coulomb e superposição", "lab1/laboratorio-coulomb.html", "https://claude.ai/artifact/38LNyVp9AUtEhUSLJsBPr1",
     "Superposição de forças e medida do expoente da lei de força com incerteza."),
    (2, "Campo elétrico", "lab2/laboratorio-campo.html", "https://claude.ai/artifact/2UFXGU56hSvcFUs7A1B1o5",
     "Vetores e linhas, carga solta que não segue a linha, barra contínua como limite da superposição."),
    (3, "Lei de Gauss no plano", "lab3/laboratorio-gauss.html", "https://claude.ai/artifact/CZY7qHoy1eDrH9ccJhyMHW",
     "Fluxo por superfícies deformáveis, cargas internas e externas, lei de força modificada."),
    (4, "Divergente", "lab4/laboratorio-divergente.html", "https://claude.ai/artifact/17ARgT5Punoz88dk3uehCo",
     "Fluxo por área numa sonda que encolhe, catálogo de campos e distribuição oculta."),
    (5, "Circulação e rotacional", "lab5/laboratorio-circulacao.html", "https://claude.ai/artifact/FAhgHjE7eFP7LWcTG52aUG",
     "Circulação nula, independência do caminho, rotacional local e campo induzido de contraste."),
    (6, "Potencial", "lab6/laboratorio-potencial.html", "https://claude.ai/artifact/ThEzqChJ4yXzqdheQP1TXJ",
     "Equipotenciais, E a partir de V, ponto de sela, equação de Poisson e trabalho."),
]
HEAD_TAGS = re.compile(r"^\s*(<title>.*?</title>|<meta[^>]*>|<link[^>]*>\s*)+", re.S)
RESET = ("<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);"
         "padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,-apple-system,"
         "'Segoe UI',sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>")


def wrap(html):
    m = HEAD_TAGS.match(html)
    head, body = (m.group(0), html[m.end():]) if m else ("", html)
    return ("<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            f"{head}\n{RESET}\n</head>\n<body>\n{body}\n</body>\n</html>\n")


def qr_card(n, title, url, path):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=3)
    q.add_data(url); q.make(fit=True)
    img = q.make_image(fill_color="#17232b", back_color="white").convert("RGB")
    W = img.width
    font_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    card = Image.new("RGB", (W, img.height + 110), "white")
    card.paste(img, (0, 0))
    d = ImageDraw.Draw(card)
    for text, f, y in ((f"Laboratório {n}", font_b, img.height + 8), (title, font, img.height + 52)):
        w = d.textlength(text, font=f)
        d.text(((W - w) / 2, y), text, fill="#17232b", font=f)
    card.save(path)


def index_html():
    items = "\n".join(
        f"<li><a href=\"laboratorios/lab{n}.html\"><span class=\"n\">Laboratório {n}</span>"
        f"<span class=\"t\">{t}</span><span class=\"d\">{d}</span></a></li>" for n, t, _, _, d in LABS)
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Laboratórios do Tomo I</title>
<style>
:root{{--bg:#f3f5f6;--sheet:#fbfcfc;--ink:#17232b;--muted:#5a6a74;--rule:#d3dce1;--accent:#0f6e6a;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0f171c;--sheet:#142028;--ink:#e3ebef;--muted:#93a5b0;--rule:#2a3a44;--accent:#4fc2b8;color-scheme:dark}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;padding:24px max(16px,env(safe-area-inset-left,0px))}}
main{{max-width:760px;margin:0 auto}} h1{{font-family:Georgia,serif;font-size:30px;margin:4px 0 8px}}
.eb{{font:12px ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
p{{color:var(--muted)}} ul{{list-style:none;padding:0;display:grid;gap:10px}}
a{{display:grid;gap:2px;padding:14px 16px;background:var(--sheet);border:1px solid var(--rule);border-radius:6px;color:inherit;text-decoration:none}}
a:hover,a:focus-visible{{border-color:var(--accent)}} .n{{font:12px ui-monospace,monospace;color:var(--accent)}} .t{{font-weight:600}} .d{{font-size:14px;color:var(--muted)}}
</style></head><body><main>
<div class="eb">Eletromagnetismo para a Licenciatura · Tomo I</div>
<h1>Laboratórios do Tomo I: Eletrostática</h1>
<p>Versão para uso sem conexão. Cada laboratório é uma página independente que roda no navegador; sem internet, as fontes tipográficas são substituídas pelas do sistema, sem prejuízo dos cálculos.</p>
<ul>
{items}
</ul>
<p>Licença CC BY-NC-SA 4.0 [confirmar]. Penn Lee Menezes Rodrigues, UEPA. Protótipo v0.1, outubro de 2026.</p>
</main></body></html>
"""


LEIA_ME = """Eletromagnetismo para a Licenciatura, Tomo I: Eletrostática
Pacote para uso sem conexão (protótipo v0.1, outubro de 2026)

Como usar
- Abra index.html em qualquer navegador atual (computador ou celular). Não é preciso instalar nada.
- Cada laboratório em laboratorios/ funciona sozinho e pode ser copiado para os computadores da sala.
- Sem internet, as fontes tipográficas são substituídas pelas do sistema; os cálculos não mudam.

QR codes (pasta qr/)
- Apontam para o endereço permanente no GitHub Pages:
  https://pennfis.github.io/eletromagnetismo-tomo-I/laboratorios/labN.html
- Se o endereço mudar, gere-os de novo com: BASE_URL=<novo endereço> python3 montar.py

Figuras (pasta figuras/)
- Figuras originais do texto do estudante, em SVG (editável) e PNG (2x), prontas para o Canva.

Licença
- CC BY-NC-SA 4.0 [confirmar antes do depósito no eduCAPES].
"""


def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    for sub in ("laboratorios", "qr", "figuras"): os.makedirs(os.path.join(OUT, sub))
    for n, t, src, url, _ in LABS:
        html = open(os.path.join(ROOT, src), encoding="utf-8").read()
        open(os.path.join(OUT, "laboratorios", f"lab{n}.html"), "w", encoding="utf-8").write(wrap(html))
        qr_card(n, t, f"{BASE}/laboratorios/lab{n}.html", os.path.join(OUT, "qr", f"qr-lab{n}.png"))
    for f in os.listdir(os.path.join(ROOT, "figuras")):
        if f.endswith((".svg", ".png")): shutil.copy(os.path.join(ROOT, "figuras", f), os.path.join(OUT, "figuras", f))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(index_html())
    open(os.path.join(OUT, "LEIA-ME.txt"), "w", encoding="utf-8").write(LEIA_ME)
    shutil.copy(__file__, os.path.join(OUT, "montar.py"))
    z = os.path.join(ROOT, "pacote", "tomo-I-eletrostatica.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for base, _, files in os.walk(OUT):
            for f in files:
                p = os.path.join(base, f); zf.write(p, os.path.relpath(p, os.path.dirname(OUT)))
    print("pacote:", z, os.path.getsize(z), "bytes")


if __name__ == "__main__":
    main()
