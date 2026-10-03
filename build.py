#!/usr/bin/env python3
"""Baut alle Seiten der Hettich-Website (v4) aus einem gemeinsamen Rahmen.
Aufruf: python3 build.py   (Vorschau, noindex)
        python3 build.py --live   (für die echte Domain: indexierbar)"""
import pathlib, json, sys, html as H

ROOT = pathlib.Path(__file__).parent
LIVE = '--live' in sys.argv
BASE = 'https://www.hettich-sicherheitsdienst.de/'
LOGO = open(ROOT / 'img/logo.svg').read().replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1)  # Original-Logo, unverändert (#FFD700)

TEL = '0171 7449939'
TEL_HREF = 'tel:+491717449939'
MAIL = 'info@hettich-sicherheitsdienst.de'
ORT = ['Ulm', 'Neu-Ulm', 'Vöhringen', 'Senden', 'Weißenhorn', 'Illertissen', 'Pfaffenhofen a. d. Roth', 'Illerkirchberg',
       'Blaustein', 'Blaubeuren', 'Ehingen', 'Erbach', 'Laupheim', 'Langenau', 'Biberach', 'Günzburg']

I = {
 'arrow': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="M7 17 17 7M8 7h9v9"/></svg>',
 'shield': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg>',
 'eye': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l18 18"/><path d="M10.6 5.1A10 10 0 0 1 12 5c5 0 9 4.5 10 7-.4 1-1.2 2.3-2.4 3.5M6.6 6.6C4.4 8 2.9 10.1 2 12c1 2.5 5 7 10 7 1.8 0 3.4-.6 4.8-1.4"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/></svg>',
 'badge': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="6"/><path d="m9 14.5-1.5 7 4.5-2.5 4.5 2.5-1.5-7"/><path d="m10 9 1.5 1.5L14 8"/></svg>',
 'lock': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15.5" r="1.5"/></svg>',
 'phone': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
 'mail': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2.5"/><path d="m22 7-10 6L2 7"/></svg>',
 'pin': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
 'plus': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" width="16" height="16"><path d="M12 5v14M5 12h14"/></svg>',
}

NAV = [('index.html', 'Start'), ('dienstleistungen.html', 'Dienstleistungen'), ('vision.html', 'Vision'), ('blog.html', 'Sicherheitsblog')]
LEIST = [('ladendetektiv-ulm.html', 'Ladendetektiv'), ('objektschutz-ulm.html', 'Objektschutz &amp; Wachdienst'), ('testkaeufe.html', 'Testkäufe'), ('dienstleistungen.html#individuell', 'Veranstaltungen &amp; mehr')]
SITEMAP = []

ORG = {"@type": "SecurityService", "@id": BASE + "#firma", "name": "Hettich Sicherheitsdienst", "url": BASE,
       "logo": BASE + "img/icon-512.png", "image": BASE + "img/og.jpg", "telephone": "+49 171 7449939", "email": MAIL,
       "slogan": "Weil Sicherheit Vertrauen schafft.", "founder": {"@type": "Person", "name": "Jan Hettich"},
       "sameAs": ["https://www.wlw.de/de/company-overview/0e1f69e2-b47b-4038-abb5-3dd75badafe1"],
       "address": {"@type": "PostalAddress", "streetAddress": "Kapellenstraße 1", "postalCode": "89269", "addressLocality": "Vöhringen", "addressRegion": "Bayern", "addressCountry": "DE"},
       "geo": {"@type": "GeoCoordinates", "latitude": 48.2803, "longitude": 10.0839},
       "areaServed": [{"@type": "City", "name": o} for o in ORT[:8]] + [{"@type": "AdministrativeArea", "name": n} for n in ["Alb-Donau-Kreis", "Landkreis Neu-Ulm", "Landkreis Biberach"]],
       "knowsAbout": ["Ladendetektiv", "Ladendetektei", "Objektschutz", "Wachdienst", "Testkäufe", "Veranstaltungsschutz", "Baustellenbewachung"],
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Sicherheitsdienstleistungen", "itemListElement": [
           {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": BASE + u}} for u, n in
           [("ladendetektiv-ulm.html", "Ladendetektiv / Ladendetektei"), ("objektschutz-ulm.html", "Objektschutz & Wachdienst"), ("testkaeufe.html", "Testkäufe im Einzelhandel"), ("dienstleistungen.html", "Veranstaltungsschutz, Empfangs- und Pfortendienst")]]}}


def esc(t):
    return H.escape(t, quote=True)


def btn(href, text, kind='gold', extra=''):
    return f'<a class="btn btn-{kind} {extra}" href="{href}">{text}<span class="ar">{I["arrow"]}</span></a>'


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'


def head(fn, title, desc, extra_ld=None, crumbs=None):
    url = BASE if fn == 'index.html' else BASE + fn
    graph = [ORG, {"@type": "WebSite", "@id": BASE + "#web", "url": BASE, "name": "Hettich Sicherheitsdienst", "inLanguage": "de-DE", "publisher": {"@id": BASE + "#firma"}}]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + (u if u != 'index.html' else '')} for i, (u, n) in enumerate([('index.html', 'Start')] + crumbs)]})
    if extra_ld:
        graph += extra_ld
    robots = 'index,follow,max-image-preview:large' if LIVE else 'noindex,nofollow'
    return f'''<!doctype html>
<html lang="de" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#09090a">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Hettich Sicherheitsdienst">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="img/icon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="fonts/poppins-300-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
{ld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<div class="loader" aria-hidden="true">{LOGO}<div class="bar"><i></i></div></div>
<div class="progress" aria-hidden="true"></div>
<div class="grid-bg" aria-hidden="true"></div>
<div class="noise" aria-hidden="true"></div>
'''


def header(fn):
    on = ' class="on" aria-current="page"'
    links = ''.join(f'<a href="{h}"{on if h == fn else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="hdr">
 <div class="wrap">
  <a class="brand" href="index.html">{LOGO}<div><b>Hettich</b><span>Sicherheitsdienst</span><small>Weil Sicherheit Vertrauen schafft.</small></div></a>
  <nav class="nav" id="menu" aria-label="Hauptmenü">{links}{btn("kontakt.html", "Kontakt", "line", "btn-sm")}</nav>
  <button class="burger" type="button" aria-label="Menü" aria-controls="menu" aria-expanded="false"><i></i><i></i></button>
 </div>
</header>
'''


def footer():
    return f'''<footer class="ftr">
 <div class="wrap">
  <div class="big" aria-hidden="true"><span>Weil Sicherheit</span> <span>Vertrauen schafft.</span></div>
  <div class="row">
   <div><a class="brand" href="index.html">{LOGO}<div><b>Hettich</b><span>Sicherheitsdienst</span></div></a>
    <p class="muted" style="font-size:14px;margin-top:18px;max-width:300px">Sicherheitsdienst für Ulm, Neu-Ulm und die Region: Ladendetektiv, Objektschutz, Testkäufe und individuelle Sicherheitslösungen.</p></div>
   <div><h2 class="fh">Leistungen</h2><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in LEIST)}</ul></div>
   <div><h2 class="fh">Unternehmen</h2><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV[1:])}<li><a href="kontakt.html">Kontakt</a></li></ul></div>
   <div><h2 class="fh">Kontakt</h2><ul><li><a href="{TEL_HREF}">{TEL}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></li><li>§ 34a GewO · ID 18865</li></ul></div>
  </div>
  <div class="bottom"><span>© 2026 Hettich Sicherheitsdienst</span><span>Zugelassenes Bewachungsunternehmen nach § 34a GewO</span></div>
 </div>
 <a class="fab magnet" href="{TEL_HREF}" aria-label="Jetzt anrufen: {TEL}"><span class="ic">{I["phone"]}</span><span class="lbl">Jetzt anrufen</span></a>
</footer>
<script src="js/gsap.min.js"></script>
<script src="js/ScrollTrigger.min.js"></script>
<script src="js/lenis.min.js"></script>
<script src="js/site.js"></script>
</body>
</html>
'''


def page(fn, title, desc, body, extra_ld=None, crumbs=None, prio='0.7'):
    out = head(fn, title, desc, extra_ld, crumbs) + header(fn) + '<main id="main">\n' + body + '\n</main>\n' + footer()
    (ROOT / fn).write_text(out, encoding='utf-8')
    SITEMAP.append((fn, prio))
    print(f'{fn:34} {len(title):3} Z. Titel  {len(desc):3} Z. Beschreibung')


def redirect(fn, target, title):
    (ROOT / fn).parent.mkdir(parents=True, exist_ok=True)
    depth = '../' * fn.count('/')
    (ROOT / fn).write_text(f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{esc(title)}</title>
<meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE}{target}">
<meta http-equiv="refresh" content="0; url={depth}{target}"><script>location.replace("{depth}{target}")</script>
<style>body{{background:#09090a;color:#eee;font:16px system-ui;display:grid;place-items:center;min-height:100vh}}a{{color:#FFD700}}</style></head>
<body><p>Diese Seite ist umgezogen: <a href="{depth}{target}">{esc(title)}</a></p></body></html>''', encoding='utf-8')


