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

# Sites tiers Forge of Empires
FOE_WIKI_URL = "https://fr.wiki.forgeofempires.com/index.php?title=Accueil"
FORGEDB_URL = "https://foestats.com/"
FOE_SCOREDB_URL = "https://foe.scoredb.io/Worlds"
FOE_DATA_URL = "https://foe-data.ovh/"
BANANA_DB_URL = "https://foe-buildings-database.streamlit.app/"
FOE_TOOLS_URL = "https://foe.tools/fr/"

# Extensions
FOE_HAMMER_URL = "https://chromewebstore.google.com/detail/forge-hammer/kmicglnhmpaebfcoiojigbnepklclboa?hl=fr"
FOE_HELPER_URL = "https://foe-helper.com/"

# Chaînes YouTube tierces
UBERNERD14_URL = "https://www.youtube.com/@UBERnerd14"
SENSHI_URL = "https://www.youtube.com/@drikanorrin9697"
PIXELPULSE_URL = "https://www.youtube.com/@PixelVibes63"
MOOINGCAT_URL = "https://www.youtube.com/@MooingCatFoE"
GUIGEEKS_URL = "https://www.youtube.com/@GuigeekX"
ZOUMA_URL = "https://www.youtube.com/@PassionFoeforgeofempire"

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
.profile-tableau-logo { width:110px; height:110px; object-fit:contain; }

.section-block { margin-top: 44px; }
.section-block:first-of-type { margin-top: 30px; }
.section-title {
    margin: 0 0 8px;
    font-size: 28px;
    color: #ffffff;
}
.section-subtitle {
    max-width: 820px;
    margin: 0 auto 18px;
    color: #bfc5cf;
    font-size: 14px;
    line-height: 1.55;
}
.third-party-logo {
    width: 96px;
    height: 88px;
    object-fit: contain;
}
.third-party-logo.wide {
    width: 108px;
    height: 82px;
}
.third-party-logo.small {
    width: 82px;
    height: 82px;
}
.external-badge {
    display: inline-block;
    margin-top: 10px;
    padding: 5px 9px;
    border-radius: 999px;
    border: 1px solid rgba(255,212,147,.22);
    background: rgba(255,212,147,.07);
    color: #d9c39f;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .35px;
}
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

/* =========================================================
   LOGO CLIQUABLE + ROI QUI TOMBE
   ========================================================= */

.logo-zone {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 0 14px 0;
}

.logo-trigger {
    display: block;
    flex: 0 0 165px;
    width: 165px;
    max-width: 72%;
    padding: 0;
    margin: 0;
    border: 0;
    background: transparent;
    line-height: 0;
}

.logo-trigger .logo {
    display: block;
    width: 100%;
    max-width: none;
    height: auto;
    margin: 0;
    transition: transform .18s ease, filter .18s ease;
}

.logo-trigger:hover .logo {
    transform: scale(1.045);
    filter:
        drop-shadow(0 8px 15px rgba(0,0,0,.42))
        drop-shadow(0 0 12px rgba(255,184,82,.22));
}

.logo-trigger:active .logo {
    transform: scale(.98);
}

.falling-king {
    position: fixed;
    left: 0;
    top: 0;
    width: clamp(125px, 15vw, 230px);
    height: auto;
    z-index: 99999;
    pointer-events: none;
    user-select: none;
    -webkit-user-drag: none;
    will-change: transform, opacity;
    filter: drop-shadow(0 12px 18px rgba(0,0,0,.38));
}

@media (prefers-reduced-motion: reduce) {
    .falling-king {
        display: none;
    }
}

