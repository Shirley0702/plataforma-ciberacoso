"""Construye el resumen personalizado que consume el dashboard."""

from apps.courses.models import CourseProgress, Lesson
from apps.diagnostics.models import DiagnosticResult
from apps.text_review.models import TextReview


def build_dashboard_summary(user):
    latest_result = (
        DiagnosticResult.objects.filter(attempt__user=user)
        .select_related("suggested_unit")
        .order_by("-created_at")
        .first()
    )
    assigned_unit_id = latest_result.suggested_unit_id if latest_result else None
    completed_lessons = CourseProgress.objects.filter(
        user=user,
        completed=True,
        lesson__unit_id=assigned_unit_id,
    ).count()
    total_lessons = (
        Lesson.objects.filter(unit_id=assigned_unit_id).count() if latest_result else 0
    )
    latest_text_review = TextReview.objects.filter(user=user).first()
    return {
        "diagnostic": _diagnostic_summary(latest_result),
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


def _diagnostic_summary(result):
    if result is None:
        return None
    return {
        "suggested_unit": {
            "id": result.suggested_unit.id,
            "title": result.suggested_unit.title,
            "slug": result.suggested_unit.slug,
            "description": result.suggested_unit.description,
        },
        "created_at": result.created_at,
    }
