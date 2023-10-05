# Generated by Django 4.2.1 on 2023-07-25 05:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("group", "0004_tournamentgroups_round_id"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="tournamentgroups",
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name="tournamentgroups",
            constraint=models.UniqueConstraint(
                condition=models.Q(("status", 1)),
                fields=("tournament_id", "name"),
                name="unique_group_in_tournament",
            ),
        ),
    ]