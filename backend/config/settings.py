import os
from datetime import timedelta
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")

DEVELOPMENT_SECRET_KEY = "solo-desarrollo-cambia-esta-clave"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", DEVELOPMENT_SECRET_KEY)
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
if not DEBUG and SECRET_KEY == DEVELOPMENT_SECRET_KEY:
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY debe configurarse con un valor seguro cuando DJANGO_DEBUG=False."
    )
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "apps.users",
    "apps.diagnostics",
    "apps.courses",
    "apps.resources",
    "apps.text_review",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"

if os.getenv("DATABASE_ENGINE", "sqlite") == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "cibersegura"),
            "USER": os.getenv("POSTGRES_USER", "cibersegura"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

SECURE_SSL_REDIRECT = os.getenv(
    "DJANGO_SECURE_SSL_REDIRECT", str(not DEBUG)
).lower() == "true"
SESSION_COOKIE_SECURE = os.getenv(
    "DJANGO_SESSION_COOKIE_SECURE", str(not DEBUG)
).lower() == "true"
CSRF_COOKIE_SECURE = os.getenv(
    "DJANGO_CSRF_COOKIE_SECURE", str(not DEBUG)
).lower() == "true"
SECURE_HSTS_SECONDS = int(
    os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000" if not DEBUG else "0")
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", str(not DEBUG)
).lower() == "true"
SECURE_HSTS_PRELOAD = os.getenv(
    "DJANGO_SECURE_HSTS_PRELOAD", str(not DEBUG)
).lower() == "true"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
TEXT_REVIEW_MODEL_PATH = Path(
    os.getenv(
        "TEXT_REVIEW_MODEL_PATH",
        BASE_DIR / "model_artifacts" / "text_review_classifier.joblib",
    )
)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:8080"
    ).split(",")
    if origin.strip()
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTLE_RATES": {
        "registration": "5/hour",
        "email_verification": "10/minute",
        "email_verification_resend": "3/hour",
        "text_review": "30/hour",
    },
}

UNIVERSITY_DOMAINS_DATA_FILE = (
    BASE_DIR / "apps" / "users" / "data" / "world_universities_and_domains.json"
)
ADDITIONAL_UNIVERSITY_EMAIL_DOMAINS = tuple(
    domain.strip().lower()
    for domain in os.getenv("ADDITIONAL_UNIVERSITY_EMAIL_DOMAINS", "").split(",")
    if domain.strip()
)
EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "10"))
if EMAIL_USE_TLS and EMAIL_USE_SSL:
    raise ImproperlyConfigured("EMAIL_USE_TLS y EMAIL_USE_SSL no pueden activarse a la vez.")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "CiberSegura <no-reply@localhost>")
EMAIL_VERIFICATION_MINUTES = int(os.getenv("EMAIL_VERIFICATION_MINUTES", "10"))
EMAIL_VERIFICATION_MAX_ATTEMPTS = int(
    os.getenv("EMAIL_VERIFICATION_MAX_ATTEMPTS", "5")
)
EMAIL_VERIFICATION_RESEND_SECONDS = int(
    os.getenv("EMAIL_VERIFICATION_RESEND_SECONDS", "60")
)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
