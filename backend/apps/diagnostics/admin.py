from django.contrib import admin

from .models import (
    DiagnosticAnswer,
    DiagnosticAttempt,
    DiagnosticOption,
    DiagnosticQuestion,
    DiagnosticResult,
)


class DiagnosticOptionInline(admin.TabularInline):
    model = DiagnosticOption
    extra = 0


@admin.register(DiagnosticQuestion)
class DiagnosticQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "primary_unit", "order", "active")
    list_filter = ("primary_unit", "active")
    list_editable = ("order", "active")
    inlines = (DiagnosticOptionInline,)


admin.site.register(DiagnosticAttempt)
admin.site.register(DiagnosticAnswer)


@admin.register(DiagnosticResult)
class DiagnosticResultAdmin(admin.ModelAdmin):
    list_display = (
        "attempt",
        "suggested_unit",
        "scoring_version",
        "created_at",
    )
    list_filter = ("scoring_version",)
    readonly_fields = (
        "attempt",
        "scores",
        "suggested_unit",
        "maximum_score",
        "scoring_version",
        "created_at",
    )
