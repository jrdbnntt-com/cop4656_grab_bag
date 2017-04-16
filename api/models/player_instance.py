from django.db import models
from django.contrib import admin
from cop4656_grab_bag.admin import site_admin
from api.models import Player, Game


class PlayerInstance(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField()

    def __str__(self):
        return '[PlayerInstance {}]'.format(self.player.user.username)


@admin.register(PlayerInstance, site=site_admin)
class PlayerInstanceAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('id', 'player', 'game', 'coins', 'created')
    list_editable = ('coins',)
    list_display_links = ('id',)
    search_fields = ('player__user_username', 'game__name')
    ordering = ('-created',)
