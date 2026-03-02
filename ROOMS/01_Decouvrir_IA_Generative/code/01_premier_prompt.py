# Script 01 — Envoyer un premier prompt à un LLM et afficher la réponse brute
# Room 01 — Découvrir l'IA générative

# On ajoute le dossier racine du projet au chemin pour pouvoir importer utils.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Importation du module utilitaire qui détecte automatiquement l'API gratuite
from utils import creer_client, MODELE

# Création du client (Groq via votre .env)
client = creer_client()

# Définition du prompt : c'est la question ou instruction envoyée au modèle
prompt = "Qui a écrit le roman Les Fleurs du Mal ?"

# Affichage du prompt pour que l'étudiant sache ce qui est envoyé
print("=== Prompt envoyé ===")
print(prompt)
print()

# Appel à l'API pour générer une réponse
# model : le modèle est choisi automatiquement selon l'API détectée
# messages : la liste des messages de la conversation
#   - role "user" : c'est nous qui parlons
#   - content : le texte de notre message
# temperature : 0 = réponses déterministes et précises
# max_tokens : limite la longueur de la réponse
reponse = client.chat.completions.create(
    model=MODELE,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0,
    max_tokens=200
)

# Extraction du texte de la réponse
# La réponse est un objet structuré ; le texte est dans choices[0].message.content
texte_reponse = reponse.choices[0].message.content

# Affichage de la réponse dans le terminal
print("=== Réponse du modèle ===")
print(texte_reponse)
print()

# Affichage des métadonnées pour comprendre le coût de l'échange
# prompt_tokens : tokens utilisés pour notre question
# completion_tokens : tokens utilisés pour la réponse
# total_tokens : total
if reponse.usage:
    print("=== Informations sur l'échange ===")
    print(f"Tokens pour le prompt  : {reponse.usage.prompt_tokens}")
    print(f"Tokens pour la réponse : {reponse.usage.completion_tokens}")
    print(f"Total de tokens        : {reponse.usage.total_tokens}")
