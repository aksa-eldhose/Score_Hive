from django.urls import path

from team_tournaments.views import (AddTeamtoTournament,
                                    RemoveTeamFromTournament)

urlpatterns = [
    path(
        "addTeamtoTournament/",
        AddTeamtoTournament.as_view(),
        name="addTeamtoTournament",
    ),
    path(
        "removeTeamFromTournament/",
        RemoveTeamFromTournament.as_view(),
        name="removeTeamFromTournament",
    ),
]
