from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from cop4656_grab_bag.admin import site_admin


class Player(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return '[Player {} {}]'.format(self.user.first_name, self.user.last_name)


@admin.register(Player, site=site_admin)
class PlayerAdmin(admin.ModelAdmin):
    list_filter = None
    list_display = ('id', 'user_info', 'created')
    list_editable = None
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created',)

    @staticmethod
    def user_info(obj):
        return "{} {} - {}".format(obj.user.first_name, obj.user.last_name, obj.user.email)
