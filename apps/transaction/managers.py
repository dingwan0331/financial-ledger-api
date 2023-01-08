from datetime import datetime

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
                transaction_row.deposit     = deposit 
                transaction_row.updated_at  = datetime.now().timestamp()

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

    def get_from_self(self, transaction_id, user_id):
        try: 
            transaction_row = super().get(id = transaction_id)

            if transaction_row.user_id != user_id:
                raise PermissionError()            

            result = {
                    'id'          : transaction_row.id,
                    'deposit'     : transaction_row.deposit,
                    'title'       : transaction_row.title,
                    'description' : transaction_row.description,
                    'created_at'  : datetime.fromtimestamp(transaction_row.created_at),
                    'updated_at'  : datetime.fromtimestamp(transaction_row.updated_at)
            }
            
            return result

        except ObjectDoesNotExist:
            raise NotFoundException()

        
    def get(self, transaction_id):
        try: 
            transaction_row = super().get(id = transaction_id) 

            result = {
                    'id'          : transaction_row.id,
                    'deposit'     : transaction_row.deposit,
                    'title'       : transaction_row.title,
                    'description' : transaction_row.description,
                    'created_at'  : datetime.fromtimestamp(transaction_row.created_at),
                    'updated_at'  : datetime.fromtimestamp(transaction_row.updated_at)
            }
            
            return result

        except ObjectDoesNotExist:
            raise NotFoundException()

    def get_all(self, **kwargs):
        filter = kwargs['filter']
        order  = kwargs['order']
        offset = kwargs['offset']
        limit  = kwargs['limit']

        transaction_rows = super().filter(filter).order_by(order)[offset: offset+limit]

        result = [
            {
                'id'          : transaction_row.id,
                'deposit'     : transaction_row.deposit,
                'title'       : transaction_row.title,
                'created_at'  : datetime.fromtimestamp(transaction_row.created_at)
            } for transaction_row in transaction_rows
        ]

        return result