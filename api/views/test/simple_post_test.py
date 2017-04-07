"""
    Simple POST test
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView


class RequestForm(forms.Form):
    some_integer = forms.IntegerField(min_value=0, max_value=100)


class ResponseForm(forms.Form):
    some_message = forms.CharField()


class SimplePostTestView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm

    def work(self, request, req, res):
        res['some_message'] = "You entered " + str(req['some_integer'])
