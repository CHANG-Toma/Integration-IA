# Script 11 — Mini serveur FastAPI qui interroge un LLM
# Room 04 — Connecter une API
# Challenge : historique de conversation (10 derniers échanges max)
# Lancer avec : uvicorn ROOMS.04_Connecter_une_API.code.11_mini_api_fastapi:app --reload --port 8000

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from fastapi import FastAPI
from pydantic import BaseModel
from utils import creer_client, MODELE

# Création du client (API gratuite détectée automatiquement)
client = creer_client()

# Création de l'application FastAPI
app = FastAPI(title="Mini Assistant LLM", version="1.0")

# Historique de conversation en mémoire (max 10 échanges = 20 messages)
MAX_ECHANGES = 10
historique: list[dict] = []


class QuestionRequest(BaseModel):
    question: str


class ReponseResult(BaseModel):
    question: str
    reponse: str
    tokens_utilises: int


def _tronquer_historique():
    """Garde au maximum les MAX_ECHANGES derniers échanges."""
    global historique
    if len(historique) > MAX_ECHANGES * 2:
        historique = historique[-(MAX_ECHANGES * 2):]


@app.post("/question", response_model=ReponseResult)
def poser_question(req: QuestionRequest):
    """Reçoit une question, l'envoie au LLM avec l'historique et retourne la réponse."""
    # Construire les messages : system + historique + nouvelle question
    messages = [
        {"role": "system", "content": "Tu es un assistant concis et pédagogique."},
        *historique,
        {"role": "user", "content": req.question}
    ]

    completion = client.chat.completions.create(
        model=MODELE,
        messages=messages,
        temperature=0.3,
        max_tokens=300
    )

    reponse = completion.choices[0].message.content
    tokens = completion.usage.total_tokens if completion.usage else 0

    # Ajouter l'échange à l'historique
    historique.append({"role": "user", "content": req.question})
    historique.append({"role": "assistant", "content": reponse})
    _tronquer_historique()

    return ReponseResult(
        question=req.question,
        reponse=reponse,
        tokens_utilises=tokens
    )


@app.get("/historique")
def obtenir_historique():
    """Retourne la liste des messages échangés."""
    return {"messages": historique}


@app.post("/reset")
def reinitialiser_historique():
    """Vide l'historique de conversation."""
    global historique
    historique = []
    return {"statut": "ok", "message": "Historique vidé."}


@app.get("/sante")
def verifier_sante():
    """Retourne un message simple pour vérifier que le serveur est opérationnel."""
    return {"statut": "ok", "message": "Le serveur fonctionne correctement."}
