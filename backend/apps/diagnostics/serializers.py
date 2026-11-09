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
    recommended_units = serializers.SerializerMethodField()
    dimension_profile = serializers.SerializerMethodField()
    route_type = serializers.CharField(source="profile.route_type", read_only=True)
    validation_status = serializers.CharField(
        source="profile.validation_status", read_only=True
    )

    class Meta:
        model = DiagnosticResult
        fields = (
            "id",
            "suggested_unit",
            "recommended_units",
            "maximum_score",
            "dimension_profile",
            "route_type",
            "validation_status",
            "created_at",
        )

    def get_suggested_unit(self, obj):
        return self._unit_summary(obj.suggested_unit)

    def get_recommended_units(self, obj):
        unit_ids = obj.profile.get("recommended_unit_ids") or [obj.suggested_unit_id]
        units = self._units_by_id(unit_ids)
        priorities = {
            dimension["unit_id"]: dimension.get("priority")
            for dimension in obj.profile.get("dimensions", [])
        }
        return [
            self._unit_summary(units[unit_id], priorities.get(unit_id) or 1)
            for unit_id in unit_ids
            if unit_id in units
        ]

    def get_dimension_profile(self, obj):
        dimensions = obj.profile.get("dimensions", [])
        units = self._units_by_id(
            [dimension.get("unit_id") for dimension in dimensions]
        )
        return [
            {
                **dimension,
                "title": units[dimension["unit_id"]].title,
            }
            for dimension in dimensions
            if dimension.get("unit_id") in units
        ]

    @staticmethod
    def _unit_summary(unit, priority=None):
        summary = {
            "id": unit.id,
            "title": unit.title,
            "slug": unit.slug,
            "description": unit.description,
        }
        if priority is not None:
            summary["priority"] = priority
        return summary

    @staticmethod
    def _units_by_id(unit_ids):
        from apps.courses.models import CourseUnit

        return CourseUnit.objects.filter(id__in=unit_ids).in_bulk()
