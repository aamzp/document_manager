from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Document

# Vista para subir documentos
class DocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

# Vista para validar documentos
def validate_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return JsonResponse({
        "title": document.title,
        "file_url": document.file.url,
        "qr_code_url": document.qr_code.url,
        "uploaded_at": document.uploaded_at
    })