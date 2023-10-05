from django.urls import path

from .views import MatchesView

urlpatterns = [
    path("schedule/", MatchesView.as_view(), name="scheduleMatch"),
    path("<tournament_id>/list/", MatchesView.as_view(), name="listMatch"),
    path("<match_id>/delete/", MatchesView.as_view(), name="deleteMatch"),
]
