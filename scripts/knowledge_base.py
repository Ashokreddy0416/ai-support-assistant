import requests
from bs4 import BeautifulSoup
import json
import time

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

documents = []
for i, url in enumerate(urls):
    try:
        doc = scrape_page(url)
        if doc["text"]:
            doc["id"] = f"doc_{i}"
            documents.append(doc)
        time.sleep(0.5)
    except Exception as e:
        print(f"Skipped {url}: {e}")

with open("data/documents.jsonl", "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(json.dumps(doc) + "\n")

print(f"Saved {len(documents)} documents to data/documents.jsonl")

def chunk_text(text, size=800, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

all_chunks = []
for doc in documents:
    for j, piece in enumerate(chunk_text(doc["text"])):
        all_chunks.append({
            "chunk_id": f"{doc['id']}_chunk_{j}",
            "doc_id": doc["id"],
            "url": doc["url"],
            "title": doc["title"],
            "text": piece,
        })

with open("data/chunks.jsonl", "w", encoding="utf-8") as f:
    for c in all_chunks:
        f.write(json.dumps(c) + "\n")

print(f"Saved {len(all_chunks)} chunks to data/chunks.jsonl")