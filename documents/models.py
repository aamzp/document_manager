import qrcode
import hashlib
import qrcode

from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


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