# -*- coding: utf-8 -*-
"""Generate the static CEEG site into OUT from content.py."""
import os, sys, html, datetime, shutil
sys.path.insert(0, os.path.dirname(__file__))
from content import *

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date(2026, 11, 25)
SRC = "https://ceegim.com/wp-content/uploads/"
MANIFEST = {}

MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]

def img(path):
    """Register an upload and return its site-root-relative local path."""
    if not path: return ""
    if path.startswith("http") or path.startswith("assets/"): return path
    ym = "-".join(path.split("/")[:2])
    local = "assets/img/" + ym + "-" + path.split("/")[-1]
    MANIFEST[SRC + path] = local
    return local

def esc(s): return html.escape(s, quote=True)

def fdate(d):
    d = datetime.date.fromisoformat(d[:10])
    return f"{d.day} {MOIS[d.month-1]} {d.year}"

def ftime(t): return t[11:16].replace(":", " h ") if t[11:16] != "00:00" else ""

NAV = [("Accueil",""),("Nouvelles","nouvelles/"),("À propos","a-propos/"),("Programmes","programmes/"),
       ("Événements","evenements/"),("Partenaires","partenaires/"),("Nous joindre","nous-joindre/")]

ICONS = {
 "Facebook": '<path d="M14 8h3V4h-3c-2.8 0-4 1.7-4 4.2V10H7v4h3v8h4v-8h3l1-4h-4V8.5c0-.4.2-.5.5-.5z"/>',
 "Instagram": '<path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm5.2-8.4a1.2 1.2 0 1 1-2.4 0 1.2 1.2 0 0 1 2.4 0zM12 3c-2.4 0-2.7 0-3.7.1C5.4 3.2 3.2 5.4 3.1 8.3 3 9.3 3 9.6 3 12s0 2.7.1 3.7c.1 2.9 2.3 5.1 5.2 5.2 1 .1 1.3.1 3.7.1s2.7 0 3.7-.1c2.9-.1 5.1-2.3 5.2-5.2.1-1 .1-1.3.1-3.7s0-2.7-.1-3.7c-.1-2.9-2.3-5.1-5.2-5.2C14.7 3 14.4 3 12 3zm0 1.8c2.4 0 2.6 0 3.6.1 2 .1 3.4 1.5 3.5 3.5.1.9.1 1.2.1 3.6s0 2.7-.1 3.6c-.1 2-1.5 3.4-3.5 3.5-.9.1-1.2.1-3.6.1s-2.7 0-3.6-.1c-2-.1-3.4-1.5-3.5-3.5-.1-.9-.1-1.2-.1-3.6s0-2.7.1-3.6c.1-2 1.5-3.4 3.5-3.5.9-.1 1.2-.1 3.6-.1z"/>',
 "LinkedIn": '<path d="M5 3a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM3 9h4v12H3zm6 0h3.8v1.7c.6-1 1.9-2 3.9-2 4 0 4.3 2.6 4.3 6V21h-4v-5.6c0-1.4 0-3.1-1.9-3.1s-2.2 1.5-2.2 3V21H9z"/>',
}

