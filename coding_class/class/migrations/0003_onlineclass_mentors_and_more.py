# Generated by Django 5.1.1 on 2024-09-29 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0002_onlineclass_available_and_more'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineclass',
            name='mentors',
            field=models.ManyToManyField(blank=True, related_name='mentors', to='user.userprofile'),
        ),
        migrations.AlterField(
            model_name='onlineclass',
            name='adding_start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 29, 14, 23, 28, 38810, tzinfo=datetime.timezone.utc)),
        ),
    ]
