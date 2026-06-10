from typing import TypedDict
from backend.rag import _get_clients
from backend.rag import answer
from backend.graph_rag import graph_answer
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    question: str
    route: str
    answer: str

def router(state: AgentState) -> AgentState:
    _, _, groq_client = _get_clients()
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

builder = StateGraph(AgentState)
builder.add_node("router", router)
builder.add_node("vector", vector_node)
builder.add_node("graph", graph_node)
builder.add_node("clarify", clarify_node)

builder.add_edge(START, "router")
builder.add_conditional_edges("router", lambda s: s["route"],
    {"vector": "vector", "graph": "graph", "clarify": "clarify"})
builder.add_edge("vector", END)
builder.add_edge("graph", END)
builder.add_edge("clarify", END)

agent = builder.compile()

if __name__ == "__main__":
    result = agent.invoke({"question": "how do auth and dependencies work together"})
    print("ROUTE:", result["route"])
    print("ANSWER:", result["answer"])