# Generated by Django 4.2.1 on 2023-06-19 04:46

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0009_alter_city_status_alter_team_status"),
        ("tournament", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ground",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("status", models.IntegerField(default=1)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "ground",
            },
        ),
        migrations.AddField(
            model_name="tournament",
            name="city",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="team.city"
            ),
        ),
        migrations.AlterField(
            model_name="tournament",
            name="status",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="tournament",
            name="ground",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="tournament.ground",
            ),
        ),
    ]
