"""
    Logs the user out if the session has a logged in user
"""

from django.contrib.auth import logout
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl


class LogOutView(ApiView):
    http_method_names = ['post', 'get']
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req, res):
        logout(request=request)

