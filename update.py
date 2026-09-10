import urllib.request
import json
import html
import os
import shutil
import re
from datetime import datetime, timezone


# =========================================================
# LIENS
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

GOOGLE_META = """<!-- Google Search Console -->"""


# =========================================================
# FONCTIONS
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
        with open(
            "last-update.txt",
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                if line.startswith("Abonnés YouTube :"):

                    value = line.split(":", 1)[1].strip()

                    if value not in (
                        "",
                        "indisponible",
                        "inconnu"
                    ):
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
                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/140.0 Safari/537.36",

                "Accept":
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,*/*;q=0.8",

                "Accept-Language":
                    "fr-FR,fr;q=0.9,en;q=0.8"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            page = response.read().decode(
                "utf-8",
                errors="ignore"
            )

        patterns = [

            r"Legodingo13(?:&#x27;|['’])s "
            r"YouTube presence with\s*"
            r"([\d,\s]+)\s*subscribers",

            r"Legodingo13.*?"
            r"YouTube presence with\s*"
            r"([\d,\s]+)\s*subscribers",

            r"with\s*"
            r"([\d,\s]+)\s*subscribers"
            r"\s+and\s+[\d,\s]+\s+videos"

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                page,
                flags=re.IGNORECASE | re.DOTALL
            )

            if match:

                number = re.sub(
                    r"[^\d]",
                    "",
                    match.group(1)
                )

                if number:

                    return format_number(
                        int(number)
                    )

        json_patterns = [

            r'"subscriberCount"\s*:\s*"?(\d+)"?',
            r'"subscribers"\s*:\s*"?(\d+)"?',
            r'"subscriber_count"\s*:\s*"?(\d+)"?'

        ]

        for pattern in json_patterns:

            match = re.search(
                pattern,
                page,
                flags=re.IGNORECASE
            )

            if match:

                return format_number(
                    int(match.group(1))
                )

        print(
            "SocialCounts a répondu, "
            "mais le nombre d'abonnés "
            "n'a pas été trouvé."
        )

    except Exception as error:

        print(
            "Impossible de lire SocialCounts :",
            error
        )

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
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(
    discord_request,
    timeout=30
) as response:

    discord_data = json.loads(
        response.read().decode("utf-8")
    )


guild = discord_data.get("guild", {})

guild_name = html.escape(
    guild.get(
        "name",
        "Legodingo13 - Serv FOE FR"
    )
)

member_count = format_number(
    discord_data.get(
        "approximate_member_count",
        "inconnu"
    )
)

online_count = format_number(
    discord_data.get(
        "approximate_presence_count",
        "inconnu"
    )
)


# =========================================================
# YOUTUBE
# =========================================================

youtube_subscribers = get_youtube_subscribers()

if youtube_subscribers == "indisponible":

    youtube_display = "Compteur temporairement indisponible"

else:

    youtube_display = f"{youtube_subscribers} abonnés"


# =========================================================
# DATE
# =========================================================

updated = datetime.now(
    timezone.utc
).strftime(
    "%d/%m/%Y à %H:%M UTC"
)


# =========================================================
# CRÉATION DU SITE
# =========================================================

os.makedirs(
    "_site",
    exist_ok=True
)


page = f"""<!DOCTYPE html>

<html lang="fr">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
Legodingo13 - Discord, YouTube et Forge of Empires
</title>

<meta
    name="description"
    content="Legodingo13 : serveur Discord francophone Forge of Empires avec {member_count} membres et chaîne YouTube avec {youtube_display}."
>

<meta
    name="robots"
    content="index, follow"
>

{GOOGLE_META}


<style>


/* =========================================================
   CURSEURS
   ========================================================= */

html,
body {{

    cursor:
        url("cursor_default.cur"),
        auto;
}}


body * {{

    cursor:
        inherit;
}}


a,
a *,
button,
button * {{

    cursor:
        url("cursor_hover.cur"),
        pointer !important;
}}


/* =========================================================
   GÉNÉRAL
   ========================================================= */

* {{
    box-sizing: border-box;
}}


html {{
    min-height: 100%;
}}


body {{

    margin: 0;

    min-height: 100vh;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    color: white;

    background:
        linear-gradient(
            rgba(6, 10, 18, 0.42),
            rgba(6, 10, 18, 0.74)
        ),
        url("fond.png");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;

    display: flex;
    align-items: center;
    justify-content: center;

    padding:
        40px
        20px;
}}


.page {{

    width: 100%;
    max-width: 1050px;
}}


/* =========================================================
   CARTE PRINCIPALE
   ========================================================= */

.card {{

    position: relative;

    width: 100%;

    background:
        linear-gradient(
            145deg,
            rgba(17, 21, 31, 0.90),
            rgba(31, 20, 18, 0.86)
        );

    border:
        1px solid
        rgba(255, 210, 130, 0.23);

    border-radius:
        28px;

    overflow: hidden;

    box-shadow:
        0
        30px
        90px
        rgba(0, 0, 0, 0.58);

    backdrop-filter:
        blur(8px);
}}


.card::before {{

    content: "";

    position: absolute;

    top: 0;
    left: 10%;
    right: 10%;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255, 177, 73, 0.90),
            transparent
        );
}}


