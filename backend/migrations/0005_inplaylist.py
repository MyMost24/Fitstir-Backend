# Generated by Django 3.0.3 on 2020-10-29 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20201029_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='InPlaylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.PlaylistVideo')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Video')),
            ],
        ),
    ]