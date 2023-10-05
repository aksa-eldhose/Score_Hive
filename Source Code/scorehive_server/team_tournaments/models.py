from django.db import models

from team.models import Team
from tournament.models import Tournament

# Create your models here.


class TeamTournamentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)

    def get_deleted_row(self, **kwargs):
        return super().get_queryset().get(**kwargs)


class TeamTournaments(models.Model):
    id = models.AutoField(primary_key=True)
    tournament_id = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        db_column="tournament_id",
        related_name="teamTournament_tournament",
    )
    team_id = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        db_column="team_id",
        related_name="teamTournament_team",
    )
    status = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TeamTournamentManager()

    class Meta:
        db_table = "tournament_teams"
        unique_together = ("tournament_id", "team_id")
