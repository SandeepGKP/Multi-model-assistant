import os
import re
import fitz  # PyMuPDF
import requests
import mimetypes
from dotenv import load_dotenv

load_dotenv()

from .embedding import generate_embedding
from .vector_store import add_text_to_vector_store

# Extract text from PDF
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_number, page in enumerate(doc):
        page_text = page.get_text()
        if page_text:
            text += f"\n[Page {page_number+1}]\n"
            text += page_text
    return text

# Extract text from image (via OCR microservice)
def extract_text_from_image(file_path):
    try:
        url = "https://ocr-microservice-02ej.onrender.com/api/ocr"

        if not os.path.exists(file_path):
            print("File not found:", file_path)
            return ""

        filename = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "image/png"

        print("File:", filename)
        print("Size:", os.path.getsize(file_path))

        with open(file_path, "rb") as f:
            files = {"file": (filename, f, mime_type)}
            response = requests.post(url, files=files, timeout=180)

            print("OCR Status:", response.status_code)
            print("OCR Response:", response.text)

            if response.ok:
                data = response.json()
                return data.get("res", "")

            return ""

    except Exception as e:
        print("OCR error:", e)
        return ""

# Extract text from TXT
def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Chunk text
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 20 and re.search(r'[a-zA-Z]', chunk):
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# Ingest document
def ingest_document(file_path):
    print("file path ....:: ", file_path)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    ext = file_path.split(".")[-1].lower()
    if ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in ["png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "gif", "ico", "heic"]:
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
