# Generated by Django 3.1.7 on 2021-04-09 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='duration',
            field=models.CharField(blank=True, default='0:0', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='hr_attendance',
            name='duration',
            field=models.CharField(blank=True, default='0:0', max_length=50, null=True),
        ),
    ]