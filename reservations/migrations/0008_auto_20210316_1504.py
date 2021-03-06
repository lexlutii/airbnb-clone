# Generated by Django 2.2.15 on 2021-03-16 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0007_bookedday_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedday',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_days', to='reservations.Reservation'),
        ),
    ]
