from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────
# SEGURIDAD — mover a .env en producción
# ─────────────────────────────────────────────
SECRET_KEY = 'django-insecure-mg3(a=wpd3e#_y&6t3fw=3yndd(5(y8r(fl1b)mds6^$e#w%3#'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# ─────────────────────────────────────────────
# APPS
# ─────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'axes',
]

# ─────────────────────────────────────────────
# MIDDLEWARE  — el orden importa
# ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',          # Debe ir segundo
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.AdminAccessMiddleware',
    'axes.middleware.AxesMiddleware',                      # Axes siempre al final
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ─────────────────────────────────────────────
# BASE DE DATOS
# ─────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_security',
        'USER': 'root',
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',   # ✅ utf8mb4 soporta emojis y más caracteres
        },
    }
}

# ─────────────────────────────────────────────
# VALIDACIÓN DE CONTRASEÑAS
# ─────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},   # ✅ Mínimo 8 caracteres explícito
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─────────────────────────────────────────────
# INTERNACIONALIZACIÓN
# ─────────────────────────────────────────────
LANGUAGE_CODE = 'es-mx'     # ✅ Español México, mensajes de error en español
TIME_ZONE = 'America/Mexico_City'   # ✅ Zona horaria correcta
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────
# ARCHIVOS ESTÁTICOS
# ─────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ─────────────────────────────────────────────
# SESIONES Y COOKIES
# ─────────────────────────────────────────────
SESSION_COOKIE_SECURE = True       # → True en producción (HTTPS)
CSRF_COOKIE_SECURE = True         # → True en producción (HTTPS)
SESSION_COOKIE_HTTPONLY = True      # ✅ JS no puede leer la cookie de sesión
CSRF_COOKIE_HTTPONLY = True         # ✅ JS no puede leer el token CSRF
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # ✅ Sesión termina al cerrar navegador
SESSION_COOKIE_AGE = 3600           # ✅ Sesión expira en 1 hora

# ─────────────────────────────────────────────
# SEGURIDAD HTTP
# ─────────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER = True    # ✅ Corrección del nombre (tenías SESSION_BROWSER...)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'            # ✅ Evita clickjacking

# ─────────────────────────────────────────────
# LOGIN / LOGOUT
# ─────────────────────────────────────────────
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/user_panel'
LOGOUT_REDIRECT_URL = '/login/'

# ─────────────────────────────────────────────
# AXES — protección contra fuerza bruta
# ─────────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_FAILURE_LIMIT = 3
AXES_LOCK_OUT_AT_FAILURE = True
AXES_COOLOFF_TIME = 1
AXES_RESET_ON_SUCCESS = True
AXES_USERNAME_FORM_FIELD = 'username'
AXES_LOCKOUT_PARAMETERS = ['ip_address', 'username']
AXES_LOCKOUT_URL = '/'              # ✅ Redirige al login al quedar bloqueado
AXES_VERBOSE = False                # ✅ Limpia logs en producción

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'