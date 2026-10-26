import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from auth import authenticate, create_token, decode_token
from rag import answer

app = FastAPI(title="Secure Enterprise RAG")
bearer = HTTPBearer()


class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    question: str


def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        return decode_token(creds.credentials)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.post("/login")
def login(req: LoginRequest):
    role = authenticate(req.username, req.password)
    if not role:
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return {"access_token": create_token(req.username, role), "role": role}


@app.post("/chat")
def chat(req: ChatRequest, user: dict = Depends(current_user)):
    ans, docs = answer(req.question, user["role"])
    sources = sorted({(d.metadata["source"], d.metadata["department"]) for d in docs})
    return {
        "answer": ans,
        "role": user["role"],
        "sources": [{"file": s, "department": d} for s, d in sources],
    }