/* =========================================================
   EN-TÊTE
   ========================================================= */

.header {{

    text-align: center;

    padding:
        38px
        35px
        15px
        35px;
}}


.logo {{

    width: 190px;
    max-width: 75%;
    height: auto;

    display: block;

    margin:
        0
        auto
        20px
        auto;

    filter:
        drop-shadow(
            0
            8px
            15px
            rgba(0, 0, 0, 0.42)
        );
}}


.badge {{

    display: inline-block;

    padding:
        8px
        17px;

    margin-bottom: 18px;

    border-radius: 999px;

    background:
        rgba(202, 112, 33, 0.20);

    border:
        1px solid
        rgba(255, 183, 82, 0.40);

    color: #ffd69a;

    font-size: 13px;
    font-weight: bold;

    letter-spacing: 1px;
}}


h1 {{

    margin: 0;

    font-size:
        clamp(
            34px,
            5.5vw,
            58px
        );

    line-height: 1.05;

    text-shadow:
        0
        4px
        20px
        rgba(0, 0, 0, 0.55);
}}


.server-name {{

    margin-top: 14px;

    color: #ffd493;

    font-size: 22px;
    font-weight: bold;
}}


.description {{

    max-width: 820px;

    margin:
        20px
        auto
        0
        auto;

    color: #e7e3df;

    font-size: 16px;
    line-height: 1.7;
}}


/* =========================================================
   STATISTIQUES
   ========================================================= */

.stats {{

    display: grid;

    grid-template-columns:
        repeat(2, 1fr);

    gap: 24px;

    padding:
        28px
        38px;
}}


.stat {{

    text-align: center;

    padding:
        30px
        20px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.075),
            rgba(255, 255, 255, 0.035)
        );

    border:
        1px solid
        rgba(255, 255, 255, 0.09);
}}


.number {{

    display: block;

    margin-bottom: 9px;

    font-size:
        clamp(
            42px,
            6vw,
            62px
        );

    line-height: 1;

    font-weight: 800;

    color: white;

    text-shadow:
        0
        3px
        15px
        rgba(0, 0, 0, 0.45);
}}


.label {{

    color: #d4d7de;

    font-size: 16px;
}}


.online-dot {{

    display: inline-block;

    width: 10px;
    height: 10px;

    margin-right: 7px;

    border-radius: 50%;

    background: #3ba55d;

    box-shadow:
        0
        0
        8px
        rgba(59, 165, 93, 0.8);
}}


/* =========================================================
   DISCORD
   ========================================================= */

.discord-area {{

    text-align: center;

    padding:
        4px
        38px
        36px
        38px;
}}


.main-text {{

    max-width: 760px;

    margin:
        0
        auto
        25px
        auto;

    color: #f2f2f2;

    font-size: 17px;
    line-height: 1.7;
}}


.main-text strong {{

    color: #ffd18a;
}}


