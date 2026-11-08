"""Service data for Patios, Decks, Porches, Landscaping (Fireplaces pending photos).
Headings and body copy come verbatim from the current site (tools/data/original-content.json);
only bullets, process, value points, photos and CTAs are authored here."""
import json, os, re

_orig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'original-content.json'), encoding='utf-8'))

FAQS = [('What types of construction services does Potros Construction offer?', 'We handle hardscapes, patios, decks, porches, landscaping, outdoor fireplaces, and full outdoor living builds.'),
        ('Do you provide free estimates for projects?', 'Yes, we offer free on site estimates where we review your goals, materials, and project details.'),
        ('Are you licensed and insured for residential construction?', 'Yes, Potros Construction is fully licensed and insured for all work we perform in Virginia.'),
        ('How long do most projects take to complete?', 'Project timelines vary based on design, materials, and site conditions, but we provide a clear schedule before work begins.'),
        ('Can you help with design ideas and material selection?', 'Absolutely. We guide you through choosing styles, colors, and materials that fit your home and budget.'),
        ('Do your projects come with any warranties or guarantees?', 'Yes, we offer workmanship warranties on all projects and use materials backed by manufacturer guarantees.')]
PROCESS = [('In-Person Estimate', 'We visit your home, discuss your project, and take measurements.'),
           ('3D Virtual Design', 'See your project in a realistic 3D virtual tour before we start.'),
           ('Build & Enjoy', 'Our team brings your approved design to life with quality craftsmanship.')]


def _split(text, first=2):
    """Split a long paragraph into two readable ones (by sentences), never altering the words."""
    s = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(s) <= first + 1:
        return [text.strip()]
    return [' '.join(s[:first]), ' '.join(s[first:])]


def _build(slug, name, extra):
    o = _orig[slug]; it = [x for _, x in o['items']]
    h1 = re.sub(r'^Top\s+', '', it[0])
    intro_paras = _split(it[4], 1)
    blocks = []
    for i, (k, bl, photos) in enumerate(extra['blocks']):
        blocks.append({'kicker': k, 'h2': it[5 + 2 * i], 'paras': _split(it[6 + 2 * i], 2), 'bullets': bl, 'photos': photos})
    return {
        'slug': slug, 'name': name, 'folder': 'p1',
        'title': o['title'], 'description': o['desc'], 'h1': h1, 'lead': extra.get('lead', it[2]),
        'chips': extra['chips'], 'hero': [(extra['hero'], extra['hero_alt'])],
        'intro': {'kicker': it[1], 'h2': it[3], 'paras': intro_paras if len(intro_paras) == 2 else [intro_paras[0], ''], 'photo': (extra['hero'], extra['hero_alt'])},
        'blocks': blocks,
        'gallery_title': extra['gallery_title'], 'gallery_lead': extra['gallery_lead'], 'gallery': extra['gallery'],
        'value': {'h2': it[14], 'lead': it[15], 'points': extra['points'], 'photo': extra['value_photo']},
        'process': PROCESS, 'faqs': FAQS, 'cta': extra['cta'], 'video': extra.get('video'),
    }


P = lambda n: 'p1/' + n

_VL = 'Every project starts with a realistic 3D virtual tour, so you can walk through your design and approve every detail before we break ground.'
V1 = {'src': 'video/design-1', 'iso': 'PT1M15S', 'lead': _VL, 'label': '3D virtual design walkthrough of a deck, patio and screened porch'}
V2 = {'src': 'video/design-2', 'iso': 'PT1M43S', 'lead': _VL, 'label': '3D virtual design walkthrough of a backyard with outdoor kitchen, pergola and landscaping'}

