from typing import TypedDict
from backend.rag import groq_client
from backend.rag import answer
from backend.graph_rag import graph_answer

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

def vector_node(state: AgentState) -> AgentState:
    return {"answer": answer(state["question"])}

def graph_node(state: AgentState) -> AgentState:
    return {"answer": graph_answer(state["question"])}

def clarify_node(state: AgentState) -> AgentState:
    return {"answer": "Could you be more specific? Tell me what you're trying to do and which part of FastAPI you mean."}
