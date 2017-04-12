# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 04:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'START_PENDING'), (1, 'ACTIVE'), (3, 'PAUSED'), (4, 'COMPLETE_PENDING'), (5, 'COMPLETE')], default=0)),
                ('name', models.CharField(max_length=100)),
                ('join_code', models.CharField(max_length=10)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('maximum_steal_distance_in_meters', models.PositiveIntegerField()),
                ('starting_coins', models.PositiveIntegerField()),
                ('steal_percent', models.PositiveIntegerField()),
                ('steal_game_seconds', models.PositiveIntegerField()),
                ('steal_defend_seconds', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('location_lat', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('location_lng', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('location_updated_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('coins', models.PositiveIntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Player')),
            ],
        ),
        migrations.CreateModel(
            name='StealAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveIntegerField(choices=[(0, 'WAITING_FOR_DEFENSE'), (1, 'VICTIM_DEFENDING'), (2, 'COMPLETE')], default=0)),
                ('thief_score', models.PositiveIntegerField()),
                ('victim_score', models.PositiveIntegerField(blank=True, null=True)),
                ('coins_stolen', models.PositiveIntegerField(blank=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Game')),
                ('thief', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_instance_thief', to='api.PlayerInstance')),
                ('victim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_instance_victim', to='api.PlayerInstance')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Player'),
        ),
    ]
