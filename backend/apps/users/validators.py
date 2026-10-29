import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework import serializers


def validate_full_name(value):
    normalized = " ".join(value.split())
    if any(not (character.isalpha() or character in " '-") for character in normalized):
        raise serializers.ValidationError(
            "El nombre completo solo puede contener letras, espacios, apóstrofes o guiones."
        )
    if len(normalized.split(" ")) < 2:
        raise serializers.ValidationError("Ingresa al menos un nombre y un apellido.")
    return normalized


def validate_strong_password(password, user=None):
    missing_rules = []
    if not re.search(r"[A-Z]", password):
        missing_rules.append("una mayúscula")
    if not re.search(r"[a-z]", password):
        missing_rules.append("una minúscula")
    if not re.search(r"\d", password):
        missing_rules.append("un número")
    if not re.search(r"[^A-Za-z0-9]", password):
        missing_rules.append("un símbolo")
    if missing_rules:
        raise serializers.ValidationError(
            f"La contraseña debe incluir {', '.join(missing_rules)}."
        )
    try:
        validate_password(password, user=user)
    except DjangoValidationError as error:
        raise serializers.ValidationError(error.messages) from error
    return password


def validate_birth_date(value):
    today = timezone.localdate()
    if value > today:
        raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
    age = today.year - value.year - (
        (today.month, today.day) < (value.month, value.day)
    )
    if age > 120:
        raise serializers.ValidationError("Ingresa una fecha de nacimiento válida.")
    return value
