from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from apps.users.authentication import ParticipantTokenRefreshView, ParticipantTokenView
from apps.users.views import (
    LogoutView,
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path(
        "api/auth/resend-verification/",
        ResendEmailVerificationView.as_view(),
        name="resend_verification",
    ),
    path("api/auth/token/", ParticipantTokenView.as_view(), name="token_obtain_pair"),
    path(
        "api/auth/token/refresh/",
        ParticipantTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/auth/logout/", LogoutView.as_view(), name="logout"),
    path("api/users/", include("apps.users.urls")),
    path("api/diagnostics/", include("apps.diagnostics.urls")),
    path("api/courses/", include("apps.courses.urls")),
    path("api/resources/", include("apps.resources.urls")),
    path("api/text-reviews/", include("apps.text_review.urls")),
]

admin.site.site_header = "CiberSegura - Administración"
admin.site.site_title = "CiberSegura"
admin.site.index_title = "Gestión de contenidos"

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
