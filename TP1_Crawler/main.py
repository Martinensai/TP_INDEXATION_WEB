from crawling import crawling_website
from saving import save_data_to_json
Start_url="https://web-scraping.dev/products"
MAX_DOCUMENTS=50
crawled_results=crawling_website(Start_url,MAX_DOCUMENTS)
save_data_to_json(crawled_results)