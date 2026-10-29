import logging

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework.exceptions import APIException

from apps.courses.models import CourseUnit

from ..models import (
    DiagnosticAnswer,
    DiagnosticAttempt,
    DiagnosticOption,
    DiagnosticResult,
)
from ..ml.features import aggregate_option_scores
from ..ml.model import predict_route


DEFAULT_ROUTE_SLUG = "acoso-tecnologico"
MINIMUM_MODEL_CONFIDENCE = 0.55
logger = logging.getLogger(__name__)


class CourseCatalogUnavailable(APIException):
    status_code = 409
    default_detail = "No existen módulos activos para construir la ruta."
    default_code = "course_catalog_unavailable"


def _rank_selected_options(options):
    return list(
        DiagnosticOption.objects.filter(
            id__in=[option.id for option in options],
            destination_unit__isnull=False,
        )
        .values("destination_unit")
        .annotate(total_score=Sum("weight"))
        .order_by("-total_score", "destination_unit")
    )


def _fallback_unit():
    return (
        CourseUnit.objects.filter(slug=DEFAULT_ROUTE_SLUG, active=True).first()
        or CourseUnit.objects.filter(active=True).order_by("order", "id").first()
    )


def _rule_selected_unit(ranking):
    if not ranking:
        unit = _fallback_unit()
        if unit is None:
            raise CourseCatalogUnavailable()
        return unit, 0
    winner = ranking[0]
    return CourseUnit.objects.get(id=winner["destination_unit"]), winner["total_score"]


def _machine_learning_selection(options):
    feature_scores = aggregate_option_scores(options)
    if not any(feature_scores.values()):
        return None
    try:
        prediction = predict_route(feature_scores)
    except Exception:
        logger.exception("No fue posible ejecutar el modelo de recomendación.")
        return None
    if prediction["confidence"] < MINIMUM_MODEL_CONFIDENCE:
        return None
    unit = CourseUnit.objects.filter(
        slug=prediction["slug"],
        active=True,
    ).first()
    if unit is None:
        return None
    return unit, prediction


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

    ranking = _rank_selected_options(options)
    rule_unit, maximum_score = _rule_selected_unit(ranking)
    ml_selection = _machine_learning_selection(options)
    if ml_selection:
        suggested_unit, prediction = ml_selection
        recommendation_method = DiagnosticResult.RecommendationMethod.MACHINE_LEARNING
        model_version = prediction["version"]
        model_confidence = prediction["confidence"]
    else:
        suggested_unit = rule_unit
        recommendation_method = DiagnosticResult.RecommendationMethod.RULE_FALLBACK
        model_version = ""
        model_confidence = None
    attempt.completed_at = timezone.now()
    attempt.save(update_fields=("completed_at",))
    return DiagnosticResult.objects.create(
        attempt=attempt,
        suggested_unit=suggested_unit,
        maximum_score=maximum_score,
        recommendation_method=recommendation_method,
        model_version=model_version,
        model_confidence=model_confidence,
        scores={
            str(item["destination_unit"]): item["total_score"] for item in ranking
        },
    )
