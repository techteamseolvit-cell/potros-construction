"""Genera el reporte de auditoría SEO (MD, HTML, CSV) desde audit-data.json."""
import json, csv, html, os
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, 'audit-data.json')))
short = lambda u: u.replace('https://potrosconstruction.com', '') or '/'
svc = [r for r in d if r['url'].endswith('-winchester-va/')]

def issues(r):
    i = []
    if r['title_len'] > 60: i.append(('Medio', f"Title de {r['title_len']} caracteres (recomendado ≤60), se corta en Google"))
    if r['desc_len'] == 0: i.append(('Alto', 'Sin meta description'))
    elif r['desc_len'] > 155: i.append(('Bajo', f"Meta description de {r['desc_len']} caracteres (≤155)"))
    if not r['h1']: i.append(('Alto', 'Sin H1'))
    if r['words'] < 300 and 'category' not in r['url']: i.append(('Alto' if r['words'] < 100 else 'Medio', f"Contenido delgado: {r['words']} palabras"))
    if r['img_noalt']: i.append(('Medio', f"{r['img_noalt']} imágenes sin texto alternativo"))
    if not r['schema']: i.append(('Medio', 'Sin datos estructurados (schema)'))
    if 'Lever' in r['typos'] or 'Checkout Out' in r['typos']: i.append(('Medio', 'Errores de texto: "Next Lever" / "Checkout Out Blog"'))
    if 'category' in r['url']: i.append(('Medio', 'Página de categoría "uncategorized" indexable: debe ser noindex o eliminarse'))
    return i

rows = [(short(r['url']), r) for r in d]
all_issues = {u: issues(r) for u, r in rows}
count = lambda lvl: sum(1 for v in all_issues.values() for s, _ in v if s == lvl)

