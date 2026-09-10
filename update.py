import urllib.request
import json
import html
import os
import shutil
import re
from datetime import datetime, timezone


# =========================================================
# LIENS ET PARAMÈTRES
# =========================================================

DISCORD_INVITE = "ujHH2bNzhn"
YOUTUBE_URL = "https://www.youtube.com/@Legodingo13"
SOCIALCOUNTS_URL = (
    "https://socialcounts.org/"
    "youtube-live-subscriber-count/"
    "UC_1T2zJa_uOU2xNeQHdPutQ"
)
FOE_URL = "https://fr0.forgeofempires.com/page/"
GUNS_URL = "https://guns.lol/legodingo13"
SITE_BASE = "https://legodingo13.github.io/serveur-discord-legodingo13/"

# Nous ajouterons la vraie balise Google Search Console plus tard.
GOOGLE_META = """<!-- Google Search Console -->"""


# =========================================================
# FONCTIONS DE DONNÉES
# =========================================================

def format_number(value):
    try:
        return f"{int(value):,}".replace(",", " ")
    except (TypeError, ValueError):
        return str(value)


def read_previous_youtube_count():
    if not os.path.exists("last-update.txt"):
        return None

    try:
        with open("last-update.txt", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Abonnés YouTube :"):
                    value = line.split(":", 1)[1].strip()
                    if value not in ("", "indisponible", "inconnu"):
                        return value
    except Exception:
        pass

    return None


def get_youtube_subscribers():
    previous_count = read_previous_youtube_count()

    try:
        request = urllib.request.Request(
            SOCIALCOUNTS_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/140.0 Safari/537.36"
                ),
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,*/*;q=0.8"
                ),
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            },
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            page = response.read().decode("utf-8", errors="ignore")

        patterns = [
            r"Legodingo13(?:&#x27;|['’])s YouTube presence with\s*([\d,\s]+)\s*subscribers",
            r"Legodingo13.*?YouTube presence with\s*([\d,\s]+)\s*subscribers",
            r"with\s*([\d,\s]+)\s*subscribers\s+and\s+[\d,\s]+\s+videos",
        ]

        for pattern in patterns:
            match = re.search(pattern, page, flags=re.IGNORECASE | re.DOTALL)
            if match:
                number = re.sub(r"[^\d]", "", match.group(1))
                if number:
                    return format_number(int(number))

        json_patterns = [
            r'"subscriberCount"\s*:\s*"?(\d+)"?',
            r'"subscribers"\s*:\s*"?(\d+)"?',
            r'"subscriber_count"\s*:\s*"?(\d+)"?',
        ]

        for pattern in json_patterns:
            match = re.search(pattern, page, flags=re.IGNORECASE)
            if match:
                return format_number(int(match.group(1)))

        print("SocialCounts a répondu, mais le nombre d'abonnés n'a pas été trouvé.")

    except Exception as error:
        print("Impossible de lire SocialCounts :", error)

    if previous_count:
        return previous_count

    return "indisponible"


# =========================================================
# STATISTIQUES DISCORD
# =========================================================

discord_url = (
    "https://discord.com/api/v10/invites/"
    + DISCORD_INVITE
    + "?with_counts=true"
)

discord_request = urllib.request.Request(
    discord_url,
    headers={"User-Agent": "Mozilla/5.0"},
)

with urllib.request.urlopen(discord_request, timeout=30) as response:
    discord_data = json.loads(response.read().decode("utf-8"))

guild = discord_data.get("guild", {})
guild_name = html.escape(guild.get("name", "Legodingo13 - Serv FOE FR"))
member_count = format_number(discord_data.get("approximate_member_count", "inconnu"))
online_count = format_number(discord_data.get("approximate_presence_count", "inconnu"))


# =========================================================
# STATISTIQUES YOUTUBE
# =========================================================

youtube_subscribers = get_youtube_subscribers()
youtube_display = (
    "Compteur temporairement indisponible"
    if youtube_subscribers == "indisponible"
    else f"{youtube_subscribers} abonnés"
)


# =========================================================
# DATE
# =========================================================

updated = datetime.now(timezone.utc).strftime("%d/%m/%Y à %H:%M UTC")


# =========================================================
# STYLE COMMUN À TOUT LE SITE
# =========================================================

CSS = r"""
* { box-sizing: border-box; }
html { min-height: 100%; }
html, body { cursor: url("cursor_default.cur"), auto; }
body * { cursor: inherit; }
a, a *, button, button * { cursor: url("cursor_hover.cur"), pointer !important; }

body {
    margin: 0;
    min-height: 100vh;
    font-family: Arial, Helvetica, sans-serif;
    color: white;
    background:
        linear-gradient(rgba(6,10,18,.43), rgba(6,10,18,.76)),
        url("fond.png") center / cover no-repeat fixed;
    padding: 40px 20px;
}

.page { width: 100%; max-width: 1080px; margin: 0 auto; }
.card {
    position: relative;
    width: 100%;
    background: linear-gradient(145deg, rgba(17,21,31,.91), rgba(31,20,18,.87));
    border: 1px solid rgba(255,210,130,.23);
    border-radius: 28px;
    overflow: hidden;
    box-shadow: 0 30px 90px rgba(0,0,0,.58);
    backdrop-filter: blur(8px);
}
.card::before {
    content: "";
    position: absolute;
    top: 0; left: 10%; right: 10%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,177,73,.9), transparent);
}

.site-head { text-align: center; padding: 30px 32px 16px; }
.logo { width: 165px; max-width: 72%; height: auto; display: block; margin: 0 auto 14px; filter: drop-shadow(0 8px 15px rgba(0,0,0,.42)); }
.badge {
    display: inline-block;
    padding: 8px 17px;
    border-radius: 999px;
    background: rgba(202,112,33,.20);
    border: 1px solid rgba(255,183,82,.40);
    color: #ffd69a;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
}

.nav {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 18px;
}
.nav a {
    text-decoration: none;
    color: #eceff5;
    padding: 10px 16px;
    border-radius: 11px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.055);
    font-weight: 700;
    font-size: 14px;
    transition: .2s ease;
}
.nav a:hover { transform: translateY(-2px); background: rgba(255,255,255,.10); border-color: rgba(255,210,130,.35); }
.nav a.active { color: #1d160f; background: linear-gradient(135deg,#ffd493,#e8a34b); border-color: transparent; }

.content { padding: 18px 38px 38px; text-align: center; }
h1 { margin: 8px 0 0; font-size: clamp(34px,5vw,56px); line-height: 1.05; text-shadow: 0 4px 20px rgba(0,0,0,.55); }
h2 { margin: 10px 0 16px; }
.gold { color: #ffd493; }
.lead { max-width: 820px; margin: 18px auto 28px; color: #e7e3df; font-size: 16px; line-height: 1.7; }

.stats { display: grid; grid-template-columns: repeat(2,1fr); gap: 24px; margin: 26px 0; }
.stat {
    padding: 30px 20px;
    border-radius: 20px;
    background: linear-gradient(145deg,rgba(255,255,255,.075),rgba(255,255,255,.035));
    border: 1px solid rgba(255,255,255,.09);
}
.number { display: block; margin-bottom: 9px; font-size: clamp(42px,6vw,62px); line-height: 1; font-weight: 800; }
.label { color: #d4d7de; font-size: 16px; }
.online-dot { display:inline-block; width:10px; height:10px; margin-right:7px; border-radius:50%; background:#3ba55d; box-shadow:0 0 8px rgba(59,165,93,.8); }

.primary-button {
    display: inline-block;
    padding: 15px 27px;
    border-radius: 14px;
    text-decoration: none;
    color: white;
    font-size: 17px;
    font-weight: 700;
    background: linear-gradient(135deg,#5865F2,#7289da);
    box-shadow: 0 12px 30px rgba(88,101,242,.35);
    transition: .2s ease;
}
.primary-button:hover { transform: translateY(-3px); box-shadow:0 17px 35px rgba(88,101,242,.45); }
.gold-button { background: linear-gradient(135deg,#c47a2b,#f0b45c); color:#1b130d; box-shadow:0 12px 30px rgba(196,122,43,.25); }

.grid { display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-top:24px; }
.grid.two { grid-template-columns: repeat(2,1fr); }
.tile {
    min-height: 185px;
    padding: 24px 18px;
    border-radius: 18px;
    text-decoration: none;
    color: white;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.10);
    transition:.2s ease;
}
.tile:hover { transform:translateY(-4px); background:rgba(255,255,255,.09); border-color:rgba(255,210,130,.42); }
.tile-logo { display:block; object-fit:contain; margin:0 auto 12px; filter:drop-shadow(0 5px 10px rgba(0,0,0,.35)); transition:.2s; }
.tile:hover .tile-logo { transform:scale(1.07); }
.youtube-logo { width:92px; height:58px; }
.foe-logo { width:90px; height:70px; }
.guns-logo { width:92px; height:92px; }
.server-logo-small { width:100px; height:auto; }
.tile-title { font-size:19px; font-weight:700; margin-bottom:7px; }
.tile-detail { color:#c4c9d2; font-size:14px; line-height:1.45; }
.tile-count { color:#ffd493; font-size:25px; font-weight:800; margin-bottom:7px; }

.table-frame {
    width: 100%;
    overflow: auto;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 18px;
    padding: 16px;
    margin: 24px auto;
}
.table-image { display:block; max-width:none; width:auto; min-width:100%; height:auto; margin:0 auto; border-radius:8px; }
.notice { max-width:760px; margin:22px auto; padding:18px; border-radius:15px; background:rgba(255,212,147,.08); border:1px solid rgba(255,212,147,.20); color:#e6dccd; line-height:1.6; }

.footer { margin: 0 38px; padding: 23px 0 30px; border-top:1px solid rgba(255,255,255,.08); text-align:center; color:#aeb4bf; font-size:13px; }
.footer small { color:#7f8794; }

@media (max-width:760px) {
    body { padding:18px 10px; background-attachment:scroll; }
    .card { border-radius:20px; }
    .site-head { padding:25px 16px 12px; }
    .logo { width:145px; }
    .nav { gap:7px; }
    .nav a { flex:1 1 calc(50% - 8px); padding:10px 8px; }
    .content { padding:15px 18px 28px; }
    .stats, .grid, .grid.two { grid-template-columns:1fr; gap:15px; }
    .tile { min-height:155px; }
    .footer { margin:0 18px; }
}
"""


# =========================================================
# GÉNÉRATION DES PAGES
# =========================================================

def navigation(active):
    links = [
        ("Accueil", "index.html", "accueil"),
        ("Discord", "discord.html", "discord"),
        ("YouTube", "youtube.html", "youtube"),
        ("Profil Legodingo13", "profil.html", "profil"),
    ]

    parts = []
    for label, href, key in links:
        cls = ' class="active"' if key == active else ""
        parts.append(f'<a href="{href}"{cls}>{label}</a>')
    return "".join(parts)


def shell(filename, active, title, description, body):
    canonical = SITE_BASE + ("" if filename == "index.html" else filename)
    page = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{GOOGLE_META}
<style>{CSS}</style>
</head>
<body>
<main class="page">
<section class="card">
<header class="site-head">
    <img src="logo.png" alt="Logo du serveur Discord Legodingo13" class="logo">
    <div class="badge">COMMUNAUTÉ LEGODINGO13</div>
    <nav class="nav" aria-label="Navigation principale">{navigation(active)}</nav>
</header>
<div class="content">{body}</div>
<footer class="footer">
    Dernière mise à jour automatique : <strong>{updated}</strong><br>
    <small>Site communautaire Legodingo13 • Forge of Empires</small>
</footer>
</section>
</main>
</body>
</html>"""

    with open(os.path.join("_site", filename), "w", encoding="utf-8") as f:
        f.write(page)


os.makedirs("_site", exist_ok=True)


# ACCUEIL
home_body = f"""
<h1>Legodingo13</h1>
<p class="lead">
Bienvenue sur le site de la communauté Legodingo13 autour de Forge of Empires.
Retrouve ici le serveur Discord, la chaîne YouTube, le profil Legodingo13
et le tableau communautaire mis à jour depuis l'application du bot.
</p>
<div class="stats">
    <div class="stat"><span class="number">{member_count}</span><span class="label">membres sur le serveur Discord</span></div>
    <div class="stat"><span class="number">{youtube_subscribers}</span><span class="label">abonnés sur YouTube</span></div>
</div>
<div class="grid two">
    <a class="tile" href="discord.html"><img src="logo.png" class="tile-logo server-logo-small" alt="Discord Legodingo13"><div class="tile-title">Discord</div><div class="tile-detail">Le plus gros serveur communautaire francophone autour de Forge of Empires.</div></a>
    <a class="tile" href="youtube.html"><img src="Youtube.png" class="tile-logo youtube-logo" alt="YouTube"><div class="tile-title">YouTube</div><div class="tile-detail">Retrouver la chaîne YouTube de Legodingo13.</div></a>
    <a class="tile" href="profil.html"><img src="guns.png" class="tile-logo guns-logo" alt="Profil Legodingo13"><div class="tile-title">Profil Legodingo13</div><div class="tile-detail">Les liens officiels et le profil de Legodingo13.</div></a>
    <a class="tile" href="tableau.html"><img src="foe_logo.png" class="tile-logo foe-logo" alt="Tableau Forge of Empires"><div class="tile-title">Tableau communautaire</div><div class="tile-detail">Consulter la dernière version publiée depuis l'application Legodingo13 Bot4.</div></a>
</div>
"""
shell(
    "index.html",
    "accueil",
    "Legodingo13 - Communauté Forge of Empires",
    f"Site de Legodingo13 : serveur Discord Forge of Empires avec {member_count} membres, chaîne YouTube et tableau communautaire.",
    home_body,
)


# DISCORD
discord_body = f"""
<h1>Serveur Discord de Legodingo13</h1>
<h2 class="gold">{guild_name}</h2>
<p class="lead">
Le plus gros serveur communautaire francophone autour de Forge of Empires.
Rejoins la communauté pour bénéficier des meilleures aides et de la meilleure activité
de la communauté francophone de Forge of Empires !
</p>
<div class="stats">
    <div class="stat"><span class="number">{member_count}</span><span class="label">membres sur le serveur</span></div>
    <div class="stat"><span class="number">{online_count}</span><span class="label"><span class="online-dot"></span>membres actuellement en ligne</span></div>
</div>
<p class="lead">Le serveur Discord de Legodingo13 compte actuellement <strong class="gold">{member_count} membres</strong>, dont environ <strong class="gold">{online_count} membres en ligne</strong>.</p>
<a class="primary-button" href="https://discord.gg/{DISCORD_INVITE}" target="_blank" rel="noopener noreferrer">Rejoindre le serveur Discord</a>
<div class="grid">
    <a class="tile" href="{YOUTUBE_URL}" target="_blank" rel="noopener noreferrer"><img src="Youtube.png" class="tile-logo youtube-logo" alt="YouTube"><div class="tile-title">YouTube</div><div class="tile-count">{youtube_display}</div><div class="tile-detail">Chaîne YouTube Legodingo13</div></a>
    <a class="tile" href="{FOE_URL}" target="_blank" rel="noopener noreferrer"><img src="foe_logo.png" class="tile-logo foe-logo" alt="Forge of Empires"><div class="tile-title">Forge of Empires</div><div class="tile-detail">Accéder au site officiel francophone du jeu</div></a>
    <a class="tile" href="{GUNS_URL}" target="_blank" rel="noopener noreferrer"><img src="guns.png" class="tile-logo guns-logo" alt="guns.lol Legodingo13"><div class="tile-title">guns.lol</div><div class="tile-detail">Accéder à la page de Legodingo13</div></a>
</div>
"""
shell(
    "discord.html",
    "discord",
    f"Serveur Discord Legodingo13 - {member_count} membres",
    f"Le serveur Discord de Legodingo13 compte actuellement environ {member_count} membres, dont {online_count} membres en ligne.",
    discord_body,
)


# YOUTUBE
youtube_body = f"""
<img src="Youtube.png" class="tile-logo youtube-logo" alt="Logo YouTube">
<h1>Chaîne YouTube Legodingo13</h1>
<p class="lead">Retrouve la chaîne YouTube officielle de Legodingo13 et les contenus autour de Forge of Empires et de sa communauté.</p>
<div class="stats">
    <div class="stat"><span class="number">{youtube_subscribers}</span><span class="label">abonnés YouTube</span></div>
    <div class="stat"><span class="number">FOE</span><span class="label">contenus Forge of Empires</span></div>
</div>
<a class="primary-button" href="{YOUTUBE_URL}" target="_blank" rel="noopener noreferrer">Ouvrir la chaîne YouTube</a>
"""
shell(
    "youtube.html",
    "youtube",
    f"YouTube Legodingo13 - {youtube_display}",
    f"Chaîne YouTube officielle Legodingo13 avec {youtube_display}.",
    youtube_body,
)


# PROFIL
profil_body = f"""
<img src="guns.png" class="tile-logo guns-logo" alt="Logo profil Legodingo13">
<h1>Profil Legodingo13</h1>
<p class="lead">Retrouve les principaux liens publics associés à Legodingo13 et à sa communauté Forge of Empires.</p>
<div class="grid two">
    <a class="tile" href="{GUNS_URL}" target="_blank" rel="noopener noreferrer"><img src="guns.png" class="tile-logo guns-logo" alt="guns.lol"><div class="tile-title">guns.lol</div><div class="tile-detail">Page de profil Legodingo13</div></a>
    <a class="tile" href="{FOE_URL}" target="_blank" rel="noopener noreferrer"><img src="foe_logo.png" class="tile-logo foe-logo" alt="Forge of Empires"><div class="tile-title">Forge of Empires</div><div class="tile-detail">Site officiel francophone du jeu</div></a>
</div>
"""
shell(
    "profil.html",
    "profil",
    "Profil Legodingo13 - Liens officiels",
    "Profil Legodingo13 : guns.lol, Forge of Empires, Discord et YouTube.",
    profil_body,
)


# TABLEAU
if os.path.exists("tableau.png"):
    tableau_view = """
    <div class="table-frame">
        <img src="tableau.png" class="table-image" alt="Tableau communautaire Forge of Empires de Legodingo13">
    </div>
    <a class="primary-button gold-button" href="tableau.png" target="_blank" rel="noopener noreferrer">Ouvrir le tableau en grand</a>
    """
else:
    tableau_view = """
    <div class="notice">
        Aucun tableau n'a encore été envoyé sur le site. Il apparaîtra ici automatiquement
        après le prochain lancement de l'application Legodingo13 Bot4.
    </div>
    """

tableau_body = f"""
<h1>Tableau communautaire</h1>
<p class="lead">
Cette page affiche la dernière version du tableau Excel publiée depuis l'application
Legodingo13 Bot4. Enregistre le fichier Excel avant d'ouvrir l'application pour publier
les dernières modifications.
</p>
{tableau_view}
"""
shell(
    "tableau.html",
    "",
    "Tableau communautaire Legodingo13 - Forge of Empires",
    "Dernière version du tableau communautaire Forge of Empires publiée par Legodingo13.",
    tableau_body,
)


# =========================================================
# ROBOTS.TXT + SITEMAP.XML
# =========================================================

with open("_site/robots.txt", "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_BASE}sitemap.xml\n")

sitemap_urls = [
    SITE_BASE,
    SITE_BASE + "discord.html",
    SITE_BASE + "youtube.html",
    SITE_BASE + "profil.html",
    SITE_BASE + "tableau.html",
]

sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap += f"  <url><loc>{url}</loc></url>\n"
sitemap += "</urlset>\n"

with open("_site/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)


# =========================================================
# COPIE DES ASSETS
# =========================================================

assets = [
    "fond.png",
    "logo.png",
    "Youtube.png",
    "foe_logo.png",
    "guns.png",
    "cursor_default.cur",
    "cursor_hover.cur",
    "tableau.png",
]

for asset in assets:
    if os.path.exists(asset):
        shutil.copy2(asset, os.path.join("_site", asset))
    elif asset != "tableau.png":
        print(f"ATTENTION : {asset} est introuvable.")


# =========================================================
# FICHIER DE SUIVI
# =========================================================

with open("last-update.txt", "w", encoding="utf-8") as f:
    f.write(f"Dernière mise à jour : {updated}\n")
    f.write(f"Membres Discord : {member_count}\n")
    f.write(f"En ligne Discord : {online_count}\n")
    f.write(f"Abonnés YouTube : {youtube_subscribers}\n")

print(f"Discord : {member_count} membres / {online_count} en ligne")
print(f"YouTube via SocialCounts : {youtube_subscribers} abonnés")
print("Pages générées : accueil, Discord, YouTube, Profil, Tableau")
