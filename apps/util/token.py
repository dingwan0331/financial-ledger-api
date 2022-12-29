import jwt

from datetime import datetime, timedelta

from config.env import SECRET_KEY, REFRESH_TOKEN_SECRET_KEY

class Token:
    def __init__(self):
        self.EXPIRES = {
            'access_token' : timedelta(hours = 1), 
            'refresh_token' : timedelta(hours = 8)
            }
        self.SECRET_KEYS = {
            'access_token' : SECRET_KEY , 
            'refresh_token' : REFRESH_TOKEN_SECRET_KEY
            }
        
    def sign_token(self, user_id, type):
        expire     = datetime.utcnow() + self.EXPIRES[type]
        payload    = {"id" : user_id, "exp" : expire }
        SECRET_KEY = self.SECRET_KEYS[type]

        token = jwt.encode(payload, SECRET_KEY)

        return token

import jwt

from datetime import datetime, timedelta

from django.core.cache import cache

from config.env          import SECRET_KEY, REFRESH_TOKEN_SECRET_KEY
from apps.util.exeptions import UnauthorizedException

class Token:
    def __init__(self):
        self.EXPIRES = {
            'access_token' : timedelta(hours = 1), 
            'refresh_token' : timedelta(hours = 8)
            }
        self.SECRET_KEYS = {
            'access_token' : SECRET_KEY , 
            'refresh_token' : REFRESH_TOKEN_SECRET_KEY
            }
        
    def sign_token(self, user_id, type):
        expire     = datetime.utcnow() + self.EXPIRES[type]
        payload    = {"id" : user_id, "exp" : expire }
        SECRET_KEY = self.SECRET_KEYS[type]

        token = jwt.encode(payload, SECRET_KEY)

        return token

    def decode_token(self,token, type):
        try: 
            return jwt.decode(token, self.SECRET_KEYS[type], 'HS256')

        except jwt.exceptions.DecodeError:
            raise UnauthorizedException('Invalid token')

        except jwt.exceptions.ExpiredSignatureError:
            raise UnauthorizedException('Expired token')

def verify_token(func):
    def wrapper(self,request,*args,**kwargs):
        try:
            access_token = request.headers.get("Authorization")
            payload = Token().decode_token(access_token, 'access_token')

            refresh_token = cache.get(access_token)

            if refresh_token == 'logout':
                raise UnauthorizedException('Invalid token')
            
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            raise UnauthorizedException('Invalid token')

        except jwt.exceptions.ExpiredSignatureError:
            raise UnauthorizedException('Expired token')
            
    return wrapper