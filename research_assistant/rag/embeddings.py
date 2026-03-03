from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")  # smallest, fast

def generate_embedding(text):
    return _model.encode(text)