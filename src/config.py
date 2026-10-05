import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# folder name inside data/ -> department tag
DEPARTMENTS = {
    "finance": "finance",
    "hr": "hr",
    "marketing": "marketing",
    "engineering": "engineering",
    "general": "general",
}