import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_collection("fastapi_docs")

question = "How do I handle authentication in FastAPI?"
q_vec = model.encode([question]).tolist()

results = collection.query(query_embeddings=q_vec, n_results=3)

context = "\n\n".join(results["documents"][0])

prompt = f"""Answer the question using ONLY the context below.
If the context doesn't contain the answer, say so.

Context:
{context}

Question: {question}"""

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
resp = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
)
print(resp.choices[0].message.content)