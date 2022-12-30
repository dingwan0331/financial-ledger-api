from django.views import View
from django.http  import JsonResponse, HttpResponse

from apps.transaction.models import Transaction
from apps.transaction.dtos   import (
    PostTransactionsDto, 
    PatchTransactionDto, 
    GetTransactionsDto
    )
from apps.util.token import verify_token

class TransactionsView(View):
    @verify_token
    def post(self, request):
        dto = PostTransactionsDto(request.body)

        user_id = request.user['id']
        
        transaction_row = Transaction.objects.create(
            deposit     = dto.deposit,
            title       = dto.title,
            description = dto.description,
            user_id     = user_id
        )

        transaction_id = transaction_row.id

        location = f'/transactions/{transaction_id}'

        return JsonResponse(
            {'message' : 'Created'},status = 201, headers = {'Location' : location}
            )

    @verify_token
    def get(self, request):
        user_id = request.user['id']
        dto = GetTransactionsDto(request.GET, user_id)

        transaction_rows = Transaction.objects.get_all(
            offset = dto.offset,
            limit  = dto.limit,
            order  = dto.order,
            filter = dto.filter
        )

        return JsonResponse({'trsnactions' : transaction_rows}, status = 200)

class TransactionView(View):
    @verify_token
    def patch(self, request, transaction_id):
        dto = PatchTransactionDto(request.body)
        
        user_id = request.user['id']

        transaction_row = Transaction.objects.update(
            deposit        = dto.deposit,
            title          = dto.title,
            description    = dto.description,
            user_id        = user_id,
            transaction_id = transaction_id
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
        user_id = request.user['id']

        transaction_row = Transaction.objects.get_from_self(transaction_id, user_id)

        return JsonResponse({'transaction' : transaction_row}, status = 200)