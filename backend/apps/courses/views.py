from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsLearningParticipant

from .documents.certificate import build_certificate_pdf
from .models import Certificate, CourseUnit, Lesson
from .serializers import CertificateSerializer, CourseUnitSerializer
from .use_cases import (
    PASSING_SCORE_PERCENT,
    build_course_context,
    require_assigned_unit,
    require_assigned_units,
    submit_module_quiz,
    update_lesson_progress,
)


class CourseUnitListView(APIView):
    permission_classes = [IsLearningParticipant]

    def get(self, request):
        assigned_units = require_assigned_units(request.user)
        unit_ids = [unit.id for unit in assigned_units]
        units_by_id = (
            CourseUnit.objects.filter(active=True, id__in=unit_ids)
            .prefetch_related("lessons", "quiz_questions__options")
            .in_bulk()
        )
        units = [units_by_id[unit_id] for unit_id in unit_ids if unit_id in units_by_id]
        context = build_course_context(request.user, units)
        return Response(CourseUnitSerializer(units, many=True, context=context).data)


class CompleteLessonView(APIView):
    permission_classes = [IsLearningParticipant]

    def post(self, request, lesson_id):
        assigned_units = require_assigned_units(request.user)
        lesson = get_object_or_404(
            Lesson,
            id=lesson_id,
            unit__active=True,
            unit_id__in=[unit.id for unit in assigned_units],
        )
        completed = request.data.get("completed", True)
        if not isinstance(completed, bool):
            return Response(
                {"completed": ["Debe ser un valor booleano."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = update_lesson_progress(
            request.user,
            lesson,
            completed,
            request.data.get("activity_choice"),
        )
        return Response(result)


class SubmitModuleQuizView(APIView):
    permission_classes = [IsLearningParticipant]

    def post(self, request):
        try:
            unit_id = int(request.data.get("unit_id"))
        except (TypeError, ValueError):
            return Response(
                {"unit_id": ["Selecciona un módulo válido."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        unit = require_assigned_unit(request.user, unit_id)
        attempt, certificate = submit_module_quiz(
            request.user,
            unit,
            request.data.get("answers"),
        )
        return Response(
            {
                "attempt_id": attempt.id,
                "score_percentage": attempt.score_percentage,
                "passed": attempt.passed,
                "minimum_score": PASSING_SCORE_PERCENT,
                "certificate": (
                    CertificateSerializer(certificate).data if certificate else None
                ),
            },
            status=status.HTTP_201_CREATED,
        )


class CertificateDownloadView(APIView):
    permission_classes = [IsLearningParticipant]

    def get(self, request, code):
        certificate = get_object_or_404(
            Certificate.objects.select_related("user", "user__profile", "unit"),
            verification_code=code.upper(),
            user=request.user,
        )
        response = HttpResponse(
            build_certificate_pdf(certificate),
            content_type="application/pdf",
        )
        response["Content-Disposition"] = (
            f'attachment; filename="certificado-{certificate.verification_code}.pdf"'
        )
        return response


class CertificateVerifyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, code):
        certificate = get_object_or_404(
            Certificate.objects.select_related("user", "user__profile", "unit"),
            verification_code=code.upper(),
        )
        profile = getattr(certificate.user, "profile", None)
        student_name = (
            profile.full_name
            if profile and profile.full_name
            else certificate.user.username
        )
        return Response(
            {
                "valid": True,
                "verification_code": certificate.verification_code,
                "student": student_name,
                "module_title": certificate.unit.title,
                "issued_at": certificate.issued_at,
            }
        )
