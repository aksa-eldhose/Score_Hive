from django.db import models

from round.models import Round
from team.models import Team
from tournament.models import Tournament

# Create your models here.


class TournamentGroupsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class TournamentGroups(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tournament_id = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        db_column="tournament_id",
        related_name="tournamentGroups_tournament",
    )
    round_id = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        db_column="round_id",
        related_name="tournamentGroups_round",
        default=1,
    )
    status = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TournamentGroupsManager()

    class Meta:
        db_table = "tournament_groups"
        constraints = [
            models.UniqueConstraint(
                fields=["tournament_id", "name"],
                condition=models.Q(status=1),
                name="unique_group_in_tournament",
            )
        ]


class TournamentGroupTeamsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class TournamentGroupTeams(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(
        TournamentGroups,
        on_delete=models.CASCADE,
        db_column="group_id",
        related_name="tournamentGroupTeams_tournamentGroups",
    )
    team_id = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        db_column="team_id",
        related_name="tournamentGroupTeams_Team",
    )
    status = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TournamentGroupTeamsManager()

    class Meta:
        db_table = "tournament_group_teams"
