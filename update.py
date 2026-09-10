import urllib.request
import json
import html
import os
import shutil
from datetime import datetime, timezone

import yt_dlp


# =========================================================
# LIENS LEGODINGO13
# =========================================================

DISCORD_INVITE = "ujHH2bNzhn"

YOUTUBE_URL = "https://www.youtube.com/@Legodingo13"
YOUTUBE_VIDEOS_URL = "https://www.youtube.com/@Legodingo13/videos"

FOE_URL = "https://fr0.forgeofempires.com/page/"
GUNS_URL = "https://guns.lol/legodingo13"

# Nous nous occuperons de Google Search Console plus tard.
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


def find_follower_count(data):

    if isinstance(data, dict):

        count = data.get(
            "channel_follower_count"
        )

        if count is not None:
            return count

        entries = data.get("entries")

        if entries:

            for entry in entries:

                result = find_follower_count(
                    entry
                )

                if result is not None:
                    return result

    elif isinstance(data, list):

        for item in data:

            result = find_follower_count(
                item
            )

            if result is not None:
                return result

    return None


def get_first_video_url():

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": "in_playlist",
        "playlist_items": "1",
    }

    with yt_dlp.YoutubeDL(
        options
    ) as ydl:

        info = ydl.extract_info(
            YOUTUBE_VIDEOS_URL,
            download=False
        )

    entries = info.get(
        "entries"
    ) or []

    if not entries:
        return None

    entry = entries[0] or {}

    if entry.get("webpage_url"):
        return entry["webpage_url"]

    if entry.get("id"):

        return (
            "https://www.youtube.com/watch?v="
            + entry["id"]
        )

    if (
        isinstance(entry.get("url"), str)
        and entry["url"].startswith("http")
    ):
        return entry["url"]

    return None


def get_youtube_subscribers():

    previous_count = (
        read_previous_youtube_count()
    )

    # -----------------------------------------------------
    # MÉTHODE 1 :
    # lecture directe de la chaîne YouTube
    # -----------------------------------------------------

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "playlist_items": "0,0",
    }

    try:

        with yt_dlp.YoutubeDL(
            options
        ) as ydl:

            info = ydl.extract_info(
                YOUTUBE_URL,
                download=False
            )

        count = find_follower_count(
            info
        )

        if count is not None:

            return format_number(
                count
            )

    except Exception as error:

        print(
            "Lecture directe YouTube impossible :",
            error
        )


    # -----------------------------------------------------
    # MÉTHODE 2 :
    # si nécessaire, lecture via une vidéo publique
    # -----------------------------------------------------

    try:

        video_url = (
            get_first_video_url()
        )

        if video_url:

            video_options = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "noplaylist": True,
            }

            with yt_dlp.YoutubeDL(
                video_options
            ) as ydl:

                video_info = (
                    ydl.extract_info(
                        video_url,
                        download=False
                    )
                )

            count = (
                find_follower_count(
                    video_info
                )
            )

            if count is not None:

                return format_number(
                    count
                )

    except Exception as error:

        print(
            "Lecture YouTube via vidéo impossible :",
            error
        )


    # -----------------------------------------------------
    # MÉTHODE DE SECOURS :
    # garder le dernier compteur connu
    # -----------------------------------------------------

    if previous_count:
        return previous_count

    return "indisponible"


# =========================================================
# RÉCUPÉRATION DES STATISTIQUES DISCORD
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
        response.read().decode(
            "utf-8"
        )
    )


guild = discord_data.get(
    "guild",
    {}
)

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
# RÉCUPÉRATION DU NOMBRE D'ABONNÉS YOUTUBE
# =========================================================

youtube_subscribers = (
    get_youtube_subscribers()
)

if youtube_subscribers == "indisponible":

    youtube_display = (
        "Compteur temporairement indisponible"
    )

else:

    youtube_display = (
        f"{youtube_subscribers} abonnés"
    )


# =========================================================
# DATE DE MISE À JOUR
# =========================================================

updated = datetime.now(
    timezone.utc
).strftime(
    "%d/%m/%Y à %H:%M UTC"
)


# =========================================================
# CRÉATION DU DOSSIER DU SITE
# =========================================================

os.makedirs(
    "_site",
    exist_ok=True
)


# =========================================================
# PAGE INTERNET
# =========================================================

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
    content="Legodingo13 : serveur Discord francophone Forge of Empires avec {member_count} membres, chaîne YouTube Legodingo13 avec {youtube_display}, liens Forge of Empires et guns.lol."
>

<meta
    name="robots"
    content="index, follow"
>

{GOOGLE_META}


<style>


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

    max-width:
        1050px;
}}


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

    overflow:
        hidden;

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

    position:
        absolute;

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


.header {{

    text-align:
        center;

    padding:
        38px
        35px
        15px
        35px;
}}


.logo {{

    width:
        190px;

    max-width:
        75%;

    height:
        auto;

    display:
        block;

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

    display:
        inline-block;

    padding:
        8px
        17px;

    margin-bottom:
        18px;

    border-radius:
        999px;

    background:
        rgba(202, 112, 33, 0.20);

    border:
        1px solid
        rgba(255, 183, 82, 0.40);

    color:
        #ffd69a;

    font-size:
        13px;

    font-weight:
        bold;

    letter-spacing:
        1px;
}}


