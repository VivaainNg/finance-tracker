from django.urls import path

from apps.charts.views import DisplayChartsView


urlpatterns = [
    path("", DisplayChartsView.as_view(), name="charts"),
]
