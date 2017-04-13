"""
    User account registration. Creates basic user account
"""
from django import forms
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.core.exceptions import ValidationError
from jrdbnntt_com.views.generic import ApiView
from api.views.user.login import log_user_in
from api.models import Player
from jrdbnntt_com.util import acl


class RequestForm(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(min_length=8, max_length=1000)


class ResponseForm(forms.Form):
    logged_in = forms.BooleanField(required=False)


class RegisterView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_deny=[acl.groups.USER])

    def work(self, request: HttpRequest, req: dict, res: dict):
        # Clean fields
        req['email'] = req['email'].lower()
        req['first_name'] = req['first_name'].lower().capitalize()
        req['last_name'] = req['last_name'].lower().capitalize()

        # Check if username already in use
        if User.objects.filter(username=req['username']).exists():
            raise ValidationError('Email already in use', params=['email'])

        # Attempt to create new user
        user = User.objects.create_user(
            username=req['username'],
            email=req['email'],
            password=req['password']
        )
        user.first_name = req['first_name']
        user.last_name = req['last_name']
        user.save()

        # Create respective Player
        Player.objects.create(user=user)

        # Log user in
        try:
            log_user_in(request=request, username=req['username'], password=req['password'])
            res['logged_in'] = True
        except ValidationError:
            res['logged_in'] = False
