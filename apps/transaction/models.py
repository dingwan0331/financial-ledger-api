from django.db import models

from apps.util.models          import TimeStampModel
from apps.transaction.managers import TransactionManager

class Transaction(TimeStampModel):
    deposit          = models.BigIntegerField()
    title            = models.CharField(max_length = 20)
    description      = models.CharField(max_length = 100)
    user             = models.ForeignKey('auth.User', on_delete = models.CASCADE)

    objects = TransactionManager()

    class Meta():
        db_table = 'transactions'