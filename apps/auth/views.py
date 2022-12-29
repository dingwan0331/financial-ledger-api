import json

import bcrypt

from django.views      import View
from django.http       import JsonResponse, HttpResponse
from django.core.cache import cache

from .models           import User
from ..util.validators import validate_email, validate_password
from ..util.exeptions  import UnauthorizedException
from ..util.token      import Token, verify_token

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

class LogOutView(View):
    @verify_token
    def post(self, request):
        access_token = request.headers.get("Authorization")

        cache.set(access_token, 'logout')
        
        return HttpResponse(status = 204)

class TokenView(View):
    def get(self, request):
        access_token  = request.headers.get("Authorization")
        refresh_token = cache.get(access_token)

        if refresh_token == 'logout':
            raise UnauthorizedException('Invalid token')

        token   = Token()
        payload = token.decode_token(refresh_token, 'refresh_token')
        user_id = payload['id']

        new_access_token = token.sign_token(user_id, 'access_token')    
        new_expire       = cache.ttl(access_token)

        cache.set(access_token, new_access_token, new_expire)
        cache.delete(access_token)
        
        return HttpResponse(headers={'Authorization' : new_access_token}, status = 204)