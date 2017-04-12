from django.db import models
from django.contrib import admin
from cop4656_grab_bag.admin import site_admin
from api.models import Player


class PlayerInstance(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player = models.ManyToManyField(to=Player, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField()

    def __str__(self):
        return '[PlayerInstance {} {}]'.format(self.player.user.first_name, self.player.user.last_name)


@admin.register(PlayerInstance, site=site_admin)
class PlayerInstanceAdmin(admin.ModelAdmin):
    list_filter = None
    list_display = ('id', 'user_info', 'created')
    list_editable = None
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created',)

    @staticmethod
    def user_info(obj: PlayerInstance):
        user = obj.player
        return "{} {} - {}".format(user.first_name, user.last_name, user.email)
