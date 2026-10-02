#!/usr/bin/env python3
"""Baut alle Seiten der Hettich-Website (v4) aus einem gemeinsamen Rahmen.
Aufruf: python3 build.py  → schreibt *.html in diesen Ordner."""
import pathlib, json

ROOT = pathlib.Path(__file__).parent
LOGO = open(ROOT / 'img/logo.svg').read()  # Original-Logo, unverändert (#FFD700)

TEL = '0171 7449939'
TEL_HREF = 'tel:+491717449939'
MAIL = 'info@hettich-sicherheitsdienst.de'

I = {
 'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="M7 17 17 7M8 7h9v9"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg>',
 'eye': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l18 18"/><path d="M10.6 5.1A10 10 0 0 1 12 5c5 0 9 4.5 10 7-.4 1-1.2 2.3-2.4 3.5M6.6 6.6C4.4 8 2.9 10.1 2 12c1 2.5 5 7 10 7 1.8 0 3.4-.6 4.8-1.4"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/></svg>',
 'badge': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="6"/><path d="m9 14.5-1.5 7 4.5-2.5 4.5 2.5-1.5-7"/><path d="m10 9 1.5 1.5L14 8"/></svg>',
 'lock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15.5" r="1.5"/></svg>',
 'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2.5"/><path d="m22 7-10 6L2 7"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
 'plus': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" width="16" height="16"><path d="M12 5v14M5 12h14"/></svg>',
}

NAV = [('index.html', 'Start'), ('dienstleistungen.html', 'Dienstleistungen'), ('vision.html', 'Vision'), ('blog.html', 'Sicherheitsblog')]


def btn(href, text, kind='gold', extra=''):
    return f'<a class="btn btn-{kind} {extra}" href="{href}">{text}<span class="ar">{I["arrow"]}</span></a>'


def head(title, desc, page):
    return f'''<!doctype html>
<html lang="de" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#09090a">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="img/og.jpg">
<link rel="icon" href="img/logo.svg" type="image/svg+xml">
<link rel="preload" href="fonts/poppins-300-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
</head>
<body data-page="{page}">
<div class="loader" aria-hidden="true">{LOGO}<div class="bar"><i></i></div></div>
<div class="progress" aria-hidden="true"></div>
<div class="grid-bg" aria-hidden="true"></div>
<div class="noise" aria-hidden="true"></div>
'''


def header(page):
    on = ' class="on" aria-current="page"'
    links = ''.join(f'<a href="{h}"{on if h == page else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="hdr">
 <div class="wrap">
  <a class="brand" href="index.html" aria-label="Hettich Sicherheitsdienst – Startseite">{LOGO}<div><b>Hettich</b><span>Sicherheitsdienst</span><small>Weil Sicherheit Vertrauen schafft.</small></div></a>
  <nav class="nav" aria-label="Hauptmenü">{links}{btn("kontakt.html", "Kontakt", "line", "btn-sm")}</nav>
  <button class="burger" aria-label="Menü öffnen" aria-expanded="false"><i></i><i></i></button>
 </div>
</header>
'''


def footer():
    return f'''<footer class="ftr">
 <div class="wrap">
  <div class="big" aria-hidden="true">Weil Sicherheit Vertrauen schafft.</div>
  <div class="row">
   <div><a class="brand" href="index.html">{LOGO}<div><b>Hettich</b><span>Sicherheitsdienst</span></div></a>
    <p class="muted" style="font-size:14px;margin-top:18px;max-width:300px">Ladendetektei, Objektschutz und individuelle Sicherheitslösungen in Ulm, um Ulm und um Ulm herum.</p></div>
   <div><h4>Seiten</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}<li><a href="kontakt.html">Kontakt</a></li></ul></div>
   <div><h4>Kontakt</h4><ul><li><a href="{TEL_HREF}">{TEL}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>Ulm · Neu-Ulm · Umgebung</li></ul></div>
   <div><h4>Rechtliches</h4><ul><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li><li>§ 34a GewO · ID 18865</li></ul></div>
  </div>
  <div class="bottom"><span>© 2026 Hettich Sicherheitsdienst</span><span>Zugelassenes Bewachungsunternehmen nach § 34a GewO</span></div>
 </div>
