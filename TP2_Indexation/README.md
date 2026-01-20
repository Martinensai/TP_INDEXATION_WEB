#  Web Indexing Project - ENSAI 2026

Ce dépôt contient les travaux réalisés dans le cadre du cours d'**Indexation Web**. [L'objectif est de concevoir un moteur de recherche complet, de la collecte des données à la structuration de l'information.

## Structure du TP2 : Création des Index

Ce deuxième volet porte sur la transformation des documents bruts collectés (`products.jsonl`) en structures de données optimisées pour la recherche rapide.

### 1. Organisation des Index
Le script génère plusieurs fichiers d'index dans le dossier `WORK_TP2/output/` pour répondre aux besoins spécifiques du moteur de recherche :

* **Index Inversés Standards** (`index_title.json`, `index_description.json`) : Associent chaque terme nettoyé à la liste des URLs des documents.
* **Index de Position** (`index_positional_title.json`) : Pour le champ titre, cet index stocke l'URL et les positions exactes de chaque mot pour permettre les recherches par expressions exactes.
* **Index des Reviews** (`index_reviews.json`) : Index non-inversé stockant le nombre total de reviews, la note moyenne et la dernière note pour l'ordonnancement.
* **Index des Features** (`index_brand.json`, `index_origin.json`) : Index inversés basés sur les attributs `brand` (marque) et `origin` (mappé sur `made in`) pour le filtrage par facettes.


### 2. Choix d'implémentation
* **Prétraitement du texte (NLP)** : 
    * **Tokenisation & Nettoyage** : Découpage par espaces et suppression de la ponctuation via expressions régulières.
    * **Stopwords (NLTK)** : Suppression des mots outils anglais basée sur la **Loi de Zipf** pour réduire le bruit.
    * **Stemming (NLTK PorterStemmer)** : Racinisation pour regrouper les mots de même famille morphologique.
* **Gestion des données réelles** : Le code cible dynamiquement les champs `product_features` et `product_reviews` identifiés dans les données JSONL.
* **Gestion des chemins** : Utilisation de `os.path` pour garantir la portabilité du code et automatiser la création des dossiers de sortie.

## Installation et Utilisation

### Prérequis
* Python 3.x
* Un fichier `products.jsonl` valide situé à la racine du projet.

### Installation des dépendances
Avant de lancer le script, installez les bibliothèques nécessaires (notamment `nltk`) :
```bash
pip install -r requirements.txt