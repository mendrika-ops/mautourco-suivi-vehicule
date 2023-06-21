# Generated by Django 3.1.6 on 2023-03-12 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suiviVehicule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordcomment',
            name='FromPlace',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='recordcomment',
            name='ToPlace',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='recordcomment',
            name='driver_mobile_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='recordcomment',
            name='driver_oname',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='recordcomment',
            name='pick_up_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='recordcomment',
            name='trip_start_date',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='recordcomment',
            name='vehicleno',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recordcomment',
            name='datetime',
            field=models.DateField(),
        ),
    ]
