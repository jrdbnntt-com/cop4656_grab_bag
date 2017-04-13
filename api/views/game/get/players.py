"""
    Retrieve players and game with their coin amounts
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import PlayerInstance, Game
from django.core.exceptions import ValidationError
from jrdbnntt_com.util.forms import JsonField


class RequestForm(forms.Form):
    game_id = forms.IntegerField()


class ResponseForm(forms.Form):
    player_instances = JsonField()


class PlayersView(ApiView):
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

        player_instances = []
        for pi in PlayerInstance.objects.filter(game=game).all():
            player_instances.append({
                'id': pi.id,
                'coins': pi.coins,
                'username': pi.player.user.username
            })

        res['player_instances'] = player_instances
