from rest_framework import generics

from .models import Document
from .serializers import DocumentSerializer

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import binascii

# Vista para subir documentos
class DocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

# Vista para validar documentos
def validate_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Leer el archivo para verificar la firma
    with document.file.open('rb') as f:
        file_data = f.read()

    # Crear hash del archivo
    file_hash = SHA256.new(file_data)

    # Cargar la clave pública
    with open("public.pem", "rb") as key_file:
        public_key = RSA.import_key(key_file.read())

    try:
        # Convertir la firma de hex a bytes
        signature_bytes = binascii.unhexlify(document.signature)
        # Verificar la firma
        pkcs1_15.new(public_key).verify(file_hash, signature_bytes)
        signature_valid = True
    except (ValueError, TypeError):
        signature_valid = False

    return JsonResponse({
        "title": document.title,
        "file_url": document.file.url,
        "qr_code_url": document.qr_code.url,
        "uploaded_at": document.uploaded_at,
        "signature_valid": signature_valid
    })