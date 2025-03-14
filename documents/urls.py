from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )

from .views import (DocumentUploadView, 
                    validate_document, 
                    UserManagementView, 
                    UserDetailView,
                    AccessLogView,
                    DocumentListView,
                    DocumentDetailView
                    )

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/validate/<int:document_id>/', validate_document, name='validate-document'),
    path('users/', UserManagementView.as_view(), name='user-management'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('access-log/', AccessLogView.as_view(), name='access-log'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)