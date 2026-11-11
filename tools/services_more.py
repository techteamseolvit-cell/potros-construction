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
        'title': extra.get('title', o['title']), 'description': o['desc'], 'h1': h1, 'lead': extra.get('lead', it[2]),
        'chips': extra['chips'], 'hero': [(extra['hero'], extra['hero_alt'])],
        'intro': {'kicker': it[1], 'h2': it[3], 'paras': intro_paras if len(intro_paras) == 2 else [intro_paras[0], ''], 'photo': (extra['hero'], extra['hero_alt'])},
        'blocks': blocks,
        'gallery_title': extra['gallery_title'], 'gallery_lead': extra['gallery_lead'], 'gallery': extra['gallery'],
        'value': {'h2': it[14], 'lead': it[15], 'points': extra['points'], 'photo': extra['value_photo']},
        'process': PROCESS, 'faqs': FAQS, 'cta': extra['cta'], 'video': extra.get('video'), 'reel': extra.get('reel'),
    }


P = lambda n: 'p1/' + n

_VL = 'Every project starts with a realistic 3D virtual tour, so you can walk through your design and approve every detail before we break ground.'
V1 = {'src': 'video/design-1', 'iso': 'PT1M15S', 'lead': _VL, 'label': '3D virtual design walkthrough of a deck, patio and screened porch'}
V3 = {'src': 'video/design-6', 'iso': 'PT1M27S', 'lead': _VL, 'label': '3D virtual design walkthrough of a covered patio with a stone fireplace and fire pit'}
V2 = {'src': 'video/design-2', 'iso': 'PT1M43S', 'lead': _VL, 'label': '3D virtual design walkthrough of a backyard with outdoor kitchen, pergola and landscaping'}

_PATIOS = {
    'lead': 'We design and build durable patios in pavers and natural stone, creating beautiful, functional outdoor spaces that last longer.',
    'chips': ['Pavers', 'Natural stone', 'Fire pits', 'Seating walls', 'Lighting'],
    'hero': 'hero/patios', 'hero_alt': 'Paver patio with stone columns under a covered deck at a Winchester VA home',
    'blocks': [
        ('Materials', ['Pavers, stamped concrete and natural stone', 'Patterns, colors and textures to match your home', 'Premium materials chosen for durability'],
         [(P('paver-patio-diagonal'), 'Paver patio laid in a diagonal pattern beside a stone seating wall'), (P('paver-patio-bistro-border'), 'Paver patio with a dark border and bistro table set')]),
        ('Entertaining', ['Fire pits, seating walls and outdoor kitchens', 'Pergolas and lighting built into the layout', 'Planned around how you live and entertain'],
         [(P('patio-under-deck-covered'), 'Covered paver patio under a deck with outdoor seating'), ('p2/covered-patio-hanging-chairs', 'Covered patio with hanging chairs and a lounge area')]),
        ('Built to last', ['Reinforced base with proper compaction', 'Precise leveling to prevent shifting or sinking', 'Materials chosen for strength and moisture resistance'],
         [(P('patio-covered-dusk'), 'Lit covered patio at dusk with stone columns'), (P('patio-flagstone-path'), 'Paver patio with a flagstone path leading to the yard')]),
    ],
    'gallery_title': 'Patio projects', 'gallery_lead': 'Paver and natural stone patios from recent builds around Winchester and the surrounding communities.',
    'gallery': [(P('deck-stairs-flagstone-patio'), 'Flagstone patio and walkway at the base of a deck staircase'), ('p2/firepit-patio-boulders-side', 'Paver patio with fire pit and boulder landscaping'),
                (P('patio-seating-wall-house'), 'Patio seating wall and outdoor dining area'), ('p2/covered-patio-tv-stairs', 'Covered patio under a deck with seating and a TV'),
                ('p2/paver-patio-table-side', 'Paver patio with dining table beside a home')],
    'points': [('Outdoor living', 'A patio that extends your home and gives every gathering a place.'), ('Curb appeal', 'Clean patterns, borders and finishing details that lift the whole yard.'), ('Lasting value', 'A properly built base protects your investment and adds value to your home.')],
    'value_photo': P('patio-under-deck-covered'),
    'video': V1,
    'cta': {'eyebrow': 'Patios in Winchester, VA', 'title': 'Ready to build your custom <em>patio?</em>', 'button': 'Get a free patio estimate', 'photo': P('paver-patio-diagonal')},
}

