from rest_framework import serializers

from .models import OrientationResource


class OrientationResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrientationResource
        fields = ("id", "name", "description", "url", "phone", "country", "emergency")
