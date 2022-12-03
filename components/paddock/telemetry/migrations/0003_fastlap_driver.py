# Generated by Django 3.2.16 on 2022-12-03 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("telemetry", "0002_auto_20221201_1729"),
    ]

    operations = [
        migrations.AddField(
            model_name="fastlap",
            name="driver",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fast_laps",
                to="telemetry.driver",
            ),
        ),
    ]
