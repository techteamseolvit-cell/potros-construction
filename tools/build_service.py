"""Service-page generator for the Potros Construction redesign.

One template, one data dict per service. Run:  python3 tools/build_service.py [slug ...]
Writes docs/<slug>-winchester-va/index.html (same URL pattern as the current site, so no SEO is lost).
Add a new service by adding an entry to SERVICES (see 'hardscapes').
"""
import html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
VERSION = '20261015w'          # cache-busting for css/js
SITE = 'https://potrosconstruction.com'
PHONE, PHONE_HREF = '(540) 514-8725', '+15405148725'
TI_ID = '585d188595d53198d00608bfd4f'   # Trustindex widget used on the current site

CITIES = ['Winchester', 'Front Royal', 'Strasburg', 'Berryville', 'Stephens City', 'Middletown', 'Clear Brook',
          'Martinsburg, WV', 'Charles Town, WV', 'Ranson, WV', 'Leesburg', 'Ashburn', 'Sterling', 'South Riding',
          'Purcellville', 'Middleburg', 'Hamilton', 'Lovettsville', 'Manassas']

SERVICE_INDEX = [  # slug, label, card photo, one-liner (used by the "other services" block)
    ('hardscapes', 'Hardscapes', 'cards/hardscapes.webp', 'Patios, walkways and retaining walls built to last.'),
    ('patios', 'Patios', 'cards/patios.webp', 'Paver and stone patios for every way you live outside.'),
    ('decks', 'Decks', 'cards/decks.webp', 'Composite and wood decks with precise framing.'),
    ('porches', 'Porches', 'cards/porches.webp', 'Front, covered and screened porches.'),
    ('fireplaces', 'Fireplaces', 'cards/fireplaces.webp', 'Stone and brick outdoor fireplaces.'),
    ('landscaping', 'Landscaping', 'cards/landscaping.webp', 'Beds, grading, sod and mulch, done right.'),
]

