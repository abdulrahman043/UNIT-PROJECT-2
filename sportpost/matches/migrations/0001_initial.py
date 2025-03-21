# Generated by Django 5.1.7 on 2025-03-20 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('leauge', models.CharField(blank=True, max_length=6, null=True)),
                ('logo', models.ImageField(blank=True, default='images/team_logo/default.png', null=True, upload_to='images/team_logo/')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('home_score', models.PositiveIntegerField(default=0)),
                ('away_score', models.PositiveIntegerField(default=0)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_matches', to='matches.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_matches', to='matches.team')),
            ],
        ),
    ]
