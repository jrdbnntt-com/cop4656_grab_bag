from django.db import models
from django.contrib import admin
from cop4656_grab_bag.admin import site_admin
from api.models import Player, PlayerInstance


class Game(models.Model):
    class Status(object):
        START_PENDING = 0
        ACTIVE = 1
        PAUSED = 3
        COMPLETE = 4

        @staticmethod
        def choices():
            return (
                (Game.Status.START_PENDING, 'START_PENDING'),
                (Game.Status.ACTIVE, 'ACTIVE'),
                (Game.Status.PAUSED, 'PAUSED'),
                (Game.Status.COMPLETE, 'COMPLETE')
            )

    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    player_instances = models.ManyToManyField(to=PlayerInstance)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name = models.CharField(max_length=100)
    status = models.IntegerField(choices=Status.choices())

    def __str__(self):
        return '[Game {}]'.format(self.name)


@admin.register(Game, site=site_admin)
class GameAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('id', 'name', 'creator', 'start_time', 'end_time', 'status', 'created')
    list_editable = None
    list_display_links = ('id',)
    search_fields = ('name',)
    ordering = ('-created',)
