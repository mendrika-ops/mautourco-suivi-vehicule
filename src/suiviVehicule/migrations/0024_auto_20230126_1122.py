# Generated by Django 3.1.6 on 2023-01-26 08:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suiviVehicule', '0023_auto_20230126_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusposdetail',
            name='datetime',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
