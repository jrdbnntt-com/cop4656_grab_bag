"""
    Returns all the games the current player has participated in or is participating in
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import PlayerInstance
from jrdbnntt_com.util.forms import JsonField


class ResponseForm(forms.Form):
    games = JsonField()


class GameHistoryView(ApiView):
    http_method_names = ['get']
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        games = []
        for pi in PlayerInstance.objects.filter(player__user=request.user).order_by('-created').all():
            games.append({
                'player_instance_id': pi.id,
                'player_instance_coins': pi.coins,
                'game_id': pi.game.id,
                'game_status': pi.game.status,
                'game_name': pi.game.name
            })

        res['games'] = games
