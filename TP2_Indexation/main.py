import os
import json
from indexer import build_inverted_index, build_reviews_index, build_features_index, build_positional_index

# Chemins
base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)
INPUT_FILE = os.path.join(base_dir, "input","products.jsonl")
OUTPUT_DIR = os.path.join(base_dir, "output")

def main():
    docs = []
    # Lecture du fichier JSONL
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line))

    # Génération des index avec les clés
    results = {
        "index_title.json": build_inverted_index(docs, "title"),
        "index_description.json": build_inverted_index(docs, "description"),
        "index_reviews.json": build_reviews_index(docs),
        "index_brand.json": build_features_index(docs, "brand"), 
        "index_origin.json": build_features_index(docs, "made in"), 
        "index_positional_title.json": build_positional_index(docs, "title")
    }

    # Sauvegarde
    for filename, data in results.items():
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, "w", encoding="utf-8") as out:
            json.dump(data, out, indent=4, ensure_ascii=False)
        print(f"Sauvegardé : {path}")

if __name__ == "__main__":
    main()