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