# Generated by Django 2.2.15 on 2021-03-15 20:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0006_auto_20210315_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedday',
            name='day',
            field=models.DateField(default=datetime.datetime(2021, 3, 15, 20, 19, 29, 331508, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
