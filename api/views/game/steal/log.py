"""
    Returns a log of all steals in a game, in order by latest steal
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from jrdbnntt_com.util.forms import JsonField
from api.models import StealAttempt
from api.util.game import get_valid_game


class RequestForm(forms.Form):
    game_id = forms.IntegerField()


class ResponseForm(forms.Form):
    completed_steal_attempts = JsonField()


class LogView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        game = get_valid_game(req['game_id'])

        # Get all the steal attempts that are completed
        completed_steal_attempts = []
        for attempt in StealAttempt.objects.filter(
                game=game, status=StealAttempt.Status.COMPLETE
        ).order_by('-completed_at').all():
            completed_steal_attempts.append({
                'id': attempt.id,
                'completed_at': attempt.completed_at,
                'victim_username': attempt.victim.player.user.username,
                'thief_username': attempt.thief.player.user.username,
                'coins_stolen': attempt.coins_stolen,
                'thief_score': attempt.thief_score,
                'victim_score': attempt.victim_score
            })

        res['completed_steal_attempts'] = completed_steal_attempts
