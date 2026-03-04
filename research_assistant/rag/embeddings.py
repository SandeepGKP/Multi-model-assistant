from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_embedding(text):
    response = client.models.embed_content(
        model="models/gemini-embedding-001",   
        contents=text
    )
    return response.embeddings[0].values

# Test
if __name__ == "__main__":
    emb = generate_embedding("Hello world")
    print(len(emb))