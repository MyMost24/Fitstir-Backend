# Generated by Django 3.0.3 on 2020-10-29 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20201028_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='imageChallenge',
        ),
    ]