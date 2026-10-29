from django.urls import path

from .views import DashboardView, MeView, PasswordChangeView, ProfileView


urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password/", PasswordChangeView.as_view(), name="password_change"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
