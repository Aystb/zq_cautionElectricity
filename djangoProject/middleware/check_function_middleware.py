from django.http import HttpResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from jwt_auth import jwt_auth
from datetime import datetime


class CheckFunctionMiddleware(MiddlewareMixin):
    EXCLUDED_FUNCTIONS = ['login', 'getJwtToken', 'getToken', 'userIndex', 'sign_up', 'login_nameAndPassword']

    def process_request(self, request):
        path = request.path
        match = resolve(path)
        request_name = match.func.__name__
        if request_name not in self.EXCLUDED_FUNCTIONS:
            jwtToken = request.META['HTTP_JWTTOKEN']
            print("this func is not in the middleware dict")
            res = jwt_auth.identify_token(jwtToken)
            if not res:
                return HttpResponse("TOKEN ERROR")
            # 做一次时间验证保险
            jwtTime = datetime.fromtimestamp(res['exp'])
            nowTime = datetime.now()
            if (jwtTime <= nowTime):
                return HttpResponse("TOKEN IS OUT OF DATE")
