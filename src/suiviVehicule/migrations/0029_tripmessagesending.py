# Generated by Django 5.1.2 on 2024-10-12 07:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("suiviVehicule", "0028_trajetcoordonneevehicleinfo"),
    ]

    operations = [
        migrations.CreateModel(
            name="TripMessageSending",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, null=True)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_send", models.BooleanField(default=False)),
                (
                    "planning",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="planning_tripmessage_sending",
                        to="suiviVehicule.planning",
                    ),
                ),
            ],
        ),
    ]