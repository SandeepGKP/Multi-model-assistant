# rag/vector_store.py
import faiss
import numpy as np
from .embeddings import generate_embedding

# FAISS setup
dimension = 3072  # models/gemini-embedding-001
index = faiss.IndexFlatL2(dimension)
documents = []  # store text chunks

def add_text_to_vector_store(text):
    global index, documents

    embedding = generate_embedding(text)
    print("Embedding length:", len(embedding))  

    vector = np.array([embedding]).astype("float32")
    print("Vector shape:", vector.shape)  
    index.add(vector)
    documents.append(text)
    print("==========================================")
    print("==========================================")
    print(f"Added to FAISS: {text[:50]}...")
    print(f"FAISS total vectors: {index.ntotal}, Documents stored: {len(documents)}")

def search(query_embedding, top_k=3):
    if len(documents) == 0:
        print("FAISS empty, nothing to search")
        return []

    vector = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(vector, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])

    print(f"Search results: {results}")
    return results
