import urllib.request
import urllib.robotparser
import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time


def get_robot_parser(seed_url):
    """Crée et charge le parser robots.txt une seule fois pour le domaine."""
    parsed_url = urlparse(seed_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urljoin(base_url, "robots.txt"))
    try:
        rp.read()
    except Exception as e:
        print(f"Impossible de lire le robots.txt : {e}")
    return rp

def crawling_permission_check(url, rp):
    """Vérifie la permission en utilisant le parser déjà chargé."""
    try:
        
        return rp.can_fetch("ENSAI-Crawler-2026", url)
    except:
        return True
    
def extraction_of_page(html_content,current_url):
    """Extraire le tire, le 1er pagraphe etc"""

    soup=BeautifulSoup(html_content,"html.parser")
    title=soup.title.string.strip() if soup.title else "sans titre"

    first_paragraph=""
    p_tag=soup.find("p")
    if p_tag:
        first_paragraph=p_tag.get_text().strip()
    links=[]
    body=soup.find("body")
    
    if body: 
        for a_tag in body.find_all("a",href=True):
            href=a_tag["href"]
            full_url=urljoin(current_url,href)

            if urlparse(full_url).netloc == urlparse(current_url).netloc:
                links.append(full_url)
    return {
        "title": title,
        "url": current_url,
         "first_paragraph": first_paragraph,
         "links": list(set(links))
    }
            

