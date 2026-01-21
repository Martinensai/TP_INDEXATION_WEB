import urllib.request
import urllib.robotparser
import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time

def make_http_request(url):
    try:
        headers = {"User-Agent": "ENSAI-Crawler-2026"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content_type = response.info().get_content_type()
            if 'text/html' not in content_type:
                print(f"Format non supporté ({content_type}) pour {url}")
                return None
            return response.read()
    except urllib.error.HTTPError as e:
        print(f"Erreur HTTP {e.code} sur {url}") # Erreurs 404, 403, etc.
    except urllib.error.URLError as e:
        print(f"Serveur inaccessible : {e.reason}") # Problème DNS ou connexion
    except Exception as e:
        print(f"Erreur imprévue : {e}")
    return None
    

    
