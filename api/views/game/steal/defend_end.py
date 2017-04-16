"""
    Finish a defend against the user
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import StealAttempt
from django.core.exceptions import ValidationError
from api.util.game import finalize_steal_attempt


class RequestForm(forms.Form):
    steal_attempt_id = forms.IntegerField()
    score = forms.IntegerField(min_value=0)


class DefendEndView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        # Get the attempt
        attempt = StealAttempt.objects.filter(
            id=req['steal_attempt_id'],
            status=StealAttempt.Status.WAITING_FOR_DEFENSE_END,
            victim__player__user=request.user
        ).all()
        if len(attempt) == 0:
            raise ValidationError('Invalid steal_attempt_id')
        attempt = attempt[0]

        # Finalize the attempt
        attempt.victim_score = req['score']
        attempt.coins_stolen = attempt.calculate_coins_stolen()
        attempt.save()
        finalize_steal_attempt(attempt)

        # TODO cancel defend end timeout
        # TODO update any COMPLETE_PENDING games
