# Intégration des systèmes d'IA générative — M1 LDFS

Bienvenue dans ce dépôt pédagogique conçu pour le cours de Master 1 intitulé **« Intégration des systèmes d'IA générative »**.

Ce cours s'adresse à des étudiants qui savent programmer en Python mais qui n'ont aucune connaissance préalable en intelligence artificielle. Chaque notion est expliquée depuis zéro, avec des exemples concrets et des manipulations immédiates.

---

## Ce que vous allez apprendre

A la fin de ce cours, vous serez capable de :

- Expliquer simplement ce qu'est un modèle de langage et comment il fonctionne
- Construire des prompts efficaces pour obtenir des réponses utiles et fiables
- Comparer et choisir un modèle open source adapté à un besoin
- Connecter une API de LLM dans une application Python
- Construire un système RAG pour interroger vos propres documents
- Identifier et prévenir les principaux risques liés à l'IA générative
- Concevoir et documenter un projet intégrant plusieurs de ces composants

---

## Prérequis

- Python 3.10 ou supérieur installé sur votre machine
- Connaissance des bases de Python (variables, fonctions, boucles, fichiers)
- Un compte Hugging Face (gratuit) : https://huggingface.co
- Une clé API Groq (voir section suivante)

Aucune connaissance en mathématiques, statistiques ou machine learning n'est requise.

---

## API — Groq uniquement

Ce cours utilise exclusivement l'API **Groq** (gratuit, modèles Llama et Mixtral).

| Fournisseur | Inscription | Configuration |
|-------------|-------------|----------------|
| **Groq** | https://console.groq.com | Créez un compte, générez une clé dans API Keys, ajoutez `GROQ_API_KEY` dans votre `.env` |

Le module `utils.py` à la racine du dépôt utilise automatiquement Groq.

---

## Installation

Clonez ce dépôt, puis installez les dépendances :

```bash
git clone https://github.com/AbidHamza/Int-gration-d-IA-g-n-rative-M1-LDFS.git
cd Int-gration-d-IA-g-n-rative-M1-LDFS
pip install -r requirements.txt
```

Copiez le fichier d'exemple et renseignez au moins une clé :

```bash
cp .env.example .env
```

Puis éditez `.env` avec votre clé Groq :

```
GROQ_API_KEY=gsk_votre_cle_groq_ici
HF_TOKEN=hf_votre_token_huggingface_ici
```

Vérifiez que tout fonctionne :

```bash
python utils.py
```

Vous devez voir s'afficher le fournisseur détecté et le modèle utilisé.

---

## Parcours des 8 Rooms

Le cours est organisé en 8 Rooms progressives. Chaque Room produit un résultat visible et exploitable.

| Room | Titre | Ce que vous construisez |
|------|-------|------------------------|
| 01 | Découvrir l'IA générative | Votre premier dialogue avec un LLM, observation des hallucinations |
| 02 | Construire avec des prompts | Un assistant pédagogique avec des prompts structurés |
| 03 | Explorer les modèles open source | Un tableau comparatif de 3 modèles Hugging Face |
| 04 | Connecter une API | Un mini service FastAPI interfacé avec un LLM |
| 05 | Créer un système RAG | Un assistant qui répond en citant vos documents |
| 06 | Comprendre les risques | Une grille d'audit de réponses générées |
| 07 | Projets guidés | Trois assistants thématiques complets |
| 08 | Projet final | Un système intégrant prompts, API, RAG et analyse des risques |

Commencez par la Room 01 et progressez dans l'ordre. Chaque Room suppose que les précédentes ont été complétées.

---

## Structure de chaque Room

Chaque Room contient les fichiers suivants :

```
README.md          — Objectif, résultat attendu, liste des fichiers
theory.md          — Explications des notions, avec exemples concrets
practice.md        — Exercices guidés, étape par étape
challenge.md       — Extension plus avancée pour aller plus loin
rubric.md          — Critères d'évaluation
code/              — Scripts Python commentés ligne par ligne
expected_outputs/  — Exemples de ce que vous devez obtenir
```

---

## Dossiers transverses

```
datasets/    — Fichiers de données utilisés dans les exercices
templates/   — Modèles de rapport et de livrable
solutions/   — Corrigés des exercices (à consulter après avoir essayé)
evaluation/  — Barèmes et grilles d'évaluation du cours
```

---

## Conventions de rendu

- Vos travaux doivent être remis dans un dépôt Git personnel, avec un historique de commits lisible.
- Chaque livrable doit inclure un fichier `README.md` décrivant comment l'exécuter.
- Le code doit s'exécuter sans erreur avec `pip install -r requirements.txt`.
- Les réponses aux questions d'analyse doivent être rédigées en français, en phrases complètes.

---

## Obtenir de l'aide

Si un script ne fonctionne pas, vérifiez dans l'ordre :
1. Que votre fichier `.env` est bien renseigné.
2. Que les dépendances sont installées (`pip install -r requirements.txt`).
3. Que vous utilisez Python 3.10 ou supérieur (`python --version`).
4. Le fichier `expected_outputs/` de la Room pour comparer avec votre résultat.