_DECKS = {
    'title': 'Decks in Winchester VA | Potros Construction Deck Builders',
    'lead': 'We design and build custom decks, from composite and wood decking to stairs, railings and lighting, creating outdoor spaces that last longer.',
    'chips': ['Composite', 'Wood', 'Railings', 'Stairs', 'Lighting'],
    'hero': 'hero/decks', 'hero_alt': 'Elevated deck with stairs and lighting at dusk on a home built by Potros Construction',
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
                (P('deck-post-cap-light'), 'Deck post cap with built-in light'), ('p2/deck-patio-night-lights', 'Raised deck with string lights above a fire pit patio at night'),
                (P('deck-stairs-aerial'), 'Deck stairs and landing seen from above')],
    'points': [('Outdoor space', 'A deck turns the back of your home into a place to dine, relax and gather.'), ('Safe & solid', 'Strong framing, footings and railings built to code.'), ('Home value', 'A well-built deck adds beauty, function and value to your property.')],
    'value_photo': P('deck-wide-autumn'),
    'video': V1,
    'cta': {'eyebrow': 'Decks in Winchester, VA', 'title': 'Ready to build your custom <em>deck?</em>', 'button': 'Get a free deck estimate', 'photo': P('deck-dining-sunset')},
}

_PORCHES = {
    'title': 'Porches in Winchester VA | Potros Custom Porch Builders',
    'lead': 'We design and build custom front, covered and screened porches that add comfort, curb appeal and lasting value to your home.',
    'chips': ['Front porches', 'Covered', 'Screened', 'Railings', 'Roofing'],
    'hero': 'hero/porches', 'hero_alt': 'Home with a screened porch above a deck, built by Potros Construction',
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
                ('p2/covered-patio-tv-lounge', 'Covered lounge area under a deck with TV and wood ceiling'), (P('deck-dining-sunset'), 'Deck dining set beside a porch at sunset'),
                ('p2/covered-patio-dusk-lounge', 'Covered lounge at dusk with heater and hanging chairs')],
    'points': [('Year-round comfort', 'Shade, rain protection and screens make the porch usable in almost any weather.'), ('Curb appeal', 'Railings, posts and rooflines designed to match your home.'), ('More living space', 'A porch extends your home and adds lasting value.')],
    'value_photo': P('deck-house-twilight'),
    'video': V1,
    'cta': {'eyebrow': 'Porches in Winchester, VA', 'title': 'Ready to build your custom <em>porch?</em>', 'button': 'Get a free porch estimate', 'photo': P('screened-porch-lake-view')},
}

_LANDSCAPING = {
    'title': 'Landscaping in Winchester VA | Potros Landscape Design',
    'chips': ['Design', 'Planting', 'Beds & mulch', 'Grading & sod', 'Hardscape'],
    'hero': 'hero/landscaping', 'hero_alt': 'Stepping stone path through a landscaped garden in autumn at a Winchester VA home',
    'blocks': [
        ('Design', ['A plan built around sunlight, soil and drainage', 'Shrubs, flowers, trees, mulch beds and stone accents', 'Modern, lush or low-maintenance styles'],
         [(P('stepping-stone-path-stairs'), 'Stepping stone path leading to deck stairs'), (P('deck-stairs-flagstone-patio'), 'Flagstone path and plantings beside deck stairs')]),
        ('Planting', ['Plants selected for Virginia’s seasons', 'Proper soil preparation, spacing and layering', 'Mulch beds and edging for a finished look'],
         [(P('deck-lit-stairs-dusk'), 'Landscaped yard with plantings and lit stairs at dusk'), (P('patio-seating-wall-house'), 'Plantings in front of a patio seating wall')]),
        ('Hardscape integration', ['Patios, walkways and retaining walls in one design', 'Raised beds supported by stone walls', 'Style, scale and color that work together'],
         [(P('patio-flagstone-path'), 'Flagstone path connecting a patio to the yard'), (P('paver-patio-diagonal'), 'Paver patio surrounded by plantings')]),
    ],
    'gallery_title': 'Landscape projects', 'gallery_lead': 'Gardens, paths and planted beds from recent builds around Winchester.',
    'gallery': [('p2/stone-pillar-walkway-plantings', 'Flagstone walkway with planted beds beside a stone pillar'), ('p2/aerial-patio-firepit-boulders', 'Aerial view of a patio, fire pit and boulder garden'),
                ('p2/firepit-patio-boulders-garden', 'Boulder water feature and plantings beside a patio'), (P('deck-house-exterior-lawn'), 'Lawn and grading behind a home'),
                (P('deck-stairs-aerial'), 'Landscaped yard seen from above a deck')],
    'points': [('Curb appeal', 'Plantings and beds that make a strong first impression.'), ('Healthy growth', 'Drainage, soil preparation and plant selection done for the long term.'), ('Property value', 'Professional landscaping improves the look, use and value of your property.')],
    'value_photo': P('patio-under-deck-covered'),
    'video': V2,
    'cta': {'eyebrow': 'Landscaping in Winchester, VA', 'title': 'Ready to transform your <em>landscape?</em>', 'button': 'Get a free landscaping estimate', 'photo': P('stepping-stone-path-stairs')},
}