def contact_rows():
    return f'''<div class="contact-rows">
 <a class="crow" href="{TEL_HREF}"><span class="ic">{I["phone"]}</span><span><small>Telefon – auch kurzfristig</small><b>{TEL}</b></span></a>
 <a class="crow" href="mailto:{MAIL}"><span class="ic">{I["mail"]}</span><span><small>E-Mail</small><b>{MAIL}</b></span></a>
 <div class="crow"><span class="ic">{I["pin"]}</span><span><small>Einsatzgebiet</small><b>Ulm, Neu-Ulm &amp; Umgebung</b></span></div>
</div>'''


def cta_block(h='Bereit für mehr <span class="gold">Sicherheit?</span>'):
    return f'''<section class="sec cta" id="kontakt" aria-label="Kontakt">
 <div class="wrap"><div class="frame"><div class="cols">
  <div><canvas class="fx" data-fx="globe" aria-hidden="true"></canvas><h2 class="h-l" data-split>{h}</h2></div>
  <div>
   <p data-up>Ob Ladendetektiv, Objektschutz oder individuelle Sicherheitslösung – wir sind Ihr Partner für maßgeschneiderte Sicherheit in Ulm, Neu-Ulm und Umgebung.</p>
   <p data-up class="muted">Schnell erreichbar, flexibel im Einsatz und immer diskret. Nehmen Sie jetzt Kontakt auf und erhalten Sie Ihr persönliches Sicherheitskonzept.</p>
   <div data-up>{contact_rows()}</div>
   <div data-up style="display:flex;flex-wrap:wrap;gap:14px;align-items:center">{btn("kontakt.html", "Kontakt aufnehmen")}<span class="muted" style="font-size:13px">Unverbindlich anfragen – wir melden uns umgehend.</span></div>
  </div>
 </div></div></div>
</section>'''


def faq_block(qs, title='Häufige <span class="gold">Fragen</span>', eyebrow='FAQ'):
    items = ''.join(f'<details data-up><summary>{q}<i>{I["plus"]}</i></summary><div class="a">{a}</div></details>' for q, a in qs)
    sec = f'''<section class="sec" id="faq" style="padding-top:0"><div class="wrap">
 <span class="eyebrow" data-up>{eyebrow}</span><h2 class="h-l" data-split style="margin:16px 0 40px">{title}</h2>
 <div class="faq">{items}</div></div></section>'''
    import re
    strip = lambda t: re.sub(r'<[^>]+>', '', t).replace('&amp;', '&')
    schema = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qs]}
    return sec, schema


def area_block():
    mc = ' class="main"'
    chips = ''.join(f'<span{mc if o in ("Ulm", "Neu-Ulm") else ""}>{o}</span>' for o in ORT)
    return f'''<section class="sec" id="einsatzgebiet" style="padding-top:0"><div class="wrap"><div class="two">
 <div><span class="eyebrow" data-up>Einsatzgebiet</span><h2 class="h-l" data-split style="margin-top:16px">Ihr Sicherheitsdienst für Ulm, Neu-Ulm <span class="gold">und die Region.</span></h2></div>
 <div><p data-up class="muted">Unser Sitz ist in Vöhringen (Landkreis Neu-Ulm). Von hier aus sind wir schnell in Ulm, Neu-Ulm, im Alb-Donau-Kreis, im Landkreis Neu-Ulm und bis Biberach im Einsatz – für Einzelhandel, Gewerbe und Veranstalter.</p>
 <div class="area" data-up>{chips}<span>und Umgebung</span></div></div>
</div></div></section>'''


SVC = [
 ('Ladendetektiv', 'ladendetektei', 'ladendetektiv-ulm.html', 'Unsere Kernkompetenz. Mit geschultem Blick und unauffälliger Präsenz decken wir Ladendiebstähle frühzeitig auf und senken Inventurdifferenzen im Einzelhandel – in Ulm, Neu-Ulm und Umgebung.'),
 ('Objektschutz &amp; Wachdienst', 'objektschutz', 'objektschutz-ulm.html', 'Festposten, Kontrollgänge und Revierdienst für Firmengebäude, Parkplätze, Baustellen und Lagerflächen – damit geschützt bleibt, was Ihnen wichtig ist.'),
 ('Testkäufe', 'testkauf', 'testkaeufe.html', 'Geschulte Tester treten als Kunden auf und zeigen, wie aufmerksam Ihr Team arbeitet und wo Abläufe nachgeschärft werden sollten – zur Schulung, nicht zur Bestrafung.'),
 ('Individuelle Lösungen', 'individuell', 'dienstleistungen.html#individuell', 'Veranstaltungsschutz, Empfangs- und Pfortendienst, Zutrittskontrollen oder Baustellenbewachung: Wir entwickeln ein Konzept, das genau zu Ihren Anforderungen passt.'),
]

FAQ_START = [
 ('Für welche Orte ist der Hettich Sicherheitsdienst im Einsatz?', 'Unser Schwerpunkt liegt auf Ulm und Neu-Ulm. Wir arbeiten außerdem in der ganzen Region – unter anderem in Vöhringen, Senden, Weißenhorn, Illertissen, Blaustein, Blaubeuren, Ehingen, Laupheim und Biberach.'),
 ('Was kostet ein Sicherheitsdienst oder Ladendetektiv?', 'Der Preis hängt von Einsatzart, Einsatzzeiten und Häufigkeit ab. Ein Einsatz dauert bei uns in der Regel 8 Stunden. Nach einem kurzen Gespräch erhalten Sie ein transparentes, unverbindliches Angebot.'),
 ('Ist der Hettich Sicherheitsdienst zugelassen?', 'Ja. Wir sind ein Bewachungsunternehmen mit Erlaubnis nach § 34a Gewerbeordnung und im Bewacherregister unter der ID 18865 registriert.'),
 ('Wie schnell können Sie einen Einsatz übernehmen?', 'Rufen Sie uns an – als inhabergeführtes Unternehmen entscheiden wir ohne Umwege und planen Einsätze auch kurzfristig, sofern es die Einsatzlage zulässt.'),
 ('Arbeiten Ihre Ladendetektive verdeckt?', 'Ja. Unsere Ladendetektive sind in Zivil im Einsatz und fallen im Laden nicht auf. Auf Wunsch zeigen wir auch bewusst sichtbare Präsenz zur Abschreckung.'),
]


