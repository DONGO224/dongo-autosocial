
import json
import os
import urllib.request
import urllib.error
from datetime import datetime


BRAND = "DONGO INNOVATION"
SLOGAN = "Quand la créativité rencontre l'intelligence"


def generate_publication():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Secret GEMINI_API_KEY introuvable.")

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    prompt = f"""
Tu es le responsable marketing de {BRAND}.

Notre slogan : {SLOGAN}

Date : {datetime.now().strftime("%Y-%m-%d")}

Notre activité :
- Infographie et design graphique
- Intelligence artificielle
- Formation numérique
- Montage photo et vidéo
- Marketing digital

Crée une publication Facebook originale en français.

Choisis un sujet intéressant parmi nos activités.

La publication doit contenir :
1. Un titre accrocheur.
2. Un texte utile et intéressant.
3. Un appel à l'action.
4. Trois à cinq hashtags.

Adopte un ton professionnel, naturel et accessible.
Ne fabrique pas de témoignages ou de résultats.
Retourne uniquement la publication.
"""

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{model}:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
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

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        publication = (
            result["candidates"][0]["content"]["parts"][0]["text"]
        )

        return publication.strip()

    except urllib.error.HTTPError as error:
        details = error.read().decode(
            "utf-8", errors="replace"
        )
        raise RuntimeError(
            f"Erreur Gemini HTTP {error.code}: {details[:1500]}"
        ) from error

    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError(
            "Gemini a répondu sans fournir de texte exploitable."
        ) from error


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
