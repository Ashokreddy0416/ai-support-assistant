import requests
from bs4 import BeautifulSoup

SITEMAP_URL = "https://fastapi.tiangolo.com/sitemap.xml"

resp = requests.get(SITEMAP_URL, timeout=30)
soup = BeautifulSoup(resp.text, "xml")
urls = [loc.text for loc in soup.find_all("loc")]

print(f"Found {len(urls)} pages")
print(urls[:5])