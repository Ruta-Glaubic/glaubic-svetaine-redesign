# GLAUBIC laiškų šablonai: tas pats maketas kaip training-platform/server.js emailLayout().
# Kintami laukai rašomi {{taip}}; juos pakeičia siuntimo sistema.
import os, html
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'laisku-sablonai') if os.path.basename(os.path.dirname(os.path.abspath(__file__))) == 'glaubic-svetaine-redesign' else '/home/user/glaubic-svetaine-redesign/laisku-sablonai'
B = dict(yellow='#FFED00', violet100='#ECEEFB', violet500='#9AA2E6', coral='#FF6A3D', ink800='#322838', ink600='#6B6072', paper='#F5F5F3', white='#FFFFFF')
FONT = "'Hanken Grotesk',Arial,Helvetica,sans-serif"
HEAD = "Manrope,'Hanken Grotesk',Arial,Helvetica,sans-serif"
# Logotipas įdėtas į pačius failus (data URI), kad šablonai ir peržiūra visada rodytų logotipą
# net atidarius be interneto. Siunčiant per server.js naudojamas MAIL_LOGO.url
# (https://glaubic.com/img/glaubic-logotipas.png), nes Gmail data URI paveikslėlių nerodo.
import base64
_LOGO_FILE = os.path.join(OUT, 'glaubic-logotipas.png')
LOGO = 'data:image/png;base64,' + base64.b64encode(open(_LOGO_FILE, 'rb').read()).decode()
FOOT = {
  'lt': ('MB „Glaubic“ · Raitininkų g. 4-74, Vilnius', 'glaubic.com', 'https://glaubic.com'),
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
def cal_button(href, label, bg, border): return f'<table role="presentation" cellpadding="0" cellspacing="0" style="display:inline-table;margin:0 8px 8px 0;"><tr><td style="background:{bg};border:2px solid {border};border-radius:999px;"><a href="{href}" style="display:inline-block;padding:11px 22px;font-family:{FONT};font-size:15px;font-weight:700;color:{B["ink800"]};text-decoration:none;border-radius:999px;">{label}</a></td></tr></table>'
# Kalendoriaus mygtukai. Nuorodas sudaro siuntimo sistema:
#   {{google_kalendoriaus_nuoroda}} = https://calendar.google.com/calendar/render?action=TEMPLATE&text=...&dates=YYYYMMDDTHHMMSS/YYYYMMDDTHHMMSS&ctz=Europe/Vilnius&location=...&details=...
#   {{ics_nuoroda}} = viešas .ics failo adresas (Apple, Outlook)
def calendar_block():
    return ('<p style="margin:0 0 10px;font-weight:700;">Išsisaugokite mokymus kalendoriuje:</p>'
            + cal_button('{{google_kalendoriaus_nuoroda}}', '+ Google kalendorius', B['coral'], B['coral'])
            + cal_button('{{ics_nuoroda}}', '+ Apple / Outlook (.ics)', B['white'], B['ink800']))
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

# Kiekvienas šablonas: failo pavadinimas, tema, laukai ir turinys.
TEMPLATES = []

def sf():
    lt = layout('lt', 'Sąskaita faktūra', '{{saskaitos_numeris}}',
        'Prisegame jūsų sąskaitą faktūrą {{saskaitos_numeris}}.',
        '\n'.join([
            p('Sveiki,'),
            p('dėkojame, kad įsigijote GLAUBIC AI mokymus „{{mokymu_pavadinimas}}“. Prisegame jūsų sąskaitą faktūrą {{saskaitos_numeris}}.'),
            p('Kilus klausimų, drąsiai rašykite.'),
            signature(['Su linkėjimais,', 'Glaubic komanda', link('https://www.glaubic.com', 'www.glaubic.com')]),
        ]))
    TEMPLATES.append(dict(
        key='saskaita-faktura', name='Sąskaita faktūra', when='Kai išrašoma sąskaita faktūra (per 3 darbo dienas po pirkimo). Prisegamas PDF.',
        subject_lt='Sąskaita faktūra {{saskaitos_numeris}}',
        fields_lt=['{{mokymu_pavadinimas}}', '{{saskaitos_numeris}}'],
        example={'{{mokymu_pavadinimas}}': 'Claude verslo ir asmeninėse užduotyse', '{{saskaitos_numeris}}': 'GL26/146'},
        lt=lt))

sf()

PREP_LT = dict(
  topics=['Praktiškai pradėsime taikyti Claude Cowork.',
          'Claude galimybės projektų valdymui.',
          'Claude užklausų formulavimas, kad gautumėte tikslų rezultatą.',
          'Claude ir el. paštas: atsakymų rengimas, šablonai, komunikacijos automatizavimas.',
          'Ataskaitų ir dokumentų kūrimas su Claude.',
          'Bendravimas su klientais: pasiūlymų, pristatymų ir atsakymų rengimas su Claude.',
          'Darbas su failais: dokumentų analizė ir tvarkymas tiesiai jūsų kompiuteryje.',
          '<strong>Svarbiausia:</strong> Claude jungtys (angl. <em>connectors</em>) ir integracija su Canva, Google Workspace, kalendoriais ar kitais įrankiais, kurie prijungiami prie Claude.'],
  fit=['Visiems, kurie dar nėra dirbę su Claude arba dirbo tik su Claude Chat funkcija ir nori daugiau galimybių.',
       'Verslo savininkams, specialistams ir visiems, kurie nori neatsilikti ir tobulinti savo darbo su AI įgūdžius.'])

def prep(city_key, city_lt, place_lt, maps, directions_lt=None, ex=None, calendar=None):
    lt_body = [
        p('Laba diena,'),
        p('ačiū, kad renkatės tobulėti. Siunčiame jums informaciją apie praktinius mokymus „{{mokymu_pavadinimas}}“.'),
        box('Data: <strong>{{data}}, {{laikas}} val.</strong><br>Trukmė: <strong>{{trukme}}</strong><br>Vieta: <strong>' + place_lt + '</strong>', 'Mokymų informacija'),
    ]
    if calendar:
        lt_body += [calendar_block()]
    lt_body += [
        h2('Ką darysime mokymų metu?'), ul(PREP_LT['topics']),
        box('Atsineškite savo kompiuterį ir turėkite mokamą <strong>Claude Pro</strong> prenumeratą.', 'Būtina', B['yellow']),
        h2('Mokymai tinka'), ul(PREP_LT['fit']),
        h2('Lektorius'), p('{{lektorius}}'),
    ]
    if directions_lt:
        lt_body += [h2('Kaip mus rasti'), p(directions_lt)]
    lt_body += [button(maps, 'Atidaryti žemėlapyje'),
                p('Jeigu turėsite klausimų, rašykite ar skambinkite: ' + link('mailto:ai@marketyourvisions.lt', 'ai@marketyourvisions.lt') + ' arba ' + link('tel:+37062469115', '+370 624 69115') + '.'),
                signature(['Su linkėjimais,', 'Glaubic komanda', link('https://www.glaubic.com', 'www.glaubic.com')])]
    lt = layout('lt', 'Pasiruošimas mokymams', '{{mokymu_pavadinimas}} · ' + city_lt, 'Data, vieta ir ką pasiimti į mokymus.', '\n'.join(lt_body))
    TEMPLATES.append(dict(
        key=f'pasiruosimas-{city_key}', name=f'Pasiruošimas: {city_lt}', when='Per 24 val. po pirkimo. Visa informacija apie mokymus.',
        subject_lt='Pasiruošimas mokymams: {{mokymu_pavadinimas}}',
        fields_lt=['{{mokymu_pavadinimas}}', '{{data}}', '{{laikas}}', '{{trukme}}', '{{lektorius}}']
                  + (['{{google_kalendoriaus_nuoroda}}', '{{ics_nuoroda}}'] if calendar else []),
        example=dict(ex, **(calendar or {})), lt=lt))


def remind(city_key, city_lt, place_lt, maps, directions_lt=None, ex=None):
    lt_body = [
        p('Laba diena,'),
        p('primename, kad jau poryt vyks praktiniai mokymai „{{mokymu_pavadinimas}}“. Laukiame jūsų!'),
        box('Data: <strong>{{data}}, {{laikas}} val.</strong><br>Trukmė: <strong>{{trukme}}</strong><br>Vieta: <strong>' + place_lt + '</strong>', 'Mokymų informacija'),
        box(ul(['Pasiimkite savo kompiuterį ir jo įkroviklį.',
                'Įsitikinkite, kad turite mokamą <strong>Claude Pro</strong> prenumeratą ir galite prisijungti prie savo Claude paskyros.']).replace('margin:0 0 16px', 'margin:0'),
            'Prieš mokymus patikrinkite', B['yellow']),
    ]
    if directions_lt:
        lt_body += [h2('Kaip mus rasti'), p(directions_lt)]
    lt_body += [button(maps, 'Atidaryti žemėlapyje'),
                p('Jei negalite dalyvauti, praneškite mums kuo greičiau: registraciją galima perkelti į kitą datą arba vietoj savęs paskirti kitą žmogų.'),
                p('Jeigu turėsite klausimų, rašykite ar skambinkite: ' + link('mailto:ai@marketyourvisions.lt', 'ai@marketyourvisions.lt') + ' arba ' + link('tel:+37062469115', '+370 624 69115') + '.'),
                signature(['Iki susitikimo!', 'Glaubic komanda', link('https://www.glaubic.com', 'www.glaubic.com')])]
    lt = layout('lt', 'Iki mokymų liko 2 dienos', '{{mokymu_pavadinimas}} · ' + city_lt, 'Primename datą, vietą ir ką pasiimti.', '\n'.join(lt_body))
    TEMPLATES.append(dict(
        key=f'priminimas-{city_key}', name=f'Priminimas likus 2 d.: {city_lt}', when='Likus 2 dienoms iki mokymų.',
        subject_lt='Priminimas: mokymai jau poryt',
        fields_lt=['{{mokymu_pavadinimas}}', '{{data}}', '{{laikas}}', '{{trukme}}'],
        example=ex, lt=lt))

LECT_LT = 'Vilhelmas Šulcas, IT projektų vadovas, Code Academy dėstytojas'
CITY_V = ('vilnius', 'Vilnius',
     'Glaubic ofisas, Dominikonų g. 5, Vilnius',
     'https://www.google.com/maps/search/?api=1&amp;query=Dominikon%C5%B3+g.+5%2C+Vilnius',
     'Glaubic ofisas yra Dominikonų g. 5, tačiau į vidinį kiemą įeinama tarp Vokiečių g. 13 ir 15 pastatų. Praėję pro bromą, eikite tiesiai iki pat kiemo galo. Ten pamatysite žalius vartus: įėję pro juos, prie durų priešais paspauskite skambutį <strong>Nr. 9</strong>.',
     {'{{mokymu_pavadinimas}}': 'Claude darbe ir kasdienėse užduotyse', '{{data}}': 'spalio 9 d., penktadienis', '{{laikas}}': '9:30', '{{trukme}}': '3,5 val.', '{{lektorius}}': LECT_LT})
# Pavyzdinės kalendoriaus nuorodos: spalio 9 d. 9:30–13:00 (3,5 val.), Vilniaus laiku
CAL_V = {
    '{{google_kalendoriaus_nuoroda}}': 'https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=Claude%20darbe%20ir%20kasdien%C4%97se%20u%C5%BEduotyse&amp;dates=20261009T093000/20261009T130000&amp;ctz=Europe%2FVilnius&amp;location=Glaubic%20ofisas%2C%20Dominikon%C5%B3%20g.%205%2C%20Vilnius&amp;details=Praktiniai%20GLAUBIC%20mokymai.%20Atsine%C5%A1kite%20savo%20kompiuter%C4%AF%20ir%20tur%C4%97kite%20Claude%20Pro%20prenumerat%C4%85.',
    '{{ics_nuoroda}}': '2026-10-08-kalendorius-pavyzdys-vilnius.ics',
}
prep(*CITY_V, calendar=CAL_V)
CITY_K = ('kaunas', 'Kaunas',
     '<a href="https://www.redakcijacoworking.lt/redakcija-laisve/" style="color:#322838;">Redakcija</a> bendradarbystės ir ofisų erdvė, E. Ožeškienės g. 10, Kaunas',
     'https://www.google.com/maps/search/?api=1&amp;query=E.+O%C5%BEe%C5%A1kien%C4%97s+g.+10%2C+Kaunas',
     'Mokymai vyks <a href="https://www.redakcijacoworking.lt/redakcija-laisve/" style="color:#322838;">Redakcijos</a> bendradarbystės ir ofisų erdvėje, E. Ožeškienės g. 10, Kaunas, <strong>4 aukšte</strong>. Jeigu nerasite, skambinkite lektoriui Vilhelmui tel. <a href="tel:+37062469115" style="color:#322838;">+370 624 69115</a>.',
     {'{{mokymu_pavadinimas}}': 'Claude darbe ir kasdienėse užduotyse', '{{data}}': 'spalio 8 d., ketvirtadienis', '{{laikas}}': '10:00', '{{trukme}}': '3,5 val.', '{{lektorius}}': LECT_LT})
# Pavyzdinės kalendoriaus nuorodos: spalio 8 d. 10:00–13:30 (3,5 val.), Vilniaus laiku
CAL_K = {
    '{{google_kalendoriaus_nuoroda}}': 'https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=Claude%20darbe%20ir%20kasdien%C4%97se%20u%C5%BEduotyse&amp;dates=20261008T100000/20261008T133000&amp;ctz=Europe%2FVilnius&amp;location=Redakcija%2C%20E.%20O%C5%BEe%C5%A1kien%C4%97s%20g.%2010%2C%20Kaunas&amp;details=Praktiniai%20GLAUBIC%20mokymai.%20Atsine%C5%A1kite%20savo%20kompiuter%C4%AF%20ir%20tur%C4%97kite%20Claude%20Pro%20prenumerat%C4%85.',
    '{{ics_nuoroda}}': '2026-10-08-kalendorius-pavyzdys-kaunas.ics',
}
prep(*CITY_K, calendar=CAL_K)
remind(*CITY_V)
remind(*CITY_K)

def gif():
    data = base64.b64encode(open(os.path.join(OUT, '2026-10-06-padeka-lt.gif'), 'rb').read()).decode()
    alt = 'Ačiū, kad mokėtės kartu!'
    return f'<img src="data:image/gif;base64,{data}" alt="{alt}" width="536" style="display:block;width:100%;max-width:536px;height:auto;border:0;border-radius:16px;margin:0 0 24px;">'

# Bendra padėka visiems mokymams. Užduotys ar namų darbai dedami į mokymų medžiagą.
def thanks():
    lt_body = [gif(),
        p('Laba diena,'),
        p('dėkojame, kad dalyvavote mokymuose „{{mokymu_pavadinimas}}“. Tikimės, kad išmoktus dalykus jau spėjote išbandyti savo darbe.'),
        h2('Mokymų medžiaga'),
        p('Skaidres, šablonus ir užduotis rasite paspaudę mygtuką žemiau.'),
        button('{{medziagos_nuoroda}}', 'Atsisiųsti medžiagą'),
        h2('Pasidalinkite įspūdžiais'),
        p('Labai vertintume jūsų atsiliepimą: jis padeda mums tobulėti, o kitiems lengviau apsispręsti. Tai užtruks vos kelias minutes.'),
        button('{{atsiliepimo_nuoroda}}', 'Palikti atsiliepimą'),
        p('Jeigu turėsite klausimų, rašykite ar skambinkite: ' + link('mailto:ai@marketyourvisions.lt', 'ai@marketyourvisions.lt') + ' arba ' + link('tel:+37062469115', '+370 624 69115') + '.'),
        signature(['Su linkėjimais,', 'Glaubic komanda', link('https://www.glaubic.com', 'www.glaubic.com')])]
    lt = layout('lt', 'Ačiū, kad mokėtės kartu!', '{{mokymu_pavadinimas}}', 'Mokymų medžiaga ir trumpas klausimas apie jūsų patirtį.', '\n'.join(lt_body))
    TEMPLATES.append(dict(
        key='padeka', name='Padėka po mokymų (visiems mokymams)', when='3 dienos po mokymų. Padėka, medžiaga ir atsiliepimo forma.',
        subject_lt='Ačiū už mokymus! Jūsų medžiaga ir trumpas klausimas',
        fields_lt=['{{mokymu_pavadinimas}}', '{{medziagos_nuoroda}}', '{{atsiliepimo_nuoroda}}'],
        example={'{{mokymu_pavadinimas}}': 'Claude darbe ir kasdienėse užduotyse', '{{medziagos_nuoroda}}': '#', '{{atsiliepimo_nuoroda}}': '#'},
        lt=lt))

thanks()


def coupon(label, code, amount, valid):
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:24px 0;"><tr>'
            f'<td align="center" style="background:{B["violet100"]};border:2px dashed {B["ink800"]};border-radius:18px;padding:22px 20px;font-family:{FONT};color:{B["ink800"]};">'
            f'<p style="margin:0 0 8px;font-size:13px;font-weight:700;letter-spacing:3px;text-transform:uppercase;">{label}</p>'
            f'<p style="margin:0 0 12px;font-family:{HEAD};font-size:30px;line-height:1.2;font-weight:800;letter-spacing:3px;">{code}</p>'
            f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 auto 10px;"><tr><td style="background:{B["coral"]};border-radius:999px;padding:6px 16px;font-family:{FONT};font-size:16px;font-weight:700;color:{B["ink800"]};">{amount}</td></tr></table>'
            f'<p style="margin:0;font-size:14px;line-height:1.5;">{valid}</p></td></tr></table>')

