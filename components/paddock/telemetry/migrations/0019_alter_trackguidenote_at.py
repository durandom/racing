# Generated by Django 4.2.3 on 2023-08-28 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("telemetry", "0018_trackguidenote_at_alter_coach_mode_alter_fastlap_car_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trackguidenote",
            name="at",
            field=models.TextField(null=True),
        ),
    ]