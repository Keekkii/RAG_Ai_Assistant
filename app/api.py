from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client, Client
from app.rag import generate_answer
from dotenv import load_dotenv
import json
import os

# Load variables from root .env
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env")

# Initialize Supabase Admin/Client (for token verification)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Security Dependency ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verifies the Supabase JWT token.
    Supabase's auth.get_user(token) will return the user object if the token is valid.
    """
    try:
        # This call validates the JWT with Supabase Auth service
        response = supabase.auth.get_user(token)
        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return response.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- Models ---
class QuestionRequest(BaseModel):
    question: str

# --- Endpoints ---
@app.post("/chat")
def chat(request: QuestionRequest, user=Depends(get_current_user)):
    # You can access user.id or user.email here for logging if needed
    answer = generate_answer(request.question)
    return {"answer": answer}

@app.get("/logs")
def get_logs(user=Depends(get_current_user)):
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
    
    return logs[::-1][:50]

@app.get("/health")
def health():
    return {"status": "ok"}