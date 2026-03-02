# Challenge Room 03 — Comparaison des modèles sur le résumé de texte

**Texte source :** `datasets/texte_entreprise.txt` (document stratégie TechVision SAS)  
**Prompt :** « Résume ce texte en 5 phrases claires et concises. »  
**API utilisée :** Groq (Llama-3.1-8B, Llama-3.3-70B, GPT-OSS-20B)

Pour regénérer : `python ROOMS\03_Explorer_les_Modeles_Open_Source\code\challenge_room03_resumes.py` (depuis la racine du projet)

---

## Les 3 résumés produits

### Llama-3.1-8B (rapide) — 0,7 s

Voici un résumé du texte en 5 phrases claires et concises :

- TechVision SAS est une entreprise française fondée en 2018, spécialisée dans le développement de solutions logicielles pour le secteur de la santé, avec 120 collaborateurs et un chiffre d'affaires annuel de 8,5 millions d'euros en 2024.
- L'objectif principal pour 2025 est d'augmenter le chiffre d'affaires de 15 % pour atteindre 9,8 millions d'euros, en développant le produit phare MedTrack vers le marché européen et en renforçant l'équipe commerciale.
- Trois risques majeurs ont été identifiés, notamment la dépendance au fournisseur cloud Amazon Web Services (AWS), la pénurie de développeurs seniors sur le marché français et les nouvelles obligations de conformité réglementaires liées à l'entrée en vigueur du règlement européen sur l'IA (AI Act).
- L'entreprise est organisée en quatre départements : Recherche et Développement, Commercial, Support Client et Administration, avec des méthodologies et des processus spécifiques à chaque département.
- Trois projets majeurs sont en cours de développement, notamment le projet MedTrack v3.0, le projet DataBridge et le projet SecureHealth, avec un budget total alloué de 2,1 millions d'euros.

### Llama-3.3-70B (puissant) — 1,0 s

Voici un résumé du texte en 5 phrases claires et concises :

TechVision SAS est une entreprise française spécialisée dans le développement de solutions logicielles pour le secteur de la santé, employant 120 collaborateurs et réalisant un chiffre d'affaires annuel de 8,5 millions d'euros en 2024. L'entreprise a fixé pour objectif d'augmenter son chiffre d'affaires de 15 % en 2025, en développant son produit phare MedTrack sur le marché européen, en renforçant son équipe commerciale et en améliorant la satisfaction client. Trois risques majeurs ont été identifiés, notamment la dépendance au fournisseur cloud Amazon Web Services, la pénurie de développeurs seniors et les nouvelles obligations de conformité liées au règlement européen sur l'IA. L'entreprise est organisée en quatre départements et utilise des méthodologies agiles pour développer ses produits, avec un taux de résolution au premier contact de 72 % pour le support client. Trois projets majeurs sont en cours de développement, dont le projet MedTrack v3.0, qui introduit un module d'intelligence artificielle pour la prédiction des réadmissions hospitalières, avec un budget total alloué de 2,1 millions d'euros.

### GPT-OSS-20B — 0,4 s

TechVision SAS, fondée en 2018, développe des logiciels de santé et compte 120 employés répartis entre Lyon et Nantes, avec un chiffre d'affaires de 8,5 M € en 2024. En 2025, l'entreprise vise une hausse de 15 % de son chiffre d'affaires (9,8 M €) grâce à l'expansion de son produit MedTrack en Europe, à l'embauche de 8 commerciaux spécialisés et à l'amélioration du NPS de 42 à 55. Les principaux risques identifiés sont la dépendance à AWS (migration vers OVHcloud prévue), la pénurie de développeurs seniors et les exigences de conformité de l'AI Act. L'organisation se compose de quatre départements (R&D, Commercial, Support Client, Administration) dirigés par des responsables et fonctionnant selon une méthodologie agile. Trois projets majeurs (MedTrack v3.0, DataBridge, SecureHealth) sont en cours, avec un budget total de 2,1 M € et des livraisons prévues pour juin 2025.

---

## Tableau comparatif enrichi

| Critère | Llama-3.1-8B (rapide) | Llama-3.3-70B (puissant) | GPT-OSS-20B |
|--------|------------------------|---------------------------|-------------|
| **Fidélité** | Très bonne : chiffres exacts, trois axes, trois risques, trois projets. | Très bonne : idées principales présentes + taux 72 %, module IA. | Excellente : Lyon, Nantes, OVHcloud, NPS 42→55, 8 commerciaux, juin 2025. |
| **Concision** | 5 phrases (format puces). | 5 phrases en paragraphe continu. | 5 phrases, très dense. |
| **Lisibilité** | Claire, structurée en puces. | Fluide, bien enchaînée. | Très dense, style télégraphique. |
| **Informations manquantes** | Quelques détails (Lyon/Nantes, OVHcloud, NPS). | Peu : pas Lyon/Nantes, pas OVHcloud. | Aucune : lieux, OVHcloud, NPS, budget, date livraison. |

---

## Conclusion

Pour une tâche de résumé en 5 phrases sur un document d'entreprise structuré, **GPT-OSS-20B** est le plus adapté : il combine la meilleure fidélité au texte source (lieux, chiffres précis, NPS, OVHcloud, dates) avec un temps de réponse très court (0,4 s). **Llama-3.3-70B** offre une bonne qualité et une excellente lisibilité ; son résumé est fluide et inclut des éléments comme le taux de résolution au premier contact. **Llama-3.1-8B** respecte bien la contrainte et reste lisible grâce aux puces, mais omet quelques détails. En pratique, GPT-OSS-20B convient le mieux pour un résumé exécutif professionnel ; Llama-3.3-70B pour un résumé plus narratif ; Llama-3.1-8B pour un aperçu rapide et structuré.
