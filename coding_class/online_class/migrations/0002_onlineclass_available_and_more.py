# Generated by Django 5.1.1 on 2024-09-29 07:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineclass',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='onlineclass',
            name='adding_start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 29, 7, 2, 31, 370384, tzinfo=datetime.timezone.utc)),
        ),
    ]
