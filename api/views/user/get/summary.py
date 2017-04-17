"""
    Get basic user information
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView


class ResponseForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()


class SummaryView(ApiView):
    http_method_names = ['get']
    response_form_class = ResponseForm

    def work(self, request, req, res):
        if request.user.is_authenticated:
            res['username'] = request.user.username
            res['first_name'] = request.user.first_name
            res['last_name'] = request.user.last_name

