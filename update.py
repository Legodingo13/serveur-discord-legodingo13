import urllib.request
import json
import html
import os
from datetime import datetime, timezone

# Invitation permanente de ton serveur Discord
INVITE_CODE = "ujHH2bNzhn"

# On ajoutera ici la balise Google plus tard.
GOOGLE_META = """<!-- Balise Google Search Console à ajouter plus tard -->"""

# Demande à Discord le nombre de membres
url = f"https://discord.com/api/v10/invites/{INVITE_CODE}?with_counts=true"

request = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=30) as response:
    data = json.loads(response.read().decode("utf-8"))

guild = data.get("guild", {})

guild_name = html.escape(
    guild.get("name", "Serveur Discord de Legodingo13")
)

member_count = data.get("approximate_member_count", "inconnu")
online_count = data.get("approximate_presence_count", "inconnu")

updated = datetime.now(timezone.utc).strftime("%d/%m/%Y à %H:%M UTC")

# Création du dossier du site
os.makedirs("_site", exist_ok=True)

# Création de la page que Google pourra lire
page = f"""<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">

    <title>Serveur Discord de Legodingo13 - {member_count} membres</title>

    <meta name="description"
          content="Le serveur Discord de Legodingo13 compte actuellement environ {member_count} membres, dont {online_count} membres en ligne.">

    <meta name="robots" content="index, follow">

    {GOOGLE_META}

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>

    <main>

        <h1>Serveur Discord de Legodingo13</h1>

        <h2>{guild_name}</h2>

        <p>
            Le serveur Discord de Legodingo13 compte actuellement
            <strong>{member_count} membres</strong>.
        </p>

        <p>
            Environ
            <strong>{online_count} membres sont actuellement en ligne</strong>.
        </p>

        <p>
            Il s'agit de la communauté Discord de Legodingo13,
            notamment consacrée à Forge of Empires.
        </p>

        <p>
            Invitation officielle :
            <a href="https://discord.gg/{INVITE_CODE}">
                Rejoindre le serveur Discord
            </a>
        </p>

        <p>
            Dernière mise à jour automatique :
            <strong>{updated}</strong>
        </p>

    </main>

</body>
</html>
"""

with open("_site/index.html", "w", encoding="utf-8") as f:
    f.write(page)

# Ce fichier change à chaque exécution afin que le dépôt reste actif.
with open("last-update.txt", "w", encoding="utf-8") as f:
    f.write(f"Dernière mise à jour : {updated}\n")
    f.write(f"Membres : {member_count}\n")
    f.write(f"En ligne : {online_count}\n")

print(f"{guild_name} : {member_count} membres")