_FIREPLACES = {
    'title': 'Fireplaces in Winchester VA | Potros Outdoor Fire Features',
    'lead': 'We design and build outdoor fireplaces and fire features in stone and brick, bringing warmth and year-round comfort to your backyard.',
    'chips': ['Stone', 'Brick', 'Gas', 'Wood-burning', 'Fire pits'],
    'hero': 'hero/fireplaces', 'hero_alt': 'Fire pit patio with boulders and landscaping at a Winchester VA home',
    'blocks': [
        ('Stone & brick', ['Premium natural stone and brick', 'High-quality masonry materials', 'Built to last for decades'],
         [('patio-firepit-boulders', 'Paver patio with fire pit, boulders and landscaping'), ('paver-patio-firepit', 'Paver patio with a fire pit beside a home')]),
        ('Gathering', ['A focal point for family nights and entertaining', 'Seating planned around the fire', 'Designed to fit your outdoor living area'],
         [('p2/firepit-patio-boulders-side', 'Fire pit patio with Adirondack chairs and boulder landscaping'), ('p2/deck-patio-night-lights', 'Deck with string lights above a fire pit patio at night')]),
        ('Gas & wood', ['Gas fireplaces for convenience', 'Wood-burning for the traditional crackle', 'Custom fire features to suit your lifestyle'],
         [('p1/screened-porch-fire-table', 'Screened porch with a fire table and lounge seating'), ('p1/screened-porch-seating', 'Screened porch seating area around a fire table')]),
    ],
    'gallery_title': 'Fire feature projects', 'gallery_lead': 'Fire pits and fire features from recent builds around Winchester.',
    'gallery': [('patio-firepit-chairs', 'Fire pit with Adirondack chairs on a stamped paver patio'), ('paver-patio-firepit', 'Paver patio with fire pit'),
                ('p2/aerial-patio-firepit-boulders', 'Aerial view of a fire pit patio with boulders'), ('p1/screened-porch-lake-view', 'Fire table and lounge seating with a lake view'),
                ('p2/firepit-patio-boulders-garden', 'Fire pit patio with boulder water feature')],
    'points': [('Year-round comfort', 'A fire feature extends the season you can enjoy your yard.'), ('A natural focal point', 'Stone and brick give your outdoor space a place everyone gathers.'), ('Lasting value', 'Quality masonry adds beauty and value to your property.')],
    'value_photo': 'p2/firepit-patio-boulders-side',
    'video': V3,
    'cta': {'eyebrow': 'Fireplaces in Winchester, VA', 'title': 'Ready to add a custom <em>fire feature?</em>', 'button': 'Get a free fireplace estimate', 'photo': 'patio-firepit-boulders'},
}

