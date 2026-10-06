# GLAUBIC laiškų šablonai: tas pats maketas kaip training-platform/server.js emailLayout().
# Kintami laukai rašomi {{taip}}; juos pakeičia siuntimo sistema.
import os, html
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'laisku-sablonai') if os.path.basename(os.path.dirname(os.path.abspath(__file__))) == 'glaubic-svetaine-redesign' else '/home/user/glaubic-svetaine-redesign/laisku-sablonai'
B = dict(yellow='#FFED00', violet100='#ECEEFB', violet500='#9AA2E6', coral='#FF6A3D', ink800='#322838', ink600='#6B6072', paper='#F5F5F3', white='#FFFFFF')
FONT = "'Hanken Grotesk',Arial,Helvetica,sans-serif"
HEAD = "Manrope,'Hanken Grotesk',Arial,Helvetica,sans-serif"
LOGO = 'https://glaubic.com/img/glaubic-logotipas.png?v=20261004'
FOOT = {
  'lt': ('MB „Glaubic“ · Raitininkų g. 4-74, Vilnius', 'glaubic.com', 'https://glaubic.com'),
  'en': ('MB “Glaubic” · Raitininkų g. 4-74, Vilnius, Lithuania', 'glaubic.com/en', 'https://glaubic.com/en'),
}

def p(t): return f'<p style="margin:0 0 16px;">{t}</p>'
def link(href, t): return f'<a href="{href}" style="color:{B["ink800"]};">{t}</a>'
def signature(lines): return f'<p style="margin:24px 0 0;">{"<br>".join(lines)}</p>'
def h2(t): return f'<h2 style="margin:28px 0 10px;font-family:{HEAD};font-size:18px;line-height:1.3;font-weight:800;color:{B["ink800"]};">{t}</h2>'
def ul(items): return '<ul style="margin:0 0 16px;padding-left:22px;">' + ''.join(f'<li style="margin:0 0 6px;">{i}</li>' for i in items) + '</ul>'
def box(inner, title='', bg=None):
    bg = bg or B['violet100']
    head = f'<p style="margin:0 0 6px;font-weight:700;">{title}</p>' if title else ''
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;"><tr><td style="background:{bg};border-radius:16px;padding:16px 20px;font-family:{FONT};font-size:15px;line-height:1.6;color:{B["ink800"]};">{head}{inner}</td></tr></table>'
def button(href, label): return f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:20px 0;"><tr><td style="background:{B["coral"]};border-radius:999px;"><a href="{href}" style="display:inline-block;padding:13px 26px;font-family:{FONT};font-size:16px;font-weight:700;color:{B["ink800"]};text-decoration:none;border-radius:999px;">{label}</a></td></tr></table>'

def layout(lang, title, subtitle, preheader, body):
    comp, site, url = FOOT[lang]
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light only"><meta name="supported-color-schemes" content="light"><title>{html.escape(title)}</title></head>
<body style="margin:0;padding:0;background:{B["paper"]};">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">{html.escape(preheader)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{B["paper"]};">
  <tr><td align="center" style="padding:24px 12px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;">
      <tr><td style="background:{B["violet500"]};border-radius:24px 24px 0 0;padding:26px 32px 24px;font-family:{FONT};color:{B["ink800"]};">
        <img src="{LOGO}" alt="GLAUBIC" width="139" height="21" style="display:block;border:0;outline:none;text-decoration:none;width:139px;height:21px;">
        <h1 style="margin:16px 0 0;font-family:{HEAD};font-size:26px;line-height:1.2;font-weight:800;color:{B["ink800"]};">{title}</h1>
        <p style="margin:8px 0 0;font-size:15px;line-height:1.5;color:{B["ink800"]};">{subtitle}</p>
      </td></tr>
      <tr><td style="background:{B["white"]};border-radius:0 0 24px 24px;padding:28px 32px 32px;font-family:{FONT};font-size:16px;line-height:1.6;color:{B["ink800"]};">
{body}
      </td></tr>
      <tr><td style="padding:18px 24px 0;font-family:{FONT};font-size:12px;line-height:1.6;color:{B["ink600"]};text-align:center;">
        {comp}<br>
        <a href="mailto:ai@marketyourvisions.lt" style="color:{B["ink600"]};">ai@marketyourvisions.lt</a> · <a href="tel:+37062469115" style="color:{B["ink600"]};">+370 624 69115</a> · <a href="{url}" style="color:{B["ink600"]};">{site}</a>
      </td></tr>
    </table>
  </td></tr>
