# 🔌 API Documentation - CellWorkshopManager

Documentación completa de las APIs RESTful para el sistema de gestión de inventario de talleres de celulares.

## 📋 Información General

- **Base URL**: `http://localhost:8000/api/inventario/`
- **Formato**: JSON
- **Autenticación**: Session Authentication / Basic Authentication
- **Versión**: v1.0.0

## 🔐 Autenticación

### Session Authentication (Recomendado para navegador)
```bash
# Primero hacer login en /admin/
# Luego las cookies de sesión se usarán automáticamente
```

### Basic Authentication (Para aplicaciones)
```bash
curl -X GET "http://localhost:8000/api/inventario/productos/" \
  -H "Authorization: Basic $(echo -n 'username:password' | base64)"
```

## 📦 Endpoints de Productos

### 1. Listar Productos

**Endpoint:** `GET /api/inventario/productos/`

**Parámetros de consulta:**
- `taller` (opcional): ID del taller para filtrar
- `page` (opcional): Número de página para paginación
- `search` (opcional): Búsqueda por modelo o descripción

**Ejemplo de solicitud:**
```bash
curl -X GET "http://localhost:8000/api/inventario/productos/?taller=1&page=1" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

**Respuesta exitosa (200):**
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/inventario/productos/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "taller": {
                "id": 1,
                "nombre": "Taller Central"
            },
            "modelo": "iPhone 12 Pantalla",
            "descripcion": "Pantalla de repuesto para iPhone 12",
            "cantidad": 10,
            "cantidad_minima": 2,
            "precio_costo": 25000,
            "precio_venta": 40000,
            "fecha_ingreso": "2025-07-18T12:00:00Z",
            "etiquetas": [
                {
                    "id": 1,
                    "nombre": "Pantallas"
                }
            ]
        }
    ]
}
```

### 2. Crear Producto

**Endpoint:** `POST /api/inventario/productos/`

**Permisos requeridos:** `crear`

**Cuerpo de la solicitud:**
```json
{
    "taller_id": 1,
    "modelo": "Samsung S21 Batería",
    "descripcion": "Batería original Samsung S21",
    "cantidad": 5,
    "cantidad_minima": 1,
    "precio_costo": 12000,
    "precio_venta": 20000,
    "etiquetas_ids": [2, 3]
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/inventario/productos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)" \
  -d '{
    "taller_id": 1,
    "modelo": "Samsung S21 Batería",
    "descripcion": "Batería original Samsung S21",
    "cantidad": 5,
    "cantidad_minima": 1,
    "precio_costo": 12000,
    "precio_venta": 20000,
    "etiquetas_ids": [2, 3]
  }'
```

**Respuesta exitosa (201):**
```json
{
    "id": 2,
    "taller": {
        "id": 1,
        "nombre": "Taller Central"
    },
    "modelo": "Samsung S21 Batería",
    "descripcion": "Batería original Samsung S21",
    "cantidad": 5,
    "cantidad_minima": 1,
    "precio_costo": 12000,
    "precio_venta": 20000,
    "fecha_ingreso": "2025-07-19T10:30:00Z",
    "etiquetas": [
        {
            "id": 2,
            "nombre": "Baterías"
        },
        {
            "id": 3,
            "nombre": "Cables"
        }
    ]
}
```

### 3. Ver Producto Específico

**Endpoint:** `GET /api/inventario/productos/{id}/`

**Ejemplo de solicitud:**
```bash
curl -X GET "http://localhost:8000/api/inventario/productos/1/" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

**Respuesta exitosa (200):**
```json
{
    "id": 1,
    "taller": {
        "id": 1,
        "nombre": "Taller Central"
    },
    "modelo": "iPhone 12 Pantalla",
    "descripcion": "Pantalla de repuesto para iPhone 12",
    "cantidad": 10,
    "cantidad_minima": 2,
    "precio_costo": 25000,
    "precio_venta": 40000,
    "fecha_ingreso": "2025-07-18T12:00:00Z",
    "etiquetas": [
        {
            "id": 1,
            "nombre": "Pantallas"
        }
    ]
}
```

### 4. Actualizar Producto

**Endpoint:** `PUT /api/inventario/productos/{id}/`

**Permisos requeridos:** `editar`

**Cuerpo de la solicitud:**
```json
{
    "taller_id": 1,
    "modelo": "iPhone 12 Pantalla Premium",
    "descripcion": "Pantalla de repuesto premium para iPhone 12",
    "cantidad": 15,
    "cantidad_minima": 3,
    "precio_costo": 28000,
    "precio_venta": 45000,
    "etiquetas_ids": [1, 4]
}
```

**Ejemplo de solicitud:**
```bash
curl -X PUT "http://localhost:8000/api/inventario/productos/1/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)" \
  -d '{
    "taller_id": 1,
    "modelo": "iPhone 12 Pantalla Premium",
    "descripcion": "Pantalla de repuesto premium para iPhone 12",
    "cantidad": 15,
    "cantidad_minima": 3,
    "precio_costo": 28000,
    "precio_venta": 45000,
    "etiquetas_ids": [1, 4]
  }'
