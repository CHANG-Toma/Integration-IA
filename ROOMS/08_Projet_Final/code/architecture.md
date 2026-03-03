## Projet final — Assistant de recherche documentaire (RAG + logging)

### 1. Entrées du système

- **Questions utilisateur** : texte libre saisi dans le terminal (français).
- **Corpus documentaire** : fichier `datasets/rapport_fictif.pdf` fourni dans le dépôt (rapport long servant de base de connaissances).
- **Commandes spéciales** :
  - `quitter` : arrêter le programme.
  - `rapport` : générer et afficher un rapport d’utilisation à partir des logs.

### 2. Composants principaux

- **Chargement & découpage du corpus (`indexation_corpus.py`)**
  - Charge le PDF avec PyMuPDF (`fitz`).
  - Découpe le texte en segments de taille fixe avec chevauchement pour éviter de perdre de l’information.

- **Indexation vectorielle (`indexation_corpus.py`)**
  - Transforme chaque segment en vecteur via `SentenceTransformer("all-MiniLM-L6-v2")`.
  - Stocke les vecteurs et les segments dans une collection ChromaDB (`assistant_recherche_doc`).

- **Recherche de contexte pertinent (`assistant_recherche_documentaire.py`)**
  - Encode la question de l’utilisateur en vecteur.
  - Interroge la collection ChromaDB pour récupérer les `n` segments les plus proches.

- **Génération de réponse via API Groq (`assistant_recherche_documentaire.py`)**
  - Construit un prompt structuré :
    - Rôle système : assistant de recherche documentaire qui ne répond qu’à partir des documents.
    - Contexte : passages retrouvés par la recherche vectorielle.
    - Instruction : répondre de façon structurée, citer les passages utilisés et dire clairement quand l’information manque.
  - Appelle le modèle `llama-3.1-8b-instant` via le client Groq défini dans `utils.py`.

- **Logging & monitoring (`assistant_recherche_documentaire.py`)**
  - Mesure le **temps de réponse** pour chaque question.
  - Estime le **nombre de tokens** à partir de la longueur des textes (approximation par nombre de mots).
  - Enregistre dans `code/logs/journal_sessions.csv` :
    - Date/heure
    - Question
    - Longueur de la réponse
    - Nombre de passages de contexte utilisés
    - Temps de réponse (secondes)
    - Nombre de tokens estimés
  - Permet de générer un rapport d’utilisation synthétique (`rapport` dans le terminal) écrit aussi dans `code/logs/rapport_utilisation.txt`.

### 3. Flux de données (schéma texte)

```
Utilisateur (question texte)
        ↓
Assistant (script principal)
        ↓
Recherche de contexte (ChromaDB + SentenceTransformer)
        ↓
Construction du prompt (contexte + question + contraintes)
        ↓
Appel API Groq (LLM : llama-3.1-8b-instant)
        ↓
Réponse structurée avec citations de passages
        ↓
Logging (CSV) + mise à jour du rapport d’utilisation
        ↓
Affichage de la réponse dans le terminal
```

### 4. Sorties du système

- **Pour l’utilisateur final** :
  - Réponse rédigée en français, structurée, en s’appuyant sur les passages les plus pertinents du rapport.
  - Mention explicite lorsque la réponse ne peut pas être déduite du document.
  - Affichage des passages contextuels utilisés (aperçu tronqué) pour transparence.

- **Pour l’analyse du système** :
  - Fichier de logs `code/logs/journal_sessions.csv` (historique détaillé des requêtes).
  - Fichier `code/logs/rapport_utilisation.txt` (statistiques agrégées : nombre de requêtes, temps moyen, tokens estimés, etc.).

### 5. Risques identifiés (vue synthétique)

- **Hallucination / répond au-delà des documents**
  - Mitigation : prompt explicite demandant de répondre *uniquement* à partir des passages fournis et de dire quand l’information n’est pas disponible.

- **Biais du corpus**
  - Mitigation : le rapport source est présenté comme un exemple fictif ; le rapport final rappelle que les conclusions ne doivent pas être généralisées sans validation humaine.

- **Données sensibles / mauvaise utilisation**
  - Mitigation : le système n’accepte que des questions textuelles et répond à partir d’un corpus fixe (rapport fictif) stocké localement. Rappel dans le rapport final que ce type de système ne doit pas être utilisé sans revue humaine sur des données sensibles réelles.

