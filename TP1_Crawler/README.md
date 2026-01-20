# 🕸️ Web Crawler Project - ENSAI 2026 (TP1)

Ce projet consiste en la création d'un crawler web "poli" et optimisé en Python. L'objectif est d'explorer un site e-commerce, d'extraire des données structurées et de prioriser les pages produits.

## 📂 Structure du projet

Le code est divisé en plusieurs modules pour respecter le principe de responsabilité unique :

* **`main.py`** : Point d'entrée du script. Configure l'URL de départ et lance le crawling.
* **`crawling.py`** : Gère la logique d'exploration, la file d'attente (frontier) et la priorité des URLs.
* **`extraction.py`** : Contient les fonctions d'analyse HTML (BeautifulSoup) et la gestion du fichier `robots.txt`.
* **`configuration.py`** : Gère les requêtes HTTP, les headers (User-Agent) et la gestion des erreurs réseau.
* **`saving.py`** : Gère l'exportation des données au format JSON.
* **`test_crawler.py`** : Tests unitaires pour valider la priorité et l'extraction.



## Fonctionnalités implémentées

### 1. Politesse et Respect
* **Robots.txt** : Le crawler vérifie systématiquement les permissions via `urllib.robotparser` avant de visiter une page.
* **User-Agent** : Identification personnalisée (`ENSAI-Crawler-2026`).
* **Délai (Politeness delay)** : Une pause de 1 seconde est marquée entre chaque requête pour ne pas surcharger le serveur.

### 2. Stratégie d'exploration
* **Priorisation** : Les URLs contenant le mot-clé `product` sont placées en tête de file pour être traitées en priorité.
* **Limite de volume** : Le crawler s'arrête automatiquement après avoir visité 50 pages uniques.
* **Gestion des doublons** : Utilisation d'un ensemble (`set`) pour garantir qu'aucune page n'est visitée deux fois.

### 3. Extraction des données
Pour chaque page valide, le crawler extrait :
* Le titre de la page.
* L'URL complète.
* Le premier paragraphe (`<p>`) du contenu.
* La liste des liens internes présents dans le corps (`<body>`) de la page.

## Utilisation

### Prérequis
* Python 3.x
* Bibliothèque BeautifulSoup4 : `pip install beautifulsoup4`

### Lancement
Exécutez simplement le script principal :
```bash
python main.py