</footer>
<a class="fab magnet" href="{TEL_HREF}" aria-label="Jetzt anrufen: {TEL}"><span class="ic">{I["phone"]}</span><span class="lbl">Jetzt anrufen</span></a>
<script src="js/gsap.min.js"></script>
<script src="js/ScrollTrigger.min.js"></script>
<script src="js/lenis.min.js"></script>
<script src="js/site.js"></script>
</body>
</html>
'''


def page(fn, title, desc, body):
    out = head(title, desc, fn) + header(fn) + '<main>\n' + body + '\n</main>\n' + footer()
    (ROOT / fn).write_text(out, encoding='utf-8')
    print('geschrieben', fn, len(out))


def contact_rows():
    return f'''<div class="contact-rows">
 <a class="crow" href="{TEL_HREF}"><span class="ic">{I["phone"]}</span><span><small>Telefon – auch kurzfristig</small><b>{TEL}</b></span></a>
 <a class="crow" href="mailto:{MAIL}"><span class="ic">{I["mail"]}</span><span><small>E-Mail</small><b>{MAIL}</b></span></a>
 <div class="crow"><span class="ic">{I["pin"]}</span><span><small>Einsatzgebiet</small><b>Ulm, Neu-Ulm &amp; Umgebung</b></span></div>
</div>'''


def cta_block():
    return f'''<section class="sec cta" id="kontakt">
 <div class="wrap"><div class="frame"><div class="cols">
  <div><canvas class="fx" data-fx="globe" aria-hidden="true"></canvas><h2 class="h-l" data-split>Bereit für mehr <span class="gold">Sicherheit?</span></h2></div>
  <div>
   <p data-up>Ob Ladendetektei, Objektschutz oder individuelle Sicherheitslösung – wir sind Ihr Partner für maßgeschneiderte Sicherheit.</p>
   <p data-up class="muted">Schnell erreichbar, flexibel im Einsatz und immer diskret. Nehmen Sie jetzt Kontakt auf und erhalten Sie Ihr persönliches Sicherheitskonzept.</p>
   <div data-up>{contact_rows()}</div>
   <div data-up style="display:flex;flex-wrap:wrap;gap:14px;align-items:center">{btn("kontakt.html", "Kontakt aufnehmen")}<span class="muted" style="font-size:13px">Unverbindlich anfragen – wir melden uns umgehend.</span></div>
  </div>
 </div></div></div>
</section>'''


SVC = [
 ('Ladendetektei', 'ladendetektei', 'Unsere Kernkompetenz. Mit geschultem Blick und unauffälliger Präsenz decken wir Diebstähle frühzeitig auf und verhindern hohe Verluste im Einzelhandel – in Ulm, um Ulm und um Ulm herum.'),
 ('Objektschutz', 'objektschutz', 'Kontrollgänge, Präsenz und moderne Technik für Firmengebäude, Parkplätze, Baustellen und Lagerflächen – damit geschützt bleibt, was Ihnen wichtig ist.'),
 ('Testkäufe', 'testkauf', 'Geschulte Tester treten als Kunden auf und zeigen, wie aufmerksam Ihr Team arbeitet und wo Abläufe nachgeschärft werden sollten – zur Schulung, nicht zur Bestrafung.'),
 ('Individuelle Lösungen', 'individuell', 'Veranstaltungsschutz, Personenschutz oder spezielle Überwachungsaufgaben: Wir entwickeln ein Konzept, das exakt zu Ihren Anforderungen passt.'),
]


def index():
    vals = [('shield', 'Prävention', 'Gefahren erkennen, bevor sie entstehen: Mit vorausschauenden Maßnahmen schützen wir Menschen, Werte und Objekte effektiv und nachhaltig.'),
            ('eye', 'Diskretion', 'Wir arbeiten unauffällig und mit höchster Verschwiegenheit. So bleibt Ihre Sicherheit jederzeit geschützt, ohne Aufmerksamkeit zu erregen.'),
            ('badge', 'Professionalität', 'Unsere Mitarbeiter sind geschult, erfahren und handeln nach höchsten Standards – auf jedem Einsatzgebiet.'),
            ('lock', 'Vertrauen', 'Verlässlichkeit und Transparenz: Durch klare Kommunikation und konsequentes Handeln schaffen wir die Basis für langfristiges Vertrauen.')]
    cards = ''.join(f'<article class="card" data-up><div class="ic">{I[ic]}</div><h3>{t}</h3><p>{p}</p><span class="ln"></span></article>' for ic, t, p in vals)
    items = ''.join(f'''<div class="svc-item" role="button" tabindex="0" aria-expanded="false"><span class="no">0{i+1}</span><div><h3>{t}</h3><p>{p}</p><div class="mimg"><img src="img/{im}-760.webp" alt="" loading="lazy" width="760" height="434"></div></div><span class="plus">{I["plus"]}</span></div>''' for i, (t, im, p) in enumerate(SVC))
    imgs = ''.join(f'<img src="img/{im}-1400.webp" alt="{t}" loading="lazy" width="1344" height="768">' for t, im, p in SVC)
    mq = ''.join(f'<span>{w}<em>✦</em></span>' for w in ['Prävention', 'Diskretion', 'Professionalität', 'Vertrauen', 'Ladendetektei', 'Objektschutz', 'Testkäufe', 'Ulm &amp; Umgebung'] * 2)
    ld = json.dumps({"@context": "https://schema.org", "@type": "SecurityService", "name": "Hettich Sicherheitsdienst",
                     "telephone": "+49 171 7449939", "email": MAIL, "url": "https://www.hettich-sicherheitsdienst.de/",
                     "areaServed": ["Ulm", "Neu-Ulm", "Alb-Donau-Kreis", "Landkreis Neu-Ulm"],
                     "address": {"@type": "PostalAddress", "addressLocality": "Vöhringen", "postalCode": "89269", "addressCountry": "DE"},
                     "slogan": "Weil Sicherheit Vertrauen schafft."}, ensure_ascii=False)
    body = f'''<script type="application/ld+json">{ld}</script>
