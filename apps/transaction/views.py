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
        dto            = PatchTransactionsDto(request.body)

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