def referral():
    lt_body = [
        p('Laba diena,'),
        p('džiaugiamės, kad mokėtės kartu su mumis! Jei mokymai jums patiko, pasidalinkite jais: <strong>persiųskite šį laišką draugui(-ei) ar kolegai(-ei)</strong>, kuriems AI galėtų palengvinti darbą.'),
        coupon('Nuolaidos kodas', '{{kupono_kodas}}', '−20 € GLAUBIC mokymams', 'Galioja 30 dienų, iki <strong>{{galioja_iki}}</strong>'),
        p('Kodą panaudokite registruodamiesi į mokymus svetainėje www.glaubic.com.'),
        button('https://www.glaubic.com/#kursai', 'Pasirinkti mokymus'),
        p('Jeigu turėsite klausimų, rašykite ar skambinkite: ' + link('mailto:ai@marketyourvisions.lt', 'ai@marketyourvisions.lt') + ' arba ' + link('tel:+37062469115', '+370 624 69115') + '.'),
        signature(['Ačiū, kad rekomenduojate mus!', 'Glaubic komanda', link('https://www.glaubic.com', 'www.glaubic.com')]),
    ]
    lt = layout('lt', 'Pasidalinkite nuolaida', '20 € draugui(-ei) ar kolegai(-ei)', 'Persiųskite šį laišką: 20 € nuolaida GLAUBIC mokymams, galioja 30 dienų.', '\n'.join(lt_body))
    TEMPLATES.append(dict(
        key='persiusk-draugui', name='Persiųsk draugui(-ei) ar kolegai(-ei)', when='Po mokymų (siuntimo laiką patikslinti). Kodas galioja 30 dienų nuo išsiuntimo.',
        subject_lt='Dovanojame 20 € nuolaidą jūsų draugui(-ei) ar kolegai(-ei)',
        fields_lt=['{{kupono_kodas}}', '{{galioja_iki}}'],
        example={'{{kupono_kodas}}': 'DRAUGAS-7K2M', '{{galioja_iki}}': '2026 m. lapkričio 8 d.'},
        lt=lt))

