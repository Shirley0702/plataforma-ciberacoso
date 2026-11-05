"""Permisos del instrumento de evaluación de la plataforma."""

from rest_framework.permissions import BasePermission

from apps.courses.use_cases import has_completed_course


class HasCompletedCourse(BasePermission):
    """Habilita la encuesta después de aprobar la ruta personalizada."""

    message = "Completa y aprueba tu curso antes de evaluar la plataforma."

    def has_permission(self, request, view):
        return has_completed_course(request.user)
