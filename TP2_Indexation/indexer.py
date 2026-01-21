import json
import re
import os
from collections import defaultdict
from preprocessing import clean_text

# --- CRÉATION DES INDEX ---

def build_inverted_index(documents, field_name):
    """Index inversé classique (Mot -> Liste d'URLs)."""
    index = defaultdict(set)
    for doc in documents:
        url = doc.get("url")
        tokens = clean_text(doc.get(field_name, ""))
        for token in tokens:
            index[token].add(url)
    return {k: list(v) for k, v in index.items()}


def build_positional_index(documents, field_name):
    """Index inversé avec positions des mots."""
    index = defaultdict(lambda: defaultdict(list))
    for doc in documents:
        url = doc.get("url")
        tokens = clean_text(doc.get(field_name, ""))
        for pos, token in enumerate(tokens):
            index[token][url].append(pos)
    return index


def build_features_index(documents, feature_key):
    """Index inversé par feature (ex: brand)."""
    index = defaultdict(list)
    for doc in documents:
        url = doc.get("url") 
        # La clé est 'product_features'
        features = doc.get("product_features", {})
        
        feature_value = features.get(feature_key)
        
        if feature_value:
            # On stocke l'URL pour chaque valeur de feature trouvée
            index[str(feature_value).lower()].append(url) 
            
    return dict(index)

def build_reviews_index(documents):
    """Index non-inversé pour les statistiques de notes."""
    index = {}
    for doc in documents:
        url = doc.get("url") 
        reviews = doc.get("product_reviews", [])
        
        count = len(reviews)
        avg_rating = sum(r.get('rating', 0) for r in reviews) / count if count > 0 else 0
        last_rating = reviews[-1].get('rating', 0) if count > 0 else 0
        
        index[url] = {
            "total_reviews": count,
            "average_rating": avg_rating,
            "last_rating": last_rating
        }
    return index