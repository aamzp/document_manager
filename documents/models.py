from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models

from io import BytesIO

import qrcode
import hashlib
import qrcode

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# Modelo para documentos

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    signature = models.TextField(blank=True, null=True)  # Almacena la firma digital
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guardar primero para obtener el ID

        # Leer el contenido del archivo
        with self.file.open('rb') as f:
            file_data = f.read()
        
        # Crear un hash del archivo
        file_hash = SHA256.new(file_data)

        # Firmar el hash con la clave privada
        with open("private.pem", "rb") as key_file:
            private_key = RSA.import_key(key_file.read())
            signature = pkcs1_15.new(private_key).sign(file_hash)

        # Guardar la firma en la base de datos
        self.signature = signature.hex()
        
        # Generar la URL de validación para el QR
        qr_url = f"http://127.0.0.1:8000/api/documents/validate/{self.pk}/"
        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        self.qr_code.save(f"{self.pk}_qr.png", ContentFile(buffer.getvalue()), save=False)

        super().save(update_fields=['qr_code', 'signature'])

# Modelo de usuario personalizado

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('editor', 'Editor'),
        ('user', 'Usuario Normal'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

# Modelo para registrar accesos

User = get_user_model()

class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)  # Tipo de acción (ej. "LOGIN", "VIEW_DOCUMENT", "UPLOAD_DOCUMENT")
    timestamp = models.DateTimeField(auto_now_add=True)  # Fecha y hora del evento
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # IP del usuario

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"