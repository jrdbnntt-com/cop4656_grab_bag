"""
    Create a new game
"""

from django import forms
from django.http.request import HttpRequest
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import Game, PlayerInstance, Player
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    name = forms.CharField(max_length=100)
    join_code = forms.CharField(max_length=10)
    duration_in_minutes = forms.IntegerField(min_value=1)
    maximum_steal_distance_in_meters = forms.IntegerField(min_value=1)
    starting_coins = forms.IntegerField(min_value=1)
    steal_percent = forms.IntegerField(min_value=1)
    steal_game_seconds = forms.IntegerField(min_value=1)
    steal_defend_seconds = forms.IntegerField(min_value=1)
    steal_cool_down_seconds = forms.IntegerField(min_value=0)


class ResponseForm(forms.Form):
    game_id = forms.IntegerField()


class CreateView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request: HttpRequest, req: dict, res: dict):
        # Make sure request code not in use
        if Game.objects.filter(status=Game.Status.START_PENDING, join_code__iexact=req['join_code']).exists():
            raise ValidationError('Join code already in use')

        player = Player.objects.get(user=request.user)

        # Create the game
        game = Game.objects.create(
            creator=player,
            name=req['name'],
            join_code=req['join_code'].lower(),
            duration_in_minutes=req['duration_in_minutes'],
            maximum_steal_distance_in_meters=req['maximum_steal_distance_in_meters'],
            starting_coins=req['starting_coins'],
            steal_percent=req['steal_percent'],
            steal_game_seconds=req['steal_game_seconds'],
            steal_defend_seconds=req['steal_defend_seconds'],
            steal_cool_down_seconds=req['steal_cool_down_seconds']
        )

        # Give the player an instance
        PlayerInstance.objects.create(
            player=player,
            game=game,
            coins=game.starting_coins
        )

        res['game_id'] = game.id
