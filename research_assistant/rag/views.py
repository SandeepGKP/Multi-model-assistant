from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rag.pipeline import run_rag_pipeline
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import traceback

@method_decorator(csrf_exempt, name="dispatch")
class health(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({"status": " backend working"})


# @method_decorator(csrf_exempt, nameDiaspatch)
class AskQuestion(APIView):
    def post(self, request):
        try:
            question = request.data.get("question")
            answer = run_rag_pipeline(question)
            return Response({"answer": answer})
        except Exception as e:
            print("🔥 ERROR START 🔥")
            traceback.print_exc()
            print("🔥 ERROR END 🔥")
            return Response({"error": str(e)}, status=500)