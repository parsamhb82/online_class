# Generated by Django 5.1.1 on 2024-11-06 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_class', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineclass',
            name='adding_start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 11, 6, 15, 45, 21, 210955, tzinfo=datetime.timezone.utc)),
        ),
    ]
