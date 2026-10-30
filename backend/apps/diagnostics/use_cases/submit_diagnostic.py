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
DEFAULT_ROUTE_SLUG = "acoso-tecnologico"
SCORING_VERSION = "weighted-scores-v1"


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


def _select_unit(ranking):
    if not ranking:
        unit = _fallback_unit()
        if unit is None:
            raise CourseCatalogUnavailable()
        return unit, 0
    winner = ranking[0]
    return CourseUnit.objects.get(id=winner["destination_unit"]), winner["total_score"]


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
    suggested_unit, maximum_score = _select_unit(ranking)
    attempt.completed_at = timezone.now()
    attempt.save(update_fields=("completed_at",))
    return DiagnosticResult.objects.create(
        attempt=attempt,
        suggested_unit=suggested_unit,
        maximum_score=maximum_score,
        scoring_version=SCORING_VERSION,
        scores={
            str(item["destination_unit"]): item["total_score"] for item in ranking
        },
    )