</table>
</body>
</html>
'''

# Kiekvienas šablonas: failo pavadinimas, tema, laukai, LT ir EN turinys.
TEMPLATES = []

def sf():
    lt = layout('lt', 'Sąskaita faktūra', '{{saskaitos_numeris}}',
        'Prisegame jūsų sąskaitą faktūrą {{saskaitos_numeris}}.',
        '\n'.join([
            p('Sveiki,'),
            p('dėkojame, kad įsigijote GLAUBIC AI mokymus „{{mokymu_pavadinimas}}“. Prisegame Jūsų sąskaitą faktūrą {{saskaitos_numeris}}.'),
            p('Kilus klausimų, drąsiai rašykite.'),
            signature(['Su linkėjimais,', 'Glaubic AI komanda', link('https://www.glaubic.com', 'www.glaubic.com')]),
        ]))
    en = layout('en', 'Invoice', '{{invoice_number}}',
        'Please find attached your invoice {{invoice_number}}.',
        '\n'.join([
            p('Hello,'),
            p('thank you for purchasing the GLAUBIC AI training “{{training_name}}”. Please find attached your invoice {{invoice_number}}.'),
            p('If you have any questions, feel free to get in touch.'),
            signature(['Kind regards,', 'Glaubic AI team', link('https://www.glaubic.com/en', 'www.glaubic.com')]),
        ]))
    TEMPLATES.append(dict(
        key='saskaita-faktura', name='Sąskaita faktūra', when='Kai išrašoma sąskaita faktūra (per 3 darbo dienas po pirkimo). Prisegamas PDF.',
        subject_lt='Sąskaita faktūra {{saskaitos_numeris}}', subject_en='Invoice {{invoice_number}}',
        fields_lt=['{{mokymu_pavadinimas}}', '{{saskaitos_numeris}}'], fields_en=['{{training_name}}', '{{invoice_number}}'],
        example={'{{mokymu_pavadinimas}}': 'Claude verslo ir asmeninėse užduotyse', '{{saskaitos_numeris}}': 'GL26/146',
                 '{{training_name}}': 'Claude for work and everyday tasks', '{{invoice_number}}': 'GL26/146'},
        lt=lt, en=en))

sf()

PREP_LT = dict(
  topics=['Praktiškai pradėsime taikyti Claude Cowork.',
          'Claude potencialas projektų valdymui.',
          'Claude užklausų formulavimas, kad gautumėte tikslų rezultatą.',
          'Claude ir el. pašto valdymas: atsakymų rengimas, šablonai, komunikacijos automatizavimas.',
          'Claude ataskaitų ir dokumentų kūrimui.',
          'Claude klientų komunikacijai: pasiūlymų, pristatymų ir atsakymų rengimas.',
          'Claude darbas su failais: dokumentų analizė ir tvarkymas tiesiai iš savo kompiuterio.',
          '<strong>Svarbiausia:</strong> Claude jungtys (connectors) ir integracija su Canva, Google Workspace, kalendoriais ar kitais įrankiais, kurie prijungiami prie Claude.'],
  fit=['Visiems, kurie niekada nėra dirbę su Claude arba dirbo tik su Claude Chat funkcija ir nori daugiau galimybių.',
       'Verslų savininkams, specialistams ir tobulėjantiems, kurie nori neatsilikti ir plėsti AI kompetencijas.'])
PREP_EN = dict(
  topics=['We will start using Claude Cowork in practice.',
          'Claude’s potential for project management.',
          'Writing Claude prompts that get you precise results.',
          'Claude and email: drafting replies, templates, automating communication.',
          'Claude for creating reports and documents.',
          'Claude for client communication: preparing proposals, presentations and replies.',
          'Claude and files: analysing and organising documents right from your computer.',
          '<strong>Most important:</strong> Claude connectors and integrations with Canva, Google Workspace, calendars and other tools you can connect to Claude.'],
  fit=['Anyone who has never used Claude, or has only used Claude Chat and wants to do more.',
       'Business owners, specialists and lifelong learners who want to keep up and grow their AI skills.'])

def prep(city_key, city_lt, place_lt, place_en, maps, directions_lt=None, directions_en=None, ex=None):
    lt_body = [
        p('Laba diena,'),
        p('ačiū, kad renkatės tobulėti. Siunčiame jums informaciją apie praktinius mokymus „{{mokymu_pavadinimas}}“.'),
        box('Data: <strong>{{data}}, {{laikas}} val.</strong><br>Trukmė: <strong>{{trukme}}</strong><br>Vieta: <strong>' + place_lt + '</strong>', 'Mokymų informacija'),
        h2('Ką darysime mokymų metu?'), ul(PREP_LT['topics']),
        box('Turėti savo kompiuterį ir mokamą Claude versiją <strong>Pro</strong>.', 'Būtina', B['yellow']),
        h2('Mokymai tinka'), ul(PREP_LT['fit']),
        h2('Lektorius'), p('{{lektorius}}'),
    ]
    if directions_lt:
        lt_body += [h2('Kaip mus rasti'), p(directions_lt)]
    lt_body += [button(maps, 'Atidaryti žemėlapyje'),
                p('Jeigu turėsite klausimų, rašykite ar skambinkite: ' + link('mailto:ai@marketyourvisions.lt', 'ai@marketyourvisions.lt') + ' arba ' + link('tel:+37062469115', '+370 624 69115') + '.'),
                signature(['Su linkėjimais,', 'Glaubic AI komanda', link('https://www.glaubic.com', 'www.glaubic.com')])]
    en_body = [
        p('Hello,'),
        p('thank you for choosing to learn with us. Here is everything you need to know about the hands-on training “{{training_name}}”.'),
        box('Date: <strong>{{date}}, {{time}}</strong><br>Duration: <strong>{{duration}}</strong><br>Venue: <strong>' + place_en + '</strong>', 'Training details'),
        h2('What we will do'), ul(PREP_EN['topics']),
        box('Bring your own laptop and have a paid <strong>Claude Pro</strong> plan.', 'Required', B['yellow']),
        h2('Who it is for'), ul(PREP_EN['fit']),
        h2('Trainer'), p('{{trainer}}'),
    ]
    if directions_en:
        en_body += [h2('How to find us'), p(directions_en)]
    en_body += [button(maps, 'Open in maps'),
                p('If you have any questions, email or call us: ' + link('mailto:ai@marketyourvisions.lt', 'ai@marketyourvisions.lt') + ' or ' + link('tel:+37062469115', '+370 624 69115') + '.'),
                signature(['Kind regards,', 'Glaubic AI team', link('https://www.glaubic.com/en', 'www.glaubic.com')])]
    lt = layout('lt', 'Pasiruošimas mokymams', '{{mokymu_pavadinimas}} · ' + city_lt, 'Data, vieta ir ką pasiimti į mokymus.', '\n'.join(lt_body))
    en = layout('en', 'Getting ready for your training', '{{training_name}} · ' + {'vilnius':'Vilnius','kaunas':'Kaunas'}[city_key], 'Date, venue and what to bring to your training.', '\n'.join(en_body))
    TEMPLATES.append(dict(
        key=f'pasiruosimas-{city_key}', name=f'Pasiruošimas: {city_lt}', when='Per 24 val. po pirkimo. Visa informacija apie mokymus.',
        subject_lt='Pasiruošimas mokymams: {{mokymu_pavadinimas}}', subject_en='Getting ready for your training: {{training_name}}',
        fields_lt=['{{mokymu_pavadinimas}}', '{{data}}', '{{laikas}}', '{{trukme}}', '{{lektorius}}'],
        fields_en=['{{training_name}}', '{{date}}', '{{time}}', '{{duration}}', '{{trainer}}'],
        example=ex, lt=lt, en=en))

LECT_LT = 'Vilhelmas Šulcas, IT projektų vadovas, Code Academy dėstytojas'
LECT_EN = 'Vilhelmas Šulcas, IT project manager and Code Academy lecturer'
prep('vilnius', 'Vilnius',
     'Glaubic ofisas, Dominikonų g. 5, Vilnius', 'Glaubic office, Dominikonų g. 5, Vilnius',
     'https://www.google.com/maps/search/?api=1&amp;query=Dominikon%C5%B3+g.+5%2C+Vilnius',
     'Glaubic ofisas yra Dominikonų g. 5, bet įėjimas į vidinį kiemą yra tarp Vokiečių g. 13 ir 15 pastatų. Įėję pro bromą, eikite tiesiai gilyn iki pat vidinio kiemo galo. Ten pamatysite žalius vartus. Įeikite pro juos ir tiesiai esančiose duryse paspauskite <strong>Nr. 9</strong>.',
     'The Glaubic office is at Dominikonų g. 5, but the entrance to the inner courtyard is between the buildings at Vokiečių g. 13 and 15. Go through the archway and walk straight to the far end of the courtyard. You will see a green gate: go through it and press <strong>No. 9</strong> at the door straight ahead.',
     {'{{mokymu_pavadinimas}}': 'Claude darbe ir kasdienėse užduotyse', '{{data}}': 'spalio 9 d., penktadienis', '{{laikas}}': '9:30', '{{trukme}}': '3,5 val.', '{{lektorius}}': LECT_LT,
      '{{training_name}}': 'Claude for work and everyday tasks', '{{date}}': 'Friday, 9 October', '{{time}}': '9:30', '{{duration}}': '3.5 hours', '{{trainer}}': LECT_EN})
prep('kaunas', 'Kaunas',
     '<a href="https://www.redakcijacoworking.lt/redakcija-laisve/" style="color:#322838;">Redakcija</a> bendradarbystės ir ofisų erdvė, E. Ožeškienės g. 10, Kaunas',
     '<a href="https://www.redakcijacoworking.lt/redakcija-laisve/" style="color:#322838;">Redakcija</a> coworking and office space, E. Ožeškienės g. 10, Kaunas',
     'https://www.google.com/maps/search/?api=1&amp;query=E.+O%C5%BEe%C5%A1kien%C4%97s+g.+10%2C+Kaunas',
     None, None,
     {'{{mokymu_pavadinimas}}': 'Claude darbe ir kasdienėse užduotyse', '{{data}}': 'spalio 8 d., ketvirtadienis', '{{laikas}}': '10:00', '{{trukme}}': '3,5 val.', '{{lektorius}}': LECT_LT,
      '{{training_name}}': 'Claude for work and everyday tasks', '{{date}}': 'Thursday, 8 October', '{{time}}': '10:00', '{{duration}}': '3.5 hours', '{{trainer}}': LECT_EN})

DATE = '2026-10-06'
os.makedirs(OUT, exist_ok=True)
cards = []
for t in TEMPLATES:
    for lang in ('lt', 'en'):
        fn = f'{DATE}-laiskas-{t["key"]}-{lang}.html'
        open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(t[lang])
        ex = t[lang]
        for k, v in t['example'].items(): ex = ex.replace(k, v)
        exfn = f'{DATE}-laiskas-{t["key"]}-{lang}-pavyzdys.html'
        open(os.path.join(OUT, exfn), 'w', encoding='utf-8').write(ex)
    cards.append(t)

def esc(s): return html.escape(s)
rows = ''
for t in cards:
    rows += f'''
  <section class="tpl">
    <h2>{esc(t["name"])}</h2>
    <p class="when">{esc(t["when"])}</p>
    <div class="pair">
      <figure><figcaption><b>LT</b> · Tema: <code>{esc(t["subject_lt"])}</code><br>Laukai: {", ".join(f"<code>{esc(f)}</code>" for f in t["fields_lt"])}</figcaption>
        <iframe src="{DATE}-laiskas-{t["key"]}-lt-pavyzdys.html" title="{esc(t["name"])} LT"></iframe>
        <a href="{DATE}-laiskas-{t["key"]}-lt.html">Šablonas su laukais</a></figure>
      <figure><figcaption><b>EN</b> · Subject: <code>{esc(t["subject_en"])}</code><br>Fields: {", ".join(f"<code>{esc(f)}</code>" for f in t["fields_en"])}</figcaption>
        <iframe src="{DATE}-laiskas-{t["key"]}-en-pavyzdys.html" title="{esc(t["name"])} EN"></iframe>
        <a href="{DATE}-laiskas-{t["key"]}-en.html">Template with fields</a></figure>
    </div>
  </section>'''
preview = f'''<!doctype html>
<html lang="lt">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>GLAUBIC laiškų šablonai</title>
<style>
  body {{ margin: 0; background: #ECEEFB; color: #322838; font-family: 'Hanken Grotesk', Arial, sans-serif; }}
  header {{ max-width: 1240px; margin: 0 auto; padding: 32px 24px 0; }}
  h1 {{ font-family: Manrope, Arial, sans-serif; font-size: 32px; margin: 0; }}
  header p {{ color: #6B6072; margin: 8px 0 0; max-width: 60em; }}
  .tpl {{ max-width: 1240px; margin: 24px auto; padding: 0 24px; }}
  .tpl h2 {{ font-family: Manrope, Arial, sans-serif; margin: 0; font-size: 24px; }}
  .when {{ margin: 6px 0 14px; color: #6B6072; }}
  .pair {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 520px), 1fr)); gap: 20px; }}
  figure {{ margin: 0; background: #fff; border-radius: 16px; padding: 14px; }}
  figcaption {{ font-size: 14px; line-height: 1.6; margin-bottom: 10px; }}
  code {{ background: #ECEEFB; border-radius: 6px; padding: 1px 6px; font-size: 13px; }}
  iframe {{ width: 100%; height: 760px; border: 1px solid #CBC4D0; border-radius: 12px; background: #F5F5F3; }}
  figure > a {{ display: inline-block; margin-top: 8px; font-size: 14px; color: #322838; }}
</style></head>
<body>
<header><h1>GLAUBIC laiškų šablonai</h1>
<p>Kiekvienas laiškas lietuvių ir anglų kalbomis. Peržiūroje laukai užpildyti pavyzdinėmis reikšmėmis; šablonų failuose jie pažymėti {{{{taip}}}} ir juos pakeičia siuntimo sistema.</p></header>
{rows}
</body></html>
'''
open(os.path.join(OUT, f'{DATE}-laisku-sablonu-perziura.html'), 'w', encoding='utf-8').write(preview)
print('ok', len(cards))
