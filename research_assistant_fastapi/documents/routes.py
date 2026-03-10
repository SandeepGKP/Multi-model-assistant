from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import os, shutil, traceback

from rag.document_util import ingest_document

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/tesseract_view/")
async def test_tesseract_view():
    path = shutil.which("tesseract")
    return PlainTextResponse(f"Tesseract path: {path}")

#upload endpoint
@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    try:
        if not file:
            return JSONResponse({"error": "No file uploaded."}, status_code=400)

        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = ingest_document(file_path)

        # optional cleanup
        os.remove(file_path)

        return {"status": "success", "filename": file.filename, "result": result}

    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return JSONResponse({"error": str(e), "trace": traceback_str}, status_code=500)
