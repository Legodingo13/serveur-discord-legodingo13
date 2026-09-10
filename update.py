import urllib.request
import json
import html
import os
import shutil
from datetime import datetime, timezone

# =========================================================
# PARAMÈTRES DU SERVEUR DISCORD
# =========================================================

INVITE_CODE = "ujHH2bNzhn"

# Cette partie servira plus tard pour Google Search Console.
# Pour l'instant, ne touche à rien.
GOOGLE_META = """<!-- Google Search Console -->"""


# =========================================================
# RÉCUPÉRATION DES INFORMATIONS DEPUIS DISCORD
# =========================================================

url = f"https://discord.com/api/v10/invites/{INVITE_CODE}?with_counts=true"

request = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    data = json.loads(response.read().decode("utf-8"))


guild = data.get("guild", {})

guild_name = html.escape(
    guild.get("name", "Legodingo13 - Serv FOE FR")
)

member_count = data.get(
    "approximate_member_count",
    "inconnu"
)

online_count = data.get(
    "approximate_presence_count",
    "inconnu"
)

updated = datetime.now(timezone.utc).strftime(
    "%d/%m/%Y à %H:%M UTC"
)


# =========================================================
# CRÉATION DU SITE
# =========================================================

os.makedirs("_site", exist_ok=True)


page = f"""<!DOCTYPE html>

<html lang="fr">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Serveur Discord Legodingo13 - {member_count} membres
</title>

<meta name="description"
      content="Le serveur Discord de Legodingo13 compte actuellement environ {member_count} membres, dont {online_count} membres en ligne. Communauté francophone Forge of Empires.">

<meta name="robots" content="index, follow">

{GOOGLE_META}

<style>

/* =========================================================
   PARAMÈTRES GÉNÉRAUX
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
            rgba(6, 10, 18, 0.72)
        ),
        url("fond.png");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 40px 20px;
}}


/* =========================================================
   CONTENEUR PRINCIPAL
   ========================================================= */

.page {{
    width: 100%;
    max-width: 1050px;
}}


.card {{
    position: relative;

    width: 100%;

    background:
        linear-gradient(
            145deg,
            rgba(17, 21, 31, 0.86),
            rgba(27, 20, 20, 0.80)
        );

    border:
        1px solid rgba(255, 210, 130, 0.22);

    border-radius: 28px;

    overflow: hidden;

    box-shadow:
        0 30px 90px rgba(0, 0, 0, 0.55);

    backdrop-filter: blur(8px);
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
            rgba(255, 177, 73, 0.85),
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
            rgba(0, 0, 0, 0.40)
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

    color:
        #ffd69a;

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

    color:
        #ffd493;

    font-size: 22px;

    font-weight: bold;
}}


.description {{
    max-width: 720px;

    margin:
        20px
        auto
        0
        auto;

    color:
        #e7e3df;

    font-size: 16px;

    line-height: 1.7;
}}


/* =========================================================
   COMPTEURS
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

    box-shadow:
        inset
        0
        1px
        0
        rgba(255, 255, 255, 0.06);
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
    color:
        #d4d7de;

    font-size: 16px;
}}


.online-dot {{
    display: inline-block;

    width: 10px;
    height: 10px;

    margin-right: 7px;

    border-radius: 50%;

    background:
        #3ba55d;

    box-shadow:
        0
        0
        8px
        rgba(59, 165, 93, 0.8);
}}


/* =========================================================
   TEXTE ET BOUTON
   ========================================================= */

.bottom {{
    text-align: center;

    padding:
        4px
        38px
        34px
        38px;
}}


.main-text {{
    max-width: 760px;

    margin:
        0
        auto
        25px
        auto;

    color:
        #f2f2f2;

    font-size: 17px;

    line-height: 1.7;
}}


.main-text strong {{
    color:
        #ffd18a;
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
    transform:
        translateY(-3px);

    box-shadow:
        0
        17px
        35px
        rgba(88, 101, 242, 0.45);
}}


/* =========================================================
   DERNIÈRE MISE À JOUR
   ========================================================= */

.update {{
    margin-top: 28px;

    padding-top: 22px;

    border-top:
        1px solid
        rgba(255, 255, 255, 0.08);

    color:
        #aeb4bf;

    font-size: 13px;
}}


.update strong {{
    color:
        #d1d5dc;
}}


.footer {{
    margin-top: 8px;

    color:
        #7f8794;

    font-size: 12px;
}}


/* =========================================================
   VERSION TÉLÉPHONE
   ========================================================= */

@media
(max-width: 700px) {{

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


    .stat {{
        padding:
            23px
            15px;
    }}


    .bottom {{
        padding:
            0
            20px
            28px
            20px;
    }}


    .discord-button {{
        width:
            100%;
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

Communauté francophone autour de Legodingo13
et de Forge of Empires.

Rejoins les joueurs du serveur pour discuter,
échanger et partager autour du jeu.

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


<div class="bottom">


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
    href="https://discord.gg/{INVITE_CODE}"
    target="_blank"
    rel="noopener noreferrer"
>

Rejoindre le serveur Discord

</a>


<div class="update">

Dernière mise à jour automatique :

<strong>
{updated}
</strong>

</div>


<div class="footer">

Les statistiques sont mises à jour automatiquement
à partir des données publiques de Discord.

</div>


</div>


</section>

</main>

</body>

</html>
"""


# =========================================================
# ENREGISTREMENT DE LA PAGE
# =========================================================

with open(
    "_site/index.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(page)


# =========================================================
# COPIE DE L'IMAGE DE FOND ET DU LOGO
# =========================================================

images = [
    "fond.png",
    "logo.png"
]

for image in images:

    if os.path.exists(image):

        shutil.copy2(
            image,
            os.path.join(
                "_site",
                image
            )
        )


# =========================================================
# PETIT FICHIER DE SUIVI
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
        f"Membres : {member_count}\\n"
    )

    f.write(
        f"En ligne : {online_count}\\n"
    )


print(
    f"{guild_name} : "
    f"{member_count} membres / "
    f"{online_count} en ligne"
)