def index():
    vals = [('shield', 'Prävention', 'Gefahren erkennen, bevor sie entstehen: Mit vorausschauenden Maßnahmen schützen wir Menschen, Werte und Objekte effektiv und nachhaltig.'),
            ('eye', 'Diskretion', 'Wir arbeiten unauffällig und verschwiegen. So bleibt Ihre Sicherheit jederzeit gewahrt, ohne Aufmerksamkeit zu erregen.'),
            ('badge', 'Professionalität', 'Unsere Mitarbeiter sind geschult, erfahren und handeln nach klaren Standards – in jedem Einsatzgebiet.'),
            ('lock', 'Vertrauen', 'Verlässlichkeit und Transparenz: Durch klare Kommunikation und konsequentes Handeln schaffen wir die Basis für langfristiges Vertrauen.')]
    cards = ''.join(f'<article class="card" data-up><div class="ic">{I[ic]}</div><h3>{t}</h3><p>{p}</p><span class="ln"></span></article>' for ic, t, p in vals)
    rows = ''.join(f'''<article class="srow" data-scan><div class="sim" aria-hidden="true"><img src="img/{im}-1400.webp" alt="" loading="lazy" width="1344" height="768"><span class="scan"></span><span class="vf"><i></i><i></i><i></i><i></i></span></div><div class="stx" data-up><span class="no">0{i+1}</span><h3>{t}</h3><p>{p}</p><a class="more" href="{u}">Mehr erfahren<span class="sr"> über {t}</span> {I["arrow"]}</a></div></article>''' for i, (t, im, u, p) in enumerate(SVC))
    mq = ''.join(f'<span>{w}<em>✦</em></span>' for w in ['Prävention', 'Diskretion', 'Professionalität', 'Vertrauen', 'Ladendetektiv', 'Objektschutz', 'Testkäufe', 'Ulm &amp; Neu-Ulm'] * 2)
    faq, faq_ld = faq_block(FAQ_START)
    body = f'''<section class="hero">
 <canvas class="fx" data-fx="waves" aria-hidden="true"></canvas>
 <div class="wrap">
  <div class="hero-logo">{LOGO}</div>
  <div>
   <h1 class="eyebrow" data-up>Sicherheitsdienst &amp; Ladendetektiv in Ulm</h1>
   <p class="h-xl" data-split style="margin:18px 0 22px">Weil Sicherheit <span class="gold">Vertrauen</span> schafft.</p>
   <p class="lead" data-up>Hettich Sicherheitsdienst – Ladendetektei, Objektschutz und Testkäufe für Unternehmen in Ulm, Neu-Ulm und Umgebung. Zuverlässig, diskret und modern.</p>
   <div class="ctas" data-up>{btn("kontakt.html", "Kontakt aufnehmen")}{btn("#leistungen", "Unsere Dienstleistungen", "line")}</div>
  </div>
 </div>
 <div class="hero-meta"><div class="wrap"><span>§ 34a GewO · Bewacherregister-ID 18865</span><span class="scrollcue">Scrollen <i></i></span></div></div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{mq}</div></div>

<section class="sec values" id="werte">
 <div class="wrap"><div class="frame"><div class="cols">
  <div>
   <span class="eyebrow" data-up>Unser Anspruch</span>
   <h2 class="h-l" data-split>Maßgeschneiderte Sicherheit – <span class="gold">zuverlässig, diskret und modern.</span></h2>
   <p data-up class="muted">Mit dem Hettich Sicherheitsdienst erhalten Sie individuelle Sicherheitskonzepte, die genau auf Ihre Anforderungen abgestimmt sind. Ob Objektschutz, Ladendetektive oder Veranstaltungsschutz – wir sorgen für Prävention, Schutz und Vertrauen.</p>
   <p data-up class="muted">Unsere erfahrenen Mitarbeiter handeln diskret, zuverlässig und professionell, damit Sie sich ganz auf Ihr Kerngeschäft konzentrieren können.</p>
   <div data-up>{btn("dienstleistungen.html", "Unsere Dienstleistungen", "line")}</div>
  </div>
  <div class="vgrid">{cards}</div>
 </div></div></div>
</section>

<section class="sec state" id="ueber" style="padding-top:0">
 <div class="wrap"><div class="frame"><div class="cols">
  <div><canvas class="fx" data-fx="rings" aria-hidden="true"></canvas><h2 class="h-m" data-split>Sicherheitsdienst neu gedacht.<br><span class="gold">Zuverlässig. Diskret. Professionell.</span></h2></div>
  <div>
   <p class="reveal-words">Der Hettich Sicherheitsdienst ist ein inhabergeführtes Unternehmen mit klarem Schwerpunkt auf Ladendetektei in Ulm, um Ulm und um Ulm herum. Unsere erfahrenen Ladendetektive arbeiten diskret und professionell und haben bereits zahlreiche Diebstähle im Einzelhandel aufgeklärt.</p>
   <p class="reveal-words">Neben unserer Kernkompetenz im Handel bieten wir Objektschutz in Ulm und der Region sowie Veranstaltungsschutz – individuell geplant und flexibel, für Unternehmen ebenso wie für Privatkunden.</p>
   <div data-up style="margin-top:34px">{btn("vision.html", "Unsere Vision", "line")}</div>
  </div>
 </div></div></div>
</section>

<section class="sec" id="leistungen" style="padding-top:0">
 <div class="wrap">
  <div class="svc-head"><div><span class="eyebrow" data-up>Dienstleistungen</span><h2 class="h-l" data-split style="margin-top:16px">Was wir für Sie <span class="gold">schützen.</span></h2></div><div data-up>{btn("dienstleistungen.html", "Alle Leistungen im Detail", "line")}</div></div>
  <div class="svc2">{rows}</div>
  </div>
 </div>
</section>

<section class="sec nums" style="padding-top:0" aria-label="In Zahlen">
 <div class="wrap"><div class="frame">
  <canvas class="fx" data-fx="columns" aria-hidden="true"></canvas>
  <div class="nums-top" data-up>{LOGO}<span class="t">Hettich Sicherheitsdienst <span class="gold">in Zahlen</span></span></div>
  <div class="ngrid">
   <div class="n" data-up><small>Über</small><span class="v" data-count="5">5</span><p>Jahre Erfahrung im Sicherheitsgewerbe</p><i></i></div>
   <div class="n" data-up><small>Über</small><span class="v" data-count="900">900</span><p>erfolgreich abgeschlossene Einsätze</p><i></i></div>
   <div class="n" data-up><small>&nbsp;</small><span class="v">24/7</span><p>einsatzbereit für unsere Kunden in Ulm und Umgebung</p><i></i></div>
   <div class="n" data-up><small>§</small><span class="v">34a</span><p>zugelassen nach GewO – Bewacherregister-ID 18865</p><i></i></div>
  </div>
 </div></div>
</section>

<section class="sec" id="warum" style="padding-top:0">
 <div class="wrap">
  <span class="eyebrow" data-up>Der Unterschied</span>
  <h2 class="h-l" data-split style="margin:16px 0 50px;max-width:900px">Was uns von großen Anbietern <span class="gold">unterscheidet.</span></h2>
  <div class="why">
   <div data-up><span class="k">01</span><h3>Persönlich durch den Inhaber</h3><p>Sie sprechen direkt mit dem Chef – vom ersten Gespräch bis zum laufenden Einsatz.</p></div>
   <div data-up><span class="k">02</span><h3>Kurze Entscheidungswege</h3><p>Keine Zentrale, keine Warteschleife. Absprachen gelten sofort und werden umgesetzt.</p></div>
   <div data-up><span class="k">03</span><h3>Schnelle Reaktion</h3><p>Wir reagieren zügig auf Ihre Wünsche und passen Einsätze flexibel an Ihre Lage an.</p></div>
  </div>
 </div>
</section>
{area_block()}
{faq}
{cta_block()}'''
    page('index.html', 'Sicherheitsdienst Ulm & Neu-Ulm | Ladendetektiv | Hettich',
         'Hettich Sicherheitsdienst: Ladendetektiv, Objektschutz, Wachdienst und Testkäufe in Ulm, Neu-Ulm und Umgebung. Zugelassen nach § 34a GewO. Jetzt anfragen!',
         body, [faq_ld], prio='1.0')


def phero(eyebrow, h1, lead, fx='waves', crumb=None):
    c = f'<nav class="crumbs" aria-label="Brotkrumen" data-up><a href="index.html">Start</a> / {crumb}</nav>' if crumb else ''
    return f'''<section class="phero"><canvas class="fx" data-fx="{fx}" aria-hidden="true"></canvas><div class="wrap">{c}<span class="eyebrow" data-up>{eyebrow}</span><h1 class="h-l" data-split>{h1}</h1><p class="lead" data-up>{lead}</p><div class="ctas" data-up style="display:flex;flex-wrap:wrap;gap:14px;margin-top:30px">{btn(TEL_HREF, "Anrufen: " + TEL)}{btn("kontakt.html", "Anfrage senden", "line")}</div></div></section>'''


