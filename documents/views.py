from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes

from .models import Document, CustomUser, AccessLog
from .serializers import DocumentSerializer, UserSerializer, AccessLogSerializer
from .permissions import IsEditorOrAdmin, IsAdminUser

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import binascii

# Vista para subir documentos

class DocumentUploadView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEditorOrAdmin]

# Vista para visualizar documentos

class DocumentListView(generics.ListAPIView):
    queryset = Document.objects.all().order_by('-uploaded_at')  # Ordenado por fecha de subida
    serializer_class = DocumentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEditorOrAdmin]  

# Vistas para acciones específicas sobre un documento

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEditorOrAdmin]

    def retrieve(self, request, *args, **kwargs):
        document = self.get_object()

        # Guardar historial de accesos
        AccessLog.objects.create(
            user=request.user,
            document=document,
            action="viewed"
            # considera agregar más detalles relevantes si necesitas
        )

        serializer = self.get_serializer(document)
        return Response(serializer.data)

# Vista para validar documentos

@api_view(['GET'])
@permission_classes([AllowAny])  # Solo editores y administradores

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


# Vista para gestión de usuarios

class UserManagementView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# Vista para crear, editar y eliminar usuarios

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# Vista para registro de accesos

class DocumentDetailView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEditorOrAdmin]

    def retrieve(self, request, *args, **kwargs):
        document = self.get_object()

        # Guardar en el historial de accesos
        AccessLog.objects.create(
            user=request.user,
            action=f"VIEW_DOCUMENT {document.id}",
            ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0')
        )

        return super().retrieve(request, *args, **kwargs)

# Vista para visualización de historial de accesos

class AccessLogView(generics.ListAPIView):
    queryset = AccessLog.objects.all().order_by('-timestamp')
    serializer_class = AccessLogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]