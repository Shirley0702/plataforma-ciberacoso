from django.conf import settings
from django.db import models


class CourseUnit(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=80, unique=True)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=10)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    KINDS = [("lesson", "Lección"), ("activity", "Actividad interactiva")]

    unit = models.ForeignKey(CourseUnit, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=160)
    summary = models.CharField(max_length=260)
    content = models.TextField()
    kind = models.CharField(max_length=20, choices=KINDS, default="lesson")
    duration_minutes = models.PositiveIntegerField(default=5)
    activity_prompt = models.TextField(blank=True)
    activity_options = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return self.title


class CourseProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_progress"
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    activity_response = models.CharField(max_length=260, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "lesson"), name="unique_progress_per_lesson"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.lesson}"


class ModuleQuizQuestion(models.Model):
    unit = models.ForeignKey(
        CourseUnit, on_delete=models.CASCADE, related_name="quiz_questions"
    )
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.unit}: {self.text}"


class ModuleQuizOption(models.Model):
    question = models.ForeignKey(
        ModuleQuizQuestion, on_delete=models.CASCADE, related_name="options"
    )
    label = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.question_id}: {self.label}"


class ModuleQuizAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts"
    )
    unit = models.ForeignKey(
        CourseUnit, on_delete=models.PROTECT, related_name="quiz_attempts"
    )
    score_percentage = models.PositiveSmallIntegerField()
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "-id")


class Certificate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificates"
    )
    unit = models.ForeignKey(
        CourseUnit, on_delete=models.PROTECT, related_name="certificates"
    )
    verification_code = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "unit"), name="unique_certificate_per_user_unit"
            )
        ]

    def __str__(self):
        return f"{self.verification_code} - {self.user}"
