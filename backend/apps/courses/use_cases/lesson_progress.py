"""Reglas para completar lecciones y actividades de la ruta asignada."""

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, ValidationError

from ..models import Certificate, CourseProgress, Lesson


class CertifiedCourseConflict(APIException):
    status_code = 409
    default_detail = "La ruta certificada ya no puede marcarse como pendiente."
    default_code = "certified_course_conflict"


def _find_activity_option(lesson, choice):
    return next(
        (
            option
            for option in lesson.activity_options
            if str(option.get("id")) == str(choice)
        ),
        None,
    )


@transaction.atomic
def update_lesson_progress(user, lesson, completed, activity_choice=None):
    if Certificate.objects.filter(user=user, unit=lesson.unit).exists() and not completed:
        raise CertifiedCourseConflict()

    feedback = ""
    activity_response = ""
    if lesson.kind == "activity" and completed:
        selected_option = _find_activity_option(lesson, activity_choice)
        if selected_option is None:
            raise ValidationError(
                {"activity_choice": ["Selecciona una decisión válida."]}
            )
        activity_response = str(selected_option["id"])
        feedback = selected_option.get("feedback", "")

    progress, _ = CourseProgress.objects.get_or_create(user=user, lesson=lesson)
    progress.completed = completed
    progress.completed_at = timezone.now() if completed else None
    progress.activity_response = activity_response if completed else ""
    progress.save(update_fields=("completed", "completed_at", "activity_response"))

    completed_count = CourseProgress.objects.filter(
        user=user, completed=True, lesson__unit=lesson.unit
    ).count()
    total_count = Lesson.objects.filter(unit=lesson.unit).count()
    return {
        "lesson_id": lesson.id,
        "completed": completed,
        "progress": round(completed_count / total_count * 100) if total_count else 0,
        "feedback": feedback,
        "quiz_unlocked": bool(total_count) and completed_count == total_count,
    }
