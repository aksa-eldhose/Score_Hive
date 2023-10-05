from django.db import models
from django.utils import timezone

from accounts.models import User
from team.models import City

type_1 = "Type 1"
type_2 = "Type 2"
type_3 = "Type 3"


# Create your models here.
class TournamentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class Ground(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ground"


class Tournament(models.Model):
    BALL_TYPE_CHOICES = (
        (0, type_1),
        (1, type_2),
        (2, type_3),
    )
    TOURNAMENT_TYPE_CHOICES = (
        (0, type_1),
        (1, type_2),
        (2, type_3),
    )
    MATCH_TYPE_CHOICES = (
        (0, type_1),
        (1, type_2),
        (2, type_3),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    ball_type = models.SmallIntegerField(choices=BALL_TYPE_CHOICES)
    tournament_type = models.SmallIntegerField(choices=TOURNAMENT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    match_type = models.SmallIntegerField(choices=MATCH_TYPE_CHOICES)
    description = models.CharField(max_length=500, null=True)
    logo_url = models.FileField(
        upload_to="Tour_logo", null=True, blank=True, default=None
    )
    banner_url = models.FileField(
        upload_to="Tour_banner", null=True, blank=True, default=None
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    deleted_reason = models.CharField(max_length=150, null=True)
    deleted_description = models.CharField(max_length=255, null=True)
    player_of_tournament = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="player_of_tournament",
        related_name="best_player_tournaments",
        null=True,
    )
    best_batsman = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="best_batsman",
        related_name="best_batsman_tournaments",
        null=True,
    )
    best_bowler = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="best_bowler",
        related_name="best_bowler_tournaments",
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    ground = models.ForeignKey(Ground, on_delete=models.CASCADE)
    objects = TournamentManager()

    class Meta:
        db_table = "tournament"
