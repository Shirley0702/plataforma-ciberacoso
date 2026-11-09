from collections import defaultdict

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException

from apps.courses.models import CourseUnit

from ..models import DiagnosticAnswer, DiagnosticAttempt, DiagnosticResult

PREVENTIVE_ROUTE_SLUG = "fundamentos-preventivos"
SCORING_VERSION = "multidimensional-profile-v2"
VALIDATION_STATUS = "pending_field_validation"
MAXIMUM_DIMENSION_SCORE = 12
PRIORITY_SCORE_BANDS = 2


class CourseCatalogUnavailable(APIException):
    status_code = 409
    default_detail = "No existen módulos activos para construir la ruta."
    default_code = "course_catalog_unavailable"


def _dimension_units(options):
    unit_ids = {
        option.question.primary_unit_id
        for option in options
        if option.question.primary_unit_id
    }
    return list(
        CourseUnit.objects.filter(id__in=unit_ids, active=True).order_by("order", "id")
    )


def _calculate_scores(options, units):
    scores = defaultdict(int, {unit.id: 0 for unit in units})
    for option in options:
        unit_id = option.question.primary_unit_id
        if unit_id in scores:
            scores[unit_id] += option.weight
    return dict(scores)


def _prioritized_units(units, scores):
    positive_bands = sorted(
        {score for score in scores.values() if score > 0}, reverse=True
    )[:PRIORITY_SCORE_BANDS]
    if not positive_bands:
        return []
    units_by_id = {unit.id: unit for unit in units}
    ranked_ids = sorted(
        (unit_id for unit_id, score in scores.items() if score in positive_bands),
        key=lambda unit_id: (-scores[unit_id], units_by_id[unit_id].order, unit_id),
    )
    return [units_by_id[unit_id] for unit_id in ranked_ids]


def _preventive_unit():
    unit = CourseUnit.objects.filter(slug=PREVENTIVE_ROUTE_SLUG, active=True).first()
    if unit is None:
        raise CourseCatalogUnavailable()
    return unit


def _build_profile(units, scores, recommended_units, route_type):
    score_bands = sorted(
        {scores[unit.id] for unit in recommended_units if unit.id in scores},
        reverse=True,
    )
    priorities = {
        unit.id: score_bands.index(scores[unit.id]) + 1
        for unit in recommended_units
        if unit.id in scores
    }
    if route_type == "preventive_general":
        priorities = {recommended_units[0].id: 1}
    return {
        "instrument_version": SCORING_VERSION,
        "validation_status": VALIDATION_STATUS,
        "route_type": route_type,
        "recommended_unit_ids": [unit.id for unit in recommended_units],
        "dimensions": [
            {
                "unit_id": unit.id,
                "score": scores[unit.id],
                "maximum": MAXIMUM_DIMENSION_SCORE,
                "percentage": round(scores[unit.id] / MAXIMUM_DIMENSION_SCORE * 100),
                "priority": priorities.get(unit.id),
            }
            for unit in units
        ],
    }


@transaction.atomic
def create_diagnostic_result(user, options):
    attempt = DiagnosticAttempt.objects.create(user=user)
    DiagnosticAnswer.objects.bulk_create(
        [
            DiagnosticAnswer(
                attempt=attempt,
                question=option.question,
                option=option,
            )
            for option in options
        ]
    )

    units = _dimension_units(options)
    if not units:
        raise CourseCatalogUnavailable()
    scores = _calculate_scores(options, units)
    recommended_units = _prioritized_units(units, scores)
    route_type = "prioritized"
    if not recommended_units:
        recommended_units = [_preventive_unit()]
        route_type = "preventive_general"

    attempt.completed_at = timezone.now()
    attempt.save(update_fields=("completed_at",))
    profile = _build_profile(units, scores, recommended_units, route_type)
    return DiagnosticResult.objects.create(
        attempt=attempt,
        suggested_unit=recommended_units[0],
        maximum_score=max(scores.values(), default=0),
        scoring_version=SCORING_VERSION,
        scores={str(unit_id): score for unit_id, score in scores.items()},
        profile=profile,
    )
