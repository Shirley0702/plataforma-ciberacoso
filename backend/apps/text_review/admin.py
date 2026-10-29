from django.contrib import admin

from .models import TextReview


@admin.register(TextReview)
class TextReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "classification",
        "attention_level",
        "recommended_unit",
        "created_at",
    )
    list_filter = ("classification", "attention_level", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = (
        "user",
        "diagnostic_result",
        "recommended_unit",
        "classification",
        "attention_score",
        "attention_level",
        "model_version",
        "character_count",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

