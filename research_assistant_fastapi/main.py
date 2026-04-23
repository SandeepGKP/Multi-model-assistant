from fastapi import FastAPI
from rag.routes import router as rag_router
from documents.routes import router as documents_router

from fastapi.middleware.cors import CORSMiddleware 
import uvicorn,os
# Create FastAPI app
app = FastAPI(
    title="Multi‑Modal Research Assistant",
    description="FastAPI backend for document ingestion and RAG pipeline",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://localhost:3000", "https://your-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)


# Register routers
app.include_router(documents_router, prefix="/api/documents", tags=["documents"])
app.include_router(rag_router, prefix="/api/rag", tags=["rag"])

# Health check endpoint (like Django's /health/)
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "FastAPI backend working"}

if __name__ == "__main__":
    # Render injects PORT into the environment
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)