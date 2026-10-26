import time
import bcrypt
import jwt

from config import JWT_SECRET

ALGO = "HS256"
EXPIRE_SECONDS = 3600

# demo users only; a real system would use a database
_DEMO = {
    "fin_user": ("finance123", "finance"),
    "hr_user": ("hr123", "hr"),
    "mkt_user": ("marketing123", "marketing"),
    "eng_user": ("eng123", "engineering"),
    "emp_user": ("employee123", "employee"),
    "ceo_user": ("ceo123", "c_level"),
}
USERS = {
    u: {"hash": bcrypt.hashpw(p.encode(), bcrypt.gensalt()), "role": r}
    for u, (p, r) in _DEMO.items()
}


def authenticate(username: str, password: str):
    user = USERS.get(username)
    if user and bcrypt.checkpw(password.encode(), user["hash"]):
        return user["role"]
    return None


def create_token(username: str, role: str) -> str:
    payload = {"sub": username, "role": role, "exp": int(time.time()) + EXPIRE_SECONDS}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[ALGO])