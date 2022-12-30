import uuid

from django.views     import View
from django.http      import JsonResponse

from django_redis import get_redis_connection

from apps.util.token         import verify_token
from apps.util.exeptions     import NotFoundException
from apps.transaction.models import Transaction

redis = get_redis_connection('signed_url')

class TransactionSignedUrlView(View):
    @verify_token
    def get(self, request, transaction_id):
        user_id = request.user['id']
        
        Transaction.objects.get_from_self(transaction_id, user_id)
        
        uuid_path = uuid.uuid4()

        signed_url   = f'/urls/transactions/{uuid_path}'
        redirect_url = f'/transactions/{transaction_id}'
        REDIS_EXPIRE = 3600

        redis.set(signed_url, redirect_url, REDIS_EXPIRE)

        return JsonResponse({'signed_url' : signed_url}, status = 200)

class TransactionRedirectView(View):
    @verify_token
    def get(self, request, transaction_uuid):
        origin_url = redis.get(f'/urls/transactions/{transaction_uuid}').decode('utf-8')
        
        if not origin_url:
            raise NotFoundException()
        
        transaction_id = origin_url.replace('/transactions/','')

        transaction_row = Transaction.objects.get(transaction_id)
        

        return JsonResponse({'transaction' : transaction_row}, status = 200)