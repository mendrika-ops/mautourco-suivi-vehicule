# Generated by Django 5.1.2 on 2024-12-10 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("suiviVehicule", "0033_delete_user_lograpportauto_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogRapportAutoView",
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
                ("log_recipient", models.CharField(max_length=100, null=True)),
                ("log_result", models.TextField()),
                ("log_status", models.CharField(max_length=100, null=True)),
                ("log_created_at", models.DateTimeField()),
                ("rapport_id", models.IntegerField()),
                ("rapport_title", models.CharField(max_length=100, null=True)),
                ("rapport_description", models.TextField()),
                ("rapport_created_at", models.DateTimeField()),
                ("rapport_is_active", models.BooleanField()),
                ("type_rapport_id", models.IntegerField()),
                ("type_rapport_type", models.CharField(max_length=100, null=True)),
                ("type_rapport_description", models.TextField()),
                ("type_rapport_is_active", models.BooleanField()),
                ("user_id", models.IntegerField(null=True)),
                ("user_username", models.CharField(max_length=150, null=True)),
                ("user_email", models.EmailField(max_length=254, null=True)),
            ],
            options={"db_table": "log_rapport_auto_view", "managed": False,},
        ),
        migrations.CreateModel(
            name="RapportAutoView",
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
                ("rapport_title", models.CharField(max_length=100, null=True)),
                ("rapport_description", models.TextField()),
                ("rapport_created_at", models.DateTimeField()),
                ("rapport_is_active", models.BooleanField()),
                ("type_rapport_id", models.IntegerField()),
                ("type_rapport_type", models.CharField(max_length=100, null=True)),
                ("type_rapport_description", models.TextField()),
                ("type_rapport_created_at", models.DateTimeField()),
                ("type_rapport_is_active", models.BooleanField()),
                ("group_id", models.IntegerField()),
                ("group_name", models.CharField(max_length=150)),
            ],
            options={"db_table": "rapport_auto_view", "managed": False,},
        ),
        migrations.AlterField(
            model_name="statusposdetail",
            name="odometer",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
