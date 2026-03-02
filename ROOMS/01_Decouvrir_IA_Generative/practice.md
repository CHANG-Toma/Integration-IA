# Practice — Room 01 : Découvrir l'IA générative

## Objectif de cette pratique

Envoyer des prompts à un LLM, observer ses réponses, identifier des hallucinations et mesurer l'effet de la température. Chaque étape produit une sortie visible dans le terminal.

## Avant de commencer

Vérifiez que votre environnement est prêt :

```bash
python --version          # doit afficher Python 3.10 ou supérieur
python -c "import openai"  # ne doit pas afficher d'erreur (utilisé pour l'API xAI)
```

Vérifiez que votre fichier `.env` à la racine du dépôt contient :
```
GROQ_API_KEY=gsk_votre_cle_groq_ici
```

---

## Etape 1 — Premier contact avec un LLM

Ouvrez le fichier `code/01_premier_prompt.py` et lisez-le entièrement avant de l'exécuter.

Exécutez-le :

```bash
python code/01_premier_prompt.py
```

Vous devez voir une réponse s'afficher dans le terminal.

**Ce que vous observez** : le modèle répond à votre question. La réponse peut varier légèrement d'une exécution à l'autre (si la température n'est pas à 0).

**A noter** : copiez la réponse obtenue dans `expected_outputs/tableau_observations.txt` à la ligne "Etape 1".

---

## Etape 2 — Provoquer une hallucination

Modifiez le prompt dans `code/01_premier_prompt.py` pour poser une question sur un auteur ou un événement fictif. Par exemple :

```python
prompt = "Qui est l'auteur du roman 'Le Voyage des Ombres Silencieuses' publié en 1934 ?"
```

Ré-exécutez le script. Le modèle va probablement inventer un auteur et une biographie.

**Ce que vous observez** : une hallucination. Le modèle génère une réponse plausible mais fausse.

**A noter** : consignez cette réponse dans `expected_outputs/tableau_observations.txt` à la ligne "Etape 2 — hallucination".

---

## Etape 3 — Comparer deux questions factuelles

Modifiez le prompt deux fois et notez les réponses :

- Prompt A : "Quelle est la capitale de l'Australie ?"
- Prompt B : "Quelle est la capitale de l'Australie ? Réponds en une seule phrase."

**Question à vous poser** : la réponse change-t-elle selon la formulation ? Pourquoi ?

Notez vos observations dans `expected_outputs/tableau_observations.txt` à la ligne "Etape 3".

---

## Etape 4 — Observer l'effet de la température

Ouvrez le fichier `code/02_comparer_temperatures.py` et lisez-le entièrement.

Exécutez-le :

```bash
python code/02_comparer_temperatures.py
```

Le script envoie le même prompt deux fois : une fois avec une température de 0 et une fois avec une température de 0.9. Les deux réponses s'affichent côte à côte.

**Ce que vous observez** :
- A température 0, la réponse est toujours identique si vous ré-exécutez le script.
- A température 0.9, la réponse change à chaque exécution.

Ré-exécutez le script 3 fois et notez si les réponses varient dans `expected_outputs/tableau_observations.txt` à la ligne "Etape 4".

---

## Etape 5 — Remplir le tableau d'observations

Ouvrez `expected_outputs/tableau_observations.txt`. Complétez toutes les lignes avec vos résultats des étapes précédentes.

Le tableau attend :
- Le prompt utilisé
- La réponse obtenue (résumée en 1-2 phrases)
- Votre jugement : réponse correcte / incorrecte / impossible à vérifier

---

## Etape 6 — Analyse réflexive

Sur votre éditeur de texte, rédigez 3 phrases qui répondent à ces questions :

1. Pourquoi le modèle peut-il affirmer quelque chose de faux sans le savoir ?
2. Dans quel contexte professionnel l'hallucination serait-elle dangereuse ?
3. Quelle précaution simple pourriez-vous prendre pour réduire ce risque ?

Enregistrez ce texte dans `expected_outputs/analyse_room01.txt`.

---

## Vérification finale

Avant de passer à la Room 02, vérifiez que vous avez :

- [ ] Exécuté `01_premier_prompt.py` avec succès
- [ ] Observé au moins une hallucination
- [ ] Exécuté `02_comparer_temperatures.py` et noté les différences
- [ ] Complété `expected_outputs/tableau_observations.txt`
- [ ] Rédigé l'analyse réflexive dans `expected_outputs/analyse_room01.txt`
