# Generated by Django 4.2.1 on 2023-08-17 08:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("team", "0009_alter_city_status_alter_team_status"),
        ("match", "0002_rename_datetime_matches_date_time_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Score",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("inning", models.IntegerField()),
                ("extras", models.IntegerField(null=True)),
                ("is_wicket", models.BooleanField(null=True)),
                ("wicket_type", models.IntegerField(null=True)),
                (
                    "batting_team",
                    models.ForeignKey(
                        db_column="batting_team",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="batting_team_score",
                        to="team.team",
                    ),
                ),
                (
                    "bowler_id",
                    models.ForeignKey(
                        db_column="bowler_id",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bowler_score",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "fielder_id",
                    models.ForeignKey(
                        db_column="fielder_id",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fielder_score",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "match_id",
                    models.ForeignKey(
                        db_column="match_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="match_score",
                        to="match.matches",
                    ),
                ),
                (
                    "non_striker_id",
                    models.ForeignKey(
                        db_column="non_striker_id",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="non_striker_score",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "out_player_id",
                    models.ForeignKey(
                        db_column="out_player_id",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="out_player_score",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "striker_id",
                    models.ForeignKey(
                        db_column="striker_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="striker_score",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "score",
            },
        ),
    ]