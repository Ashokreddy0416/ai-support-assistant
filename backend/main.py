from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.rag import answer
from backend.graph_rag import graph_answer
from backend.agent import agent
from backend.auth import sign_up, log_in

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
    
@app.post("/agent")
def ask_agent(payload: Question):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        result = agent.invoke({"question": payload.question})
        return {
            "question": payload.question,
            "answer": result["answer"],
            "route": result["route"],
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Agent failed: {e}")
    
class Credentials(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(creds: Credentials):
    try:
        user = sign_up(creds.email, creds.password)
        return {"user_id": user.id, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signup failed: {e}")

@app.post("/login")
def login(creds: Credentials):
    try:
        token = log_in(creds.email, creds.password)
        return {"access_token": token}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")