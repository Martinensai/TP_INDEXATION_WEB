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
        # Détermination dynamique du chemin absolu
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_dir = os.path.join(self.base_dir, input_folder)
        
        self.load_indexes()
        self.load_synonyms()
        # Nombre total de documents pour le calcul du BM25
        self.total_docs = len(self.reviews_index)

    def load_indexes(self):
        """Charge les index avec des chemins robustes."""
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
        """Ajoute les synonymes d'origine à la requête."""
        expanded = set(tokens)
        for token in tokens:
            for country, syns in self.synonyms.items():
                if token.lower() == country.lower() or token.lower() in [s.lower() for s in syns]:
                    expanded.add(country)
                    expanded.update(syns)
        return list(expanded)

    def check_exact_match(self, query_tokens, url):
        """Bonus : Vérifie si les mots de la requête se suivent exactement dans le titre."""
        if len(query_tokens) < 2: return 0
        
        title_idx = self.indexes["title"]
        positions_by_token = []
        
        for token in query_tokens:
            if token in title_idx and url in title_idx[token]:
                positions_by_token.append(title_idx[token][url])
            else:
                return 0 # Un des mots est absent
        
        # Vérification de la contiguïté des positions
        matches = 0
        for start_pos in positions_by_token[0]:
            is_sequence = True
            for i in range(1, len(positions_by_token)):
                if (start_pos + i) not in positions_by_token[i]:
                    is_sequence = False
                    break
            if is_sequence: matches += 1
            
        return matches * 10.0 # Gros boost pour match exact

    def calculate_bm25(self, token, url, index_key):
        """Score BM25 simplifié (TF-IDF robuste)."""
        index = self.indexes[index_key]
        if token not in index or url not in index[token]:
            return 0
        
        tf = len(index[token][url]) if isinstance(index[token][url], list) else 1
        n_qi = len(index[token])
        idf = math.log((self.total_docs - n_qi + 0.5) / (n_qi + 0.5) + 1)
        return idf * (tf * 2.5) / (tf + 1.5)

    def get_ranking_score(self, url, query_tokens, expanded_tokens):
        """Combine BM25, Match Exact, Marque et Reviews."""
        score = 0
        
        # 1. Scoring Textuel (BM25)
        for token in expanded_tokens:
            score += self.calculate_bm25(token, url, "title") * 3.0 # Titre prioritaire
            score += self.calculate_bm25(token, url, "description") * 1.0

        # 2. Match Exact dans le titre (Boost)
        score += self.check_exact_match(query_tokens, url)

        # 3. Marque (Boost si le token correspond à la marque)
        brand_idx = self.indexes["brand"]
        for token in query_tokens:
            if token in brand_idx and url in brand_idx[token]:
                score += 15.0

        # 4. Signal Avis (Moyenne des notes)
        rev = self.reviews_index.get(url, {})
        score += rev.get("mean_mark", 0) * 0.8
        
        return round(score, 4)

    def search(self, query):
        query_tokens = self.tokenize(query)
        expanded_tokens = self.expand_query(query_tokens)
        
        # Filtrage : au moins un token présent (OU logique)
        results = []
        unique_urls = set()
        for t in expanded_tokens:
            if t in self.indexes["title"]: unique_urls.update(self.indexes["title"][t].keys())
            if t in self.indexes["description"]: unique_urls.update(self.indexes["description"][t].keys())

        for url in unique_urls:
            score = self.get_ranking_score(url, query_tokens, expanded_tokens)
            results.append({"url": url, "score": score})
            
        return sorted(results, key=lambda x: x["score"], reverse=True)