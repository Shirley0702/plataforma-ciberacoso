from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsLearningParticipant

from .models import DiagnosticQuestion
from .serializers import (
    DiagnosticQuestionSerializer,
    DiagnosticResultSerializer,
    DiagnosticSubmissionSerializer,
)
from .use_cases import create_diagnostic_result


class QuestionListView(APIView):
    permission_classes = [IsLearningParticipant]

    def get(self, request):
        questions = (
            DiagnosticQuestion.objects.filter(active=True)
            .prefetch_related("options")
        )
        serializer = DiagnosticQuestionSerializer(questions, many=True)
        return Response(serializer.data)


class SubmitDiagnosticView(APIView):
    permission_classes = [IsLearningParticipant]

    def post(self, request):
        submission = DiagnosticSubmissionSerializer(data=request.data)
        submission.is_valid(raise_exception=True)
        result = create_diagnostic_result(
            request.user,
            submission.validated_data["answers"],
        )
        return Response(
            DiagnosticResultSerializer(result).data,
            status=status.HTTP_201_CREATED,
        )