@media (max-width:760px) {
    body { padding:18px 10px; background-attachment:scroll; }
    .card { border-radius:20px; }
    .site-head { padding:25px 16px 12px; }
    .logo { width:145px; }
    .logo-trigger { flex-basis:145px; width:145px; }
    .nav { gap:7px; }
    .nav a { flex:1 1 calc(50% - 8px); padding:10px 8px; }
    .content { padding:15px 18px 28px; }
    .stats, .grid, .grid.two { grid-template-columns:1fr; gap:15px; }
    .tile { min-height:155px; }
    .footer { margin:0 18px; }
}
"""

SCRIPT = r"""
<script>
(function () {
    const trigger = document.getElementById("logoKingTrigger");

    if (!trigger) return;

    trigger.addEventListener("click", function () {
        if (document.querySelector(".falling-king")) return;

        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

        const king = document.createElement("img");
        king.src = "roi_chute.png";
        king.alt = "";
        king.className = "falling-king";
        king.setAttribute("aria-hidden", "true");
        document.body.appendChild(king);

        const vw = window.innerWidth;
        const vh = window.innerHeight;
        const size = Math.min(230, Math.max(125, vw * 0.15));

        const animation = king.animate(
            [
                {
                    transform: `translate(${-size * 0.85}px, ${-size * 1.15}px) rotate(-28deg)`,
                    opacity: 0,
                    offset: 0
                },
                {
                    transform: `translate(${vw * 0.02}px, ${vh * 0.02}px) rotate(18deg)`,
                    opacity: 1,
                    offset: 0.08
                },
                {
                    transform: `translate(${vw * 0.16}px, ${vh * 0.17}px) rotate(-22deg)`,
                    opacity: 1,
                    offset: 0.20
                },
                {
                    transform: `translate(${vw * 0.25}px, ${vh * 0.31}px) rotate(25deg)`,
                    opacity: 1,
                    offset: 0.34
                },
                {
                    transform: `translate(${vw * 0.43}px, ${vh * 0.43}px) rotate(-20deg)`,
                    opacity: 1,
                    offset: 0.48
                },
                {
                    transform: `translate(${vw * 0.53}px, ${vh * 0.58}px) rotate(21deg)`,
                    opacity: 1,
                    offset: 0.62
                },
                {
                    transform: `translate(${vw * 0.71}px, ${vh * 0.70}px) rotate(-17deg)`,
                    opacity: 1,
                    offset: 0.76
                },
                {
                    transform: `translate(${vw * 0.82}px, ${vh * 0.87}px) rotate(19deg)`,
                    opacity: 1,
                    offset: 0.89
                },
                {
                    transform: `translate(${vw + size * 0.85}px, ${vh + size * 0.65}px) rotate(-12deg)`,
                    opacity: 0,
                    offset: 1
                }
            ],
            {
                duration: 5200,
                easing: "ease-in-out",
                fill: "forwards"
            }
        );

        animation.onfinish = function () {
            king.remove();
        };

        animation.oncancel = function () {
            king.remove();
        };
    });
})();
</script>
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
    <div class="logo-zone">
        <button
            type="button"
            class="logo-trigger"
            id="logoKingTrigger"
            aria-label="Faire tomber le roi Legodingo13"
            title="Clique sur le logo"
        >
            <img src="logo.png" alt="Logo du serveur Discord Legodingo13" class="logo">
        </button>
    </div>
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
{SCRIPT}
</body>
</html>"""

    with open(os.path.join("_site", filename), "w", encoding="utf-8") as f:
        f.write(page)


if os.path.exists("_site"):
    shutil.rmtree("_site")
os.makedirs("_site", exist_ok=True)


# ACCUEIL
home_body = f"""
<h1>Legodingo13</h1>
<p class="lead">
Bienvenue sur le site de la communauté Legodingo13 autour de Forge of Empires.
Retrouve ici mes liens officiels, puis une sélection de sites, extensions et chaînes YouTube tierces utiles à la communauté Forge of Empires.
</p>

<div class="stats">
    <div class="stat"><span class="number">{member_count}</span><span class="label">membres sur le serveur Discord</span></div>
    <div class="stat"><span class="number">{youtube_subscribers}</span><span class="label">abonnés sur YouTube</span></div>
</div>

