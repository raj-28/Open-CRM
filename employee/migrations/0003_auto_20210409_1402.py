# Generated by Django 3.1.7 on 2021-04-09 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20210409_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='hr_attendance',
            name='duration',
        ),
    ]
