from django.conf import settings
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    full_name = models.CharField(max_length=120, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    university = models.CharField(max_length=150, blank=True)
    academic_program = models.CharField(max_length=150, blank=True)
    bio = models.CharField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to="profiles/avatars/", blank=True)
    accepted_terms_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or self.user.username

    @property
    def age(self):
        if self.birth_date is None:
            return None
        today = timezone.localdate()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )


class EmailVerification(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verification",
    )
    code_digest = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    sent_at = models.DateTimeField(auto_now=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Verificación de {self.user.email}"
