_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    return _model

def generate_embedding(text):
    model = get_model()   # 👈 VERY IMPORTANT
    return model.encode(text)