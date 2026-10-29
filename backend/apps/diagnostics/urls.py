from django.urls import path

from .views import QuestionListView, SubmitDiagnosticView


urlpatterns = [
    path("questions/", QuestionListView.as_view(), name="question-list"),
    path("submit/", SubmitDiagnosticView.as_view(), name="diagnostic-submit"),
]
