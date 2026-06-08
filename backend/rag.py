import os
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma = chromadb.PersistentClient(path="data/chroma")
collection = chroma.get_collection("fastapi_docs")
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def answer(question: str, k: int = 3) -> str:
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