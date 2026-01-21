import json
import os
from search_engine import SearchEngine

def print_banner():
    """Affiche un en-tête professionnel pour le moteur de recherche."""
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    END = "\033[0m"
    print(f"\n{CYAN}{BOLD}" + "═"*65)
    print("        🚀 ENSAI SEARCH ENGINE | SYSTÈME D'INDEXATION v3.0      ".center(65))
    print("═"*65 + f"{END}")

def run_tp3():
    # --- INITIALISATION ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    engine = SearchEngine(input_folder="input")
    
    # Palette de couleurs ANSI pour un rendu moderne
    BLUE, GREEN, YELLOW, CYAN = "\033[94m", "\033[92m", "\033[93m", "\033[96m"
    BOLD, UNDERLINE, END = "\033[1m", "\033[4m", "\033[0m"

    print_banner()

    # --- ZONE DE SAISIE ÉLÉGANTE ---
    # cadre visuel pour inviter l'utilisateur à taper
    print(f"\n{BOLD}┌" + "─"*63 + "┐")
    user_query = input(f"│  🔍 Tapez les mots-clés à rechercher : ").strip()
    print("└" + "─"*63 + "┘" + f"{END}")
    
    # Définition de la requête (valeur par défaut si vide)
    query = user_query if user_query else "Box of Chocolate"
    if not user_query:
        print(f"{YELLOW}   ℹ️  Entrée vide. Utilisation du terme par défaut : '{query}'{END}")

    # --- CHARGEMENT DES DONNÉES SOURCES ---
    product_data = {}
    jsonl_path = os.path.join(base_dir, "rearranged_products.jsonl")
    
    if not os.path.exists(jsonl_path):
        print(f"❌ Erreur : {jsonl_path} introuvable.")
        return

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            product_data[p["url"]] = p

    # --- MOTEUR DE RECHERCHE ---
    print(f"\n{BLUE}📡 Analyse des index inversés et calcul du BM25...{END}")
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

    # --- AFFICHAGE DES RÉSULTATS (TOP 5 VISUEL) ---
    print(f"\n{GREEN}{BOLD}{UNDERLINE}CLASSEMENT DES RÉSULTATS PAR PERTINENCE{END}")
    
    if not raw_results:
        print(f"\n{YELLOW}   ⚠️ Aucun résultat trouvé pour cette requête.{END}")
    
    for i, res in enumerate(raw_results[:20]):
        info = product_data.get(res["url"], {})
        
        # Remplissage de la structure pour le fichier de sortie (Top 20)
        output["results"].append({
            "title": info.get("title"),
            "url": res["url"],
            "description": info.get("description"),
            "ranking_score": res["score"]
        })

        # Affichage détaillé pour les 5 premiers dans le terminal
        if i < 5:
            print(f"\n{BOLD}{GREEN}{i+1}. {info.get('title')}{END}")
            print(f"   📊 Score de Ranking : {YELLOW}{res['score']}{END}")
            print(f"   🔗 URL : {BLUE}{UNDERLINE}{res['url']}{END}")
            # Aperçu du contenu
            desc = info.get('description', '')[:130] + "..." if info.get('description') else "Pas de description."
            print(f"   📝 {desc}")

    # --- SAUVEGARDE ET CLÔTURE ---
    output_path = os.path.join(base_dir, "search_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"\n" + "═"*65)
    print(f"{GREEN}✅ PROCESSUS TERMINÉ{END}")
    print(f"💾 Résultats exportés : {BOLD}{output_path}{END}")
    print(f"🎯 Total correspondances : {BOLD}{len(raw_results)}{END}")
    print("═"*65 + "\n")

if __name__ == "__main__":
    run_tp3()