# Challenge Room 05 — RAG sur fichier .txt fourni en ligne de commande
# Room 05 — Créer un système RAG
# Usage : python challenge_room05.py chemin/vers/fichier.txt

import io
import os
import sys

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

import chromadb
from sentence_transformers import SentenceTransformer

from utils import creer_client, MODELE

client_llm = creer_client()

TAILLE_SEGMENT = 300
CHEVAUCHEMENT = 50
N_PASSAGES = 3
COLLECTION_NAME = "rag_txt"

# Charge le fichier .txt et retourne son contenu en UTF-8.
def charger_fichier_txt(chemin):
    """Charge un fichier .txt et retourne son contenu en UTF-8."""
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()

# Découpe le texte en segments avec chevauchement.
def decouper_en_segments(texte, taille_segment=TAILLE_SEGMENT, chevauchement=CHEVAUCHEMENT):
    """Découpe le texte en segments avec chevauchement."""
    mots = texte.split()
    segments = []
    debut = 0
    while debut < len(mots):
        fin = debut + taille_segment
        segment = " ".join(mots[debut:fin])
        segments.append(segment)
        debut += taille_segment - chevauchement
    return segments

# Crée l'index ChromaDB à partir des segments.
def construire_index(segments, modele_embedding):
    """Crée l'index ChromaDB à partir des segments."""
    embeddings = modele_embedding.encode(segments)
    client_chroma = chromadb.Client()
    collection = client_chroma.get_or_create_collection(name=COLLECTION_NAME)
    collection.add(
        documents=segments,
        embeddings=[emb.tolist() for emb in embeddings],
        ids=[f"seg_{i}" for i in range(len(segments))],
    )
    return collection

# Retourne les n segments les plus pertinents pour la question.
def rechercher_contexte(question, collection, modele_embedding, n_resultats=N_PASSAGES):
    """Retourne les n segments les plus pertinents pour la question."""
    vecteur_q = modele_embedding.encode([question])[0]
    resultats = collection.query(
        query_embeddings=[vecteur_q.tolist()],
        n_results=n_resultats,
    )
    return resultats["documents"][0]

# Génère une réponse à partir des passages et de la question.
def generer_reponse_rag(question, passages):
    """Génère une réponse à partir des passages et de la question."""
    contexte = "\n---\n".join(passages)
    prompt = (
        f"Voici des extraits d'un document :\n"
        f"---\n{contexte}\n---\n\n"
        f"En te basant UNIQUEMENT sur ces extraits, réponds à la question suivante.\n"
        f"Si l'information n'est pas dans les extraits, dis-le explicitement.\n"
        f"Réponse concise.\n\n"
        f"Question : {question}"
    )
    reponse = client_llm.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "system", "content": "Tu réponds uniquement à partir des documents fournis."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=500,
    )
    return reponse.choices[0].message.content

# Lance le programme.
def main():
    if len(sys.argv) < 2:
        print("Usage : python challenge_room05.py <fichier.txt>")
        print("Exemple : python challenge_room05.py mon_fichier.txt")
        sys.exit(1)

    chemin = sys.argv[1].strip()

    if not chemin.lower().endswith(".txt"):
        print("Erreur : le fichier doit avoir l'extension .txt")
        sys.exit(1)

    if not os.path.isfile(chemin):
        print(f"Erreur : le fichier '{chemin}' n'existe pas ou n'est pas accessible.")
        sys.exit(1)

    print("Chargement du fichier...")
    texte = charger_fichier_txt(chemin)
    if not texte.strip():
        print("Erreur : le fichier est vide.")
        sys.exit(1)

    segments = decouper_en_segments(texte)
    print(f"Document découpé en {len(segments)} segments.")

    print("Chargement du modèle d'embedding...")
    modele_emb = SentenceTransformer("all-MiniLM-L6-v2")

    print("Création de l'index vectoriel (ChromaDB)...")
    collection = construire_index(segments, modele_emb)
    print(f"Index prêt : {collection.count()} segments indexés.")
    print()

    print("=== Système RAG prêt ===")
    print("Posez vos questions sur le document. Tapez 'quitter' pour arrêter.")
    print()

    while True:
        question = input("Question : ").strip()

        if question.lower() == "quitter":
            print("Au revoir.")
            break

        if not question:
            continue

        passages = rechercher_contexte(question, collection, modele_emb)

        print("\n--- Passages sources utilisés ---")
        for i, p in enumerate(passages, 1):
            affichage = p[:200] + "..." if len(p) > 200 else p
            print(f"  [{i}] {affichage}")
        print()

        print("--- Réponse ---")
        reponse = generer_reponse_rag(question, passages)
        print(reponse)
        print()


if __name__ == "__main__":
    main()
