# documents/views.py
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Document
from rag.document_utils import ingest_document
from rag.pipeline import run_rag_pipeline

class UploadDocumentView(APIView):
    permission_classes = []  # no login required

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded."}, status=400)

        doc = Document.objects.create(
            user=request.user if request.user.is_authenticated else None,
            file=file,
            title=file.name
        )

        # Save chunks into FAISS
        file_path = doc.file.path
        ingest_document(file_path)
        # if os.path.exists(file_path):
        #    os.remove(file_path)  # Clean up uploaded file after processing
        doc.file.delete(save=False)

        return Response({"status": "success", "document_id": doc.id}, status=200)

class AskQuestionView(APIView):
    permission_classes = []

    def post(self, request):
        question = request.data.get("question", "")
        if not question.strip():
            return Response({"answer": "Question is empty."}, status=400)

        result = run_rag_pipeline(question)
        return Response(result, status=200)