def page(path, title, body, desc="", active="", og=""):
    depth = path.count("/")
    r = "../" * depth  # relative root
    nav = []
    for label, href in NAV:
        cls = ' class="active"' if href == active else ""
        if href == "programmes/":
            sub = "".join(f'<li><a href="{r}programmes/{p["slug"]}/">{esc(p["title"])}</a></li>' for p in PROGRAMMES)
            nav.append(f'<li class="has-sub"><a href="{r}{href}"{cls}>{label}</a><ul class="sub">{sub}</ul></li>')
        else:
            nav.append(f'<li><a href="{r}{href}"{cls}>{label}</a></li>')
    icons = "".join(f'<a href="{u}" rel="noopener" aria-label="{n}"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true">{ICONS[n]}</svg></a>' for n, u in SOCIAL.items())
    social = "".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOCIAL.items())
    full_title = f"{title} – Club Entrepreneur Étudiant Gaspé" if title != "Accueil" else "Club Entrepreneur Étudiant Gaspé"
    doc = f"""<!DOCTYPE html>
<html lang="fr-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc or FOOTER_TEXT)}">
<meta property="og:title" content="{esc(full_title)}">
{f'<meta property="og:image" content="{r}{og}">' if og else ''}
<link rel="icon" href="{r}favicon.ico" sizes="any"><link rel="icon" href="{r}favicon-32.png" type="image/png" sizes="32x32"><link rel="icon" href="{r}favicon-192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="{r}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@800&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/site.css?v=20261121b">
</head>
<body>
<div class="topbar"><div class="wrap tb">
 <details class="network"><summary>Réseau CEEGIM</summary><ul>{''.join(f'<li><a href="{u if u.startswith("http") else r}">{esc(n)}</a></li>' for n, u in NETWORK)}</ul></details>
 <p class="tb-social">{icons}</p>
</div></div>
<header class="site-header">
 <div class="wrap bar">
  <a class="brand" href="{r}"><img src="{r}{img(LOGO)}" alt="Club Entrepreneur Étudiant Gaspé" width="190" height="107"></a>
  <button class="menu-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav id="nav"><ul>{''.join(nav)}</ul></nav>
 </div>
</header>
<main>
{body.replace("url('assets/", f"url('{r}assets/").replace('src="assets/', f'src="{r}assets/').replace('href="assets/', f'href="{r}assets/').replace('href="/', f'href="{r}')}
</main>
<footer class="site-footer">
 <div class="wrap cols">
  <div><img class="flogo" src="{r}{img(LOGO)}" alt="" width="160" height="90"><p>{FOOTER_TEXT}</p></div>
  <div><h3>Nous joindre</h3><p>{ADDRESS}<br><a href="tel:+15142223064">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  <div><h3>@ceegim</h3><p class="social">{social}</p></div>
 </div>
 <div class="wrap legal"><span>© {TODAY.year} Club Entrepreneur Étudiant Gaspé</span><a href="{r}privacy-policy/">Politique de confidentialité</a></div>
</footer>
<script src="{r}assets/site.js?v=20261121b"></script>
</body>
</html>
"""
    dest = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f: f.write(doc)

def redirect(path, target_from_root):
    depth = path.count("/")
    t = "../" * depth + target_from_root
    dest = os.path.join(OUT, path, "index.html"); os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html lang="fr-CA"><head><meta charset="utf-8"><title>Redirection</title>'
                f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={t}">'
                f'<link rel="canonical" href="{t}"></head><body><p><a href="{t}">Continuer</a></p></body></html>')

def hero(title, sub="", image=""):
    bg = f' style="--hero:url(\'{img(image)}\')"' if image else ""
    cls = "page-hero has-img" if image else "page-hero"
    return f'<section class="{cls}"{bg}><div class="wrap"><p class="ph-kicker">Club Entrepreneur Étudiant Gaspé</p><h1>{esc(title)}</h1>{f"<p>{sub}</p>" if sub else ""}</div></section>'

# Banner photos for programme pages (photos, not posters, so the heading stays readable)
PROG_BANNER = {"pex":"2026/08/20241121_111507.jpg","festif":"2024/04/20231104_205707-min-scaled.jpg",
 "cantine":"2024/04/20231103_150215-min-scaled.jpg","boutique":"2024/04/20231103_145936-min-scaled.jpg",
 "pef":"2026/08/20241119_134500.jpg","pdp":"2024/04/20231104_081107-min-scaled.jpg",
 "simulations":"2024/04/20231104_183218-min-scaled.jpg","clq":"assets/img/clq-2026-acee.jpg"}  # CLQ 2026, official ACEE backdrop

POSTS_BY = {p[0]: p for p in POSTS}

def post_card(slug):
    s, d, t, feat, body, extra = POSTS_BY[slug]
    im = f'<img src="{img(feat)}" alt="" loading="lazy">' if feat else '<div class="ph"></div>'
    return (f'<a class="card" href="/nouvelles/#{s}">{im}<div class="card-body"><time>{fdate(d)}</time>'
            f'<h3>{esc(t)}</h3></div></a>')