# ───────────── photo assignment (reviewed): each service uses its own subject, mixing different projects ─────────────
_PATIOS.update({
    'hero': 'hero/patios', 'hero_alt': 'Paver patio with stone columns under a covered deck at a Winchester VA home',
    'blocks': [
        ('Materials', _PATIOS['blocks'][0][1], [('paver-patio-dining', 'Large paver patio with outdoor dining table beside a gray-sided home'), (P('paver-patio-diagonal'), 'Paver patio laid in a diagonal pattern beside a stone seating wall')]),
        ('Entertaining', _PATIOS['blocks'][1][1], [('patio-firepit-chairs', 'Stamped paver patio with fire pit and Adirondack chairs'), ('p2/covered-patio-hanging-chairs', 'Covered patio with hanging chairs and a lounge area')]),
        ('Built to last', _PATIOS['blocks'][2][1], [('p2/paver-patio-table-side', 'Paver patio with dining table beside a home'), ('curved-stone-wall', 'Flagstone patio with a curved natural stone wall')]),
    ],
    'gallery': [(P('paver-patio-bistro-border'), 'Paver patio with a dark border and bistro table set'), ('p2/firepit-patio-boulders-side', 'Paver patio with fire pit and boulder landscaping'),
                ('paver-patio-firepit', 'Paver patio with fire pit beside a home'), ('p2/flagstone-patio-pillar', 'Flagstone patio with a lit stone pillar'),
                ('stone-wall-seating-house', 'Flagstone patio with stone seating wall and lantern in front of a farmhouse')],
    'value_photo': 'stone-wall-seating-house',
})
_PORCHES.update({
    'hero': 'hero/porches', 'hero_alt': 'Screened porch with vaulted wood ceiling and lounge seating built by Potros Construction',
    'blocks': [
        ('Front porches', _PORCHES['blocks'][0][1], [(P('screened-porch-house-exterior'), 'Home with a screened porch above a deck, built by Potros Construction'), (P('deck-house-dusk-corner'), 'Home with lit porch and deck at dusk')]),
        ('Covered & screened', _PORCHES['blocks'][1][1], [(P('screened-porch-seating'), 'Screened porch seating area with fire table'), (P('screened-porch-lake-view'), 'Screened porch with lounge seating and a lake view')]),
        ('Craftsmanship', _PORCHES['blocks'][2][1], [(P('screened-porch-interior'), 'Interior of a screened porch with recessed lighting and a fire table'), (P('screened-porch-fire-table'), 'Screened porch with a fire table and lounge seating')]),
    ],
    'gallery': [('p2/covered-patio-hanging-chairs', 'Covered porch area with hanging chairs'), ('p2/covered-patio-tv-lounge', 'Covered lounge under a deck with TV and wood ceiling'),
                ('p2/covered-patio-dusk-lounge', 'Covered lounge at dusk with heater and hanging chairs'), ('p2/covered-patio-tv-stairs', 'Covered area with seating, TV and stairs'),
                (P('deck-house-dusk-lit'), 'Lit porch and deck on a home at dusk')],
    'value_photo': P('deck-house-twilight'),
})
_LANDSCAPING.update({
    'hero': 'hero/landscaping', 'hero_alt': 'Stepping stone path through a landscaped garden in autumn at a Winchester VA home',
    'blocks': [
        ('Design', _LANDSCAPING['blocks'][0][1], [('p2/ls-stepping-stones-plants', 'Stepping stone path winding through planted beds'), ('p2/stone-pillar-walkway-plantings', 'Flagstone walkway with planted beds beside a stone pillar')]),
        ('Planting', _LANDSCAPING['blocks'][1][1], [('p2/ls-grasses-mulch-bed', 'Ornamental grasses and mulch beds beside a paver patio'), ('p2/firepit-patio-boulders-garden', 'Boulder water feature and plantings beside a patio')]),
        ('Hardscape integration', _LANDSCAPING['blocks'][2][1], [('p2/ls-flagstone-plantings', 'Paver patio edged with flagstone steps and shrubs'), ('patio-firepit-boulders', 'Paver patio, boulders and plantings around a fire pit')]),
    ],
    'gallery': [('p2/ls-boulder-bed', 'Boulder landscaping, ornamental grasses and mulch beds'), ('p2/ls-garden-path-close', 'Flagstone stepping stones through a mulch bed with shrubs'),
                ('flagstone-pool-edge', 'Flagstone pool edge with river rock and plantings'), ('p2/ls-flagstone-beds', 'Flagstone path and shrubs in mulch beds beside a patio'),
                ('p2/aerial-patio-firepit-boulders', 'Aerial view of a patio, fire pit and boulder garden')],
    'value_photo': 'p2/ls-garden-path-close',
})
_LANDSCAPING['cta']['photo'] = 'p2/stone-pillar-walkway-plantings'
_FIREPLACES.update({
    'blocks': [
        ('Stone & brick', _FIREPLACES['blocks'][0][1], [('paver-patio-firepit', 'Paver patio with a fire pit beside a home'), ('design/design-06', '3D design of a lit stone seating wall with a fire pit')]),
        ('Gathering', _FIREPLACES['blocks'][1][1], [('p2/deck-patio-night-lights', 'Deck with string lights above a fire pit patio at night'), ('p1/screened-porch-lake-view', 'Fire table and lounge seating with a lake view')]),
        ('Gas & wood', _FIREPLACES['blocks'][2][1], [('p1/screened-porch-fire-table', 'Screened porch with a fire table and lounge seating'), ('p2/aerial-patio-firepit-boulders', 'Aerial view of a fire pit patio with boulders')]),
    ],
    'gallery': [('patio-firepit-chairs', 'Fire pit with Adirondack chairs on a stamped paver patio'), ('p1/screened-porch-seating', 'Screened porch seating area around a fire table'),
                ('design/design-05', '3D design of a deck, patio and lit stone seating walls at dusk'), ('design/design-09', '3D design of a covered patio with a fire pit lounge'),
                ('p2/firepit-patio-boulders-side', 'Fire pit patio with Adirondack chairs and boulder landscaping')],
    'value_photo': 'patio-firepit-chairs',
})

