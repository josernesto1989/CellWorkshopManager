# 🏭 CellWorkshopManager

Sistema de gestión de inventario para talleres de reparación de celulares con múltiples sucursales, control de acceso por roles y auditoría completa de operaciones.

## 📋 Características Principales

### 🏢 Gestión Multi-Taller
- **Múltiples talleres**: Cada taller tiene su propio inventario independiente
- **Traslados entre talleres**: Sistema de traslado de productos entre sucursales
- **Control por taller**: Usuarios pueden ser asignados a talleres específicos

### 📦 Gestión de Inventario
- **Productos por taller**: Cada producto pertenece a un taller específico
- **Control de stock**: Cantidad actual y cantidad mínima
- **Precios en centavos**: Evita problemas de precisión con decimales
- **Etiquetas**: Sistema de categorización de productos
- **Alertas de stock bajo**: Notificación cuando el stock está por debajo del mínimo

### 👥 Sistema de Usuarios y Roles
- **6 roles predefinidos**: Admin, Gerente, Técnico, Vendedor, Inventario, Auditor
- **Permisos granulares**: Crear, editar, eliminar, ver logs, administrar usuarios
- **Perfiles extendidos**: Información adicional de usuarios (teléfono, dirección, etc.)
- **Asignación por taller**: Usuarios pueden ser asignados a talleres específicos

### 📊 Auditoría y Logs
- **Logs automáticos**: Todas las acciones se registran automáticamente
- **Logs de inventario**: Seguimiento detallado de cambios en stock
- **Logs de acciones**: Registro de operaciones CRUD en todos los modelos
- **Trazabilidad completa**: Usuario, fecha, hora y motivo de cada cambio

### 🔌 APIs RESTful
- **Endpoints completos**: CRUD para productos y etiquetas
- **Operaciones de inventario**: Adicionar, rebajar y trasladar stock
- **Autenticación**: Sistema de autenticación y permisos
- **Validaciones**: Verificaciones de stock antes de operaciones

## 🚀 Instalación

### Prerrequisitos
- Python 3.8+
- pip
- virtualenv (recomendado)

