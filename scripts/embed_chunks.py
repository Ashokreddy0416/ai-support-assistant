import json
from sentence_transformers import SentenceTransformer
import chromadb

chunks = [json.loads(l) for l in open("data/chunks.jsonl", encoding="utf-8")]
print(f"Loaded {len(chunks)} chunks")

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_or_create_collection("fastapi_docs")

texts = [c["text"] for c in chunks]
embeddings = model.encode(texts, show_progress_bar=True).tolist()

collection.add(
    ids=[c["chunk_id"] for c in chunks],
    embeddings=embeddings,
    documents=texts,
    metadatas=[{"url": c["url"], "title": c["title"]} for c in chunks],
)
print(f"Stored {collection.count()} vectors in Chroma")