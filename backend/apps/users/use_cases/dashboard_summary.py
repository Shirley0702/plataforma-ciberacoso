"""Construye el resumen personalizado que consume el dashboard."""

from apps.courses.models import CourseProgress, CourseUnit, Lesson
from apps.courses.use_cases.course_assignment import get_assigned_units
from apps.diagnostics.models import DiagnosticResult
from apps.text_review.models import TextReview


def build_dashboard_summary(user):
    latest_result = (
        DiagnosticResult.objects.filter(attempt__user=user)
        .select_related("suggested_unit")
        .order_by("-created_at")
        .first()
    )
    assigned_units = get_assigned_units(user) if latest_result else []
    assigned_unit_ids = [unit.id for unit in assigned_units]
    completed_lessons = CourseProgress.objects.filter(
        user=user,
        completed=True,
        lesson__unit_id__in=assigned_unit_ids,
    ).count()
    total_lessons = (
        Lesson.objects.filter(unit_id__in=assigned_unit_ids).count()
        if latest_result
        else 0
    )
    latest_text_review = TextReview.objects.filter(user=user).first()
    return {
        "diagnostic": _diagnostic_summary(latest_result, assigned_units),
        "text_review": _text_review_summary(latest_text_review),
        "course": {
            "completed": completed_lessons,
            "total": total_lessons,
            "percentage": round(
                completed_lessons / total_lessons * 100 if total_lessons else 0
            ),
        },
    }


def _text_review_summary(review):
    if review is None:
        return None
    return {
        "possible_signals": (
            review.classification == TextReview.Classification.NEEDS_ATTENTION
        ),
        "attention_level": review.attention_level,
        "created_at": review.created_at,
    }


def _diagnostic_summary(result, recommended_units):
    if result is None:
        return None
    dimensions = result.profile.get("dimensions", [])
    dimension_units = {
        unit.id: unit
        for unit in CourseUnit.objects.filter(
            id__in=[dimension.get("unit_id") for dimension in dimensions]
        )
    }
    priorities = {
        dimension["unit_id"]: dimension.get("priority") for dimension in dimensions
    }
    return {
        "suggested_unit": _unit_summary(result.suggested_unit),
        "recommended_units": [
            _unit_summary(unit, priorities.get(unit.id) or 1)
            for unit in recommended_units
        ],
        "route_type": result.profile.get("route_type", "prioritized"),
        "dimension_profile": [
            {**dimension, "title": dimension_units[dimension["unit_id"]].title}
            for dimension in dimensions
            if dimension.get("unit_id") in dimension_units
        ],
        "created_at": result.created_at,
    }


def _unit_summary(unit, priority=None):
    summary = {
        "id": unit.id,
        "title": unit.title,
        "slug": unit.slug,
        "description": unit.description,
    }
    if priority is not None:
        summary["priority"] = priority
    return summary
