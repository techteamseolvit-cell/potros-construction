"""Re-export site photos at high resolution from the client's originals (kept outside the repo).
Usage: python3 tools/process_assets.py <photos_dir> <more_dir> <p1_dir>
 photos_dir: Drive 'Best Potros Content' originals (IMG_*.jpg)   more_dir: extra downloads (photo_IMG_*.jpg, d_img2_*.png)   p1_dir: unzipped P1 folder (*.webp, 2500 px)"""
import os, sys
from PIL import Image
PH, MORE, P1 = sys.argv[1:4]
A = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'assets')
Image.MAX_IMAGE_PIXELS = None


def save(im, rel, width, q=78):
    im = im.convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    p = os.path.join(A, rel + '.webp'); os.makedirs(os.path.dirname(p), exist_ok=True)
    im.save(p, 'WEBP', quality=q, method=6); return os.path.getsize(p) // 1024


def op(n):
    for d, pre in ((PH, ''), (MORE, 'photo_')):
        f = os.path.join(d, pre + n + '.jpg')
        if os.path.exists(f): return Image.open(f)
    raise FileNotFoundError(n)


# 1) existing hardscape photos: replace the 1100 px exports by 1600 px portrait / 2000 px landscape
HS = {'curved-stone-wall': 'IMG_0041', 'flagstone-pool-edge': 'IMG_0167', 'house-deck-stone-landscape': 'IMG_5207', 'lit-stone-column': 'IMG_0024', 'lit-stone-steps': 'IMG_0084',
      'patio-firepit-boulders': 'IMG_5214', 'patio-firepit-chairs': 'IMG_5206', 'paver-patio-dining': 'IMG_9821', 'paver-patio-firepit': 'IMG_9797', 'paver-patio-steps-wide': 'IMG_9838',
      'paver-steps-entry': 'IMG_9741', 'paver-walkway-grill': 'IMG_9752', 'pool-deck-aerial': 'IMG_0143', 'rounded-paver-steps': 'IMG_9757', 'stone-pillar-wall': 'IMG_0190',
      'stone-wall-lanterns': 'IMG_0068', 'stone-wall-seating-house': 'IMG_0072'}
for name, o in HS.items():
    im = op(o); w = 1600 if im.height > im.width else 2000
    print('hardscapes/' + name, save(im, 'hardscapes/' + name, w, 76), 'KB')

# 2) additional originals -> p2/
P2 = {'paver-steps-landing': 'IMG_9742', 'paver-steps-double-doors': 'IMG_9801', 'paver-steps-closeup': 'IMG_9805', 'paver-patio-table-side': 'IMG_9826', 'paver-patio-chair-doors': 'IMG_9845',
      'stone-pillar-walkway-plantings': 'IMG_0025', 'flagstone-patio-pillar': 'IMG_0036', 'flagstone-pillar-pool-view': 'IMG_0044',
      'covered-patio-tv-lounge': 'IMG_5149', 'covered-patio-dusk-lounge': 'IMG_5167', 'covered-patio-tv-stairs': 'IMG_5217', 'covered-patio-hanging-chairs': 'IMG_5219',
      'deck-patio-night-lights': 'IMG_5166', 'firepit-patio-boulders-side': 'IMG_5213', 'firepit-patio-boulders-garden': 'IMG_5215', 'aerial-patio-firepit-boulders': 'IMG_5198'}
for name, o in P2.items():
    im = op(o); w = 1600 if im.height > im.width else 2200
    print('p2/' + name, save(im, 'p2/' + name, w, 76), 'KB')

# 3) heroes, 2560 px wide, from the largest landscape originals
H = 2560
def p1(n): return Image.open(os.path.join(P1, n + '_.webp'))
heroes = {'hardscapes': op('IMG_5214'), 'fireplaces': op('IMG_5215'), 'blog': op('IMG_5207'), 'guide': op('IMG_5213'), 'faq': op('IMG_5217'), 'reviews': p1('_dsc6402'),
          'portfolio': op('IMG_5166'), 'patios': p1('dsc00024'), 'decks': p1('dji_20261104173141_0172_d'), 'porches': p1('_dsc6388'), 'landscaping': p1('dsc09984'),
          'service-area': p1('dji_20261104165355_0143_d'), 'legal': op('IMG_5149')}
pool = op('IMG_0143'); w, h = pool.size; box = (0, int(h * .26), w, int(h * .26) + int(w * 9 / 16))
heroes['pools'] = pool.crop(box)
for n, im in heroes.items():
    print('hero/' + n, im.size, save(im, 'hero/' + n, H, 78), 'KB')

# 4) 3D design stills
D = {'design-01': 'd_img2_10', 'design-02': 'd_img2_1a', 'design-03': 'd_img2_2', 'design-04': 'd_img2_3a', 'design-05': 'd_img2_3d', 'design-06': 'd_img2_4b', 'design-07': 'd_img2_5a',
     'design-08': 'd_img2_6', 'design-09': 'd_img2_7a', 'design-10': 'd_img2_8', 'design-11': 'd_img2_9'}
for name, o in D.items():
    print('design/' + name, save(Image.open(os.path.join(MORE, o + '.png')), 'design/' + name, 1800, 78), 'KB')

# 5) landscaping-focused crops (plants, beds, paths and boulders) from the same originals
def crop(im, x0, y0, x1, y1):
    w, h = im.size; return im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
CROPS = {'ls-stepping-stones-plants': (p1('dsc00084'), .38, .30, 1, 1), 'ls-flagstone-beds': (p1('dsc00043'), 0, .38, .62, 1), 'ls-grasses-mulch-bed': (p1('dsc00012'), 0, .45, .66, 1),
         'ls-boulder-bed': (op('IMG_5207'), 0, .58, .78, 1), 'ls-garden-path-close': (p1('dsc09984'), .05, .42, .78, 1), 'ls-flagstone-plantings': (p1('dsc09994'), .25, .42, 1, 1)}
for n, (im, a, b, c, d) in CROPS.items():
    print('p2/' + n, save(crop(im, a, b, c, d), 'p2/' + n, 1400, 78), 'KB')
