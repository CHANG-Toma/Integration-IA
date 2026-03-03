# Protocole d'audit des réponses LLM avant publication

**Room 06 — Comprendre les risques**

Ce protocole en 4 étapes permet à toute personne utilisant un LLM en contexte professionnel de vérifier les réponses générées avant diffusion ou publication. Chaque étape est nommée, décrite, outillée et illustrée.

---

## Étape 1 — Vérification factuelle

### Nom
**Contrôler la véracité des affirmations**

### Description
Toute information factuelle produite par un LLM (chiffres, dates, noms, références, propriétés techniques) doit être considérée comme potentiellement erronée ou inventée (hallucination). Il faut identifier chaque affirmation vérifiable dans la réponse, puis la confronter à une source externe fiable. Aucune donnée factuelle ne doit être publiée sans cette confrontation.

### Outillage
- **Grille de vérification** : tableau listant chaque affirmation, le jugement (vraie / fausse / partiellement vraie / non vérifiable) et la source de vérification (URL, document officiel).
- **Sources à privilégier** : bases officielles (INSEE, sites institutionnels), Wikipédia pour une première vérification, moteur de recherche pour les références scientifiques ou juridiques.
- **Script ou checklist** : réutilisation d’une grille type (ex. `grille_verification_faits.txt`) pour chaque lot de réponses à auditer.

### Exemple concret
*Contexte : rédaction de fiches produit pour un site e-commerce.*

Le LLM indique qu’un matériau est « résistant jusqu’à 120 °C ». L’auditeur note cette affirmation dans la grille, consulte la fiche technique fournie par le fournisseur et constate que la limite est 100 °C. Il marque « fausse » et cite la fiche technique comme source. La fiche produit est corrigée avant publication.

---

## Étape 2 — Détection des biais

### Nom
**Repérer les stéréotypes et les biais de représentation**

### Description
Les modèles reproduisent souvent les biais présents dans leurs données d’entraînement (genre, âge, origine, métiers). Il s’agit de relire la réponse en se demandant si des stéréotypes sont véhiculés (pronoms systématiques, descriptions genrées ou culturalisées, généralisations abusives). Toute formulation qui pourrait exclure ou stigmatiser un groupe doit être identifiée et, si besoin, reformulée de manière neutre ou équilibrée.

### Outillage
- **Grille d’analyse de biais** : structure type (ex. `analyse_biais.txt`) avec rubriques « différences observées », « pronoms utilisés », « stéréotypes détectés », « reformulation neutre ».
- **Comparaison de variantes** : envoyer le même type de prompt avec des contextes variés (neutre vs. stéréotypé) et comparer les réponses (comme dans `19_tester_biais.py`).
- **Relecture ciblée** : checklist « métiers/genre », « nationalité/origine », « âge » pour ne rien laisser passer.

### Exemple concret
*Contexte : descriptions de postes générées par un LLM pour des offres d’emploi.*

Le LLM décrit le candidat idéal pour un poste d’« ingénieur logiciel » avec « il maîtrise… » et des traits associés à un profil masculin stéréotypé. L’auditeur note le biais dans la grille, coche « stéréotypes détectés : oui » et propose une reformulation neutre : « La personne retenue maîtrise… » et suppression des détails non pertinents (âge, style vestimentaire). La fiche est modifiée avant mise en ligne.

---

## Étape 3 — Protection des données personnelles

### Nom
**Vérifier l’absence de données personnelles et la conformité RGPD**

### Description
Les réponses ne doivent pas contenir de données permettant d’identifier une personne physique (nom, prénom, adresse, e-mail, numéro de téléphone, etc.), sauf si leur présence est légale et sécurisée. Il faut aussi s’assurer qu’aucune donnée personnelle n’a été envoyée au LLM sans anonymisation ou pseudonymisation, pour éviter des transferts non autorisés (ex. vers des serveurs hors UE).

### Outillage
- **Liste de contrôle** : vérification systématique des champs « nom, prénom, adresse, e-mail, téléphone, numéro de sécu, identifiants » dans les entrées envoyées au modèle et dans les sorties.
- **Anonymisation en amont** : remplacement des données identifiantes par des pseudonymes ou des placeholders avant envoi au LLM (outils de masquage ou scripts dédiés).
- **Référentiel** : rappel des règles RGPD (finalité, minimisation, transferts) et, si besoin, avis juridique ou DPO pour les usages sensibles.

### Exemple concret
*Contexte : synthèses de réunions générées à partir de comptes rendus internes.*

Un compte rendu contient les noms et e-mails des participants. Avant envoi au LLM, l’équipe remplace les noms par « Participant 1 », « Participant 2 », etc. Lors de l’audit, on vérifie que la synthèse publiée ne contient aucun nom ni e-mail. Si une version non anonymisée avait été envoyée par erreur, la synthèse serait retirée et l’incident signalé au DPO.

---

## Étape 4 — Validation humaine finale

### Nom
**Validation et responsabilité humaines avant publication**

### Description
L’IA est un outil : la responsabilité du contenu publié reste du ressort de l’humain. Une personne identifiée (rédacteur, responsable de publication, relecteur) doit valider explicitement que les étapes 1 à 3 ont été menées et que le contenu est conforme à l’usage prévu (ton, public, cadre juridique). Aucune réponse LLM ne doit être publiée ou envoyée à des tiers sans cette validation écrite ou tracée.

### Outillage
- **Checklist de validation** : case à cocher pour chaque étape (factuel, biais, données personnelles) + signature ou validation électronique (workflow, ticket, e-mail).
- **Traçabilité** : enregistrement de la date, du validateur et de la version du contenu (versioning ou historique).
- **Rôle clairement défini** : désignation d’un « responsable publication » dans la charte ou le processus métier.

### Exemple concret
*Contexte : chatbot de support client dont les réponses sont parfois reprises telles quelles sur le site.*

Avant de publier une nouvelle réponse type (FAQ), le responsable support vérifie la grille factuelle (étape 1), la grille biais (étape 2) et confirme qu’aucune donnée client n’apparaît (étape 3). Il coche la checklist « Protocole Room 06 complété » et valide dans l’outil de publication. En cas de litige, la trace permet de montrer qu’un contrôle humain a été effectué.

---

## Synthèse du protocole

| Étape | Objectif principal | Livrable type |
|-------|--------------------|----------------|
| 1. Vérification factuelle | Éviter les hallucinations | Grille remplie + sources |
| 2. Détection des biais | Éviter les stéréotypes | Grille biais + reformulations |
| 3. Données personnelles | Conformité RGPD et confidentialité | Vérification entrées/sorties, anonymisation si besoin |
| 4. Validation humaine | Responsabilité et traçabilité | Checklist validée + trace de publication |

*Ce protocole peut être intégré à une charte d’usage des LLM ou à un processus qualité existant.*
