/*
 * GLAUBIC mokymų laiškų seka: bendra dalis visiems 10 šablonų.
 * Kiekvienas šablonas kviečia GLAUBIC.page({...}) su savo tema, laukais ir turiniu.
 * Įvesti duomenys saugomi naršyklėje (localStorage), todėl bendrus laukus užtenka įrašyti vieną kartą.
 */
(function () {
  "use strict";

  // Brandbook spalvos laiškui (el. pašto klientai nepalaiko CSS kintamųjų)
  var C = {
    ink: "#322838", inkSoft: "#6B6072", violet: "#9AA2E6", violet200: "#D3D7F4", violet100: "#ECEEFB",
    coral: "#FF6A3D", yellow: "#FFED00", paper: "#F5F5F3", white: "#FFFFFF", line: "#CBC4D0"
  };
  var HEAD = "Manrope, 'Helvetica Neue', Arial, sans-serif";
  var BODY = "'Hanken Grotesk', 'Helvetica Neue', Arial, sans-serif";
  var TZ = "Europe/Vilnius";
  var STORE = "glaubic-laiskai-v1";

  var MONTHS = ["sausio", "vasario", "kovo", "balandžio", "gegužės", "birželio", "liepos", "rugpjūčio", "rugsėjo", "spalio", "lapkričio", "gruodžio"];
  var DAYS_ACC = ["sekmadienį", "pirmadienį", "antradienį", "trečiadienį", "ketvirtadienį", "penktadienį", "šeštadienį"];
  var DAYS_NOM = ["Sekmadienis", "Pirmadienis", "Antradienis", "Trečiadienis", "Ketvirtadienis", "Penktadienis", "Šeštadienis"];

  // Sekos žingsniai: base = nuo ko skaičiuojama siuntimo diena, days = poslinkis dienomis
  var PAGES = [
    { no: 1, file: "2026-09-28-01-patvirtinimas.html", name: "Patvirtinimas", when: "Iškart po pirkimo", base: "purchase", days: 0 },
    { no: 2, file: "2026-09-28-02-susipazinkime.html", name: "Susipažinkime", when: "+1 d. po pirkimo", base: "purchase", days: 1 },
    { no: 3, file: "2026-09-28-03-pasiruosimas.html", name: "Pasiruošimas", when: "7 d. iki mokymų", base: "training", days: -7 },
    { no: 4, file: "2026-09-28-04-priminimas.html", name: "Priminimas", when: "1 d. iki mokymų", base: "training", days: -1 },
    { no: 5, file: "2026-09-28-05-sms.html", name: "SMS", when: "Mokymų dieną, 2 val. iki pradžios", base: "training", days: 0, hoursBefore: 2 },
    { no: 6, file: "2026-09-28-06-padeka-ir-medziaga.html", name: "Padėka ir medžiaga", when: "Tą patį vakarą arba +1 d.", base: "training", days: 0 },
    { no: 7, file: "2026-09-28-07-atsiliepimo-priminimas.html", name: "Atsiliepimas", when: "+3 d. po mokymų", base: "training", days: 3 },
    { no: 8, file: "2026-09-28-08-vertes-laiskas.html", name: "Vertės laiškas", when: "+7 d. po mokymų", base: "training", days: 7 },
    { no: 9, file: "2026-09-28-09-pasiulymas.html", name: "Pasiūlymas", when: "+14–21 d. po mokymų", base: "training", days: 14, daysTo: 21 },
    { no: 10, file: "2026-09-28-10-rekomendacija-ir-bendruomene.html", name: "Rekomendacija", when: "+30 d. po mokymų", base: "training", days: 30 }
  ];

  var SIGNERS = {
    sonata: {
      name: "Sonata Šulcė", role: "GLAUBIC Co-Founder",
      links: [["Substack", "https://substack.com/@sonatasulce"], ["Instagram", "https://www.instagram.com/sonata.sulce/"], ["LinkedIn", "https://www.linkedin.com/in/sonata-%C5%A1ulc%C4%97-8576b391/"]]
    },
    vilhelmas: {
      name: "Vilhelmas Šulcas", role: "GLAUBIC įkūrėjas, AI mokymų lektorius",
      links: [["Instagram", "https://www.instagram.com/glaubicai/"]]
    }
  };

  // Visi laukai. group: kurioje formos dalyje rodomi. Tuščias laukas su ph laiške virsta geltona [VIETA] žyma.
  var FIELDS = {
    signer: { group: "Laiškas", label: "Parašas", type: "select", options: [["sonata", "Sonata Šulcė"], ["vilhelmas", "Vilhelmas Šulcas"]], def: "sonata" },
    firstName: { group: "Laiškas", label: "Dalyvio vardas šauksmininku (nebūtina)", def: "", hint: "pvz. „Rūta“ → „Sveiki, Rūta,“. Tuščia → „Sveiki,“" },
    purchaseDate: { group: "Laiškas", label: "Pirkimo data", type: "date", def: "", hint: "Reikalinga tik 1–2 laiškų siuntimo dienai apskaičiuoti." },
    title: { group: "Mokymai", label: "Mokymų pavadinimas", def: "Claude galimybės verslo ir kasdieninėse užduotyse" },
    date: { group: "Mokymai", label: "Data", type: "date", def: "2026-07-23" },
    time: { group: "Mokymai", label: "Pradžia", type: "time", def: "10:00" },
    hours: { group: "Mokymai", label: "Trukmė, val.", type: "number", def: "3.5" },
    agenda: { group: "Mokymai", label: "Programa (viena eilutė = vienas punktas)", type: "textarea", def: [
      "Praktiškai pradėsime taikyti Claude Cowork.",
      "Claude galimybės projektų valdymui.",
      "Claude užklausų formulavimas, kad gautumėte tikslų rezultatą.",
      "Claude ir el. pašto valdymas: atsakymų rengimas, šablonai, komunikacijos automatizavimas.",
      "Claude ataskaitų ir dokumentų kūrimui.",
      "Claude klientų komunikacijai: pasiūlymų, pristatymų ir atsakymų rengimas.",
      "Claude darbas su failais: dokumentų analizė ir tvarkymas tiesiai iš savo kompiuterio.",
      "Svarbiausia – Claude connectoriai ir integracija su Canva, Google Workspace, kalendoriais ar kitais įrankiais, kurie prijungiami prie Claude."
    ].join("\n") },
    required: { group: "Mokymai", label: "Būtina", def: "Turėti savo kompiuterį ir mokamą Claude versiją PRO." },
    venue: { group: "Vieta", label: "Erdvės pavadinimas", def: "Redakcija" },
    venueUrl: { group: "Vieta", label: "Erdvės nuoroda", type: "url", def: "https://www.redakcijacoworking.lt/redakcija-laisve/" },
    venueNote: { group: "Vieta", label: "Erdvės aprašymas", def: "bendradarbystės ir ofisų erdvė" },
    address: { group: "Vieta", label: "Adresas", def: "E. Ožeškienės g. 10, Kaunas", hint: "Google Maps nuoroda sudaroma automatiškai." },
    entryNote: { group: "Vieta", label: "Pastaba apie įėjimą", def: "Pridedame ekrano nuotrauką, pro kur įeiti." },
    parking: { group: "Vieta", label: "Parkavimas", type: "textarea", def: "", ph: "PARKAVIMO INFORMACIJA" },
    icsUrl: { group: "Nuorodos", label: ".ics failo adresas (Apple / Outlook)", type: "url", def: "", hint: "Atsisiųskite .ics, įkelkite į svetainę ir įklijuokite adresą. Tuščia → Apple mygtuko nebus." },
    logoUrl: { group: "Nuorodos", label: "Logotipo PNG adresas (nebūtina)", type: "url", def: "", hint: "Tuščia → tekstinis GLAUBIC ženklas." },
    orderNo: { group: "Užsakymas", label: "Užsakymo / bilieto Nr. (nebūtina)", def: "" },
    ticketUrl: { group: "Užsakymas", label: "Bilieto nuoroda (nebūtina)", type: "url", def: "", hint: "Jei bilietą išduoda mokėjimo sistema." },
    invoiceNote: { group: "Užsakymas", label: "Pastaba apie sąskaitą", def: "Sąskaitą faktūrą rasite prisegtą prie šio laiško." },
    surveyUrl: { group: "Nuorodos", label: "Susipažinimo anketos nuoroda", type: "url", def: "", ph: "NUORODA Į ANKETĄ" },
    materialsUrl: { group: "Nuorodos", label: "Mokymų medžiagos nuoroda", type: "url", def: "", ph: "NUORODA Į MEDŽIAGĄ" },
    npsUrl: { group: "Nuorodos", label: "Atsiliepimų (NPS) anketos nuoroda", type: "url", def: "", ph: "NUORODA Į NPS ANKETĄ", hint: "Jei nuorodoje įrašysite {balas}, kiekvienas skaičius atidarys anketą su jau pažymėtu balu." },
    reviewUrl: { group: "Nuorodos", label: "Google atsiliepimo nuoroda", type: "url", def: "", ph: "NUORODA Į GOOGLE ATSILIEPIMĄ" },
    companyLinkedin: { group: "Nuorodos", label: "GLAUBIC LinkedIn puslapis", type: "url", def: "", ph: "GLAUBIC LINKEDIN" },
    tip1Title: { group: "Patarimai", label: "1 patarimo antraštė", def: "Sukurkite projektą pasikartojančioms užduotims" },
    tip1Text: { group: "Patarimai", label: "1 patarimo tekstas", type: "textarea", def: "Claude projekte (Projects) įkelkite savo šablonus, kainoraščius ar stiliaus pavyzdžius ir parašykite nuolatines instrukcijas. Tada nebereikės kiekvieną kartą aiškinti iš naujo." },
    tip2Title: { group: "Patarimai", label: "2 patarimo antraštė", def: "Paprašykite Claude pirmiausia paklausti" },
    tip2Text: { group: "Patarimai", label: "2 patarimo tekstas", type: "textarea", def: "Užklausos pabaigoje parašykite: „Prieš atsakydamas užduok man 3 klausimus, kurių reikia geram rezultatui.“ Taip gausite daug tikslesnį atsakymą." },
    discount: { group: "Pasiūlymas", label: "Alumni nuolaida", def: "", ph: "NUOLAIDA", hint: "pvz. „15 %“" },
    discountCode: { group: "Pasiūlymas", label: "Nuolaidos kodas", def: "", ph: "KODAS" },
    deadline: { group: "Pasiūlymas", label: "Pasiūlymas galioja iki", type: "date", def: "", ph: "TERMINAS" },
    offerUrl: { group: "Pasiūlymas", label: "Pasiūlymo nuoroda", type: "url", def: "https://www.glaubic.com" },
    referralBenefit: { group: "Rekomendacija", label: "Nauda rekomenduojant (nebūtina)", def: "", hint: "pvz. „Jūsų rekomenduotas kolega gaus 10 % nuolaidą.“ Tuščia → sakinio nebus." },
    scheduleUrl: { group: "Rekomendacija", label: "Mokymų tvarkaraščio nuoroda", type: "url", def: "https://www.glaubic.com" },
    unsubscribeUrl: { group: "Nuorodos", label: "Atsisakymo nuoroda (nebūtina)", type: "url", def: "", hint: "Tuščia → prašoma atsakyti žodžiu „Atsisakyti“." },
    smsPhone: { group: "SMS", label: "Telefonas SMS žinutėje", def: "+37062910499" }
  };
  var GROUP_ORDER = ["Laiškas", "Mokymai", "Vieta", "Užsakymas", "Nuorodos", "Patarimai", "Pasiūlymas", "Rekomendacija", "SMS"];

  // ---------- Pagalbinės funkcijos ----------
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function loadStore() { try { return JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) { return {}; } }
  function saveStore(v) { try { localStorage.setItem(STORE, JSON.stringify(v)); } catch (e) {} }

  // Datos skaičiuojamos kaip „sieninis“ laikas per UTC, kad naršyklės laiko juosta neturėtų įtakos
  function parseDate(s) {
    if (!s) return null;
    var d = s.split("-").map(Number);
    return new Date(Date.UTC(d[0], d[1] - 1, d[2]));
  }
  function addDays(dt, n) { return new Date(dt.getTime() + n * 86400000); }
  function stamp(dt) { return dt.getUTCFullYear() + pad(dt.getUTCMonth() + 1) + pad(dt.getUTCDate()) + "T" + pad(dt.getUTCHours()) + pad(dt.getUTCMinutes()) + "00"; }
  function isoDate(dt) { return dt.getUTCFullYear() + "-" + pad(dt.getUTCMonth() + 1) + "-" + pad(dt.getUTCDate()); }
  function hhmm(dt) { return pad(dt.getUTCHours()) + ":" + pad(dt.getUTCMinutes()); }
  function dateAcc(dt) { return MONTHS[dt.getUTCMonth()] + " " + dt.getUTCDate() + " d., " + DAYS_ACC[dt.getUTCDay()]; }
  function dateNom(dt) { return DAYS_NOM[dt.getUTCDay()] + ", " + MONTHS[dt.getUTCMonth()] + " " + dt.getUTCDate() + " d."; }
  function dateShort(dt) { return MONTHS[dt.getUTCMonth()] + " " + dt.getUTCDate() + " d."; }

  function values() {
    var st = loadStore(), x = {};
    Object.keys(FIELDS).forEach(function (k) { x[k] = (st[k] !== undefined ? st[k] : FIELDS[k].def); });
    var d = (x.date || FIELDS.date.def).split("-").map(Number);
    var t = (x.time || FIELDS.time.def).split(":").map(Number);
    var hours = parseFloat(x.hours) || 1;
    x.start = new Date(Date.UTC(d[0], d[1] - 1, d[2], t[0], t[1]));
    x.end = new Date(x.start.getTime() + Math.round(hours * 60) * 60000);
    x.hoursText = String(hours).replace(".", ",");
    x.agendaList = String(x.agenda).split("\n").map(function (l) { return l.trim(); }).filter(Boolean);
    x.location = [x.venue, x.address].filter(Boolean).join(", ");
    x.mapsUrl = "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(x.address);
    x.sig = SIGNERS[x.signer] || SIGNERS.sonata;
    return x;
  }

  // ---------- Kalendorius ----------
  function plainDescription(x) {
    var lines = ["Praktiniai GLAUBIC mokymai. Trukmė: " + x.hoursText + " val."];
    if (x.required) lines.push("Būtina: " + x.required);
    lines.push("Klausimai: +37062910499, +37062469115", "www.glaubic.com");
    return lines.join("\n");
  }
  function googleUrl(x) {
    return "https://calendar.google.com/calendar/render?action=TEMPLATE" +
      "&text=" + encodeURIComponent(x.title) +
      "&dates=" + stamp(x.start) + "/" + stamp(x.end) +
      "&ctz=" + encodeURIComponent(TZ) +
      "&location=" + encodeURIComponent(x.location) +
      "&details=" + encodeURIComponent(plainDescription(x));
  }
  // RFC 5545: kabliataškiai ir kableliai ekranuojami, eilutės lankstomos po 75 baitus
  function icsText(s) { return String(s).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n"); }
  function fold(line) {
    var enc = new TextEncoder(), out = [], cur = "";
    for (var ch of line) {
      if (enc.encode(cur + ch).length > 75) { out.push(cur); cur = " " + ch; }
      else cur += ch;
    }
    out.push(cur);
    return out.join("\r\n");
  }
  function buildIcs(x) {
    var now = new Date();
    var dtstamp = now.getUTCFullYear() + pad(now.getUTCMonth() + 1) + pad(now.getUTCDate()) + "T" + pad(now.getUTCHours()) + pad(now.getUTCMinutes()) + pad(now.getUTCSeconds()) + "Z";
    var lines = [
      "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//GLAUBIC//Mokymai//LT", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
      "BEGIN:VTIMEZONE", "TZID:" + TZ,
      "BEGIN:DAYLIGHT", "TZOFFSETFROM:+0200", "TZOFFSETTO:+0300", "TZNAME:EEST", "DTSTART:19700329T030000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU", "END:DAYLIGHT",
      "BEGIN:STANDARD", "TZOFFSETFROM:+0300", "TZOFFSETTO:+0200", "TZNAME:EET", "DTSTART:19701025T040000", "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU", "END:STANDARD",
      "END:VTIMEZONE",
      "BEGIN:VEVENT",
      "UID:mokymai-" + stamp(x.start) + "@glaubic.com",
      "DTSTAMP:" + dtstamp,
      "DTSTART;TZID=" + TZ + ":" + stamp(x.start),
      "DTEND;TZID=" + TZ + ":" + stamp(x.end),
      "SUMMARY:" + icsText(x.title),
      "LOCATION:" + icsText(x.location),
      "DESCRIPTION:" + icsText(plainDescription(x)),
      "URL:https://www.glaubic.com",
      "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + icsText(x.title), "TRIGGER:-PT1H", "END:VALARM",
      "END:VEVENT", "END:VCALENDAR"
    ];
    return lines.map(fold).join("\r\n") + "\r\n";
  }

  // ---------- Laiško blokai (tik lentelės ir įterpti stiliai, kad veiktų Gmail) ----------
  function makeKit(x, missing) {
    var link = "color:" + C.ink + ";text-decoration:underline;";
    var P = "margin:0 0 16px;font-family:" + BODY + ";font-size:16px;line-height:24px;color:" + C.ink + ";";

    function mark(label) {
      if (missing.indexOf(label) < 0) missing.push(label);
      return '<span style="background:' + C.yellow + ';border:1px dashed ' + C.ink + ';padding:0 4px;font-weight:700;">[' + esc(label) + ']</span>';
    }
    var k = {
      C: C, x: x, link: link, esc: esc,
      // Teksto reikšmė arba geltona žyma, jei laukas tuščias
      v: function (key) {
        var val = x[key];
        if (val && String(val).trim()) {
          return FIELDS[key] && FIELDS[key].type === "date" ? esc(dateShort(parseDate(val))) : esc(val);
        }
        return mark(FIELDS[key].ph || FIELDS[key].label.toUpperCase());
      },
      // Nuoroda arba "#", jei laukas tuščias (žyma įtraukiama į trūkstamų sąrašą)
      u: function (key) {
        var val = String(x[key] || "").trim();
        if (val) return val;
        var label = FIELDS[key].ph || FIELDS[key].label.toUpperCase();
        if (missing.indexOf(label) < 0) missing.push(label);
        return "#";
      },
      p: function (html, extra) { return '<tr><td style="padding:0 32px;"><p style="' + P + (extra || "") + '">' + html + '</p></td></tr>'; },
      small: function (html) { return '<tr><td style="padding:0 32px;"><p style="margin:0 0 16px;font-family:' + BODY + ';font-size:14px;line-height:21px;color:' + C.inkSoft + ';">' + html + '</p></td></tr>'; },
      heading: function (text) {
        return '<tr><td style="padding:12px 32px 0;"><p style="margin:0 0 12px;font-family:' + HEAD + ';font-size:13px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:' + C.ink + ';">' + text + '</p></td></tr>';
      },
      title: function (text) {
        return '<tr><td style="padding:0 32px;"><p style="margin:0 0 16px;font-family:' + HEAD + ';font-size:26px;font-weight:700;line-height:32px;letter-spacing:-0.02em;color:' + C.ink + ';">' + text + '</p></td></tr>';
      },
      button: function (href, label, variant) {
        var bg = variant === "outline" ? C.white : (variant === "violet" ? C.violet200 : C.coral);
        var border = variant === "outline" ? C.ink : bg;
        return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="display:inline-table;margin:0 8px 10px 0;"><tr>' +
          '<td align="center" bgcolor="' + bg + '" style="background:' + bg + ';border:2px solid ' + border + ';border-radius:999px;">' +
          '<a href="' + esc(href) + '" target="_blank" style="display:inline-block;padding:13px 24px;font-family:' + BODY + ';font-size:16px;font-weight:700;line-height:20px;color:' + C.ink + ';text-decoration:none;border-radius:999px;">' + label + '</a>' +
          '</td></tr></table>';
      },
      buttons: function (html) { return '<tr><td style="padding:4px 32px 12px;">' + html + '</td></tr>'; },
      card: function (inner, opts) {
        opts = opts || {};
        var bg = opts.bg || C.violet200;
        var accent = opts.accent ? "border-left:6px solid " + opts.accent + ";" : "";
        return '<tr><td style="padding:4px 24px 20px;">' +
          '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="' + bg + '" style="background:' + bg + ';border-radius:20px;' + accent + '">' +
          '<tr><td style="padding:22px 24px;">' + inner + '</td></tr></table></td></tr>';
      },
      cardLabel: function (text) { return '<p style="margin:0 0 8px;font-family:' + HEAD + ';font-size:13px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:' + C.ink + ';">' + text + '</p>'; },
      cardTitle: function (text) { return '<p style="margin:0 0 8px;font-family:' + HEAD + ';font-size:20px;font-weight:700;line-height:26px;letter-spacing:-0.02em;color:' + C.ink + ';">' + text + '</p>'; },
      cardText: function (html, last) { return '<p style="margin:0 0 ' + (last ? 0 : 14) + 'px;font-family:' + BODY + ';font-size:16px;line-height:24px;color:' + C.ink + ';">' + html + '</p>'; },
      bullets: function (items, inCard) {
        var rows = items.map(function (item) {
          return '<tr><td valign="top" width="22" style="padding:0 0 10px;"><span style="display:inline-block;width:10px;height:10px;border-radius:999px;background:' + (inCard ? C.ink : C.violet) + ';margin-top:7px;"></span></td>' +
            '<td style="padding:0 0 10px;font-family:' + BODY + ';font-size:16px;line-height:24px;color:' + C.ink + ';">' + item + '</td></tr>';
        }).join("");
        var table = '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">' + rows + '</table>';
        return inCard ? table : '<tr><td style="padding:0 32px 8px;">' + table + '</td></tr>';
      },
      // Sunumeruoti žingsniai: [{title, text}]
      steps: function (items) {
        var rows = items.map(function (it, i) {
          return '<tr><td valign="top" width="48" style="padding:0 0 18px;">' +
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" valign="middle" width="34" height="34" bgcolor="' + C.violet200 + '" style="width:34px;height:34px;border-radius:999px;background:' + C.violet200 + ';font-family:' + HEAD + ';font-size:15px;font-weight:700;color:' + C.ink + ';">' + (i + 1) + '</td></tr></table></td>' +
            '<td style="padding:4px 0 18px;"><p style="margin:0 0 4px;font-family:' + HEAD + ';font-size:17px;font-weight:700;line-height:24px;color:' + C.ink + ';">' + it.title + '</p>' +
            '<p style="margin:0;font-family:' + BODY + ';font-size:15px;line-height:23px;color:' + C.ink + ';">' + it.text + '</p></td></tr>';
        }).join("");
        return '<tr><td style="padding:0 32px 4px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">' + rows + '</table></td></tr>';
      },
      // Renginio kortelė: kada, trukmė, vieta ir (nebūtinai) kalendoriaus mygtukai
      eventCard: function (withCalendar) {
        var s = x.start;
        var venue = x.venueUrl ? '<a href="' + esc(x.venueUrl) + '" target="_blank" style="' + link + '">' + esc(x.venue) + '</a>' : esc(x.venue);
        var address = x.address ? ' <a href="' + esc(x.mapsUrl) + '" target="_blank" style="' + link + '">' + esc(x.address) + '</a>' : "";
        var cell = "font-family:" + BODY + ";font-size:16px;line-height:24px;color:" + C.ink + ";";
        var lab = "padding:0 16px 8px 0;font-family:" + BODY + ";font-size:14px;line-height:24px;color:" + C.inkSoft + ";";
        var inner =
          '<p style="margin:0 0 6px;font-family:' + BODY + ';font-size:14px;line-height:20px;color:' + C.ink + ';">Praktiniai mokymai</p>' +
          '<p style="margin:0 0 16px;font-family:' + HEAD + ';font-size:22px;font-weight:700;line-height:28px;letter-spacing:-0.02em;color:' + C.ink + ';">' + esc(x.title) + '</p>' +
          '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 ' + (withCalendar ? 18 : 0) + 'px;">' +
            '<tr><td valign="top" style="' + lab + '">Kada</td><td style="padding:0 0 8px;' + cell + 'font-weight:700;">' + esc(dateNom(s)) + ', ' + hhmm(s) + '–' + hhmm(x.end) + '</td></tr>' +
            '<tr><td valign="top" style="' + lab + '">Trukmė</td><td style="padding:0 0 8px;' + cell + 'font-weight:700;">' + esc(x.hoursText) + ' val.</td></tr>' +
            '<tr><td valign="top" style="' + lab + 'padding-bottom:0;">Vieta</td><td style="' + cell + '">' + venue + (x.venueNote ? " " + esc(x.venueNote) : "") + (address ? "," + address : "") + '</td></tr>' +
          '</table>';
        if (withCalendar) {
          inner += '<p style="margin:0 0 10px;font-family:' + BODY + ';font-size:14px;font-weight:700;color:' + C.ink + ';">Įsitraukite į savo kalendorių:</p>' +
            k.button(googleUrl(x), "+ Google Calendar") +
            (x.icsUrl ? k.button(x.icsUrl, "+ Apple / Outlook", "outline") : "");
        }
        return k.card(inner);
      },
      requiredCard: function () {
        if (!x.required) return "";
        return k.card(k.cardLabel("Būtina") + k.cardText(esc(x.required), true), { bg: C.violet100, accent: C.coral });
      },
      dateAcc: dateAcc(x.start), dateNom: dateNom(x.start), dateShort: dateShort(x.start), time: hhmm(x.start), endTime: hhmm(x.end),
      googleUrl: googleUrl(x)
    };
    return k;
  }

  function signature(x, k) {
    var sig = x.sig;
    var socials = sig.links.map(function (l) { return '<a href="' + esc(l[1]) + '" target="_blank" style="' + k.link + '">' + l[0] + '</a>'; }).join(" | ");
    return '<tr><td style="padding:12px 32px 32px;">' +
      '<p style="margin:0 0 4px;font-family:' + BODY + ';font-size:16px;line-height:24px;color:' + C.ink + ';">Su linkėjimais,</p>' +
      '<p style="margin:0;font-family:' + HEAD + ';font-size:17px;font-weight:700;line-height:24px;color:' + C.ink + ';">' + esc(sig.name) + '</p>' +
      '<p style="margin:0 0 12px;font-family:' + BODY + ';font-size:14px;line-height:20px;color:' + C.inkSoft + ';">' + esc(sig.role) + '</p>' +
      '<p style="margin:0 0 4px;font-family:' + BODY + ';font-size:14px;line-height:22px;color:' + C.ink + ';">' +
        '<a href="tel:+37062910499" style="' + k.link + '">+370 629 10499</a>, <a href="tel:+37062469115" style="' + k.link + '">+370 624 69115</a><br>' +
        '<a href="https://www.glaubic.com" target="_blank" style="' + k.link + 'font-weight:700;">www.glaubic.com</a></p>' +
      '<p style="margin:0;font-family:' + BODY + ';font-size:14px;line-height:22px;color:' + C.ink + ';">' + socials + '</p>' +
    '</td></tr>';
  }

  function unsubscribe(x, k) {
    var how = x.unsubscribeUrl
      ? '<a href="' + esc(x.unsubscribeUrl) + '" target="_blank" style="color:' + C.inkSoft + ';text-decoration:underline;">atsisakykite čia</a>'
      : "atsakykite į šį laišką žodžiu „Atsisakyti“";
    return '<tr><td align="center" style="padding:16px 32px 0;"><p style="margin:0;font-family:' + BODY + ';font-size:12px;line-height:18px;color:' + C.inkSoft + ';">' +
      'Gavote šį laišką, nes dalyvavote GLAUBIC mokymuose. Jei nebenorite gauti tokių laiškų, ' + how + '.</p></td></tr>';
  }

  function shell(cfg, x, k, bodyRows, preheader) {
    var logo = x.logoUrl
      ? '<img src="' + esc(x.logoUrl) + '" alt="GLAUBIC" width="140" style="display:block;width:140px;height:auto;border:0;">'
      : '<span style="font-family:' + HEAD + ';font-size:22px;font-weight:700;letter-spacing:0.12em;color:' + C.ink + ';">GLAUBIC</span>';
    var pillBg = cfg.pillColor === "violet" ? C.violet200 : (cfg.pillColor === "coral" ? C.coral : C.yellow);
    var greeting = "Sveiki" + (x.firstName && x.firstName.trim() ? ", " + esc(x.firstName.trim()) : "") + ",";
    return '' +
      (preheader ? '<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">' + esc(preheader) + '</div>' : "") +
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="' + C.paper + '" style="background:' + C.paper + ';">' +
      '<tr><td align="center" style="padding:24px 12px;">' +
      '<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:' + C.white + ';border-radius:24px;">' +
      '<tr><td style="padding:28px 32px 24px;">' +
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>' +
        '<td valign="middle">' + logo + '</td>' +
        '<td align="right" valign="middle"><span style="display:inline-block;padding:6px 14px;border-radius:999px;background:' + pillBg + ';font-family:' + BODY + ';font-size:13px;font-weight:700;color:' + C.ink + ';">' + esc(cfg.pill) + '</span></td>' +
        '</tr></table>' +
      '</td></tr>' +
      k.p(greeting) +
      bodyRows +
      signature(x, k) +
      '</table>' +
      '<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;">' +
      (cfg.marketing ? unsubscribe(x, k) : "") +
      '</table>' +
      '</td></tr></table>';
  }

  // ---------- SMS ----------
  var TRANSLIT = { "ą": "a", "č": "c", "ę": "e", "ė": "e", "į": "i", "š": "s", "ų": "u", "ū": "u", "ž": "z", "Ą": "A", "Č": "C", "Ę": "E", "Ė": "E", "Į": "I", "Š": "S", "Ų": "U", "Ū": "U", "Ž": "Z", "„": "\"", "“": "\"", "–": "-" };
  function translit(s) { return String(s).replace(/[ąčęėįšųūžĄČĘĖĮŠŲŪŽ„“–]/g, function (c) { return TRANSLIT[c]; }); }

  // ---------- Puslapis ----------
  function sendDate(meta, x) {
    if (meta.base === "purchase") {
      var pd = parseDate(x.purchaseDate);
      if (!pd) return meta.days ? "įrašykite pirkimo datą" : "iškart po pirkimo";
      return isoDate(addDays(pd, meta.days));
    }
    var td = parseDate(isoDate(x.start));
    var out = isoDate(addDays(td, meta.days));
    if (meta.daysTo) out += " – " + isoDate(addDays(td, meta.daysTo));
    if (meta.hoursBefore) out += ", " + hhmm(new Date(x.start.getTime() - meta.hoursBefore * 3600000));
    return out;
  }

  function page(cfg) {
    var meta = PAGES.filter(function (p) { return p.no === cfg.no; })[0];
    document.title = pad(meta.no) + " " + meta.name + " – GLAUBIC laiškai";

    var nav = PAGES.map(function (p) {
      return '<a href="' + p.file + '"' + (p.no === meta.no ? ' aria-current="page"' : "") + '><b>' + p.no + '</b> ' + esc(p.name) + '</a>';
    }).join("");

    var fieldKeys = cfg.fields.slice();
    if (!cfg.sms) ["signer", "firstName"].forEach(function (k) { if (fieldKeys.indexOf(k) < 0) fieldKeys.unshift(k); });
    if (meta.base === "purchase" && fieldKeys.indexOf("purchaseDate") < 0) fieldKeys.push("purchaseDate");

    var groups = {};
    fieldKeys.forEach(function (key) { var g = FIELDS[key].group; (groups[g] = groups[g] || []).push(key); });
    var formHtml = GROUP_ORDER.filter(function (g) { return groups[g]; }).map(function (g, i) {
      return '<details class="group"' + (i < 2 ? " open" : "") + '><summary>' + g + '</summary>' + groups[g].map(fieldHtml).join("") + '</details>';
    }).join("");

    document.body.innerHTML =
      '<nav class="seq-nav" aria-label="Laiškų seka">' + nav + '</nav>' +
      '<div class="app">' +
        '<form class="panel" id="form" autocomplete="off">' +
          '<h1>' + meta.no + '. ' + esc(meta.name) + '</h1>' +
          '<p class="goal">' + esc(cfg.goal) + '</p>' +
          '<div class="meta">' +
            '<div class="meta-row"><span>Kada siunčiama</span><output>' + esc(meta.when) + '</output></div>' +
            '<div class="meta-row"><span>Siuntimo data</span><output id="sendDate"></output></div>' +
          '</div>' +
          '<div class="warn" id="missing" hidden></div>' +
          formHtml +
          '<div class="actions">' +
            (cfg.sms
              ? '<button type="button" class="btn btn--cta" id="copySms">Kopijuoti SMS</button>'
              : '<button type="button" class="btn btn--cta" id="copyEmail">Kopijuoti laišką</button>' +
                (cfg.ics ? '<button type="button" class="btn" id="downloadIcs">Atsisiųsti .ics</button>' : "") +
                '<button type="button" class="btn" id="copyHtml">Kopijuoti HTML</button>') +
          '</div>' +
          '<p class="status" id="status" role="status"></p>' +
          (cfg.sms ? "" :
          '<h2>Kaip išsiųsti per Gmail</h2>' +
          '<ol style="padding-left:20px;margin:0;font-size:14px;">' +
            '<li>Nukopijuokite temą ir įklijuokite ją į Gmail laukelį „Tema“.</li>' +
            '<li>Paspauskite <b>Kopijuoti laišką</b> ir įklijuokite laiško lauke (<code>Ctrl/Cmd + V</code>).</li>' +
            '<li>Patikrinkite, ar neliko geltonų [VIETA] žymų.</li>' +
            (cfg.attach ? '<li>' + cfg.attach + '</li>' : "") +
          '</ol>' +
          '<p style="font-size:13px;color:var(--ink-600);margin-top:12px;">„Kopijuoti HTML“ skirtas MailerLite, Brevo ar n8n. Jame yra ir paslėptas peržiūros tekstas (preheader).</p>') +
        '</form>' +
        '<section>' +
          (cfg.sms ? "" :
          '<div class="subject"><span>Tema:</span><output id="subject"></output><button type="button" class="btn" id="copySubject">Kopijuoti</button></div>' +
          '<div class="subject"><span>Peržiūros tekstas:</span><output id="preheader" style="font-weight:400;"></output></div>') +
          '<p class="preview-label">' + (cfg.sms ? "SMS peržiūra" : "Laiško peržiūra") + '</p>' +
          '<div class="preview-wrap"><div id="preview"></div></div>' +
        '</section>' +
      '</div>';

    var form = document.getElementById("form");
    var preview = document.getElementById("preview");
    var statusEl = document.getElementById("status");
    var current = {};

    function say(msg) { statusEl.textContent = msg; }

    function render() {
      var x = values();
      var missing = [];
      var k = makeKit(x, missing);
      document.getElementById("sendDate").textContent = sendDate(meta, x);
      if (cfg.sms) {
        var text = translit(cfg.sms(x, k));
        var len = text.length, parts = len <= 160 ? 1 : Math.ceil(len / 153);
        current = { sms: text };
        preview.innerHTML = '<div class="sms"><div class="sms-bubble">' + esc(text) + '</div>' +
          '<p class="sms-count">' + len + ' simb. · ' + parts + ' SMS' + (parts > 1 ? " (patrumpinkite iki 160 simbolių)" : "") + ' · be lietuviškų raidžių</p></div>';
      } else {
        var subject = cfg.subject(x, k), pre = cfg.preheader(x, k);
        var body = cfg.body(x, k);
        current = { x: x, subject: subject, pre: pre, html: shell(cfg, x, k, body, ""), htmlFull: shell(cfg, x, k, body, pre) };
        preview.innerHTML = current.html;
        document.getElementById("subject").textContent = subject;
        document.getElementById("preheader").textContent = pre;
      }
      var box = document.getElementById("missing");
      box.hidden = !missing.length;
      box.innerHTML = missing.length ? "<b>Trūksta duomenų:</b><ul>" + missing.map(function (m) { return "<li>" + esc(m) + "</li>"; }).join("") + "</ul>" : "";
    }

    form.addEventListener("input", function (e) {
      var el = e.target;
      if (!el.name) return;
      var st = loadStore(); st[el.name] = el.value; saveStore(st);
      render();
    });

    function copyRich() {
      var html = current.html;
      function fallback() {
        var range = document.createRange();
        range.selectNodeContents(preview);
        var sel = window.getSelection();
        sel.removeAllRanges(); sel.addRange(range);
        var ok = false;
        try { ok = document.execCommand("copy"); } catch (e) {}
        sel.removeAllRanges();
        say(ok ? "Laiškas nukopijuotas, įklijuokite jį į Gmail." : "Nepavyko nukopijuoti. Pažymėkite peržiūrą ir spauskite Ctrl/Cmd + C.");
      }
      if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write) {
        navigator.clipboard.write([new ClipboardItem({
          "text/html": new Blob([html], { type: "text/html" }),
          "text/plain": new Blob([preview.innerText], { type: "text/plain" })
        })]).then(function () { say("Laiškas nukopijuotas, įklijuokite jį į Gmail."); }, fallback);
      } else fallback();
    }
    function copyText(text, msg) {
      navigator.clipboard.writeText(text).then(function () { say(msg); }, function () { say("Nepavyko nukopijuoti."); });
    }
    function on(id, fn) { var el = document.getElementById(id); if (el) el.addEventListener("click", fn); }

    on("copyEmail", copyRich);
    on("copyHtml", function () { copyText(current.htmlFull, "HTML kodas nukopijuotas."); });
    on("copySubject", function () { copyText(current.subject, "Tema nukopijuota."); });
    on("copySms", function () { copyText(current.sms, "SMS tekstas nukopijuotas."); });
    on("downloadIcs", function () {
      var blob = new Blob([buildIcs(current.x)], { type: "text/calendar;charset=utf-8" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = isoDate(current.x.start) + "-glaubic-mokymai.ics";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      say("Failas atsisiųstas. Įkelkite jį į svetainę ir įrašykite adresą laukelyje „.ics failo adresas“.");
    });

    render();
    window.__glaubic = { values: values, buildIcs: buildIcs, googleUrl: googleUrl, render: render };
  }

  function fieldHtml(key) {
    var f = FIELDS[key], st = loadStore();
    var val = st[key] !== undefined ? st[key] : f.def;
    var input;
    if (f.type === "textarea") input = '<textarea name="' + key + '">' + esc(val) + '</textarea>';
    else if (f.type === "select") input = '<select name="' + key + '">' + f.options.map(function (o) { return '<option value="' + o[0] + '"' + (o[0] === val ? " selected" : "") + '>' + esc(o[1]) + '</option>'; }).join("") + '</select>';
    else input = '<input type="' + (f.type || "text") + '" name="' + key + '" value="' + esc(val) + '"' + (f.type === "number" ? ' step="0.5" min="0.5"' : "") + (f.ph ? ' placeholder="' + esc(f.ph) + '"' : "") + '>';
    return '<label class="field"><span>' + esc(f.label) + '</span>' + input + (f.hint ? '<small>' + esc(f.hint) + '</small>' : "") + '</label>';
  }

  window.GLAUBIC = { page: page, pages: PAGES };
})();
