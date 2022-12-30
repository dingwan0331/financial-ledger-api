import json

import bcrypt

from django.views      import View
from django.http       import JsonResponse, HttpResponse
from django.core.cache import cache

from apps.auth.models     import User
from apps.util.exeptions  import UnauthorizedException, BadRequestException
from apps.util.token      import Token, verify_token
from apps.auth.dtos       import PostUsersDto, SignInDto

class UserView(View):
    def post(self, request):
        dto      = PostUsersDto(request.body)
        password = dto.password

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User.objects.create(email = dto.email, password = hashed_password)

        user_id  = user.id
        location = f'/users/{user_id}'
        
        return JsonResponse(
            {'message' : 'Created'}, status = 201, headers = {'Location' : location}
            )

class SignInView(View):
    def post(self, request):
        dto = SignInDto(request.body)

        user = User.objects.get_by_email(dto.email)

        if not bcrypt.checkpw(dto.password.encode('utf-8'), user.password):
            raise BadRequestException('Invalid password')

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