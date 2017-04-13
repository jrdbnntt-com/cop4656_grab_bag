"""
    Join a pending game
"""

from django import forms
from django.http.request import HttpRequest
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import PlayerInstance, Player, Game
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    game_join_code = forms.CharField(max_length=100)


class ResponseForm(forms.Form):
    game_id = forms.IntegerField()
    game_name = forms.CharField()


class JoinView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request: HttpRequest, req: dict, res: dict):
        # Get the game
        game = Game.objects.filter(join_code__iexact=req['game_join_code'], status=Game.Status.START_PENDING).all()
        if len(game) == 0:
            raise ValidationError('Invalid game_join_code')
        game = game[0]

        player = Player.objects.get(user=request.user)

        # Already in it?
        if PlayerInstance.objects.filter(game=game, player=player).exists():
            raise ValidationError('Cannot join, already in game')

        # Give the player an instance
        PlayerInstance.objects.create(
            player=player,
            game=game,
            coins=game.starting_coins
        )

        res['game_id'] = game.id
        res['game_name'] = game.name
