"""Self-contained, copy-paste HTML per page -> docs/paste/<slug>.html
Each file has its CSS and JS inline; images/videos use absolute URLs (GitHub Pages assets); links point to the real site URLs."""
import os, re, shutil, sys
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


def encode_scripts(t):
    """WordPress turns '&&' into '&#038;&#038;' and wpautop injects <p>/<br> into inline scripts, which breaks them.
    Each plain inline <script> is re-emitted as one safe line (base64) that rebuilds and runs the original code."""
    import base64
    def enc(m):
        js = m.group(1)
        b64 = base64.b64encode(js.encode('utf-8')).decode()
        return ('<script>(function(){var s=document.createElement("script");s.text=decodeURIComponent(escape(atob("' + b64 + '")));'
                'document.head.appendChild(s);})();</script>')
    return re.sub(r'<script>(.*?)</script>', enc, t, flags=re.S)


def wrap_page(t):
    """Full-bleed wrapper (breaks out of the theme's centered container) + restores the <body> classes the CMS drops."""
    m = re.search(r'<body([^>]*)>', t)
    cls = re.search(r'class="([^"]*)"', m.group(1)).group(1) if m and 'class=' in m.group(1) else ''
    t = re.sub(r'<body[^>]*>', '<body><div class="potros-page">', t, 1)
    t = t.replace('</body>', '</div></body>', 1)
    names = ','.join('"%s"' % c for c in cls.split() if c)
    shim = f'<script>(function(){{var b=document.body;[{names}].forEach(function(c){{b.classList.add(c)}});}})();</script>'
    return t.replace('<div class="potros-page">', '<div class="potros-page">' + shim, 1)


def build(name, linked=False):
    src = 'index.html' if name == 'home' else f'{name}/index.html'
    t = read(src); path = '/' if name == 'home' else f'/{name}/'; base = SITE + path
    css_dir = '' if name == 'home' else '../'

    def css(m):
        c = read('css/' + m.group(1))
        c = re.sub(r'url\((?![\'"]?(?:https?:|data:))([^)]+)\)', lambda x: 'url(' + absolutize(x.group(1).strip('\'"'), SITE + '/css/x.css') + ')', c)
        return f'<style>\n{c}\n</style>'
    if not linked:
        t = re.sub(r'<link rel="stylesheet" href="(?:\.\./)?css/([a-z]+\.css)(?:\?[^"]*)?">', css, t)
        t = re.sub(r'<script src="(?:\.\./)?js/([a-z0-9]+\.js)(?:\?[^"]*)?"></script>', lambda m: f'<script>\n{read("js/" + m.group(1))}\n</script>', t)
    else:
        t = re.sub(r'(href|src)="(?:\.\./)?((?:css|js)/[a-z0-9]+\.(?:css|js))(\?[^"]*)?"', lambda m: f'{m.group(1)}="{ASSETS[:-len("assets/")]}{m.group(2)}{m.group(3) or ""}"', t)
    t = re.sub(r'(?<=\s)(src|href|poster)="([^"]+)"', lambda m: f'{m.group(1)}="{absolutize(m.group(2), base)}"', t)
    t = t.replace(SITE + '/assets/', ASSETS)
    t = t.replace('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="index,follow,max-image-preview:large">')
    t = re.sub(r'<!-- PREVIEW[^>]*-->\n?', '', t)
    t = wrap_page(t)
    if not linked:
        t = encode_scripts(t)
    outdir = os.path.join(OUT, 'linked') if linked else OUT
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, name + '.html'), 'w', encoding='utf-8').write(t)
    return len(t)


