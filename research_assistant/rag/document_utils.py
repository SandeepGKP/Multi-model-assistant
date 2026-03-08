# rag/document_utils.py
import os
import fitz  # PyMuPDF
from PIL import Image,ImageEnhance
import pytesseract
from dotenv import load_dotenv
load_dotenv()

from .embeddings import generate_embedding
from .vector_store import add_text_to_vector_store

import shutil


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
    try:
        if shutil.which("tesseract") is None:
            raise RuntimeError("Tesseract is not installed on this server")

        img = Image.open(file_path)

        # Convert to grayscale
        img = img.convert("L")

        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)

        # Sharpen image
        sharp = ImageEnhance.Sharpness(img)
        img = sharp.enhance(2)

        text = pytesseract.image_to_string(img)

        return text
    except Exception:
        return ""
   
#   extract text from .txt file  
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