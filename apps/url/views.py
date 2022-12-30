import uuid

from django.views import View
from django.http  import JsonResponse

from django_redis import get_redis_connection

from apps.util.token import verify_token

class TransactionSignedUrlView(View):
    @verify_token
    def get(self, request, transaction_id):
        redis     = get_redis_connection('signed_url')
        uuid_path = uuid.uuid4()

        signed_url   = f'/transactions/{uuid_path}'
        redirect_url = f'/transactions/{transaction_id}'
        REDIS_EXPIRE = 3600

        redis.set(signed_url, redirect_url, REDIS_EXPIRE)

        return JsonResponse({'signed_url' : signed_url}, status = 200)