SERVICES = {
    'hardscapes': {
        'slug': 'hardscapes', 'name': 'Hardscapes', 'folder': 'hardscapes',
        'title': 'Hardscapes in Winchester VA | Potros Construction',
        'description': 'Custom hardscapes in Winchester, VA: patios, walkways, retaining walls and stone masonry. Free on-site estimates and 3D design from Potros Construction.',
        'h1': 'Top Hardscape Services in Winchester, VA',
        'lead': 'We design and build durable hardscapes, including patios, walkways, and retaining walls, creating beautiful, functional outdoor spaces that last longer.',
        'chips': ['Patios', 'Walkways', 'Retaining walls', 'Stone borders', 'Masonry'],
        'hero': [('patio-firepit-boulders', 'Paver patio with fire pit, boulders and landscaping at a Winchester VA home built by Potros Construction')],
        'intro': {
            'kicker': 'Winchester, VA’s Trusted Hardscape Specialists',
            'h2': 'Hardscapes in Winchester VA Designed for Beauty and Durability',
            'paras': ['Hardscaping is the structural framework of your landscape: the patios, walkways, retaining walls, stone borders and masonry that give an outdoor space its shape and make it usable every day.',
                      'Our hardscaping services in Winchester VA are built to enhance your property with long-lasting, functional, and beautiful outdoor features. Every project begins with a consultation, and we build with premium materials and careful attention to grading, drainage and structure.'],
            'photo': ('patio-firepit-boulders', 'Paver patio with fire pit, boulders and landscaping at a Winchester VA home'),
        },
        'blocks': [
            {'kicker': 'Patios', 'h2': 'Custom Patios Built to Transform Your Outdoor Space',
             'paras': ['A custom patio is one of the most valuable upgrades you can make to your outdoor area. We design each patio for proper drainage and long-term stability, and around the way you actually use the space: dining, lounging, grilling and entertaining.'],
             'bullets': ['Paver and natural stone patios', 'Dining, lounging and grilling zones', 'Drainage and a stable base engineered first'],
             'photos': [('paver-patio-dining', 'Large paver patio with outdoor dining table beside a gray-sided home'),
                        ('paver-patio-steps-wide', 'Paver patio with centered steps and a contrasting paver border')]},
            {'kicker': 'Walkways', 'h2': 'Walkways and Paths That Improve Flow and Functionality',
             'paras': ['Walkways are essential for creating a safe and welcoming outdoor environment. We build paths in brick, pavers, stone, concrete or gravel, with proper grading and a stable base so they stay level and safe through every season.'],
             'bullets': ['Brick, paver, stone, concrete and gravel paths', 'Steps and landings that connect home and yard', 'Clean borders and consistent grading'],
             'photos': [('paver-walkway-grill', 'Curved paver walkway leading around a home with a grill'),
                        ('paver-steps-entry', 'Paver steps and landing at a back-door entry')]},
            {'kicker': 'Retaining walls', 'h2': 'Retaining Walls for Support, Strength, and Landscape Appeal',
             'paras': ['Retaining walls are a powerful addition to any yard, offering structural support while adding style. We build them in stone, concrete block or segmental systems for erosion control, planting beds and curb appeal.'],
             'bullets': ['Natural stone and segmental block walls', 'Erosion control and level terraces', 'Columns, caps and integrated lighting'],
             'photos': [('curved-stone-wall', 'Curved natural stone wall over a flagstone patio'),
                        ('stone-wall-seating-house', 'Stone seating wall with lantern and flagstone patio in front of a farmhouse')]},
        ],
        'gallery_title': 'Hardscape projects',
        'gallery_lead': 'Natural stone, pavers and masonry from recent builds around Winchester and the surrounding communities.',
        'gallery': [('pool-deck-aerial', 'Aerial view of a flagstone pool deck with stone retaining walls'),
                    ('lit-stone-column', 'Lit natural stone column on a flagstone patio'),
                    ('rounded-paver-steps', 'Rounded paver steps with dark cap stones'),
                    ('stone-pillar-wall', 'Stone pillar and wall with accent lighting'),
                    ('paver-patio-firepit', 'Paver patio with fire pit beside a home'),
                    ('flagstone-pool-edge', 'Flagstone pool edge with river rock and plantings'),
                    ('stone-wall-lanterns', 'Stone wall with lantern posts and flagstone patio'),
                    ('lit-stone-steps', 'Natural stone steps with step lighting'),
                    ('house-deck-stone-landscape', 'Home with deck, natural stone and landscaped yard'),
                    ('patio-firepit-chairs', 'Stamped paver patio with fire pit and Adirondack chairs')],
        'value': {'h2': 'Enhance Your Property Value With Professional Hardscaping',
                  'lead': 'High-quality hardscaping dramatically increases curb appeal, improves functionality, and boosts property value. Potros Construction delivers expert craftsmanship, premium materials, and detailed design so your investment looks great and performs for years.',
                  'points': [('Curb appeal', 'Clean lines, quality materials and finishing details that make a first impression.'),
                             ('Usable space', 'Patios, paths and walls that turn unused yard into places you actually live.'),
                             ('Drainage & resale value', 'Proper grading protects your home and adds lasting value.')],
                  'photo': 'pool-deck-aerial'},
        'process': [('In-Person Estimate', 'We visit your home, discuss your project, and take measurements.'),
                    ('3D Virtual Design', 'See your project in a realistic 3D virtual tour before we start.'),
                    ('Build & Enjoy', 'Our team brings your approved design to life with quality craftsmanship.')],
        'faqs': [('What types of construction services does Potros Construction offer?', 'We handle hardscapes, patios, decks, porches, landscaping, outdoor fireplaces, and full outdoor living builds.'),
                 ('Do you provide free estimates for projects?', 'Yes, we offer free on site estimates where we review your goals, materials, and project details.'),
                 ('Are you licensed and insured for residential construction?', 'Yes, Potros Construction is fully licensed and insured for all work we perform in Virginia.'),
                 ('How long do most projects take to complete?', 'Project timelines vary based on design, materials, and site conditions, but we provide a clear schedule before work begins.'),
                 ('Can you help with design ideas and material selection?', 'Absolutely. We guide you through choosing styles, colors, and materials that fit your home and budget.'),
                 ('Do your projects come with any warranties or guarantees?', 'Yes, we offer workmanship warranties on all projects and use materials backed by manufacturer guarantees.')],
        'cta_photo': 'house-deck-stone-landscape',
    },
}

e = html.escape


def img_path(name):
    return f'../assets/hardscapes/{name}.webp'


