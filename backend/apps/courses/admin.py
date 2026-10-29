from django.contrib import admin

from .models import (
    Certificate,
    CourseProgress,
    CourseUnit,
    Lesson,
    ModuleQuizAttempt,
    ModuleQuizOption,
    ModuleQuizQuestion,
)


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0


class QuizOptionInline(admin.TabularInline):
    model = ModuleQuizOption
    extra = 0


@admin.register(CourseUnit)
class CourseUnitAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "order", "duration_minutes", "active")
    list_editable = ("order", "active")
    inlines = (LessonInline,)


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed", "completed_at")
    list_filter = ("completed",)


@admin.register(ModuleQuizQuestion)
class ModuleQuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "unit", "order", "active")
    list_filter = ("unit", "active")
    inlines = (QuizOptionInline,)


@admin.register(ModuleQuizAttempt)
class ModuleQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "unit", "score_percentage", "passed", "created_at")
    list_filter = ("unit", "passed")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("verification_code", "user", "unit", "issued_at")
    search_fields = ("verification_code", "user__username", "user__email")