<section class="hero">
 <canvas class="fx" data-fx="waves" aria-hidden="true"></canvas>
 <div class="wrap">
  <div class="hero-logo">{LOGO}</div>
  <div>
   <span class="eyebrow" data-up>Hettich Sicherheitsdienst · Ulm</span>
   <h1 class="h-xl" data-split>Weil Sicherheit <span class="gold">Vertrauen</span> schafft.</h1>
   <p class="lead" data-up>Sicherheitslösungen für Unternehmen – Objektschutz &amp; Ladendetektei in Ulm und Umgebung. Zuverlässig, diskret und modern.</p>
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
   <p data-up class="muted">Mit dem Hettich Sicherheitsdienst erhalten Sie individuelle Sicherheitskonzepte, die exakt auf Ihre Anforderungen abgestimmt sind. Ob Objektschutz, Ladendetektive oder Veranstaltungssicherheit – wir sorgen für Prävention, Schutz und Vertrauen.</p>
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
   <p class="reveal-words">Der Hettich Sicherheitsdienst ist ein inhabergeführtes Unternehmen mit klarem Schwerpunkt auf Ladendetektei in Ulm, um Ulm und um Ulm herum. Unsere erfahrenen Ladendetektive arbeiten diskret, professionell und haben bereits zahlreiche Diebstähle im Einzelhandel erfolgreich aufgeklärt.</p>
   <p class="reveal-words">Neben unserer Kernkompetenz im Handel bieten wir Objektschutz in Ulm und der Region sowie kundenorientierte Veranstaltungssicherheit – individuell geplant, flexibel, für Privatkunden ebenso wie für Unternehmen.</p>
   <div data-up style="margin-top:34px">{btn("vision.html", "Unsere Vision", "line")}</div>
  </div>
 </div></div></div>
</section>

<section class="sec" id="leistungen" style="padding-top:0">
 <div class="wrap">
  <div class="svc-head"><div><span class="eyebrow" data-up>Dienstleistungen</span><h2 class="h-l" data-split style="margin-top:16px">Was wir für Sie <span class="gold">schützen.</span></h2></div><div data-up>{btn("dienstleistungen.html", "Alle Leistungen im Detail", "line")}</div></div>
  <div class="svc">
   <div class="svc-list">{items}</div>
   <div class="svc-stage">{imgs}<div class="cap"><span>Ladendetektei</span><b>01</b></div></div>
  </div>
 </div>
</section>

