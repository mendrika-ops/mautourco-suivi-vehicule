# Generated by Django 3.1.6 on 2023-01-25 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suiviVehicule', '0016_auto_20230125_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trajetcoordonnee',
            name='PickEnd_H_Pos',
        ),
    ]
