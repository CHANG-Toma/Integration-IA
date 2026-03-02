# utils.py — Module utilitaire pour le cours
# Utilise l'API Groq exclusivement (package officiel groq).
#
# Configuration : définir GROQ_API_KEY dans votre fichier .env
# Clé API : https://console.groq.com
#
# Usage dans un script :
#   from utils import creer_client, MODELE
#   client = creer_client()
#   reponse = client.chat.completions.create(model=MODELE, messages=[...])

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "Clé GROQ_API_KEY manquante. "
        "Ajoutez-la dans votre fichier .env (voir .env.example). "
        "Obtenez une clé gratuite sur https://console.groq.com"
    )

FOURNISSEUR = "Groq"
MODELE = "llama-3.1-8b-instant"
BASE_URL = "https://api.groq.com/openai/v1"


def creer_client():
    """
    Crée et retourne le client officiel Groq (package groq).
    """
    print(f"[API] Fournisseur : {FOURNISSEUR}")
    print(f"[API] Modèle     : {MODELE}")
    print()
    return Groq(api_key=GROQ_API_KEY)


def afficher_config():
    """Affiche la configuration pour aider au diagnostic."""
    print("=== Configuration API (Groq) ===")
    print(f"Fournisseur : {FOURNISSEUR}")
    print(f"Modèle      : {MODELE}")
    print(f"URL de base : {BASE_URL}")
    print(f"Clé Groq    : oui")
    print()


if __name__ == "__main__":
    afficher_config()
