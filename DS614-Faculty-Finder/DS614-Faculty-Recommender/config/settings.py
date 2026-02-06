from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PHASE1_API_BASE = "http://localhost:8000"
PHASE1_FACULTY_ENDPOINT = "/faculty"

PHASE1_FACULTY_URL = PHASE1_API_BASE + PHASE1_FACULTY_ENDPOINT

DATA_DIR = PROJECT_ROOT / "data"
INDEX_DIR = PROJECT_ROOT / "index"

INDEX_FILE = INDEX_DIR / "vectors.pkl"
STOPWORDS_PATH = DATA_DIR / "stopwords.txt"
