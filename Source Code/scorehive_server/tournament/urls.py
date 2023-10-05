from django.urls import path

from .views import (DeleteTournament, GroundView, HomeTournamentView,
                    PublicTournamentTeam, TournamentTeamView, TournamentView,
                    TournamentViewII)

urlpatterns = [
    path("tournament/", TournamentView.as_view()),
    path("ground/", GroundView.as_view()),
    path("home/", HomeTournamentView.as_view()),
    path("home/<id>", TournamentViewII.as_view()),
    path("teams/<id>/", TournamentTeamView.as_view()),
    path("<id>/teams/", PublicTournamentTeam.as_view()),
    path("tournamentDelete/", DeleteTournament.as_view(), name="deleteTournament"),
]
