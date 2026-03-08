import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image,ImageEnhance
from .vector_store import add_text_to_vector_store
from dotenv import load_dotenv

load_dotenv()
import shutil
# ✅ Check if Tesseract is installed
if shutil.which("tesseract") is None:
    raise RuntimeError("Tesseract is not installed on this server")


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

#extract image from image
def extract_text_from_image(file_path):
    try:
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