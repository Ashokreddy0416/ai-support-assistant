import os
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb

load_dotenv()

_model = None
_collection = None
_groq_client = None

def _get_clients():
    global _model, _collection, _groq_client
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        chroma = chromadb.PersistentClient(path="data/chroma")
        _collection = chroma.get_collection("fastapi_docs")
        _groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _model, _collection, _groq_client

def answer(question: str, k: int = 3) -> str:
    model, collection, groq_client = _get_clients()
    q_vec = model.encode([question]).tolist()
    results = collection.query(query_embeddings=q_vec, n_results=k)
    context = "\n\n".join(results["documents"][0])
    prompt = f"""Answer the question using ONLY the context below.
If the context doesn't contain the answer, say so.

Context:
{context}

Question: {question}"""
    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    print(answer("How do I handle authentication in FastAPI?"))