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


def _validate_video(response):
    response_data = response if isinstance(response, dict) else {}
    if response_data.get("watched") is not True:
        raise ValidationError(
            {"interaction_response": ["Confirma que terminaste de ver el video."]}
        )
    return {"watched": True}, "Video completado. Continúa con el siguiente reto."


def _validate_exploration(lesson, response):
    response_data = response if isinstance(response, dict) else {}
    selected_items = response_data.get("selected_items")
    if not isinstance(selected_items, list):
        raise ValidationError(
            {"interaction_response": ["Explora todos los caminos antes de continuar."]}
        )
    configured_ids = _configured_ids(lesson, "options")
    selected_ids = {str(item_id) for item_id in selected_items}
    if not configured_ids or selected_ids != configured_ids:
        raise ValidationError(
            {"interaction_response": ["Explora todos los caminos antes de continuar."]}
        )
    ordered_ids = [
        str(item["id"])
        for item in lesson.interaction_config["options"]
        if str(item["id"]) in selected_ids
    ]
    return (
        {"selected_items": ordered_ids},
        "Ya conoces las consecuencias de cada camino. Puedes elegir con más información.",
    )


def _validate_matching(lesson, response):
    response_data = response if isinstance(response, dict) else {}
    matches = response_data.get("matches")
    configured_ids = _configured_ids(lesson, "items")
    if not isinstance(matches, dict) or not configured_ids:
        raise ValidationError(
            {"interaction_response": ["Conecta cada idea con su significado."]}
        )
    normalized_matches = {str(key): str(value) for key, value in matches.items()}
    expected_matches = {item_id: item_id for item_id in configured_ids}
    if normalized_matches != expected_matches:
        raise ValidationError(
            {"interaction_response": ["Algunas conexiones no coinciden. Inténtalo otra vez."]}
        )
    ordered_matches = {
        str(item["id"]): str(item["id"])
        for item in lesson.interaction_config["items"]
    }
    return (
        {"matches": ordered_matches},
        lesson.interaction_config.get("completion_feedback", ""),
    )


def _validate_safety_plan(lesson, response):
    response_data = response if isinstance(response, dict) else {}
    selected_items = response_data.get("selected_items")
    if not isinstance(selected_items, list):
        raise ValidationError(
            {"interaction_response": ["Ordena todos los pasos antes de continuar."]}
        )
    expected_order = [
        str(item["id"])
        for item in lesson.interaction_config.get("items", [])
        if item.get("id") is not None
    ]
    submitted_order = [str(item_id) for item_id in selected_items]
    if not expected_order or submitted_order != expected_order:
        raise ValidationError(
            {"interaction_response": ["La secuencia aún no está en el orden seguro."]}
        )
    return (
        {"selected_items": expected_order},
        lesson.interaction_config.get("completion_feedback", ""),
    )


def _validated_interaction(lesson, response):
    if lesson.interaction_type == Lesson.InteractionType.GUIDED:
        return {}, lesson.interaction_config.get("completion_message", "")
    if lesson.interaction_type == Lesson.InteractionType.VIDEO:
        return _validate_video(response)
    if lesson.interaction_type in {
        Lesson.InteractionType.DECISION,
        Lesson.InteractionType.PRACTICE,
    }:
        return _validate_exploration(lesson, response)
    if lesson.interaction_type == Lesson.InteractionType.MATCHING:
        return _validate_matching(lesson, response)
    if lesson.interaction_type == Lesson.InteractionType.SAFETY_PLAN:
        return _validate_safety_plan(lesson, response)
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
