from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Document, CustomUser, AccessLog

# Serializador para documentos

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'qr_code', 'uploaded_at']

# Serializador para usuarios

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Para que la contraseña no se muestre en la API

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'password', 'date_joined']
    
    # Método para crear un usuario con contraseña encriptada
    def create(self, validated_data):
        """Crear un nuevo usuario con contraseña encriptada"""
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')  # Rol por defecto: 'user'
        )
        return user

# Serializador para obtener JWT

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Permitir login con email o username"""
    
    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")

        # Buscar por username o email
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.filter(username=username_or_email).first() or User.objects.filter(email=username_or_email).first()

        if user and user.check_password(password):
            attrs["username"] = user.username  # Convertir email en username para JWT
            return super().validate(attrs)

        raise serializers.ValidationError("Credenciales inválidas.")
    
# Serializador para registros de accesos

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Registra el acceso del usuario al iniciar sesión"""

    def validate(self, attrs):
        data = super().validate(attrs)

        # Guardar acceso en el historial
        AccessLog.objects.create(
            user=self.user,
            action="LOGIN",
            ip_address=self.context['request'].META.get('REMOTE_ADDR', '0.0.0.0')
        )

        return data
    
# Serializador para log de accesos

class AccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLog
        fields = ['user', 'action', 'timestamp', 'ip_address']