_RL = 'A walk through a finished project with the Potros team.'
_PATIOS['reel'] = {'src': 'reel-patio', 'h2': 'Walk a finished patio with us.', 'lead': 'The Potros team walks you through a finished patio and deck project, step by step.', 'label': 'Video tour of a finished patio and deck project'}
_DECKS['reel'] = {'src': 'reel-deck', 'h2': 'See a finished deck up close.', 'lead': 'A closer look at the stairs, railing and lighting details of a finished deck.', 'label': 'Video tour of a finished deck'}
_PORCHES['reel'] = {'src': 'reel-aerial', 'h2': 'A finished deck, from above and at dusk.', 'lead': 'Aerial and dusk views of a deck and porch built by Potros Construction.', 'label': 'Aerial and dusk video of a finished deck and porch'}
SERVICES_MORE = {
    'patios': _build('patios', 'Patios', _PATIOS),
    'decks': _build('decks', 'Decks', _DECKS),
    'porches': _build('porches', 'Porches', _PORCHES),
    'landscaping': _build('landscaping', 'Landscaping', _LANDSCAPING),
    'fireplaces': _build('fireplaces', 'Fireplaces', _FIREPLACES),
}

# Pools: NEW copy (no original page to preserve). Scope wording to be confirmed with the client.
_POOL_P = [
    'Winchester, VA’s Pool Deck and Outdoor Living Specialists',
    'Custom Pool Projects in Winchester VA',
]
SERVICES_MORE['pools'] = {
    'slug': 'pools', 'name': 'Pools', 'folder': 'hardscapes',
    'title': 'Pools in Winchester VA | Potros Construction Pool Decks',
    'description': 'Pool decks, patios, stone walls and outdoor living around your pool in Winchester, VA. Free on-site estimates and 3D design from Potros Construction.',
    'h1': 'Pool Projects in Winchester, VA',
    'lead': 'We design and build the outdoor spaces around your pool, from flagstone and paver decks to stone walls, lighting and seating areas.',
    'chips': ['Pool decks', 'Flagstone', 'Pavers', 'Stone walls', 'Lighting'],
    'hero': [('hero/pools', 'Flagstone pool deck with lounge chairs, stone walls and lighting built by Potros Construction')],
    'intro': {'kicker': 'Winchester, VA’s Pool Deck and Outdoor Living Specialists', 'h2': 'Custom Pool Projects in Winchester VA',
              'paras': ['A pool is only as good as the space around it: the deck you walk on, the walls that frame it and the places where family and friends gather.',
                        'Potros Construction plans and builds the surroundings that make a pool feel like part of your home, with careful attention to drainage, safe surfaces and materials that hold up to sun, water and Virginia winters.'],
              'photo': ('pool-deck-aerial', 'Aerial view of a flagstone pool deck')},
    'blocks': [
        {'kicker': 'Pool decks', 'h2': 'Pool Decks and Surrounds Built for Comfort and Safety',
         'paras': ['The surface around a pool takes constant wear from water, sun and foot traffic. We build pool decks and surrounds in natural flagstone, pavers and other durable materials, with a stable base and proper grading so water drains away from the pool and your home.',
                   'Every layout is planned around how you use the space, with room for lounging, dining and walking comfortably.'],
         'bullets': ['Flagstone and paver pool decks', 'Proper grading and drainage', 'Surfaces chosen for comfort and durability'],
         'photos': [('pool-deck-aerial', 'Aerial view of a flagstone pool deck with stone retaining walls'), ('flagstone-pool-edge', 'Flagstone pool edge with river rock and plantings')]},
        {'kicker': 'Walls & seating', 'h2': 'Stone Walls, Seating and Structure Around the Water',
         'paras': ['Stone walls frame the pool, support level areas on sloped yards and create built-in seating. Combined with columns and caps, they give the space structure and a finished, custom look.',
                   'We integrate steps, planters and seating walls into the design so everything feels like one cohesive outdoor room.'],
         'bullets': ['Natural stone retaining and seating walls', 'Columns, caps and steps', 'Built-in seating and planters'],
         'photos': [('curved-stone-wall', 'Curved natural stone wall over a flagstone patio'), ('stone-wall-seating-house', 'Stone seating wall with lantern and flagstone patio')]},
        {'kicker': 'Lighting & living', 'h2': 'Lighting, Fire Features and Outdoor Living',
         'paras': ['Evenings by the pool are the best part of the summer. We add lighting to walls, steps and columns, and can include fire pits, fireplaces and outdoor kitchens so the space works well after the sun goes down.',
                   'Our 3D virtual design lets you see the finished pool area before any work begins.'],
         'bullets': ['Wall, column and step lighting', 'Fire pits and fireplaces', 'Outdoor kitchens and dining areas'],
         'photos': [('lit-stone-column', 'Lit natural stone column on a flagstone patio'), ('stone-wall-lanterns', 'Stone wall with lantern posts and flagstone patio')]},
    ],
    'gallery_title': 'Pool area projects', 'gallery_lead': 'Pool decks, stone walls and outdoor living spaces from recent builds around Winchester.',
    'gallery': [('p2/flagstone-patio-pillar', 'Flagstone patio with a lit stone pillar beside the pool'), ('p2/flagstone-pillar-pool-view', 'Stone pillar and flagstone with the pool in the background'),
                ('stone-pillar-wall', 'Stone pillar and wall with accent lighting'), ('lit-stone-steps', 'Natural stone steps with step lighting'),
                ('p2/stone-pillar-walkway-plantings', 'Flagstone walkway with planted beds and a stone pillar')],
    'value': {'h2': 'Make Your Pool the Centerpiece of Your Outdoor Space',
              'lead': 'A well-designed pool area increases how much you use your yard and adds lasting value to your property. Potros Construction delivers careful planning, quality materials and detailed craftsmanship around your pool.',
              'points': [('Safe, durable surfaces', 'Materials and grading chosen for comfort underfoot and good drainage.'), ('Cohesive design', 'Decks, walls, lighting and seating planned together.'), ('Lasting value', 'A finished pool area adds beauty, use and value to your home.')],
              'photo': 'flagstone-pool-edge'},
    'process': PROCESS, 'faqs': FAQS, 'video': None,
    'cta': {'eyebrow': 'Pools in Winchester, VA', 'title': 'Ready to design your <em>pool area?</em>', 'button': 'Get a free pool area estimate', 'photo': 'pool-deck-aerial'},
}


