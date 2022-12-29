from django.db.models import Manager
from django.db        import transaction

class TransactionManager(Manager):
    def create(self, **kwargs):
        transaction_row = super().create( **kwargs )

        return transaction_row