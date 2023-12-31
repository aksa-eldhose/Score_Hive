# Generated by Django 4.2.1 on 2023-05-23 11:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0005_team_city"),
    ]

    operations = [
        migrations.RenameField(
            model_name="team",
            old_name="createdAt",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="team",
            old_name="updatedAt",
            new_name="updated_at",
        ),
        migrations.AlterField(
            model_name="team",
            name="status",
            field=models.SmallIntegerField(default=0),
        ),
    ]
