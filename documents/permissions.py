from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """Permite acceso solo a administradores."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsEditorOrAdmin(BasePermission):
    """Permite acceso a editores y administradores."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'editor']
