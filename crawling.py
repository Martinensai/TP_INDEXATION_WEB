import urllib.request
import urllib.robotparser
import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
from extraction import crawling_permission_check
from extraction import extraction_of_page
from configuration import make_http_request
from extraction import get_robot_parser

def crawling_website(seed_url, max_pages=50):
    visited = set()
    to_visit = [seed_url]
    results = []
    
    # CHARGEMENT UNIQUE DU ROBOTS.TXT ICI
    rp = get_robot_parser(seed_url)

    while to_visit and len(visited) < max_pages:
        to_visit.sort(key=lambda url: "product" not in url.lower())
        url = to_visit.pop(0)

        # Passer 'rp' à la fonction de vérification
        if url in visited or not crawling_permission_check(url, rp):
            continue
        
        print(f'Indexing: {url}')
        content=make_http_request(url)
    
        if content: 
            page_data= extraction_of_page(content, url)
            results.append(page_data)
            visited.add(url)
            
            for link in page_data["links"]:
                if link not in visited:
                    to_visit.append(link)
        time.sleep(1)
    return results



