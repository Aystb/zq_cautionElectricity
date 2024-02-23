import jwt
import datetime

from django.http import HttpResponse

import djangoProject.settings

def create_jwtToken(openid):
    expire_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }

    payload = {
        'openid': openid,
        "exp": expire_time
    }
    result = jwt.encode(payload=payload, key=djangoProject.settings.SECRET_KEY, algorithm='HS256', headers=headers)
    return result


def identify_token(token):
    try:
        verified_payload = jwt.decode(token, key=djangoProject.settings.SECRET_KEY, algorithms="HS256")
        return verified_payload
    except jwt.ExpiredSignatureError:
        print('token已失效')
        return False
    except jwt.DecodeError:
        print('token认证失败')
        return False
    except jwt.InvalidTokenError:
        print('非法的token')
        return False
