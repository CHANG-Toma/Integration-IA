# Rapport de projet final — Intégration des systèmes d'IA générative

**Nom et prénom** : [votre nom]
**Date de remise** : [date]

---

## 1. Description du cas d'usage

### Quel problème résolvez-vous ?

Le projet met en place un assistant de recherche documentaire capable de répondre à des
questions en s’appuyant sur un rapport long (`rapport_fictif.pdf`). L’objectif est de
retrouver rapidement les passages pertinents et de formuler des réponses structurées,
tout en limitant les risques d’hallucination grâce à un pipeline RAG. Le système doit
également fournir des métriques de fonctionnement (temps de réponse, volume de texte)
pour analyser son comportement en conditions réelles.

### Qui est l'utilisateur cible ?

L’utilisateur cible est une personne qui doit explorer rapidement un document volumineux :
par exemple un chef de projet, un étudiant ou un consultant qui souhaite extraire les
informations clés sans lire tout le rapport manuellement. Il ne s’agit pas nécessairement
d’un profil technique ; l’interface est une simple ligne de commande avec des questions
en langage naturel.

### Quel est le résultat attendu ?

Après utilisation, l’utilisateur obtient :
- des réponses rédigées en français, étayées par les passages du rapport ;
- une indication claire lorsque l’information n’est pas présente dans le document ;
- un journal de session et un rapport d’utilisation qui permettent d’analyser la charge
  et les performances de l’assistant.

---

## 2. Architecture du système

### Schéma du flux de données

```
Entrée utilisateur (question texte)
        ↓
Chargement de l'index ChromaDB (segments du rapport)
        ↓
Encodage de la question en vecteur (SentenceTransformer)
        ↓
Recherche des segments les plus pertinents (ChromaDB)
        ↓
Construction du prompt (rôle système + contexte + question)
        ↓
Appel au modèle Groq (llama-3.1-8b-instant)
        ↓
Réponse structurée renvoyée à l'utilisateur
        ↓
Logging dans journal_sessions.csv + mise à jour du rapport d'utilisation
```

### Composants principaux

| Composant | Rôle | Fichier Python |
|-----------|------|----------------|
| Indexation du corpus | Charger le PDF, découper le texte et créer l’index vectoriel dans ChromaDB | `code/indexation_corpus.py` |
| Assistant RAG | Interagir avec l’utilisateur, rechercher les passages pertinents et générer une réponse contextualisée via le LLM | `code/assistant_recherche_documentaire.py` |
| Logging et rapport | Enregistrer chaque interaction dans un CSV et produire un rapport d’utilisation synthétique | Intégré dans `code/assistant_recherche_documentaire.py` |

---

## 3. Choix techniques

### Modèle utilisé

- Nom du modèle : llama-3.1-8b-instant (via l’API Groq, voir `utils.py`)
- Justification : modèle relativement léger et rapide, adapté à un usage interactif en
  ligne de commande, avec un coût en tokens raisonnable. L’intégration est simplifiée
  par l’API Groq déjà utilisée dans les rooms précédentes.

### Base vectorielle

- Outil utilisé : ChromaDB (client Python, base locale)
- Justification : solution simple à mettre en place pour des petits projets éducatifs,
  avec une API haut niveau (`get_or_create_collection`, `query`) déjà introduite dans
  la Room 05. Une base locale suffit pour ce cas d’usage.

### Stratégie de prompt

Les prompts sont structurés de la façon suivante :
- **Rôle système** : assistant de recherche documentaire qui doit se limiter strictement
  aux extraits fournis.
- **Contexte** : concaténation des segments renvoyés par ChromaDB, séparés par `---`.
- **Instruction** : demander explicitement au modèle de répondre uniquement à partir des
  extraits, de citer les passages pertinents et de signaler lorsque l’information manque.

Cette stratégie vise à réduire les hallucinations et à encourager le modèle à expliciter
ses sources dans le texte.

---

## 4. Analyse des risques

