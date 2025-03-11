import qrcode
from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Si el documento no tiene ID, guárdalo primero para generarlo
        if not self.pk:
            super().save(*args, **kwargs)

        # Generar la URL de validación basada en el ID del documento
        qr_url = f"http://127.0.0.1:8000/api/documents/validate/{self.pk}/"

        # Crear el código QR
        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        # Guardar la imagen QR en el campo qr_code
        self.qr_code.save(f"{self.pk}_qr.png", ContentFile(buffer.getvalue()), save=False)

        # Guardar nuevamente el modelo con el QR generado
        super().save(update_fields=['qr_code'])