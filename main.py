from datetime import datetime, timezone
import json
import os
from pathlib import Path

PROJECT_NAME = "DONGO AutoSocial"
BRAND_NAME = "DONGO INNOVATION"

DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "history.json"


def load_history():
    """Charge l'historique des publications."""
    if not HISTORY_FILE.exists():
        return []

    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    """Enregistre l'historique des publications."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def create_daily_idea():
    """Choisit un thème de publication selon le jour."""
    themes = {
        0: "Intelligence artificielle",
        1: "Infographie et design",
        2: "Marketing digital",
        3: "Technologies et astuces numériques",
        4: "Présentation des services DONGO INNOVATION",
        5: "Entrepreneuriat",
        6: "Communauté et échanges",
    }

    today = datetime.now().weekday()

    return {
        "date": datetime.now().astimezone().strftime("%Y-%m-%d"),
        "theme": themes[today],
        "brand": BRAND_NAME,
        "slogan": "Quand la créativité rencontre l'intelligence",
    }


def main():
    print("=" * 45)
    print(PROJECT_NAME)
    print(BRAND_NAME)
    print("=" * 45)

    idea = create_daily_idea()

    history = load_history()

    already_exists = any(
        item.get("date") == idea["date"]
        for item in history
    )

    if already_exists:
        print("Une entrée existe déjà pour aujourd'hui.")
    else:
        history.append(idea)
        save_history(history)
        print("Nouvelle idée enregistrée.")

    print("\nThème du jour :", idea["theme"])
    print("Slogan :", idea["slogan"])
    print("Date :", idea["date"])
    print("\nÉtat : programme de base exécuté.")
    print("Aucune publication Facebook n'a été envoyée.")


if __name__ == "__main__":
    main()