# Challenge Room 02 — Générateur de quiz en JSON
# Room 02 — Construire avec des prompts

import io
import json
import os
import re
import sys

# Permet l'affichage correct des accents sur Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from utils import creer_client, MODELE

MAX_TENTATIVES = 3


# Permet de charger le prompt depuis le fichier et de remplacer le placeholder par le sujet.
def charger_prompt(sujet):
    """Charge le prompt depuis le fichier et remplace le placeholder par le sujet."""
    chemin_prompt = os.path.join(os.path.dirname(__file__), "challenge_room02_prompt.txt")
    with open(chemin_prompt, "r", encoding="utf-8") as f:
        contenu = f.read()
    return contenu.replace("{{SUJET}}", sujet)


# Permet d'extraire le JSON brut de la réponse.
def extraire_json_brut(texte):
    """
    Tente d'extraire du JSON depuis une réponse qui pourrait contenir du markdown
    ou du texte avant/après (ex: ```json ... ```).
    """
    texte = texte.strip()
    # Supprimer les éventuels blocs markdown
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", texte)
    if match:
        return match.group(1).strip()
    return texte


# Permet de générer un quiz en fonction du sujet.
def generer_quiz(client, sujet):
    """Envoie le prompt au LLM et retourne la réponse brute."""
    prompt = charger_prompt(sujet)
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000,
    )
    return reponse.choices[0].message.content


# Permet de parser le texte en JSON et de valider la structure du quiz.
def parser_quiz(texte):
    """Parse le texte en JSON et valide la structure du quiz."""
    brut = extraire_json_brut(texte)
    data = json.loads(brut)

    if "sujet" not in data or "questions" not in data:
        raise ValueError("Structure invalide : 'sujet' et 'questions' sont requis.")

    if not isinstance(data["questions"], list) or len(data["questions"]) != 5:
        raise ValueError("Le tableau 'questions' doit contenir exactement 5 éléments.")

    for i, q in enumerate(data["questions"]):
        if not all(k in q for k in ("numero", "question", "options", "bonne_reponse")):
            raise ValueError(f"Question {i + 1} : clés manquantes (numero, question, options, bonne_reponse).")
        if len(q["options"]) != 4:
            raise ValueError(f"Question {q['numero']} : 4 options requises.")

    return data


# Permet d'afficher le quiz.
def afficher_quiz(quiz):
    """Affiche chaque question avec ses options et révèle la bonne réponse."""
    print(f"\nQuiz : {quiz['sujet']}\n")
    print("=" * 60)

    for q in quiz["questions"]:
        print(f"\nQuestion {q['numero']} : {q['question']}\n")
        for opt in q["options"]:
            print(f"  {opt}")
        print(f"\n  >> Bonne réponse : {q['bonne_reponse']}")
        print("-" * 60)


# Permet de lancer le script.
def main():
    if len(sys.argv) < 2:
        print("Usage : python challenge_room02.py <sujet>")
        print("Exemple : python challenge_room02.py \"l'histoire de France\"")
        sys.exit(1)

    sujet = " ".join(sys.argv[1:]).strip()
    if not sujet:
        print("Erreur : veuillez fournir un sujet.")
        sys.exit(1)

    print(f"Génération d'un quiz sur : {sujet}\n")
    client = creer_client()

    for tentative in range(1, MAX_TENTATIVES + 1):
        try:
            texte_brut = generer_quiz(client, sujet)
            quiz = parser_quiz(texte_brut)
            afficher_quiz(quiz)
            return
        except json.JSONDecodeError as e:
            print(f"Erreur (tentative {tentative}/{MAX_TENTATIVES}) :")
            print(f"  Le modèle n'a pas retourné du JSON valide.")
            print(f"  Détail : {e}")
        except ValueError as e:
            print(f"Erreur (tentative {tentative}/{MAX_TENTATIVES}) :")
            print(f"  {e}")

        if tentative < MAX_TENTATIVES:
            print("\nNouvelle tentative...\n")
        else:
            print("\nÉchec après 3 tentatives. Impossible d'obtenir un quiz valide.")
            sys.exit(1)


if __name__ == "__main__":
    main()
