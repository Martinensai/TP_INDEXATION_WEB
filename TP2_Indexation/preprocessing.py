import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Téléchargement des ressources NLTK nécessaires
nltk.download('stopwords')

def clean_text(text):
    """
    Tokenization, passage en minuscule, retrait ponctuation, 
    suppression des stopwords NLTK et stemming[cite: 277, 278, 279].
    """
    if not text: 
        return []
    
    # 1. Passage en minuscules et retrait de la ponctuation via regex [cite: 277]
    text = re.sub(r'[^\w\s]', '', str(text).lower())
    
    # 2. Tokenization par espace
    tokens = text.split()
    
    # 3. Suppression des stopwords via la liste officielle NLTK (Anglais) [cite: 278, 614]
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]
    
    # 4. Stemming (Racinisation) pour regrouper les mots de même famille [cite: 279, 645]
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(t) for t in tokens]
    
    return stemmed_tokens


def extract_url_info(url):
    """
    Extrait l'ID du produit et la variante depuis l'URL.
    """
    # Extraction de l'ID : cherche un chiffre après "/product/"
    id_match = re.search(r'/product/(\d+)', url)
    product_id = id_match.group(1) if id_match else None
    
    # Extraction de la variante : cherche la valeur après "?variant="
    variant_match = re.search(r'variant=([^&]+)', url)
    variant = variant_match.group(1) if variant_match else "standard"
    
    return {
        "product_id": product_id,
        "variant": variant
    }