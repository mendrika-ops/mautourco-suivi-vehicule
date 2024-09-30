# Generated by Django 3.1.6 on 2024-09-29 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suiviVehicule', '0019_statusposdetail_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusposMin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=50, null=True)),
                ('daty_time', models.DateTimeField()),
                ('duration', models.IntegerField(null=True)),
                ('id_trip', models.IntegerField(null=True)),
                ('distance', models.FloatField(null=True)),
                ('is_call_api', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'suivivehicule_statuspos_min',
                'managed': False,
            },
        ),
    ]