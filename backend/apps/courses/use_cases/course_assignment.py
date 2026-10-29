"""Obtiene la ruta asignada por el diagnóstico y prepara su estado."""

from rest_framework.exceptions import PermissionDenied

from apps.diagnostics.models import DiagnosticResult

from ..models import Certificate, CourseProgress, ModuleQuizAttempt


def get_assigned_unit(user):
    result = (
        DiagnosticResult.objects.filter(attempt__user=user)
        .select_related("suggested_unit")
        .order_by("-created_at")
        .first()
    )
    return result.suggested_unit if result else None


def require_assigned_unit(user):
    unit = get_assigned_unit(user)
    if unit is None:
        raise PermissionDenied("Completa primero la evaluación para generar tu curso.")
    return unit


def build_course_context(user, unit):
    progress = CourseProgress.objects.filter(user=user, lesson__unit=unit)
    return {
        "completed_ids": set(
            progress.filter(completed=True).values_list("lesson_id", flat=True)
        ),
        "activity_responses": dict(
            progress.exclude(activity_response="").values_list(
                "lesson_id", "activity_response"
            )
        ),
        "latest_quiz": ModuleQuizAttempt.objects.filter(user=user, unit=unit).first(),
        "certificate": Certificate.objects.filter(user=user, unit=unit).first(),
    }