def nav():
    return f'''<header class="nav" id="nav">
  <a class="nav__logo" href="../" aria-label="Potros Construction, home"><img src="../assets/logo.png" alt="Potros Construction LLC" width="140" height="41"></a>
  <nav class="nav__links" aria-label="Primary">
    <div class="nav__dd">
      <a href="../#services" aria-current="page">Services</a>
      <div class="nav__menu">{''.join(f'<a href="../{s}-winchester-va/">{l}</a>' for s, l, _, _ in SERVICE_INDEX)}</div>
    </div>
    <a href="../#work">Work</a><a href="../#process">Process</a><a href="../#area">Service Area</a>
    <a href="../about-us/">About</a><a href="../#reviews">Reviews</a><a href="../blog/">Blog</a>
  </nav>
  <a class="nav__phone" href="tel:{PHONE_HREF}">{PHONE}</a>
  <a class="btn btn--sm" href="../contact-us/">Free Estimate</a>
  <button class="nav__burger" id="burger" aria-label="Open menu" aria-expanded="false"><i></i><i></i></button>
</header>
<div class="drawer" id="drawer">
  <a href="../#services">Services</a><a href="../#work">Work</a><a href="../#process">Process</a><a href="../#area">Service Area</a>
  <a href="../about-us/">About</a><a href="../#reviews">Reviews</a><a href="../blog/">Blog</a><a href="../contact-us/">Contact</a>
  <a class="drawer__tel" href="tel:{PHONE_HREF}">{PHONE}</a>
</div>'''


def footer():
    return f'''<footer class="footer">
  <div class="wrap footer__grid">
    <div class="footer__brand"><img class="footer__emblem" src="../assets/emblem.png" alt="" width="84" height="93"><div><p class="footer__name"><strong>POTROS</strong><span>Construction LLC</span></p><p class="footer__note">Custom hardscapes and outdoor living in Winchester, VA and surrounding communities.</p></div></div>
    <div><h3>Services</h3>{''.join(f'<a href="../{s}-winchester-va/">{l}</a>' for s, l, _, _ in SERVICE_INDEX)}</div>
    <div><h3>Company</h3><a href="../about-us/">About us</a><a href="../reviews/">Reviews</a><a href="../service-area/">Service area</a><a href="../faq/">FAQ</a><a href="../blog/">Blog</a><a href="../contact-us/">Contact</a></div>
    <div><h3>Visit</h3><address>704 Baker Ln, Suite 5<br>Winchester, VA 22603</address><a href="tel:{PHONE_HREF}">{PHONE}</a><p>Mon–Sat · 8:00 AM – 6:00 PM<br>Sunday closed</p></div>
  </div>
  <div class="wrap footer__bar"><span>© 2026 Potros Construction LLC</span><span><a href="../privacy-policy/">Privacy</a> · <a href="../terms-and-conditions/">Terms</a></span></div>
</footer>'''


def schema(s):
    url = f'{SITE}/{s["slug"]}-winchester-va/'
    graph = [
        {'@type': 'Service', '@id': url + '#service', 'name': f'{s["name"]} in Winchester, VA', 'serviceType': s['name'],
         'description': s['description'], 'url': url,
         'provider': {'@type': 'GeneralContractor', '@id': SITE + '/#business', 'name': 'Potros Construction LLC', 'telephone': '+1-540-514-8725'},
         'areaServed': [c if 'WV' in c else f'{c}, VA' for c in CITIES]},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Services', 'item': SITE + '/#services'},
            {'@type': 'ListItem', 'position': 3, 'name': s['name'], 'item': url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in s['faqs']]},
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)


