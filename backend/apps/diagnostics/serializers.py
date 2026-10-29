from rest_framework import serializers

from .models import DiagnosticOption, DiagnosticQuestion, DiagnosticResult


class DiagnosticOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticOption
        fields = ("id", "label", "order")


class DiagnosticQuestionSerializer(serializers.ModelSerializer):
    options = DiagnosticOptionSerializer(many=True, read_only=True)

    class Meta:
        model = DiagnosticQuestion
        fields = ("id", "text", "order", "options")


class DiagnosticSubmissionSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.DictField(), allow_empty=False, write_only=True
    )

    def validate_answers(self, answers):
        question_ids = []
        validated = []
        for answer in answers:
            try:
                question_id = int(answer.get("question_id"))
                option_id = int(answer.get("option_id"))
            except (TypeError, ValueError):
                raise serializers.ValidationError("Cada respuesta debe incluir pregunta y opción.")
            if question_id in question_ids:
                raise serializers.ValidationError("No se puede responder dos veces una pregunta.")
            try:
                option = DiagnosticOption.objects.select_related("question").get(
                    id=option_id, question_id=question_id, question__active=True
                )
            except DiagnosticOption.DoesNotExist:
                raise serializers.ValidationError("Una opción seleccionada no es válida.")
            question_ids.append(question_id)
            validated.append(option)

        active_ids = set(
            DiagnosticQuestion.objects.filter(active=True).values_list("id", flat=True)
        )
        if set(question_ids) != active_ids:
            raise serializers.ValidationError("Debes responder todas las preguntas activas.")
        return validated


class DiagnosticResultSerializer(serializers.ModelSerializer):
    suggested_unit = serializers.SerializerMethodField()
    module_scores = serializers.SerializerMethodField()

    class Meta:
        model = DiagnosticResult
        fields = (
            "id",
            "suggested_unit",
            "maximum_score",
            "module_scores",
            "created_at",
        )

    def get_suggested_unit(self, obj):
        unit = obj.suggested_unit
        return {
            "id": unit.id,
            "title": unit.title,
            "slug": unit.slug,
            "description": unit.description,
        }

    def get_module_scores(self, obj):
        from apps.courses.models import CourseUnit

        units = CourseUnit.objects.filter(id__in=obj.scores.keys()).in_bulk()
        return [
            {
                "unit_id": unit_id,
                "title": units[int(unit_id)].title,
                "score": score,
            }
            for unit_id, score in obj.scores.items()
            if int(unit_id) in units
        ]
