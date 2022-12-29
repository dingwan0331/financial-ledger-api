import json

import bcrypt

from django.views import View
from django.http  import JsonResponse

from .models import User

class UserView(View):
    def post(self, request):
        body     = json.loads(request.body)
        email    = body['email']
        password = body['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User.objects.create(email=email, password=hashed_password)
        
        return JsonResponse({'message' : 'Created'}, status = 201)