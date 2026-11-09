"""Reglas para completar experiencias interactivas de una ruta asignada."""

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, ValidationError

from ..models import Certificate, CourseProgress, Lesson


class CertifiedCourseConflict(APIException):
    status_code = 409
    default_detail = "La ruta certificada ya no puede marcarse como pendiente."
    default_code = "certified_course_conflict"


def _configured_ids(lesson, key):
    return {
        str(item.get("id"))
        for item in lesson.interaction_config.get(key, [])
        if item.get("id") is not None
    }


def _validate_choice(lesson, response):
    response_data = response if isinstance(response, dict) else {}
    selected_id = str(response_data.get("selected_option", ""))
    option = next(
        (
            item
            for item in lesson.interaction_config.get("options", [])
            if str(item.get("id")) == selected_id
        ),
        None,
    )
    if option is None:
        raise ValidationError(
            {"interaction_response": ["Selecciona una alternativa válida."]}
        )
    return {"selected_option": selected_id}, option.get("feedback", "")


def _validate_checklist(lesson, response):
    response_data = response if isinstance(response, dict) else {}
    selected_items = response_data.get("selected_items")
    if not isinstance(selected_items, list):
        raise ValidationError(
            {"interaction_response": ["Marca todos los pasos antes de continuar."]}
        )
    configured_ids = _configured_ids(lesson, "items")
    selected_ids = {str(item_id) for item_id in selected_items}
    if not configured_ids or selected_ids != configured_ids:
        raise ValidationError(
            {"interaction_response": ["Marca todos los pasos antes de continuar."]}
        )
    ordered_ids = [
        str(item["id"])
        for item in lesson.interaction_config["items"]
        if str(item["id"]) in selected_ids
    ]
    return (
        {"selected_items": ordered_ids},
        lesson.interaction_config.get("completion_feedback", ""),
    )


def _validated_interaction(lesson, response):
    if lesson.interaction_type == Lesson.InteractionType.GUIDED:
        return {}, lesson.interaction_config.get("completion_message", "")
    if lesson.interaction_type in {
        Lesson.InteractionType.DECISION,
        Lesson.InteractionType.PRACTICE,
    }:
        return _validate_choice(lesson, response)
    if lesson.interaction_type in {
        Lesson.InteractionType.CHECKLIST,
        Lesson.InteractionType.SAFETY_PLAN,
    }:
        return _validate_checklist(lesson, response)
    raise ValidationError(
        {"interaction_response": ["El tipo de experiencia no es válido."]}
    )


@transaction.atomic
def update_lesson_progress(user, lesson, completed, interaction_response=None):
    if Certificate.objects.filter(user=user, unit=lesson.unit).exists() and not completed:
        raise CertifiedCourseConflict()

    stored_response, feedback = (
        _validated_interaction(lesson, interaction_response) if completed else ({}, "")
    )
    progress, _ = CourseProgress.objects.get_or_create(user=user, lesson=lesson)
    progress.completed = completed
    progress.completed_at = timezone.now() if completed else None
    progress.interaction_response = stored_response
    progress.save(update_fields=("completed", "completed_at", "interaction_response"))

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
