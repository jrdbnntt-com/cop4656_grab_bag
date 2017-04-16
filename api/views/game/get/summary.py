"""
    Get a game's basic information
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import PlayerInstance, Game
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    game_id = forms.IntegerField()


class ResponseForm(forms.Form):
    id = forms.IntegerField()
    status = forms.IntegerField()
    end_time = forms.DateTimeField(required=False)
    start_time = forms.DateTimeField(required=False)
    name = forms.CharField()
    join_code = forms.CharField()
    duration_in_minutes = forms.IntegerField()
    maximum_steal_distance_in_meters = forms.IntegerField()
    starting_coins = forms.IntegerField()
    steal_percent = forms.IntegerField()
    steal_game_seconds = forms.IntegerField()
    steal_defend_seconds = forms.IntegerField()
    steal_cool_down_seconds = forms.IntegerField()
    player_count = forms.IntegerField()
    creator_username = forms.CharField()


class SummaryView(ApiView):
    http_method_names = ['get']
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        # Get the game
        game = Game.objects.filter(id=req['game_id']).all()
        if len(game) == 0:
            raise ValidationError('Invalid game_id')
        game = game[0]

        res['id'] = game.id
        res['status'] = game.status
        res['start_time'] = game.start_time
        res['end_time'] = game.end_time
        res['name'] = game.name
        res['join_code'] = game.join_code
        res['duration_in_minutes'] = game.duration_in_minutes
        res['maximum_steal_distance_in_meters'] = game.maximum_steal_distance_in_meters
        res['starting_coins'] = game.starting_coins
        res['steal_percent'] = game.steal_percent
        res['steal_game_seconds'] = game.steal_game_seconds
        res['steal_defend_seconds'] = game.steal_defend_seconds
        res['steal_cool_down_seconds'] = game.steal_cool_down_seconds
        res['player_count'] = PlayerInstance.objects.filter(game=game).count()
        res['creator_username'] = game.creator.user.username

