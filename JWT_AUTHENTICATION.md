# 🔐 JWT Authentication - CellWorkshopManager

Documentación completa de la autenticación JWT implementada en el sistema de gestión de inventario.

## 📋 Información General

- **Base URL**: `http://localhost:8000/api/usuarios/`
- **Formato**: JSON
- **Autenticación**: JWT (JSON Web Tokens)
- **Versión**: v1.0.0

## 🔑 Endpoints de Autenticación

### 1. Login (Iniciar Sesión)

**Endpoint:** `POST /api/usuarios/auth/login/`

**Cuerpo de la solicitud:**
```json
{
    "username": "admin",
    "password": "password123"
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/usuarios/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
```

**Respuesta exitosa (200):**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "perfil": {
            "id": 1,
            "rol": {
                "id": 1,
                "nombre": "ADMIN",
                "descripcion": "Administrador del sistema",
                "permisos_crear": true,
                "permisos_editar": true,
                "permisos_eliminar": true,
                "permisos_ver_logs": true,
                "permisos_administrar_usuarios": true
            },
            "taller": {
                "id": 1,
                "nombre": "Taller Central",
                "direccion": "Calle Principal 123"
            },
            "telefono": "+1234567890",
            "direccion": "Dirección del usuario",
            "activo": true
        }
    }
}
```

### 2. Refresh Token (Renovar Token)

**Endpoint:** `POST /api/usuarios/auth/refresh/`

**Cuerpo de la solicitud:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/usuarios/auth/refresh/" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Respuesta exitosa (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Logout (Cerrar Sesión)

**Endpoint:** `POST /api/usuarios/auth/logout/`

**Headers requeridos:** `Authorization: Bearer <access_token>`

**Cuerpo de la solicitud:**
```json
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/usuarios/auth/logout/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Respuesta exitosa (200):**
```json
{
    "message": "Logout exitoso"
}
```

### 4. Register (Registro de Usuario)

**Endpoint:** `POST /api/usuarios/auth/register/`

**Cuerpo de la solicitud:**
```json
{
    "username": "nuevo_usuario",
    "email": "nuevo@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Nuevo",
    "last_name": "Usuario",
    "perfil": {
        "rol_id": 2,
        "taller_id": 1,
        "telefono": "+1234567890",
        "direccion": "Dirección del nuevo usuario"
    }
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/usuarios/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "email": "nuevo@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Nuevo",
    "last_name": "Usuario",
    "perfil": {
        "rol_id": 2,
        "taller_id": 1,
        "telefono": "+1234567890",
        "direccion": "Dirección del nuevo usuario"
    }
  }'
```

**Respuesta exitosa (201):**
```json
{
    "message": "Usuario registrado exitosamente",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 2,
        "username": "nuevo_usuario",
        "email": "nuevo@example.com",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "perfil": {
            "id": 2,
            "rol": {
                "id": 2,
                "nombre": "GERENTE"
            },
            "taller": {
                "id": 1,
                "nombre": "Taller Central"
            }
        }
    }
}
```

## 👤 Endpoints de Perfil de Usuario

### 1. Obtener Perfil

**Endpoint:** `GET /api/usuarios/profile/`

**Headers requeridos:** `Authorization: Bearer <access_token>`

**Ejemplo de solicitud:**
```bash
curl -X GET "http://localhost:8000/api/usuarios/profile/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
{
    "id": 1,
    "rol": {
        "id": 1,
        "nombre": "ADMIN",
        "descripcion": "Administrador del sistema"
    },
    "taller": {
        "id": 1,
        "nombre": "Taller Central",
        "direccion": "Calle Principal 123"
    },
    "telefono": "+1234567890",
    "direccion": "Dirección del usuario",
    "fecha_nacimiento": null,
    "fecha_contratacion": "2024-01-01",
    "activo": true,
    "fecha_creacion": "2024-01-01T00:00:00Z",
    "fecha_actualizacion": "2024-01-01T00:00:00Z"
}
```

### 2. Actualizar Perfil

**Endpoint:** `PUT /api/usuarios/profile/update/`

**Headers requeridos:** `Authorization: Bearer <access_token>`

**Cuerpo de la solicitud:**
```json
{
    "telefono": "+9876543210",
    "direccion": "Nueva dirección",
    "rol_id": 2,
    "taller_id": 1
}
```

**Ejemplo de solicitud:**
```bash
curl -X PUT "http://localhost:8000/api/usuarios/profile/update/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{
    "telefono": "+9876543210",
    "direccion": "Nueva dirección",
    "rol_id": 2,
    "taller_id": 1
  }'
```

### 3. Cambiar Contraseña

**Endpoint:** `POST /api/usuarios/profile/change-password/`

**Headers requeridos:** `Authorization: Bearer <access_token>`

**Cuerpo de la solicitud:**
```json
{
    "old_password": "password123",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/usuarios/profile/change-password/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{
    "old_password": "password123",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
  }'
```

**Respuesta exitosa (200):**
```json
{
    "message": "Contraseña cambiada exitosamente"
}
```

### 4. Obtener Permisos

**Endpoint:** `GET /api/usuarios/permissions/`

**Headers requeridos:** `Authorization: Bearer <access_token>`

**Ejemplo de solicitud:**
```bash
curl -X GET "http://localhost:8000/api/usuarios/permissions/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Respuesta exitosa (200):**
```json
{
    "puede_crear": true,
    "puede_editar": true,
    "puede_eliminar": true,
    "puede_ver_logs": true,
    "puede_administrar_usuarios": true,
    "rol": "ADMIN",
    "taller": "Taller Central"
}
```

## 🔧 Uso de Tokens en APIs

### Autenticación en Requests

Para usar las APIs protegidas, incluye el token de acceso en el header `Authorization`:

```bash
curl -X GET "http://localhost:8000/api/inventario/productos/" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### Flujo de Autenticación

