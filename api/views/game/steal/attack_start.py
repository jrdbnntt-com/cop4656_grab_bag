"""
    Retrieve players and game with their coin amounts
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.util.game import get_valid_game_with_status, get_valid_player_instance, get_valid_player_instance_from_user
from api.models import Game, StealAttempt
from api.util import location
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    game_id = forms.IntegerField()
    victim_instance_id = forms.IntegerField()


class ResponseForm(forms.Form):
    steal_attempt_id = forms.IntegerField()


class AttackStartView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        # Get the game and players
        game = get_valid_game_with_status(game_id=req['game_id'], status=Game.Status.ACTIVE)
        victim = get_valid_player_instance(game, req['victim_instance_id'], 'Invalid victim_instance_id')
        thief = get_valid_player_instance_from_user(game, request.user, 'Invalid attacker, player not in game')

        # Make sure victim is in range of attacker
        dist = location.distance_in_meters(thief.player, victim.player)
        if dist > game.maximum_steal_distance_in_meters:
            raise ValidationError('Victim out of steal range')

        # All good, start the steal
        attempt = StealAttempt.objects.create(
            game=game,
            thief=thief,
            victim=victim
        )

        res['steal_attempt_id'] = attempt.id

        # TODO schedule steal timeout
