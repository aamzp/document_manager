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
        # Generar QR basado en la URL del documento
        qr = qrcode.make(f"http://127.0.0.1:8000/media/{self.file}")
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        self.qr_code.save(f"{self.title}_qr.png", ContentFile(buffer.getvalue()), save=False)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title