<section class="section-block">
<h2 class="section-title">Liens Legodingo13</h2>
<p class="section-subtitle">Mes pages, mon serveur et les accès directement liés à la communauté Legodingo13.</p>

<div class="grid">
    <a class="tile" href="discord.html"><img src="logo.png" class="tile-logo server-logo-small" alt="Discord Legodingo13"><div class="tile-title">Discord</div><div class="tile-detail">Le plus gros serveur communautaire francophone autour de Forge of Empires.</div></a>
    <a class="tile" href="youtube.html"><img src="Youtube.png" class="tile-logo youtube-logo" alt="YouTube"><div class="tile-title">YouTube</div><div class="tile-detail">Retrouver la chaîne YouTube de Legodingo13.</div></a>
    <a class="tile" href="{FOE_URL}" target="_blank" rel="noopener noreferrer"><img src="foe_logo.png" class="tile-logo foe-logo" alt="Forge of Empires"><div class="tile-title">Forge of Empires</div><div class="tile-detail">Accéder au site officiel francophone du jeu.</div></a>
    <a class="tile" href="profil.html"><img src="profil_tableau.png" class="tile-logo profile-tableau-logo" alt="Profil Legodingo13 - Tableau Excel des mondes FOE"><div class="tile-title">Profil Legodingo13</div><div class="tile-detail">Tableau Excel des mondes FOE</div></a>
    <a class="tile" href="{GUNS_URL}" target="_blank" rel="noopener noreferrer"><img src="guns.png" class="tile-logo guns-logo" alt="guns.lol Legodingo13"><div class="tile-title">Guns</div><div class="tile-detail">Accéder à la page guns.lol de Legodingo13.</div></a>
</div>
</section>

<section class="section-block">
<h2 class="section-title">Sites tiers</h2>
<p class="section-subtitle">Outils, bases de données et ressources externes consacrés à Forge of Empires.</p>

<div class="grid">
    <a class="tile" href="{FOE_WIKI_URL}" target="_blank" rel="noopener noreferrer">
        <img src="foe_logo.png" class="tile-logo foe-logo" alt="Wiki Forge of Empires">
        <div class="tile-title">Wiki Forge of Empires</div>
        <div class="tile-detail">Wiki francophone consacré à Forge of Empires.</div>
        <div class="external-badge">SITE TIERS</div>
    </a>

    <a class="tile" href="{FORGEDB_URL}" target="_blank" rel="noopener noreferrer">
        <img src="forgedb.png" class="tile-logo third-party-logo" alt="ForgeDB">
        <div class="tile-title">ForgeDB</div>
        <div class="tile-detail">Base de données et statistiques autour de Forge of Empires.</div>
        <div class="external-badge">SITE TIERS</div>
    </a>

    <a class="tile" href="{FOE_SCOREDB_URL}" target="_blank" rel="noopener noreferrer">
        <img src="foe_scoredb.png" class="tile-logo third-party-logo small" alt="FOE ScoreDB">
        <div class="tile-title">FOE ScoreDB</div>
        <div class="tile-detail">Base de données et classements Forge of Empires.</div>
        <div class="external-badge">SITE TIERS</div>
    </a>

    <a class="tile" href="{FOE_DATA_URL}" target="_blank" rel="noopener noreferrer">
        <img src="foe_data.png" class="tile-logo third-party-logo" alt="FOE Data">
        <div class="tile-title">FOE Data</div>
        <div class="tile-detail">Base de données consacrée à Forge of Empires.</div>
        <div class="external-badge">SITE TIERS</div>
    </a>

    <a class="tile" href="{BANANA_DB_URL}" target="_blank" rel="noopener noreferrer">
        <img src="banana_db.png" class="tile-logo third-party-logo" alt="Born To Be A Banana">
        <div class="tile-title">Born To Be A Banana</div>
        <div class="tile-detail">Base de données consacrée aux bâtiments de Forge of Empires.</div>
        <div class="external-badge">SITE TIERS</div>
    </a>

    <a class="tile" href="{FOE_TOOLS_URL}" target="_blank" rel="noopener noreferrer">
        <img src="foe_tools.png" class="tile-logo third-party-logo" alt="FOE Tools">
        <div class="tile-title">FOE Tools</div>
        <div class="tile-detail">Assistant pour calculer les places et investissements des Grands Monuments.</div>
        <div class="external-badge">SITE TIERS</div>
    </a>
