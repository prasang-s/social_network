from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.encoding import force_str


class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail=None, status_code=500):
        if status_code is not None:
            self.status_code = status_code

        self.detail = force_str(detail) if detail else self.default_detail