```

### 5. Eliminar Producto

**Endpoint:** `DELETE /api/inventario/productos/{id}/`

**Permisos requeridos:** `eliminar`

**Ejemplo de solicitud:**
```bash
curl -X DELETE "http://localhost:8000/api/inventario/productos/1/" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

**Respuesta exitosa (204):** Sin contenido

## 📊 Operaciones de Inventario

### 1. Adicionar Stock

**Endpoint:** `POST /api/inventario/productos/{id}/adicionar-stock/`

**Permisos requeridos:** `editar`

**Cuerpo de la solicitud:**
```json
{
    "cantidad": 10,
    "motivo": "Compra de proveedor XYZ"
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/inventario/productos/1/adicionar-stock/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)" \
  -d '{
    "cantidad": 10,
    "motivo": "Compra de proveedor XYZ"
  }'
```

**Respuesta exitosa (200):**
```json
{
    "message": "Stock adicionado exitosamente. Nueva cantidad: 25",
    "cantidad_anterior": 15,
    "cantidad_nueva": 25,
    "cantidad_adicionada": 10
}
```

### 2. Rebajar Stock

**Endpoint:** `POST /api/inventario/productos/{id}/rebajar-stock/`

**Permisos requeridos:** `editar`

**Cuerpo de la solicitud:**
```json
{
    "cantidad": 5,
    "motivo": "Venta al cliente Juan Pérez"
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/inventario/productos/1/rebajar-stock/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)" \
  -d '{
    "cantidad": 5,
    "motivo": "Venta al cliente Juan Pérez"
  }'
```

**Respuesta exitosa (200):**
```json
{
    "message": "Stock rebajado exitosamente. Nueva cantidad: 20",
    "cantidad_anterior": 25,
    "cantidad_nueva": 20,
    "cantidad_rebajada": 5
}
```

**Error de stock insuficiente (400):**
```json
{
    "cantidad": [
        "No hay suficiente stock. Disponible: 20, Solicitado: 25"
    ]
}
```

### 3. Trasladar Stock

**Endpoint:** `POST /api/inventario/productos/{id}/trasladar-stock/`

**Permisos requeridos:** `editar`

**Cuerpo de la solicitud:**
```json
{
    "taller_destino_id": 2,
    "cantidad": 3,
    "motivo": "Traslado por alta demanda en taller norte"
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/inventario/productos/1/trasladar-stock/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)" \
  -d '{
    "taller_destino_id": 2,
    "cantidad": 3,
    "motivo": "Traslado por alta demanda en taller norte"
  }'
```

**Respuesta exitosa (200):**
```json
{
    "message": "Stock trasladado exitosamente",
    "taller_origen": "Taller Central",
    "taller_destino": "Taller Norte",
    "cantidad_trasladada": 3,
    "stock_restante_origen": 17,
    "stock_total_destino": 8
}
```

**Error de taller no encontrado (404):**
```json
{
    "error": "Taller de destino no encontrado"
}
```

### 4. Productos con Stock Bajo

**Endpoint:** `GET /api/inventario/productos/stock-bajo/`

**Ejemplo de solicitud:**
```bash
curl -X GET "http://localhost:8000/api/inventario/productos/stock-bajo/" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

**Respuesta exitosa (200):**
```json
[
    {
        "id": 3,
        "taller": {
            "id": 1,
            "nombre": "Taller Central"
        },
        "modelo": "Cable USB-C",
        "descripcion": "Cable de carga USB-C universal",
        "cantidad": 3,
        "cantidad_minima": 5,
        "precio_costo": 2000,
        "precio_venta": 5000,
        "fecha_ingreso": "2025-07-18T12:00:00Z",
        "etiquetas": [
            {
                "id": 3,
                "nombre": "Cables"
            }
        ]
    }
]
```

## 🏷️ Endpoints de Etiquetas

### 1. Listar Etiquetas

**Endpoint:** `GET /api/inventario/etiquetas/`

**Ejemplo de solicitud:**
```bash
curl -X GET "http://localhost:8000/api/inventario/etiquetas/" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

