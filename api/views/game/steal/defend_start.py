"""
    Start the defend of a steal attempt against the user
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import StealAttempt
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    steal_attempt_id = forms.IntegerField()


class DefendStartView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        # Get the attempt
        attempt = StealAttempt.objects.filter(
            id=req['steal_attempt_id'],
            status=StealAttempt.Status.WAITING_FOR_DEFENSE_START,
            victim__player__user=request.user
        ).all()
        if len(attempt) == 0:
            raise ValidationError('Invalid steal_attempt_id')
        attempt = attempt[0]

        # Update the status
        attempt.status = StealAttempt.Status.WAITING_FOR_DEFENSE_END
        attempt.save()

        # TODO cancel defend start timeout
        # TODO schedule defend end timeout
        # TODO update any COMPLETE_PENDING games

