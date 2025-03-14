from django.contrib.auth import get_user_model

from rest_framework import serializers
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import binascii

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Document, CustomUser, AccessLog

# Serializador para documentos

class DocumentSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()
    signature_valid = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'qr_code_url', 'signature', 'signature_valid', 'uploaded_at']

    # Método para obtener la URL del código QR
    def get_qr_code_url(self, obj):
        if obj.qr_code and hasattr(obj.qr_code, 'url'):
            request = self.context.get('request', None)
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
            return obj.qr_code.url  # Devolver la URL aunque no haya request
        return None
    # Método para obtener la URL del archivo
    def get_file_url(self, obj):
        if obj.file and hasattr(obj.file, 'url'):
            request = self.context.get('request', None)
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url  # En caso de que no haya request
        return None
    # Método para verificar si la firma es válida
    def get_signature_valid(self, obj):
        """ Verifica si la firma almacenada en 'signature' es válida. """
        if not obj.signature:
            return False  # Si no hay firma, se considera inválida

        try:
            # Leer el contenido del archivo
            with obj.file.open('rb') as f:
                file_data = f.read()

            # Crear un hash del archivo
            file_hash = SHA256.new(file_data)

            # Cargar la clave pública
            with open("public.pem", "rb") as key_file:
                public_key = RSA.import_key(key_file.read())

            # Verificar la firma
            signature_bytes = binascii.unhexlify(obj.signature)
            pkcs1_15.new(public_key).verify(file_hash, signature_bytes)
            return True  # Firma válida
        except (ValueError, TypeError):
            return False  # Firma inválida    
    
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
