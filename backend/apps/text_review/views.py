from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.users.permissions import IsLearningParticipant

from .models import TextReview
from .serializers import TextReviewRequestSerializer
from .use_cases import present_review, review_text


class TextReviewView(APIView):
    permission_classes = [IsLearningParticipant]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "text_review"

    def post(self, request):
        serializer = TextReviewRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = review_text(request.user, serializer.validated_data["text"])
        return Response(result, status=status.HTTP_201_CREATED)


class LatestTextReviewView(APIView):
    permission_classes = [IsLearningParticipant]

    def get(self, request):
        latest = (
            TextReview.objects.filter(user=request.user)
            .select_related("recommended_unit")
            .first()
        )
        return Response(present_review(latest) if latest else None)

