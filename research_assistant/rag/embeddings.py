# rag/embeddings.py

import os
from groq import Groq

# Initialize Groq client once
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Set in Render secrets
_client = Groq(api_key=GROQ_API_KEY)

def generate_embedding(text: str):
    """
    Returns a vector embedding for the given text using Groq API.
    """
    response = _client.embeddings.create(
        model="embedding-multilingual-v2",
        input=text
    )
    # Groq returns embeddings as a list under 'embedding'
    return response.embedding