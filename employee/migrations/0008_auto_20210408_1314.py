# Generated by Django 3.1.7 on 2021-04-08 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_auto_20210408_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='duration',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hr_attendance',
            name='duration',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