.discord-button {{

    display: inline-block;

    padding:
        16px
        30px;

    border-radius: 14px;

    text-decoration: none;

    color: white;

    font-size: 17px;
    font-weight: bold;

    background:
        linear-gradient(
            135deg,
            #5865F2,
            #7289da
        );

    box-shadow:
        0
        12px
        30px
        rgba(88, 101, 242, 0.35);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}}


.discord-button:hover {{

    transform: translateY(-3px);

    box-shadow:
        0
        17px
        35px
        rgba(88, 101, 242, 0.45);
}}


/* =========================================================
   LIENS
   ========================================================= */

.links-section {{

    padding:
        0
        38px
        38px
        38px;
}}


.links-title {{

    margin:
        0
        0
        22px
        0;

    text-align: center;

    font-size: 26px;
}}


.links-grid {{

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 18px;
}}


.link-card {{

    min-height: 190px;

    padding:
        24px
        18px;

    border-radius: 18px;

    text-decoration: none;

    color: white;

    text-align: center;

    display: flex;
    flex-direction: column;
    justify-content: center;

    background:
        rgba(255, 255, 255, 0.055);

    border:
        1px solid
        rgba(255, 255, 255, 0.10);

    transition:
        transform 0.2s ease,
        background 0.2s ease,
        border-color 0.2s ease;
}}


.link-card:hover {{

    transform: translateY(-4px);

    background:
        rgba(255, 255, 255, 0.09);

    border-color:
        rgba(255, 210, 130, 0.42);
}}


.link-icon {{

    width: 52px;
    height: 52px;

    margin:
        0
        auto
        14px
        auto;

    border-radius: 15px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 21px;
    font-weight: 800;
}}


.youtube-icon {{
    background: #ff0033;
}}


.guns-icon {{

    background:
        linear-gradient(
            145deg,
            #7d49df,
            #4c2c8e
        );
}}


/* =========================================================
   LOGO FORGE OF EMPIRES
   ========================================================= */

.foe-logo {{

    width: 90px;
    height: auto;

    display: block;

    margin:
        0
        auto
        12px
        auto;

    filter:
        drop-shadow(
            0
            5px
            10px
            rgba(0, 0, 0, 0.40)
        );

    transition:
        transform 0.2s ease;
}}


.link-card:hover .foe-logo {{

    transform:
        scale(1.07);
}}


.link-name {{

    margin-bottom: 9px;

    font-size: 19px;
    font-weight: bold;
}}


.youtube-count {{

    margin-bottom: 6px;

    color: #ffd493;

    font-size: 24px;
    font-weight: 800;
}}


.link-detail {{

    color: #c4c9d2;

    font-size: 14px;
    line-height: 1.45;
}}


/* =========================================================
   BAS DE PAGE
   ========================================================= */

.update {{

    margin:
        0
        38px;

    padding:
        23px
        0
        30px
        0;

    border-top:
        1px solid
        rgba(255, 255, 255, 0.08);

    text-align: center;

    color: #aeb4bf;

    font-size: 13px;
}}


.footer {{

    margin-top: 8px;

    color: #7f8794;

    font-size: 12px;
}}


/* =========================================================
   TÉLÉPHONE
   ========================================================= */

@media
(max-width: 760px) {{

    body {{

        padding:
            20px
            12px;

        background-attachment:
            scroll;
    }}


    .card {{
        border-radius: 20px;
    }}


    .header {{

        padding:
            28px
            20px
            10px
            20px;
    }}


    .logo {{
        width: 155px;
    }}


    .stats {{

        grid-template-columns: 1fr;

        padding:
            22px
            20px;

        gap: 15px;
    }}


    .discord-area {{

        padding:
            0
            20px
            30px
            20px;
    }}


    .discord-button {{
        width: 100%;
    }}


    .links-section {{

        padding:
            0
            20px
            30px
            20px;
    }}


    .links-grid {{
        grid-template-columns: 1fr;
    }}


    .link-card {{
        min-height: 155px;
    }}


    .update {{

        margin:
            0
            20px;
    }}

}}

