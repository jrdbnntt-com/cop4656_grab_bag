from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from cop4656_grab_bag.admin import site_admin


class Player(models.Model):
    LOCATION_EXPIRATION_MINUTES = 10

    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    location_lat = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    location_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '[Player {}]'.format(self.user.username)

    def has_valid_location(self):
        """ Checks to see if the player has a location that has not expired """
        if self.location_updated_at is None:
            return False

        expire_time = self.location_updated_at + timedelta(minutes=self.LOCATION_EXPIRATION_MINUTES)
        return expire_time < timezone.now()


@admin.register(Player, site=site_admin)
class PlayerAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('id', 'user', 'location_lat', 'location_lng', 'location_updated_at', 'created')
    list_editable = ('location_lat', 'location_lng', 'location_updated_at')
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created',)