### Pasos de Instalación

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
pip install django djangorestframework
```

4. **Configurar la base de datos**
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

5. **Crear superusuario**
```bash
python3 manage.py createsuperuser
```

6. **Cargar datos de prueba (opcional)**
```bash
python3 manage.py loaddata fixtures_iniciales.json
```

7. **Ejecutar el servidor**
```bash
python3 manage.py runserver
```

## 📁 Estructura del Proyecto

```
CellWorkshopManager/
├── cellworkshop_api/          # Configuración principal de Django
├── talleres/                  # App de gestión de talleres
│   ├── models.py             # Modelo Taller
│   ├── admin.py              # Configuración del admin
│   └── migrations/           # Migraciones de base de datos
├── inventario/               # App de gestión de inventario
│   ├── models.py             # Modelos Producto y Etiqueta
│   ├── serializers.py        # Serializers para APIs
│   ├── views.py              # Vistas y ViewSets
│   ├── urls.py               # URLs de las APIs
│   ├── signals.py            # Signals para logs automáticos
│   ├── middleware.py         # Middleware para usuario actual
│   └── admin.py              # Configuración del admin
├── usuarios/                 # App de gestión de usuarios
│   ├── models.py             # Modelos Rol y PerfilUsuario
│   ├── utils.py              # Utilidades de permisos
│   ├── signals.py            # Signals para perfiles automáticos
│   └── admin.py              # Configuración del admin
├── logs/                     # App de auditoría
│   ├── models.py             # Modelos LogAccion y LogInventario
│   └── admin.py              # Configuración del admin
├── fixtures_iniciales.json   # Datos de prueba
└── manage.py                 # Script de gestión de Django
```

## 🗄️ Modelos de Datos

### Taller
- **nombre**: Nombre del taller
- **direccion**: Dirección física
- **telefono**: Teléfono de contacto (opcional)
- **email**: Email de contacto (opcional)
- **fecha_creacion**: Fecha de creación automática

### Producto
- **taller**: Relación con el taller al que pertenece
- **modelo**: Nombre/modelo del producto
- **descripcion**: Descripción detallada
- **cantidad**: Stock actual
- **cantidad_minima**: Stock mínimo recomendado
- **precio_costo**: Precio de costo en centavos
- **precio_venta**: Precio de venta en centavos
- **fecha_ingreso**: Fecha de ingreso automática
- **etiquetas**: Relación many-to-many con etiquetas

### Etiqueta
- **nombre**: Nombre de la etiqueta (único)

### Rol
- **nombre**: Tipo de rol (ADMIN, GERENTE, TECNICO, etc.)
- **descripcion**: Descripción del rol
- **permisos_***: Campos booleanos para cada permiso

### PerfilUsuario
- **usuario**: Relación one-to-one con User de Django
- **rol**: Rol asignado al usuario
- **taller**: Taller asignado al usuario
- **telefono**: Teléfono del usuario
- **direccion**: Dirección del usuario
- **fecha_nacimiento**: Fecha de nacimiento
- **fecha_contratacion**: Fecha de contratación
- **activo**: Estado activo/inactivo

### LogAccion
- **usuario**: Usuario que realizó la acción
- **tipo_accion**: Tipo de acción (CREAR, ACTUALIZAR, ELIMINAR, etc.)
- **modelo_afectado**: Nombre del modelo afectado
- **id_objeto**: ID del objeto afectado
- **descripcion**: Descripción detallada de la acción
- **fecha_accion**: Fecha y hora de la acción
- **ip_address**: Dirección IP del usuario

### LogInventario
- **producto**: Producto afectado
- **usuario**: Usuario que realizó el cambio
- **tipo_cambio**: Tipo de cambio (INGRESO, SALIDA, AJUSTE, TRASLADO)
- **cantidad_anterior**: Cantidad antes del cambio
- **cantidad_nueva**: Cantidad después del cambio
- **cantidad_cambiada**: Diferencia (positiva/negativa)
- **motivo**: Motivo del cambio
- **fecha_cambio**: Fecha y hora del cambio

## 🔐 Sistema de Roles y Permisos

### Roles Disponibles

1. **ADMIN**: Acceso completo al sistema
   - Todos los permisos habilitados
   - Puede administrar usuarios y roles
   - Acceso a todos los talleres

2. **GERENTE**: Gestión de taller
   - Crear y editar productos
   - Ver logs del sistema
   - No puede eliminar registros
   - No puede administrar usuarios

3. **TECNICO**: Operaciones técnicas
   - Solo puede editar productos
   - No puede crear ni eliminar
   - No puede ver logs

4. **VENDEDOR**: Operaciones de venta
   - Rebajar stock por ventas
   - Ver productos disponibles

5. **INVENTARIO**: Gestión de inventario
   - Adicionar y ajustar stock
   - Crear y editar productos
   - Ver logs de inventario

6. **AUDITOR**: Solo consulta
   - Ver todos los datos
   - Ver logs del sistema
   - No puede modificar nada

### Permisos Disponibles
- **crear**: Crear nuevos registros
- **editar**: Editar registros existentes
- **eliminar**: Eliminar registros
- **ver_logs**: Ver logs del sistema
- **administrar_usuarios**: Gestionar usuarios y roles

## 🔌 APIs RESTful

### Autenticación
Todas las APIs requieren autenticación. Se soportan:
- **Session Authentication**: Para uso desde navegador
- **Basic Authentication**: Para uso desde aplicaciones

### Endpoints de Productos

#### Listar Productos
```http
GET /api/inventario/productos/
```

**Parámetros de consulta:**
- `taller`: Filtrar por ID de taller
- `page`: Número de página para paginación

**Respuesta:**
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/inventario/productos/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "taller": {"id": 1, "nombre": "Taller Central"},
            "modelo": "iPhone 12 Pantalla",
            "descripcion": "Pantalla de repuesto para iPhone 12",
            "cantidad": 10,
            "cantidad_minima": 2,
            "precio_costo": 25000,
            "precio_venta": 40000,
            "fecha_ingreso": "2025-07-18T12:00:00Z",
            "etiquetas": [{"id": 1, "nombre": "Pantallas"}]
        }
    ]
}
```

#### Crear Producto
```http
POST /api/inventario/productos/
Content-Type: application/json

{
    "taller_id": 1,
    "modelo": "Samsung S21 Batería",
    "descripcion": "Batería original Samsung S21",
    "cantidad": 5,
    "cantidad_minima": 1,
    "precio_costo": 12000,
    "precio_venta": 20000,
    "etiquetas_ids": [2]
}
```

#### Ver Producto
```http
GET /api/inventario/productos/1/
```

#### Actualizar Producto
```http
PUT /api/inventario/productos/1/
Content-Type: application/json

{
    "taller_id": 1,
    "modelo": "Samsung S21 Batería",
    "descripcion": "Batería original Samsung S21 actualizada",
    "cantidad": 8,
    "cantidad_minima": 2,
    "precio_costo": 12000,
    "precio_venta": 22000,
    "etiquetas_ids": [2, 3]
}
```

#### Eliminar Producto
```http
DELETE /api/inventario/productos/1/
```

#### Adicionar Stock
```http
POST /api/inventario/productos/1/adicionar-stock/
Content-Type: application/json

{
    "cantidad": 10,
    "motivo": "Compra de proveedor"
}
```

**Respuesta:**
```json
{
    "message": "Stock adicionado exitosamente. Nueva cantidad: 20",
    "cantidad_anterior": 10,
    "cantidad_nueva": 20,
    "cantidad_adicionada": 10
}
```

#### Rebajar Stock
```http
POST /api/inventario/productos/1/rebajar-stock/
Content-Type: application/json

{
    "cantidad": 5,
    "motivo": "Venta al cliente"
}
```

**Respuesta:**
```json
{
    "message": "Stock rebajado exitosamente. Nueva cantidad: 15",
    "cantidad_anterior": 20,
    "cantidad_nueva": 15,
    "cantidad_rebajada": 5
}
```

