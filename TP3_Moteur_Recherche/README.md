# 🔍 Search Engine Project - ENSAI 2026 (TP3)

Ce volet final consiste en la création d'un moteur de recherche performant utilisant les index inversés générés précédemment. Il intègre des algorithmes de classement (Ranking) basés sur la pertinence textuelle et des signaux métiers.

##  Structure du Projet (TP3)

Le moteur de recherche est structuré autour de deux composants principaux :

* **`search_engine.py`** : Le cœur algorithmique (Classe `SearchEngine`). Il gère le chargement des index, la tokenisation, l'extension de requête et le calcul des scores de pertinence.
* **`main.py`** : L'interface utilisateur interactive. Il gère la saisie des requêtes, l'enrichissement des résultats via le fichier JSONL et la génération du rapport final.

## Logique de Ranking et Scoring

Pour garantir des résultats pertinents, le moteur utilise un **scoring linéaire combiné** incluant les fonctionnalités suivantes :

### 1. Prétraitement et Extension de requête
* **Tokenisation & Normalisation** : Utilisation de NLTK pour le retrait des stopwords et la racinisation (Stemming) afin de faire correspondre les requêtes aux index.
* **Extension par Synonymes** : Intégration du fichier `origin_synonyms.json`. Une recherche sur "Swiss" activera automatiquement les résultats liés à "Switzerland".

### 2. Algorithmes de Score
* **BM25 (Best Matching 25)** : Calcul de la pertinence basé sur la fréquence des termes (TF) et la rareté du mot dans l'ensemble des documents (IDF).
* **Poids Différenciés** : Le titre a un coefficient de pondération plus élevé (**x3.0**) que la description (**x1.0**).
* **Match Exact (Bonus)** : Analyse des index de position pour détecter si les mots de la requête se suivent exactement dans le titre. Si une séquence exacte est trouvée, un bonus important est accordé au document.

### 3. Signaux Métiers
* **Boost Marque** : Un bonus est appliqué si un mot de la requête correspond exactement à la marque du produit.
* **Signal Avis (Reviews)** : Les produits bénéficiant d'une note moyenne (`mean_mark`) élevée sont favorisés dans le classement final.



##  Documentation des Choix et Analyse

Conformément aux critères d'évaluation, voici les justifications de nos choix techniques :

* **Choix du BM25** : Nous avons privilégié le BM25 au simple TF-IDF car il sature la fréquence des termes. Cela évite qu'un document ne soit artificiellement sur-classé par la répétition abusive d'un mot-clé (Keyword Stuffing).
* **Pondération Titre/Description** : Le titre étant le signal le plus fort de l'intention de l'auteur, un poids de 3.0 permet de garantir que la pertinence sémantique prime sur le volume de texte en description.
* **Utilisation des Positions** : L'implémentation du "Match Exact" permet de distinguer les concepts complexes (ex: "Dark Chocolate") des simples cooccurrences de mots isolés dans le document.
* **Signaux non-textuels** : L'intégration des avis clients (`mean_mark`) permet de départager des documents à pertinence textuelle égale en mettant en avant les produits "Top Rated", améliorant ainsi l'expérience utilisateur finale.

## 🚀 Utilisation

### Installation
Assurez-vous d'avoir installé les dépendances via le fichier `requirements.txt` à la racine :
```bash
pip install -r requirements.txt