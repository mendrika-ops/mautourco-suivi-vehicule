# Generated by Django 3.1.6 on 2023-03-22 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suiviVehicule', '0006_auto_20230317_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusposdetail',
            name='uid',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
