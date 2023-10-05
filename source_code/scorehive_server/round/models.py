from django.db import models

from tournament.models import Tournament

# Create your models here.


class RoundManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class Round(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    round_type = models.SmallIntegerField(default=1)
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "round"


class TournamentRounds(models.Model):
    id = models.AutoField(primary_key=True)
    tournament_id = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        db_column="tournament_id",
        related_name="tournamentRounds_tournament",
    )
    round_id = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        db_column="round_id",
        related_name="tournamentRounds_round",
    )
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tournament_rounds"
