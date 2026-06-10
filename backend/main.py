from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.rag import answer
from backend.graph_rag import graph_answer

app = FastAPI(title="AI Support Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(payload: Question):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        result = answer(payload.question)
        return {"question": payload.question, "answer": result}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Answer generation failed: {e}")
    
@app.post("/ask-graph")
def ask_graph(payload: Question):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        result = graph_answer(payload.question)
        return {"question": payload.question, "answer": result, "mode": "graph"}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Graph answer failed: {e}")