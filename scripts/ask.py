from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_collection("fastapi_docs")

question = "How do I handle authentication in FastAPI?"
q_vec = model.encode([question]).tolist()

results = collection.query(query_embeddings=q_vec, n_results=3)

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("FROM:", meta["title"])
    print(doc[:150], "...\n")