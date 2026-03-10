from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import traceback

from rag.pipeline import run_rag_pipeline

router = APIRouter()

@router.get("/health/")
async def health():
    return {"status": "backend working"}

#Question ask endpoint
@router.post("/ask/")
async def ask_question(request: Request):
    try:
        data = await request.json()
        question = data.get("question")
        answer = run_rag_pipeline(question)
        return {"answer": answer}
    except Exception as e:
        print("ERROR START")
        traceback.print_exc()
        print("ERROR END")
        return JSONResponse({"error": str(e)}, status_code=500)
