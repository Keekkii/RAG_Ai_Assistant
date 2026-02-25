from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.rag import generate_answer
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: QuestionRequest):
    answer = generate_answer(request.question)
    return {"answer": answer}

@app.get("/logs")
def get_logs():
    log_file = "chat_logs.jsonl"
    if not os.path.exists(log_file):
        return []
    
    logs = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    logs.append(json.loads(line))
                except:
                    continue
    
    # Return last 50 logs, newest first
    return logs[::-1][:50]