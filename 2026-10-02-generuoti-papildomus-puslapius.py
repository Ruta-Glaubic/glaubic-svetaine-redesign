# Generuoja DUK ir privatumo politikos puslapius iš pagrindinio puslapio (tas pats viršus, dovanų juosta, poraštė).
import re, os
os.chdir('/home/user/glaubic-svetaine-redesign')
MAIN='2026-09-27-glaubic-maketas.html'; DUK='2026-09-27-glaubic-duk.html'; PRIV='2026-09-27-glaubic-privatumo-politika.html'
s=open(MAIN,encoding='utf-8').read()

def shell(title, main_html, extra_js=''):
    head=s[:s.index('<main>')].replace('<title>GLAUBIC maketas</title>',f'<title>{title}</title>')
    head=head.replace('<a class="promo" href="#dovana" data-open-gift ',f'<a class="promo" href="{MAIN}#dovana" ')
    head=re.sub(r'<button class="btn btn--cta promo-cta" type="button" data-open-gift aria-label="Pasirinkti dovaną">(.*?)</button>',
                lambda m:f'<a class="btn btn--cta promo-cta" href="{MAIN}#dovana" aria-label="Pasirinkti dovaną">{m.group(1)}</a>',head,flags=re.S)
    head=re.sub(r'href="#(kursai|verslui|akimirkos|lektoriai|kontaktai)"',lambda m:f'href="{MAIN}#{m.group(1)}"',head)
    head=head.replace('<a class="logo" href="#" aria-label="GLAUBIC pradžia">',f'<a class="logo" href="{MAIN}" aria-label="GLAUBIC pradžia">')
    assert 'data-open-gift' not in head
    f0=s.index('<footer class="site-footer">'); f1=s.index('</footer>')+len('</footer>')
    footer=re.sub(r'href="#([a-z-]+)"',lambda m:f'href="{MAIN}#{m.group(1)}"',s[f0:f1])
    footer=footer.replace('<a class="logo" href="#" aria-label="GLAUBIC pradžia">',f'<a class="logo" href="{MAIN}" aria-label="GLAUBIC pradžia">')
    c0=s.index('<section class="cookies"'); c1=s.index('</section>',c0)+len('</section>')
    js=s[s.index('  // ---------- Meniu ----------'):s.index('  // Aktyvi meniu skiltis')]
    js+=extra_js
    js+=s[s.index('  // ---------- Kalba'):s.index('</script>')]
    return head+main_html+'\n'+footer+'\n\n'+s[c0:c1]+'\n\n<script>\n'+js+'</script>\n</body>\n</html>\n'

# DUK: turinys paimamas iš esamo DUK puslapio
d=open(DUK,encoding='utf-8').read()
open(DUK,'w',encoding='utf-8').write(shell('DUK | GLAUBIC', d[d.index('<main>'):d.index('</main>')+len('</main>')]))

def legal_page(fname, title_lt, title_en, eyebrow, h_lt, h_en, lt_body, en_body):
    """Teisinis puslapis su LT ir EN versijomis, rodoma pagal pasirinktą kalbą. Esamas turinys išsaugomas."""
    if os.path.exists(fname):
        old=open(fname,encoding='utf-8').read()
        page_main=old[old.index('<main>'):old.index('</main>')+len('</main>')]
    else:
        page_main=f'''<main>
  <section class="policy-page">
    <div class="wrap">
      <article class="policy" id="lt" lang="lt">
        <a class="back-link" href="{MAIN}">Grįžti į pradžią</a>
        <span class="eyebrow">{eyebrow[0]}</span>
        <h2>{h_lt}</h2>
{lt_body}
      </article>
      <article class="policy" id="en" lang="en" hidden>
        <a class="back-link" href="{MAIN}">Back to home</a>
        <span class="eyebrow">{eyebrow[1]}</span>
        <h2>{h_en}</h2>
{en_body}
      </article>
    </div>
  </section>
</main>'''
    lang_js=f'''  // ---------- Puslapio kalba ----------
  const hashLang = location.hash.replace('#', '');
  if (hashLang === 'lt' || hashLang === 'en') {{ try {{ localStorage.setItem('glaubic-kalba', hashLang); }} catch (e) {{ /* nieko */ }} }}
  window.onLangChange = (l) => {{
    document.getElementById('lt').hidden = l !== 'lt';
    document.getElementById('en').hidden = l !== 'en';
    document.documentElement.lang = l;
    document.title = l === 'en' ? '{title_en}' : '{title_lt}';
    if (location.hash !== `#${{l}}`) history.replaceState(null, '', `#${{l}}`);
  }};

'''
    open(fname,'w',encoding='utf-8').write(shell(title_lt, page_main, lang_js))

legal_page(PRIV, 'Privatumo politika | GLAUBIC', 'Privacy Policy | GLAUBIC', ('Teisinė informacija','Legal information'),
    'Privatumo politika', 'Privacy Policy',
    '        <div class="policy-body policy-placeholder"><p>Čia bus įkeltas privatumo politikos tekstas lietuvių kalba iš glaubic.com/privatumo-politika#lt.</p></div>',
    '        <div class="policy-body policy-placeholder"><p>The English privacy policy text from glaubic.com/privatumo-politika#en will be placed here.</p></div>')

TERMS='2026-10-02-glaubic-paslaugu-teikimo-salygos.html'
lt_terms=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'salygos-lt.html'),encoding='utf-8').read() if not os.path.exists(TERMS) else ''
legal_page(TERMS, 'Paslaugų teikimo sąlygos | GLAUBIC', 'Terms of Service | GLAUBIC', ('Teisinė informacija','Legal information'),
    'Paslaugų teikimo sąlygos', 'Terms of Service', lt_terms,
    '        <div class="policy-body policy-placeholder"><p>The English Terms of Service text from glaubic.com/naudojimosi-taisykles#en will be placed here.</p></div>')
print('ok')
