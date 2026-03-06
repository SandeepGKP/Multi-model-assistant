# rag/document_utils.py
import os
import fitz  # PyMuPDF
from PIL import Image

from dotenv import load_dotenv
load_dotenv()

import base64
import requests

from .embeddings import generate_embedding
from .vector_store import add_text_to_vector_store

#  Extract text
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_number, page in enumerate(doc):
        page_text = page.get_text()
        if page_text:
            text += f"\n[Page {page_number+1}]\n"
            text += page_text
    return text

#extract text from image
def extract_text_from_image(file_path):
    api_key = os.getenv("VISION_API_KEY")
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"

    with open(file_path, "rb") as f:
        img_content = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "requests": [
            {
                "image": {"content": img_content},
                "features": [{"type": "TEXT_DETECTION"}]
            }
        ]
    }

    response = requests.post(url, json=payload)
    result = response.json()

    try:
        return result["responses"][0]["textAnnotations"][0]["description"]
    except (KeyError, IndexError):
        return ""
    

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 2️⃣ Chunk text
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# 3️⃣ Ingest document
def ingest_document(file_path):
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    ext = file_path.split(".")[-1].lower()
    if ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in ["png", "jpg", "jpeg"]:
        text = extract_text_from_image(file_path)
    elif ext == "txt":
        text = extract_text_from_txt(file_path)
    else:
        return {"error": "Unsupported file type"}

    if not text.strip():
        return {"error": "No text extracted"}

    chunks = chunk_text(text)

    for chunk in chunks:
        add_text_to_vector_store(chunk)

    return {"status": "success", "total_chunks": len(chunks)}