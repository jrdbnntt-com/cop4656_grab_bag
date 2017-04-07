"""
    Basic exception with custom utility functions
"""

from django.http import JsonResponse
from django.utils.translation import ugettext as _
import logging
import traceback


def get_admin_email_recipients() -> list:
    recipients = list()
    recipients.append({
        'email'
    })
    return recipients


def email_log_html(title: str, code: str) -> str:
    return '<h2><b>{}</b></h2><p style="font-family: Courier">{}</p><br>'.format(
        title, code
    )


class BaseError(Exception):
    response_status = 500

    def __init__(self, source_exception: Exception):
        if source_exception is not None:
            if not isinstance(source_exception, Exception):
                raise TypeError('Invalid source_exception. Must be an Exception')
            self.message = str(source_exception)
        else:
            source_exception = Exception()

        self.cause = source_exception
        self.message = str(source_exception)
        self.stack_trace = traceback.format_exc()

    def email_log_to_dev(self, request_info: str, user=None):
        pass

    def log(self):
        logging.error(self.__class__.__name__, exc_info=True, )

    def json_response(self, include_message=True) -> JsonResponse:
        response = self.to_dict()

        if not include_message:
            del response['message']

        return JsonResponse(response, status=self.response_status)

    def to_dict(self):
        return {
            'error': _(self.__class__.__name__),
            'cause': _(self.cause.__class__.__name__),
            'message': self.message
        }

    def __str__(self):
        return str(self.to_dict())