</div>
</section>

<section class="section-block">
<h2 class="section-title">Extensions du jeu</h2>
<p class="section-subtitle">Extensions tierces utiles pour accompagner Forge of Empires dans le navigateur.</p>

<div class="grid two">
    <a class="tile" href="{FOE_HAMMER_URL}" target="_blank" rel="noopener noreferrer">
        <img src="foe_hammer.png" class="tile-logo third-party-logo" alt="FOE Hammer">
        <div class="tile-title">FOE Hammer</div>
        <div class="tile-detail">Extension Chrome pour Forge of Empires.</div>
        <div class="external-badge">EXTENSION TIERCE</div>
    </a>

    <a class="tile" href="{FOE_HELPER_URL}" target="_blank" rel="noopener noreferrer">
        <img src="foe_helper.png" class="tile-logo third-party-logo" alt="FOE Helper">
        <div class="tile-title">FOE Helper</div>
        <div class="tile-detail">Extension et assistant communautaire pour Forge of Empires.</div>
        <div class="external-badge">EXTENSION TIERCE</div>
    </a>
</div>
</section>

<section class="section-block">
<h2 class="section-title">Chaînes YouTube tierces</h2>
<p class="section-subtitle">Quelques chaînes YouTube consacrées à Forge of Empires.</p>

<div class="grid">
    <a class="tile" href="{UBERNERD14_URL}" target="_blank" rel="noopener noreferrer">
        <img src="ubernerd14.png" class="tile-logo third-party-logo" alt="UBERnerd14">
        <div class="tile-title">UBERnerd14</div>
        <div class="tile-detail">Le plus gros YouTuber Forge of Empires.</div>
        <div class="external-badge">CHAÎNE TIERCE</div>
    </a>

    <a class="tile" href="{SENSHI_URL}" target="_blank" rel="noopener noreferrer">
        <img src="Youtube.png" class="tile-logo youtube-logo" alt="YouTube Senshi">
        <div class="tile-title">Senshi</div>
        <div class="tile-detail">Chaîne YouTube autour de Forge of Empires.</div>
        <div class="external-badge">CHAÎNE TIERCE</div>
    </a>

    <a class="tile" href="{PIXELPULSE_URL}" target="_blank" rel="noopener noreferrer">
        <img src="Youtube.png" class="tile-logo youtube-logo" alt="YouTube PixelPulse">
        <div class="tile-title">PixelPulse</div>
        <div class="tile-detail">Chaîne YouTube autour de Forge of Empires.</div>
        <div class="external-badge">CHAÎNE TIERCE</div>
    </a>

    <a class="tile" href="{MOOINGCAT_URL}" target="_blank" rel="noopener noreferrer">
        <img src="Youtube.png" class="tile-logo youtube-logo" alt="YouTube MooingCatFOE">
        <div class="tile-title">MooingCatFOE</div>
        <div class="tile-detail">Chaîne YouTube autour de Forge of Empires.</div>
        <div class="external-badge">CHAÎNE TIERCE</div>
    </a>

    <a class="tile" href="{GUIGEEKS_URL}" target="_blank" rel="noopener noreferrer">
        <img src="Youtube.png" class="tile-logo youtube-logo" alt="YouTube Guigeeks">
        <div class="tile-title">Guigeeks</div>
        <div class="tile-detail">Chaîne YouTube autour de Forge of Empires.</div>
        <div class="external-badge">CHAÎNE TIERCE</div>
    </a>

    <a class="tile" href="{ZOUMA_URL}" target="_blank" rel="noopener noreferrer">
        <img src="Youtube.png" class="tile-logo youtube-logo" alt="YouTube Zouma">
        <div class="tile-title">Zouma</div>
        <div class="tile-detail">Chaîne YouTube autour de Forge of Empires.</div>
        <div class="external-badge">CHAÎNE TIERCE</div>
    </a>
