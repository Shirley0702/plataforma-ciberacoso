"""Generación de identificadores internos únicos para participantes."""

import secrets

from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()
MAX_USERNAME_LENGTH = User._meta.get_field("username").max_length


def generate_unique_username(full_name, email):
    """Genera un identificador legible sin pedirlo ni exponerlo al participante."""

    readable_base = slugify(full_name).replace("-", ".")
    email_base = slugify(email.split("@", 1)[0]).replace("-", ".")
    base = readable_base or email_base or "usuario"

    for _ in range(20):
        suffix = secrets.token_hex(5)
        prefix_length = MAX_USERNAME_LENGTH - len(suffix) - 1
        candidate = f"{base[:prefix_length].rstrip('.')}.{suffix}"
        if not User.objects.filter(username=candidate).exists():
            return candidate
    raise RuntimeError("No fue posible generar un identificador de usuario único.")
