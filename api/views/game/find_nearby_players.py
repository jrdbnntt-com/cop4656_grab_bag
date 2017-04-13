"""
    Update location & retrieve nearby players for map
"""


from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import PlayerInstance, Game, Player
from django.core.exceptions import ValidationError
from django.utils import timezone
from jrdbnntt_com.util.forms import JsonField
from api.util import location


class RequestForm(forms.Form):
    game_id = forms.IntegerField()
    location_lat = forms.DecimalField(max_digits=10, decimal_places=6)
    location_lng = forms.DecimalField(max_digits=10, decimal_places=6)


class ResponseForm(forms.Form):
    pis_in_steal_range = JsonField()
    pis_in_view_range = JsonField()


class FindNearbyPlayersView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        # Get the game
        game = Game.objects.filter(id=req['game_id']).all()
        if len(game) == 0:
            raise ValidationError('Invalid game_id')
        game = game[0]
        if game.status != Game.Status.ACTIVE:
            raise ValidationError('Game not active')

        # Get player & update location
        player = Player.objects.get(game=game, user=request.user)
        player.location_lat = req['location_lat']
        player.location_lng = req['location_lng']
        player.location_updated_at = timezone.now()
        player.save()

        # Make sure player is in game
        if not PlayerInstance.objects.filter(game=game, player=player).exists():
            raise ValidationError('Invalid game, not a player in it')

        mvd = game.max_view_distance_in_meters()
        msd = game.maximum_steal_distance_in_meters

        # Only pull nearby players from database, then check each more precisely
        spread = location.CardinalSpread(
            origin_lat=float(player.location_lat), origin_lng=float(player.location_lng), radius_in_meters=float(mvd)
        )
        nearby_pis = PlayerInstance.objects.filter(
            game=game,
            player__location_lat__lt=spread.north.lat,
            player__location_lat__gt=spread.south.lat,
            player__location_lng__lt=spread.east.lng,
            player__location_lng__gt=spread.west.lng
        ).all()

        pis_in_steal_range = []
        pis_in_view_range = []
        for pi_obj in nearby_pis:
            if not pi_obj.player.has_valid_location():
                continue

            dist = location.distance_in_meters(player, pi_obj.player)
            if dist > mvd:
                continue

            pi = {
                'distance_in_meters': round(dist, 3),
                'game_id': pi_obj.game.id,
                'player_instance_id': pi_obj.id,
                'username': pi_obj.player.user.username,
                'location_lat': float(pi_obj.player.location_lat),
                'location_lng': float(pi_obj.player.location_lng)
            }

            if dist <= msd:
                pis_in_steal_range.append(pi)
            else:
                pis_in_view_range.append(pi)

        res['pis_in_steal_range'] = pis_in_steal_range
        res['pis_in_view_range'] = pis_in_view_range
