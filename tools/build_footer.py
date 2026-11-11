"""Standalone footer (HTML + scoped CSS, no JavaScript) -> docs/paste/footer.html
Absolute URLs, full-bleed, responsive. Meant to be pasted alone into the theme's footer area."""
import os
SITE = 'https://potrosconstruction.com'
ASSET = 'https://techteamseolvit-cell.github.io/potros-construction/docs/assets/'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'paste')
SERVICES = [('hardscapes', 'Hardscapes'), ('patios', 'Patios'), ('decks', 'Decks'), ('porches', 'Porches'), ('fireplaces', 'Fireplaces'), ('landscaping', 'Landscaping'), ('pools', 'Pools')]
COMPANY = [('about-us', 'About us'), ('portfolio', 'Portfolio'), ('reviews', 'Reviews'), ('service-area', 'Service area'), ('faq', 'FAQ'), ('contact-us', 'Contact us')]

CSS = '''
#potros-footer{position:relative;left:50%;width:100vw;max-width:100vw;margin-left:-50vw;box-sizing:border-box;background:#0a0a0a;color:#f5f5f5;border-top:1px solid rgba(255,255,255,.13);padding:70px 0 26px;font-family:'Manrope',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-size:15px;line-height:1.6;text-align:left}
#potros-footer *{box-sizing:border-box}
#potros-footer .pf-wrap{width:100%;max-width:1320px;margin:0 auto;padding:0 clamp(20px,4vw,48px)}
#potros-footer .pf-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.2fr;gap:40px;align-items:start}
#potros-footer .pf-grid>*{min-width:0}
#potros-footer .pf-brand{display:flex;align-items:center;gap:18px}
#potros-footer .pf-brand img{width:84px;height:auto;flex:none;display:block;border:0}
#potros-footer .pf-brand p{margin:0;color:#a0a0a0;max-width:34ch}
#potros-footer h3{margin:0 0 16px;padding:0;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:#a0a0a0!important;font-weight:600;font-family:inherit}
#potros-footer a{display:block;color:rgba(255,255,255,.8);font-size:15px;margin:0 0 8px;text-decoration:none;transition:color .25s}
#potros-footer a:hover{color:#e0100f}
#potros-footer address{font-style:normal;color:rgba(255,255,255,.8);margin:0 0 8px}
#potros-footer .pf-hours{margin:0;color:rgba(255,255,255,.8)}
#potros-footer .pf-bar{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:50px;padding-top:22px;border-top:1px solid rgba(255,255,255,.13);font-size:13px;color:#a0a0a0}
#potros-footer .pf-bar a{display:inline;font-size:13px;color:#a0a0a0;margin:0}
#potros-footer .pf-bar a:hover{color:#e0100f}
@media (max-width:860px){
  #potros-footer{padding:54px 0 24px}
  #potros-footer .pf-grid{grid-template-columns:1fr 1fr;gap:34px 28px}
  #potros-footer .pf-grid>:first-child,#potros-footer .pf-grid>:nth-child(4){grid-column:1 / -1}
}
@media (max-width:480px){
  #potros-footer .pf-brand{flex-direction:column;align-items:flex-start}
  #potros-footer .pf-bar{flex-direction:column}
}
'''

def build():
    svc = ''.join(f'<a href="{SITE}/{s}-winchester-va/">{l}</a>' for s, l in SERVICES)
    com = ''.join(f'<a href="{SITE}/{s}/">{l}</a>' for s, l in COMPANY)
    html = f'''<style>{CSS}</style>
<footer id="potros-footer">
  <div class="pf-wrap">
    <div class="pf-grid">
      <div class="pf-brand"><img src="{ASSET}emblem.png" alt="Potros Construction" width="84" height="93"><p>Custom hardscapes and outdoor living in Winchester, VA and surrounding communities.</p></div>
      <div><h3>Services</h3>{svc}</div>
      <div><h3>Company</h3>{com}</div>
      <div><h3>Visit</h3><address>704 Baker Ln, Suite 5<br>Winchester, VA 22603</address><a href="tel:+15405148725">(540) 514-8725</a><p class="pf-hours">Mon–Sat · 8:00 AM – 6:00 PM<br>Sunday closed</p></div>
    </div>
    <div class="pf-bar"><span>© 2026 Potros Construction LLC</span><span><a href="{SITE}/privacy-policy/">Privacy</a> · <a href="{SITE}/terms-and-conditions/">Terms</a></span></div>
  </div>
</footer>
'''
    open(os.path.join(OUT, 'footer.html'), 'w', encoding='utf-8').write(html)
    open(os.path.join(OUT, 'footer.txt'), 'w', encoding='utf-8').write(html)
    print(len(html), 'bytes')

if __name__ == '__main__':
    build()