#### Trasladar Stock
```http
POST /api/inventario/productos/1/trasladar-stock/
Content-Type: application/json

{
    "taller_destino_id": 2,
    "cantidad": 3,
    "motivo": "Traslado por demanda"
}
```

**Respuesta:**
```json
{
    "message": "Stock trasladado exitosamente",
    "taller_origen": "Taller Central",
    "taller_destino": "Taller Norte",
    "cantidad_trasladada": 3,
    "stock_restante_origen": 12,
    "stock_total_destino": 8
}
```

#### Productos con Stock Bajo
```http
GET /api/inventario/productos/stock-bajo/
```

### Endpoints de Etiquetas

#### Listar Etiquetas
```http
GET /api/inventario/etiquetas/
```

#### Crear Etiqueta
```http
POST /api/inventario/etiquetas/
Content-Type: application/json

{
    "nombre": "Cables"
}
```

#### Actualizar Etiqueta
```http
PUT /api/inventario/etiquetas/1/
Content-Type: application/json

{
    "nombre": "Cables y Accesorios"
}
```

#### Eliminar Etiqueta
```http
DELETE /api/inventario/etiquetas/1/
```

## 🛠️ Uso del Sistema

### 1. Configuración Inicial

1. **Crear talleres** desde el admin de Django
2. **Crear roles** con los permisos necesarios
3. **Crear usuarios** y asignarles roles y talleres
4. **Crear etiquetas** para categorizar productos

### 2. Gestión de Inventario

#### Desde el Admin de Django
- Acceder a `/admin/` con credenciales de superusuario
- Navegar a las secciones de Productos, Etiquetas, etc.
- Todas las operaciones generan logs automáticamente

#### Desde las APIs
- Usar los endpoints RESTful para operaciones programáticas
- Autenticarse con las credenciales del usuario
- Verificar permisos antes de realizar operaciones

### 3. Monitoreo y Auditoría

#### Ver Logs de Acciones
- Ir a `/admin/logs/logaccion/` para ver todos los logs
- Filtrar por usuario, tipo de acción, modelo, etc.

#### Ver Logs de Inventario
- Ir a `/admin/logs/loginventario/` para ver cambios de stock
- Filtrar por producto, tipo de cambio, fecha, etc.

#### Productos con Stock Bajo
- Usar el endpoint `/api/inventario/productos/stock-bajo/`
- O filtrar en el admin por cantidad <= cantidad_minima

## 🔧 Configuración Avanzada

### Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Configuración de Base de Datos
Para usar PostgreSQL o MySQL, modificar `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cellworkshop_db',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Configuración de Logs
Para configurar logs personalizados, agregar en `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🧪 Testing

### Ejecutar Tests
```bash
python3 manage.py test
```

### Tests Específicos
```bash
python3 manage.py test inventario.tests
python3 manage.py test usuarios.tests
```

## 📊 Reportes y Estadísticas

### Consultas Útiles

#### Productos por Taller
```python
from inventario.models import Producto
from django.db.models import Count, Sum

# Productos por taller
productos_por_taller = Producto.objects.values('taller__nombre').annotate(
    total_productos=Count('id'),
    stock_total=Sum('cantidad')
)
```

#### Movimientos de Inventario
```python
from logs.models import LogInventario
from django.db.models import Sum

# Movimientos por tipo
movimientos = LogInventario.objects.values('tipo_cambio').annotate(
    total_movimientos=Count('id'),
    cantidad_total=Sum('cantidad_cambiada')
)
```

#### Usuarios por Rol
```python
from usuarios.models import PerfilUsuario
from django.db.models import Count

usuarios_por_rol = PerfilUsuario.objects.values('rol__nombre').annotate(
    total_usuarios=Count('id')
)
```

## 🚨 Troubleshooting

### Problemas Comunes

#### Error de Middleware
Si aparece el error `'WSGIRequest' object has no attribute 'user'`:
1. Verificar que `CurrentUserMiddleware` esté después de `AuthenticationMiddleware`
2. Reiniciar el servidor de desarrollo

#### Logs No Se Generan
1. Verificar que los signals estén registrados en `apps.py`
2. Comprobar que el middleware esté funcionando
3. Verificar que el usuario esté autenticado

#### APIs No Responden
1. Verificar autenticación
2. Comprobar permisos del usuario
3. Revisar logs del servidor

### Logs de Debug
Para activar logs detallados, agregar en `settings.py`:

```python
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'inventario': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo
- Revisar la documentación de Django y Django REST Framework

## 🔄 Changelog

### v1.0.0 (2025-07-19)
- ✅ Sistema multi-taller
- ✅ Gestión de inventario completa
- ✅ Sistema de roles y permisos
- ✅ APIs RESTful
- ✅ Auditoría automática
- ✅ Logs de acciones e inventario
- ✅ Admin de Django configurado
- ✅ Datos de prueba incluidos

---

**Desarrollado con ❤️ usando Django y Django REST Framework**
