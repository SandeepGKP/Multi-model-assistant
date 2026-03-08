import os
import fitz  # PyMuPDF

from .vector_store import add_text_to_vector_store
from dotenv import load_dotenv
import requests

import requests
import os

load_dotenv()
import shutil
# ==============================
# Extract text functions
# ==============================
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_number, page in enumerate(doc):
        page_text = page.get_text()
        if page_text:
            text += f"\n[Page {page_number+1}]\n"
            text += page_text
    # doc.close()
    return text

# extract text from image
def extract_text_from_image(file_path):
    try:
        url = "https://ocr-microservice-02ej.onrender.com/api/ocr"

        filename = os.path.basename(file_path)
        print("File path:", file_path)

        with open(file_path, "rb") as f:
            files = {
                "file": (filename, f)
            }

            response = requests.get(url, files=files, timeout=60)
            data = response.json()
            print("Status code:", response.status_code)
            print("Raw response:", data.get("res", ""))

            if response.status_code == 200:
                data = response.json()
                print("OCR response:", data.get("res", ""))
                return data.get("res", "")

            return ""

    except Exception as e:
        print("OCR error:", e)
        return ""
    


# extract text from .txt file
def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ==============================
# Chunking function
# ==============================
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# ==============================
# Main ingestion
# ==============================
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
#   # Robust deletion
#     try:
#         os.remove(file_path)
#     except Exception as e:
#         print(f"Warning: could not delete file {file_path}: {e}")

    # try:
    #     pytesseract.get_tesseract_version()
    # except Exception as e:
    #     print("Tesseract not installed:", e)
    return {"status": "success", "total_chunks": len(chunks)}