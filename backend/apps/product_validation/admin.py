from django.contrib import admin
from django.db.models import Avg

from .models import ParticipantFeedback, QualityAssessment


@admin.register(ParticipantFeedback)
class ParticipantFeedbackAdmin(admin.ModelAdmin):
    change_list_template = "admin/product_validation/participantfeedback/change_list.html"
    list_display = (
        "participant_code",
        "app_version",
        "ease_of_use",
        "content_clarity",
        "educational_usefulness",
        "satisfaction",
        "accessibility",
        "updated_at",
    )
    list_filter = ("app_version", "submitted_at")
    readonly_fields = (
        "user",
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

    @admin.display(description="Participante")
    def participant_code(self, obj):
        return f"P-{obj.user_id:05d}"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        metrics = self.get_queryset(request).aggregate(
            ease_of_use=Avg("ease_of_use"),
            content_clarity=Avg("content_clarity"),
            educational_usefulness=Avg("educational_usefulness"),
            satisfaction=Avg("satisfaction"),
            accessibility=Avg("accessibility"),
        )
        extra_context = {**(extra_context or {}), "validation_metrics": metrics}
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(QualityAssessment)
class QualityAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "app_version",
        "characteristic",
        "criterion",
        "result",
        "evaluator",
        "assessed_at",
    )
    list_filter = ("app_version", "characteristic", "result")
    search_fields = ("criterion", "evidence")
    readonly_fields = ("evaluator", "assessed_at")

    def save_model(self, request, obj, form, change):
        if not obj.evaluator_id:
            obj.evaluator = request.user
        super().save_model(request, obj, form, change)
