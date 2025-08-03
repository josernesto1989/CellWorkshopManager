# 🚀 Guía de Despliegue - CellWorkshopManager

Guía completa para desplegar el sistema CellWorkshopManager en un entorno de producción.

## 📋 Prerrequisitos

### Servidor
- **Sistema Operativo**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **RAM**: Mínimo 2GB, recomendado 4GB+
- **Almacenamiento**: Mínimo 10GB de espacio libre
- **Python**: 3.8 o superior

### Software Requerido
- Python 3.8+
- pip
- virtualenv
- PostgreSQL (recomendado) o MySQL
- Nginx
- Gunicorn
- Supervisor (opcional)

## 🔧 Instalación en Producción

### 1. Preparar el Servidor

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y nginx
sudo apt install -y git
sudo apt install -y supervisor
```

### 2. Configurar Base de Datos PostgreSQL

```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE cellworkshop_db;
CREATE USER cellworkshop_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE cellworkshop_db TO cellworkshop_user;
ALTER USER cellworkshop_user CREATEDB;
\q
```

### 3. Clonar y Configurar el Proyecto

```bash
# Crear directorio para la aplicación
sudo mkdir -p /var/www/cellworkshop
sudo chown $USER:$USER /var/www/cellworkshop
cd /var/www/cellworkshop

# Clonar el repositorio
git clone <repository-url> .

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DEBUG=False
SECRET_KEY=tu_clave_secreta_muy_larga_y_compleja
DATABASE_URL=postgresql://cellworkshop_user:tu_password_seguro@localhost/cellworkshop_db
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,localhost
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# Configuración de email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-app

# Configuración de logs
LOG_LEVEL=INFO
LOG_FILE=/var/log/cellworkshop/app.log
```

### 5. Configurar Django Settings

Modificar `cellworkshop_api/settings.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cellworkshop_db',
        'USER': 'cellworkshop_user',
        'PASSWORD': 'tu_password_seguro',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/cellworkshop/app.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'inventario': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 6. Ejecutar Migraciones y Configurar Datos

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar migraciones
python3 manage.py makemigrations
python3 manage.py migrate

# Crear superusuario
python3 manage.py createsuperuser

# Recolectar archivos estáticos
python3 manage.py collectstatic --noinput

# Cargar datos de prueba (opcional)
python3 manage.py loaddata fixtures_iniciales.json
```

### 7. Configurar Gunicorn

Crear archivo `/etc/systemd/system/cellworkshop.service`:

```ini
[Unit]
Description=CellWorkshop Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/cellworkshop
Environment="PATH=/var/www/cellworkshop/venv/bin"
ExecStart=/var/www/cellworkshop/venv/bin/gunicorn --workers 3 --bind unix:/var/www/cellworkshop/cellworkshop.sock cellworkshop_api.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### 8. Configurar Nginx

