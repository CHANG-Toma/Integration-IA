# Room 01 — Découvrir l'IA générative


## Objectif

Comprendre ce qu'est réellement un modèle de langage (LLM), sans mathématiques complexes.
A la fin de cette Room, vous saurez expliquer pourquoi un modèle peut se tromper, comment il produit du texte, et vous aurez observé ce comportement en direct avec Python.

## Résultat attendu

Vous obtiendrez en sortie :
- Des réponses affichées dans le terminal à vos propres prompts
- Une comparaison côte à côte de deux réponses avec des températures différentes
- Un tableau d'observations rempli décrivant des cas d'hallucinations détectées

## Fichiers de cette Room

| Fichier | Contenu |
|---------|---------|
| `theory.md` | Explication des notions : LLM, token, prédiction, hallucination, température |
| `practice.md` | 6 étapes guidées pour tester et observer un LLM en Python |
| `challenge.md` | Trouver des prompts qui font systématiquement halluciner le modèle |
| `rubric.md` | Critères d'évaluation de cette Room |
| `code/01_premier_prompt.py` | Envoyer un premier prompt et afficher la réponse brute |
| `code/02_comparer_temperatures.py` | Comparer une réponse à température 0 vs 0.9 |
| `expected_outputs/exemple_reponse.txt` | Exemple de sortie attendue pour le script 01 |
| `expected_outputs/tableau_observations.txt` | Gabarit de tableau à compléter |

## Avant de commencer

Assurez-vous d'avoir suivi les instructions d'installation du README principal.
Votre fichier `.env` doit contenir une clé API valide.
