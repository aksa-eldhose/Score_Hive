from django.db import models

from round.models import Round
from team.models import Team
from tournament.models import City, Ground, Tournament


# Create your models here.
class Matches(models.Model):
    id = models.AutoField(primary_key=True)
    tournament_id = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        db_column="tournament_id",
        related_name="tournament_matches",
    )
    team1 = models.ForeignKey(
        Team, on_delete=models.CASCADE, db_column="team1", related_name="match_team1"
    )
    team2 = models.ForeignKey(
        Team, on_delete=models.CASCADE, db_column="team2", related_name="match_team2"
    )
    ground_id = models.ForeignKey(
        Ground,
        on_delete=models.CASCADE,
        db_column="ground_id",
        related_name="match_ground",
    )
    city_id = models.ForeignKey(
        City, on_delete=models.CASCADE, db_column="city_id", related_name="match_city"
    )
    date_time = models.DateTimeField()
    round_id = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        db_column="round_id",
        related_name="match_round",
    )
    match_type = models.SmallIntegerField()
    over_per_bowler = models.IntegerField()
    total_overs = models.IntegerField()
    ball_type = models.IntegerField()
    winner_team_id = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        db_column="winner_team_id",
        related_name="match_winner",
        null=True,
    )
    status = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "matches"
