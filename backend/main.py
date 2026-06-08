from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag import answer

app = FastAPI(title="AI Support Assistant")

class Question(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(payload: Question):
    result = answer(payload.question)
    return {"question": payload.question, "answer": result}