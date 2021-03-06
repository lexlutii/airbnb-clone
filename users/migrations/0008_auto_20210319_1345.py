# Generated by Django 2.2.15 on 2021-03-19 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210311_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('ml', 'Male'), ('fml', 'Female'), ('usp', 'Uncpecified')], default='usp', max_length=3, verbose_name='gender'),
        ),
    ]
