# Generated by Django 4.2.3 on 2023-08-17 07:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("telemetry", "0012_alter_coach_mode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coach",
            name="mode",
            field=models.CharField(
                choices=[
                    ("default", "Default"),
                    ("debug", "Debug"),
                    ("only_brake", "Only Brakepoints"),
                    ("only_brake_debug", "Only Brakepoints (Debug))"),
                ],
                default="default",
                max_length=64,
            ),
        ),
    ]