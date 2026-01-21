import json
import math
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Configuration NLTK
nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("english"))
STEMMER = PorterStemmer()

class SearchEngine:
    def __init__(self, input_folder="input"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_dir = os.path.join(self.base_dir, input_folder)
        self.load_indexes()
        self.load_synonyms()
        self.total_docs = len(self.reviews_index)

    def load_indexes(self):
        files = {
            "title": "title_index.json",
            "description": "description_index.json",
            "brand": "brand_index.json",
            "origin": "origin_index.json",
            "reviews": "reviews_index.json"
        }
        self.indexes = {}
        for key, filename in files.items():
            path = os.path.join(self.input_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                self.indexes[key] = json.load(f)
        self.reviews_index = self.indexes["reviews"]

    def load_synonyms(self):
        path = os.path.join(self.input_dir, "origin_synonyms.json")
        with open(path, "r", encoding="utf-8") as f:
            self.synonyms = json.load(f)

    def tokenize(self, text):
        text = re.sub(r'[^\w\s]', '', str(text).lower())
        return [STEMMER.stem(t) for t in text.split() if t not in STOPWORDS]

    def expand_query(self, tokens):
        """Expansion de la requête avec synonymes pays et concepts métiers."""
        expanded = set(tokens)
        for token in tokens:
            for key, syns in self.synonyms.items():
                if token.lower() == key.lower() or token.lower() in [s.lower() for s in syns]:
                    expanded.add(key)
                    for s in syns:
                        expanded.add(s)
        return list(expanded)

    def calculate_bm25(self, token, url, index_key, k1=1.5, b=0.75):
        index = self.indexes[index_key]
        if token not in index or url not in index[token]:
            return 0
        
        # Fréquence du terme (TF) - Nombre d'occurrences/positions
        tf = len(index[token][url]) if isinstance(index[token][url], list) else 1
        n_qi = len(index[token])
        
        # IDF (Inverse Document Frequency)
        idf = math.log((self.total_docs - n_qi + 0.5) / (n_qi + 0.5) + 1)
        
        # Score BM25 simplifié
        return idf * (tf * (k1 + 1)) / (tf + k1)

    def check_exact_match(self, query_tokens, url):
        """Utilise l'index de position pour trouver des séquences exactes dans le titre."""
        if len(query_tokens) < 2: return 0
        title_idx = self.indexes["title"]
        
        # Récupération des positions pour chaque mot de la requête
        pos_lists = []
        for t in query_tokens:
            stemmed_t = STEMMER.stem(t)
            if stemmed_t in title_idx and url in title_idx[stemmed_t]:
                pos_lists.append(title_idx[stemmed_t][url])
            else:
                return 0

        # Vérification si les mots se suivent (position n, n+1, n+2...)
        matches = 0
        for start_pos in pos_lists[0]:
            current_pos = start_pos
            is_match = True
            for i in range(1, len(pos_lists)):
                if (current_pos + 1) in pos_lists[i]:
                    current_pos += 1
                else:
                    is_match = False
                    break
            if is_match: matches += 1
            
        return matches * 15.0 # Boost significatif pour match exact

    def get_ranking_score(self, url, query_tokens, expanded_tokens):
        score = 0
        
        # 1. BM25 Textuel (Poids Titre x3 / Description x1)
        for token in expanded_tokens:
            stemmed_token = STEMMER.stem(token)
            score += self.calculate_bm25(stemmed_token, url, "title") * 3.0
            score += self.calculate_bm25(stemmed_token, url, "description") * 1.0

        # 2. Match Exact dans le Titre
        score += self.check_exact_match(query_tokens, url)

        # 3. Signal de l'Origine (Si un mot de la requête cible une origine connue)
        origin_idx = self.indexes["origin"]
        for token in expanded_tokens:
            if token in origin_idx and url in origin_idx[token]:
                score += 10.0

        # 4. Signal des Avis (Qualité perçue)
        review_data = self.reviews_index.get(url, {})
        mean_mark = review_data.get("mean_mark", 0)
        if mean_mark >= 4.5:
            score += 5.0 # Boost "Top Rated"
        
        return round(score, 4)

    def search(self, query):
        # On garde les tokens originaux pour le match exact et les étendus pour le rappel
        query_tokens = [t for t in query.lower().split() if t not in STOPWORDS]
        expanded_tokens = self.expand_query(query_tokens)
        
        unique_urls = set()
        for t in expanded_tokens:
            stemmed_t = STEMMER.stem(t)
            if stemmed_t in self.indexes["title"]: 
                unique_urls.update(self.indexes["title"][stemmed_t].keys())
            if stemmed_t in self.indexes["description"]: 
                unique_urls.update(self.indexes["description"][stemmed_t].keys())

        results = []
        for url in unique_urls:
            score = self.get_ranking_score(url, query_tokens, expanded_tokens)
            results.append({"url": url, "score": score})
            
        return sorted(results, key=lambda x: x["score"], reverse=True)