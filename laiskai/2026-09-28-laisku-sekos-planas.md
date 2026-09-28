# GLAUBIC mokymų laiškų seka

Kiekvienas laiškas yra atskiras HTML failas šiame aplanke. Atidarykite jį naršyklėje, užpildykite laukus ir nukopijuokite laišką į Gmail.
Bendri duomenys (data, vieta, parašas, nuorodos) išsaugomi naršyklėje, todėl juos pakanka įrašyti vieną kartą. Viršutinė juosta leidžia pereiti nuo vieno laiško prie kito.

## Siuntimo grafikas

Pavyzdys: mokymai **ketvirtadienį, 2026-07-23, 10:00**. Tikslią datą kiekvienas šablonas apskaičiuoja pats.

| # | Failas | Kada siunčiama | Pavyzdinė data | Tema | Kalendoriaus mygtukai | Atsisakymo eilutė |
|---|---|---|---|---|---|---|
| 1 | `2026-09-28-01-patvirtinimas.html` | Iškart po pirkimo | pirkimo diena | Jūsų vieta užtikrinta: … | ✅ | – |
| 2 | `2026-09-28-02-susipazinkime.html` | +1 d. po pirkimo | pirkimo diena + 1 | Susipažinkime? 3 klausimai prieš mokymus | – | – |
| 3 | `2026-09-28-03-pasiruosimas.html` | 7 d. iki mokymų | 2026-07-16 | Po savaitės mokymai: 4 žingsniai pasiruošti | ✅ | – |
| 4 | `2026-09-28-04-priminimas.html` | 1 d. iki mokymų | 2026-07-22 | Rytoj 10:00: … | ✅ | – |
| 5 | `2026-09-28-05-sms.html` | Mokymų dieną, 2 val. iki pradžios | 2026-07-23, 08:00 | (SMS) | – | – |
| 6 | `2026-09-28-06-padeka-ir-medziaga.html` | Tą patį vakarą arba +1 d. | 2026-07-23 vakare | Ačiū! Mokymų medžiaga ir vienas klausimas | – | ✅ |
| 7 | `2026-09-28-07-atsiliepimo-priminimas.html` | +3 d. | 2026-07-26 | Ar galite skirti vieną minutę? | – | ✅ |
| 8 | `2026-09-28-08-vertes-laiskas.html` | +7 d. | 2026-07-30 | Kaip sekasi su Claude? 2 patarimai kasdienai | – | ✅ |
| 9 | `2026-09-28-09-pasiulymas.html` | +14–21 d. | 2026-08-06 – 08-13 | Kitas žingsnis su Claude: … nuolaida | – | ✅ |
| 10 | `2026-09-28-10-rekomendacija-ir-bendruomene.html` | +30 d. | 2026-08-22 | Pažįstate, kam Claude sutaupytų laiko? | – | ✅ |

Pastaba: 7 d. ir vėlesni poslinkiai (7–10 laiškai) skaičiuojami **nuo mokymų dienos**. Tai yra prielaida, nes lentelėje nenurodyta, nuo ko skaičiuoti.

## Taisyklės, kai bilietas nuperkamas vėlai

| Iki mokymų liko | Ką daryti |
|---|---|
| 8 d. ir daugiau | Siųsti visą seką. |
| 2–7 d. | Siųsti 1 laišką, o 2 ir 3 laiškus siųsti tą pačią ar kitą dieną (arba 3 laišką praleisti ir pasiruošimo sąrašą perduoti telefonu). |
| 1 d. ar mažiau | Siųsti tik 1 ir 4 laiškus, 3 laiško sąrašą įdėti kaip priedą arba nurodyti telefonu. |

## Ką reikia paruošti prieš naudojant

Kol šie duomenys neįrašyti, laiškuose rodomos geltonos žymos **[VIETA]**, o generatorius parodo trūkstamų laukų sąrašą.

- [ ] **Parkavimo informacija** (4 laiškas). Nurodėte, kad ją turite, prašome atsiųsti arba įrašyti laukelyje „Parkavimas“.
- [ ] **Susipažinimo anketa** (2 laiškas): pareigos, patirtis su AI, ką norėtų automatizuoti.
- [ ] **Mokymų medžiagos nuoroda** (6 laiškas): skaidrės ir užklausų šablonai.
- [ ] **NPS anketa** (6 laiškas). Jei anketa leidžia užpildyti atsakymą per nuorodą (pvz., Google Forms `entry.XXXX=`), vietoj balo įrašykite `{balas}`. Tada kiekvienas skaičius laiške atidarys anketą su jau pažymėtu balu.
- [ ] **Google atsiliepimo nuoroda** (7 laiškas).
- [ ] **GLAUBIC LinkedIn puslapio adresas** (7 ir 10 laiškai).
- [ ] **Alumni nuolaida, kodas ir terminas** (9 laiškas).
- [ ] **.ics failo adresas** (1, 3 ir 4 laiškai). Atsisiųskite failą mygtuku „Atsisiųsti .ics“ ir įkelkite į svetainę.

## Prielaidos ir rizikos

- **Vilhelmo parašas:** jame nurodyti tie patys telefonai ir GLAUBIC Instagram, nes asmeninių Vilhelmo nuorodų neturiu. Patikrinkite.
- **Pažengusiųjų kursų pavadinimai** 9 laiške paimti iš svetainės maketo („AI agentai ir Claude kartu“, „Susikurkite AI agentą per 3 val.“).
- **3 laiškas** teigia, kad Claude Cowork ir darbas su failais veikia Claude Desktop programoje. Prieš siunčiant verta patikrinti, ar tai vis dar tiesa, nes Claude funkcijos keičiasi.
- **Atsisakymo eilutė:** 6–10 laiškai yra rinkodaros laiškai, todėl juose yra atsisakymo eilutė (BDAR, Elektroninių ryšių įstatymas). Jei naudojate MailerLite ar Brevo, įrašykite jų atsisakymo nuorodą.
- **SMS** rašoma be lietuviškų raidžių, kad tilptų į vieną žinutę (iki 160 simbolių).
- **Rankinis siuntimas:** 10 laiškų kiekvienam dalyviui per Gmail reikalauja daug rankinio darbo. Didėjant dalyvių skaičiui rekomenduojame seką automatizuoti (MailerLite, Brevo arba n8n). Mygtukas „Kopijuoti HTML“ jau paruošia šiems įrankiams tinkamą kodą.