h1 {{

    margin:
        0;

    font-size:
        clamp(
            34px,
            5.5vw,
            58px
        );

    line-height:
        1.05;

    text-shadow:
        0
        4px
        20px
        rgba(0, 0, 0, 0.55);
}}


.server-name {{

    margin-top:
        14px;

    color:
        #ffd493;

    font-size:
        22px;

    font-weight:
        bold;
}}


.description {{

    max-width:
        820px;

    margin:
        20px
        auto
        0
        auto;

    color:
        #e7e3df;

    font-size:
        16px;

    line-height:
        1.7;
}}


/* =========================================================
   STATISTIQUES DISCORD
   ========================================================= */

.stats {{

    display:
        grid;

    grid-template-columns:
        repeat(2, 1fr);

    gap:
        24px;

    padding:
        28px
        38px;
}}


.stat {{

    text-align:
        center;

    padding:
        30px
        20px;

    border-radius:
        20px;

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

    display:
        block;

    margin-bottom:
        9px;

    font-size:
        clamp(
            42px,
            6vw,
            62px
        );

    line-height:
        1;

    font-weight:
        800;

    color:
        white;

    text-shadow:
        0
        3px
        15px
        rgba(0, 0, 0, 0.45);
}}


.label {{

    color:
        #d4d7de;

    font-size:
        16px;
}}


.online-dot {{

    display:
        inline-block;

    width:
        10px;

    height:
        10px;

    margin-right:
        7px;

    border-radius:
        50%;

    background:
        #3ba55d;

    box-shadow:
        0
        0
        8px
        rgba(59, 165, 93, 0.8);
}}


/* =========================================================
   BOUTON DISCORD
   ========================================================= */

.discord-area {{

    text-align:
        center;

    padding:
        4px
        38px
        36px
        38px;
}}


.main-text {{

    max-width:
        760px;

    margin:
        0
        auto
        25px
        auto;

    color:
        #f2f2f2;

    font-size:
        17px;

    line-height:
        1.7;
}}


.main-text strong {{

    color:
        #ffd18a;
}}


.discord-button {{

    display:
        inline-block;

    padding:
        16px
        30px;

    border-radius:
        14px;

    text-decoration:
        none;

    color:
        white;

    font-size:
        17px;

    font-weight:
        bold;

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
        0.2s;
}}


.discord-button:hover {{

    transform:
        translateY(-3px);

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

    text-align:
        center;

    font-size:
        26px;
}}


.links-grid {{

    display:
        grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap:
        18px;
}}


.link-card {{

    min-height:
        190px;

    padding:
        24px
        18px;

    border-radius:
        18px;

    text-decoration:
        none;

    color:
        white;

    text-align:
        center;

    display:
        flex;

    flex-direction:
        column;

    justify-content:
        center;

    background:
        rgba(
            255,
            255,
            255,
            0.055
        );

    border:
        1px solid
        rgba(
            255,
            255,
            255,
            0.10
        );

    transition:
        0.2s;
}}


.link-card:hover {{

    transform:
        translateY(-4px);

    background:
        rgba(
            255,
            255,
            255,
            0.09
        );

    border-color:
        rgba(
            255,
            210,
            130,
            0.42
        );
}}


.link-icon {{

    width:
        52px;

    height:
        52px;

    margin:
        0
        auto
        14px
        auto;

    border-radius:
        15px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    font-size:
        21px;

    font-weight:
        800;
}}


.youtube-icon {{

    background:
        #ff0033;
}}


.foe-icon {{

    color:
        #ffe1a5;

    background:
        linear-gradient(
            145deg,
            #b66b27,
            #744019
        );
}}


.guns-icon {{

    background:
        linear-gradient(
            145deg,
            #7d49df,
            #4c2c8e
        );
}}


.link-name {{

    margin-bottom:
        9px;

    font-size:
        19px;

    font-weight:
        bold;
}}


.youtube-count {{

    margin-bottom:
        6px;

    color:
        #ffd493;

    font-size:
        24px;

    font-weight:
        800;
}}


.link-detail {{

    color:
        #c4c9d2;

    font-size:
        14px;

    line-height:
        1.45;
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
        rgba(
            255,
            255,
            255,
            0.08
        );

    text-align:
        center;

    color:
        #aeb4bf;

    font-size:
        13px;
}}


.footer {{

    margin-top:
        8px;

    color:
        #7f8794;

    font-size:
        12px;
}}


/* =========================================================
   VERSION TÉLÉPHONE
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

        border-radius:
            20px;
    }}


    .header {{

        padding:
            28px
            20px
            10px
            20px;
    }}


    .logo {{

        width:
            155px;
    }}


    .stats {{

        grid-template-columns:
            1fr;

        padding:
            22px
            20px;

        gap:
            15px;
    }}


    .discord-area {{

        padding:
            0
            20px
            30px
            20px;
    }}


    .discord-button {{

        width:
            100%;
    }}


    .links-section {{

        padding:
            0
            20px
            30px
            20px;
    }}


    .links-grid {{

        grid-template-columns:
            1fr;
    }}


    .link-card {{

        min-height:
            155px;
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


<div class="link-icon foe-icon">
FOE
</div>


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
# COPIE DU FOND ET DU LOGO
# =========================================================

for image in [
    "fond.png",
    "logo.png"
]:

    if os.path.exists(image):

        shutil.copy2(
            image,
            os.path.join(
                "_site",
                image
            )
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
    f"YouTube : "
    f"{youtube_subscribers} abonnés"
)
