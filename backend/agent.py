from typing import TypedDict
from backend.rag import groq_client

class AgentState(TypedDict):
    question: str
    route: str
    answer: str

def router(state: AgentState) -> AgentState:
    prompt = f"""Classify this question into exactly one word:
- "clarify" if it is too vague to answer (e.g. "help", "it's broken")
- "graph" if it asks how multiple things connect or work together
- "vector" for a normal, specific question

Question: {state['question']}
Answer with only one word: clarify, graph, or vector."""
    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    choice = resp.choices[0].message.content.strip().lower()
    route = choice if choice in {"clarify", "graph", "vector"} else "vector"
    return {"route": route}
