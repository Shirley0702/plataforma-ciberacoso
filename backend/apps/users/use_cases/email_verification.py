"""Emisión y comprobación segura del código de verificación institucional."""

import secrets
import smtplib
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, ValidationError

from ..models import EmailVerification


User = get_user_model()


class EmailDeliveryUnavailable(APIException):
    status_code = 503
    default_detail = "No fue posible enviar el código. Inténtalo nuevamente más tarde."
    default_code = "email_delivery_unavailable"


class VerificationRateLimited(APIException):
    status_code = 429
    default_detail = "Espera un minuto antes de solicitar otro código."
    default_code = "verification_rate_limited"


def _new_code():
    return f"{secrets.randbelow(1_000_000):06d}"


def _deliver_code(user, code):
    try:
        send_mail(
            subject="Código de verificación de CiberSegura",
            message=(
                f"Hola,\n\nTu código de verificación es: {code}\n\n"
                f"Caduca en {settings.EMAIL_VERIFICATION_MINUTES} minutos. "
                "Si no solicitaste esta cuenta, ignora este mensaje."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except (OSError, smtplib.SMTPException) as error:
        raise EmailDeliveryUnavailable() from error


def issue_verification_code(user):
    code = _new_code()
    expires_at = timezone.now() + timedelta(
        minutes=settings.EMAIL_VERIFICATION_MINUTES
    )
    EmailVerification.objects.update_or_create(
        user=user,
        defaults={
            "code_digest": make_password(code),
            "expires_at": expires_at,
            "attempts": 0,
            "verified_at": None,
        },
    )
    _deliver_code(user, code)


def verify_email_code(email, code):
    invalid_code = False
    with transaction.atomic():
        user = User.objects.select_for_update().filter(email__iexact=email).first()
        if user is None or user.is_active:
            raise ValidationError({"code": ["El código no es válido."]})

        verification = (
            EmailVerification.objects.select_for_update().filter(user=user).first()
        )
        if verification is None or verification.verified_at is not None:
            raise ValidationError({"code": ["El código no es válido."]})
        if verification.expires_at <= timezone.now():
            raise ValidationError({"code": ["El código venció. Solicita uno nuevo."]})
        if verification.attempts >= settings.EMAIL_VERIFICATION_MAX_ATTEMPTS:
            raise ValidationError(
                {"code": ["Superaste el número de intentos. Solicita otro código."]}
            )

        if not check_password(code, verification.code_digest):
            verification.attempts += 1
            verification.save(update_fields=("attempts",))
            invalid_code = True
        else:
            now = timezone.now()
            verification.verified_at = now
            verification.save(update_fields=("verified_at",))
            user.is_active = True
            user.save(update_fields=("is_active",))

    if invalid_code:
        raise ValidationError({"code": ["El código no es válido."]})
    return user


@transaction.atomic
def resend_verification_code(email):
    user = User.objects.filter(email__iexact=email, is_active=False).first()
    if user is None:
        raise ValidationError({"email": ["No existe un registro pendiente para este correo."]})
    verification = EmailVerification.objects.filter(user=user).first()
    cooldown = timedelta(seconds=settings.EMAIL_VERIFICATION_RESEND_SECONDS)
    if verification and verification.sent_at + cooldown > timezone.now():
        raise VerificationRateLimited()
    issue_verification_code(user)
