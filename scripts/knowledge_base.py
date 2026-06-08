import requests
from bs4 import BeautifulSoup

SITEMAP_URL = "https://fastapi.tiangolo.com/sitemap.xml"

resp = requests.get(SITEMAP_URL, timeout=30)
soup = BeautifulSoup(resp.text, "xml")
urls = [loc.text for loc in soup.find_all("loc")]

def scrape_page(url):
    resp = requests.get(url, timeout=30)
    soup = BeautifulSoup(resp.text, "lxml")
    title = soup.find("title").text.strip()
    article = soup.find("article")
    text = article.get_text(separator=" ", strip=True) if article else ""
    return {"url": url, "title": title, "text": text}

doc = scrape_page(urls[1])
print("TITLE:", doc["title"])
print("TEXT (first 200 chars):", doc["text"][:200])