# ───────────── AI concept images (reviewed by client); shown with a "Design concept" tag ─────────────
C = lambda n: 'concept/' + n
def _swap(slug, blocks=None, gallery=None):
    d = SERVICES_MORE[slug]
    for i, ph in (blocks or {}).items(): d['blocks'][i]['photos'] = ph
    if gallery: d['gallery'] = gallery
_swap('patios', gallery=[(C('patio-pavers-steps'), 'Design concept: paver patio with wide steps and a dining set behind a gray-sided home'), (C('patio-under-deck'), 'Design concept: covered paver patio under an elevated deck with stone columns'),
                         (P('paver-patio-bistro-border'), 'Paver patio with a dark border and bistro table set'), ('p2/firepit-patio-boulders-side', 'Paver patio with fire pit and boulder landscaping'),
                         ('stone-wall-seating-house', 'Flagstone patio with stone seating wall and lantern in front of a farmhouse')])
_swap('fireplaces', blocks={0: [(C('fireplace-stone-patio'), 'Design concept: freestanding fieldstone outdoor fireplace on a gray paver patio'), ('paver-patio-firepit', 'Paver patio with a fire pit beside a home')],
                            1: [(C('firepit-stone-chairs'), 'Design concept: round stacked-stone fire pit with black Adirondack chairs'), ('p2/deck-patio-night-lights', 'Deck with string lights above a fire pit patio at night')]},
      gallery=[(C('fireplace-stone-patio'), 'Design concept: outdoor stone fireplace'), (C('firepit-stone-chairs'), 'Design concept: stone fire pit with chairs'), ('patio-firepit-chairs', 'Fire pit with Adirondack chairs on a stamped paver patio'),
               ('p2/aerial-patio-firepit-boulders', 'Aerial view of a fire pit patio with boulders'), ('p1/screened-porch-lake-view', 'Fire table and lounge seating with a lake view')])
