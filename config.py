from pathlib import Path


# Project directories
BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
CHROMA_DB_DIR = BASE_DIR / "chroma_data"


# Embedding model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# Retrieval settings
TOP_K = 3