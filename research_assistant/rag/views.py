from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rag.pipeline import run_rag_pipeline

class AskQuestion(APIView):
    permission_classes = []  # no login required

    def post(self, request):
        question = request.data.get("question", "").strip()
        if not question:
            return Response({"answer": "No question provided."}, status=400)
        
        result = run_rag_pipeline(question)
        return Response(result, status=200)