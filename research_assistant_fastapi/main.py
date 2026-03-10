from fastapi import FastAPI
from rag.routes import router as rag_router
from documents.routes import router as documents_router

app = FastAPI()

app.include_router(documents_router, prefix="/api", tags=["documents"])
app.include_router(rag_router, prefix="/api", tags=["rag"])
