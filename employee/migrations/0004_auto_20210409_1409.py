# Generated by Django 3.1.7 on 2021-04-09 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20210409_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='work_duration',
            field=models.CharField(blank=True, default='00:00:00 Hr', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='hr_attendance',
            name='work_duration',
            field=models.CharField(blank=True, default='00:00:00 Hr', max_length=20, null=True),
        ),
    ]