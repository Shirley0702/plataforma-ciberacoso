from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsLearningParticipant

from .models import OrientationResource
from .serializers import OrientationResourceSerializer


class OrientationResourceListView(APIView):
    permission_classes = [IsLearningParticipant]

    def get(self, request):
        resources = OrientationResource.objects.filter(active=True)
        return Response(OrientationResourceSerializer(resources, many=True).data)
