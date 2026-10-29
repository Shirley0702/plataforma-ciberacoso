"""Permisos de rol compartidos por las API educativas."""

from rest_framework.permissions import BasePermission


class IsLearningParticipant(BasePermission):
    """Permite la ruta educativa a usuarios normales, incluida la cuenta demo."""

    message = "La cuenta administrativa no puede utilizar el recorrido educativo."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and not user.is_staff
        )
