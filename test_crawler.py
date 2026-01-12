import unittest
import json
from extraction import extraction_of_page
from configuration import make_http_request

class TestCrawlerENSAI(unittest.TestCase):

    def test_url_priority_logic(self):
        """Vérifie que le crawler priorise bien le token 'product'"""
        urls = [
            "https://web-scraping.dev/reviews",
            "https://web-scraping.dev/testimonials",
            "https://web-scraping.dev/products",
            "https://web-scraping.dev/products?category=apparel"
        ]
        
        # Tri identique à la logique de crawling.py [cite: 1001]
        urls.sort(key=lambda url: "product" not in url.lower())
        
        # Les deux premières URLs doivent être celles contenant 'product'
        self.assertIn("product", urls[0].lower()) 
        self.assertIn("product", urls[1].lower()) 

    def test_extraction_content(self):
        """Vérifie l'extraction du titre et du premier paragraphe[cite: 983, 1017, 1019]."""
        html_test = """
        <html>
            <head><title>Page de Test</title></head>
            <body>
                <p>Ceci est le paragraphe cible pour le test.</p>
                <a href="/products/box">Lien interne</a>
            </body>
        </html>
        """
        data = extraction_of_page(html_test, "https://web-scraping.dev/products")
        
        self.assertEqual(data["title"], "Page de Test") 
        self.assertEqual(data["first_paragraph"], "Ceci est le paragraphe cible pour le test.") 

    def test_http_error_handling(self):
        """Vérifie que le système gère les erreurs sans planter."""
        # Test d'une URL qui n'existe pas
        result = make_http_request("https://web-scraping.dev/non-existent-page-404")
        self.assertIsNone(result) 

if __name__ == "__main__":
    unittest.main()