from django.db import models

from accounts.models import User
from team.models import Team

# Create your models here.


class TeamPlayersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)

    def get_deleted_row(self, **kwargs):
        return super().get_queryset().get(**kwargs)


class TeamPlayers(models.Model):
    id = models.AutoField(primary_key=True)
    team_id = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        db_column="team_id",
        related_name="team_players_team",
    )
    player_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="player_id",
        related_name="team_players",
    )
    status = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TeamPlayersManager()

    class Meta:
        db_table = "team_players"
        unique_together = ("team_id", "player_id")
