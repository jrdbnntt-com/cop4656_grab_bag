"""
    Start a pending game that you created
"""

from django import forms
from django.http.request import HttpRequest
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import Game
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class RequestForm(forms.Form):
    game_id = forms.IntegerField()


class StartView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request: HttpRequest, req: dict, res: dict):
        # Retrieve the game
        game = Game.objects.filter(
            id=req['game_id'],
            creator__user=request.user,
            status=Game.Status.START_PENDING
        ).all()
        if len(game) == 0:
            raise ValidationError('Invalid game_id')
        game = game[0]

        # Start the game
        game.status = Game.Status.ACTIVE
        game.start_time = timezone.now()
        game.end_time = game.start_time + timedelta(minutes=game.duration_in_minutes)
        game.save()

        # TODO schedule game end job
        # TODO send push notification to players with game state change

