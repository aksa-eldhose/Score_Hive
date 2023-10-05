from django.urls import path

from .views import AllRoundsInTournament, RoundsView, TournamentRoundsView

urlpatterns = [
    path("addRound/", TournamentRoundsView.as_view(), name="addRoundsTournament"),
    path("rounds/", RoundsView.as_view(), name="listAllRounds"),
    path("remove/", TournamentRoundsView.as_view(), name="removeRound"),
    path(
        "<tournament_id>/rounds/",
        TournamentRoundsView.as_view(),
        name="listAllRoundsInTournament",
    ),
    path(
        "<tournament_id>/rounds/noPaged",
        AllRoundsInTournament.as_view(),
        name="listAllRoundsNonPaginated",
    ),
]
