"""
Assistant de recherche documentaire basé sur un index vectoriel ChromaDB
et un modèle Groq (LLM) accessible via `utils.py`.

Fonctionnalités principales :
- RAG : recherche de passages pertinents dans `rapport_fictif.pdf`
- Génération de réponses contextualisées à partir des passages
- Extension challenge : logging + monitoring
  - journalisation de chaque requête et réponse
  - temps de réponse
  - nombre de tokens estimé
  - génération d'un rapport d'utilisation synthétique
"""

import csv
import datetime as dt
import os
import sys
import time
from typing import List, Tuple

import chromadb
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from utils import MODELE, creer_client  # noqa: E402


client_llm = creer_client()

BASE_DIR = os.path.dirname(__file__)
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

JOURNAL_PATH = os.path.join(LOGS_DIR, "journal_sessions.csv")
RAPPORT_PATH = os.path.join(LOGS_DIR, "rapport_utilisation.txt")


def charger_index(nom_collection: str = "assistant_recherche_doc") -> Tuple[object, SentenceTransformer]:
    client_chroma = chromadb.Client()
    collection = client_chroma.get_or_create_collection(name=nom_collection)

    if collection.count() == 0:
        print(
            "La collection ChromaDB est vide.\n"
            "Assurez-vous d'avoir exécuté au préalable `indexation_corpus.py` "
            "pour créer l'index vectoriel."
        )
        raise SystemExit(1)

    modele_embedding = SentenceTransformer("all-MiniLM-L6-v2")
    return collection, modele_embedding


def rechercher_contexte(question: str, collection, modele_embedding, n_resultats: int = 3) -> List[str]:
    vecteur_q = modele_embedding.encode([question])[0]
    resultats = collection.query(
        query_embeddings=[vecteur_q.tolist()],
        n_results=n_resultats,
    )
    documents = resultats.get("documents", [[]])[0]
    return documents


def generer_reponse_rag(question: str, passages: List[str]) -> str:
    if not passages:
        contexte = "(aucun passage trouvé dans le corpus)"
    else:
        contexte = "\n---\n".join(passages)

    prompt = (
        "Tu es un assistant de recherche documentaire.\n"
        "Tu dois répondre UNIQUEMENT à partir des extraits fournis.\n"
        "Si l'information ne se trouve pas dans les extraits, tu le dis clairement.\n"
        "Lorsque c'est possible, tu cites les passages pertinents (en les résumant).\n\n"
        f"Extraits du document :\n---\n{contexte}\n---\n\n"
        f"Question de l'utilisateur : {question}"
    )

    completion = client_llm.chat.completions.create(
        model=MODELE,
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un assistant de recherche documentaire sérieux, "
                    "tu t'appuies uniquement sur les documents fournis."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=600,
    )

    texte_reponse = completion.choices[0].message.content.strip()
    return texte_reponse


def estimer_tokens(textes: List[str]) -> int:
    total_mots = 0
    for t in textes:
        if not t:
            continue
        total_mots += len(t.split())
    # Approximation grossière : ~1 token pour 0.75 mot
    return int(total_mots / 0.75) if total_mots else 0


def initialiser_journal() -> None:
    if os.path.exists(JOURNAL_PATH):
        return

    with open(JOURNAL_PATH, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp_utc",
                "question",
                "reponse_longueur_caracteres",
                "nb_passages_contexte",
                "temps_reponse_secondes",
                "tokens_estimes",
            ]
        )


def journaliser_interaction(
    question: str,
    reponse: str,
    nb_passages: int,
    temps_reponse: float,
    tokens: int,
) -> None:
    initialiser_journal()
    timestamp = dt.datetime.utcnow().isoformat()
    with open(JOURNAL_PATH, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                timestamp,
                question,
                len(reponse),
                nb_passages,
                round(temps_reponse, 3),
                tokens,
            ]
        )


def generer_rapport_utilisation() -> None:
    if not os.path.exists(JOURNAL_PATH):
        print("Aucune interaction enregistrée pour le moment (fichier de log introuvable).")
        return

    nb_requetes = 0
    total_temps = 0.0
    total_tokens = 0
    temps_max = 0.0
    temps_min = None

    with open(JOURNAL_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for ligne in reader:
            nb_requetes += 1
            t = float(ligne["temps_reponse_secondes"])
            tok = int(ligne["tokens_estimes"])
            total_temps += t
            total_tokens += tok
            temps_max = max(temps_max, t)
            temps_min = t if temps_min is None else min(temps_min, t)

    if nb_requetes == 0:
        print("Le journal existe mais aucune interaction n'a encore été enregistrée.")
        return

    temps_moyen = total_temps / nb_requetes
    tokens_moyens = total_tokens / nb_requetes if nb_requetes else 0

    lignes_rapport = [
        "=== Rapport d'utilisation de l'assistant de recherche documentaire ===",
        "",
        f"Nombre total de requêtes      : {nb_requetes}",
        f"Temps de réponse moyen (s)    : {temps_moyen:.3f}",
        f"Temps de réponse min / max (s): {temps_min:.3f} / {temps_max:.3f}",
        f"Tokens estimés moyens         : {tokens_moyens:.1f}",
        "",
        f"Fichier de journal analysé    : {JOURNAL_PATH}",
        "",
        "Ce rapport est une estimation basée sur le comptage de mots et ne doit pas être",
        "interprété comme une mesure exacte des tokens facturés par le fournisseur.",
    ]

    texte_rapport = "\n".join(lignes_rapport)

    print()
    print(texte_rapport)
    print()

    with open(RAPPORT_PATH, mode="w", encoding="utf-8") as f:
        f.write(texte_rapport)

    print(f"Rapport d'utilisation enregistré dans : {RAPPORT_PATH}")


def boucle_principale() -> None:
    collection, modele_emb = charger_index()

    print("=== Assistant de recherche documentaire (RAG) ===")
    print("Posez vos questions sur le rapport indexé.")
    print("Commandes spéciales :")
    print("  - 'quitter' : terminer la session")
    print("  - 'rapport' : générer un rapport d'utilisation à partir des logs")
    print()

    while True:
        question = input("Question : ").strip()

        if not question:
            continue

        if question.lower() == "quitter":
            print("Au revoir.")
            break

        if question.lower() == "rapport":
            generer_rapport_utilisation()
            continue

        debut = time.time()
        passages = rechercher_contexte(question, collection, modele_emb, n_resultats=3)
        reponse = generer_reponse_rag(question, passages)
        fin = time.time()

        temps_reponse = fin - debut
        tokens = estimer_tokens([question] + passages + [reponse])

        print("\n--- Passages de contexte utilisés (aperçu) ---")
        if not passages:
            print("(Aucun passage trouvé)")
        else:
            for i, p in enumerate(passages):
                extrait = p[:200].replace("\n", " ")
                print(f"[{i + 1}] {extrait}...")

        print("\n--- Réponse ---")
        print(reponse)
        print(f"\n(Temps de réponse : {temps_reponse:.3f} s, tokens estimés : {tokens})")
        print()

        journaliser_interaction(
            question=question,
            reponse=reponse,
            nb_passages=len(passages),
            temps_reponse=temps_reponse,
            tokens=tokens,
        )


if __name__ == "__main__":
    boucle_principale()

