from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsLearningParticipant

from .models import ParticipantFeedback
from .serializers import ParticipantFeedbackSerializer


class ParticipantFeedbackView(APIView):
    permission_classes = [IsLearningParticipant]

    def get(self, request):
        feedback = ParticipantFeedback.objects.filter(
            user=request.user,
            app_version=settings.APP_VERSION,
        ).first()
        if feedback is None:
            return Response(None)
        return Response(ParticipantFeedbackSerializer(feedback).data)

    def post(self, request):
        already_exists = ParticipantFeedback.objects.filter(
            user=request.user,
            app_version=settings.APP_VERSION,
        ).exists()
        serializer = ParticipantFeedbackSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_status = status.HTTP_200_OK if already_exists else status.HTTP_201_CREATED
        return Response(serializer.data, status=response_status)
