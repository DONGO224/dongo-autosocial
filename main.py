
import json
import os
import time
import urllib.request
import urllib.error
from urllib.error import URLError
from datetime import datetime
from zoneinfo import ZoneInfo


BRAND = "DONGO INNOVATION"
SLOGAN = "Quand la créativité rencontre l'intelligence"

MODELS = [
    os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite"
]


def call_gemini(model, api_key, prompt):
    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{model}:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500
        }
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        },
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))

    parts = result["candidates"][0]["content"]["parts"]
    publication = "".join(
        part.get("text", "") for part in parts
    ).strip()

    if not publication:
        raise RuntimeError("Gemini a retourné un texte vide.")

    return publication


def generate_publication():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Secret GEMINI_API_KEY introuvable.")

    today = datetime.now(
        ZoneInfo("Africa/Douala")
    ).strftime("%Y-%m-%d")

    prompt = f"""
Tu es le responsable marketing de {BRAND}.

Slogan : {SLOGAN}
Date : {today}

Nos activités :
- Infographie et design graphique
- Intelligence artificielle
- Formation numérique
- Montage photo et vidéo
- Marketing digital

Crée une publication Facebook originale en français.

Choisis un sujet intéressant parmi nos activités.

La publication doit contenir :
1. Un titre accrocheur.
2. Un contenu utile et intéressant.
3. Un appel à l'action.
4. Trois à cinq hashtags.

Ton professionnel, naturel et accessible.
Ne fabrique aucun témoignage ni résultat.
Retourne uniquement la publication.
"""

    retryable_errors = {429, 500, 502, 503, 504}
    errors = []

    # Évite de tester deux fois le même modèle.
    models = list(dict.fromkeys(MODELS))

    for model in models:
        print(f"\nEssai du modèle : {model}")

        for attempt in range(3):
            try:
                publication = call_gemini(
                    model, api_key, prompt
                )

                print(f"Modèle utilisé : {model}")
                return publication

            except urllib.error.HTTPError as error:
                details = error.read().decode(
                    "utf-8", errors="replace"
                )

                errors.append(
                    f"{model} : HTTP {error.code} - {details[:500]}"
                )

                if error.code not in retryable_errors:
                    raise RuntimeError(
                        f"Erreur non temporaire avec {model}: "
                        f"HTTP {error.code}: {details[:1000]}"
                    ) from error

                print(
                    f"Erreur HTTP {error.code}, "
                    f"tentative {attempt + 1}/3"
                )

            except (URLError, TimeoutError) as error:
                errors.append(f"{model} : {str(error)}")
                print(
                    f"Problème réseau, "
                    f"tentative {attempt + 1}/3"
                )

            if attempt < 2:
                delay = 10 * (2 ** attempt)
                print(f"Nouvel essai dans {delay} secondes.")
                time.sleep(delay)

        print(f"Le modèle {model} est indisponible.")

    raise RuntimeError(
        "Tous les modèles Gemini ont échoué :\n"
        + "\n".join(errors)
    )


def main():
    print("=" * 50)
    print("DONGO AUTOSOCIAL")
    print(BRAND)
    print("=" * 50)

    publication = generate_publication()

    print("\nPUBLICATION GENEREE PAR GEMINI\n")
    print(publication)

    print("\n" + "=" * 50)
    print("TEST REUSSI : GEMINI EST CONNECTE.")
    print("Aucune publication Facebook n'a ete envoyee.")
    print("=" * 50)


if __name__ == "__main__":
    main()
