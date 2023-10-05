# Generated by Django 4.2.1 on 2023-07-06 11:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tournament", "0002_ground_tournament_city_alter_tournament_status_and_more"),
        ("group", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="tournamentgroups",
            unique_together={("tournament_id", "name")},
        ),
        migrations.AlterModelTable(
            name="tournamentgroups",
            table="tournament_groups",
        ),
    ]