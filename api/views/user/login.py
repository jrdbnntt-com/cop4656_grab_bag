"""
    Logs user with the given credentials in for the stored session
"""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl


def log_user_in(request, username, password):
    """ Authenticate user """

    user = authenticate(
        username=username,
        password=password
    )
    if user is None:
        raise ValidationError(_('Invalid email or password'))
    login(request, user)


class RequestForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(min_length=8, max_length=1000)


class LogInView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_deny=[acl.groups.USER])

    def work(self, request, req, res):
        log_user_in(request=request, username=req['username'].lower(), password=req['password'])

