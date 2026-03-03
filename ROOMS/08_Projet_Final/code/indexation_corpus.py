"""
Script d'indexation du corpus documentaire pour l'assistant de recherche.

Ce script charge le PDF `datasets/rapport_fictif.pdf`, le découpe en segments
et crée un index vectoriel dans une collection ChromaDB nommée
`assistant_recherche_doc`.
"""

import os

import chromadb
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer


def charger_pdf(chemin: str) -> str:
    document = fitz.open(chemin)
    texte = ""
    for page in document:
        texte += page.get_text() + "\n"
    document.close()
    return texte


def decouper_en_segments(texte: str, taille_segment: int = 300, chevauchement: int = 50):
    mots = texte.split()
    segments = []
    debut = 0
    while debut < len(mots):
        fin = debut + taille_segment
        segment = " ".join(mots[debut:fin])
        segments.append(segment)
        debut += taille_segment - chevauchement
    return segments


def construire_index(segments, modele_embedding, nom_collection: str = "assistant_recherche_doc"):
    embeddings = modele_embedding.encode(segments)
    client_chroma = chromadb.Client()
    collection = client_chroma.get_or_create_collection(name=nom_collection)

    collection.add(
        documents=segments,
        embeddings=[emb.tolist() for emb in embeddings],
        ids=[f"seg_{i}" for i in range(len(segments))],
    )

    return collection


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    chemin_pdf = os.path.join(base_dir, "..", "..", "..", "datasets", "rapport_fictif.pdf")

    print("=== Indexation du corpus documentaire ===")
    print(f"Chargement du document : {chemin_pdf}")
    texte = charger_pdf(chemin_pdf)
    segments = decouper_en_segments(texte)
    print(f"Texte chargé, {len(texte.split())} mots, {len(segments)} segments générés.")
    print()

    print("Chargement du modèle d'embedding (all-MiniLM-L6-v2)...")
    modele_emb = SentenceTransformer("all-MiniLM-L6-v2")
    print("Modèle d'embedding prêt.")
    print()

    print("Création de l'index vectoriel dans ChromaDB (collection 'assistant_recherche_doc')...")
    collection = construire_index(segments, modele_emb, nom_collection="assistant_recherche_doc")
    print(f"Indexation terminée : {collection.count()} segments stockés.")
    print("Vous pouvez maintenant lancer `assistant_recherche_documentaire.py` pour poser vos questions.")