</style>

</head>


<body>


<main class="page">

<section class="card">


<div class="header">

<img
    src="logo.png"
    alt="Logo de Legodingo13 Forge of Empires"
    class="logo"
>


<div class="badge">
COMMUNAUTÉ LEGODINGO13
</div>


<h1>
Serveur Discord de Legodingo13
</h1>


<div class="server-name">
{guild_name}
</div>


<p class="description">

Le plus gros serveur communautaire francophone autour de Forge of Empires.
Rejoins la communauté pour bénéficier des meilleures aides et de la meilleure
activité de la communauté francophone de Forge of Empires !

</p>


</div>


<section class="stats">


<div class="stat">

<span class="number">
{member_count}
</span>

<span class="label">
membres sur le serveur
</span>

</div>


<div class="stat">

<span class="number">
{online_count}
</span>

<span class="label">

<span class="online-dot"></span>

membres actuellement en ligne

</span>

</div>


</section>


<div class="discord-area">


<p class="main-text">

Le serveur Discord de Legodingo13 compte actuellement

<strong>
{member_count} membres
</strong>,

dont environ

<strong>
{online_count} membres en ligne
</strong>.

</p>


<a
    class="discord-button"
    href="https://discord.gg/{DISCORD_INVITE}"
    target="_blank"
    rel="noopener noreferrer"
>

Rejoindre le serveur Discord

</a>


</div>


<section class="links-section">


<h2 class="links-title">
Retrouve Legodingo13
</h2>


<div class="links-grid">


<a
    class="link-card"
    href="{YOUTUBE_URL}"
    target="_blank"
    rel="noopener noreferrer"
>

<div class="link-icon youtube-icon">
▶
</div>

<div class="link-name">
YouTube
</div>

<div class="youtube-count">
{youtube_display}
</div>

<div class="link-detail">
Chaîne YouTube Legodingo13
</div>

</a>


<a
    class="link-card"
    href="{FOE_URL}"
    target="_blank"
    rel="noopener noreferrer"
>

<img
    src="foe_logo.png"
    alt="Logo officiel Forge of Empires"
    class="foe-logo"
>

<div class="link-name">
Forge of Empires
</div>

<div class="link-detail">
Accéder au site officiel francophone du jeu
</div>

</a>


<a
    class="link-card"
    href="{GUNS_URL}"
    target="_blank"
    rel="noopener noreferrer"
>

<div class="link-icon guns-icon">
L13
</div>

<div class="link-name">
guns.lol
</div>

<div class="link-detail">
Accéder à la page de Legodingo13
</div>

</a>


</div>

</section>


<div class="update">

Dernière mise à jour automatique :

<strong>
{updated}
</strong>


<div class="footer">

Statistiques Discord et YouTube
mises à jour automatiquement.

</div>


</div>


</section>

</main>


</body>

</html>
"""


# =========================================================
# ENREGISTREMENT DU SITE
# =========================================================

with open(
    "_site/index.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(page)


# =========================================================
# COPIE DES FICHIERS
# =========================================================

assets = [
    "fond.png",
    "logo.png",
    "foe_logo.png",
    "cursor_default.cur",
    "cursor_hover.cur"
]


for asset in assets:

    if os.path.exists(asset):

        shutil.copy2(
            asset,
            os.path.join(
                "_site",
                asset
            )
        )

    else:

        print(
            f"ATTENTION : {asset} est introuvable."
        )


# =========================================================
# FICHIER DE SUIVI
# =========================================================

with open(
    "last-update.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        f"Dernière mise à jour : {updated}\\n"
    )

    f.write(
        f"Membres Discord : {member_count}\\n"
    )

    f.write(
        f"En ligne Discord : {online_count}\\n"
    )

    f.write(
        f"Abonnés YouTube : {youtube_subscribers}\\n"
    )


print(
    f"Discord : "
    f"{member_count} membres / "
    f"{online_count} en ligne"
)

print(
    f"YouTube via SocialCounts : "
    f"{youtube_subscribers} abonnés"
)
