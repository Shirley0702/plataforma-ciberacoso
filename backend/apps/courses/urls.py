from django.urls import path

from .views import (
    CertificateDownloadView,
    CertificateVerifyView,
    CompleteLessonView,
    CourseUnitListView,
    SubmitModuleQuizView,
)


urlpatterns = [
    path("units/", CourseUnitListView.as_view(), name="course-units"),
    path(
        "lessons/<int:lesson_id>/complete/",
        CompleteLessonView.as_view(),
        name="complete-lesson",
    ),
    path("quiz/submit/", SubmitModuleQuizView.as_view(), name="submit-module-quiz"),
    path(
        "certificates/<str:code>/download/",
        CertificateDownloadView.as_view(),
        name="certificate-download",
    ),
    path(
        "certificates/verify/<str:code>/",
        CertificateVerifyView.as_view(),
        name="certificate-verify",
    ),
]
