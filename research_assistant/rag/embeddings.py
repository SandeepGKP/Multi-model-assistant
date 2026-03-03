# rag/embeddings.py

from sentence_transformers import SentenceTransformer

_model = None  # placeholder for lazy loading

def generate_embedding(text):
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model.encode(text)