**Respuesta exitosa (200):**
```json
[
    {
        "id": 1,
        "nombre": "Pantallas"
    },
    {
        "id": 2,
        "nombre": "Baterías"
    },
    {
        "id": 3,
        "nombre": "Cables"
    }
]
```

### 2. Crear Etiqueta

**Endpoint:** `POST /api/inventario/etiquetas/`

**Permisos requeridos:** `crear`

**Cuerpo de la solicitud:**
```json
{
    "nombre": "Herramientas"
}
```

**Ejemplo de solicitud:**
```bash
curl -X POST "http://localhost:8000/api/inventario/etiquetas/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)" \
  -d '{
    "nombre": "Herramientas"
  }'
```

**Respuesta exitosa (201):**
```json
{
    "id": 4,
    "nombre": "Herramientas"
}
```

### 3. Actualizar Etiqueta

**Endpoint:** `PUT /api/inventario/etiquetas/{id}/`

**Permisos requeridos:** `editar`

**Cuerpo de la solicitud:**
```json
{
    "nombre": "Herramientas y Accesorios"
}
```

**Ejemplo de solicitud:**
```bash
curl -X PUT "http://localhost:8000/api/inventario/etiquetas/4/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)" \
  -d '{
    "nombre": "Herramientas y Accesorios"
  }'
```

### 4. Eliminar Etiqueta

**Endpoint:** `DELETE /api/inventario/etiquetas/{id}/`

**Permisos requeridos:** `eliminar`

**Ejemplo de solicitud:**
```bash
curl -X DELETE "http://localhost:8000/api/inventario/etiquetas/4/" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

## 📝 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado exitosamente |
| 204 | No Content - Recurso eliminado exitosamente |
| 400 | Bad Request - Datos de entrada inválidos |
| 401 | Unauthorized - Autenticación requerida |
| 403 | Forbidden - Permisos insuficientes |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

## ⚠️ Errores Comunes

### Error de Autenticación (401)
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Error de Permisos (403)
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### Error de Validación (400)
```json
{
    "cantidad": [
        "La cantidad debe ser mayor a 0"
    ],
    "taller_id": [
        "This field is required."
    ]
}
```

### Error de Stock Insuficiente (400)
```json
{
    "cantidad": [
        "No hay suficiente stock. Disponible: 10, Solicitado: 15"
    ]
}
```

## 🔧 Ejemplos de Uso con JavaScript

### Usando Fetch API
```javascript
// Configuración base
const BASE_URL = 'http://localhost:8000/api/inventario';
const credentials = btoa('admin:password');

// Listar productos
async function getProductos() {
    const response = await fetch(`${BASE_URL}/productos/`, {
        headers: {
            'Authorization': `Basic ${credentials}`,
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
}

// Crear producto
async function crearProducto(producto) {
    const response = await fetch(`${BASE_URL}/productos/`, {
        method: 'POST',
        headers: {
            'Authorization': `Basic ${credentials}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(producto)
    });
    return await response.json();
}

// Adicionar stock
async function adicionarStock(productoId, cantidad, motivo) {
    const response = await fetch(`${BASE_URL}/productos/${productoId}/adicionar-stock/`, {
        method: 'POST',
        headers: {
            'Authorization': `Basic ${credentials}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cantidad, motivo })
    });
    return await response.json();
}
```

### Usando Axios
```javascript
import axios from 'axios';

// Configuración base
const api = axios.create({
    baseURL: 'http://localhost:8000/api/inventario',
    auth: {
        username: 'admin',
        password: 'password'
    }
});

// Listar productos
const getProductos = () => api.get('/productos/');

// Crear producto
const crearProducto = (producto) => api.post('/productos/', producto);

// Adicionar stock
const adicionarStock = (productoId, cantidad, motivo) => 
    api.post(`/productos/${productoId}/adicionar-stock/`, { cantidad, motivo });
```

## 📊 Monitoreo y Logs

### Ver Logs de Acciones
```bash
curl -X GET "http://localhost:8000/admin/logs/logaccion/" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

### Ver Logs de Inventario
```bash
curl -X GET "http://localhost:8000/admin/logs/loginventario/" \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

## 🚀 Próximas Funcionalidades

- [ ] Autenticación JWT
- [ ] Filtros avanzados por fecha
- [ ] Exportación de datos a CSV/Excel
- [ ] Notificaciones en tiempo real
- [ ] Dashboard con estadísticas
- [ ] API para reportes personalizados

---

**Para soporte técnico, consultar el README principal del proyecto.** 