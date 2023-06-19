# Generated by Django 3.2.16 on 2022-12-01 17:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("telemetry", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="session",
            name="driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions",
                to="telemetry.driver",
            ),
        ),
        migrations.AlterField(
            model_name="session",
            name="game",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions",
                to="telemetry.game",
            ),
        ),
        migrations.AlterField(
            model_name="session",
            name="session_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions",
                to="telemetry.sessiontype",
            ),
        ),
    ]
