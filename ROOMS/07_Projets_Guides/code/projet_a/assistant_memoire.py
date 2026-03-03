# Projet A — Assistant mémoire avec historique de conversation
# Room 07 — Projets guidés

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()

MESSAGE_SYSTEME = {
    "role": "system",
    "content": (
        "Tu es un assistant pédagogique bienveillant et patient. "
        "Tu expliques les concepts de façon simple, avec des exemples concrets. "
        "Tu te souviens de ce que l'utilisateur a dit précédemment dans la conversation."
    )
}

historique = [MESSAGE_SYSTEME]
MAX_ECHANGES = 10


def ajouter_au_contexte(role, contenu):
    """
    Ajoute un message à l'historique et limite la taille de l'historique.

    A COMPLETER :
    - Ajouter le nouveau message à la fin de l'historique
    - Si le nombre de messages (hors message system) dépasse MAX_ECHANGES * 2,
      supprimer les 2 messages les plus anciens (après le message system)

    Version challenge :
    - Quand la limite est dépassée, au lieu de simplement supprimer les
      anciens messages, demander au LLM de résumer les 5 premiers échanges
      (10 messages) et injecter ce résumé au début de l'historique.
    """
    # Ajout du nouveau message à l'historique
    historique.append({"role": role, "content": contenu})

    # Nombre de messages hors message système
    nb_messages_sans_systeme = len(historique) - 1

    # Si on ne dépasse pas la limite de 10 échanges, on ne fait rien de plus
    if nb_messages_sans_systeme <= MAX_ECHANGES * 2:
        return

    # --- Extension challenge : résumé automatique des 5 premiers échanges ---
    # On prend les 5 premiers échanges complets (10 messages) après le message système
    # s'ils existent, sinon on revient au comportement simple de suppression.
    if nb_messages_sans_systeme >= 10:
        # Messages correspondant aux 5 premiers échanges détaillés
        premiers_messages = historique[1:11]  # indices 1 à 10 inclus

        # On construit un texte "brut" résumant ces échanges pour le LLM
        texte_conversation = []
        for msg in premiers_messages:
            texte_conversation.append(f"{msg['role']}: {msg['content']}")
        texte_conversation_str = "\n".join(texte_conversation)

        try:
            resume_completion = client.chat.completions.create(
                model=MODELE,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Tu es un assistant qui résume une conversation "
                            "entre un utilisateur et un assistant pédagogique. "
                            "Produis un résumé bref (5 à 8 phrases) en français, "
                            "conservant les informations utiles pour la suite "
                            "de la conversation."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Voici les 5 premiers échanges de la conversation. "
                            "Résume-les en un seul texte qui pourra servir de mémoire longue :\n\n"
                            f"{texte_conversation_str}"
                        ),
                    },
                ],
            )

            resume_texte = (
                resume_completion.choices[0].message.content.strip()
                if resume_completion.choices
                else ""
            )
        except Exception as e:  # pragma: no cover - comportement de secours
            print(f"[Erreur résumé] {e}")
            resume_texte = ""

        # Si le résumé a réussi, on reconstruit l'historique :
        # - message système
        # - message de résumé
        # - le reste de l'historique après les 5 premiers échanges
        if resume_texte:
            message_resume = {
                "role": "system",
                "content": (
                    "Résumé des 5 premiers échanges de la conversation :\n"
                    f"{resume_texte}"
                ),
            }
            reste_historique = historique[11:]
            historique[:] = [MESSAGE_SYSTEME, message_resume] + reste_historique
        else:
            # Comportement de secours : on supprime simplement les 2 messages
            # les plus anciens après le message système (ancienne règle).
            if len(historique) > 3:
                del historique[1:3]
    else:
        # Pas assez de messages pour faire un vrai résumé : on applique
        # le comportement simple de suppression.
        if len(historique) > 3:
            del historique[1:3]


def envoyer_message(texte_utilisateur):
    """
    Envoie le message de l'utilisateur au LLM avec l'historique complet
    et retourne la réponse.

    A COMPLETER :
    1. Ajouter le message utilisateur à l'historique
    2. Envoyer l'historique complet au LLM (model=MODELE)
    3. Récupérer la réponse
    4. Ajouter la réponse de l'assistant à l'historique
    5. Retourner le texte de la réponse
    """
    # 1. On ajoute le message utilisateur
    ajouter_au_contexte("user", texte_utilisateur)

    try:
        # 2. On envoie l'historique complet au modèle
        completion = client.chat.completions.create(
            model=MODELE,
            messages=historique,
        )
    except Exception as e:  # pragma: no cover - pour la robustesse en runtime
        print(f"[Erreur appel API] {e}")
        return None

    # 3. On récupère le texte de réponse
    try:
        texte_reponse = completion.choices[0].message.content.strip()
    except (AttributeError, IndexError, KeyError):
        print("[Erreur] Réponse du modèle inattendue.")
        return None

    # 4. On ajoute la réponse de l'assistant à l'historique
    ajouter_au_contexte("assistant", texte_reponse)

    # 5. On retourne le texte de la réponse
    return texte_reponse


# --- Programme principal ---
print("=== Assistant mémoire ===")
print("Posez vos questions. L'assistant se souvient de la conversation.")
print("Tapez 'quitter' pour arrêter.")
print("Tapez 'historique' pour voir les messages en mémoire.")
print()

while True:
    texte = input("Vous : ").strip()

    if texte.lower() == "quitter":
        print("Au revoir.")
        break

    if texte.lower() == "historique":
        print(f"\n--- Historique ({len(historique)} messages) ---")
        for msg in historique:
            role = msg["role"].upper()
            contenu = msg["content"][:80]
            print(f"  [{role}] {contenu}...")
        print()
        continue

    if not texte:
        continue

    reponse = envoyer_message(texte)
    if reponse:
        print(f"\nAssistant : {reponse}\n")
