#  Projet de Recherche d'Information - ENSAI 2026

Ce projet complet consiste en la conception et le développement d'un moteur de recherche vertical, de la collecte des données sur le web jusqu'au classement des résultats par pertinence.

## Architecture du Projet

Le projet est divisé en trois phases majeures, chacune correspondant à un Travail Pratique (TP). Pour une compréhension détaillée de l'implémentation, veuillez consulter le **README spécifique** à l'intérieur de chaque dossier.

### 1. [TP1 - Web Crawler](./TP1_Crawler/)
**Objectif :** Collecte de données brutes.
* Exploration "polie" du site cible (respect du `robots.txt` et délais).
* Extraction du contenu HTML (titres, paragraphes, liens).
* Priorisation des pages produits pour maximiser la pertinence du corpus.

### 2. [TP2 - Indexation](./TP2_Indexation/)
**Objectif :** Structuration de l'information pour la recherche.
* Création d'index inversés (mots -> documents).
* Gestion des index de position pour les recherches de proximité.
* Stockage des métadonnées (avis, marques, origines) pour le filtrage et le scoring.

### 3. [TP3 - Moteur de Recherche](./TP3_Moteur_Recherche/)
**Objectif :** Interface utilisateur et algorithme de classement.
* Implémentation du modèle de ranking **BM25**.
* Extension de requête par synonymes (noms de pays, nationalités).
* Scoring multi-signaux (Pertinence textuelle + Match exact + Qualité des avis).



##  Installation Globale

Le projet utilise Python 3.x et nécessite quelques bibliothèques externes (notamment pour le traitement du langage naturel).

1. **Cloner le dépôt** :
   ```bash
   git clone [url-du-depot]