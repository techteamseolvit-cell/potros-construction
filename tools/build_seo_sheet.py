"""Builds the copy-paste SEO sheet (docs/seo-audit/ficha-seo.md + .html) and a proposed sitemap from the generated pages."""
import html, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DOCS = os.path.join(ROOT, 'docs'); SITE = 'https://potrosconstruction.com'
AUDIT = {a['url'].replace(SITE, ''): a for a in json.load(open(os.path.join(DOCS, 'seo-audit', 'audit-data.json')))}
PAGES = [  # path, keyword, status
    ('/', 'custom hardscapes Winchester VA', 'Rediseñada'),
    ('/hardscapes-winchester-va/', 'hardscapes Winchester VA', 'Rediseñada'),
    ('/patios-winchester-va/', 'patios Winchester VA', 'Rediseñada'),
    ('/decks-winchester-va/', 'deck builder Winchester VA', 'Rediseñada'),
    ('/porches-winchester-va/', 'porch builders Winchester VA', 'Rediseñada'),
    ('/fireplaces-winchester-va/', 'outdoor fireplaces Winchester VA', 'Rediseñada'),
    ('/landscaping-winchester-va/', 'landscaping Winchester VA', 'Rediseñada'),
    ('/pools-winchester-va/', 'pool decks Winchester VA', 'NUEVA'),
    ('/about-us/', 'Potros Construction Winchester VA', 'Rediseñada'),
    ('/contact-us/', 'contact Potros Construction', 'Rediseñada'),
    ('/portfolio/', 'hardscape projects Winchester VA', 'NUEVA'),
    ('/reviews/', 'Potros Construction reviews', 'Rediseñada'),
    ('/service-area/', 'hardscapes near Winchester VA', 'Rediseñada'),
    ('/faq/', 'hardscape questions Winchester VA', 'Rediseñada'),
    ('/hardscapes-winchester-va-guide/', 'hardscape cost Winchester VA', 'Rediseñada'),
    ('/privacy-policy/', '—', 'Rediseñada'), ('/terms-and-conditions/', '—', 'Rediseñada'),
]


def g(rx, t, flags=re.S):
    m = re.search(rx, t, flags); return html.unescape(m.group(1)).strip() if m else ''


rows = []
for path, kw, status in PAGES:
    f = os.path.join(DOCS, path.strip('/'), 'index.html') if path != '/' else os.path.join(DOCS, 'index.html')
    t = open(f, encoding='utf-8').read()
    ld = g(r'<script type="application/ld\+json">(.*?)</script>', t).replace(SITE + '/assets/', 'https://techteamseolvit-cell.github.io/potros-construction/docs/assets/')
    rows.append({'path': path, 'url': SITE + path, 'kw': kw, 'status': status, 'title': g(r'<title>(.*?)</title>', t), 'desc': g(r'name="description" content="(.*?)"', t),
                 'h1': re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', g(r'<h1[^>]*>(.*?)</h1>', t))), 'ogimg': g(r'property="og:image" content="(.*?)"', t).replace(SITE + '/assets/', 'https://techteamseolvit-cell.github.io/potros-construction/docs/assets/'),
                 'ld': ld, 'old_title': AUDIT.get(path, {}).get('title', '—'), 'old_h1': (AUDIT.get(path, {}).get('h1') or ['—'])[0] if isinstance(AUDIT.get(path, {}).get('h1'), list) else AUDIT.get(path, {}).get('h1', '—')})


def snippet(r):
    return f'''<title>{html.escape(r['title'])}</title>
<meta name="description" content="{html.escape(r['desc'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{r['url']}">
<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(r['title'])}"><meta property="og:description" content="{html.escape(r['desc'])}"><meta property="og:url" content="{r['url']}"><meta property="og:image" content="{r['ogimg']}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{r['ld']}
</script>'''


md = ['# Ficha SEO — Potros Construction (copiar y pegar)', '',
      'Una ficha por página, en el orden del sitemap. Pega el bloque `<head>` (o cada campo por separado en tu plugin SEO). **Todos los bloques ya traen `index,follow`**; los HTML del preview llevan `noindex` a propósito y hay que quitarlo al publicar.', '',
      'Reglas: no cambies el slug; un solo H1 por página; title ≤ 60 caracteres y meta ≤ 155; si tu plugin SEO ya genera canonical/Open Graph, no los dupliques.', '']
