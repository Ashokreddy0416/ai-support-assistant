from backend.rag import _get_clients
from backend.graph import related_pages

def graph_answer(question: str) -> str:
    model, collection, groq_client = _get_clients()
    q_vec = model.encode([question]).tolist()
    top = collection.query(query_embeddings=q_vec, n_results=1)
    start_url = top["metadatas"][0][0]["url"]

    related = related_pages(start_url)
    urls = [start_url] + related

    chunks = collection.get(where={"url": {"$in": urls}}, limit=8)
    context = "\n\n".join(chunks["documents"])

    prompt = f"""Answer using ONLY the context below, which includes the most
relevant page and pages connected to it.

Context:
{context}

Question: {question}"""
    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    print(graph_answer("What do I need to secure an endpoint in FastAPI?"))