if __name__ == '__main__':
    for n in PAGES:
        print(n.ljust(34), build(n) // 1024, 'KB', build(n, True) // 1024, 'KB linked')


def index():
    import zipfile, glob
    for n in PAGES:   # plain-text copy so the HTML can be read in the browser
        shutil.copyfile(os.path.join(OUT, n + '.html'), os.path.join(OUT, n + '.txt'))
    with zipfile.ZipFile(os.path.join(OUT, 'potros-paginas-html.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for n in PAGES: z.write(os.path.join(OUT, n + '.html'), n + '.html')
    rows = ''.join(f'<tr><td><b>{n}</b><br><small>{"/" if n == "home" else "/" + n + "/"}</small></td><td class="a"><button data-f="{n}.html" type="button">Copiar HTML</button><a href="{n}.html" target="_blank" rel="noopener">Ver página</a><a href="{n}.txt" target="_blank" rel="noopener">Ver código</a><a href="{n}.html" download>Descargar</a></td></tr>' for n in PAGES)
    CONCEPT = [('01', 'Patio de pavers con escalones', 'patio-pavers-steps'), ('02', 'Patio bajo el deck', 'patio-under-deck'), ('03', 'Chimenea de piedra', 'fireplace-stone-patio'), ('04', 'Fire pit de piedra', 'firepit-stone-chairs'),
               ('05', 'Muro de contención con césped', 'landscape-retaining-wall'), ('06', 'Camino de pavers al frente', 'landscape-front-walkway'), ('07', 'Piscina desde la casa', 'pool-from-house'), ('08', 'Piscina con muro de piedra', 'pool-stone-wall'),
               ('09', 'Cama lateral con roca', 'landscape-side-bed'), ('10', 'Deck de flagstone en piscina', 'pool-deck-flagstone'), ('11', 'Borde de piscina (detalle)', 'pool-deck-closeup'), ('12', 'Piedras de paso y camas', 'landscape-stepping-stones')]
    imgs = ''.join(f'<figure><img src="../assets/concept/{f}.webp" alt="{t}" loading="lazy"><figcaption>{k} · {t}</figcaption><a href="../assets/concept/{f}.webp" download>Descargar imagen</a></figure>' for k, t, f in CONCEPT)
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>HTML y recursos | Potros Construction</title>
<style>:root{{--bg:#0a0a0a;--fg:#f2f2f2;--mu:#a0a0a0;--ln:rgba(255,255,255,.14);--red:#b00000}}@media(prefers-color-scheme:light){{:root{{--bg:#fff;--fg:#111;--mu:#555;--ln:rgba(0,0,0,.15)}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif;-webkit-font-smoothing:antialiased}}main{{max-width:980px;margin:0 auto;padding:32px 16px 80px}}h1{{font-size:28px;margin:0 0 8px}}h2{{font-size:20px;margin:40px 0 8px}}p{{color:var(--mu);max-width:70ch}}
table{{width:100%;border-collapse:collapse;margin-top:16px}}td{{padding:12px 8px;border-top:1px solid var(--ln);vertical-align:middle}}small{{color:var(--mu)}}.a{{display:flex;gap:6px 14px;flex-wrap:wrap;align-items:center}}a{{color:var(--fg)}}
button,.btn{{min-height:44px;min-width:130px;border:0;border-radius:8px;background:var(--red);color:#fff;font:600 14px system-ui;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;text-decoration:none;padding:0 14px}}button.ok{{background:#1a7f37}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px;margin-top:16px}}figure{{margin:0;border:1px solid var(--ln);border-radius:12px;overflow:hidden;display:grid}}figure img{{width:100%;aspect-ratio:3/2;object-fit:cover;display:block}}figcaption{{padding:8px 12px 0;font-size:14px}}figure a{{padding:6px 12px 12px;font-size:14px}}</style></head><body><main>
<h1>HTML y recursos</h1><p>Cada página es un archivo completo y autocontenido (CSS y JavaScript dentro; imágenes y videos por dirección absoluta). Pulsa <b>Copiar HTML</b>, pega en tu editor y se ve todo. Con <b>Ver código</b> lees el HTML en el navegador; con <b>Descargar</b> bajas el archivo.</p>
<p><a class="btn" href="potros-paginas-html.zip" download>Descargar las 18 páginas (.zip)</a></p>
<p>¿La página se queda en “0 %” o el editor altera el código? Usa la <b>versión ligera</b> (<a href="linked/home.html">ejemplo: home</a>): el CSS y el JavaScript se cargan por enlace en vez de ir dentro del HTML. Misma ruta con <code>linked/NOMBRE.html</code> para cada página.</p>
<table>{rows}</table>
<h2>Imágenes nuevas</h2><p>Descárgalas una por una.</p><div class="g">{imgs}</div></main>
<script>document.addEventListener('click',function(e){{var b=e.target.closest('button[data-f]');if(!b)return;b.textContent='Copiando…';fetch(b.dataset.f).then(function(r){{return r.text()}}).then(function(t){{return navigator.clipboard.writeText(t)}}).then(function(){{b.textContent='¡Copiado!';b.classList.add('ok');setTimeout(function(){{b.textContent='Copiar HTML';b.classList.remove('ok')}},1800)}}).catch(function(){{b.textContent='Error: usa Descargar'}})}});</script></body></html>'''
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)


index()