_swap('landscaping', blocks={0: [(C('landscape-stepping-stones'), 'Design concept: flagstone stepping stones through mulch beds to a paver patio'), ('p2/ls-stepping-stones-plants', 'Stepping stone path winding through planted beds')],
                             1: [(C('landscape-side-bed'), 'Design concept: mulch bed with boulder and young ornamental grasses beside a paver walkway'), ('p2/ls-grasses-mulch-bed', 'Ornamental grasses and mulch beds beside a paver patio')],
                             2: [(C('landscape-front-walkway'), 'Design concept: curved paver walkway with young shrubs in mulch beds'), ('p2/ls-flagstone-plantings', 'Paver patio edged with flagstone steps and shrubs')]},
      gallery=[(C('landscape-retaining-wall'), 'Design concept: low stone retaining wall with new sod and a flagstone path'), ('p2/ls-boulder-bed', 'Boulder landscaping, ornamental grasses and mulch beds'),
               ('p2/ls-garden-path-close', 'Flagstone stepping stones through a mulch bed with shrubs'), ('p2/ls-flagstone-beds', 'Flagstone path and shrubs in mulch beds beside a patio'),
               ('flagstone-pool-edge', 'Flagstone pool edge with river rock and plantings')])
_swap('pools', blocks={0: [(C('pool-deck-flagstone'), 'Design concept: flagstone pool deck with a lounge chair and a stone wall behind'), (C('pool-deck-closeup'), 'Design concept: flagstone pool edge with stone steps and a stone wall')],
                       1: [(C('pool-stone-wall'), 'Design concept: pool with a low stacked-stone wall, steps and farmland beyond'), ('curved-stone-wall', 'Curved natural stone wall over a flagstone patio')]},
      gallery=[(C('pool-from-house'), 'Design concept: pool and flagstone deck seen from the back door of a home'), (C('pool-stone-wall'), 'Design concept: pool with stacked-stone wall'), ('flagstone-pool-edge', 'Flagstone pool edge with river rock and plantings'),
               ('p2/flagstone-patio-pillar', 'Flagstone patio with a lit stone pillar beside the pool'), ('stone-pillar-wall', 'Stone pillar and wall with accent lighting')])
