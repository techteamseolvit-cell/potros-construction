"""Self-contained, copy-paste HTML per page -> docs/paste/<slug>.html
Each file has its CSS and JS inline; images/videos use absolute URLs (GitHub Pages assets); links point to the real site URLs."""
import os, re, sys
from urllib.parse import urljoin
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DOCS = os.path.join(ROOT, 'docs'); OUT = os.path.join(DOCS, 'paste')
SITE = 'https://potrosconstruction.com'
ASSETS = 'https://techteamseolvit-cell.github.io/potros-construction/docs/assets/'
PAGES = ['home', 'hardscapes-winchester-va', 'patios-winchester-va', 'decks-winchester-va', 'porches-winchester-va', 'fireplaces-winchester-va', 'landscaping-winchester-va', 'pools-winchester-va',
         'about-us', 'contact-us', 'portfolio', 'reviews', 'service-area', 'faq', 'blog', 'hardscapes-winchester-va-guide', 'privacy-policy', 'terms-and-conditions']


def absolutize(u, base):
    if re.match(r'^(https?:|tel:|mailto:|#|data:|javascript:)', u):
        return u
    r = urljoin(base, u)
    path = r[len(SITE):] if r.startswith(SITE) else r
    return ASSETS + path[len('/assets/'):] if path.startswith('/assets/') else r


def read(rel):
    return open(os.path.join(DOCS, rel), encoding='utf-8').read()


def build(name):
    src = 'index.html' if name == 'home' else f'{name}/index.html'
    t = read(src); path = '/' if name == 'home' else f'/{name}/'; base = SITE + path
    css_dir = '' if name == 'home' else '../'

    def css(m):
        c = read('css/' + m.group(1))
        c = re.sub(r'url\((?![\'"]?(?:https?:|data:))([^)]+)\)', lambda x: 'url(' + absolutize(x.group(1).strip('\'"'), SITE + '/css/x.css') + ')', c)
        return f'<style>\n{c}\n</style>'
    t = re.sub(r'<link rel="stylesheet" href="(?:\.\./)?css/([a-z]+\.css)(?:\?[^"]*)?">', css, t)
    t = re.sub(r'<script src="(?:\.\./)?js/([a-z0-9]+\.js)(?:\?[^"]*)?"></script>', lambda m: f'<script>\n{read("js/" + m.group(1))}\n</script>', t)
    t = re.sub(r'(?<=\s)(src|href|poster)="([^"]+)"', lambda m: f'{m.group(1)}="{absolutize(m.group(2), base)}"', t)
    t = t.replace(SITE + '/assets/', ASSETS)
    t = t.replace('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="index,follow,max-image-preview:large">')
    t = re.sub(r'<!-- PREVIEW[^>]*-->\n?', '', t)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8').write(t)
    return len(t)


if __name__ == '__main__':
    for n in PAGES:
        print(n.ljust(34), build(n) // 1024, 'KB')


def index():
    rows = ''.join(f'<tr><td><b>{n}</b><br><small>{"/" if n == "home" else "/" + n + "/"}</small></td><td><button data-f="{n}.html" type="button">Copiar HTML</button> <a href="{n}.html" target="_blank" rel="noopener">Ver</a> <a href="{n}.html" download>Descargar</a></td></tr>' for n in PAGES)
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>HTML para copiar y pegar | Potros Construction</title>
<style>:root{{--bg:#0a0a0a;--fg:#f2f2f2;--mu:#a0a0a0;--ln:rgba(255,255,255,.14);--red:#b00000}}@media(prefers-color-scheme:light){{:root{{--bg:#fff;--fg:#111;--mu:#555;--ln:rgba(0,0,0,.15)}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif;-webkit-font-smoothing:antialiased}}main{{max-width:820px;margin:0 auto;padding:32px 16px 80px}}h1{{font-size:28px;margin:0 0 8px}}p{{color:var(--mu);max-width:68ch}}
table{{width:100%;border-collapse:collapse;margin-top:20px}}td{{padding:12px 8px;border-top:1px solid var(--ln);vertical-align:middle}}small{{color:var(--mu)}}a{{color:var(--fg);margin-left:10px}}
button{{min-height:44px;min-width:130px;border:0;border-radius:8px;background:var(--red);color:#fff;font:600 14px system-ui;cursor:pointer}}button.ok{{background:#1a7f37}}</style></head><body><main>
<h1>HTML para copiar y pegar</h1><p>Cada archivo es una página completa y autocontenida: el CSS y el JavaScript van dentro y las imágenes y videos se cargan desde una dirección absoluta. Pulsa <b>Copiar HTML</b>, pega en tu editor y se ve todo, sin subir nada. Los enlaces internos ya apuntan a las URLs reales del sitio.</p>
<table>{rows}</table></main>
<script>document.addEventListener('click',function(e){{var b=e.target.closest('button[data-f]');if(!b)return;b.textContent='Copiando…';fetch(b.dataset.f).then(function(r){{return r.text()}}).then(function(t){{return navigator.clipboard.writeText(t)}}).then(function(){{b.textContent='¡Copiado!';b.classList.add('ok');setTimeout(function(){{b.textContent='Copiar HTML';b.classList.remove('ok')}},1800)}}).catch(function(){{b.textContent='Error: usa Descargar'}})}});</script></body></html>'''
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)


index()
