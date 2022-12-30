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

    def delete(self, user_id, transaction_id):
        try:
            with transaction.atomic():
                transaction_row = super().get(id = transaction_id)

                if transaction_row.user_id != user_id:
                    raise ForbiddenException()

            return transaction_row.delete()
        except ObjectDoesNotExist:
            raise NotFoundException()

    def get(self, transaction_id):
        try:
            return super().get(id = transaction_id)

        except ObjectDoesNotExist:
            raise NotFoundException()

    def get_all(self, **kwargs):
        filter = kwargs['filter']
        order  = kwargs['order']
        offset = kwargs['offset']
        limit  = kwargs['limit']

        return super().filter(filter).order_by(order)[offset: offset+limit]