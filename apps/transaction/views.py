from datetime import datetime

from django.views import View
from django.http  import JsonResponse, HttpResponse

from apps.transaction.models import Transaction
from apps.transaction.dtos   import PostTransactionsDto, PatchTransactionsDto
from apps.util.token         import verify_token

class TransactionsView(View):
    @verify_token
    def post(self, request):
        dto = PostTransactionsDto(request.body)
        
        deposit     = dto.deposit
        title       = dto.title
        description = dto.description

        user_id = request.user['id']
        
        transaction_row = Transaction.objects.create(
            deposit     = deposit,
            title       = title,
            description = description,
            user_id     = user_id
        )

        transaction_id = transaction_row.id

        location = f'/transactions/{transaction_id}'

        return JsonResponse(
            {'message' : 'Created'},status = 201, headers = {'Location' : location}
            )

class TransactionView(View):
    @verify_token
    def patch(self, request, transaction_id):
        dto = PatchTransactionsDto(request.body)

        deposit     = dto.deposit
        title       = dto.title
        description = dto.description

        user_id = request.user['id']

        transaction_row = Transaction.objects.update(
            transaction_id = transaction_id,
            deposit        = deposit,
            title          = title,
            description    = description,
            user_id        = user_id
        )

        return HttpResponse(status = 204)

    @verify_token
    def delete(self, request, transaction_id):
        user_id = request.user['id']

        transaction_row = Transaction.objects.delete(
            transaction_id = transaction_id,
            user_id        = user_id
        )

        return HttpResponse(status = 204)

    @verify_token
    def get(self, request, transaction_id):

        transaction_row = Transaction.objects.get(transaction_id)

        result = {
                'id'          : transaction_row.id,
                'deposit'     : transaction_row.deposit,
                'title'       : transaction_row.title,
                'description' : transaction_row.description,
                'created_at'  : datetime.fromtimestamp(transaction_row.created_at),
                'updated_at'  : datetime.fromtimestamp(transaction_row.updated_at)
        }

        return JsonResponse({'transaction' : result}, status = 200)