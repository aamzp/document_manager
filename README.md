# 🧾 Document Manager MVP – Firma Digital y Validación por QR

Este proyecto es un **MVP (Producto Mínimo Viable)** desarrollado como una prueba técnica para **fortalecer habilidades en programación full stack**, específicamente orientado a la **gestión y validación de documentos** mediante firma digital y códigos QR.

---

## 🎯 Objetivo del Proyecto

Crear una plataforma básica que permita:

- 📤 Subir documentos firmados digitalmente
- 🔐 Generar una firma digital al momento de la subida
- 📎 Generar un código QR único para cada documento
- 📷 Escanear el QR con la cámara y verificar su validez
- ✅ Validar si el archivo ha sido alterado o no

---

## 📦 Versión

**v0.1-alpha** – Marzo 2025  
🔖 Estado: Funcional, con pruebas realizadas de validación real y escaneo QR.

---

## 🧱 Arquitectura del Proyecto

Este MVP utiliza una arquitectura desacoplada:

- **Backend (Django REST Framework)**  
  Encargado de:  
  - Autenticación por JWT  
  - Gestión de usuarios  
  - Subida y firma de documentos  
  - Validación de firmas  
  - Generación de QR

- **Frontend (React + TypeScript)**  
  Encargado de:  
  - Login y vista protegida para usuarios  
  - Subida de documentos  
  - Escáner QR vía webcam  
  - Visualización de la validación y detalles

Comunicación entre frontend y backend vía API RESTful.

---

## 🧪 Stack Tecnológico

| Lado       | Tecnología                  |
|------------|-----------------------------|
| Backend    | Django + Django REST Framework |
| Frontend   | React + TypeScript + Tailwind CSS |
| Firma Digital | `pycryptodome` con RSA 2048 bits |
| QR         | `qrcode` + `html5-qrcode` (Webcam) |
| Auth       | JWT (SimpleJWT) |
| Base de datos | SQLite (para pruebas locales) |

---

## 🚦 Cómo Funciona

1. El usuario inicia sesión como administrador.
2. Puede crear nuevos usuarios y subir documentos.
3. El sistema:
   - Genera una firma digital del archivo con una clave privada.
   - Genera un QR que apunta a `/validate/<id>` en el frontend.
4. Cualquier persona con el QR puede escanearlo y ver si el documento ha sido modificado.

---

## 📷 Verificación de Documentos por QR

- Desde la vista `/scan`, se activa la cámara del navegador.
- Al escanear el QR, redirige a `/validate/:id`.
- El sistema muestra si la firma digital coincide con el archivo.
- Si el documento fue alterado, se indica como **firma inválida ❌**.

---

## 🛑 Importante

Este proyecto es un **prototipo técnico de aprendizaje**. No está diseñado para ambientes productivos ni para asegurar documentos oficiales. Algunas cosas que **NO incluye**:

- Gestión avanzada de usuarios con permisos finos
- Interfaz protegida por HTTPS
- Certificados digitales reales
- Revisión externa de seguridad

---

## 👤 Autor

**Adolfo Maza**  
Ingeniero en Informática – Duoc UC  
Marzo 2025

---

## 📂 Instrucciones de instalación (modo desarrollo)

```
# 1. Clonar el repositorio
git clone <url-del-repo>
cd document_manager

# 2. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Correr migraciones y servidor
python manage.py migrate
python manage.py runserver
```
Para el frontend:
```
cd frontend
npm install
npm run dev
```
