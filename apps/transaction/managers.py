from django.db.models import Manager
from django.db        import transaction

class TransactionManager(Manager):
    def create(self, deposit, title, description, user_id):
        with transaction.atomic():
            last_transaction = super().filter(user_id = user_id).last()

            if not last_transaction:
                balance = 0
            else:
                balance = last_transaction.balance - int(deposit)

            transaction_row = super().create(
                balance     = balance,
                deposit     = deposit,
                title       = title,
                description = description,
                user_id     = user_id
                )
        return transaction_row