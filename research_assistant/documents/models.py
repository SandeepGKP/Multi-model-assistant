# documents/models.py
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    embedding = models.BinaryField()  # store vector
    page_number = models.IntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)  # store chunk text