# CSV
with open(os.path.join(here, 'audit-pages.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['URL', 'Status', 'Title', 'Title len', 'Meta desc len', 'H1', 'H2 count', 'Words', 'Images', 'Img sin alt', 'Schema', 'Peso HTML (KB)', 'Hallazgos'])
    for u, r in rows:
        w.writerow([u, r['status'], r['title'], r['title_len'], r['desc_len'], ' | '.join(r['h1']), len(r['h2']), r['words'], r['images'], r['img_noalt'], ', '.join(r['schema']), round(r['bytes'] / 1024), ' ; '.join(f"[{s}] {t}" for s, t in all_issues[u])])

sections = {
 'resumen': [
  'Sitio WordPress (tema YOOtheme) con **15 URLs indexables**: 1 home, 6 servicios, 6 institucionales, 1 blog + 1 post y 1 categoría.',
  'Todas responden **200 OK**, con canonical, Open Graph y viewport. HTML liviano (≈110 KB en servicios) y respuesta rápida (0.25–0.46 s). **La base técnica es sana**.',
  f'Se detectaron **{count("Alto")} incidencias (por página) de prioridad alta, {count("Medio")} medios y {count("Bajo")} bajos**.',
  'El mayor riesgo para el rediseño no es técnico: es **perder las URLs y el contenido que ya posicionan**. El mayor potencial es **expandir páginas por servicio × ciudad**.',
 ],
}
findings = [
 ('Alto', 'Las 6 páginas de servicio comparten ~1.000 palabras casi idénticas', 'Los 6 servicios repiten la misma plantilla (31 imágenes, 11 H2; 5 H2 idénticos en las 6 páginas, además de los mismos bloques de proceso, reseñas, FAQ y blog). Google puede tratarlo como contenido duplicado y no distinguir qué página responde a cada búsqueda.', 'Reescribir cada servicio con contenido único: materiales, proceso, precios orientativos, galería propia, FAQ propio y proyectos reales.'),
 ('Alto', 'Páginas clave con contenido casi vacío', 'Reviews (42 palabras), Contact (54), Blog (75), Service Area (94) y About (170) no ofrecen texto indexable suficiente. Reviews no tiene reseñas visibles.', 'Mostrar reseñas reales con schema Review/AggregateRating, enriquecer About con historia y equipo, y dar a Service Area un contenido por ciudad.'),
 ('Alto', 'Blog sin H1 y con un solo artículo', '/blog/ no tiene H1 y solo existe 1 post (hardscapes-winchester-va-guide). El blog es la principal palanca de tráfico informacional.', 'Añadir H1 y un calendario editorial (precios, permisos, materiales, comparativas, ideas por estación).'),
 ('Alto', 'Cobertura geográfica sin páginas propias', 'Declaran servicio en ~25 ciudades (Winchester, Front Royal, Strasburg, Berryville, Martinsburg, Charles Town, Leesburg, Ashburn, Purcellville, Manassas…) pero solo hay páginas para Winchester, enlistando el resto en texto.', 'Crear páginas servicio × ciudad con contenido local único, como mayor oportunidad de crecimiento orgánico (ver estrategia).'),
 ('Medio', 'Schema incompleto y genérico', 'Solo el home tiene WebSite/Organization/LocalBusiness, y el LocalBusiness trae solo nombre. Faltan dirección, teléfono, horarios, coordenadas, areaServed, logo, sameAs y valoración. Ninguna página de servicio tiene Service, FAQPage o BreadcrumbList.', 'Implementar JSON-LD completo: HomeAndConstructionBusiness/GeneralContractor, Service por página, FAQPage, BreadcrumbList, Review/AggregateRating y Article.'),
 ('Medio', 'Imágenes sin texto alternativo', 'Todas las páginas tienen imágenes sin alt (3–6 por página). Los archivos tienen nombres con errores como "Consctructions".', 'Alt descriptivos con servicio y ciudad, nombres de archivo limpios, WebP/AVIF y dimensiones explícitas.'),
 ('Medio', 'Errores de texto visibles en 7 páginas', '"Next Lever" (por Level) y "Checkout Out Blog" aparecen en el home y en las 6 páginas de servicio.', 'Corregir en el rediseño.'),
 ('Medio', 'Mensaje cruzado entre servicios', 'La página de porches y otras mezclan texto de hardscapes en hero e intro, y el pie describe al negocio como "deck builder".', 'Cada página con un H1 y una intención de búsqueda únicos.'),
 ('Medio', 'Titles largos', f"{sum(1 for r in d if r['title_len'] > 60)} de {len(d)} titles superan 60 caracteres y se truncan en resultados.", 'Reescribir titles ≤60 caracteres con servicio + ciudad + marca.'),
 ('Medio', 'Categoría "uncategorized" indexable', 'La URL /category/uncategorized/ está en el sitemap, sin meta description y sin H1, y duplica contenido del blog.', 'Excluir del sitemap y marcar noindex (o eliminar con 301 a /blog/).'),
 ('Bajo', 'Tres videos de YouTube embebidos en cada servicio', 'Cada página de servicio carga 3 iframes de YouTube, lo que añade peso y JavaScript de terceros.', 'Cargar con facade (lazy) y añadir VideoObject schema; en el rediseño el video principal se conserva.'),
 ('Bajo', 'Enlaces CTA inconsistentes', '/contact-us/ y /contact-us (con y sin slash final) y varios textos de CTA diferentes.', 'Un único patrón de URL y CTAs consistentes.'),
 ('Info', 'robots.txt con Crawl-delay: 10', 'Googlebot ignora Crawl-delay, pero otros rastreadores pueden ralentizarse.', 'Eliminar la directiva; mantener la referencia al sitemap.'),
]
# Estrategia
cities = ['Winchester', 'Front Royal', 'Strasburg', 'Berryville', 'Stephens City', 'Middletown', 'Clear Brook', 'Martinsburg', 'Charles Town', 'Ranson', 'Leesburg', 'Ashburn', 'Sterling', 'South Riding', 'Purcellville', 'Middleburg', 'Hamilton', 'Lovettsville', 'Manassas']
services = ['Hardscapes', 'Patios', 'Decks', 'Porches', 'Fireplaces', 'Landscaping']

# --- Markdown
md = ['# Auditoría SEO — potrosconstruction.com', '', f'*Fecha: 14 oct 2026 · Alcance: 15 URLs del sitemap actual · Método: rastreo directo del HTML público.*', '', '> Línea base antes del rediseño. Sirve como respaldo y como checklist para no perder tráfico orgánico.', '', '## 1. Resumen ejecutivo', '']
md += [f'- {x}' for x in sections['resumen']]
md += ['', '## 2. Inventario de URLs y métricas', '', '| URL | Title (car.) | Meta (car.) | H1 | Palabras | Img sin alt | Schema |', '|---|---|---|---|---|---|---|']
for u, r in rows:
    md.append(f"| `{u}` | {r['title_len']} | {r['desc_len']} | {'✓' if r['h1'] else '✗'} | {r['words']} | {r['img_noalt']}/{r['images']} | {', '.join(r['schema']) or '—'} |")
md += ['', '## 3. Hallazgos priorizados', '']
for lvl, t, why, fix in findings:
    md += [f'### [{lvl}] {t}', '', why, '', f'**Acción:** {fix}', '']
md += ['## 4. Plan para no perder tráfico en el rediseño', '',
 '1. **Mantener las 15 URLs actuales** con el mismo slug. Cualquier cambio de URL lleva redirección 301 uno a uno.',
 '2. **Migrar títulos, H1 y textos que ya posicionan** (los 6 servicios + guía de hardscapes) antes de mejorarlos.',
 '3. **Render en servidor / HTML estático**: contenido y enlaces en el HTML, no solo en JavaScript.',
 '4. **Core Web Vitals en verde**: video y 3D con carga diferida, poster, `prefers-reduced-motion`, imágenes WebP/AVIF.',
 '5. **Schema completo** (GeneralContractor, Service, FAQPage, Review, BreadcrumbList, VideoObject).',
 '6. **Sitemap y robots** nuevos, envío a Search Console y monitoreo semanal de rankings durante 90 días.',
 '7. **Lanzamiento en ventana de bajo tráfico** con checklist de redirecciones validado en staging.', '',
 '## 5. Oportunidad: páginas servicio × ciudad', '',
 f'Hoy existen 6 páginas (todas Winchester). Con {len(services)} servicios × {len(cities)} ciudades de su zona de servicio hay **{len(services)*len(cities)} combinaciones posibles**; se recomienda priorizar por volumen en Search Console y Ahrefs, empezando por Winchester, Front Royal, Martinsburg, Leesburg y Ashburn.', '',
 '**Regla:** cada página debe tener contenido local único (proyectos, materiales, normas del condado, FAQ propio). Las páginas plantilla duplicadas perjudican, no ayudan.', '',
 '## 6. Pendientes de datos (necesitan acceso)', '',
 '- Google Search Console: consultas, clics y posiciones actuales (para definir qué URLs proteger primero).',
 '- Google Analytics: páginas con más tráfico y conversiones.',
 '- Ahrefs/Similarweb: backlinks y competidores (conectores bloqueados en este entorno).',
 '- PageSpeed / Core Web Vitals reales del sitio actual.',
 '- Ficha de Google Business Profile y reseñas.', '',
 '## 7. Metodología y límites', '',
 'Rastreo del HTML servido por el sitio. No incluye rankings, backlinks ni Core Web Vitals de campo, que requieren Search Console y herramientas externas. Los conteos de palabras excluyen scripts, estilos, navegación y pie.']
open(os.path.join(here, 'potros-seo-audit.md'), 'w', encoding='utf-8').write('\n'.join(md))

# --- HTML
e = html.escape
badge = {'Alto': '#b3261e', 'Medio': '#b26a00', 'Bajo': '#2e6b34', 'Info': '#555'}
trs = ''.join(f"<tr><td><code>{e(u)}</code></td><td>{r['title_len']}</td><td>{r['desc_len']}</td><td>{'✓' if r['h1'] else '✗'}</td><td>{r['words']}</td><td>{r['img_noalt']}/{r['images']}</td><td>{e(', '.join(r['schema']) or '—')}</td></tr>" for u, r in rows)
fs = ''.join(f"<article><h3><span style='background:{badge[l]}'>{l}</span>{e(t)}</h3><p>{e(w)}</p><p><b>Acción:</b> {e(f)}</p></article>" for l, t, w, f in findings)
li = lambda items: ''.join(f'<li>{x}</li>' for x in items)
bold = lambda s: s.replace('**', '§').split('§')
def md_inline(s):
    p = bold(e(s)); return ''.join(f'<b>{x}</b>' if i % 2 else x for i, x in enumerate(p))
page = f"""<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Auditoría SEO — Potros Construction</title>
<style>body{{font:15px/1.6 system-ui,sans-serif;max-width:980px;margin:40px auto;padding:0 20px;color:#1a1a1a}}h1{{font-size:32px;margin-bottom:0}}h2{{margin-top:44px;border-bottom:2px solid #c9a24b;padding-bottom:6px}}table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{border:1px solid #ddd;padding:6px 8px;text-align:left}}th{{background:#111;color:#fff}}article{{border:1px solid #e3e3e3;border-radius:8px;padding:6px 16px;margin:12px 0;break-inside:avoid}}h3 span{{color:#fff;font-size:12px;padding:2px 8px;border-radius:99px;margin-right:10px}}.kpi{{display:flex;gap:12px;flex-wrap:wrap}}.kpi div{{flex:1;min-width:140px;background:#f6f2e8;border-radius:10px;padding:12px}}.kpi b{{display:block;font-size:28px}}</style>
<h1>Auditoría SEO — potrosconstruction.com</h1><p>14 oct 2026 · 15 URLs · Línea base previa al rediseño</p>
<div class="kpi"><div><b>15</b>URLs rastreadas</div><div><b>{count('Alto')}</b>incidencias altas</div><div><b>{count('Medio')}</b>incidencias medias</div><div><b>{len(services)*len(cities)}</b>páginas servicio × ciudad posibles</div></div>
<h2>1. Resumen ejecutivo</h2><ul>{li(md_inline(x) for x in sections['resumen'])}</ul>
<h2>2. Inventario de URLs</h2><table><tr><th>URL</th><th>Title</th><th>Meta</th><th>H1</th><th>Palabras</th><th>Img sin alt</th><th>Schema</th></tr>{trs}</table>
<h2>3. Hallazgos priorizados</h2>{fs}
<h2>4. Plan para no perder tráfico</h2><ol>{li(md_inline(x[3:]) for x in md[md.index('## 4. Plan para no perder tráfico en el rediseño')+2:md.index('## 4. Plan para no perder tráfico en el rediseño')+9])}</ol>
<h2>5. Oportunidad: servicio × ciudad</h2><p>{len(services)} servicios × {len(cities)} ciudades = <b>{len(services)*len(cities)}</b> combinaciones. Prioridad inicial: Winchester, Front Royal, Martinsburg, Leesburg, Ashburn. Cada página con contenido local único.</p>
<h2>6. Pendientes de datos</h2><ul><li>Google Search Console y Analytics (consultas, clics, posiciones)</li><li>Ahrefs / Similarweb (backlinks, competidores)</li><li>Core Web Vitals reales (PageSpeed)</li><li>Google Business Profile y reseñas</li></ul></html>"""
open(os.path.join(here, 'potros-seo-audit.html'), 'w', encoding='utf-8').write(page)
print('ok', count('Alto'), count('Medio'), count('Bajo'))