for r in rows:
    md += [f"## {r['path']}  —  {r['status']}", '', f"- **URL:** {r['url']}", f"- **Palabra clave principal:** {r['kw']}", f"- **Title ({len(r['title'])}):** {r['title']}",
           f"- **Meta description ({len(r['desc'])}):** {r['desc']}", f"- **H1:** {r['h1']}", f"- **Imagen para compartir (og:image):** {r['ogimg']}",
           f"- **Title actual del sitio:** {r['old_title']}", '', '```html', snippet(r), '```', '']
open(os.path.join(DOCS, 'seo-audit', 'ficha-seo.md'), 'w', encoding='utf-8').write('\n'.join(md))

cards = ''
for i, r in enumerate(rows):
    def field(label, val, n=None):
        c = f' <small>({len(val)})</small>' if n else ''
        return f'<div class="f"><label>{label}{c}</label><div class="v"><span id="v{i}{abs(hash(label))%9999}">{html.escape(val)}</span><button type="button" data-copy>Copiar</button></div></div>'
    cards += f'''<section class="c"><h2>{html.escape(r['path'])} <em class="{'new' if r['status']=='NUEVA' else ''}">{r['status']}</em></h2>
<p class="u">{r['url']} · clave: <b>{html.escape(r['kw'])}</b></p>
{field('Title', r['title'], 1)}{field('Meta description', r['desc'], 1)}{field('H1', r['h1'])}{field('og:image', r['ogimg'])}
<div class="f"><label>Bloque &lt;head&gt; completo (title, meta, canonical, Open Graph y schema)</label><div class="v"><pre>{html.escape(snippet(r))}</pre><button type="button" data-copy>Copiar</button></div></div>
<p class="o">Title actual del sitio: {html.escape(r['old_title'])}</p></section>'''
page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Ficha SEO | Potros Construction</title>
<style>:root{{--bg:#0a0a0a;--fg:#f2f2f2;--mu:#a0a0a0;--ln:rgba(255,255,255,.14);--red:#b00000}}@media(prefers-color-scheme:light){{:root{{--bg:#fff;--fg:#111;--mu:#555;--ln:rgba(0,0,0,.15)}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif;-webkit-font-smoothing:antialiased}}main{{max-width:980px;margin:0 auto;padding:32px 16px 80px}}
h1{{font-size:30px;margin:0 0 8px}}.lead{{color:var(--mu);max-width:70ch}}.c{{border:1px solid var(--ln);border-radius:16px;padding:20px;margin:22px 0}}h2{{font-size:20px;margin:0 0 4px}}h2 em{{font-style:normal;font-size:12px;background:var(--ln);border-radius:99px;padding:2px 10px;margin-left:8px}}h2 em.new{{background:var(--red);color:#fff}}
.u,.o{{color:var(--mu);font-size:14px;margin:4px 0 14px}}label{{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mu);margin:12px 0 4px}}small{{text-transform:none}}
.v{{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--ln);border-radius:10px;padding:10px 12px}}.v span,.v pre{{flex:1;margin:0;white-space:pre-wrap;word-break:break-word;font:14px/1.5 ui-monospace,Consolas,monospace}}.v pre{{max-height:220px;overflow:auto}}
button{{flex:none;min-height:44px;min-width:76px;border:0;border-radius:8px;background:var(--red);color:#fff;font:600 13px system-ui;cursor:pointer}}button.ok{{background:#1a7f37}}</style></head><body><main>
<h1>Ficha SEO</h1><p class="lead">Una ficha por página, en el orden del sitemap. Cada campo se copia con un clic. Los bloques ya traen <b>index,follow</b>; los HTML del preview llevan noindex a propósito y hay que quitarlo al publicar. No cambies los slugs.</p>{cards}</main>
<script>document.addEventListener('click',function(e){{var b=e.target.closest('[data-copy]');if(!b)return;var s=b.parentNode.querySelector('span,pre');navigator.clipboard.writeText(s.textContent).then(function(){{b.textContent='Copiado';b.classList.add('ok');setTimeout(function(){{b.textContent='Copiar';b.classList.remove('ok')}},1400)}})}});</script></body></html>'''
open(os.path.join(DOCS, 'seo-audit', 'ficha-seo.html'), 'w', encoding='utf-8').write(page)

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + [f"  <url><loc>{r['url']}</loc></url>" for r in rows if r['path'] not in ('/privacy-policy/', '/terms-and-conditions/')] + ['</urlset>']
open(os.path.join(DOCS, 'seo-audit', 'sitemap-propuesto.xml'), 'w', encoding='utf-8').write('\n'.join(sm))
print(len(rows), 'fichas')