Crear archivo `/etc/nginx/sites-available/cellworkshop`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    # Redirigir HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Logs
    access_log /var/log/nginx/cellworkshop_access.log;
    error_log /var/log/nginx/cellworkshop_error.log;

    # Static files
    location /static/ {
        alias /var/www/cellworkshop/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/cellworkshop/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Django application
    location / {
        proxy_pass http://unix:/var/www/cellworkshop/cellworkshop.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # API endpoints
    location /api/ {
        proxy_pass http://unix:/var/www/cellworkshop/cellworkshop.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 9. Configurar SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Configurar renovación automática
sudo crontab -e
# Agregar esta línea:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### 10. Iniciar Servicios

```bash
# Cambiar permisos
sudo chown -R www-data:www-data /var/www/cellworkshop
sudo chmod -R 755 /var/www/cellworkshop

# Crear directorio de logs
sudo mkdir -p /var/log/cellworkshop
sudo chown www-data:www-data /var/log/cellworkshop

# Habilitar y iniciar servicios
sudo systemctl enable cellworkshop
sudo systemctl start cellworkshop

# Habilitar sitio de Nginx
sudo ln -s /etc/nginx/sites-available/cellworkshop /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔒 Configuración de Seguridad

### 1. Firewall

```bash
# Configurar UFW
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 2. Configuración de PostgreSQL

Editar `/etc/postgresql/13/main/postgresql.conf`:

```conf
# Configuraciones de seguridad
listen_addresses = 'localhost'
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
```

### 3. Backup Automático

Crear script `/var/www/cellworkshop/backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/cellworkshop"
DB_NAME="cellworkshop_db"
DB_USER="cellworkshop_user"

# Crear directorio de backup
mkdir -p $BACKUP_DIR

# Backup de la base de datos
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Backup de archivos
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz /var/www/cellworkshop

# Eliminar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completado: $DATE"
```

Configurar cron para ejecutar backup diario:

```bash
sudo crontab -e
# Agregar esta línea:
# 0 2 * * * /var/www/cellworkshop/backup.sh >> /var/log/cellworkshop/backup.log 2>&1
```

## 📊 Monitoreo

### 1. Configurar Supervisor (Opcional)

Crear archivo `/etc/supervisor/conf.d/cellworkshop.conf`:

```ini
[program:cellworkshop]
command=/var/www/cellworkshop/venv/bin/gunicorn --workers 3 --bind unix:/var/www/cellworkshop/cellworkshop.sock cellworkshop_api.wsgi:application
directory=/var/www/cellworkshop
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/cellworkshop/gunicorn.log
```

### 2. Logs de Monitoreo

```bash
# Ver logs de la aplicación
sudo tail -f /var/log/cellworkshop/app.log

# Ver logs de Nginx
sudo tail -f /var/log/nginx/cellworkshop_access.log
sudo tail -f /var/log/nginx/cellworkshop_error.log

# Ver logs de Gunicorn
sudo tail -f /var/log/cellworkshop/gunicorn.log
```

### 3. Monitoreo de Recursos

```bash
# Instalar herramientas de monitoreo
sudo apt install -y htop iotop nethogs

# Verificar uso de recursos
htop
df -h
free -h
```

## 🔄 Actualizaciones

### 1. Script de Actualización

Crear script `/var/www/cellworkshop/update.sh`:

```bash
#!/bin/bash
cd /var/www/cellworkshop

# Activar entorno virtual
source venv/bin/activate

# Hacer backup antes de actualizar
./backup.sh

# Obtener cambios del repositorio
git pull origin main

# Instalar nuevas dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python3 manage.py makemigrations
python3 manage.py migrate

# Recolectar archivos estáticos
python3 manage.py collectstatic --noinput

# Reiniciar servicios
sudo systemctl restart cellworkshop
sudo systemctl reload nginx

echo "Actualización completada"
```

### 2. Actualización Manual

```bash
# Detener servicios
sudo systemctl stop cellworkshop

# Hacer backup
./backup.sh

# Actualizar código
git pull origin main

# Actualizar dependencias
source venv/bin/activate
pip install -r requirements.txt

# Ejecutar migraciones
python3 manage.py makemigrations
python3 manage.py migrate

# Recolectar estáticos
python3 manage.py collectstatic --noinput

# Reiniciar servicios
sudo systemctl start cellworkshop
sudo systemctl reload nginx
```

## 🚨 Troubleshooting

### Problemas Comunes

#### Error de Permisos
```bash
# Verificar permisos
sudo chown -R www-data:www-data /var/www/cellworkshop
sudo chmod -R 755 /var/www/cellworkshop
```

#### Error de Base de Datos
```bash
# Verificar conexión
sudo -u postgres psql -d cellworkshop_db -c "SELECT version();"

# Verificar logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-13-main.log
```

#### Error de Nginx
```bash
# Verificar configuración
sudo nginx -t

# Ver logs de error
sudo tail -f /var/log/nginx/error.log
```

#### Error de Gunicorn
```bash
# Verificar estado del servicio
sudo systemctl status cellworkshop

# Ver logs
sudo journalctl -u cellworkshop -f
```

## 📞 Soporte

Para problemas de despliegue:
1. Verificar logs en `/var/log/cellworkshop/`
2. Verificar configuración de servicios
3. Consultar documentación de Django y Nginx
4. Contactar al equipo de desarrollo

---

**¡Sistema desplegado exitosamente! 🎉** 