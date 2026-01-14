import json
import os
from search_engine import SearchEngine

def run_tp3():
    # --- INITIALISATION ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    engine = SearchEngine(input_folder="input")
    
    # Couleurs et style pour la console
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    END = "\033[0m"

    print(f"\n{BLUE}{BOLD}==================================================={END}")
    print(f"{BLUE}{BOLD}       ENSAI SEARCH ENGINE - EDITION 2026          {END}")
    print(f"{BLUE}{BOLD}==================================================={END}\n")

    # --- INTERACTION UTILISATEUR ---
    user_query = input(f"{BOLD}🔍 Entrez votre recherche (ou tapez Entrée pour le query par défaut) : {END}").strip()
    
    # Gestion de la valeur par défaut
    if not user_query:
        query = "Box of Chocolate"
        print(f"{YELLOW}💡 Aucune saisie détectée. Utilisation du terme par défaut : '{query}'{END}")
    else:
        query = user_query

    # --- CHARGEMENT DES DONNÉES ---
    products_file = os.path.join(base_dir, "rearranged_products.jsonl")
    product_data = {}
    
    if not os.path.exists(products_file):
        print(f"❌ Erreur : Le fichier {products_file} est introuvable.")
        return

    with open(products_file, "r", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            product_data[p["url"]] = p

    # --- RECHERCHE ET RANKING ---
    print(f"\n📡 Analyse des index en cours pour : {BOLD}'{query}'{END}...")
    raw_results = engine.search(query)

    # --- FORMATAGE DU LIVRABLE JSON ---
    output = {
        "query": query,
        "metadata": {
            "total_documents": len(product_data),
            "filtered_documents": len(raw_results)
        },
        "results": []
    }

    for res in raw_results[:20]: # Top 20
        url = res["url"]
        info = product_data.get(url, {})
        output["results"].append({
            "title": info.get("title"),
            "url": url,
            "description": info.get("description"),
            "ranking_score": res["score"]
        })

    # --- SAUVEGARDE ---
    output_path = os.path.join(base_dir, "search_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    # --- RÉCAPITULATIF ÉLÉGANT ---
    print(f"\n{GREEN}{BOLD}✅ RECHERCHE TERMINÉE AVEC SUCCÈS{END}")
    print(f"---------------------------------------------------")
    print(f"📊 {BOLD}Statistiques :{END}")
    print(f"   - Documents totaux indexés : {len(product_data)}")
    print(f"   - Documents pertinents trouvés : {len(raw_results)}")
    
    if raw_results:
        best_url = raw_results[0]['url']
        best_title = product_data.get(best_url, {}).get('title', 'N/A')
        print(f"🏆 {BOLD}Meilleur résultat :{END}")
        print(f"   - Titre : {GREEN}{best_title}{END}")
        print(f"   - Score : {YELLOW}{raw_results[0]['score']}{END}")
        print(f"   - URL   : {best_url}")
    else:
        print(f"⚠️ {YELLOW}Aucun document ne correspond à votre requête.{END}")

    print(f"\n📂 {BOLD}Sauvegarde :{END}")
    print(f"   - Les résultats sont enregistrés dans : {output_path}")
    print(f"---------------------------------------------------\n")

if __name__ == "__main__":
    run_tp3()