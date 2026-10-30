from django.urls import path

from .views import ParticipantFeedbackView


urlpatterns = [
    path("feedback/", ParticipantFeedbackView.as_view(), name="participant_feedback"),
]
