"""Obtiene las rutas asignadas por el perfil y prepara su estado."""

from rest_framework.exceptions import PermissionDenied

from apps.diagnostics.models import DiagnosticResult

from ..models import Certificate, CourseProgress, CourseUnit, ModuleQuizAttempt


def _latest_result(user):
    return (
        DiagnosticResult.objects.filter(attempt__user=user)
        .select_related("suggested_unit")
        .order_by("-created_at")
        .first()
    )


def get_assigned_units(user):
    result = _latest_result(user)
    if result is None:
        return []
    unit_ids = result.profile.get("recommended_unit_ids") or [result.suggested_unit_id]
    units = CourseUnit.objects.filter(id__in=unit_ids, active=True).in_bulk()
    return [units[unit_id] for unit_id in unit_ids if unit_id in units]


def require_assigned_units(user):
    units = get_assigned_units(user)
    if not units:
        raise PermissionDenied("Completa primero la evaluación para generar tu curso.")
    return units


def require_assigned_unit(user, unit_id):
    units = require_assigned_units(user)
    for unit in units:
        if unit.id == unit_id:
            return unit
    raise PermissionDenied("El módulo no forma parte de tu ruta actual.")


def has_completed_course(user):
    """Indica si el usuario aprobó al menos una ruta de aprendizaje."""
    return Certificate.objects.filter(user=user).exists()


def build_course_context(user, units):
    unit_ids = [unit.id for unit in units]
    result = _latest_result(user)
    priority_levels = {
        dimension["unit_id"]: dimension.get("priority")
        for dimension in (result.profile.get("dimensions", []) if result else [])
    }
    progress = CourseProgress.objects.filter(user=user, lesson__unit_id__in=unit_ids)
    latest_quizzes = {}
    for attempt in ModuleQuizAttempt.objects.filter(user=user, unit_id__in=unit_ids):
        latest_quizzes.setdefault(attempt.unit_id, attempt)
    certificates = Certificate.objects.filter(user=user, unit_id__in=unit_ids)
    return {
        "completed_ids": set(
            progress.filter(completed=True).values_list("lesson_id", flat=True)
        ),
        "interaction_responses": dict(
            progress.exclude(interaction_response={}).values_list(
                "lesson_id", "interaction_response"
            )
        ),
        "latest_quizzes": {
            unit_id: attempt for unit_id, attempt in latest_quizzes.items()
        },
        "certificates": {
            certificate.unit_id: certificate for certificate in certificates
        },
        "priority_levels": {
            unit_id: priority_levels.get(unit_id) or 1 for unit_id in unit_ids
        },
    }
