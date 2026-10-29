from rest_framework import serializers

from .models import (
    Certificate,
    CourseUnit,
    Lesson,
    ModuleQuizAttempt,
    ModuleQuizOption,
    ModuleQuizQuestion,
)


class LessonSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    activity_response = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "summary",
            "content",
            "kind",
            "duration_minutes",
            "activity_prompt",
            "activity_options",
            "order",
            "completed",
            "activity_response",
        )

    def get_completed(self, obj):
        return obj.id in self.context.get("completed_ids", set())

    def get_activity_response(self, obj):
        return self.context.get("activity_responses", {}).get(obj.id, "")


class ModuleQuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleQuizOption
        fields = ("id", "label", "order")


class ModuleQuizQuestionSerializer(serializers.ModelSerializer):
    options = ModuleQuizOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ModuleQuizQuestion
        fields = ("id", "text", "order", "options")


class ModuleQuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleQuizAttempt
        fields = ("id", "score_percentage", "passed", "created_at")


class CertificateSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source="unit.title", read_only=True)
    download_url = serializers.SerializerMethodField()
    verification_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = (
            "verification_code",
            "module_title",
            "issued_at",
            "download_url",
            "verification_url",
        )

    def get_download_url(self, obj):
        return f"/courses/certificates/{obj.verification_code}/download/"

    def get_verification_url(self, obj):
        return f"/courses/certificates/verify/{obj.verification_code}/"


class CourseUnitSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()
    quiz_unlocked = serializers.SerializerMethodField()
    quiz_questions = serializers.SerializerMethodField()
    latest_quiz = serializers.SerializerMethodField()
    certificate = serializers.SerializerMethodField()

    class Meta:
        model = CourseUnit
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "order",
            "duration_minutes",
            "lessons",
            "quiz_unlocked",
            "quiz_questions",
            "latest_quiz",
            "certificate",
        )

    def get_lessons(self, obj):
        return LessonSerializer(obj.lessons.all(), many=True, context=self.context).data

    def get_quiz_unlocked(self, obj):
        lesson_ids = {lesson.id for lesson in obj.lessons.all()}
        completed_ids = self.context.get("completed_ids", set())
        return bool(lesson_ids) and lesson_ids.issubset(completed_ids)

    def get_quiz_questions(self, obj):
        if not self.get_quiz_unlocked(obj):
            return []
        questions = [question for question in obj.quiz_questions.all() if question.active]
        return ModuleQuizQuestionSerializer(questions, many=True).data

    def get_latest_quiz(self, obj):
        attempt = self.context.get("latest_quiz")
        return ModuleQuizAttemptSerializer(attempt).data if attempt else None

    def get_certificate(self, obj):
        certificate = self.context.get("certificate")
        return CertificateSerializer(certificate).data if certificate else None
