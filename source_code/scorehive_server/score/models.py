from django.db import models

from accounts.models import User
from match.models import Matches
from team.models import Team


# Create your models here.
class Score(models.Model):
    EXTRAS_CHOICES = (
        (0, "WD"),
        (1, "NB"),
        (2, "LB"),
    )
    id = models.AutoField(primary_key=True)
    match_id = models.ForeignKey(
        Matches,
        on_delete=models.CASCADE,
        db_column="match_id",
        related_name="match_score",
    )
    inning = models.IntegerField()
    batting_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        db_column="batting_team",
        related_name="batting_team_score",
    )
    over = models.IntegerField()
    ball_number = models.IntegerField()
    striker_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="striker_id",
        related_name="striker_score",
    )
    non_striker_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="non_striker_id",
        related_name="non_striker_score",
        null=True,
    )
    bowler_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="bowler_id",
        related_name="bowler_score",
        null=True,
    )
    runs = models.IntegerField()
    extras = models.IntegerField(choices=EXTRAS_CHOICES, null=True)
    is_wicket = models.BooleanField(null=True)
    wicket_type = models.IntegerField(null=True)
    out_player_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="out_player_id",
        related_name="out_player_score",
        null=True,
    )
    fielder_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="fielder_id",
        related_name="fielder_score",
        null=True,
    )
    status = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "score"
