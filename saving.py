import json
def save_data_to_json(data, filename="crawled_data.json"):
    """Enregistre les résultats dans un fichier JSON.""" 
    with open(filename, 'w', encoding='utf-8') as f:
        for result in data:
            json.dump(result, f, ensure_ascii=False)
            f.write("\n")
    print(f"Données sauvegardées dans {filename}")