</div>
</section>
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
<div class="grid">
    <a class="tile" href="discord.html"><img src="logo.png" class="tile-logo server-logo-small" alt="Discord Legodingo13"><div class="tile-title">Discord</div><div class="tile-detail">Accéder à la page du serveur Discord Legodingo13</div></a>
    <a class="tile" href="{FOE_URL}" target="_blank" rel="noopener noreferrer"><img src="foe_logo.png" class="tile-logo foe-logo" alt="Forge of Empires"><div class="tile-title">Forge of Empires</div><div class="tile-detail">Accéder au site officiel francophone du jeu</div></a>
    <a class="tile" href="{GUNS_URL}" target="_blank" rel="noopener noreferrer"><img src="guns.png" class="tile-logo guns-logo" alt="guns.lol Legodingo13"><div class="tile-title">Guns</div><div class="tile-detail">Accéder à la page guns.lol de Legodingo13</div></a>
</div>
"""
shell(
    "youtube.html",
    "youtube",
    f"YouTube Legodingo13 - {youtube_display}",
    f"Chaîne YouTube officielle Legodingo13 avec {youtube_display}.",
    youtube_body,
)


# PROFIL = TABLEAU EXCEL
if os.path.exists("tableau.png"):
    profil_tableau_view = """
    <div class="table-frame">
        <img src="tableau.png" class="table-image" alt="Tableau Excel des mondes Forge of Empires de Legodingo13">
    </div>
    <a class="primary-button gold-button" href="tableau.png" target="_blank" rel="noopener noreferrer">Ouvrir le tableau en grand</a>
    """
else:
    profil_tableau_view = """
    <div class="notice">
        Aucun tableau n'a encore été envoyé sur le site. Il apparaîtra ici automatiquement
        après le prochain lancement de l'application Legodingo13 Bot4.
    </div>
    """

profil_body = f"""
<img src="profil_tableau.png" class="tile-logo profile-tableau-logo" alt="Profil Legodingo13">
<h1>Profil Legodingo13</h1>
<p class="lead">
Tableau Excel des mondes Forge of Empires de Legodingo13. Cette page affiche la dernière
version publiée depuis l'application Legodingo13 Bot4. Enregistre le fichier Excel avant
d'ouvrir l'application pour publier les dernières modifications.
</p>
{profil_tableau_view}
"""
shell(
    "profil.html",
    "profil",
    "Profil Legodingo13 - Tableau Excel des mondes FOE",
    "Profil Legodingo13 : dernière version du tableau Excel des mondes Forge of Empires.",
    profil_body,
)


# TABLEAU - ANCIENNE URL CONSERVÉE POUR COMPATIBILITÉ
# Même contenu que profil.html afin que TOUS les anciens liens affichent aussi le tableau Excel.
shell(
    "tableau.html",
    "profil",
    "Profil Legodingo13 - Tableau Excel des mondes FOE",
    "Profil Legodingo13 : dernière version du tableau Excel des mondes Forge of Empires.",
    profil_body,
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
    "profil_tableau.png",
    "roi_chute.png",

    # Logos des sites tiers
    "forgedb.png",
    "foe_scoredb.png",
    "foe_data.png",
    "banana_db.png",
    "foe_tools.png",

    # Logos des extensions
    "foe_hammer.png",
    "foe_helper.png",

    # Logo de la chaîne UBERnerd14
    "ubernerd14.png",

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
print("Pages générées : Accueil, Discord, YouTube, Profil Legodingo13 (tableau Excel), compatibilité tableau.html")
