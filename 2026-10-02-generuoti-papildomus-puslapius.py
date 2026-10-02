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
    head=re.sub(r'href="#(kursai|verslui|apie|lektoriai|kontaktai)"',lambda m:f'href="{MAIN}#{m.group(1)}"',head)
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

# Privatumo politika: LT ir EN versijos, rodoma pagal pasirinktą kalbą
if os.path.exists(PRIV):
    old=open(PRIV,encoding='utf-8').read()
    priv_main=old[old.index('<main>'):old.index('</main>')+len('</main>')]
else:
    priv_main=f'''<main>
  <section class="policy-page">
    <div class="wrap">
      <article class="policy" id="lt" lang="lt">
        <a class="back-link" href="{MAIN}">Grįžti į pradžią</a>
        <span class="eyebrow">Teisinė informacija</span>
        <h2>Privatumo politika</h2>
        <div class="policy-body policy-placeholder">
          <p>Čia bus įkeltas privatumo politikos tekstas lietuvių kalba iš glaubic.com/privatumo-politika#lt.</p>
        </div>
      </article>
      <article class="policy" id="en" lang="en" hidden>
        <a class="back-link" href="{MAIN}">Back to home</a>
        <span class="eyebrow">Legal information</span>
        <h2>Privacy Policy</h2>
        <div class="policy-body policy-placeholder">
          <p>The English privacy policy text from glaubic.com/privatumo-politika#en will be placed here.</p>
        </div>
      </article>
    </div>
  </section>
</main>'''
priv_js='''  // ---------- Privatumo politikos kalba ----------
  const hashLang = location.hash.replace('#', '');
  if (hashLang === 'lt' || hashLang === 'en') { try { localStorage.setItem('glaubic-kalba', hashLang); } catch (e) { /* nieko */ } }
  window.onLangChange = (l) => {
    document.getElementById('lt').hidden = l !== 'lt';
    document.getElementById('en').hidden = l !== 'en';
    document.documentElement.lang = l;
    document.title = l === 'en' ? 'Privacy Policy | GLAUBIC' : 'Privatumo politika | GLAUBIC';
    if (location.hash !== `#${l}`) history.replaceState(null, '', `#${l}`);
  };

'''
open(PRIV,'w',encoding='utf-8').write(shell('Privatumo politika | GLAUBIC', priv_main, priv_js))
print('ok')
