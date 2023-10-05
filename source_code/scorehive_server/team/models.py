from django.db import models
from django.utils import timezone

from accounts.models import User


class TeamManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=0)


# Create your models here.
class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "city"


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    logo_url = models.FileField(
        upload_to="my_pictures", null=True, blank=True, default=None
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0)
    objects = TeamManager()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "team"
