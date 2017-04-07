"""
    Simple GET test
"""

from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util.forms import JsonField


class ResponseForm(forms.Form):
    some_boolean = forms.BooleanField()
    some_integer = forms.IntegerField()
    some_string = forms.CharField()
    some_json = JsonField()


class SimpleGetTestView(ApiView):
    http_method_names = ['get']
    response_form_class = ResponseForm

    def work(self, request, req, res):
        res['some_boolean'] = True
        res['some_integer'] = 42
        res['some_string'] = "Hello world!"
        res['some_json'] = [
            "I",
            "am",
            "an",
            "array!"
        ]