referral()


def course_card(n, more='Sužinoti daugiau'):
    pre = '{{mokymai_%d_' % n
    t = lambda f: pre + f + '}}'
    names = ('pavadinimas', 'aprasymas', 'data', 'nuoroda')
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 14px;"><tr>'
            f'<td style="border:1px solid {B["ink600"]}33;border-radius:16px;padding:18px 20px;font-family:{FONT};color:{B["ink800"]};background:{B["white"]};">'
            f'<p style="margin:0 0 6px;font-family:{HEAD};font-size:18px;font-weight:800;line-height:1.3;">{t(names[0])}</p>'
            f'<p style="margin:0 0 10px;font-size:15px;line-height:1.55;">{t(names[1])}</p>'
            f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 10px;"><tr><td style="background:{B["yellow"]};border-radius:999px;padding:4px 12px;font-size:13px;font-weight:700;">{t(names[2])}</td></tr></table>'
            f'<a href="{t(names[3])}" style="font-weight:700;color:{B["ink800"]};">{more} →</a></td></tr></table>')

def value():
    lt_body = [
        p('Laba diena,'),
        p('norime pasiteirauti, <strong>kaip jums sekasi dirbti su Claude</strong>. Nuo mokymų praėjo šiek tiek laiko, tad galbūt jau atradote užduočių, kurias Claude padeda atlikti greičiau? O gal kai kur dar kyla klausimų? Parašykite mums, tiesiog atsakydami į šį laišką. Perskaitome kiekvieną laišką ir mielai patarsime.'),
        box('Kasdienėms užduotims susikurkite Claude projektą (Projects): įkelkite dažniausiai naudojamus dokumentus ir instrukcijas, ir kiekvieną kartą nebereikės visko aiškinti iš naujo.', 'Patarimas'),
        h2('Nauji mokymai'),
        p('Ruošiame naujus praktinius mokymus. Peržiūrėkite, kurie iš jų jums būtų naudingi:'),
        course_card(1, 'Sužinoti daugiau'), course_card(2, 'Sužinoti daugiau'),
        h2('Sužinokite pirmieji'),
        p('Prenumeruokite GLAUBIC naujienlaiškį: 1–2 kartus per mėnesį siunčiame naujas mokymų datas ir Glaubic naujienas.'),
        button('https://www.glaubic.com/#naujienlaiskis', 'Prenumeruoti naujienlaiškį'),
        signature(['Sėkmės ir iki susitikimo!', 'Glaubic komanda', link('https://www.glaubic.com', 'www.glaubic.com')]),
    ]
    lt = layout('lt', 'Kaip sekasi?', 'Patarimas, nauji mokymai ir naujienlaiškis', 'Kaip sekasi dirbti su Claude? Patarimas ir nauji GLAUBIC mokymai.', '\n'.join(lt_body))
    TEMPLATES.append(dict(
        key='vertes-laiskas', name='Vertės laiškas: kaip sekasi?', when='Po mokymų (siuntimo laiką patikslinti). Naujų mokymų blokas keičiamas pagal aktualumą.',
        subject_lt='Kaip sekasi dirbti su Claude?',
        fields_lt=['{{mokymai_1_pavadinimas}}', '{{mokymai_1_aprasymas}}', '{{mokymai_1_data}}', '{{mokymai_1_nuoroda}}', '(tas pats su 2)'],
        example={'{{mokymai_1_pavadinimas}}': 'Claude Design', '{{mokymai_1_aprasymas}}': '[Trumpas mokymų aprašymas: 1–2 sakiniai, ką dalyviai išmoks.]', '{{mokymai_1_data}}': 'Datos netrukus', '{{mokymai_1_nuoroda}}': 'https://www.glaubic.com/#kursai',
                 '{{mokymai_2_pavadinimas}}': 'Claude Coding', '{{mokymai_2_aprasymas}}': '[Trumpas mokymų aprašymas: 1–2 sakiniai, ką dalyviai išmoks.]', '{{mokymai_2_data}}': 'Datos netrukus', '{{mokymai_2_nuoroda}}': 'https://www.glaubic.com/#kursai'},
        lt=lt))

value()


DATE = '2026-10-06'
os.makedirs(OUT, exist_ok=True)
cards = []
for t in TEMPLATES:
    fn = f'{DATE}-laiskas-{t["key"]}-lt.html'
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(t['lt'])
    ex = t['lt']
    for k, v in t['example'].items(): ex = ex.replace(k, v)
    exfn = f'{DATE}-laiskas-{t["key"]}-lt-pavyzdys.html'
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
<p>Peržiūroje laukai užpildyti pavyzdinėmis reikšmėmis; šablonų failuose jie pažymėti {{{{taip}}}} ir juos pakeičia siuntimo sistema.</p></header>
{rows}
</body></html>
'''
open(os.path.join(OUT, f'{DATE}-laisku-sablonu-perziura.html'), 'w', encoding='utf-8').write(preview)
print('ok', len(cards))
