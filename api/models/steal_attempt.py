from django.db import models
from django.contrib import admin
from cop4656_grab_bag.admin import site_admin
from api.models import PlayerInstance, Game
from datetime import timedelta, datetime
from django.utils import timezone


class StealAttempt(models.Model):
    class Status(object):
        WAITING_FOR_DEFENSE = 0
        VICTIM_DEFENDING = 1
        COMPLETE = 2
        choices = (
                (WAITING_FOR_DEFENSE, 'WAITING_FOR_DEFENSE'),
                (VICTIM_DEFENDING, 'VICTIM_DEFENDING'),
                (COMPLETE, 'COMPLETE')
            )

    created = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    thief = models.ForeignKey(to=PlayerInstance, on_delete=models.CASCADE, related_name='player_instance_thief')
    victim = models.ForeignKey(to=PlayerInstance, on_delete=models.CASCADE, related_name='player_instance_victim')
    status = models.PositiveIntegerField(default=Status.WAITING_FOR_DEFENSE, choices=Status.choices)
    thief_score = models.PositiveIntegerField()
    victim_score = models.PositiveIntegerField(null=True, blank=True)
    coins_stolen = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return '[StealAttempt ({}) {} <@- {}]'.format(
            self.game.name,
            self.thief.player.user.username,
            self.victim.player.user.username
        )

    def victim_defend_expiration_time(self) -> datetime:
        expire_time = self.created.date()
        steal_defend_seconds = self.game.steal_defend_seconds

        if self.status is self.Status.WAITING_FOR_DEFENSE:
            expire_time += timedelta(seconds=steal_defend_seconds)
        elif self.status is self.Status.VICTIM_DEFENDING:
            # Make sure they have time to actually play the defend game
            expire_time += timedelta(seconds=max(steal_defend_seconds*2, self.game.steal_game_seconds*2))

        return expire_time

    def victim_can_defend(self) -> bool:
        if self.status is self.Status.COMPLETE:
            return False
        return self.victim_defend_expiration_time() < timezone.now()


@admin.register(StealAttempt, site=site_admin)
class StealAttemptAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('id', 'game', 'thief', 'victim', 'coins_stolen', 'created')
    list_editable = ()
    list_display_links = ('id',)
    ordering = ('-created',)
    search_fields = (
        'game__name',
        'thief__player__user__player__username',
        'victim__player__user__player__username'
    )
