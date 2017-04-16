from django.db import models
from django.contrib import admin
from cop4656_grab_bag.admin import site_admin
from api.models import PlayerInstance, Game
from datetime import timedelta, datetime
from django.utils import timezone


class StealAttempt(models.Model):
    class Status(object):
        WAITING_FOR_THIEF_END = 0
        WAITING_FOR_DEFENSE_START = 2
        WAITING_FOR_DEFENSE_END = 3
        COMPLETE = 4
        EXPIRED = 5

        choices = (
                (WAITING_FOR_THIEF_END, 'WAITING_FOR_THIEF_END'),
                (WAITING_FOR_DEFENSE_START, 'WAITING_FOR_DEFENSE_START'),
                (WAITING_FOR_DEFENSE_END, 'WAITING_FOR_DEFENSE_END'),
                (COMPLETE, 'COMPLETE'),
                (EXPIRED, 'EXPIRED')
            )

    created = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    thief = models.ForeignKey(to=PlayerInstance, on_delete=models.CASCADE, related_name='player_instance_thief')
    victim = models.ForeignKey(to=PlayerInstance, on_delete=models.CASCADE, related_name='player_instance_victim')
    status = models.PositiveIntegerField(default=Status.WAITING_FOR_THIEF_END, choices=Status.choices)
    thief_score = models.PositiveIntegerField(null=True, blank=True)
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

        if self.status is self.Status.WAITING_FOR_DEFENSE_END:
            expire_time += timedelta(seconds=steal_defend_seconds)
        elif self.status is self.Status.WAITING_FOR_DEFENSE_START:
            # Make sure they have time to actually play the defend game
            expire_time += timedelta(seconds=max(steal_defend_seconds*2, self.game.steal_game_seconds*2))

        return expire_time

    def victim_can_defend(self) -> bool:
        if self.status is self.Status.COMPLETE:
            return False
        return self.victim_defend_expiration_time() < timezone.now()

    def calculate_coins_stolen(self) -> int:
        if self.victim_score is not None and self.thief_score < self.victim_score:
            # Failed to steal
            return 0

        coins = max(int(round(self.victim.coins * (self.game.steal_percent/100.0))), 1)
        if coins > self.victim.coins:
            coins = self.victim.coins
        return coins


@admin.register(StealAttempt, site=site_admin)
class StealAttemptAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = (
        'id', 'game', 'thief', 'victim', 'status', 'thief_score', 'victim_score', 'coins_stolen',
        'created', 'completed_at'
    )
    list_editable = ('thief_score', 'victim_score')
    list_display_links = ('id',)
    ordering = ('-created',)
    search_fields = (
        'game__name',
        'thief__player__user__player__username',
        'victim__player__user__player__username'
    )
