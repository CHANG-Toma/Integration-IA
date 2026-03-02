# Script 02 — Comparer les réponses d'un LLM à deux températures différentes
# Room 01 — Découvrir l'IA générative

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE

# Création du client (Groq)
client = creer_client()

# Le prompt utilisé pour les deux comparaisons
prompt = "Décris en quelques phrases comment fonctionne la photosynthèse."


def interroger_modele(prompt_texte, temperature_valeur):
    """
    Envoie un prompt au modèle et retourne le texte de la réponse.

    prompt_texte      : la question à poser (chaîne de caractères)
    temperature_valeur: la température souhaitée (nombre entre 0 et 1)
    """
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "user", "content": prompt_texte}
        ],
        temperature=temperature_valeur,
        max_tokens=300
    )
    return reponse.choices[0].message.content


# Affichage du prompt envoyé
print("=== Prompt utilisé pour les deux tests ===")
print(prompt)
print()

# Premier appel avec température 0 (réponses stables et précises)
print("=== Réponse avec température 0 (déterministe) ===")
reponse_t0 = interroger_modele(prompt, temperature_valeur=0)
print(reponse_t0)
print()

# Deuxième appel avec température 0.9 (réponses plus variées et créatives)
print("=== Réponse avec température 0.9 (créative) ===")
reponse_t09 = interroger_modele(prompt, temperature_valeur=0.9)
print(reponse_t09)
print()

# Comparaison simple
if reponse_t0.strip() == reponse_t09.strip():
    print("Les deux réponses sont identiques.")
else:
    print("Les deux réponses sont différentes.")
    print("Relancez ce script plusieurs fois pour observer la variabilité à température 0.9.")
