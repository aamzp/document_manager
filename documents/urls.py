from django.urls import path
from .views import DocumentUploadView, validate_document

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('validate/<int:document_id>/', validate_document, name='validate-document'),
]