from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rag.pipeline import run_rag_pipeline
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class health(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({"status": " backend working"})


# @method_decorator(csrf_exempt, nameDiaspatch)
class AskQuestion(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        question = request.data.get("question", "").strip()
        if not question:
            return Response({"answer": "No question provided."}, status=400)

        result = run_rag_pipeline(question)
        return Response(result, status=200)