1. **Login**: Obtener `access_token` y `refresh_token`
2. **Usar APIs**: Incluir `access_token` en header `Authorization`
3. **Token expirado**: Usar `refresh_token` para obtener nuevo `access_token`
4. **Logout**: Invalidar `refresh_token`

## ⚙️ Configuración JWT

### Configuración en settings.py

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Características de Seguridad

- **Access Token**: Válido por 1 hora
- **Refresh Token**: Válido por 7 días
- **Rotación automática**: Los refresh tokens se renuevan automáticamente
- **Blacklist**: Los tokens invalidados se agregan a una lista negra
- **Algoritmo**: HS256 para firma de tokens

## 📱 Ejemplos de Uso con JavaScript

### Usando Fetch API

```javascript
// Configuración base
const BASE_URL = 'http://localhost:8000/api';
let accessToken = null;
let refreshToken = null;

// Login
async function login(username, password) {
    const response = await fetch(`${BASE_URL}/usuarios/auth/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    accessToken = data.access_token;
    refreshToken = data.refresh_token;
    
    return data;
}

// Función para hacer requests autenticados
async function authenticatedRequest(url, options = {}) {
    if (!accessToken) {
        throw new Error('No hay token de acceso');
    }
    
    const response = await fetch(url, {
        ...options,
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            ...options.headers
        }
    });
    
    // Si el token expiró, intentar renovarlo
    if (response.status === 401) {
        await refreshAccessToken();
        return authenticatedRequest(url, options);
    }
    
    return response;
}

// Renovar token
async function refreshAccessToken() {
    const response = await fetch(`${BASE_URL}/usuarios/auth/refresh/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh: refreshToken })
    });
    
    const data = await response.json();
    accessToken = data.access;
    refreshToken = data.refresh;
}

// Ejemplo de uso
async function getProductos() {
    const response = await authenticatedRequest(`${BASE_URL}/inventario/productos/`);
    return await response.json();
}

// Logout
async function logout() {
    await authenticatedRequest(`${BASE_URL}/usuarios/auth/logout/`, {
        method: 'POST',
        body: JSON.stringify({ refresh_token: refreshToken })
    });
    
    accessToken = null;
    refreshToken = null;
}
```

### Usando Axios

```javascript
import axios from 'axios';

// Configuración base
const api = axios.create({
    baseURL: 'http://localhost:8000/api'
});

// Interceptor para agregar token
api.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Interceptor para manejar errores de token
api.interceptors.response.use(
    response => response,
    async error => {
        if (error.response.status === 401) {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                try {
                    const response = await axios.post('/api/usuarios/auth/refresh/', {
                        refresh: refreshToken
                    });
                    
                    localStorage.setItem('access_token', response.data.access);
                    localStorage.setItem('refresh_token', response.data.refresh);
                    
                    // Reintentar request original
                    error.config.headers.Authorization = `Bearer ${response.data.access}`;
                    return axios.request(error.config);
                } catch (refreshError) {
                    // Token de refresh expirado, redirigir a login
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    window.location.href = '/login';
                }
            }
        }
        return Promise.reject(error);
    }
);

// Funciones de autenticación
export const authAPI = {
    login: (credentials) => api.post('/usuarios/auth/login/', credentials),
    register: (userData) => api.post('/usuarios/auth/register/', userData),
    logout: (refreshToken) => api.post('/usuarios/auth/logout/', { refresh_token: refreshToken }),
    refresh: (refreshToken) => api.post('/usuarios/auth/refresh/', { refresh: refreshToken }),
    getProfile: () => api.get('/usuarios/profile/'),
    updateProfile: (data) => api.put('/usuarios/profile/update/', data),
    changePassword: (data) => api.post('/usuarios/profile/change-password/', data),
    getPermissions: () => api.get('/usuarios/permissions/')
};
```

## ⚠️ Errores Comunes

### Error de Token Requerido (401)
```json
{
    "error": "Token de autenticación requerido",
    "detail": "Debe incluir un token Bearer en el header Authorization"
}
```

### Error de Token Inválido (401)
```json
{
    "error": "Token inválido",
    "detail": "Token has expired"
}
```

### Error de Credenciales Inválidas (400)
```json
{
    "username": [
        "Credenciales inválidas"
    ]
}
```

### Error de Usuario Inactivo (400)
```json
{
    "username": [
        "Usuario inactivo"
    ]
}
```

## 🔒 Mejores Prácticas de Seguridad

1. **Almacenamiento seguro**: Guarda tokens en localStorage o sessionStorage
2. **Renovación automática**: Implementa renovación automática de tokens
3. **Logout seguro**: Siempre invalida refresh tokens al hacer logout
4. **HTTPS**: Usa HTTPS en producción
5. **Validación de tokens**: Valida tokens en el servidor
6. **Expiración corta**: Usa tiempos de expiración cortos para access tokens

## 🚀 Próximas Mejoras

- [ ] Implementar refresh token rotation
- [ ] Agregar rate limiting para endpoints de autenticación
- [ ] Implementar 2FA (Two-Factor Authentication)
- [ ] Agregar auditoría de sesiones
- [ ] Implementar logout en todos los dispositivos
- [ ] Agregar notificaciones de login sospechoso

---

**Para soporte técnico, consultar el README principal del proyecto.** 