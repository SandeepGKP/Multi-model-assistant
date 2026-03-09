# documents/views.py
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Document
from rag.document_utils import ingest_document
from rag.pipeline import run_rag_pipeline

import traceback

import shutil
from django.http import HttpResponse

def test_tesseract_view(request):
    path = shutil.which("tesseract")
    return HttpResponse(f"Tesseract path: {path}")


class UploadDocumentView(APIView):
    permission_classes = []

    def post(self, request):
        try:
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
            result = ingest_document(file_path)

            # Optional: delete file after embedding
            # os.remove(file_path)
            doc.file.delete(save=False)
            return Response({"status": "success", "document_id": doc.id, "result": result}, status=200)

        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)  # This will show the real error in Render logs
            return Response({"error": str(e), "trace": traceback_str}, status=500)

class AskQuestionView(APIView):
    permission_classes = []

    def post(self, request):
        question = request.data.get("question", "")
        if not question.strip():
            return Response({"answer": "Question is empty."}, status=400)

        result = run_rag_pipeline(question)
        return Response(result, status=200)