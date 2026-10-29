"""Validación, calificación y certificación del cuestionario final."""

import secrets

from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

from ..models import (
    Certificate,
    CourseProgress,
    Lesson,
    ModuleQuizAttempt,
    ModuleQuizOption,
    ModuleQuizQuestion,
)


PASSING_SCORE_PERCENT = 80


def _validate_answer_map(raw_answers, questions):
    if not isinstance(raw_answers, list):
        raise ValidationError({"answers": ["Envía una lista de respuestas."]})

    answer_map = {}
    for answer in raw_answers:
        try:
            question_id = int(answer["question_id"])
            option_id = int(answer["option_id"])
        except (KeyError, TypeError, ValueError):
            raise ValidationError(
                {"answers": ["Cada respuesta debe incluir pregunta y opción."]}
            )
        if question_id in answer_map:
            raise ValidationError(
                {"answers": ["No se puede responder dos veces una pregunta."]}
            )
        answer_map[question_id] = option_id

    if set(answer_map) != {question.id for question in questions}:
        raise ValidationError(
            {"answers": ["Debes responder todas las preguntas del módulo."]}
        )
    return answer_map


def _calculate_score(questions, answer_map):
    correct_count = 0
    for question in questions:
        option = ModuleQuizOption.objects.filter(
            id=answer_map[question.id], question=question
        ).first()
        if option is None:
            raise ValidationError(
                {"answers": ["Una opción seleccionada no pertenece a su pregunta."]}
            )
        correct_count += int(option.is_correct)
    return round(correct_count / len(questions) * 100) if questions else 0


def _new_certificate_code():
    while True:
        code = secrets.token_hex(8).upper()
        if not Certificate.objects.filter(verification_code=code).exists():
            return code


@transaction.atomic
def submit_module_quiz(user, unit, raw_answers):
    lesson_count = Lesson.objects.filter(unit=unit).count()
    completed_count = CourseProgress.objects.filter(
        user=user, lesson__unit=unit, completed=True
    ).count()
    if not lesson_count or completed_count != lesson_count:
        raise PermissionDenied(
            "Completa las tres lecciones y la actividad antes del cuestionario."
        )

    questions = list(
        ModuleQuizQuestion.objects.filter(unit=unit, active=True).prefetch_related(
            "options"
        )
    )
    answer_map = _validate_answer_map(raw_answers, questions)
    score = _calculate_score(questions, answer_map)
    passed = score >= PASSING_SCORE_PERCENT
    attempt = ModuleQuizAttempt.objects.create(
        user=user,
        unit=unit,
        score_percentage=score,
        passed=passed,
    )
    certificate = None
    if passed:
        certificate, _ = Certificate.objects.get_or_create(
            user=user,
            unit=unit,
            defaults={"verification_code": _new_certificate_code()},
        )
    return attempt, certificate
