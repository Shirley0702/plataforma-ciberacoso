from django.urls import path

from .views import OrientationResourceListView


urlpatterns = [path("", OrientationResourceListView.as_view(), name="resources")]
