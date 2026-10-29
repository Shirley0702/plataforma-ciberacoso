from django.db import transaction
from rest_framework.exceptions import APIException

from apps.diagnostics.models import DiagnosticResult

from ..ml import classify_text
from ..models import TextReview


class DiagnosticRequired(APIException):
    status_code = 409
    default_detail = "Completa primero la evaluación para recibir una orientación personalizada."
    default_code = "diagnostic_required"


def _attention_level(score):
    if score >= 0.75:
        return "high"
    if score >= 0.55:
        return "moderate"
    return "low"


def _recommendations(review):
    if review.classification == TextReview.Classification.NEEDS_ATTENTION:
        items = [
            "Conserva capturas completas, fechas y enlaces si hacerlo no aumenta el riesgo.",
            "Evita responder bajo presión; bloquea o reporta la cuenta si es seguro para ti.",
            "Comparte lo ocurrido con una persona de confianza o con bienestar estudiantil.",
        ]
    else:
        items = [
            "Observa el contexto, la repetición y si la situación cambia después de expresar un límite.",
            "Si algo te incomoda, puedes conservar el mensaje y comentarlo con una persona de confianza.",
        ]
    if review.recommended_unit:
        items.append(
            f"Continúa con tu ruta educativa: {review.recommended_unit.title}."
        )
    return items


def present_review(review):
    possible_signals = (
        review.classification == TextReview.Classification.NEEDS_ATTENTION
    )
    return {
        "result_id": review.id,
        "possible_signals": possible_signals,
        "attention_level": review.attention_level,
        "title": (
            "Conviene revisar esta situación con cuidado"
            if possible_signals
            else "No aparecen señales claras en este fragmento"
        ),
        "guidance": (
            "El texto contiene patrones que pueden requerir apoyo. El contexto y la repetición también son importantes."
            if possible_signals
            else "Un solo texto no permite conocer todo el contexto. Si te hizo sentir incómodo o inseguro, busca apoyo aunque el sistema no marque señales claras."
        ),
        "recommendations": _recommendations(review),
        "recommended_unit": (
            {
                "id": review.recommended_unit.id,
                "slug": review.recommended_unit.slug,
                "title": review.recommended_unit.title,
                "description": review.recommended_unit.description,
            }
            if review.recommended_unit
            else None
        ),
        "created_at": review.created_at,
        "privacy_notice": "El texto original no se guardó en la base de datos.",
    }


@transaction.atomic
def review_text(user, text):
    diagnostic_result = (
        DiagnosticResult.objects.filter(attempt__user=user)
        .select_related("suggested_unit")
        .order_by("-created_at")
        .first()
    )
    if diagnostic_result is None:
        raise DiagnosticRequired()

    prediction = classify_text(text)
    classification = (
        TextReview.Classification.NEEDS_ATTENTION
        if prediction["label"] == "attention"
        else TextReview.Classification.NO_CLEAR_SIGNALS
    )
    review = TextReview.objects.create(
        user=user,
        diagnostic_result=diagnostic_result,
        recommended_unit=diagnostic_result.suggested_unit,
        classification=classification,
        attention_score=prediction["attention_score"],
        attention_level=_attention_level(prediction["attention_score"]),
        model_version=prediction["version"],
        character_count=len(text),
    )
    return present_review(review)

