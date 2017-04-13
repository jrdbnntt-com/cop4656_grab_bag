"""
    Update's the user's player's location
"""

from django import forms
from django.http.request import HttpRequest
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import Player
from django.utils import timezone


class RequestForm(forms.Form):
    location_lat = forms.DecimalField(max_digits=10, decimal_places=6)
    location_lng = forms.DecimalField(max_digits=10, decimal_places=6)


class UpdateLocationView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request: HttpRequest, req: dict, res: dict):
        player = Player.objects.get(user=request.user)
        player.location_lat = req['location_lat']
        player.location_lng = req['location_lng']
        player.location_updated_at = timezone.now()
        player.save()
