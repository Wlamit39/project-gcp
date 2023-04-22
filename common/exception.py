from __future__ import print_function
import copy
import json

from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR, HTTP_429_TOO_MANY_REQUESTS)
from common.error_codes import UNEXPECTED_ERROR

class ProjectResponseBaseException(Exception):
    def __init__(self):
        self._before_raising()

    def get_response(self):
        error = self.get_error()
        status = self.get_status_code()
        message = self.get_message()
        if isinstance(error, dict) and message:
            error['message'] = message

        return Response(data=error, status=status)

    def get_message(self):
        # default value of message is empty string so if there is empty string then set it None
        return copy.copy(getattr(self, 'message', None) or None)

    def get_error(self):
        return copy.copy(getattr(self, 'error', None) or UNEXPECTED_ERROR)

    def get_status_code(self):
        return copy.copy(
            getattr(self, 'status_code', None) or HTTP_400_BAD_REQUEST)

    def _before_raising(self):
        before_raising_func = getattr(self, 'before_raising', None)
        if callable(before_raising_func):
            try:
                before_raising_func(self)
            except Exception as e:
                print(e)

class MissingFieldException(ProjectResponseBaseException):
    def __init__(self, field_name=None, message=None, error=None):
        if error:
            self.message = error.get('message')
            self.error = error.get('error')
        elif message:
            self.message = message
        elif not field_name:
            self.message = "One or more fields are missing"
        else:
            self.message = "%s field is missing" % field_name