def landing(fn, crumb, eyebrow, h1, lead, fx, intro_h, intro_ps, checks_h, checks, steps, faqs, title, desc, img, service_name):
    ck = ''.join(f'<li data-up><span><b>{a}</b> – {b}</span></li>' for a, b in checks)
    st = ''.join(f'<div data-up><span class="k">0{i+1}</span><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(steps))
    faq, faq_ld = faq_block(faqs, f'Fragen zum Thema <span class="gold">{crumb}</span>')
    body = phero(eyebrow, h1, lead, fx, crumb) + f'''
<section class="sec" style="padding-top:40px"><div class="wrap"><div class="two">
 <div><h2 class="h-l" data-split>{intro_h}</h2>{"".join(f'<p data-up class="muted" style="margin-top:18px">{p}</p>' for p in intro_ps)}</div>
 <div class="detail" style="margin:0;grid-template-columns:1fr" data-up><div class="im" style="min-height:380px"><img data-par src="img/{img}-1400.webp" alt="{service_name} – Hettich Sicherheitsdienst Ulm" loading="lazy" width="1344" height="768"></div></div>
</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="frame" style="padding:clamp(28px,5vw,72px)">
 <span class="eyebrow" data-up>Leistungsumfang</span><h2 class="h-l" data-split style="margin:16px 0 30px">{checks_h}</h2>
 <ul class="checks">{ck}</ul>
</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
 <span class="eyebrow" data-up>Ablauf</span><h2 class="h-l" data-split style="margin:16px 0 46px">So starten wir <span class="gold">gemeinsam.</span></h2>
 <div class="steps">{st}</div>
</div></section>
{faq}
{cta_block()}'''
    svc_ld = {"@type": "Service", "name": service_name, "serviceType": service_name, "provider": {"@id": BASE + "#firma"},
              "areaServed": ORG["areaServed"], "url": BASE + fn, "description": desc}
    page(fn, title, desc, body, [faq_ld, svc_ld], [(fn, crumb)], prio='0.9')


STEPS = [('Anfrage', 'Sie rufen an oder schreiben uns – wir melden uns umgehend.'),
         ('Gespräch &amp; Analyse', 'Wir besprechen Ziele, Zeiten und Schwachstellen – auf Wunsch direkt vor Ort.'),
         ('Angebot &amp; Planung', 'Sie erhalten ein klares Angebot und einen abgestimmten Einsatzplan.'),
         ('Einsatz &amp; Bericht', 'Wir sind diskret im Einsatz und dokumentieren nachvollziehbar.')]


def ladendetektiv():
    landing('ladendetektiv-ulm.html', 'Ladendetektiv', 'Ladendetektei Ulm &amp; Neu-Ulm',
            'Ladendetektiv für Ulm, Neu-Ulm <span class="gold">&amp; Umgebung.</span>',
            'Diskrete Ladendetektive für Supermärkte, Drogerien und Fachhandel: Wir decken Ladendiebstähle auf, schrecken Täter ab und senken Ihre Inventurdifferenzen.', 'waves',
            'Ladendiebstahl kostet den Handel <span class="gold">Milliarden.</span>',
            ['Laut der EHI-Studie „Inventurdifferenzen 2025“ verliert der deutsche Einzelhandel jedes Jahr rund 3,05 Milliarden Euro durch Ladendiebstahl. Mehr als 98 Prozent der Fälle bleiben unentdeckt.',
             'Genau hier setzen unsere Ladendetektive an: Sie sind in Zivil unterwegs, kennen die typischen Muster und greifen rechtssicher ein. Die Ladendetektei ist die Kernkompetenz des Hettich Sicherheitsdienstes – in Ulm, Neu-Ulm und der ganzen Region.',
             'Quelle: <a href="https://www.ehi.org/themen/inventurdifferenzen-sicherheit/" rel="noopener" target="_blank" style="color:var(--gold)">EHI Retail Institute, Inventurdifferenzen 2025</a>'],
            'Was unsere Ladendetektive für Sie tun',
            [('Verdeckte Beobachtung', 'im Verkaufsraum, an Kassen, Ein- und Ausgängen sowie auf Wunsch im Lager'),
             ('Prävention', 'auf Wunsch bewusst sichtbare Präsenz, die Täter abschreckt'),
             ('Rechtssicheres Anhalten', 'nach dem Passieren der Kasse, gestützt auf das Festnahmerecht nach § 127 Abs. 1 StPO'),
             ('Saubere Dokumentation', 'Einsatzbericht mit Warenwert und Hergang – nachvollziehbar und gerichtsverwertbar'),
             ('Zusammenarbeit mit der Polizei', 'Übergabe der Täter und auf Wunsch Erteilung von Hausverboten'),
             ('Auswertung', 'Hinweise auf Diebstahlmuster, gefährdete Warengruppen und Schwachstellen in Ihrem Markt')],
            STEPS,
            [('Was kostet ein Ladendetektiv?', 'Der Preis richtet sich nach Einsatzzeiten, Häufigkeit und Größe der Verkaufsfläche. Ein Einsatz dauert bei uns in der Regel 8 Stunden. Nach einem kurzen Gespräch erhalten Sie ein transparentes, unverbindliches Angebot.'),
             ('Darf ein Ladendetektiv einen Dieb festhalten?', 'Ja. Wer auf frischer Tat betroffen wird, darf nach § 127 Abs. 1 StPO vorläufig festgehalten werden, bis die Polizei eintrifft. Unsere Ladendetektive handeln dabei verhältnismäßig und dokumentieren jeden Vorfall.'),
             ('Erkennt man Ihre Ladendetektive im Laden?', 'Nein. Unsere Detektive sind in Zivil im Einsatz und verhalten sich wie normale Kunden. Auf Wunsch setzen wir zusätzlich auf sichtbare Präsenz.'),
             ('Für welche Geschäfte lohnt sich ein Ladendetektiv?', 'Für Supermärkte und Lebensmittelhandel, Drogerien, Discounter, Getränkemärkte und den Fachhandel – überall dort, wo Inventurdifferenzen spürbar sind.'),
             ('Brauchen Ladendetektive eine Zulassung?', 'Ja. Ladendetektive unterliegen § 34a GewO. Der Hettich Sicherheitsdienst ist ein zugelassenes Bewachungsunternehmen (Bewacherregister-ID 18865).')],
            'Ladendetektiv Ulm & Neu-Ulm | Hettich Sicherheitsdienst',
            'Ladendetektiv in Ulm & Neu-Ulm: diskrete Ladendetektei für Supermarkt, Drogerie und Fachhandel. Weniger Inventurdifferenzen, rechtssicher. Jetzt anfragen!',
            'ladendetektei', 'Ladendetektiv')


def objektschutz():
    landing('objektschutz-ulm.html', 'Objektschutz', 'Objektschutz &amp; Wachdienst Ulm',
            'Objektschutz &amp; Wachdienst <span class="gold">in Ulm und Neu-Ulm.</span>',
            'Wir schützen Firmengebäude, Lager, Parkplätze und Baustellen – mit Festposten, Kontrollgängen und Revierdienst, bei Tag, in der Nacht und am Wochenende.', 'rings',
            'Sicherheit für Gebäude, Gelände <span class="gold">und Werte.</span>',
            ['Einbruch, Vandalismus und Diebstahl verursachen nicht nur direkte Schäden, sondern auch Ausfallzeiten. Sichtbare Präsenz und regelmäßige Kontrollen schrecken ab, bevor etwas passiert.',
             'Der Hettich Sicherheitsdienst plant den Objektschutz passend zu Ihrem Gelände: stationär am Eingang, als mobile Kontrollgänge oder als Revierdienst über mehrere Objekte hinweg – auf Wunsch abgestimmt mit Ihrer vorhandenen Alarm- und Videotechnik.'],
            'Unsere Leistungen im Objektschutz',
            [('Stationärer Objektschutz', 'Festposten am Eingang oder im Objekt'),
             ('Kontrollgänge &amp; Revierdienst', 'regelmäßige Rundgänge mit Kontrollbericht und Zeitstempel'),
             ('Nacht und Wochenende', 'Bewachung außerhalb Ihrer Betriebszeiten'),
             ('Baustellenbewachung', 'Schutz vor Diebstahl, Vandalismus und unbefugtem Betreten'),
             ('Empfangs- und Pfortendienst', 'Besucherempfang, Ausweis- und Zutrittskontrolle, Schlüsselverwaltung'),
             ('Alarmverfolgung &amp; Meldungen', 'Reaktion auf Alarme sowie Meldung technischer Mängel und Brandschutzrisiken')],
            STEPS,
            [('Was kostet Objektschutz?', 'Das hängt von Objektgröße, Einsatzzeiten und der Art der Bewachung ab – Festposten, Kontrollgänge oder Revierdienst. Wir erstellen Ihnen nach einem kurzen Gespräch ein unverbindliches Angebot.'),
             ('Was ist der Unterschied zwischen Objektschutz und Revierdienst?', 'Beim Objektschutz ist eine Sicherheitskraft fest an Ihrem Objekt. Beim Revierdienst kontrollieren wir mehrere Objekte nacheinander in festgelegten oder wechselnden Zeitfenstern – meist nachts und am Wochenende.'),
             ('Bewachen Sie auch Baustellen?', 'Ja. Wir sichern Baustellen gegen Diebstahl von Material und Werkzeug, gegen Vandalismus und unbefugtes Betreten – abgestimmt mit der Bauleitung.'),
             ('Können Sie mit unserer Alarm- und Videotechnik zusammenarbeiten?', 'Ja. Wir stimmen unsere Kontrollen und die Alarmverfolgung auf Ihre vorhandene Technik ab und beraten Sie bei Bedarf zu sinnvollen Ergänzungen.')],
            'Objektschutz & Wachdienst Ulm | Hettich Sicherheitsdienst',
            'Objektschutz und Wachdienst in Ulm & Neu-Ulm: Festposten, Kontrollgänge, Revierdienst und Baustellenbewachung – zuverlässig, auch nachts. Jetzt anfragen!',
            'objektschutz', 'Objektschutz und Wachdienst')


def testkaeufe():
    landing('testkaeufe.html', 'Testkäufe', 'Testkäufe im Einzelhandel',
            'Testkäufe für den Einzelhandel <span class="gold">in Ulm und Umgebung.</span>',
            'Geschulte Testkäufer prüfen Ihren Markt wie echte Kunden: Kassenabläufe, Warensicherung, Aufmerksamkeit und Service – mit klarem, schriftlichem Ergebnis.', 'columns',
            'Sehen, wie Ihr Markt <span class="gold">wirklich arbeitet.</span>',
            ['Viele Schwachstellen fallen erst im echten Alltag auf: ungesicherte Ware, unaufmerksame Kassenvorgänge oder fehlende Kontrollen. Ein Testkauf macht sichtbar, was im Tagesgeschäft untergeht.',
             'Die Ergebnisse dienen nicht der Bestrafung, sondern der Schulung und Qualitätssicherung. In Kombination mit Ladendetektiven und Objektschutz entsteht ein umfassendes Schutzkonzept für Ihr Geschäft.'],
            'Was ein Testkauf bei uns umfasst',
            [('Realistische Prüfung', 'unsere Tester treten als ganz normale Kunden auf'),
             ('Kassen- und Abläufe', 'Kontrolle von Kassiervorgängen und internen Abläufen'),
             ('Warensicherung', 'sind gefährdete Artikel richtig gesichert und im Blick?'),
             ('Aufmerksamkeit &amp; Service', 'wie aufmerksam und kundenorientiert arbeitet Ihr Team?'),
             ('Schriftlicher Bericht', 'nachvollziehbares Ergebnis mit konkreten Verbesserungsvorschlägen'),
             ('Schulungsgrundlage', 'Erkenntnisse, die Sie direkt in die Mitarbeiterschulung übernehmen können')],
            STEPS,
            [('Was ist ein Testkauf?', 'Bei einem Testkauf tritt eine geschulte Person als Kunde auf und prüft unauffällig Abläufe, Warensicherung und Service im Geschäft. Sie erhalten danach einen schriftlichen Bericht.'),
             ('Wozu dienen Testkäufe?', 'Testkäufe zeigen, wie Abläufe im Alltag tatsächlich funktionieren. Sie decken Schwachstellen auf, bevor Schäden entstehen, und liefern Inhalte für gezielte Mitarbeiterschulungen.'),
             ('Erfahren die Mitarbeiter vorher davon?', 'Nein, der Testkauf selbst ist unangekündigt – nur so ist das Ergebnis aussagekräftig. Wie Sie Ihr Team vorab grundsätzlich über Qualitätskontrollen informieren, besprechen wir gern mit Ihnen.'),
             ('Lassen sich Testkäufe mit einem Ladendetektiv kombinieren?', 'Ja. Testkäufe zeigen Schwachstellen, der Ladendetektiv schützt im laufenden Betrieb – beides ergänzt sich ideal.')],
            'Testkäufe im Einzelhandel | Hettich Sicherheitsdienst Ulm',
            'Testkäufe für den Einzelhandel in Ulm & Neu-Ulm: Kassenabläufe, Warensicherung und Service realistisch prüfen – mit schriftlichem Bericht. Jetzt anfragen!',
            'testkauf', 'Testkäufe im Einzelhandel')


def dienstleistungen():
    D = [
     ('Ladendetektiv', 'Diskret und effektiv', 'ladendetektei', ['Kernkompetenz', 'Einzelhandel', 'Inventurdifferenzen senken'], 'ladendetektiv-ulm.html', '',
      'Unsere Kernkompetenz liegt in der Ladendetektei. Mit geschultem Blick und unauffälliger Präsenz decken wir Diebstähle frühzeitig auf und verhindern hohe Verluste im Einzelhandel. In Ulm, um Ulm und um Ulm herum haben wir bereits zahlreiche Fälle gelöst.',
      'Unsere Detektive arbeiten diskret, professionell und kundenorientiert – für mehr Sicherheit im Handel.'),
     ('Objektschutz &amp; Wachdienst', 'Schutz für Gebäude und Werte', 'objektschutz', ['Kontrollgänge', 'Revierdienst', 'Baustellen', 'Lagerflächen'], 'objektschutz-ulm.html', '',
      'Parkplätze, Firmengebäude und Lagerflächen sind besonders durch Vandalismus und Diebstahl gefährdet. Unser Objektschutz in Ulm sorgt mit Kontrollgängen und Präsenz für die Sicherheit von Fahrzeugen, Besuchern und Mitarbeitern.',
      'Zusätzlich sichern wir Baustellen und Gewerbeflächen zuverlässig ab – mit geschultem Personal und abgestimmt auf Ihre vorhandene Technik.'),
     ('Testkäufe', 'Kontrolle und Mitarbeiterschulung im Alltag', 'testkauf', ['Mystery Shopping', 'Qualitätssicherung', 'Schulung'], 'testkaeufe.html', '',
      'Testkäufe sind ein wirkungsvolles Instrument, um Abläufe und Mitarbeiter im Einzelhandel realistisch zu prüfen. Geschulte Tester treten als Kunden auf und machen sichtbar, wie aufmerksam Ihr Team arbeitet, ob Waren richtig gesichert sind und wo Verbesserungsbedarf besteht.',
      'Die Ergebnisse dienen nicht der Bestrafung, sondern der Mitarbeiterschulung und Qualitätssicherung.'),
     ('Individuelle Sicherheitslösungen', 'Flexibel und bedarfsgerecht', 'individuell', ['Veranstaltungsschutz', 'Empfangsdienst', 'Zutrittskontrolle', 'Baustellen'], 'kontakt.html', 'individuell',
      'Neben unseren Kernbereichen bieten wir auf Anfrage maßgeschneiderte Sicherheitsdienstleistungen an: Veranstaltungsschutz und Einlasskontrollen, Empfangs- und Pfortendienst, Zutrittskontrollen oder Baustellenbewachung.',
      'Wir entwickeln ein Konzept, das genau auf Ihre Anforderungen zugeschnitten ist – flexibel, zuverlässig und diskret.'),
     ('Nahtlose Integration', 'In Ihr Unternehmen', 'empfang', ['Enge Abstimmung', 'Klare Kommunikation', 'Minimale Störung'], 'kontakt.html', '',
      'Ob im Einzelhandel, bei Veranstaltungen oder im Objektschutz – wir passen uns Ihren Strukturen an und arbeiten unauffällig im Hintergrund. Unser Ziel: maximale Sicherheit bei minimaler Störung Ihres Betriebsablaufs.',
      'Durch enge Abstimmung und klare Kommunikation fügen wir uns reibungslos in Ihr bestehendes Team ein.'),
    ]
    blocks = ''.join(f'''<article class="detail" data-up{f' id="{aid}"' if aid else ''}><div class="im"><img data-par src="img/{im}-1400.webp" alt="{t} – Hettich Sicherheitsdienst Ulm" loading="lazy" width="1344" height="768"></div>
<div class="tx"><span class="no">0{i+1} — {sub}</span><h2>{t}</h2><p>{p1}</p><p class="muted">{p2}</p><div class="tags">{"".join(f"<span>{x}</span>" for x in tags)}</div><div>{btn(u, "Mehr erfahren" if u != "kontakt.html" else "Jetzt anfragen", "line", "btn-sm")}</div></div></article>''' for i, (t, sub, im, tags, u, aid, p1, p2) in enumerate(D))
    body = phero('Unsere Dienstleistungen', 'Ladendetektiv, Objektschutz &amp; <span class="gold">Sicherheit</span> in Ulm und Umgebung.',
                 'Der Hettich Sicherheitsdienst ist Ihr Partner für diskrete, professionelle Sicherheit – vom Supermarkt bis zum Firmengelände.', crumb='Dienstleistungen') + \
        f'<section class="sec" style="padding-top:40px"><div class="wrap">{blocks}</div></section>' + area_block() + cta_block()
    page('dienstleistungen.html', 'Dienstleistungen: Ladendetektiv & Objektschutz Ulm | Hettich',
         'Ladendetektiv, Objektschutz, Wachdienst, Testkäufe und Veranstaltungsschutz in Ulm, Neu-Ulm und Umgebung – diskret, flexibel und professionell.',
         body, crumbs=[('dienstleistungen.html', 'Dienstleistungen')], prio='0.9')


def vision():
    body = phero('Unsere Vision', 'Sicherheit neu denken – <span class="gold">diskret, präventiv und modern.</span>',
                 'Wir wollen in Ulm und der Region der erste Ansprechpartner für professionelle Ladendetektei, Objektschutz und maßgeschneiderte Sicherheitslösungen sein.', 'rings', 'Vision') + f'''
<section class="sec" style="padding-top:40px"><div class="wrap">
 <div class="frame"><div class="cols">
  <div class="prose">
   <h2 data-up style="margin-top:0">Was uns auszeichnet</h2>
   <p data-up>Der Hettich Sicherheitsdienst steht für maßgeschneiderte Sicherheitslösungen, die sich konsequent an den Bedürfnissen unserer Kunden orientieren. Ob Ladendetektei in Ulm, um Ulm und um Ulm herum, Objektschutz für Gebäude und Werte oder diskrete Sicherheitsmaßnahmen im Hintergrund – wir stehen für Verlässlichkeit, Diskretion und Professionalität.</p>
   <p data-up>Unser Unternehmen zeichnet sich durch persönliche Betreuung, kurze Entscheidungswege und schnelle Reaktionszeiten aus. Während große Anbieter oft unpersönlich arbeiten, profitieren unsere Kunden von direkter Kommunikation und flexiblen Lösungen. Jeder Auftrag wird individuell geplant, um Risiken frühzeitig zu erkennen und Schäden zu verhindern.</p>
   <p data-up>So schaffen wir ein Umfeld, in dem Menschen, Unternehmen und Werte langfristig geschützt sind und Vertrauen gestärkt wird.</p>
  </div>
  <div class="prose">
   <h2 data-up style="margin-top:0">Unsere Philosophie</h2>
   <p class="reveal-words" style="font-size:clamp(22px,2.2vw,30px);line-height:1.35;color:#fff;font-weight:300">Sicherheit muss wirken, ohne aufzufallen.</p>
   <p data-up>Deshalb arbeiten wir diskret im Hintergrund, stärken Strukturen und minimieren Risiken, bevor Schaden entsteht. Seit der Gründung hat sich der Hettich Sicherheitsdienst in Ulm und Umgebung als verlässlicher Partner etabliert.</p>
   <p data-up>Besonders wichtig ist uns die enge Zusammenarbeit mit unseren Auftraggebern. Durch klare Kommunikation, schnelle Entscheidungswege und individuelle Sicherheitskonzepte reagieren wir flexibel auf jede Situation – ob im Handel oder direkt vor Ort.</p>
   <p data-up>So verbinden wir moderne Sicherheitstechnik mit menschlicher Erfahrung.</p>
  </div>
 </div></div>
</div></section>''' + cta_block()
    page('vision.html', 'Vision | Hettich Sicherheitsdienst Ulm',
         'Unsere Vision: Sicherheit neu denken – diskret, präventiv und modern. Persönliche Betreuung, kurze Wege und schnelle Reaktion in Ulm und Umgebung.',
         body, crumbs=[('vision.html', 'Vision')], prio='0.5')


def kontakt():
    fields = [('Name', 'text', 'required', 'name'), ('Telefon', 'tel', '', 'tel'), ('Unternehmen', 'text', '', 'organization')]
    fl = ''.join(f'<div class="field{" full" if n == "Unternehmen" else ""}"><input id="f{i}" name="{n}" type="{t}" placeholder=" " {r} autocomplete="{ac}"><label for="f{i}">{n}{" *" if r else ""}</label></div>' for i, (n, t, r, ac) in enumerate(fields))
    body = phero('Kontakt', 'Bereit für mehr <span class="gold">Sicherheit?</span>',
                 'Ob Ladendetektiv, Objektschutz oder individuelle Sicherheitslösung – nehmen Sie unverbindlich Kontakt auf und lassen Sie sich persönlich beraten.', 'globe', 'Kontakt') + f'''
<section class="sec" style="padding-top:40px"><div class="wrap"><div class="frame"><div class="cols">
 <div><span class="eyebrow" data-up>Direkt erreichen</span><h2 class="h-m" data-up style="margin:16px 0 26px">Am schnellsten geht es <span class="gold">telefonisch.</span></h2><div data-up>{contact_rows()}</div></div>
 <div><form class="form" data-mail data-up aria-label="Anfrageformular">
  {fl}
  <div class="field full"><textarea id="fm" name="Nachricht" placeholder=" " required></textarea><label for="fm">Ihre Nachricht *</label></div>
  <p class="form-err" role="alert">Bitte geben Sie Ihren Namen und Ihre Nachricht ein.</p>
  <div class="full" style="display:flex;flex-wrap:wrap;gap:16px;align-items:center"><button class="btn btn-gold" type="submit">Anfrage senden<span class="ar">{I["arrow"]}</span></button>
  <span class="note">Öffnet Ihr E-Mail-Programm mit der fertigen Anfrage. <a href="datenschutz.html" style="color:var(--gold)">Datenschutz</a></span></div>
  <div class="form-fallback" role="status"><p>Kein E-Mail-Programm geöffnet? Anfrage kopieren und an <a href="mailto:{MAIL}" style="color:var(--gold)">{MAIL}</a> senden – oder einfach anrufen: <a href="{TEL_HREF}" style="color:var(--gold)">{TEL}</a>.</p>
   <textarea readonly aria-label="Ihre Anfrage zum Kopieren"></textarea>
   <button class="btn btn-line btn-sm copy" type="button" style="margin-top:12px">Anfrage kopieren <span class="ar">{I["arrow"]}</span></button></div>
 </form></div>
</div></div></div></section>'''
    page('kontakt.html', 'Kontakt | Hettich Sicherheitsdienst Ulm',
         'Kontakt zum Hettich Sicherheitsdienst in Ulm & Neu-Ulm: Telefon 0171 7449939, E-Mail info@hettich-sicherheitsdienst.de. Unverbindlich anfragen.',
         body, crumbs=[('kontakt.html', 'Kontakt')], prio='0.8')


POSTS = [
 ('blog-objektschutz.html', 'post/objektschutz-erklärt-mehr-als-nur-wachschutz.html', 'Objektschutz erklärt – mehr als nur Wachschutz', '2025-09-10', '2 Min. Lesezeit', 'gebaeude',
  'Moderner Objektschutz verbindet Erfahrung mit Technik und schützt Gebäude, Werte und Menschen rund um die Uhr. So funktioniert er in Ulm und Umgebung.',
  '''<p>Wenn es um Sicherheit geht, denken viele sofort an einen Wachmann vor der Tür. Doch moderner Objektschutz ist viel mehr als das: Er verbindet Erfahrung mit Technik, schafft Vertrauen und sorgt dafür, dass Gebäude, Werte und Menschen rund um die Uhr geschützt bleiben. Für Unternehmen in Ulm und Umgebung ist Objektschutz längst kein „Extra“ mehr, sondern ein zentraler Bestandteil verantwortungsvoller Unternehmensführung.</p>
<h2>Klassischer Wachdienst – sichtbare Präsenz vor Ort</h2>
<p>Der traditionelle Wachdienst basiert auf menschlicher Präsenz. Sicherheitskräfte sind direkt am Objekt, führen regelmäßige Kontrollgänge durch, überwachen Eingänge und reagieren im Ernstfall sofort. Das schafft nicht nur Sicherheit, sondern auch ein sichtbares Signal: „Dieses Objekt wird geschützt.“ Besonders sinnvoll ist klassischer Wachdienst auf weitläufigen Geländen, in Industriegebieten oder bei Gebäuden mit hohem Publikumsverkehr.</p>
<h2>Moderner Objektschutz – Technik als Verstärker</h2>
<p>Heute geht Objektschutz deutlich weiter: Moderne Systeme kombinieren Kameras mit KI-gestützter Auswertung, Sensoren für Bewegung oder Glasbruch, digitale Zutrittskontrollen und Alarmsysteme mit direkter Verbindung zur Leitstelle. Das hat zwei Vorteile:</p>
<ul><li><strong>Lückenlose Überwachung</strong> – auch dort, wo Menschen nicht ständig präsent sein können.</li><li><strong>Kosteneffizienz</strong> – Technik ergänzt Personal, sodass Ressourcen gezielt eingesetzt werden können.</li></ul>
<h2>Die Kombination macht den Unterschied</h2>
<p>Der größte Effekt entsteht, wenn Mensch und Technik zusammenarbeiten. Sicherheitspersonal reagiert flexibel und individuell, während Technik rund um die Uhr dokumentiert und meldet. In Ulm sind vor allem Mischformen gefragt – etwa die Kombination aus Kontrollgängen, Kameraüberwachung und Alarmaufschaltung für Firmen, Baustellen oder Lagerhallen.</p>
<h2>Separatwachdienst – Sicherheit durch Vertrautheit</h2>
<p>Ein Sonderfall des Objektschutzes ist der Separatwachdienst: Hier sind feste Teams langfristig für ein bestimmtes Objekt zuständig. Dadurch kennen sie die Abläufe, mögliche Schwachstellen und das Gelände im Detail. Diese Vertrautheit erhöht die Sicherheit spürbar.</p>
<h2>Mehr als nur Schutz – ein Beitrag zum Unternehmenserfolg</h2>
<p>Objektschutz hat auch eine psychologische Dimension: Mitarbeitende fühlen sich sicherer, Kunden und Geschäftspartner nehmen ein geschütztes Umfeld als professionell und vertrauenswürdig wahr. Das kann sogar Schäden verhindern, die durch Produktionsausfälle oder Vandalismus entstehen würden.</p>
<h2>Fazit für Ulm &amp; Region</h2>
<p>Objektschutz ist weit mehr als nur Wachschutz. Wer auf eine Kombination aus moderner Technik, geschultem Sicherheitspersonal und maßgeschneiderten Konzepten setzt, erhält ein Sicherheitsnetz, das effizient, flexibel und nachhaltig ist. Mehr dazu: <a href="objektschutz-ulm.html">Objektschutz &amp; Wachdienst in Ulm</a>.</p>'''),
 ('blog-testkaeufe.html', 'post/testkäufe-im-handel-warum-sie-so-wichtig-sind.html', 'Testkäufe im Handel – warum sie so wichtig sind', '2025-09-10', '2 Min. Lesezeit', 'testkauf',
  'Mystery Shopping deckt Schwachstellen auf, stärkt die Mitarbeiterschulung und sichert die Servicequalität im Einzelhandel. Das sollten Händler wissen.',
  '''<p>Im Einzelhandel zählt nicht nur das Sortiment, sondern auch, wie zuverlässig Mitarbeiter und Abläufe funktionieren. Genau hier setzen Testkäufe – auch bekannt als Mystery Shopping – an. Sie sind ein wertvolles Instrument, um Prozesse realistisch zu überprüfen, Schwachstellen aufzudecken und Mitarbeiter gezielt zu schulen.</p>
<h2>Was sind Testkäufe?</h2>
<p>Bei einem Testkauf tritt eine geschulte Person als Kunde auf und prüft die Abläufe im Geschäft. Dabei wird unauffällig beobachtet, wie aufmerksam das Personal ist, ob Waren richtig gesichert sind und wie sich Mitarbeiter im Kundenkontakt verhalten. Das Ergebnis ist ein objektiver Bericht über den Ist-Zustand im Alltag – praxisnah und ohne Schönfärberei.</p>
<h2>Warum Testkäufe so wertvoll sind</h2>
<ul><li><strong>Früherkennung von Schwachstellen:</strong> Viele Sicherheitslücken fallen erst im realen Ablauf auf. Testkäufe decken sie zuverlässig auf.</li><li><strong>Mitarbeiterschulung:</strong> Erkenntnisse aus den Tests fließen gezielt in Schulungen ein.</li><li><strong>Prävention statt Reaktion:</strong> Wer Probleme erkennt, bevor sie zu Schäden führen, spart Kosten.</li><li><strong>Kundenerlebnis verbessern:</strong> Testkäufe prüfen auch, ob Mitarbeiter freundlich, aufmerksam und kundenorientiert arbeiten.</li></ul>
<h2>Unterschied zu klassischen Kontrollen</h2>
<p>Während Kontrollen oft angekündigt oder routinemäßig stattfinden, sind Testkäufe unauffällig und realistisch. Händler erfahren, wie ihre Abläufe tatsächlich funktionieren – nicht nur, wie sie auf dem Papier geplant sind.</p>
<h2>Testkäufe im Sicherheitskonzept</h2>
<p>Für einen Sicherheitsdienst gehören Testkäufe zum Gesamtpaket moderner Prävention. In Kombination mit Ladendetektiven und Objektschutz entsteht ein umfassendes Schutzsystem:</p>
<ul><li>Detektive erkennen akute Risiken.</li><li>Objektschutz sichert das Umfeld.</li><li>Testkäufe zeigen, ob Abläufe und Mitarbeiter im Alltag wirklich standhalten.</li></ul>
<h2>Fazit</h2>
<p>Testkäufe sind kein Kontrollinstrument gegen Mitarbeiter, sondern eine Chance zur Weiterentwicklung. Sie schaffen Klarheit, fördern Sicherheit und stärken das Vertrauen zwischen Kunden, Mitarbeitern und Unternehmen. Mehr dazu: <a href="testkaeufe.html">Testkäufe im Einzelhandel</a>.</p>'''),
 ('blog-diebstahlpraevention.html', 'post/wachsam-bleiben-clevere-strategien-zur-diebstahlprävention-im-einzelhandel.html', 'Wachsam bleiben – clevere Strategien zur Diebstahlprävention im Einzelhandel', '2025-09-10', '2 Min. Lesezeit', 'ladendetektei',
  'Präsenz, Sichtbarkeit, Technik und geprüfte Abläufe: vier Hebel, mit denen Händler Verluste durch Ladendiebstahl wirksam senken.',
  '''<p>Ladendiebstahl ist kein Kleinrisiko. Laut der EHI-Studie „Inventurdifferenzen 2025“ verliert der deutsche Einzelhandel rund 3,05 Milliarden Euro pro Jahr durch Ladendiebstahl – und mehr als 98 Prozent der Fälle bleiben unentdeckt. Die Kosten tragen am Ende oft die Kunden über höhere Preise. Die gute Nachricht: Schon einige gezielte Maßnahmen können Ihre Verluste deutlich senken – ohne übertriebenen Aufwand.</p>
<h2>1. Präsenz zeigt Wirkung – Sicherheitspersonal als Abschreckung</h2>
<p>Gut geschulte Sicherheitskräfte, etwa <a href="ladendetektiv-ulm.html">Ladendetektive</a>, wirken präventiv: Ihre unaufdringliche Anwesenheit im Geschäft signalisiert potenziellen Dieben, dass ihr Verhalten beobachtet wird.</p>
<h2>2. Sichtbarkeit schaffen – klare Raumgestaltung &amp; Videoüberwachung</h2>
<p>Ein heller, offener Laden macht es Dieben schwer, sich unbemerkt zu verhalten. Kameras erhöhen sowohl das Gefühl von Sicherheit als auch die Beweiskraft im Ernstfall. Beachten Sie dabei die Datenschutzpflichten.</p>
<h2>3. Technik einsetzen – Warensicherung &amp; Sicherheitsspiegel</h2>
<p>RFID-Etiketten, Sensorschleusen oder Warensicherungssysteme schützen gezielt Artikel. Sicherheitsspiegel helfen Mitarbeitern, tote Winkel im Blick zu behalten – vor allem in verwinkelten Verkaufsräumen eine effektive und kostengünstige Lösung.</p>
<h2>4. Abläufe prüfen – Testkäufe für Prozesse &amp; Mitarbeiter</h2>
<p><a href="testkaeufe.html">Testkäufe</a> dienen nicht der Kontrolle, sondern der Qualitätsverbesserung. Die Ergebnisse führen zu Schulungen und besseren Abläufen.</p>
<h2>Fazit</h2>
<p>Verluste durch Diebstahl lassen sich wirksam reduzieren – durch eine Kombination aus physischer Präsenz, Technik und gezielter Prozesskontrolle. Als inhabergeführter Sicherheitsdienst in Ulm unterstützen wir Sie dabei – lokal, persönlich und effizient.</p>
<p class="src">Quelle: <a href="https://www.ehi.org/themen/inventurdifferenzen-sicherheit/" rel="noopener" target="_blank">EHI Retail Institute, Inventurdifferenzen 2025</a></p>'''),
]


def datum(iso):
    y, m, d = iso.split('-')
    return f'{int(d)}. {["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"][int(m)-1]} {y}'


def blog():
    cards = ''.join(f'''<a class="post" href="{fn}" data-up><div class="im"><img src="img/{im}-760.webp" alt="" loading="lazy" width="760" height="434"></div><div class="tx"><span class="meta">{datum(dt)} · {rt}</span><h2>{t}</h2><p>{teaser}</p><span class="more">Weiterlesen {I["arrow"]}</span></div></a>''' for fn, old, t, dt, rt, im, teaser, _ in POSTS)
    body = phero('Der Sicherheitsblog', 'Prävention, Schutz &amp; <span class="gold">Vertrauen.</span>',
                 'Wissen aus der Praxis: Ladendetektiv, Objektschutz und Testkäufe – verständlich erklärt.', crumb='Sicherheitsblog') + \
        f'<section class="sec" style="padding-top:40px"><div class="wrap"><div class="posts">{cards}</div></div></section>' + cta_block()
    page('blog.html', 'Sicherheitsblog | Hettich Sicherheitsdienst Ulm', 'Tipps und Wissen rund um Ladendetektiv, Objektschutz und Testkäufe vom Hettich Sicherheitsdienst in Ulm und Neu-Ulm.',
         body, crumbs=[('blog.html', 'Sicherheitsblog')], prio='0.6')
    for fn, old, t, dt, rt, im, teaser, html in POSTS:
        others = ''.join(f'<li><a href="{f2}">{t2}</a></li>' for f2, o2, t2, *_ in POSTS if f2 != fn)
        body = f'''<section class="phero" style="padding-bottom:40px"><canvas class="fx" data-fx="waves" aria-hidden="true"></canvas><div class="wrap"><nav class="crumbs" aria-label="Brotkrumen" data-up><a href="index.html">Start</a> / <a href="blog.html">Sicherheitsblog</a></nav><span class="eyebrow" data-up><time datetime="{dt}">{datum(dt)}</time> · {rt}</span><h1 class="h-l" data-split style="max-width:1000px">{t}</h1></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap">
 <div class="article-img" data-up><img src="img/{im}-1400.webp" alt="" width="1344" height="768"></div>
 <article class="prose" data-up>{html}
  <h2>Weitere Beiträge</h2><ul>{others}</ul>
 </article>
</div></section>''' + cta_block()
        art = {"@type": "BlogPosting", "headline": t, "datePublished": dt, "dateModified": "2026-10-02", "image": BASE + f"img/{im}-1400.webp",
               "author": {"@type": "Person", "name": "Jan Hettich"}, "publisher": {"@id": BASE + "#firma"}, "mainEntityOfPage": BASE + fn, "inLanguage": "de-DE", "description": teaser}
        seo = {'blog-objektschutz.html': 'Objektschutz erklärt: mehr als nur Wachschutz | Hettich',
               'blog-testkaeufe.html': 'Testkäufe im Handel: warum sie so wichtig sind | Hettich',
               'blog-diebstahlpraevention.html': 'Diebstahlprävention im Einzelhandel: 4 Strategien | Hettich'}[fn]
        page(fn, seo, teaser, body, [art], [('blog.html', 'Sicherheitsblog'), (fn, t.split(' – ')[0])], prio='0.5')
        redirect(old, fn, t)


def legal():
    imp = f'''<div class="legal">
 <div class="box" data-up><h2><span>01</span>Angaben gemäß § 5 DDG</h2><p>Hettich Sicherheitsdienst<br>Inhaber: Jan Hettich<br>Kapellenstraße 1<br>89269 Vöhringen<br>Deutschland</p></div>
 <div class="box" data-up><h2><span>02</span>Kontakt</h2><p>Telefon: <a href="{TEL_HREF}">{TEL}</a><br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p></div>
 <div class="box" data-up><h2><span>03</span>Umsatzsteuer</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: DE367352444</p></div>
 <div class="box" data-up><h2><span>04</span>Erlaubnis &amp; Aufsicht</h2><p>Bewachungsgewerbe gemäß § 34a GewO mit Erlaubnis (uneingeschränkte Bewachungserlaubnis).<br>Registriert im Bewacherregister – ID 18865.<br>Zuständige Aufsichtsbehörde: Landratsamt Neu-Ulm.</p></div>
 <div class="box" data-up><h2><span>05</span>Verantwortlich für den Inhalt</h2><p>Verantwortlich nach § 18 Abs. 2 MStV: Jan Hettich, Anschrift wie oben.</p></div>
 <div class="box" data-up><h2><span>06</span>Haftung</h2><p>Die Inhalte dieser Website wurden mit größter Sorgfalt erstellt. Für Richtigkeit, Vollständigkeit und Aktualität übernehmen wir keine Gewähr. Für Inhalte verlinkter externer Seiten ist stets der jeweilige Anbieter verantwortlich.</p></div>
 <div class="box" data-up><h2><span>07</span>Verbraucherstreitbeilegung</h2><p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p></div>
</div>'''
    pl = lambda t, lead, crumb: f'''<section class="phero"><canvas class="fx" data-fx="waves" aria-hidden="true"></canvas><div class="wrap"><nav class="crumbs" aria-label="Brotkrumen" data-up><a href="index.html">Start</a> / {crumb}</nav><span class="eyebrow" data-up>Rechtliches</span><h1 class="h-l" data-split>{t}</h1><p class="lead" data-up>{lead}</p></div></section>'''
    page('impressum.html', 'Impressum | Hettich Sicherheitsdienst', 'Impressum des Hettich Sicherheitsdienstes, Kapellenstraße 1, 89269 Vöhringen – Bewachungsunternehmen nach § 34a GewO.',
         pl('Impressum', 'Anbieterkennzeichnung des Hettich Sicherheitsdienstes.', 'Impressum') + f'<section class="sec" style="padding-top:20px"><div class="wrap">{imp}</div></section>',
         crumbs=[('impressum.html', 'Impressum')], prio='0.3')
    ds = f'''<div class="legal">
 <div class="box" data-up><h2><span>01</span>Verantwortliche Stelle</h2><p>Hettich Sicherheitsdienst · Inhaber Jan Hettich · Kapellenstraße 1, 89269 Vöhringen<br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a> · Telefon: {TEL}</p></div>
 <div class="box" data-up><h2><span>02</span>Hosting</h2><p>Diese Website wird als statische Seite über GitHub Pages (GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA) ausgeliefert. Beim Abruf werden technische Zugriffsdaten verarbeitet (IP-Adresse, Zeitpunkt, abgerufene Datei, Browsertyp). Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO – unser berechtigtes Interesse an einer sicheren und stabilen Bereitstellung. GitHub ist unter dem EU-US Data Privacy Framework zertifiziert; ergänzend gelten die EU-Standardvertragsklauseln.</p></div>
 <div class="box" data-up><h2><span>03</span>Keine Analyse, keine Cookies</h2><p>Diese Website setzt keine Analyse- oder Marketing-Werkzeuge ein, bildet keine Profile und bindet keine Inhalte oder Schriftarten fremder Anbieter ein. Es werden keine Cookies gesetzt. Lediglich ein technisch notwendiger Eintrag im Sitzungsspeicher Ihres Browsers merkt sich, dass die Startanimation bereits gezeigt wurde; er wird beim Schließen des Browsers gelöscht (§ 25 Abs. 2 Nr. 2 TDDDG).</p></div>
 <div class="box" data-up><h2><span>04</span>Kontaktaufnahme</h2><p>Wenn Sie uns per E-Mail, Telefon oder über das Kontaktformular (es öffnet Ihr eigenes E-Mail-Programm) kontaktieren, verarbeiten wir Ihre Angaben ausschließlich zur Bearbeitung der Anfrage (Art. 6 Abs. 1 lit. b DSGVO). Unser E-Mail-Postfach wird über Microsoft 365 (Microsoft Ireland Operations Ltd., Dublin) betrieben. Die Daten werden gelöscht, sobald die Anfrage abgeschlossen ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p></div>
 <div class="box" data-up><h2><span>05</span>Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21 DSGVO) – formlos an die oben genannte Adresse.</p><p>Beschwerderecht: Bayerisches Landesamt für Datenschutzaufsicht (BayLDA), Promenade 18, 91522 Ansbach.</p></div>
</div>'''
    page('datenschutz.html', 'Datenschutz | Hettich Sicherheitsdienst', 'Datenschutzerklärung des Hettich Sicherheitsdienstes: keine Cookies, keine Analyse, keine fremden Schriftarten.',
         pl('Datenschutz', 'Stand: 2. Oktober 2026', 'Datenschutz') + f'<section class="sec" style="padding-top:20px"><div class="wrap">{ds}</div></section>',
         crumbs=[('datenschutz.html', 'Datenschutz')], prio='0.3')


def extras():
    # 404
    body = f'''<section class="phero e404"><canvas class="fx" data-fx="rings" aria-hidden="true"></canvas><div class="wrap"><span class="eyebrow">Fehler 404</span><h1 class="h-l" style="margin:20px 0">Diese Seite gibt es <span class="gold">nicht (mehr).</span></h1><p class="lead">Vielleicht hilft Ihnen einer dieser Wege weiter:</p><div class="ctas" style="display:flex;flex-wrap:wrap;gap:14px;margin-top:30px">{btn("index.html", "Zur Startseite")}{btn("dienstleistungen.html", "Dienstleistungen", "line")}{btn(TEL_HREF, "Anrufen", "line")}</div></div></section>'''
    out = head('404.html', 'Seite nicht gefunden | Hettich Sicherheitsdienst', 'Diese Seite wurde nicht gefunden.').replace('<link rel="canonical" href="https://www.hettich-sicherheitsdienst.de/404.html">', '').replace(f'content="{"index,follow,max-image-preview:large" if LIVE else "noindex,nofollow"}"', 'content="noindex"')
    # Auf GitHub Pages wird 404.html unter beliebigen Pfaden ausgeliefert → absolute Pfade setzen
    out += header('404.html') + '<main id="main">' + body + '</main>' + footer()
    base_tag = '<base href="/">' if LIVE else '<base href="/hettich-sicherheitsdienst-neu/">'
    out = out.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + base_tag, 1)
    (ROOT / '404.html').write_text(out, encoding='utf-8')
    # alte Wix-Adressen
    redirect('blank.html', 'vision.html', 'Vision')
    redirect('loslegen.html', 'kontakt.html', 'Kontakt')
    redirect('cookies.html', 'datenschutz.html', 'Datenschutz')
    redirect('jobs.html', 'kontakt.html', 'Kontakt')
    # Sitemap + robots + Manifest
    urls = ''.join(f'<url><loc>{BASE if fn == "index.html" else BASE + fn}</loc><lastmod>2026-10-02</lastmod><priority>{p}</priority></url>' for fn, p in SITEMAP)
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding='utf-8')
    (ROOT / 'robots.txt').write_text(('User-agent: *\nAllow: /\n' if LIVE else 'User-agent: *\nDisallow: /\n') + f'\nSitemap: {BASE}sitemap.xml\n', encoding='utf-8')
    (ROOT / 'site.webmanifest').write_text(json.dumps({"name": "Hettich Sicherheitsdienst", "short_name": "Hettich", "start_url": "./", "display": "standalone",
        "background_color": "#09090a", "theme_color": "#09090a", "icons": [{"src": "img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    index(); ladendetektiv(); objektschutz(); testkaeufe(); dienstleistungen(); vision(); kontakt(); blog(); legal(); extras()
    print('fertig:', len(SITEMAP), 'Seiten,', 'LIVE' if LIVE else 'VORSCHAU (noindex)')