<section class="sec nums" style="padding-top:0">
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
{cta_block()}'''
    page('index.html', 'Hettich Sicherheitsdienst Ulm | Ladendetektiv & Objektschutz',
         'Hettich Sicherheitsdienst: Ladendetektei, Objektschutz, Testkäufe und individuelle Sicherheitslösungen in Ulm, Neu-Ulm und Umgebung. Zugelassen nach § 34a GewO.', body)


def phero(eyebrow, h1, lead, fx='waves', crumb=None):
    c = f'<div class="crumbs" data-up><a href="index.html">Start</a> / {crumb}</div>' if crumb else ''
    return f'''<section class="phero"><canvas class="fx" data-fx="{fx}" aria-hidden="true"></canvas><div class="wrap">{c}<span class="eyebrow" data-up>{eyebrow}</span><h1 class="h-l" data-split>{h1}</h1><p class="lead" data-up>{lead}</p></div></section>'''


def dienstleistungen():
    D = [
     ('Ladendetektei', 'Diskret und effektiv', 'ladendetektei', ['Kernkompetenz', 'Einzelhandel', 'Inventurdifferenzen senken'],
      'Unsere Kernkompetenz liegt in der Ladendetektei. Mit geschultem Blick und unauffälliger Präsenz decken wir Diebstähle frühzeitig auf und verhindern hohe Verluste im Einzelhandel. In Ulm, um Ulm und um Ulm herum haben wir bereits zahlreiche Fälle erfolgreich gelöst.',
      'Unsere Detektive arbeiten diskret, professionell und kundenorientiert – für maximale Sicherheit im Handel.'),
     ('Objektschutz', 'Schutz für Gebäude und Werte', 'objektschutz', ['Kontrollgänge', 'Parkplätze', 'Baustellen', 'Lagerflächen'],
      'Parkplätze sind besonders gefährdet durch Vandalismus und Diebstähle. Unser Objektschutz in Ulm sorgt mit Kontrollgängen, Präsenz und moderner Technik für die Sicherheit von Fahrzeugen, Besuchern und Mitarbeitern.',
      'Zusätzlich sichern wir Firmengebäude, Baustellen und Lagerflächen zuverlässig ab – mit geschultem Personal und abgestimmter Technik. So schützen wir, was Ihnen wichtig ist.'),
     ('Testkäufe', 'Kontrolle und Mitarbeiterschulung im Alltag', 'testkauf', ['Mystery Shopping', 'Qualitätssicherung', 'Schulung'],
      'Testkäufe sind ein wirkungsvolles Instrument, um Abläufe und Mitarbeiter im Einzelhandel realistisch zu prüfen. Geschulte Tester treten als Kunden auf und machen sichtbar, wie aufmerksam Ihr Team arbeitet, ob Waren richtig gesichert sind und wo Verbesserungsbedarf besteht.',
      'Die Ergebnisse dienen nicht der Bestrafung, sondern der Mitarbeiterschulung und Qualitätssicherung – damit Ihr Geschäft dauerhaft sicher aufgestellt ist.'),
     ('Individuelle Sicherheitslösungen', 'Flexibel und bedarfsgerecht', 'individuell', ['Veranstaltungsschutz', 'Personenschutz', 'Sonderaufgaben'],
      'Neben unseren Kernbereichen bieten wir auf Anfrage maßgeschneiderte Sicherheitsdienstleistungen an. Ob Veranstaltungsschutz, Personenschutz oder spezielle Überwachungsaufgaben – wir entwickeln ein Konzept, das exakt auf Ihre Anforderungen zugeschnitten ist.',
      'Flexibel, zuverlässig und diskret.'),
     ('Nahtlose Integration', 'In Ihr Unternehmen', 'empfang', ['Enge Abstimmung', 'Klare Kommunikation', 'Minimale Störung'],
      'Ob im Einzelhandel, bei Veranstaltungen oder im Objektschutz – wir passen uns Ihren Strukturen an und arbeiten unauffällig im Hintergrund. Unser Ziel: maximale Sicherheit bei minimaler Störung Ihres Betriebsablaufs.',
      'Durch enge Abstimmung und klare Kommunikation integrieren wir uns reibungslos in Ihr bestehendes Team – flexibel, professionell und diskret.'),
    ]
    blocks = ''.join(f'''<article class="detail" data-up><div class="im"><img data-par src="img/{im}-1400.webp" alt="{t}" loading="lazy" width="1344" height="768"></div>
