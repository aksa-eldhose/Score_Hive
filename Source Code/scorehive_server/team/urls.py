from django.urls import path

from .views import CityView, PlayerTeamsView, TeamView, TeamViewII

urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("cities/", CityView.as_view()),
    path("teams/<id>", TeamViewII.as_view()),
    path("playingTeams/", PlayerTeamsView.as_view()),
]
