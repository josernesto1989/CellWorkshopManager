# 🔧 CellWorkshopManager

Sistema de gestión de inventario para talleres de celulares con autenticación JWT.

## 🚀 Características

- **Autenticación JWT**: Sistema de autenticación seguro con tokens
- **Gestión de Inventario**: Control completo de productos y stock
- **Múltiples Talleres**: Soporte para múltiples ubicaciones
- **Sistema de Roles**: Permisos granulares por usuario
- **Logs de Actividad**: Auditoría completa de cambios
- **API RESTful**: Interfaz completa para aplicaciones móviles y web

## 🔐 Autenticación JWT

El sistema utiliza autenticación JWT (JSON Web Tokens) para mayor seguridad:

### Endpoints de Autenticación

- `POST /api/usuarios/auth/login/` - Iniciar sesión
- `POST /api/usuarios/auth/refresh/` - Renovar token
- `POST /api/usuarios/auth/logout/` - Cerrar sesión
- `POST /api/usuarios/auth/register/` - Registrar usuario

### Ejemplo de Uso

```bash
# 1. Login
curl -X POST "http://localhost:8000/api/usuarios/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 2. Usar API con token
curl -X GET "http://localhost:8000/api/inventario/productos/" \
  -H "Authorization: Bearer <access_token>"
```

**Ver documentación completa en `JWT_AUTHENTICATION.md`**

## 📋 Requisitos

- Python 3.8+
- Django 5.2+
- Django REST Framework 3.16+
- djangorestframework-simplejwt 5.3+

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd CellWorkshopManager
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor**
```bash
python manage.py runserver
```

## 🧪 Pruebas

Ejecutar el script de prueba para verificar la autenticación JWT:

```bash
python test_jwt.py
```

## 📚 Documentación

- **API Documentation**: `API_DOCUMENTATION.md`
- **JWT Authentication**: `JWT_AUTHENTICATION.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Configuración JWT

La configuración JWT se encuentra en `cellworkshop_api/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

## 📱 Uso de la API

### Autenticación

1. **Login** para obtener tokens
2. **Incluir** `Authorization: Bearer <token>` en headers
3. **Renovar** token cuando expire
4. **Logout** para invalidar tokens

### Ejemplo con JavaScript

```javascript
// Login
const response = await fetch('/api/usuarios/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
});

const { access_token } = await response.json();

// Usar API
const productos = await fetch('/api/inventario/productos/', {
    headers: { 'Authorization': `Bearer ${access_token}` }
});
```

## 🏗️ Estructura del Proyecto

```
CellWorkshopManager/
├── cellworkshop_api/     # Configuración principal
├── inventario/          # Gestión de productos y stock
├── talleres/            # Gestión de talleres
├── usuarios/            # Autenticación y perfiles
├── logs/               # Sistema de auditoría
├── venv/               # Entorno virtual
├── requirements.txt    # Dependencias
├── API_DOCUMENTATION.md
├── JWT_AUTHENTICATION.md
└── README.md
```

## 🔒 Seguridad

- **JWT Tokens**: Autenticación stateless
- **Permisos Granulares**: Control por rol y taller
- **Auditoría**: Logs de todas las acciones
- **Validación**: Validación de datos en frontend y backend
- **HTTPS**: Recomendado para producción

## 🚀 Despliegue

Ver `DEPLOYMENT_GUIDE.md` para instrucciones detalladas de despliegue en producción.

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear un issue en GitHub
- Revisar la documentación en los archivos `.md`
- Consultar los logs del sistema

---

**¡Gracias por usar CellWorkshopManager! 🎉**