| Risque identifié | Gravité (1-5) | Mesure de mitigation |
|------------------|---------------|---------------------|
| Hallucination (le modèle invente des informations qui ne figurent pas dans le rapport) | 4 | Prompt explicite demandant de répondre uniquement à partir des extraits, avec mention claire lorsque l’information n’est pas disponible. Utilisation d’une température faible. |
| Biais ou lacunes du document source | 3 | Rappel dans le rapport que le corpus est fictif et que les réponses ne doivent pas être généralisées sans validation humaine. L’utilisateur est encouragé à vérifier les passages cités dans le PDF. |
| Exposition de données sensibles si le système était appliqué à de vrais documents | 5 | Dans ce projet, seul un rapport fictif local est utilisé. Pour un déploiement réel, il faudrait ajouter des contrôles d’accès, de l’anonymisation et une gouvernance claire des données. |
| Mauvaise interprétation des métriques de logging (temps, tokens estimés) | 2 | Le rapport d’utilisation indique explicitement qu’il s’agit d’estimations approximatives et non de métriques de facturation officielles. |

---

## 5. Résultats et démonstration

### Résultats obtenus

- L’assistant est capable de retrouver les principaux objectifs du rapport et de les
  reformuler de manière synthétique.
- Il identifie correctement les indicateurs de suivi mentionnés dans le document et les
  restitue sous forme de liste.
- Lorsqu’on lui pose une question hors sujet (par exemple sur la météo), il signale que
  l’information n’est pas présente dans le rapport au lieu d’inventer une réponse.
- Les interactions et les temps de réponse sont journalisés dans `code/logs/journal_sessions.csv`.

Des exemples concrets de session (incluant un cas limite) sont fournis dans
`ROOMS/08_Projet_Final/expected_outputs/demo.txt`.

### Limites observées

- L’approximation du nombre de tokens à partir du nombre de mots reste grossière et peut
  s’éloigner des valeurs réelles.
- La qualité des réponses dépend fortement de la qualité du découpage en segments et de
  la pertinence de la recherche vectorielle.
- Le système ne gère pas encore la mise à jour dynamique du corpus (il faudrait relancer
  l’indexation en cas de nouveau document).

---

## 6. Conclusion et pistes d'amélioration

Ce projet montre comment combiner un pipeline RAG simple avec un modèle de langage pour
construire un assistant de recherche documentaire utilisable en pratique. Le travail sur
les prompts et la contrainte de s’appuyer uniquement sur les extraits permet de limiter
les hallucinations. L’ajout du logging et du rapport d’utilisation donne une première
visibilité sur le comportement du système.

Avec plus de temps, il serait intéressant d’ajouter une interface web (par exemple avec
Streamlit), de gérer plusieurs documents et de mettre en place une évaluation automatique
de la qualité des réponses sur un petit jeu de questions de référence.

---

## 7. Extension — Logging et monitoring

Pour répondre au challenge de la Room 08, une extension de logging et de monitoring a été
intégrée à l’assistant :

- **Journalisation détaillée** : chaque interaction est enregistrée dans
  `code/logs/journal_sessions.csv` avec la question, la longueur de la réponse, le nombre
  de passages de contexte utilisés, le temps de réponse et une estimation du nombre de
  tokens.
- **Rapport d’utilisation** : la commande `rapport` dans l’interface génère un résumé des
  métriques (nombre de requêtes, temps moyen, min/max, tokens moyens) et l’enregistre
  dans `code/logs/rapport_utilisation.txt`.
- **Transparence** : le rapport précise que les tokens sont estimés et ne doivent pas être
  confondus avec les métriques de facturation.

Cette extension permet de mieux comprendre le comportement du système et d’ouvrir la voie
à une supervision plus avancée (alertes, suivi dans le temps, comparaison entre versions).

---

## Annexes

- Fichier de démonstration : `ROOMS/08_Projet_Final/expected_outputs/demo.txt`
- Architecture détaillée : `ROOMS/08_Projet_Final/code/architecture.md`
- Dépendances : `ROOMS/08_Projet_Final/code/requirements.txt`

