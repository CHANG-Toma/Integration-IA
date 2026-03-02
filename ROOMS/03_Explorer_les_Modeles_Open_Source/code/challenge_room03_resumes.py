# Challenge Room 03 — Résumé de texte avec 3 modèles
# Utilise Groq (3 modèles différents) pour comparer les résumés.
# Alternative : Hugging Face router (décommenter USE_HF_ROUTER et définir HF_TOKEN).

import io
import os
import sys
import time
import requests
from dotenv import load_dotenv

# Affichage UTF-8 sur Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Charger .env depuis la racine du projet
projet_root = os.path.join(os.path.dirname(__file__), "..", "..", "..")
load_dotenv(os.path.join(projet_root, ".env"))
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Chemin du texte à résumer
TEXTE_PATH = os.path.join(projet_root, "datasets", "texte_entreprise.txt")
PROMPT_INSTRUCTION = "Résume ce texte en 5 phrases claires et concises."

# --- Option Groq (recommandé : fonctionne sans config HF Inference Providers) ---
# 3 modèles Groq pour la comparaison : petit, moyen, gros
MODELES_GROQ = [
    ("Llama-3.1-8B (rapide)", "llama-3.1-8b-instant"),
    ("Llama-3.3-70B (puissant)", "llama-3.3-70b-versatile"),
    ("GPT-OSS-20B", "openai/gpt-oss-20b"),
]

# --- Option Hugging Face router (si providers activés + carte enregistrée) ---
MODELES_HF = [
    ("Mistral-7B-Instruct", "mistralai/Mistral-7B-Instruct-v0.1:fastest"),
    ("Llama-2-7b-chat", "meta-llama/Llama-2-7b-chat-hf:fastest"),
    ("Phi-3-mini", "microsoft/Phi-3-mini-4k-instruct:fastest"),
]
ROUTER_CHAT_URL = "https://router.huggingface.co/v1/chat/completions"


def charger_texte():
    with open(TEXTE_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def appeler_groq(client, nom, model_id, prompt_complet):
    debut = time.time()
    try:
        r = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt_complet}],
            max_tokens=400,
            temperature=0.3,
        )
        duree = time.time() - debut
        texte = (r.choices[0].message.content or "").strip()
        return texte, duree, None
    except Exception as e:
        duree = time.time() - debut
        return None, duree, str(e)[:200]


def appeler_hf_router(nom, model_id, prompt_complet):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt_complet}],
        "max_tokens": 400,
        "temperature": 0.3,
    }
    debut = time.time()
    try:
        r = requests.post(ROUTER_CHAT_URL, headers=headers, json=payload, timeout=120)
        duree = time.time() - debut
        if r.status_code != 200:
            return None, duree, f"{r.status_code}: {r.text[:200]}"
        data = r.json()
        texte = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
        return texte.strip(), duree, None
    except Exception as e:
        duree = time.time() - debut
        return None, duree, str(e)[:200]


def main():
    # Priorité : Groq si clé présente (évite les soucis HF Inference Providers)
    if GROQ_API_KEY:
        try:
            sys.path.insert(0, projet_root)
            from utils import creer_client
            client = creer_client()
        except Exception:
            client = None
        if client:
            texte = charger_texte()
            prompt_complet = f"{PROMPT_INSTRUCTION}\n\n{texte}"
            print("=== Challenge Room 03 — Resumes par 3 modeles (Groq) ===\n")
            resultats = {}
            for nom, model_id in MODELES_GROQ:
                print(f"Appel {nom}... ", end="", flush=True)
                resume, duree, err = appeler_groq(client, nom, model_id, prompt_complet)
                if err:
                    print(f"ERREUR: {err}")
                    resultats[nom] = {"resume": f"[Erreur: {err}]", "duree": duree}
                else:
                    print(f"OK ({duree:.1f}s)")
                    resultats[nom] = {"resume": resume, "duree": duree}
            print("\n" + "=" * 60)
            for nom, data in resultats.items():
                print(f"\n--- {nom} ({data['duree']:.1f}s) ---\n{data['resume']}\n")
            return resultats
    # Sinon : essai Hugging Face router
    if not HF_TOKEN or HF_TOKEN == "hf_votre_token_huggingface_ici":
        print("Erreur : definissez GROQ_API_KEY ou HF_TOKEN dans le fichier .env (racine du projet)")
        sys.exit(1)
    texte = charger_texte()
    prompt_complet = f"{PROMPT_INSTRUCTION}\n\n{texte}"
    print("=== Challenge Room 03 — Resumes par 3 modeles (router.huggingface.co) ===\n")
    resultats = {}
    for nom, model_id in MODELES_HF:
        print(f"Appel {nom}... ", end="", flush=True)
        resume, duree, err = appeler_hf_router(nom, model_id, prompt_complet)
        if err:
            print(f"ERREUR: {err}")
            resultats[nom] = {"resume": f"[Erreur: {err}]", "duree": duree}
        else:
            print(f"OK ({duree:.1f}s)")
            resultats[nom] = {"resume": resume, "duree": duree}
    print("\n" + "=" * 60)
    for nom, data in resultats.items():
        print(f"\n--- {nom} ({data['duree']:.1f}s) ---\n{data['resume']}\n")
    return resultats


if __name__ == "__main__":
    main()
