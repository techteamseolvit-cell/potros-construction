"""About Us + Contact Us generator (shares nav/footer/head with build_service.py).
Run:  python3 tools/build_pages.py   ->  docs/about-us/index.html, docs/contact-us/index.html
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_service as bs
from build_service import e, img_path, nav, footer, head, SITE, PHONE, PHONE_HREF, TI_ID, CITIES, VERSION, LIVE_SERVICES, DOCS

EMAIL = 'potrosconstruction@gmail.com'
MAPS = 'https://www.google.com/maps/search/?api=1&query=704+Baker+Ln+Ste+5+Winchester+VA+22603'

LB = '<div class="lb" id="lb" hidden><button class="lb__x" id="lbX" aria-label="Close">×</button><button class="lb__n lb__n--p" id="lbP" aria-label="Previous">←</button><img id="lbImg" alt=""><button class="lb__n" id="lbN" aria-label="Next">→</button></div>'


def hero(h1, lead, photo, alt, crumb, chips, cta=True):
    lis = ''.join(f'<li><b>0{i + 1}</b>{e(c)}</li>' for i, c in enumerate(chips))
    btns = f'<div class="sp-hero__cta"><a class="btn" href="../contact-us/">Get a free estimate</a><a class="sp-call" href="tel:{PHONE_HREF}">Call {PHONE}</a></div>' if cta else ''
    return f'''<section class="sp-hero pg-hero" aria-labelledby="sp-h1">
  <div class="sp-hero__bg" aria-hidden="true"><img src="{photo if photo.startswith('../') else img_path(photo)}" alt="" width="1800" height="750" fetchpriority="high" decoding="async"></div>
  <div class="sp-hero__shade" aria-hidden="true"></div>
  <div class="wrap sp-hero__in">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span>/</span><b aria-current="page">{e(crumb)}</b></nav>
    <h1 id="sp-h1" class="sp-h1">{e(h1)}</h1>
    <p class="sp-hero__lead">{e(lead)}</p>
    {btns}
  </div>
  <div class="sp-hero__strip"><ul class="wrap" style="--cols:{len(chips)}" aria-label="At a glance">{lis}</ul></div>
</section>'''


def reviews():
    return f'''<section class="reviews" id="reviews" aria-labelledby="reviews-title">
  <div class="wrap">
    <div class="reviews__head"><div><p class="eyebrow"><span class="dot"></span> Reviews</p>
      <h2 id="reviews-title" class="h2">What our clients <em>say about us.</em></h2></div><a class="btn" href="../reviews/">Read all reviews</a></div>
    <div class="reviews__widget" id="reviewsWidget" data-trustindex="{TI_ID}"><noscript><p>Our customer reviews are shown here. Enable JavaScript to view them, or visit our <a href="../reviews/">reviews page</a>.</p></noscript></div>
  </div>
</section>'''


def area(title='Proudly Serving Winchester, VA and Nearby Communities'):
    cities = ''.join(f'<li>{e(c)}</li>' for c in CITIES)
    return f'''<section class="sp-area" aria-labelledby="area-h2">
  <div class="wrap sp-area__grid">
    <div class="rv"><p class="eyebrow"><span class="dot"></span> Service area</p><h2 id="area-h2" class="h2">{e(title)}</h2></div>
    <div class="rv"><ul class="area__list">{cities}</ul><p class="sp-area__note">Also servicing Loudoun County, Virginia.</p></div>
  </div>
</section>'''


def steps(items):
    li = ''.join(f'<li class="sp-step rv"><span class="sp-step__dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(items))
    return f'<ol class="sp-steps">{li}</ol>'


def page(title, desc, url, og, schema, body, cls, current):
    return head(title, desc, url, og, json.dumps(schema, ensure_ascii=False, indent=1)) + f'''
<body class="sp {cls}">
<a class="skip" href="#main">Skip to content</a>
<div class="progress" id="progress" aria-hidden="true"></div>
{nav(current)}
<main id="main">
{body}
</main>
{footer()}
{LB}
<script src="../js/service.js?v={VERSION}"></script>
</body>
</html>
'''


def crumbs_schema(name, url):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': name, 'item': url}]}


# ───────────────────────── ABOUT ─────────────────────────
def about():
    url = SITE + '/about-us/'
    values = [('Work honestly', 'Clear scopes, straight answers and a written schedule before work begins. No surprises on the site or on the invoice.'),
              ('Treat others with respect', 'Your home, your time and your budget come first. Our crew leaves every property as clean as it was found.'),
              ('Take pride in everything we do', 'From the base under a paver to the last cap on a wall, the details nobody sees are the ones we care about most.')]
    trust = [('Licensed & insured', 'Fully licensed and insured for all residential work in Virginia.'),
             ('Free on-site estimates', 'We visit, listen and review goals, materials and project details with you.'),
             ('Workmanship warranties', 'Every project is backed by our workmanship warranty and manufacturer guarantees.'),
             ('Locally owned', 'A family-run company based in Winchester, building where we live.')]
    vals = ''.join(f'<li class="rv"><b>0{i + 1}</b><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(values))
    tr = ''.join(f'<li class="rv"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in trust)
    svc = ''.join(f'<a class="pg-svc" href="../{s}-winchester-va/"><span>{l}</span><i aria-hidden="true">→</i></a>' for s, l in LIVE_SERVICES)
    body = f'''
{hero('About Us', 'A family-owned outdoor construction company in Winchester, Virginia, building patios, walkways and stone work with honesty, respect and pride.', '../assets/about/hero.webp', 'Potros Construction branded clipboard, blueprints, tape measure and tools on a builders workbench', 'About Us', ['Family owned', 'Licensed & insured', 'Free estimates', 'Warranted work'])}

<section class="sp-intro pg-story" aria-labelledby="story-h2">
  <div class="wrap sp-intro__grid">
    <div class="rv">
      <p class="eyebrow"><span class="dot"></span> Our story</p>
      <h2 id="story-h2" class="h2">The Potros Family Story</h2>
    </div>
    <div class="rv sp-intro__text">
      <p class="sp-quote">Success isn’t just measured by what we create, but by the trust we earn along the way.</p>
      <p class="sp-p">Potros Construction began as a family business with a simple idea: build outdoor spaces the way we would want them built at our own homes. That means honest conversations, careful craftsmanship and a finished project that holds up season after season.</p>
      <p class="sp-p">Today we design and build hardscapes and outdoor living spaces for homeowners across Winchester and the surrounding communities. We are still hands-on with every job, and we still treat every client like a neighbour.</p>
    </div>
  </div>
</section>

<section class="pg-video" aria-labelledby="vid-h2">
  <div class="wrap">
    <div class="pg-center rv"><p class="eyebrow"><span class="dot"></span> Watch</p><h2 id="vid-h2" class="h2">See how we <em>build.</em></h2></div>
    <div class="about__video pg-video__frame rv" id="filmFrame" data-yt="MiFIxfJCo3g">
      <div class="about__thumb" aria-hidden="true"></div>
      <button class="about__play" id="filmPlay" aria-label="Play the Potros Construction video"><i></i></button>
      <span class="about__cap">Watch Potros Construction</span>
    </div>
  </div>
</section>

<section class="pg-band" aria-label="Recent work">
  <div class="wrap pg-band__grid rv">
    <figure class="sp-dip sp-dip--a"><img src="{img_path('curved-stone-wall')}" alt="Curved natural stone wall over a flagstone patio built by Potros Construction" loading="lazy" decoding="async" width="1100" height="1467"></figure>
    <figure class="sp-dip sp-dip--b"><img src="{img_path('lit-stone-column')}" alt="Lit natural stone column on a flagstone patio" loading="lazy" decoding="async" width="1100" height="1467"></figure>
    <figure class="sp-dip"><img src="{img_path('paver-patio-dining')}" alt="Large paver patio with outdoor dining table beside a home" loading="lazy" decoding="async" width="1100" height="1467"></figure>
  </div>
</section>

<section class="pg-values" aria-labelledby="val-h2">
  <div class="wrap">
    <div class="pg-center rv"><p class="eyebrow"><span class="dot"></span> What we stand for</p><h2 id="val-h2" class="h2">Three promises behind <em>every project.</em></h2></div>
    <ol class="pg-values__list">{vals}</ol>
  </div>
</section>

<section class="pg-trust" aria-labelledby="trust-h2">
  <div class="wrap">
    <h2 id="trust-h2" class="sr">Why homeowners choose Potros Construction</h2>
    <ul class="pg-trust__list">{tr}</ul>
  </div>
</section>

<section class="sp-process" aria-labelledby="proc-h2">
  <div class="wrap">
    <p class="eyebrow rv"><span class="dot"></span> How we work</p>
    <h2 id="proc-h2" class="h2 rv">From first visit to <em>finished space.</em></h2>
    {steps([('In-Person Estimate', 'We visit your home, discuss your project, and take measurements.'), ('3D Virtual Design', 'See your project in a realistic 3D virtual tour before we start.'), ('Build & Enjoy', 'Our team brings your approved design to life with quality craftsmanship.')])}
  </div>
</section>

<section class="pg-svcs" aria-labelledby="svc-h2">
  <div class="pg-svcs__bg" aria-hidden="true"><img src="{img_path('pool-deck-aerial')}" alt="" loading="lazy" decoding="async"></div>
  <div class="wrap sp-intro__grid pg-svcs__in">
    <div class="rv"><p class="eyebrow"><span class="dot"></span> What we build</p><h2 id="svc-h2" class="h2">Outdoor construction, done properly.</h2></div>
    <div class="rv">{svc}</div>
  </div>
</section>

{reviews()}
{area()}

<section class="cta" aria-labelledby="cta-title">
  <div class="cta__bg" aria-hidden="true"><img src="{img_path('patio-firepit-chairs')}" alt="" loading="lazy" decoding="async"></div>
  <div class="wrap cta__in">
    <p class="eyebrow"><span class="dot"></span> Let’s build together</p>
    <h2 id="cta-title" class="cta__title">Let’s talk about <em>your outdoor space.</em></h2>
    <div class="cta__row"><a class="btn" href="../contact-us/">Get your free estimate</a><a class="cta__tel" href="tel:{PHONE_HREF}">Call {PHONE}</a></div>
  </div>
</section>'''
    schema = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'AboutPage', '@id': url + '#page', 'url': url, 'name': 'About Potros Construction',
         'about': {'@type': 'GeneralContractor', '@id': SITE + '/#business', 'name': 'Potros Construction LLC', 'telephone': '+1-540-514-8725'}},
        crumbs_schema('About Us', url)]}
    return page('About Us | Potros Construction, Winchester VA',
                'Meet Potros Construction, a family-owned outdoor construction company in Winchester, VA. Licensed, insured and committed to honest, quality work.',
                url, SITE + '/assets/about/hero.webp', schema, body, 'pg-about', 'about')


# ───────────────────────── CONTACT ─────────────────────────
def contact():
    url = SITE + '/contact-us/'
    def dd(name, label, items, placeholder, required=False):
        lis = ''.join(f'<li role="option" tabindex="-1" data-v="{e(v)}">{e(v)}</li>' for v in items)
        return (f'<div class="pg-f"><span class="pg-f__l" id="l-{name}">{label}</span><div class="dd" data-dd>'
                f'<input type="hidden" name="{name}"><button type="button" class="dd__btn" aria-haspopup="listbox" aria-expanded="false" aria-labelledby="l-{name}">'
                f'<span class="dd__v" data-ph="{placeholder}">{placeholder}</span><i aria-hidden="true"></i></button>'
                f'<ul class="dd__list" role="listbox" aria-labelledby="l-{name}" hidden>{lis}</ul></div></div>')
    city_dd = dd('city', 'Community', CITIES + ['Other'], 'Select your community')
    svc_dd = dd('service', 'Service', [x[1] for x in bs.SERVICE_INDEX] + ['Not sure yet'], 'Not sure yet')
    body = f'''
{hero('Contact Us Today', 'Tell us about your project and we will schedule a free on-site estimate. Prefer to talk? Call us, we pick up.', '../assets/about/contact-hero.webp', 'Potros Construction office desk with material samples, blueprints and a branded plaque', 'Contact Us', ['Free estimates', 'On-site visit', 'Call or write'], cta=False)}

<section class="pg-contact" aria-labelledby="ct-h2">
  <div class="wrap pg-contact__grid">
    <div class="pg-info rv">
      <p class="eyebrow"><span class="dot"></span> Get in touch</p>
      <h2 id="ct-h2" class="h2">Let’s plan <em>your project.</em></h2>
      <dl class="pg-details">
        <div><dt>Call</dt><dd><a href="tel:{PHONE_HREF}">{PHONE}</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        <div><dt>Visit</dt><dd><a href="{MAPS}" target="_blank" rel="noopener">704 Baker Ln, Suite 5<br>Winchester, VA 22603</a></dd></div>
        <div><dt>Hours</dt><dd>Mon – Sat · 8:00 AM – 6:00 PM<br>Sunday closed</dd></div>
      </dl>
    </div>
    <form class="pg-form rv" id="estimateForm" novalidate>
      <h3 class="pg-form__t">Request a free estimate</h3>
      <div class="pg-row">
        <label><span>Name</span><input name="name" autocomplete="name" required></label>
        <label><span>Phone</span><input name="phone" type="tel" autocomplete="tel" required></label>
      </div>
      <label><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
      <div class="pg-row">
        {city_dd}
        {svc_dd}
      </div>
      <label><span>Tell us about your project</span><textarea name="message" rows="4" required></textarea></label>
      <input class="pg-hp" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn pg-send" type="submit"><span>Send request</span><i aria-hidden="true">→</i></button>
      <p class="pg-form__note" id="formNote" role="status">We will get back to you as soon as we can. Your details are only used to answer your request.</p>
    </form>
  </div>
</section>

<section class="sp-process pg-next" aria-labelledby="next-h2">
  <div class="wrap">
    <p class="eyebrow rv"><span class="dot"></span> What happens next</p>
    <h2 id="next-h2" class="h2 rv">Three simple steps, <em>no pressure.</em></h2>
    {steps([('We get back to you', 'A member of our family team reaches out to talk through your ideas and set a time.'), ('We visit your home', 'We walk the property, take measurements and review materials and options together.'), ('You get a clear plan', 'A detailed proposal and schedule, with a 3D design so you can see it before we build.')])}
  </div>
</section>

'''
    schema = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'ContactPage', '@id': url + '#page', 'url': url, 'name': 'Contact Potros Construction',
         'mainEntity': {'@type': 'GeneralContractor', '@id': SITE + '/#business', 'name': 'Potros Construction LLC', 'telephone': '+1-540-514-8725', 'email': EMAIL,
                        'address': {'@type': 'PostalAddress', 'streetAddress': '704 Baker Ln, Suite 5', 'addressLocality': 'Winchester', 'addressRegion': 'VA', 'postalCode': '22603', 'addressCountry': 'US'}}},
        crumbs_schema('Contact Us', url)]}
    return page('Contact Us | Potros Construction, Winchester VA',
                'Contact Potros Construction in Winchester, VA for a free on-site estimate. Call (540) 514-8725 or send your project details online.',
                url, SITE + '/assets/about/contact-hero.webp', schema, body, 'pg-contact-page', 'contact')


def main():
    for slug, fn in (('about-us', about), ('contact-us', contact)):
        out = os.path.join(DOCS, slug)
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(fn())
        print('built', out)


if __name__ == '__main__':
    main()
