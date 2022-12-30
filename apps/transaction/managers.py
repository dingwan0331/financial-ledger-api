from django.db.models       import Manager
from django.db              import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.util.exeptions import ForbiddenException, NotFoundException

class TransactionManager(Manager):
    def create(self, **kwargs):
        transaction_row = super().create( **kwargs )

        return transaction_row
        
    def update(self, **kwarg):
        try:
            with transaction.atomic():
                deposit        = kwarg['deposit']
                title          = kwarg['title']
                description    = kwarg['description']
                user_id        = kwarg['user_id']
                transaction_id = kwarg['transaction_id']

                transaction_row = super().get(id = transaction_id)

                if transaction_row.user_id != user_id:
                    raise ForbiddenException()

                transaction_row.description = description
                transaction_row.title       = title
                transaction_row.deposi      = deposit 

            return transaction_row.save()
        except ObjectDoesNotExist:
            raise NotFoundException()
