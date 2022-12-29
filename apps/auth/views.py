import json

import bcrypt

from django.views      import View
from django.http       import JsonResponse, HttpResponse
from django.core.cache import cache

from .models           import User
from ..util.validators import validate_email, validate_password
from ..util.exeptions  import UnauthorizedException
from ..util.token      import Token

class UserView(View):
    def post(self, request):
        body     = json.loads(request.body)
        email    = body['email']
        password = body['password']

        validate_email(email)
        validate_password(password)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User.objects.create(email=email, password=hashed_password)
        
        return JsonResponse({'message' : 'Created'}, status = 201)

class SignInView(View):
    def post(self, request):
        body     = json.loads(request.body)
        email    = body['email']
        password = body['password']

        validate_email(email)

        user = User.objects.get_by_email(email)

        if not bcrypt.checkpw(password.encode('utf-8'), user.password):
            raise UnauthorizedException('Invalid password')

        token = Token()

        access_token = token.sign_token(user.id, 'access_token')
        refresh_token = token.sign_token(user.id, 'refresh_token')

        redis_expire = token.EXPIRES['refresh_token'].total_seconds()

        cache.set(access_token, refresh_token, redis_expire)

        return HttpResponse(headers={'Authorization' : access_token}, status = 204)