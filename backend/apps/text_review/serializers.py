from rest_framework import serializers


class TextReviewRequestSerializer(serializers.Serializer):
    text = serializers.CharField(
        min_length=20,
        max_length=3000,
        trim_whitespace=True,
        error_messages={
            "required": "Escribe la situación que deseas revisar.",
            "blank": "Escribe la situación que deseas revisar.",
            "min_length": "Describe la situación con un poco más de detalle.",
            "max_length": "El texto no puede superar los 3000 caracteres.",
        },
    )

    def validate_text(self, value):
        if len(value.split()) < 4:
            raise serializers.ValidationError(
                "Describe la situación con al menos cuatro palabras."
            )
        return value

