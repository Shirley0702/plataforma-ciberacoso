from django.urls import path

from .views import LatestTextReviewView, TextReviewView


urlpatterns = [
    path("review/", TextReviewView.as_view(), name="text-review"),
    path("latest/", LatestTextReviewView.as_view(), name="latest-text-review"),
]

