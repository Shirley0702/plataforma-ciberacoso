from django.conf import settings
from rest_framework import serializers

from .models import ParticipantFeedback


class ParticipantFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantFeedback
        fields = (
            "id",
            "app_version",
            "ease_of_use",
            "content_clarity",
            "educational_usefulness",
            "satisfaction",
            "accessibility",
            "open_comment",
            "informed_consent",
            "submitted_at",
            "updated_at",
        )
        read_only_fields = ("id", "app_version", "submitted_at", "updated_at")

    def validate_informed_consent(self, value):
        if not value:
            raise serializers.ValidationError(
                "Debes aceptar el uso de estas respuestas para evaluar y mejorar la plataforma."
            )
        return value

    def create(self, validated_data):
        feedback, _ = ParticipantFeedback.objects.update_or_create(
            user=self.context["request"].user,
            app_version=settings.APP_VERSION,
            defaults=validated_data,
        )
        return feedback
