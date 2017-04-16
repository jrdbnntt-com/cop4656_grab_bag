from django.db import models
from django.contrib import admin
from cop4656_grab_bag.admin import site_admin
from api.models import Player


class Game(models.Model):
    class Status(object):
        START_PENDING = 0       # Waiting for creator to start game, new players can join the game
        ACTIVE = 1              # Game is live, players may steal from one another
        PAUSED = 3              # players may not steal from one another temporarily
        COMPLETE_PENDING = 4    # Waiting for any unfinished steal attempts
        COMPLETE = 5            # Scores are final, no pending steal attempts
        choices = (
                (START_PENDING, 'START_PENDING'),
                (ACTIVE, 'ACTIVE'),
                (PAUSED, 'PAUSED'),
                (COMPLETE_PENDING, 'COMPLETE_PENDING'),
                (COMPLETE, 'COMPLETE')
            )

    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    status = models.IntegerField(default=Status.START_PENDING, choices=Status.choices)
    end_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)

    # Configuration
    name = models.CharField(max_length=100)
    join_code = models.CharField(max_length=100)
    duration_in_minutes = models.PositiveIntegerField()
    maximum_steal_distance_in_meters = models.PositiveIntegerField()
    starting_coins = models.PositiveIntegerField()
    steal_percent = models.PositiveIntegerField()           # Percent of victim coins stolen on successful steal
    steal_game_seconds = models.PositiveIntegerField()      # Seconds to tap screen in steal game (defending/stealing)
    steal_defend_seconds = models.PositiveIntegerField()    # Seconds to wait for victim to initiate defend
    steal_cool_down_seconds = models.PositiveIntegerField() # Seconds before thief can steal from victim again

    def __str__(self):
        return '[Game {}]'.format(self.name)

    def max_view_distance_in_meters(self):
        return self.maximum_steal_distance_in_meters * 3


@admin.register(Game, site=site_admin)
class GameAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('id', 'name', 'join_code', 'status', 'creator', 'start_time', 'end_time', 'created')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('name', 'join_code', 'creator__user__username')
    ordering = ('-created',)