<div class="tx"><span class="no">0{i+1} — {sub}</span><h2>{t}</h2><p>{p1}</p><p class="muted">{p2}</p><div class="tags">{"".join(f"<span>{x}</span>" for x in tags)}</div><div>{btn("kontakt.html", "Jetzt anfragen", "line", "btn-sm")}</div></div></article>''' for i, (t, sub, im, tags, p1, p2) in enumerate(D))
    body = phero('Unsere Dienstleistungen', 'Ladendetektei, Objektschutz &amp; <span class="gold">Sicherheit</span> in Ulm und Umgebung.',
                 'Der Hettich Sicherheitsdienst ist Ihr Partner für diskrete, professionelle Sicherheit – vom Supermarkt bis zum Firmengelände.', crumb='Dienstleistungen') + \
        f'<section class="sec" style="padding-top:20px"><div class="wrap">{blocks}</div></section>' + cta_block()
    page('dienstleistungen.html', 'Dienstleistungen | Hettich Sicherheitsdienst Ulm',
         'Ladendetektei, Objektschutz, Testkäufe und individuelle Sicherheitslösungen in Ulm und Umgebung – diskret, flexibel und professionell.', body)


def vision():
    body = phero('Unsere Vision', 'Sicherheit neu denken – <span class="gold">diskret, präventiv und modern.</span>',
                 'Wir wollen in Ulm und der Region der erste Ansprechpartner für professionelle Ladendetektei, Objektschutz und maßgeschneiderte Sicherheitslösungen sein.', 'rings', 'Vision') + f'''
<section class="sec" style="padding-top:30px"><div class="wrap">
 <div class="frame"><div class="cols">
  <div class="prose">
   <h2 data-up style="margin-top:0">Was uns auszeichnet</h2>
   <p data-up>Der Hettich Sicherheitsdienst steht für maßgeschneiderte Sicherheitslösungen, die sich konsequent an den Bedürfnissen unserer Kunden orientieren. Ob Ladendetektei in Ulm, um Ulm und um Ulm herum, Objektschutz für Gebäude und Werte oder diskrete Sicherheitsmaßnahmen im Hintergrund – wir stehen für Verlässlichkeit, Diskretion und Professionalität.</p>
   <p data-up>Unser Unternehmen zeichnet sich durch persönliche Betreuung, kurze Entscheidungswege und schnelle Reaktionszeiten aus. Während große Anbieter oft unpersönlich arbeiten, profitieren unsere Kunden von direkter Kommunikation und flexiblen Lösungen. Jeder Auftrag wird individuell geplant, um Risiken frühzeitig zu erkennen und Schäden zu verhindern.</p>
   <p data-up>So schaffen wir ein Umfeld, in dem Menschen, Unternehmen und Werte langfristig geschützt und Vertrauen gestärkt wird.</p>
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
         'Unsere Vision: Sicherheit neu denken – diskret, präventiv und modern. Persönliche Betreuung, kurze Wege, schnelle Reaktion.', body)


def kontakt():
    fields = [('Vorname', 'text', ''), ('Nachname', 'text', ''), ('E-Mail', 'email', 'required'), ('Telefon', 'tel', ''), ('Unternehmen', 'text', ''), ('Position', 'text', '')]
    fl = ''.join(f'<div class="field"><input id="f{i}" name="{n}" type="{t}" placeholder=" " {r} autocomplete="on"><label for="f{i}">{n}{" *" if r else ""}</label></div>' for i, (n, t, r) in enumerate(fields))
    body = phero('Kontakt', 'Bereit für mehr <span class="gold">Sicherheit?</span>',
                 'Ob Ladendetektei, Objektschutz oder individuelle Sicherheitslösung – nehmen Sie unverbindlich Kontakt auf und lassen Sie sich persönlich beraten.', 'globe', 'Kontakt') + f'''
<section class="sec" style="padding-top:30px"><div class="wrap"><div class="frame"><div class="cols">
 <div><span class="eyebrow" data-up>Direkt erreichen</span><h2 class="h-m" data-up style="margin:16px 0 26px">Am schnellsten geht es <span class="gold">telefonisch.</span></h2><div data-up>{contact_rows()}</div></div>
 <div><form class="form" data-mail novalidate data-up>
  {fl}
  <div class="field full"><textarea id="fm" name="Nachricht" placeholder=" " required></textarea><label for="fm">Ihre Nachricht *</label></div>
  <div class="full" style="display:flex;flex-wrap:wrap;gap:16px;align-items:center"><button class="btn btn-gold" type="submit">Anfrage senden<span class="ar">{I["arrow"]}</span></button>
  <span class="note">Öffnet Ihr E-Mail-Programm mit der fertigen Anfrage. Hinweise zum <a href="datenschutz.html" style="color:var(--gold)">Datenschutz</a>.</span></div>
 </form></div>
</div></div></div></section>'''
    page('kontakt.html', 'Kontakt | Hettich Sicherheitsdienst Ulm',
         'Kontakt zum Hettich Sicherheitsdienst in Ulm: Telefon 0171 7449939, E-Mail info@hettich-sicherheitsdienst.de. Unverbindlich anfragen.', body)