_PATIOS = {
    'lead': 'We design and build durable patios in pavers and natural stone, creating beautiful, functional outdoor spaces that last longer.',
    'chips': ['Pavers', 'Natural stone', 'Fire pits', 'Seating walls', 'Lighting'],
    'hero': P('paver-patio-columns'), 'hero_alt': 'Paver patio with stone columns under a covered deck at a Winchester VA home',
    'blocks': [
        ('Materials', ['Pavers, stamped concrete and natural stone', 'Patterns, colors and textures to match your home', 'Premium materials chosen for durability'],
         [(P('paver-patio-diagonal'), 'Paver patio laid in a diagonal pattern beside a stone seating wall'), (P('paver-patio-bistro-border'), 'Paver patio with a dark border and bistro table set')]),
        ('Entertaining', ['Fire pits, seating walls and outdoor kitchens', 'Pergolas and lighting built into the layout', 'Planned around how you live and entertain'],
         [(P('patio-under-deck-covered'), 'Covered paver patio under a deck with outdoor seating'), (P('patio-seating-wall-house'), 'Patio with stone seating wall behind a two-story home')]),
        ('Built to last', ['Reinforced base with proper compaction', 'Precise leveling to prevent shifting or sinking', 'Materials chosen for strength and moisture resistance'],
         [(P('patio-covered-dusk'), 'Lit covered patio at dusk with stone columns'), (P('patio-flagstone-path'), 'Paver patio with a flagstone path leading to the yard')]),
    ],
    'gallery_title': 'Patio projects', 'gallery_lead': 'Paver and natural stone patios from recent builds around Winchester and the surrounding communities.',
    'gallery': [(P('deck-stairs-flagstone-patio'), 'Flagstone patio and walkway at the base of a deck staircase'), (P('stepping-stone-garden'), 'Stepping stone path through a landscaped garden'),
                (P('deck-lit-stairs-dusk'), 'Lit deck stairs above a stone patio at dusk'), (P('patio-seating-wall-house'), 'Patio seating wall and outdoor dining area'),
                (P('paver-patio-diagonal'), 'Diagonal paver patio with a stone seating wall')],
    'points': [('Outdoor living', 'A patio that extends your home and gives every gathering a place.'), ('Curb appeal', 'Clean patterns, borders and finishing details that lift the whole yard.'), ('Lasting value', 'A properly built base protects your investment and adds value to your home.')],
    'value_photo': P('patio-under-deck-covered'),
    'video': V1,
    'cta': {'eyebrow': 'Patios in Winchester, VA', 'title': 'Ready to build your custom <em>patio?</em>', 'button': 'Get a free patio estimate', 'photo': P('paver-patio-diagonal')},
}

_DECKS = {
    'lead': 'We design and build custom decks, from composite and wood decking to stairs, railings and lighting, creating outdoor spaces that last longer.',
    'chips': ['Composite', 'Wood', 'Railings', 'Stairs', 'Lighting'],
    'hero': P('deck-house-dusk-aerial'), 'hero_alt': 'Elevated deck with stairs and lighting at dusk on a home built by Potros Construction',
    'blocks': [
        ('Materials', ['Composite decking: low maintenance and long lasting', 'Wood decking, including pressure-treated lumber', 'Options for every home and budget'],
         [(P('deck-composite-wide'), 'Wide composite deck with white and black railing'), (P('deck-corner-house'), 'Composite deck corner beside a home with railing and lighting')]),
        ('Design', ['Lounge areas, dining zones and grilling stations', 'Shade structures, pergolas and built-in seating', 'Layouts planned around how people move through the space'],
         [(P('lake-deck-dining'), 'Deck dining area with a lake view'), (P('lake-deck-grill'), 'Deck with grill and seating overlooking a pond')]),
        ('Built to last', ['Reinforced framing and proper footings', 'Corrosion-resistant fasteners', 'Built to code and weather resistant'],
         [(P('deck-stairs-led'), 'Deck staircase with step lighting and post caps'), (P('deck-stair-rail-lights'), 'Deck stair railing with integrated lighting')]),
    ],
    'gallery_title': 'Deck projects', 'gallery_lead': 'Composite and wood decks, stairs and railings from recent builds around Winchester.',
    'gallery': [(P('deck-railing-autumn'), 'Composite deck with railing among autumn trees'), (P('deck-stairs-led-detail'), 'Lit deck stairs with white post caps'),
                (P('deck-post-cap-light'), 'Deck post cap with built-in light'), (P('deck-house-exterior-day'), 'Raised deck with stairs on the back of a home'),
                (P('deck-stairs-aerial'), 'Deck stairs and landing seen from above')],
    'points': [('Outdoor space', 'A deck turns the back of your home into a place to dine, relax and gather.'), ('Safe & solid', 'Strong framing, footings and railings built to code.'), ('Home value', 'A well-built deck adds beauty, function and value to your property.')],
    'value_photo': P('deck-wide-autumn'),
    'video': V1,
    'cta': {'eyebrow': 'Decks in Winchester, VA', 'title': 'Ready to build your custom <em>deck?</em>', 'button': 'Get a free deck estimate', 'photo': P('deck-dining-sunset')},
}

