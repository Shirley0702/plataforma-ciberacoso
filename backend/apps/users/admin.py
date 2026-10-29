from django.contrib import admin

from .models import EmailVerification, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "university", "academic_program", "birth_date", "created_at")
    search_fields = (
        "user__username",
        "full_name",
        "user__email",
        "university",
        "academic_program",
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "sent_at", "expires_at", "attempts", "verified_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = (
        "user",
        "code_digest",
        "sent_at",
        "expires_at",
        "attempts",
        "verified_at",
    )

    def has_add_permission(self, request):
        return False