POSTS = [
 ('blog-objektschutz.html', 'Objektschutz erklärt – mehr als nur Wachschutz', '10. Sept. 2025 · 2 Min. Lesezeit', 'gebaeude',
  'Moderner Objektschutz verbindet Erfahrung mit Technik, schafft Vertrauen und schützt Gebäude, Werte und Menschen rund um die Uhr.',
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
<p>Objektschutz ist weit mehr als nur Wachschutz. Wer auf eine Kombination aus moderner Technik, geschultem Sicherheitspersonal und maßgeschneiderten Konzepten setzt, erhält ein Sicherheitsnetz, das effizient, flexibel und nachhaltig ist.</p>'''),
 ('blog-testkaeufe.html', 'Testkäufe im Handel – warum sie so wichtig sind', '10. Sept. 2025 · 2 Min. Lesezeit', 'testkauf',
  'Mystery Shopping deckt Schwachstellen auf, stärkt die Mitarbeiterschulung und sichert Servicequalität im Einzelhandel.',
  '''<p>Im Einzelhandel zählt nicht nur das Sortiment, sondern auch, wie zuverlässig Mitarbeiter und Abläufe funktionieren. Genau hier setzen Testkäufe – auch bekannt als Mystery Shopping – an. Sie sind ein wertvolles Instrument, um Prozesse realistisch zu überprüfen, Schwachstellen aufzudecken und Mitarbeiter gezielt zu schulen.</p>
<h2>Was sind Testkäufe?</h2>
<p>Bei einem Testkauf tritt eine geschulte Person als Kunde auf und prüft die Abläufe im Geschäft. Dabei wird unauffällig beobachtet, wie aufmerksam das Personal ist, ob Waren richtig gesichert sind und wie sich Mitarbeiter im Kundenkontakt verhalten. Das Ergebnis ist ein objektiver Bericht über den Ist-Zustand im Alltag – praxisnah und ohne Schönfärberei.</p>
<h2>Warum Testkäufe so wertvoll sind</h2>
<ul><li><strong>Früherkennung von Schwachstellen:</strong> Viele Sicherheitslücken fallen erst im realen Ablauf auf. Testkäufe decken diese zuverlässig auf.</li><li><strong>Mitarbeiterschulung:</strong> Erkenntnisse aus den Tests fließen gezielt in Schulungen ein.</li><li><strong>Prävention statt Reaktion:</strong> Wer Probleme erkennt, bevor sie zu Schäden führen, spart Kosten.</li><li><strong>Kundenerlebnis verbessern:</strong> Testkäufe prüfen auch, ob Mitarbeiter freundlich, aufmerksam und kundenorientiert arbeiten.</li></ul>
<h2>Unterschied zu klassischen Kontrollen</h2>
<p>Während Kontrollen oft angekündigt oder routinemäßig stattfinden, sind Testkäufe unauffällig und realistisch. Händler erfahren, wie ihre Abläufe tatsächlich funktionieren – nicht nur, wie sie auf dem Papier geplant sind.</p>
<h2>Testkäufe im Sicherheitskonzept</h2>
<p>Für einen Sicherheitsdienst gehören Testkäufe zum Gesamtpaket moderner Prävention. In Kombination mit Ladendetektiven und Objektschutz entsteht ein umfassendes Schutzsystem:</p>
<ul><li>Detektive erkennen akute Risiken.</li><li>Objektschutz sichert das Umfeld.</li><li>Testkäufe zeigen, ob Abläufe und Mitarbeiter im Alltag wirklich standhalten.</li></ul>
<h2>Fazit</h2>
<p>Testkäufe sind kein Kontrollinstrument gegen Mitarbeiter, sondern eine Chance zur Weiterentwicklung. Sie schaffen Klarheit, fördern Sicherheit und stärken das Vertrauen zwischen Kunden, Mitarbeitern und Unternehmen.</p>'''),
 ('blog-diebstahlpraevention.html', 'Wachsam bleiben – clevere Strategien zur Diebstahlprävention im Einzelhandel', '10. Sept. 2025 · 1 Min. Lesezeit', 'ladendetektei',
  'Präsenz, Sichtbarkeit, Technik und geprüfte Abläufe: vier Hebel, mit denen sich Verluste durch Diebstahl wirksam senken lassen.',
  '''<p>Ladendiebstahl ist kein Kleinrisiko. Laut einer Studie bleiben jährlich 3,5 Milliarden Euro Verlust unentdeckt – oft gedeckt durch höhere Preise für die Kundschaft. Die gute Nachricht: Schon einige gezielte Maßnahmen können Ihre Verluste deutlich senken – ohne übertriebenen Aufwand.</p>
<h2>1. Präsenz zeigt Wirkung – Sicherheitspersonal als Abschreckung</h2>
<p>Gut geschulte Sicherheitsmitarbeitende, etwa Ladendetektive, wirken präventiv: Ihre unaufdringliche Anwesenheit im Geschäft signalisiert potenziellen Dieben, dass Verhalten beobachtet wird.</p>
<h2>2. Sichtbarkeit schaffen – klare Raumgestaltung &amp; Videoüberwachung</h2>
<p>Ein heller, offener Laden macht es Dieben schwer, sich unbemerkt zu verhalten. Kameras erhöhen sowohl das Gefühl von Sicherheit als auch die Beweiskraft im Ernstfall. Beachten Sie dabei die Datenschutzpflichten.</p>
<h2>3. Technik einsetzen – Warensicherung &amp; Sicherheitsspiegel</h2>
<p>RFID-Etiketten, Sensorschleusen oder Warensicherungssysteme schützen gezielt Artikel. Sicherheitsspiegel helfen Mitarbeitern, tote Winkel im Blick zu behalten – vor allem in verwinkelten Verkaufsräumen eine effektive und kostengünstige Lösung.</p>
<h2>4. Abläufe prüfen – Testkäufe für Prozesse &amp; Mitarbeiter</h2>
<p>Mystery Shopping dient nicht zur Kontrolle, sondern zur Qualitätsoptimierung. Die Ergebnisse führen zu Schulungen und verbesserten Prozessen.</p>
<h2>Fazit</h2>
<p>Verluste durch Diebstahl lassen sich wirksam reduzieren – durch eine Kombination aus physischer Präsenz, Technik und gezielter Prozesskontrolle. Als inhabergeführter Sicherheitsdienst in Ulm unterstützen wir Sie dabei – lokal, persönlich und effizient.</p>'''),
]


def blog():
    cards = ''.join(f'''<a class="post" href="{fn}" data-up><div class="im"><img src="img/{im}-760.webp" alt="" loading="lazy" width="760" height="434"></div><div class="tx"><span class="meta">{meta}</span><h2>{t}</h2><p>{teaser}</p><span class="more">Weiterlesen {I["arrow"]}</span></div></a>''' for fn, t, meta, im, teaser, _ in POSTS)
    body = phero('Der Sicherheitsblog', 'Prävention, Schutz &amp; <span class="gold">Vertrauen.</span>',
                 'Wissen aus der Praxis: Ladendetektei, Objektschutz und Testkäufe – verständlich erklärt.', crumb='Sicherheitsblog') + \
        f'<section class="sec" style="padding-top:20px"><div class="wrap"><div class="posts">{cards}</div></div></section>' + cta_block()
    page('blog.html', 'Sicherheitsblog | Hettich Sicherheitsdienst Ulm', 'Tipps und Wissen rund um Ladendetektei, Objektschutz und Testkäufe vom Hettich Sicherheitsdienst in Ulm.', body)
    for fn, t, meta, im, teaser, html in POSTS:
        others = ''.join(f'<li><a href="{f2}">{t2}</a></li>' for f2, t2, *_ in POSTS if f2 != fn)
        body = f'''<section class="phero" style="padding-bottom:40px"><canvas class="fx" data-fx="waves" aria-hidden="true"></canvas><div class="wrap"><div class="crumbs" data-up><a href="index.html">Start</a> / <a href="blog.html">Sicherheitsblog</a></div><span class="eyebrow" data-up>{meta}</span><h1 class="h-l" data-split style="max-width:1000px">{t}</h1></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap">
 <div class="article-img" data-up><img src="img/{im}-1400.webp" alt="" width="1344" height="768"></div>
 <article class="prose" data-up>{html}
  <h2>Weitere Beiträge</h2><ul>{others}</ul>
 </article>
</div></section>''' + cta_block()
        page(fn, f'{t} | Hettich Sicherheitsdienst', teaser, body)


def legal():
    imp = f'''<div class="legal">
 <div class="box" data-up><h2><span>01</span>Angaben gemäß § 5 DDG</h2><p>Hettich Sicherheitsdienst<br>Inhaber: Jan Hettich<br>Kapellenstraße 1<br>89269 Vöhringen<br>Deutschland</p></div>
 <div class="box" data-up><h2><span>02</span>Kontakt</h2><p>Telefon: <a href="{TEL_HREF}">{TEL}</a><br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p></div>
 <div class="box" data-up><h2><span>03</span>Umsatzsteuer</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: DE367352444</p></div>
 <div class="box" data-up><h2><span>04</span>Erlaubnis &amp; Aufsicht</h2><p>Bewachungsgewerbe gemäß § 34a GewO mit Zulassung (uneingeschränkte Bewachungserlaubnis).<br>Registriert im Bewacherregister – ID 18865.<br>Zuständige Aufsichtsbehörde: Landratsamt Neu-Ulm.</p></div>
 <div class="box" data-up><h2><span>05</span>Haftung</h2><p>Die Inhalte dieser Website wurden mit größter Sorgfalt erstellt. Für Richtigkeit, Vollständigkeit und Aktualität übernehmen wir keine Gewähr. Für Inhalte verlinkter externer Seiten ist stets der jeweilige Anbieter verantwortlich.</p></div>
 <div class="box" data-up><h2><span>06</span>Verbraucherstreitbeilegung</h2><p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p></div>
</div>'''
    page('impressum.html', 'Impressum | Hettich Sicherheitsdienst', 'Impressum des Hettich Sicherheitsdienstes, Vöhringen.',
         phero('Rechtliches', 'Impressum', 'Anbieterkennzeichnung des Hettich Sicherheitsdienstes.', crumb='Impressum') + f'<section class="sec" style="padding-top:20px"><div class="wrap">{imp}</div></section>')
    ds = f'''<div class="legal">
 <div class="box" data-up><h2><span>01</span>Verantwortliche Stelle</h2><p>Hettich Sicherheitsdienst · Inhaber Jan Hettich · Kapellenstraße 1, 89269 Vöhringen<br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a> · Telefon: {TEL}</p></div>
 <div class="box" data-up><h2><span>02</span>Hosting</h2><p>Diese Website wird als statische Seite über GitHub Pages (GitHub Inc., San Francisco, USA) ausgeliefert. Beim Abruf werden technische Zugriffsdaten verarbeitet (IP-Adresse, Zeitpunkt, abgerufene Datei, Browsertyp). Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO – unser berechtigtes Interesse an einer sicheren Bereitstellung. Für die Übermittlung in die USA gelten die EU-Standardvertragsklauseln.</p></div>
 <div class="box" data-up><h2><span>03</span>Keine Analyse, keine Cookies</h2><p>Diese Website setzt keine Analyse- oder Marketing-Werkzeuge ein, bildet keine Profile und bindet keine Dienste Dritter ein – auch keine externen Schriftarten. Es werden keine Cookies gesetzt. Lediglich eine technisch notwendige Kennung im Sitzungsspeicher Ihres Browsers merkt sich, dass die Startanimation bereits gezeigt wurde; sie wird beim Schließen des Browsers gelöscht (§ 25 Abs. 2 Nr. 2 TDDDG).</p></div>
 <div class="box" data-up><h2><span>04</span>Kontaktaufnahme</h2><p>Bei Kontakt per E-Mail, Telefon oder über das Kontaktformular (das Ihr E-Mail-Programm öffnet) verarbeiten wir Ihre Angaben ausschließlich zur Bearbeitung der Anfrage (Art. 6 Abs. 1 lit. b DSGVO). Die Daten werden gelöscht, sobald die Anfrage abgeschlossen ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p></div>
 <div class="box" data-up><h2><span>05</span>Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21 DSGVO) – formlos an die oben genannte Adresse.</p><p>Beschwerderecht: Bayerisches Landesamt für Datenschutzaufsicht (BayLDA), Promenade 18, 91522 Ansbach.</p></div>
</div>'''
    page('datenschutz.html', 'Datenschutz | Hettich Sicherheitsdienst', 'Datenschutzerklärung des Hettich Sicherheitsdienstes.',
         phero('Rechtliches', 'Datenschutz', 'Stand: 2. Oktober 2026', crumb='Datenschutz') + f'<section class="sec" style="padding-top:20px"><div class="wrap">{ds}</div></section>')


if __name__ == '__main__':
    index(); dienstleistungen(); vision(); kontakt(); blog(); legal()