_PORCHES = {
    'lead': 'We design and build custom front, covered and screened porches that add comfort, curb appeal and lasting value to your home.',
    'chips': ['Front porches', 'Covered', 'Screened', 'Railings', 'Roofing'],
    'hero': P('screened-porch-house-exterior'), 'hero_alt': 'Home with a screened porch above a deck, built by Potros Construction',
    'blocks': [
        ('Front porches', ['Traditional, farmhouse or modern styles', 'Custom railings, posts, flooring and roof structures', 'Charm and curb appeal for your entrance'],
         [(P('deck-house-exterior-lawn'), 'Back of a home with a raised porch and stairs'), (P('deck-house-dusk-corner'), 'Home with lit porch and deck at dusk')]),
        ('Covered & screened', ['Shade and protection from rain', 'Screens that keep insects out and let fresh air in', 'The right roofing, framing and layout for each space'],
         [(P('screened-porch-wide'), 'Screened porch with vaulted wood ceiling and seating'), (P('screened-porch-seating'), 'Screened porch seating area with fire table')]),
        ('Craftsmanship', ['Pressure-treated wood, composite decking and durable roofing', 'Reinforced posts and rot-resistant materials', 'Precision from structural framing to finishing touches'],
         [(P('screened-porch-interior'), 'Interior of a screened porch with recessed lighting and a fire table'), (P('screened-porch-fire-table'), 'Screened porch with a fire table and lounge seating')]),
    ],
    'gallery_title': 'Porch projects', 'gallery_lead': 'Covered and screened porches from recent builds around Winchester.',
    'gallery': [(P('screened-porch-lake-view'), 'Screened porch with lounge seating and a lake view'), (P('deck-house-dusk-lit'), 'Lit porch and deck on a home at dusk'),
                (P('lake-deck-stairs'), 'Deck stairs leading down to the yard'), (P('deck-dining-sunset'), 'Deck dining set beside a porch at sunset'),
                (P('aerial-lake-homes'), 'Aerial view of a neighborhood by a lake')],
    'points': [('Year-round comfort', 'Shade, rain protection and screens make the porch usable in almost any weather.'), ('Curb appeal', 'Railings, posts and rooflines designed to match your home.'), ('More living space', 'A porch extends your home and adds lasting value.')],
    'value_photo': P('deck-house-twilight'),
    'video': V1,
    'cta': {'eyebrow': 'Porches in Winchester, VA', 'title': 'Ready to build your custom <em>porch?</em>', 'button': 'Get a free porch estimate', 'photo': P('screened-porch-lake-view')},
}

_LANDSCAPING = {
    'chips': ['Design', 'Planting', 'Beds & mulch', 'Grading & sod', 'Hardscape'],
    'hero': P('stepping-stone-garden'), 'hero_alt': 'Stepping stone path through a landscaped garden in autumn at a Winchester VA home',
    'blocks': [
        ('Design', ['A plan built around sunlight, soil and drainage', 'Shrubs, flowers, trees, mulch beds and stone accents', 'Modern, lush or low-maintenance styles'],
         [(P('stepping-stone-path-stairs'), 'Stepping stone path leading to deck stairs'), (P('deck-stairs-flagstone-patio'), 'Flagstone path and plantings beside deck stairs')]),
        ('Planting', ['Plants selected for Virginia’s seasons', 'Proper soil preparation, spacing and layering', 'Mulch beds and edging for a finished look'],
         [(P('deck-lit-stairs-dusk'), 'Landscaped yard with plantings and lit stairs at dusk'), (P('patio-seating-wall-house'), 'Plantings in front of a patio seating wall')]),
        ('Hardscape integration', ['Patios, walkways and retaining walls in one design', 'Raised beds supported by stone walls', 'Style, scale and color that work together'],
         [(P('patio-flagstone-path'), 'Flagstone path connecting a patio to the yard'), (P('paver-patio-diagonal'), 'Paver patio surrounded by plantings')]),
    ],
    'gallery_title': 'Landscape projects', 'gallery_lead': 'Gardens, paths and planted beds from recent builds around Winchester.',
    'gallery': [(P('deck-stairs-aerial'), 'Landscaped yard seen from above a deck'), (P('patio-covered-dusk'), 'Landscaped patio at dusk'),
                (P('deck-house-exterior-lawn'), 'Lawn and grading behind a home'), (P('paver-patio-columns'), 'Paver patio framed by plantings'),
                (P('aerial-community-lake'), 'Aerial view of a community by a lake')],
    'points': [('Curb appeal', 'Plantings and beds that make a strong first impression.'), ('Healthy growth', 'Drainage, soil preparation and plant selection done for the long term.'), ('Property value', 'Professional landscaping improves the look, use and value of your property.')],
    'value_photo': P('patio-under-deck-covered'),
    'video': V2,
    'cta': {'eyebrow': 'Landscaping in Winchester, VA', 'title': 'Ready to transform your <em>landscape?</em>', 'button': 'Get a free landscaping estimate', 'photo': P('stepping-stone-path-stairs')},
}

SERVICES_MORE = {
    'patios': _build('patios', 'Patios', _PATIOS),
    'decks': _build('decks', 'Decks', _DECKS),
    'porches': _build('porches', 'Porches', _PORCHES),
    'landscaping': _build('landscaping', 'Landscaping', _LANDSCAPING),
}
