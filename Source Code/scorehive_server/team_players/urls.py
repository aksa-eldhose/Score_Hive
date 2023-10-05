from django.urls import path

from .views import (CheckPlayerTeamMember, ExitPlayerFromTeam,
                    InviteExistingPlayerToTeam, InvitePlayerToTeam,
                    PlayerJoinToTeam, PlayerList, RemovePlayerFromTeam,
                    SearchPlayer)

urlpatterns = [
    path("listPlayers/<teamid>/", PlayerList.as_view(), name="playerList"),
    path("searchPlayer/", SearchPlayer.as_view(), name="searchPlayer"),
    path(
        "checkIfTeamMember/",
        CheckPlayerTeamMember.as_view(),
        name="checkPlayerMemberOfTeam",
    ),
    path("joinToTeam/", PlayerJoinToTeam.as_view(), name="playerJoinToTeam"),
    path("invitePlayer/", InvitePlayerToTeam.as_view(), name="invitePlayerToTeam"),
    path(
        "addtoPlayertoTeam/",
        InviteExistingPlayerToTeam.as_view(),
        name="inviteExistingPlayer",
    ),
    path(
        "removeFromTeam/", RemovePlayerFromTeam.as_view(), name="removePlayerFromTeam"
    ),
    path(
        "<team_id>/exitFromTeam/",
        ExitPlayerFromTeam.as_view(),
        name="exitPlayerFromTeam",
    ),
]