def ev_when(e):
    s, start, end, allday = e[0], e[1], e[2], e[3]
    if allday:
        return fdate(start) if start[:10] == end[:10] else f"{fdate(start)} au {fdate(end)}"
    t = ftime(start)
    return f"{fdate(start)}{' à ' + t if t else ''}"

def ev_row(e, full=True):
    s, start, end, allday, title, venue, cost, url, image, desc = e
    meta = " · ".join(x for x in [ev_when(e), venue, cost] if x)
    link = f'<p><a class="btn small" href="{url}" rel="noopener">{"Billets" if "zeffy" in url else "Détails"}</a></p>' if url and full else ""
    anchor = s + "-" + start[:10]
    return (f'<article class="event" id="{anchor}">'
            + (f'<a href="{img(image)}" target="_blank" rel="noopener" aria-label="Voir l’affiche : {esc(title)}"><img src="{img(image)}" alt="" loading="lazy"></a>' if image else '<div></div>') +
            f'<div><h3>{esc(title)}</h3><p class="meta">{esc(meta)}</p>{desc if full else ""}{link}</div></article>')

def gallery(items):
    if not items: return ""
    return '<div class="gallery">' + "".join(f'<a href="{img(i)}"><img src="{img(i)}" alt="" loading="lazy"></a>' for i in items) + "</div>"

def logos(items):
    return '<div class="logos">' + "".join(f'<img src="{img(i)}" alt="Partenaire" loading="lazy">' for i in items) + "</div>"

