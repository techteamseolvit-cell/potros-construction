"""FAQ, Reviews, Service area, Blog (+ guide post), Portfolio, Privacy and Terms pages.
Run: python3 tools/build_content.py   (text comes from tools/data/original-content2.json, the current site's copy)"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_service as bs
import build_pages as bp
from build_service import e, img_path, SITE, PHONE, PHONE_HREF, CITIES, DOCS, SERVICES, LIVE_SERVICES
from build_pages import hero, reviews, area, steps, page, crumbs_schema
from services_more import SERVICES_MORE, FAQS
SERVICES.update(SERVICES_MORE)

O = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'original-content2.json'), encoding='utf-8'))
GBUSINESS = {'@type': 'GeneralContractor', '@id': SITE + '/#business', 'name': 'Potros Construction LLC', 'telephone': '+1-540-514-8725'}


def cta(title, eyebrow='Let’s build together', photo='patio-firepit-chairs', button='Get your free estimate'):
    return f'''<section class="cta" aria-labelledby="cta-title">
  <div class="cta__bg" aria-hidden="true"><img src="{img_path(photo)}" alt="" loading="lazy" decoding="async"></div>
  <div class="wrap cta__in">
    <p class="eyebrow"><span class="dot"></span> {e(eyebrow)}</p>
    <h2 id="cta-title" class="cta__title">{title}</h2>
    <div class="cta__row"><a class="btn" href="../contact-us/">{e(button)}</a><a class="cta__tel" href="tel:{PHONE_HREF}">Call {PHONE}</a></div>
  </div>
</section>'''


def write(slug, content):
    out = os.path.join(DOCS, slug); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(content)
    print('built', slug)


def schema(*parts):
    return {'@context': 'https://schema.org', '@graph': list(parts)}


# ───────────── FAQ ─────────────
def faq():
    url = SITE + '/faq/'
    items = ''.join(f'<details class="sp-faq__i"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQS)
    svc = ''.join(f'<a class="pg-svc pg-svc--s" href="../{s}-winchester-va/"><span>{l}</span><i aria-hidden="true">→</i></a>' for s, l in LIVE_SERVICES)
    body = f'''
{hero('Frequently Asked Questions', 'Clear answers about our services, estimates, timelines and warranties. Can’t find yours? Call us and we’ll help.', 'hero/faq', '', 'FAQ', ['Free estimates', 'Licensed & insured', 'Clear schedules', 'Warranted work'])}
<section class="sp-faq pg-faq" aria-labelledby="faq-h2">
  <div class="wrap sp-faq__grid">
    <div class="rv"><p class="eyebrow"><span class="dot"></span> Questions & answers</p><h2 id="faq-h2" class="h2">Hardscape Questions Answered</h2>
      <p class="lede">Still have a question? Call <a class="sp-inline" href="tel:{PHONE_HREF}">{PHONE}</a> or send us your project details.</p></div>
    <div class="sp-faq__list rv">{items}</div>
  </div>
</section>
<section class="pg-svcs pg-svcs--plain" aria-labelledby="svc-h2">
  <div class="wrap sp-intro__grid">
    <div class="rv"><p class="eyebrow"><span class="dot"></span> Our services</p><h2 id="svc-h2" class="h2">Explore what we build</h2></div>
    <div class="rv">{svc}</div>
  </div>
</section>
{cta('Have a project in <em>mind?</em>')}'''
    sch = schema({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQS]}, crumbs_schema('FAQ', url))
    write('faq', page(O['faq']['title'], O['faq']['desc'], url, SITE + '/assets/hero/faq.webp', sch, body, 'pg-faqpage', 'faq'))


# ───────────── Reviews ─────────────
def reviews_page():
    url = SITE + '/reviews/'
    body = f'''
{hero('Customer Reviews', 'Real feedback from homeowners across Winchester and the surrounding communities.', 'hero/reviews', '', 'Reviews', ['Local homeowners', 'Real reviews', 'Verified source'])}
<section class="sp-video pg-testi" aria-labelledby="testi-h2">
  <div class="wrap">
    <div class="sp-video__head rv"><p class="eyebrow"><span class="dot"></span> Video testimonial</p><h2 id="testi-h2" class="h2">Hear it from <em>our clients.</em></h2>
      <p class="lede">Homeowners in Front Royal, VA share their experience working with Potros Construction.</p></div>
    <div class="sp-video__frame rv"><video controls preload="none" playsinline poster="../assets/video/testimonial-front-royal-poster.webp" aria-label="Video testimonial from Front Royal, VA homeowners"><source src="../assets/video/testimonial-front-royal.mp4" type="video/mp4"></video></div>
  </div>
</section>
<section class="reviews pg-reviews" id="reviews" aria-labelledby="reviews-title">
  <div class="wrap">
    <div class="pg-center rv"><p class="eyebrow"><span class="dot"></span> Reviews</p><h2 id="reviews-title" class="h2">A Word From Our <em>Happy Customers</em></h2></div>
    <div class="reviews__widget" id="reviewsWidget" data-trustindex="{bs.TI_ID}"><noscript><p>Enable JavaScript to see our customer reviews.</p></noscript></div>
  </div>
</section>
{cta('Ready to be our next <em>happy customer?</em>')}'''
    sch = schema({'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': 'Customer Reviews', 'about': GBUSINESS},
                 {'@type': 'VideoObject', 'name': 'Video testimonial from Front Royal, VA homeowners', 'description': 'Homeowners in Front Royal, VA share their experience working with Potros Construction.',
                  'thumbnailUrl': SITE + '/assets/video/testimonial-front-royal-poster.webp', 'contentUrl': SITE + '/assets/video/testimonial-front-royal.mp4', 'uploadDate': '2026-11-09', 'duration': 'PT2M3S'},
                 crumbs_schema('Reviews', url))
    write('reviews', page(O['reviews']['title'], O['reviews']['desc'], url, SITE + '/assets/hero/reviews.webp', sch, body, 'pg-reviewspage', 'reviews'))


# ───────────── Service area ─────────────
def service_area():
    url = SITE + '/service-area/'
    body = f'''
{hero('Service Areas', 'Proudly building outdoor spaces in Winchester, Virginia and the surrounding communities.', 'hero/service-area', '', 'Service Area', ['Virginia', 'West Virginia', 'Loudoun County'])}
{area('Our Satisfied Winchester, VA Area Clients Are Our Main Priority')}
<section class="pg-svcs pg-svcs--plain" aria-labelledby="svc-h2">
  <div class="wrap sp-intro__grid">
    <div class="rv"><p class="eyebrow"><span class="dot"></span> What we build</p><h2 id="svc-h2" class="h2">Every service, across the area</h2></div>
    <div class="rv">{''.join(f'<a class="pg-svc pg-svc--s" href="../{s}-winchester-va/"><span>{l}</span><i aria-hidden="true">→</i></a>' for s, l in LIVE_SERVICES)}</div>
  </div>
</section>
{cta('Not sure we serve your <em>neighborhood?</em>', photo='p2/stone-pillar-walkway-plantings', button='Ask us')}'''
    sch = schema({'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': 'Service Areas'},
                 dict(GBUSINESS, areaServed=[c if 'WV' in c else f'{c}, VA' for c in CITIES]), crumbs_schema('Service Area', url))
    write('service-area', page(O['service-area']['title'], O['service-area']['desc'], url, SITE + '/assets/hero/service-area.webp', sch, body, 'pg-areapage', 'area'))


# ───────────── Blog + guide ─────────────
G_SLUG = 'hardscapes-winchester-va-guide'


def blog():
    url = SITE + '/blog/'
    g = O[G_SLUG]
    body = f'''
{hero('Hardscape & Outdoor Living Blog', 'Insights from Potros Construction on hardscapes, decks, patios and fireplaces in Winchester, VA.', 'hero/blog', '', 'Blog', ['Hardscapes', 'Patios', 'Decks', 'Fireplaces'], cta=False)}
<section class="pg-blog" aria-labelledby="blog-h2">
  <div class="wrap">
    <h2 id="blog-h2" class="sr">Latest articles</h2>
    <a class="pg-post" href="../{G_SLUG}/">
      <figure><img src="{img_path('house-deck-stone-landscape')}" alt="Home with deck, natural stone and landscaped yard in Winchester VA" loading="lazy" decoding="async" width="1100" height="1467"></figure>
      <div><p class="eyebrow"><span class="dot"></span> Guide · March 21, 2025</p>
        <h3>Hardscapes in Winchester, VA — What Homeowners Need to Know</h3>
        <p>{e(g['desc'])}</p><span class="pg-post__more">Read the guide <i aria-hidden="true">→</i></span></div>
    </a>
    <p class="pg-blog__note">More articles on pricing, permits, materials and design ideas are coming soon.</p>
  </div>
</section>
{cta('Planning your <em>next project?</em>')}'''
    sch = schema({'@type': 'Blog', '@id': url + '#blog', 'url': url, 'name': 'Potros Construction Blog', 'publisher': GBUSINESS}, crumbs_schema('Blog', url))
    write('blog', page('Blog | Potros Construction, Hardscapes in Winchester, VA', O['blog']['desc'], url, SITE + '/assets/hero/blog.webp', sch, body, 'pg-blogpage', 'blog'))


def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def guide():
    url = f'{SITE}/{G_SLUG}/'
    g = O[G_SLUG]; items = g['items']
    g = dict(g, desc='Why hardscaping matters in Winchester, VA, popular projects, local costs and how to choose a contractor. Tips before you start.')
    start = next(i for i, (k, _) in enumerate(items) if k == 'h2')
    end = next(i for i, (k, x) in enumerate(items) if k == 'h2' and x == 'Popular Articles')
    toc, art = [], []
    for k, x in items[start:end]:
        if k == 'h2':
            toc.append((2, x)); art.append(f'<h2 id="{slugify(x)}">{e(x)}</h2>')
        elif k == 'h3':
            toc.append((3, x)); art.append(f'<h3 id="{slugify(x)}">{e(x)}</h3>')
        elif x.startswith('Material choiceSize'):
            art.append('<ul>' + ''.join(f'<li>{e(v)}</li>' for v in ['Material choice', 'Size & layout', 'Excavation & site prep', 'Drainage solutions', 'Permits & HOA requirements']) + '</ul>')
        else:
            art.append(f'<p>{e(x)}</p>')
    tocl = ''.join(f'<li class="l{lv}"><a href="#{slugify(t)}">{e(t)}</a></li>' for lv, t in toc)
    body = f'''
{hero(g['items'][0][1], 'Costs, project ideas and contractor tips before you start your hardscape project in Winchester, VA.', 'hero/guide', '', 'Guide', ['Freeze-thaw climate', 'Drainage & grading', 'Costs', 'Choosing a contractor'], cta=False, trail='<span>/</span><a href="../blog/">Blog</a>')}
<article class="pg-article" aria-labelledby="art-h1">
  <div class="wrap pg-article__grid">
    <aside class="pg-toc"><p class="pg-toc__t">In this guide</p><ol>{tocl}</ol></aside>
    <div class="pg-prose"><p class="pg-meta">Published March 21, 2025 · Potros Construction</p>{''.join(art)}</div>
  </div>
</article>
{cta('Ready to plan your <em>hardscape project?</em>', photo='paver-patio-firepit')}'''
    sch = schema({'@type': 'BlogPosting', '@id': url + '#post', 'headline': g['items'][0][1], 'description': g['desc'], 'datePublished': '2025-03-21',
                  'image': SITE + '/assets/hero/guide.webp', 'mainEntityOfPage': url, 'author': {'@type': 'Organization', 'name': 'Potros Construction LLC'}, 'publisher': GBUSINESS},
                 {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'}, {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': SITE + '/blog/'}, {'@type': 'ListItem', 'position': 3, 'name': 'Hardscapes in Winchester, VA guide', 'item': url}]})
    write(G_SLUG, page(g['title'], g['desc'], url, SITE + '/assets/hero/guide.webp', sch, body, 'pg-guidepage', 'blog'))


# ───────────── Legal ─────────────
def legal(slug, name, photo='hero/legal'):
    url = f'{SITE}/{slug}/'; d = O[slug]; out = []
    for k, x in d['items']:
        if k == 'h1': continue
        tag = {'h2': 'h2', 'h3': 'h3', 'h4': 'h3'}.get(k)
        out.append(f'<{tag}>{e(x)}</{tag}>' if tag else (f'<p>{e(x)}</p>' if k == 'p' else f'<p>{e(x)}</p>'))
    h1 = next((x for k, x in d['items'] if k == 'h1'), name)
    body = f'''
{hero(h1, '', photo, '', name, [], cta=False)}
<article class="pg-article pg-article--legal"><div class="wrap"><div class="pg-prose">{''.join(out)}</div></div></article>'''
    sch = schema({'@type': 'WebPage', 'url': url, 'name': name}, crumbs_schema(name, url))
    write(slug, page(d['title'], d['desc'] or f'{name} for Potros Construction LLC.', url, SITE + '/assets/hero/legal.webp', sch, body, 'pg-legalpage', None))


# ───────────── Portfolio ─────────────
CATS = ['Hardscapes', 'Patios', 'Decks', 'Porches', 'Landscaping', 'Fireplaces', 'Pools']


def portfolio():
    url = SITE + '/portfolio/'
    seen, items = set(), []
    for slug in ['pools', 'fireplaces', 'hardscapes', 'patios', 'decks', 'porches', 'landscaping']:
        s = SERVICES[slug]
        photos = [x for b in s['blocks'] for x in b['photos']] + list(s['gallery']) + [s['hero'][0]]
        for n, alt in photos:
            if n not in seen and not n.startswith(('hero/', 'design/')):
                seen.add(n); items.append((n, alt, s['name']))
    def cat_of(n):
        k = n.split('/')[-1]
        if k.startswith('ls-'): return 'Landscaping'
        if 'porch' in k or 'covered' in k: return 'Porches' if 'screened' in k else 'Patios'
        if 'firepit' in k: return 'Fireplaces'
        if 'flagstone' in k: return 'Pools'
        if 'walkway' in k or 'stepping' in k: return 'Landscaping'
        if 'paver' in k: return 'Patios'
        if 'aerial' in k and 'patio' in k: return 'Landscaping'
        if 'deck' in k or 'lake' in k: return 'Decks'
        return 'Aerials'
    for sub in ('p1', 'p2'):
        for f in sorted(os.listdir(os.path.join(DOCS, 'assets', sub))):
            n = f'{sub}/{f[:-5]}'
            if n not in seen:
                seen.add(n); items.append((n, f[:-5].replace('-', ' ').capitalize() + ' by Potros Construction', cat_of(n)))
    DESIGN = ['Aerial 3D design of a deck, patio and fire pit seating wall at night', 'Aerial 3D design of a deck with screened porch and a curved fire pit seating wall', 'Top-down 3D design plan of a deck, patio and seating wall',
              '3D design of a two-level deck with stairs and a stone seating wall', '3D design of a deck, patio and lit stone seating walls at dusk', '3D design of a lit stone seating wall with fire pit and a deck above',
              '3D design of a patio under a deck with steps and bistro seating', '3D design of a covered patio with outdoor kitchen and bar seating', '3D design of a covered patio with a fire pit lounge and TV',
              '3D design of a deck with outdoor dining beside a screened porch', '3D design of a screened porch interior with lounge seating']
    for i, a_ in enumerate(DESIGN, 1):
        items.append((f'design/design-{i:02d}', a_, '3D Design'))
    cats = [c for c in CATS + ['Aerials', '3D Design'] if any(i[2] == c for i in items)]
    chips = '<button class="pf-chip is-on" data-f="all" type="button">All</button>' + ''.join(f'<button class="pf-chip" data-f="{c}" type="button">{c}</button>' for c in cats)
    VIDS = [(1, 'Deck, patio and screened porch'), (2, 'Backyard with outdoor kitchen, pergola and landscaping'), (3, 'Patio with circular fire pit, outdoor kitchen and spa'),
            (4, 'Deck, screened porch and stone fireplace pavilion'), (5, 'Backyard patio with pergola, fire pit and grill island'), (6, 'Covered patio with a stone fireplace'), (7, 'Paver patio with pergola, fire pit and spa')]
    videos = ''.join(f'<figure class="pf-vid rv"><div class="sp-video__frame"><video controls preload="none" playsinline poster="../assets/video/design-{n}-poster.webp" aria-label="3D virtual design walkthrough: {e(lb)}"><source src="../assets/video/design-{n}.mp4" type="video/mp4"></video></div><figcaption>{e(lb)}</figcaption></figure>' for n, lb in VIDS)
    grid = ''.join(f'<figure class="sp-g pf" data-c="{c}"><img src="{img_path(n)}" alt="{e(a)}" loading="lazy" decoding="async" width="1100" height="733"></figure>' for n, a, c in items)
    body = f'''
{hero('Our Portfolio', 'A selection of hardscapes, patios, decks, porches, landscapes and outdoor living spaces built around Winchester, VA.', 'hero/portfolio', '', 'Portfolio', ['Hardscapes', 'Patios & decks', 'Porches', 'Outdoor living'])}
<section class="pg-portfolio" aria-labelledby="pf-h2">
  <div class="wrap">
    <div class="pg-center rv"><p class="eyebrow"><span class="dot"></span> Recent work</p><h2 id="pf-h2" class="h2">Built by <em>Potros Construction.</em></h2></div>
    <div class="pf-chips rv" role="group" aria-label="Filter projects">{chips}</div>
    <div class="pf-grid" id="spGallery">{grid}</div>
  </div>
</section>
<section class="sp-video pg-pfvideo" aria-labelledby="vid-h2">
  <div class="wrap">
    <div class="sp-video__head rv"><p class="eyebrow"><span class="dot"></span> 3D virtual design</p><h2 id="vid-h2" class="h2">From design to <em>finished space.</em></h2>
      <p class="lede">Every project starts with a realistic 3D virtual tour, so you can approve every detail before we break ground.</p></div>
    <div class="pf-videos">{videos}</div>
  </div>
</section>
{reviews()}
{cta('Want results like <em>these?</em>')}'''
    sch = schema({'@type': 'CollectionPage', '@id': url + '#page', 'url': url, 'name': 'Potros Construction Portfolio', 'about': GBUSINESS}, crumbs_schema('Portfolio', url))
    write('portfolio', page('Portfolio | Potros Construction, Winchester VA', 'See hardscapes, patios, decks, porches and outdoor living projects built by Potros Construction in Winchester, VA.',
                            url, SITE + '/assets/hero/portfolio.webp', sch, body, 'pg-portfoliopage', 'portfolio'))


if __name__ == '__main__':
    faq(); reviews_page(); service_area(); blog(); guide(); portfolio()
    legal('privacy-policy', 'Privacy Policy'); legal('terms-and-conditions', 'Terms & Conditions')
