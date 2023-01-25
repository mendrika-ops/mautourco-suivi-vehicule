# Generated by Django 3.1.6 on 2023-01-21 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('mail', models.EmailField(max_length=150)),
                ('pswd', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('etat', models.IntegerField()),
            ],
        ),
    ]