# ------------------------------------------------------------------ build
def build():
    if os.path.isdir(OUT):
        for name in os.listdir(OUT):
            if name in (".git", "assets", ".github", "README.md", "CNAME", ".nojekyll", "favicon.ico", "favicon-32.png", "favicon-192.png", "apple-touch-icon.png", "tools"): continue
            p = os.path.join(OUT, name)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

    upcoming = sorted([e for e in EVENTS if e[2][:10] >= TODAY.isoformat()], key=lambda e: e[1])
    past = sorted([e for e in EVENTS if e[2][:10] < TODAY.isoformat()], key=lambda e: e[1], reverse=True)

    # --- accueil
    nxt = upcoming[0] if upcoming else None
    nxt_html = ""
    if nxt:
        nxt_html = f'<section class="next"><div class="wrap"><h2>Prochain événement</h2>{ev_row(nxt)}</div></section>'
    progs = "".join(f'<a class="card" href="/programmes/{p["slug"]}/"><img src="{img(p["card"])}" alt="" loading="lazy"><div class="card-body"><h3>{esc(p["title"])}</h3><p>{PROGRAMME_BLURB[p["slug"]]}</p></div></a>' for p in PROGRAMMES)
    body = f'''<section class="home-hero"><div class="hero-box">
 <svg class="hero-art" viewBox="0 0 1392 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <polygon fill="#fff" points="128,27 345,-6 541,300 305,300"/>
  <polygon fill="#002c88" points="95,207 212,151 306,300 160,300"/>
  <g stroke-linecap="round" stroke-width="50" fill="none"><line x1="1208" y1="62" x2="1000" y2="330" stroke="#fff"/><line x1="1268" y1="82" x2="1080" y2="330" stroke="#002c88"/><line x1="1282" y1="150" x2="1130" y2="340" stroke="#fff"/></g>
 </svg>
 <h1>Club<br>Entrepreneur<br>Étudiant<span>Gaspé</span></h1>
 <div class="acee"><p><span>Fier membre du réseau de</span> <br>l’Association des clubs <br>d’entrepreneurs étudiants <br>du Québec</p><img src="assets/img/acee-badge.png" alt="ACEE" width="96" height="96"></div>
 <img class="hero-photo" src="assets/img/hero-etudiants.jpg" alt="Délégation du Club Entrepreneur Étudiant Gaspé au colloque de l’ACEE 2026" width="1367" height="911">
</div></section>
<div class="tagline"><div class="wrap">Nous entreprenons pour le futur de la Gaspésie !</div></div>
{nxt_html}
<section><div class="wrap grid3">
 <div><h2>Qui sommes-nous ?</h2>{"".join(f"<p>{x}</p>" for x in HOME_WHO)}</div>
 <div class="stack">{"".join(f'<img src="{img(i)}" alt="" loading="lazy">' for i in HOME_PHOTOS[:2])}</div>
 <div><h2>Qu’est-ce qu’on fait ?</h2>{"".join(f"<p>{x}</p>" for x in HOME_WHAT)}</div>
</div></section>
<section class="alt"><div class="wrap"><h2>Notre impact</h2><p class="lead">{HOME_IMPACT}</p><div class="cards">{progs}</div></div></section>
<section><div class="wrap"><h2>Nouvelles</h2><p class="lead">Le Club Entrepreneur Étudiant de Gaspé vous invite à découvrir ses dernières actualités.</p>
<div class="cards">{"".join(post_card(p[0]) for p in POSTS[:3])}</div><p><a class="btn" href="/nouvelles/">Toutes les nouvelles</a></p></div></section>'''
    page("", "Accueil", body, og="assets/img/hero-etudiants.jpg")

    # --- à propos
    mem = "".join(f'<figure class="person"><img src="{img(i)}" alt="{esc(n)}" loading="lazy"><figcaption>{esc(n)}</figcaption></figure>' for n, i in MEMBERS)
    alu = "".join(f'<figure class="person"><img src="{img(i)}" alt="{esc(n)}" loading="lazy"><figcaption>{esc(n)}{f"<small>{esc(t)}</small>" if t else ""}</figcaption></figure>' for n, i, t in ALUMNI)
    body = hero("À propos", "Un club-école opéré par ses étudiants, au service de l’entrepreneuriat gaspésien.", ABOUT_IMGS[0]) + f'''
<section><div class="wrap grid2"><div><h2>Notre mission</h2><p class="lead">{MISSION}</p><h2>Notre vision</h2><p class="lead">{VISION}</p></div>
<div><img class="rounded" src="{img(ABOUT_IMGS[1])}" alt="" loading="lazy"></div></div></section>
<section class="alt"><div class="wrap"><h2>Membres actuels</h2><div class="people">{mem}</div></div></section>
<section><div class="wrap"><h2>Anciens membres</h2><div class="people">{alu}</div></div></section>'''
    page("a-propos/", "À propos", body, desc=MISSION, active="a-propos/", og=img(ABOUT_IMGS[0]))

    # --- programmes
    cards = "".join(f'<a class="card" href="/programmes/{p["slug"]}/"><img src="{img(p["card"])}" alt="" loading="lazy"><div class="card-body"><h3>{esc(p["title"])}</h3><p>{PROGRAMME_BLURB[p["slug"]]}</p></div></a>' for p in PROGRAMMES)
    body = hero("Programmes", PROGRAMMES_INTRO, "2024/04/20231103_153043-min-scaled.jpg") + f'<section><div class="wrap"><h2>Découvrez-les!</h2><div class="cards">{cards}</div></div></section>'
    page("programmes/", "Programmes", body, desc=PROGRAMMES_INTRO, active="programmes/")

    ev_by = {}
    for e in EVENTS: ev_by.setdefault(e[0], []).append(e)
    for p in PROGRAMMES:
        parts = [hero(p["title"], p["intro"], PROG_BANNER.get(p["slug"], p["card"]))]
        parts.append(f'<section><div class="wrap narrow"><h2>{p["services_h"]}</h2>{"".join(f"<p>{s}</p>" for s in p["services"])}</div></section>')
        if p["gallery"]:
            parts.append(f'<section class="alt"><div class="wrap"><h2>Revivez ces moments avec nous!</h2>{gallery(p["gallery"])}</div></section>')
        if p["posts"]:
            parts.append(f'<section><div class="wrap"><h2>Nouvelles du programme</h2><div class="cards">{"".join(post_card(s) for s in p["posts"])}</div></div></section>')
        evs = sorted([e for s in p["events"] for e in ev_by.get(s, [])], key=lambda e: e[1], reverse=True)
        if evs:
            parts.append(f'<section class="alt"><div class="wrap"><h2>Événements du programme</h2><div class="events compact">{"".join(ev_row(e, full=False) for e in evs)}</div><p><a class="btn" href="/evenements/">Tous les événements</a></p></div></section>')
        parts.append(f'<section><div class="wrap"><h2>Partenaires du programme</h2>{logos(p["partners"])}</div></section>')
        page(f'programmes/{p["slug"]}/', p["title"], "".join(parts), desc=p["intro"][:160], active="programmes/", og=img(p["card"]))

    # --- nouvelles
    arts = []
    for s, d, t, feat, body_html, extra in POSTS:
        im = f'<img class="feat" src="{img(feat)}" alt="" loading="lazy">' if feat else ""
        arts.append(f'<article class="post" id="{s}">{im}<div><time>{fdate(d)}</time><h2>{esc(t)}</h2>{body_html}{gallery(extra)}</div></article>')
    body = hero("Nouvelles", "Les actualités du Club, de 2022 à aujourd’hui. Pour les nouvelles les plus récentes, suivez-nous sur Facebook et Instagram (@ceegim).", "2024/04/20231103_152321-min-scaled.jpg") + f'<section><div class="wrap narrow posts">{"".join(arts)}</div></section>'
    page("nouvelles/", "Nouvelles", body, active="nouvelles/")

    # --- événements
    up = "".join(ev_row(e) for e in upcoming) or "<p>Aucun événement à venir pour le moment. Suivez-nous sur Facebook (@ceegim).</p>"
    years = {}
    for e in past: years.setdefault(e[1][:4], []).append(e)
    pastb = "".join(f'<h3 class="year">{y}</h3><div class="events">{"".join(ev_row(e) for e in es)}</div>' for y, es in sorted(years.items(), reverse=True))
    body = hero("Événements", "Partys, ateliers, colloques et activités de financement organisés par le Club.", "assets/img/clq-2026-gala.jpg") + f'''
<section><div class="wrap"><h2>À venir</h2><div class="events">{up}</div></div></section>
<section class="alt"><div class="wrap"><h2>Archives</h2>{pastb}</div></section>'''
    page("evenements/", "Événements", body, active="evenements/")

    # --- partenaires
    groups = "".join(f'<h2>{g}</h2>{logos(items)}' for g, items in PARTNERS)
    body = hero("Partenaires", "Ensemble, nous entreprenons!", "2024/04/20231104_175832-min-scaled.jpg") + f'<section><div class="wrap"><p class="lead">{PARTNERS_INTRO}</p>{groups}</div></section>'
    page("partenaires/", "Partenaires", body, desc=PARTNERS_INTRO, active="partenaires/")

    # --- nous joindre
    grp = "".join(f'<div class="box"><h3>{g}</h3>{"".join(f"<p><a href=\"mailto:{m}\">{m}</a></p>" for m in ms)}</div>' for g, ms in CONTACT_GROUPS)
    icons = "".join(f'<a href="{u}" rel="noopener" aria-label="{n}"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true">{ICONS[n]}</svg></a>' for n, u in SOCIAL.items())
    social = "".join(f'<a class="btn ghost" href="{u}" rel="noopener">{n}</a> ' for n, u in SOCIAL.items())
    body = hero("Nous joindre", "", "2024/04/20231103_150914-min-scaled.jpg") + f'''<section><div class="wrap"><p class="lead">{CONTACT_INTRO}</p>
<div class="boxes"><div class="box"><h3>Locaux</h3><p>{CONTACT_LOCAL}</p></div>
<div class="box"><h3>Coordonnées</h3><p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p><p><a href="tel:+15142223064">{CONTACT_PHONE}</a></p></div>
<div class="box"><h3>Social</h3><p>@ceegim sur toutes les plateformes</p><p>{social}</p></div></div>
<h2>L’équipe</h2><div class="boxes">{grp}</div></div></section>'''
    page("nous-joindre/", "Nous joindre", body, desc=CONTACT_INTRO, active="nous-joindre/")

    # --- gala, beach party, privacy
    body = hero("Gala du mérite éducatif 2025", "", "2024/04/20231104_205653-min-scaled.jpg") + f'<section><div class="wrap narrow center"><img class="gala-logo" src="{img(GALA_LOGO)}" alt="Gala des finissants 2025"><p class="lead">Le Club Entrepreneur Étudiant Gaspé souligne la réussite des finissants. Voir aussi <a href="/nouvelles/#gala-finissant-2024">le Gala finissant 2024</a>.</p></div></section>'
    page("gala/", "Gala des finissants 2025", body)
    body = hero("Beach Party 2024 – Fin de session", "", "2024/04/20231104_205646-min-scaled.jpg") + f'<section><div class="wrap center"><img class="rounded" src="{img(BEACH_PARTY_BANNER)}" alt="Beach Party 2024" loading="lazy"><p><a class="btn" href="/evenements/#16523-2024-05-04">Voir l’événement</a></p></div></section>'
    page("beach-party-2023-fin-de-session/", "Beach Party 2024 – Fin de session", body)
    body = hero("Politique de confidentialité", "", "2024/04/20231103_150524-min-scaled.jpg") + f'''<section><div class="wrap narrow">
<p>Ce site est un site statique hébergé sur GitHub Pages. Il ne comporte ni comptes utilisateurs, ni formulaires, ni commentaires, et le Club Entrepreneur Étudiant Gaspé n’y recueille aucune donnée personnelle.</p>
<h2>Contenu externe</h2><p>Les pages chargent les polices Google Fonts. Les liens vers Facebook, Instagram, LinkedIn ou Zeffy vous amènent sur ces plateformes, qui appliquent leurs propres politiques de confidentialité.</p>
<h2>Hébergement</h2><p>GitHub, l’hébergeur, peut conserver des journaux techniques (comme l’adresse IP) pour des raisons de sécurité, selon sa propre politique.</p>
<h2>Nous joindre</h2><p>Pour toute question : <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p></div></section>'''
    page("privacy-policy/", "Politique de confidentialité", body)

    # --- 404
    body = hero("Page introuvable", "La page que vous cherchez a été déplacée lors de la migration du site.", "2024/04/20231103_150524-min-scaled.jpg") + '<section><div class="wrap center"><p><a class="btn" href="/">Accueil</a> <a class="btn ghost" href="/nouvelles/">Nouvelles</a> <a class="btn ghost" href="/evenements/">Événements</a></p></div></section>'
    page("404/", "Page introuvable", body)
    os.replace(os.path.join(OUT, "404", "index.html"), os.path.join(OUT, "404.html")); os.rmdir(os.path.join(OUT, "404"))
    # 404.html lives at root: fix relative prefix (it was built one level deep). Use absolute-root-safe rewrite later.

    # --- redirects for old WordPress URLs
    for s, *_ in POSTS: redirect(f"{s}/", f"nouvelles/#{s}")
    redirect("a-determiner/", "nouvelles/")
    seen = set()
    for e in EVENTS:
        if e[0] in seen: continue
        seen.add(e[0]); redirect(f"event/{e[0]}/", f"evenements/#{e[0]}-{e[1][:10]}")
    redirect("events/", "evenements/")
    redirect("boutique/", "")

    # --- manifest for the image-fetch workflow
    os.makedirs(os.path.join(OUT, "assets", "img"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "img", "manifest.tsv"), "w", encoding="utf-8") as f:
        for url, local in sorted(MANIFEST.items(), key=lambda x: x[1]):
            f.write(f"{url}\t{local}\n")
    print(f"pages built; {len(MANIFEST)} images in manifest; {len(upcoming)} upcoming, {len(past)} past events")

build()
