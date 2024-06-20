# Generated by Django 3.1.6 on 2023-03-08 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recordcommenttrajet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_trip', models.IntegerField()),
                ('comment', models.TextField(max_length=500)),
                ('vehicleno', models.CharField(max_length=100)),
                ('driver_oname', models.CharField(max_length=150)),
                ('FromPlace', models.CharField(max_length=150)),
                ('ToPlace', models.CharField(max_length=150)),
                ('trip_start_time', models.TimeField()),
                ('trip_start_date', models.CharField(max_length=15)),
                ('pick_up_time', models.TimeField()),
                ('status', models.CharField(max_length=100, null=True)),
                ('couleur', models.CharField(max_length=100, null=True)),
                ('daterecord', models.DateField()),
                ('etat', models.IntegerField(default=0)),
                ('driver_mobile_number', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'suiviVehicule_recordtrajet',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Statusparameterlib',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('min_percent', models.FloatField()),
                ('max_percent', models.FloatField()),
                ('couleur', models.CharField(max_length=50)),
                ('desce', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'suiviVehicule_statusparameterlib',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TrajetcoordonneeSamm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicleno', models.CharField(max_length=100)),
                ('driver_oname', models.CharField(max_length=150)),
                ('driver_mobile_number', models.CharField(max_length=50)),
                ('FromPlace', models.CharField(max_length=150)),
                ('ToPlace', models.CharField(max_length=150)),
                ('id_trip', models.IntegerField()),
                ('trip_no', models.IntegerField()),
                ('trip_start_date', models.CharField(max_length=15)),
                ('pick_up_time', models.TimeField()),
                ('PickUp_H_Pos', models.CharField(max_length=100)),
                ('PickEnd_H_Pos', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('duration', models.CharField(max_length=100, null=True)),
                ('couleur', models.CharField(max_length=100, null=True)),
                ('estimatetime', models.CharField(max_length=50, null=True)),
                ('datetime', models.CharField(max_length=15)),
                ('Uid', models.CharField(max_length=50, null=True)),
                ('idstatusposdetail', models.IntegerField(null=True)),
                ('trip_start_time', models.TimeField()),
                ('idstatusparameter', models.IntegerField(null=True)),
                ('difftimestart', models.FloatField()),
                ('difftimepickup', models.FloatField()),
                ('current', models.CharField(max_length=150, null=True)),
            ],
            options={
                'db_table': 'suivivehicle_laststatus',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TrajetcoordonneeWithUid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicleno', models.CharField(max_length=100)),
                ('driver_oname', models.CharField(max_length=150)),
                ('driver_mobile_number', models.CharField(max_length=50)),
                ('FromPlace', models.CharField(max_length=150)),
                ('ToPlace', models.CharField(max_length=150)),
                ('id_trip', models.IntegerField()),
                ('trip_no', models.IntegerField()),
                ('trip_start_date', models.CharField(max_length=15)),
                ('pick_up_time', models.TimeField()),
                ('PickUp_H_Pos', models.CharField(max_length=100)),
                ('Uid', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'suiviVehicule_trajetcoordonneesummary',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UidName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicleno', models.CharField(max_length=100)),
                ('Uid', models.CharField(max_length=50)),
                ('coordonnee', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'UidName',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Recordcomment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_trip', models.IntegerField()),
                ('comment', models.TextField(max_length=500)),
                ('datetime', models.DateTimeField()),
                ('etat', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Statusparameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('min_percent', models.FloatField()),
                ('max_percent', models.FloatField()),
                ('couleur', models.CharField(max_length=50)),
                ('desce', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Statuspos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('desc', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Trajetcoordonnee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicleno', models.CharField(max_length=100)),
                ('driver_oname', models.CharField(max_length=150)),
                ('driver_mobile_number', models.CharField(max_length=50)),
                ('FromPlace', models.CharField(max_length=150)),
                ('ToPlace', models.CharField(max_length=150)),
                ('id_trip', models.IntegerField()),
                ('trip_no', models.IntegerField()),
                ('trip_start_date', models.CharField(max_length=15)),
                ('pick_up_time', models.TimeField()),
                ('PickUp_H_Pos', models.CharField(max_length=100)),
                ('PickEnd_H_Pos', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('duration', models.CharField(max_length=100, null=True)),
                ('couleur', models.CharField(max_length=100, null=True)),
                ('estimatetime', models.CharField(max_length=50, null=True)),
                ('trip_start_time', models.TimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('mail', models.EmailField(max_length=150)),
                ('pswd', models.CharField(max_length=250)),
                ('contact', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('sexe', models.CharField(max_length=20, null=True)),
                ('description', models.TextField()),
                ('etat', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Statusposdetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=50)),
                ('coordonnee', models.CharField(max_length=100)),
                ('daty_time', models.DateTimeField()),
                ('duration', models.IntegerField(null=True)),
                ('id_trip', models.IntegerField(null=True)),
                ('current', models.CharField(max_length=150, null=True)),
                ('idmere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiviVehicule.statuspos')),
            ],
        ),
    ]
