"""Autenticación del participante de la plataforma educativa."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


User = get_user_model()


class ParticipantTokenSerializer(serializers.Serializer):
    """Autentica por correo; conserva `demo` como identificador de pruebas."""

    identifier = serializers.CharField(max_length=254, trim_whitespace=True)
    password = serializers.CharField(max_length=128, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        identifier = attrs["identifier"].strip().lower()
        if "@" in identifier:
            user = User.objects.filter(email__iexact=identifier).first()
        else:
            user = User.objects.filter(username__iexact=identifier).first()
        if user is None or not user.is_active or not user.check_password(attrs["password"]):
            raise AuthenticationFailed("Correo o contraseña incorrectos.")
        if user.is_staff:
            raise AuthenticationFailed(
                "La cuenta administrativa debe ingresar por el panel de administración."
            )
        self.user = user
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class ParticipantTokenView(TokenObtainPairView):
    serializer_class = ParticipantTokenSerializer


class ParticipantTokenRefreshSerializer(TokenRefreshSerializer):
    """Impide renovar tokens antiguos pertenecientes a cuentas administrativas."""

    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])
        participant_exists = User.objects.filter(
            id=refresh["user_id"],
            is_active=True,
            is_staff=False,
        ).exists()
        if not participant_exists:
            raise AuthenticationFailed("El token no pertenece a un usuario participante.")
        return super().validate(attrs)


class ParticipantTokenRefreshView(TokenRefreshView):
    serializer_class = ParticipantTokenRefreshSerializer
