import shutil
from django.http import HttpResponse

def test_tesseract_view(request):
    path = shutil.which("tesseract")
    return HttpResponse(f"Tesseract path: {path}")