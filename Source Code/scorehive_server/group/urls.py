from django.urls import path

from .views import (DeleteGroupView, TournamentGroupDetails,
                    TournamentGroupsView, TournamentGroupTeamListView)

urlpatterns = [
    path("addGroup/", TournamentGroupsView.as_view(), name="createGroup"),
    path(
        "<tournament_id>/listGroup/", TournamentGroupsView.as_view(), name="listGroup"
    ),
    path(
        "<tournament_id>/listTeam/",
        TournamentGroupTeamListView.as_view(),
        name="listUngroupedTeams",
    ),
    path("editGroup/", TournamentGroupsView.as_view(), name="updateGroup"),
    path("remove/", DeleteGroupView.as_view(), name="deleteGroup"),
    path("details/<group_id>/", TournamentGroupDetails.as_view(), name="groupDetails"),
]