def render(s):
    url = f'{SITE}/{s["slug"]}-winchester-va/'
    hero, intro, val = s['hero'], s['intro'], s['value']
    others = [x for x in SERVICE_INDEX if x[0] != s['slug']]

    blocks = ''
    for i, b in enumerate(s['blocks']):
        (p1, a1), (p2, a2) = b['photos']
        blocks += f'''
<section class="sp-block{' is-flip' if i % 2 else ''}" id="{e(b['kicker'].lower().replace(' ', '-'))}" aria-labelledby="blk{i}">
  <div class="wrap sp-block__grid">
    <div class="sp-block__photos rv">
      <figure class="sp-arch"><img src="{img_path(p1)}" alt="{e(a1)}" loading="lazy" decoding="async" width="1100" height="1467"></figure>
      <figure class="sp-mini"><img src="{img_path(p2)}" alt="{e(a2)}" loading="lazy" decoding="async" width="1100" height="1467"></figure>
    </div>
    <div class="sp-block__copy rv">
      <p class="sp-kick"><b>0{i + 1}</b><i></i>{e(b['kicker'])}</p>
      <h2 id="blk{i}" class="h2">{e(b['h2'])}</h2>
      {''.join(f'<p class="sp-p">{e(p)}</p>' for p in b['paras'])}
      <ul class="sp-list">{''.join(f'<li>{e(x)}</li>' for x in b['bullets'])}</ul>
    </div>
  </div>
</section>'''

    gallery = ''.join(
        f'<figure class="sp-g rv" data-i="{i}"><img src="{img_path(n)}" alt="{e(a)}" loading="lazy" decoding="async" width="1100" height="1467"></figure>'
        for i, (n, a) in enumerate(s['gallery']))

    points = ''.join(f'<li class="rv"><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in val['points'])
    steps = ''.join(f'<li class="sp-step rv"><span class="sp-step__dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(s['process']))
    faqs = ''.join(f'<details class="sp-faq__i"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in s['faqs'])
    cities = ''.join(f'<li>{e(c)}</li>' for c in CITIES)
    related = ''.join(
        f'<a class="sp-rel" href="../{sl}-winchester-va/"><img src="../assets/{ph}" alt="" loading="lazy" decoding="async" width="900" height="600"><span><b>{lb}</b><i>{ds}</i></span></a>'
        for sl, lb, ph, ds in others)
    chips = ''.join(f'<li><b>0{i + 1}</b>{e(c)}</li>' for i, c in enumerate(s['chips']))

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(s['title'])}</title>
<meta name="description" content="{e(s['description'])}">
<!-- PREVIEW: remove noindex before launch -->
<meta name="robots" content="noindex,nofollow">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0a0a0a">
<meta property="og:type" content="website"><meta property="og:title" content="{e(s['title'])}"><meta property="og:description" content="{e(s['description'])}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/hardscapes/{hero[0][0]}.webp"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/icon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="../assets/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@300;400;500;600;700&display=swap">
<link rel="preload" as="image" href="{img_path(hero[0][0])}" fetchpriority="high">
<link rel="stylesheet" href="../css/styles.css?v={VERSION}">
<link rel="stylesheet" href="../css/service.css?v={VERSION}">
<script type="application/ld+json">
{schema(s)}
</script>
</head>
<body class="sp">
<a class="skip" href="#main">Skip to content</a>
<div class="progress" id="progress" aria-hidden="true"></div>
{nav()}
<main id="main">

<!-- HERO -->
<section class="sp-hero" aria-labelledby="sp-h1">
  <div class="sp-hero__bg" aria-hidden="true"><img src="{img_path(hero[0][0])}" alt="" width="1800" height="1012" fetchpriority="high" decoding="async"></div>
  <div class="sp-hero__shade" aria-hidden="true"></div>
  <div class="wrap sp-hero__in">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span>/</span><a href="../#services">Services</a><span>/</span><b aria-current="page">{e(s['name'])}</b></nav>
    <p class="eyebrow"><span class="dot"></span> {e(s['name'])} · Winchester, VA</p>
    <h1 id="sp-h1" class="sp-h1">{e(s['h1'])}</h1>
    <p class="sp-hero__lead">{e(s['lead'])}</p>
    <div class="sp-hero__cta">
      <a class="btn" href="../contact-us/">Build Your Dream Space Now!</a>
      <a class="sp-call" href="tel:{PHONE_HREF}">Call {PHONE}</a>
    </div>
  </div>
  <div class="sp-hero__strip"><ul class="wrap" aria-label="What we build">{chips}</ul></div>
</section>

<!-- INTRO -->
<section class="sp-intro" aria-labelledby="intro-h2">
  <div class="wrap sp-intro__grid">
    <div class="rv">
      <p class="eyebrow"><span class="dot"></span> {e(intro['kicker'])}</p>
      <h2 id="intro-h2" class="h2">{e(intro['h2'])}</h2>
    </div>
    <div class="rv sp-intro__text">
      <p class="sp-quote">{e(intro['paras'][0])}</p>
      <p class="sp-p">{e(intro['paras'][1])}</p>
    </div>
  </div>
</section>
{blocks}

<!-- GALLERY -->
<section class="sp-gallery" aria-labelledby="gal-h2">
  <div class="wrap">
    <div class="sp-gallery__head rv">
      <div><p class="eyebrow"><span class="dot"></span> Our work</p><h2 id="gal-h2" class="h2">{e(s['gallery_title'])}</h2></div>
      <p class="lede">{e(s['gallery_lead'])}</p>
    </div>
    <div class="sp-gallery__grid" id="spGallery">{gallery}</div>
  </div>
</section>

<!-- VALUE -->
<section class="sp-value" aria-labelledby="val-h2">
  <div class="sp-value__bg" aria-hidden="true"><img src="{img_path(val['photo'])}" alt="" loading="lazy" decoding="async" width="1100" height="1467"></div>
  <div class="wrap sp-value__in">
    <p class="eyebrow rv"><span class="dot"></span> Why it matters</p>
    <h2 id="val-h2" class="h2 rv">{e(val['h2'])}</h2>
    <p class="lede rv">{e(val['lead'])}</p>
    <ul class="sp-points">{points}</ul>
  </div>
</section>

<!-- PROCESS -->
<section class="sp-process" aria-labelledby="proc-h2">
  <div class="wrap">
    <p class="eyebrow rv"><span class="dot"></span> Our process</p>
    <h2 id="proc-h2" class="h2 rv">From first visit to <em>finished space.</em></h2>
    <ol class="sp-steps">{steps}</ol>
  </div>
</section>

<!-- FAQ -->
<section class="sp-faq" aria-labelledby="faq-h2">
  <div class="wrap sp-faq__grid">
    <div class="rv"><p class="eyebrow"><span class="dot"></span> FAQ</p><h2 id="faq-h2" class="h2">Common Questions We Get</h2>
      <p class="lede">Can’t find your answer? Call us at <a class="sp-inline" href="tel:{PHONE_HREF}">{PHONE}</a> and we’ll help.</p></div>
    <div class="sp-faq__list rv">{faqs}</div>
  </div>
</section>

<!-- REVIEWS -->
<section class="reviews" id="reviews" aria-labelledby="reviews-title">
  <div class="wrap">
    <div class="reviews__head"><div><p class="eyebrow"><span class="dot"></span> Reviews</p>
      <h2 id="reviews-title" class="h2">What our clients <em>say about us.</em></h2></div><a class="btn" href="../reviews/">Read all reviews</a></div>
    <div class="reviews__widget" id="reviewsWidget" data-trustindex="{TI_ID}"><noscript><p>Our customer reviews are shown here. Enable JavaScript to view them, or visit our <a href="../reviews/">reviews page</a>.</p></noscript></div>
  </div>
</section>

<!-- AREA -->
<section class="sp-area" aria-labelledby="area-h2">
  <div class="wrap sp-area__grid">
    <div class="rv"><p class="eyebrow"><span class="dot"></span> Service area</p>
      <h2 id="area-h2" class="h2">Our Satisfied Winchester, VA Area Clients Are Our Main Priority</h2></div>
    <div class="rv"><ul class="area__list">{cities}</ul>
      <p class="sp-area__note">Also servicing Loudoun County, Virginia.</p></div>
  </div>
</section>

<!-- OTHER SERVICES -->
<section class="sp-more" aria-labelledby="more-h2">
  <div class="wrap">
    <h2 id="more-h2" class="sp-more__h rv">More outdoor services</h2>
    <div class="sp-more__grid">{related}</div>
  </div>
</section>

<!-- CTA -->
<section class="cta" aria-labelledby="cta-title">
  <div class="cta__bg" aria-hidden="true"><img src="{img_path(s['cta_photo'])}" alt="" loading="lazy" decoding="async"></div>
  <div class="wrap cta__in">
    <p class="eyebrow"><span class="dot"></span> Let’s build</p>
    <h2 id="cta-title" class="cta__title">Ready to take your outdoor space to the <em>next level?</em></h2>
    <div class="cta__row"><a class="btn" href="../contact-us/">Let’s Get Started</a><a class="cta__tel" href="tel:{PHONE_HREF}">Call {PHONE}</a></div>
  </div>
</section>

</main>
{footer()}
<div class="lb" id="lb" hidden><button class="lb__x" id="lbX" aria-label="Close">×</button><button class="lb__n lb__n--p" id="lbP" aria-label="Previous">←</button><img id="lbImg" alt=""><button class="lb__n" id="lbN" aria-label="Next">→</button></div>
<script src="../js/service.js?v={VERSION}"></script>
</body>
</html>
'''


def main(slugs):
    for slug in slugs or SERVICES:
        s = SERVICES[slug]
        out = os.path.join(DOCS, f'{slug}-winchester-va')
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(render(s))
        print('built', out)


if __name__ == '__main__':
    main(sys.argv[1:])
