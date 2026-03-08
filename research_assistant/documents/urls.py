

from django.urls import path
from .views import UploadDocumentView
from .test_tesseract_view import test_tesseract_view
urlpatterns = [
    path("upload/", UploadDocumentView.as_view(), name="upload"),
    path("tesseract_view/",test_tesseract_view)
]