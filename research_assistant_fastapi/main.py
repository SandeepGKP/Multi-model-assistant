from fastapi import FastAPI
from rag.routes import router as rag_router
from documents.routes import router as documents_router
from documents.db import Base,engine

# Create FastAPI app
app = FastAPI(
    title="Multi‑Modal Research Assistant",
    description="FastAPI backend for document ingestion and RAG pipeline",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(documents_router, prefix="/api/documents", tags=["documents"])
app.include_router(rag_router, prefix="/api/rag", tags=["rag"])

# Health check endpoint (like Django's /health/)
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "FastAPI backend working"}
