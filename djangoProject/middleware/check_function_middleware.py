from django.http import HttpResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

from jwt_auth import jwt_auth


class CheckFunctionMiddleware(MiddlewareMixin):
    EXCLUDED_FUNCTIONS = ['login', 'getJwtToken', 'getToken']

    def process_request(self, request):
        jwtToken = request.META['HTTP_JWTTOKEN']
        path = request.path
        match = resolve(path)
        request_name = match.func.__name__

        if request_name not in self.EXCLUDED_FUNCTIONS:
            print("this func is not in the middleware dict")
            jwt_auth.identify_token(jwtToken)
